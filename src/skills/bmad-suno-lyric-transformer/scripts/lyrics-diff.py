# /// script
# requires-python = ">=3.9"
# ///
"""Produce structured diff between original and transformed lyrics.

Compares two versions of lyrics and categorizes changes by type (added,
removed, modified) and tracks which sections they fall in.

Usage:
    python lyrics-diff.py --original orig.txt --transformed trans.txt [options]

    # Compare two files
    python lyrics-diff.py --original orig.txt --transformed trans.txt

    # Compare two text strings
    python lyrics-diff.py --original-text "old lyrics" --transformed-text "new lyrics"

    # Output to file
    python lyrics-diff.py --original orig.txt --transformed trans.txt -o diff.json
"""

import argparse
import difflib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_NAME = "lyrics-diff"
VERSION = "1.0.0"


def get_section_at_line(lines: list[str], line_idx: int) -> str:
    """Determine which section a given line index falls in."""
    current_section = "(no section)"
    for i in range(line_idx + 1):
        if i < len(lines):
            stripped = lines[i].strip()
            tag_match = re.match(r'^\[([^\]:]+)\]$', stripped)
            if tag_match:
                current_section = tag_match.group(1).strip()
    return current_section


def compute_diff(original: str, transformed: str) -> dict:
    """Compute structured diff between original and transformed lyrics."""
    orig_lines = original.split('\n')
    trans_lines = transformed.split('\n')

    matcher = difflib.SequenceMatcher(None, orig_lines, trans_lines)
    changes = []
    sections_affected = set()

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            continue
        elif tag == 'replace':
            # Modified lines
            max_len = max(i2 - i1, j2 - j1)
            for k in range(max_len):
                orig_idx = i1 + k if k < (i2 - i1) else None
                trans_idx = j1 + k if k < (j2 - j1) else None

                if orig_idx is not None and trans_idx is not None:
                    section = get_section_at_line(orig_lines, orig_idx)
                    sections_affected.add(section)
                    changes.append({
                        "type": "modified",
                        "section": section,
                        "line": orig_idx + 1,
                        "original": orig_lines[orig_idx],
                        "transformed": trans_lines[trans_idx]
                    })
                elif orig_idx is not None:
                    section = get_section_at_line(orig_lines, orig_idx)
                    sections_affected.add(section)
                    changes.append({
                        "type": "removed",
                        "section": section,
                        "line": orig_idx + 1,
                        "original": orig_lines[orig_idx],
                        "transformed": ""
                    })
                elif trans_idx is not None:
                    section = get_section_at_line(trans_lines, trans_idx)
                    sections_affected.add(section)
                    changes.append({
                        "type": "added",
                        "section": section,
                        "line": trans_idx + 1,
                        "original": "",
                        "transformed": trans_lines[trans_idx]
                    })
        elif tag == 'delete':
            for k in range(i1, i2):
                section = get_section_at_line(orig_lines, k)
                sections_affected.add(section)
                changes.append({
                    "type": "removed",
                    "section": section,
                    "line": k + 1,
                    "original": orig_lines[k],
                    "transformed": ""
                })
        elif tag == 'insert':
            for k in range(j1, j2):
                section = get_section_at_line(trans_lines, k)
                sections_affected.add(section)
                changes.append({
                    "type": "added",
                    "section": section,
                    "line": k + 1,
                    "original": "",
                    "transformed": trans_lines[k]
                })

    # Generate unified diff for human-readable output
    unified = list(difflib.unified_diff(
        orig_lines, trans_lines,
        fromfile="original", tofile="transformed",
        lineterm=""
    ))

    summary = {
        "lines_added": sum(1 for c in changes if c["type"] == "added"),
        "lines_removed": sum(1 for c in changes if c["type"] == "removed"),
        "lines_modified": sum(1 for c in changes if c["type"] == "modified"),
        "sections_affected": sorted(sections_affected)
    }

    return {
        "changes": changes,
        "unified_diff": "\n".join(unified),
        "summary": summary
    }


def build_report(result: dict, skill_path: str = "") -> dict:
    """Build the standard output report."""
    total_changes = len(result["changes"])

    status = "pass"
    if total_changes == 0:
        status = "pass"
    else:
        status = "info"

    findings = []
    if total_changes == 0:
        findings.append({
            "severity": "info",
            "category": "diff",
            "issue": "No differences found between original and transformed lyrics.",
            "fix": "Lyrics are identical."
        })

    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        severity_counts[f["severity"]] = severity_counts.get(f["severity"], 0) + 1

    return {
        "script": SCRIPT_NAME,
        "version": VERSION,
        "skill_path": skill_path,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "changes": result["changes"],
        "unified_diff": result["unified_diff"],
        "summary": result["summary"],
        "findings": findings,
        "finding_counts": {
            "total": len(findings),
            **severity_counts
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Produce structured diff between original and transformed lyrics.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --original orig.txt --transformed trans.txt
  %(prog)s --original-text "old lyrics" --transformed-text "new lyrics"
  %(prog)s --original orig.txt --transformed trans.txt -o diff.json --verbose

Exit codes: 0=pass, 1=differences found, 2=error
        """
    )
    parser.add_argument("file", nargs="?", help="Unused (for pattern consistency)")
    parser.add_argument("--original", help="Path to original lyrics file")
    parser.add_argument("--transformed", help="Path to transformed lyrics file")
    parser.add_argument("--original-text", help="Original lyrics text directly")
    parser.add_argument("--transformed-text", help="Transformed lyrics text directly")
    parser.add_argument("--text", help="Unused (for pattern consistency)")
    parser.add_argument("--stdin", action="store_true", help="Unused (for pattern consistency)")
    parser.add_argument("-o", "--output", help="Output file path (defaults to stdout)")
    parser.add_argument("--verbose", action="store_true", help="Print diagnostics to stderr")
    parser.add_argument("--skill-path", default="", help="Skill path for report context")

    args = parser.parse_args()

    original = ""
    transformed = ""

    if args.original_text and args.transformed_text:
        original = args.original_text.replace('\\n', '\n')
        transformed = args.transformed_text.replace('\\n', '\n')
    elif args.original and args.transformed:
        orig_path = Path(args.original)
        trans_path = Path(args.transformed)
        if not orig_path.exists():
            print(f"Error: File not found: {args.original}", file=sys.stderr)
            sys.exit(2)
        if not trans_path.exists():
            print(f"Error: File not found: {args.transformed}", file=sys.stderr)
            sys.exit(2)
        original = orig_path.read_text()
        transformed = trans_path.read_text()
    else:
        print("Error: Provide --original and --transformed files, or --original-text and --transformed-text.", file=sys.stderr)
        parser.print_help()
        sys.exit(2)

    if args.verbose:
        print(f"Comparing lyrics (original: {len(original)} chars, transformed: {len(transformed)} chars)...", file=sys.stderr)

    result = compute_diff(original, transformed)
    report = build_report(result, args.skill_path)

    output_json = json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(output_json)
        if args.verbose:
            print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(output_json)

    sys.exit(0 if len(result["changes"]) == 0 else 1)


if __name__ == "__main__":
    main()
