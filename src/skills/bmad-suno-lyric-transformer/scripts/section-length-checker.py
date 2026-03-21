# /// script
# requires-python = ">=3.9"
# ///
"""Check section content lengths against expected ranges from the section-jobs framework.

Parses lyrics by metatag headers and validates that each section falls within
recommended line count ranges for Suno compatibility.

Usage:
    python section-length-checker.py <lyrics-file> [options]

    # Check section lengths in a file
    python section-length-checker.py lyrics.txt

    # Check from text argument
    python section-length-checker.py --text "[Verse 1]\\nLine one\\nLine two"

    # Output to file
    python section-length-checker.py lyrics.txt -o results.json
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_NAME = "section-length-checker"
VERSION = "1.0.0"

# Expected line count ranges per section type (min, max)
SECTION_RANGES = {
    "intro": (0, 4),
    "verse": (4, 8),
    "pre-chorus": (2, 4),
    "chorus": (2, 6),
    "bridge": (2, 6),
    "breakdown": (2, 4),
    "build-up": (2, 4),
    "outro": (2, 6),
    "hook": (1, 4),
    "refrain": (2, 6),
    "interlude": (0, 4),
    "post-chorus": (2, 4),
    "solo": (0, 2),
    "guitar solo": (0, 2),
    "piano solo": (0, 2),
    "sax solo": (0, 2),
    "saxophone solo": (0, 2),
    "drum solo": (0, 2),
    "bass solo": (0, 2),
    "instrumental": (0, 4),
    "build": (2, 4),
    "drop": (0, 4),
    "break": (0, 4),
    "end": (0, 4),
    "fade out": (0, 4),
    "fade in": (0, 4),
}


def normalize_section_name(tag: str) -> str:
    """Normalize section tag to base name: 'Verse 1' -> 'verse', 'Final Chorus' -> 'chorus'."""
    tag_lower = tag.lower().strip()
    # Strip trailing numbers
    tag_lower = re.sub(r'\s*\d+$', '', tag_lower)
    # Handle "final chorus" -> "chorus"
    tag_lower = re.sub(r'^final\s+', '', tag_lower)
    return tag_lower.strip()


def parse_sections(text: str) -> list[dict]:
    """Parse lyrics into sections with line counts."""
    lines = text.split('\n')
    sections = []
    current_section = None

    for line in lines:
        stripped = line.strip()

        # Check for section metatag
        tag_match = re.match(r'^\[([^\]:]+)\]$', stripped)
        if tag_match:
            tag_content = tag_match.group(1).strip()
            # Skip descriptor metatags (contain colon)
            if ':' in tag_content:
                continue
            # Save previous section
            if current_section is not None:
                sections.append(current_section)
            current_section = {
                "tag": tag_content,
                "base_name": normalize_section_name(tag_content),
                "lyric_lines": []
            }
            continue

        # Check for descriptor metatags like [Energy: slow] — don't count as content
        descriptor_match = re.match(r'^\[[^\]]*:[^\]]*\]$', stripped)
        if descriptor_match:
            continue

        # Non-empty, non-tag line goes into current section
        if stripped and current_section is not None:
            current_section["lyric_lines"].append(stripped)

    # Don't forget last section
    if current_section is not None:
        sections.append(current_section)

    return sections


# Genres that get relaxed section length constraints
PROG_GENRES = {"prog", "metal", "progressive", "experimental"}


def check_sections(text: str, genre: str = "") -> dict:
    """Check section lengths against expected ranges."""
    sections = parse_sections(text)
    findings = []
    section_results = []
    is_prog = genre.lower() in PROG_GENRES if genre else False

    for section in sections:
        line_count = len(section["lyric_lines"])
        base = section["base_name"]
        expected = SECTION_RANGES.get(base)
        # In prog/metal mode, double the max for all sections
        if expected and is_prog:
            expected = (expected[0], expected[1] * 2)

        result = {
            "tag": section["tag"],
            "base_name": base,
            "line_count": line_count,
            "expected_range": list(expected) if expected else None,
            "status": "unknown"
        }

        if expected is None:
            result["status"] = "unknown"
            findings.append({
                "severity": "info",
                "category": "section-length",
                "location": {"section": section["tag"]},
                "issue": f"Section [{section['tag']}] has no defined expected range.",
                "fix": "This section type is not in the standard range database."
            })
        elif line_count < expected[0]:
            result["status"] = "short"
            findings.append({
                "severity": "medium",
                "category": "section-length",
                "location": {"section": section["tag"]},
                "issue": f"Section [{section['tag']}] is too short: {line_count} lines (expected {expected[0]}-{expected[1]}).",
                "fix": f"Add {expected[0] - line_count} more line(s) to reach the minimum of {expected[0]}."
            })
        elif line_count > expected[1]:
            result["status"] = "long"
            findings.append({
                "severity": "medium",
                "category": "section-length",
                "location": {"section": section["tag"]},
                "issue": f"Section [{section['tag']}] is too long: {line_count} lines (expected {expected[0]}-{expected[1]}).",
                "fix": f"Remove {line_count - expected[1]} line(s) to reach the maximum of {expected[1]}."
            })
        else:
            result["status"] = "pass"

        section_results.append(result)

    return {
        "sections": section_results,
        "findings": findings
    }


def build_report(result: dict, text: str, skill_path: str = "") -> dict:
    """Build the standard output report."""
    findings = result["findings"]

    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        severity_counts[f["severity"]] = severity_counts.get(f["severity"], 0) + 1

    passed = sum(1 for s in result["sections"] if s["status"] == "pass")
    failed = sum(1 for s in result["sections"] if s["status"] in ("short", "long"))

    status = "pass"
    if failed > 0:
        status = "warning"

    return {
        "script": SCRIPT_NAME,
        "version": VERSION,
        "skill_path": skill_path,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "metrics": {
            "total_sections": len(result["sections"]),
            "sections_pass": passed,
            "sections_fail": failed,
        },
        "sections": result["sections"],
        "findings": findings,
        "summary": {
            "total": len(findings),
            **severity_counts
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Check section content lengths against expected ranges.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s lyrics.txt
  %(prog)s --text "[Verse 1]\\nLine 1\\nLine 2\\nLine 3\\nLine 4"
  %(prog)s --stdin < lyrics.txt
  %(prog)s lyrics.txt -o results.json --verbose

Expected ranges (lines):
  Intro=0-4, Verse=4-8, Pre-Chorus=2-4, Chorus=2-6,
  Bridge=2-6, Breakdown=2-4, Build-Up=2-4, Outro=2-6,
  Hook=1-4, Refrain=2-6

Exit codes: 0=pass, 1=issues, 2=error
        """
    )
    parser.add_argument("file", nargs="?", help="Path to lyrics text file")
    parser.add_argument("--text", help="Lyrics text to check directly")
    parser.add_argument("--stdin", action="store_true", help="Read lyrics from stdin")
    parser.add_argument("-o", "--output", help="Output file path (defaults to stdout)")
    parser.add_argument("--verbose", action="store_true", help="Print diagnostics to stderr")
    parser.add_argument("--skill-path", default="", help="Skill path for report context")
    parser.add_argument("--genre", default="", help="Genre hint (prog, metal, progressive, experimental) to relax length constraints")

    args = parser.parse_args()

    text = ""
    if args.text:
        text = args.text.replace('\\n', '\n')
    elif args.stdin:
        text = sys.stdin.read()
    elif args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(2)
        text = file_path.read_text()
    else:
        parser.print_help()
        sys.exit(2)

    if args.verbose:
        print(f"Checking section lengths ({len(text.splitlines())} lines)...", file=sys.stderr)

    result = check_sections(text, genre=args.genre)
    report = build_report(result, text, args.skill_path)

    output_json = json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(output_json)
        if args.verbose:
            print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(output_json)

    sys.exit(0 if report["status"] == "pass" else 1)


if __name__ == "__main__":
    main()
