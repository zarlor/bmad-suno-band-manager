# /// script
# requires-python = ">=3.9"
# ///
"""Assemble Transformation Summary from validation, syllable, and cliche reports.

Collects outputs from validate-lyrics.py, syllable-counter.py, and cliche-detector.py
and assembles a formatted Transformation Summary markdown block.

Usage:
    python assemble-summary.py --validation val.json --syllables syl.json --cliches cli.json [options]

    # Assemble from three JSON files
    python assemble-summary.py --validation val.json --syllables syl.json --cliches cli.json

    # With transformation codes
    python assemble-summary.py --validation val.json --syllables syl.json --cliches cli.json --transformations "ST,CC,RA"

    # Output to file
    python assemble-summary.py --validation val.json --syllables syl.json --cliches cli.json -o summary.md
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_NAME = "assemble-summary"
VERSION = "1.0.0"

CODE_DESCRIPTIONS = {
    "ST": "Structural Transformation",
    "CE": "Cliche Elimination",
    "CC": "Consistency Check",
    "RA": "Rhyme Analysis",
    "FR": "Full Rewrite",
    "CD": "Cliche Detection",
    "WF": "Word Flow",
}

# Approximate duration: ~15 seconds per section on average
SECONDS_PER_SECTION = 15


def load_json_file(path: str) -> dict:
    """Load and parse a JSON file."""
    p = Path(path)
    if not p.exists():
        return {}
    return json.loads(p.read_text())


def assemble_summary(validation: dict, syllables: dict, cliches: dict,
                     transformations: list[str]) -> dict:
    """Assemble summary data from the three reports."""
    # Extract from validation report
    val_metrics = validation.get("metrics", {})
    section_count = val_metrics.get("section_count", 0)
    section_types = val_metrics.get("sections", [])
    val_status = validation.get("status", "unknown")
    lyric_lines = val_metrics.get("lyric_lines", 0)
    total_lines = val_metrics.get("total_lines", 0)

    # Estimate character count from validation raw data or total lines
    char_count = 0
    if "raw_text" in validation:
        char_count = len(validation["raw_text"])

    # Extract from syllable report
    syl_metrics = syllables.get("metrics", {})
    min_syl = syl_metrics.get("min_syllables", 0)
    max_syl = syl_metrics.get("max_syllables", 0)
    avg_syl = syl_metrics.get("average_syllables_per_line", 0)
    total_syl = syl_metrics.get("total_syllables", 0)

    # Extract from cliche report
    cli_metrics = cliches.get("metrics", {})
    total_cliches = cli_metrics.get("total_cliches_found", 0)
    cliche_categories = cli_metrics.get("categories", {})
    cli_status = cliches.get("status", "unknown")

    # Estimated duration
    estimated_duration_sec = section_count * SECONDS_PER_SECTION
    minutes = estimated_duration_sec // 60
    seconds = estimated_duration_sec % 60

    # Transformation descriptions
    trans_descriptions = [
        f"- {code}: {CODE_DESCRIPTIONS.get(code, code)}"
        for code in transformations
    ]

    return {
        "section_count": section_count,
        "section_types": section_types,
        "unique_section_types": sorted(set(
            s.split()[0] if ' ' in s else s for s in section_types
        )),
        "lyric_lines": lyric_lines,
        "total_lines": total_lines,
        "character_count": char_count,
        "syllable_range": f"{min_syl}-{max_syl}",
        "average_syllables": avg_syl,
        "total_syllables": total_syl,
        "estimated_duration": f"{minutes}:{seconds:02d}",
        "estimated_duration_sec": estimated_duration_sec,
        "total_cliches": total_cliches,
        "cliche_categories": cliche_categories,
        "cliche_status": cli_status,
        "validation_status": val_status,
        "transformations_applied": transformations,
        "transformation_descriptions": trans_descriptions,
    }


def format_markdown(data: dict) -> str:
    """Format the summary data as a markdown block."""
    lines = [
        "## Transformation Summary",
        "",
        f"**Validation Status:** {data['validation_status'].upper()}",
        f"**Sections:** {data['section_count']} ({', '.join(data['unique_section_types'])})",
        f"**Lyric Lines:** {data['lyric_lines']}",
        f"**Syllable Range:** {data['syllable_range']} (avg {data['average_syllables']})",
        f"**Estimated Duration:** ~{data['estimated_duration']}",
    ]

    if data['character_count'] > 0:
        lines.append(f"**Character Count:** {data['character_count']}")

    lines.append("")
    lines.append(f"**Cliche Detection:** {data['total_cliches']} found ({data['cliche_status']})")
    if data['cliche_categories']:
        for cat, count in sorted(data['cliche_categories'].items()):
            lines.append(f"  - {cat}: {count}")

    if data['transformations_applied']:
        lines.append("")
        lines.append("**Transformations Applied:**")
        for desc in data['transformation_descriptions']:
            lines.append(desc)

    lines.append("")
    return "\n".join(lines)


def build_report(data: dict, markdown: str, skill_path: str = "") -> dict:
    """Build the standard output report."""
    findings = []

    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}

    return {
        "script": SCRIPT_NAME,
        "version": VERSION,
        "skill_path": skill_path,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "pass",
        "metrics": data,
        "markdown": markdown,
        "findings": findings,
        "summary": {
            "total": 0,
            **severity_counts
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Assemble Transformation Summary from validation, syllable, and cliche reports.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --validation val.json --syllables syl.json --cliches cli.json
  %(prog)s --validation val.json --syllables syl.json --cliches cli.json --transformations "ST,CC,RA"
  %(prog)s --validation val.json --syllables syl.json --cliches cli.json -o summary.md --verbose

Exit codes: 0=pass, 1=issues, 2=error
        """
    )
    parser.add_argument("file", nargs="?", help="Unused (for pattern consistency)")
    parser.add_argument("--validation", required=True, help="Path to validate-lyrics.py JSON output")
    parser.add_argument("--syllables", required=True, help="Path to syllable-counter.py JSON output")
    parser.add_argument("--cliches", required=True, help="Path to cliche-detector.py JSON output")
    parser.add_argument("--transformations", default="", help="Comma-separated transformation codes applied")
    parser.add_argument("--text", help="Unused (for pattern consistency)")
    parser.add_argument("--stdin", action="store_true", help="Unused (for pattern consistency)")
    parser.add_argument("-o", "--output", help="Output file path (defaults to stdout)")
    parser.add_argument("--verbose", action="store_true", help="Print diagnostics to stderr")
    parser.add_argument("--skill-path", default="", help="Skill path for report context")

    args = parser.parse_args()

    # Load input files
    validation = load_json_file(args.validation)
    syllables_data = load_json_file(args.syllables)
    cliches_data = load_json_file(args.cliches)

    if not validation and not syllables_data and not cliches_data:
        print("Error: Could not load any input JSON files.", file=sys.stderr)
        sys.exit(2)

    transformations = [c.strip().upper() for c in args.transformations.split(",") if c.strip()] if args.transformations else []

    if args.verbose:
        print(f"Assembling summary (transformations: {transformations})...", file=sys.stderr)

    data = assemble_summary(validation, syllables_data, cliches_data, transformations)
    markdown = format_markdown(data)
    report = build_report(data, markdown, args.skill_path)

    # Decide output format
    if args.output:
        out_path = Path(args.output)
        if out_path.suffix == ".json":
            out_path.write_text(json.dumps(report, indent=2))
        else:
            out_path.write_text(markdown)
        if args.verbose:
            print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(markdown)

    sys.exit(0)


if __name__ == "__main__":
    main()
