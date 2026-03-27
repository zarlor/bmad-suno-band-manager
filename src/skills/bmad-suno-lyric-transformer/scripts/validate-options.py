# /// script
# requires-python = ">=3.9"
# ///
"""Validate transformation option selections against mutual exclusion rules.

Checks that selected transformation option codes are valid and consistent,
enforcing mutual exclusion and dependency rules between options.

Usage:
    python validate-options.py <option-codes> [options]

    # Validate option codes from positional argument
    python validate-options.py "ST,CC,RA,CD"

    # Validate with --codes flag
    python validate-options.py --codes "ST,CC,RA,CD"

    # Output to file
    python validate-options.py "ST,CC,RA" -o results.json
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_NAME = "validate-options"
VERSION = "1.0.0"

VALID_CODES = {"ST", "CE", "CC", "RA", "FR", "CD", "WF"}

CODE_DESCRIPTIONS = {
    "ST": "Structural Transformation",
    "CE": "Cliche Elimination",
    "CC": "Consistency Check",
    "RA": "Rhyme Analysis",
    "FR": "Full Rewrite",
    "CD": "Cliche Detection",
    "WF": "Word Flow",
}


def validate_options(codes_str: str) -> dict:
    """Validate option codes and return results with findings."""
    raw_codes = [c.strip().upper() for c in codes_str.split(",") if c.strip()]
    findings = []
    removed_codes = []
    validated_codes = []

    if not raw_codes:
        findings.append({
            "severity": "critical",
            "category": "validation",
            "issue": "No option codes provided.",
            "fix": "Provide at least one valid option code: " + ", ".join(sorted(VALID_CODES))
        })
        return {
            "validated_codes": [],
            "removed_codes": [],
            "findings": findings
        }

    # Check for invalid codes
    invalid = [c for c in raw_codes if c not in VALID_CODES]
    valid_input = [c for c in raw_codes if c in VALID_CODES]

    for code in invalid:
        findings.append({
            "severity": "high",
            "category": "validation",
            "issue": f"Invalid option code: '{code}'.",
            "fix": f"Valid codes are: {', '.join(sorted(VALID_CODES))}"
        })

    # Check for duplicates
    seen = set()
    deduped = []
    for code in valid_input:
        if code in seen:
            findings.append({
                "severity": "info",
                "category": "validation",
                "issue": f"Duplicate option code: '{code}'.",
                "fix": "Each code should appear only once."
            })
        else:
            seen.add(code)
            deduped.append(code)

    working = list(deduped)

    # FR and WF are mutually exclusive
    if "FR" in working and "WF" in working:
        findings.append({
            "severity": "high",
            "category": "exclusion",
            "issue": "FR (Full Rewrite) and WF (Word Flow) are mutually exclusive.",
            "fix": "Choose either FR or WF, not both."
        })

    # CE is skipped if FR is selected (warn, auto-remove CE)
    if "FR" in working and "CE" in working:
        working.remove("CE")
        removed_codes.append("CE")
        findings.append({
            "severity": "medium",
            "category": "dependency",
            "issue": "CE (Cliche Elimination) auto-removed: redundant when FR (Full Rewrite) is selected.",
            "fix": "FR already encompasses cliche elimination."
        })

    # CC is skipped if CE is selected (info, can be overridden)
    if "CE" in working and "CC" in working:
        findings.append({
            "severity": "info",
            "category": "dependency",
            "issue": "CC (Consistency Check) may be redundant when CE (Cliche Elimination) is selected.",
            "fix": "CE may alter consistency; CC can still be kept if desired."
        })

    validated_codes = working

    return {
        "validated_codes": validated_codes,
        "removed_codes": removed_codes,
        "findings": findings
    }


def build_report(result: dict, codes_str: str, skill_path: str = "") -> dict:
    """Build the standard output report."""
    findings = result["findings"]

    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        severity_counts[f["severity"]] = severity_counts.get(f["severity"], 0) + 1

    status = "pass"
    if severity_counts["critical"] > 0 or severity_counts["high"] > 0:
        status = "error"
    elif severity_counts["medium"] > 0:
        status = "warning"

    return {
        "script": SCRIPT_NAME,
        "version": VERSION,
        "skill_path": skill_path,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "validated_codes": result["validated_codes"],
        "removed_codes": result["removed_codes"],
        "findings": findings,
        "summary": {
            "total": len(findings),
            **severity_counts
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Validate transformation option selections against mutual exclusion rules.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "ST,CC,RA,CD"
  %(prog)s --codes "ST,CC,RA,CD"
  %(prog)s "FR,CE" -o results.json --verbose

Valid codes: ST, CE, CC, RA, FR, CD, WF
Rules:
  - FR and WF are mutually exclusive
  - CE is auto-removed when FR is selected
  - CC info note when CE is selected

Exit codes: 0=pass, 1=issues, 2=error
        """
    )
    parser.add_argument("file", nargs="?", help="Comma-separated option codes (positional)")
    parser.add_argument("--codes", help="Comma-separated option codes")
    parser.add_argument("--text", help="Alias for --codes (for consistency)")
    parser.add_argument("--stdin", action="store_true", help="Read codes from stdin")
    parser.add_argument("-o", "--output", help="Output file path (defaults to stdout)")
    parser.add_argument("--verbose", action="store_true", help="Print diagnostics to stderr")
    parser.add_argument("--skill-path", default="", help="Skill path for report context")

    args = parser.parse_args()

    codes_str = ""
    if args.codes is not None:
        codes_str = args.codes
    elif args.text is not None:
        codes_str = args.text
    elif args.stdin:
        codes_str = sys.stdin.read().strip()
    elif args.file:
        codes_str = args.file
    else:
        parser.print_help()
        sys.exit(2)

    if args.verbose:
        print(f"Validating option codes: {codes_str}", file=sys.stderr)

    result = validate_options(codes_str)
    report = build_report(result, codes_str, args.skill_path)

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
