# /// script
# requires-python = ">=3.9"
# ///
"""Detect cliche phrases in song lyrics.

Scans lyrics against a curated list of overused songwriting phrases and
returns flagged matches with line numbers and suggested alternatives.

Usage:
    python cliche-detector.py <lyrics-file> [options]

    # Detect cliches in a file
    python cliche-detector.py lyrics.txt

    # Detect from text argument
    python cliche-detector.py --text "Fire in my soul keeps burning bright"

    # Output to file
    python cliche-detector.py lyrics.txt -o results.json
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_NAME = "cliche-detector"
VERSION = "1.0.0"

# Cliche database: pattern -> category and alternatives
# Patterns use word boundaries for accurate matching
CLICHES = {
    # Nature/Weather cliches
    r"dance\s+in\s+the\s+rain": {
        "category": "nature",
        "alternatives": ["stand still in the downpour", "let the storm soak through", "walk the wet streets barefoot"]
    },
    r"light\s+(?:in|at)\s+(?:the\s+)?(?:end\s+of\s+the\s+)?tunnel": {
        "category": "nature",
        "alternatives": ["a crack in the wall letting day through", "the exit sign still glowing", "morning edging past the blinds"]
    },
    r"(?:a|the)\s+storm\s+(?:is\s+)?coming": {
        "category": "nature",
        "alternatives": ["the pressure's dropping", "sky's gone that green color", "the stillness before everything moves"]
    },
    r"garden\s+grow(?:ing|s)?\s+(?:through|in)\s+(?:the\s+)?rain": {
        "category": "nature",
        "alternatives": ["roots pushing through concrete", "something green where nothing should be", "growing sideways toward the light"]
    },
    # Fire/Passion cliches
    r"fire\s+in\s+my\s+soul": {
        "category": "passion",
        "alternatives": ["this ache that won't sit still", "something restless under my ribs", "a hum I can't turn off"]
    },
    r"burn(?:ing)?\s+(?:bright|inside|with\s+desire)": {
        "category": "passion",
        "alternatives": ["glowing like a wire", "running hot and quiet", "lit up from the inside out"]
    },
    r"(?:set|light)\s+(?:my|the)\s+world\s+on\s+fire": {
        "category": "passion",
        "alternatives": ["rearrange everything I know", "flip the table", "make the ground shake under me"]
    },
    r"spark\s+(?:that|which)\s+(?:ignit|light)": {
        "category": "passion",
        "alternatives": ["the moment it all shifted", "the first crack in the wall", "when the static cleared"]
    },
    # Heart/Emotional cliches
    r"broken\s+(?:heart|wings|dreams)": {
        "category": "emotional",
        "alternatives": ["bent out of shape", "cracked but not split", "the pieces I keep finding"]
    },
    r"heart\s+of\s+gold": {
        "category": "emotional",
        "alternatives": ["stubborn tenderness", "gentle past the rough", "kind in a way that costs them"]
    },
    r"(?:my|your|the)\s+heart\s+(?:is\s+)?(?:beating|racing|pounding)": {
        "category": "emotional",
        "alternatives": ["blood drumming in my ears", "chest tight with the rush", "pulse in my fingertips"]
    },
    r"tear(?:s)?\s+(?:fall(?:ing)?|roll(?:ing)?)\s+down": {
        "category": "emotional",
        "alternatives": ["eyes stinging", "wet face in the mirror", "salt on my lips"]
    },
    r"(?:mend|heal|fix)\s+(?:my|your|a)\s+broken\s+heart": {
        "category": "emotional",
        "alternatives": ["learn to carry this differently", "stop picking at the wound", "let the scar do its work"]
    },
    # Strength/Resilience cliches
    r"stand(?:ing)?\s+tall": {
        "category": "strength",
        "alternatives": ["not flinching", "still here", "planted and refusing to move"]
    },
    r"rise\s+(?:from|above|out\s+of)\s+the\s+ashes": {
        "category": "strength",
        "alternatives": ["rebuild from the wreckage", "walk out of the rubble", "start with what's left"]
    },
    r"(?:light|darkness)\s+(?:in|at)\s+the\s+(?:end|darkest)": {
        "category": "strength",
        "alternatives": ["one clear note in all the noise", "a way through I didn't see before", "the moment the fog thins"]
    },
    r"never\s+give\s+up": {
        "category": "strength",
        "alternatives": ["keep dragging forward", "refuse to quit this", "stubborn enough to stay"]
    },
    r"stronger\s+(?:than|now)": {
        "category": "strength",
        "alternatives": ["built different now", "tougher in the broken places", "harder to knock down"]
    },
    # Love cliches
    r"you\s+complete\s+me": {
        "category": "love",
        "alternatives": ["you fill the gaps I didn't know I had", "with you the noise stops", "I make more sense next to you"]
    },
    r"love\s+(?:is\s+)?(?:a\s+)?(?:battlefield|drug|addiction)": {
        "category": "love",
        "alternatives": ["love is a habit I can't break", "love is the thing that rearranges the furniture", "love is showing up when it's inconvenient"]
    },
    r"(?:my|our)\s+love\s+(?:is\s+)?(?:forever|eternal|undying)": {
        "category": "love",
        "alternatives": ["this thing between us doesn't have an off switch", "we keep finding our way back", "stubborn love that won't let go"]
    },
    r"lost\s+(?:in|without)\s+(?:your|those)\s+eyes": {
        "category": "love",
        "alternatives": ["caught in your attention", "held by the way you look", "frozen when you notice me"]
    },
    # Journey/Path cliches
    r"(?:long|winding)\s+(?:road|path|journey)": {
        "category": "journey",
        "alternatives": ["all these miles of wrong turns", "the route that kept changing", "following the bread crumbs"]
    },
    r"(?:find|finding|found)\s+(?:my|your|the)\s+way\s+(?:home|back)": {
        "category": "journey",
        "alternatives": ["recognize these streets again", "remember where the door is", "follow the familiar sounds"]
    },
    r"chasing\s+(?:dreams|the\s+sun|shadows)": {
        "category": "journey",
        "alternatives": ["running toward something unnamed", "following the pull", "reaching for what keeps moving"]
    },
}


def detect_cliches(text: str) -> list[dict]:
    """Scan text for cliche phrases and return matches."""
    findings = []
    lines = text.split('\n')

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # Skip metatags
        if not stripped or re.match(r'^\[.*\]$', stripped):
            continue

        for pattern, info in CLICHES.items():
            match = re.search(pattern, stripped, re.IGNORECASE)
            if match:
                findings.append({
                    "severity": "medium",
                    "category": "cliche",
                    "location": {"line": i, "column": match.start()},
                    "issue": f"Cliche phrase detected: '{match.group()}'",
                    "fix": f"Consider alternatives: {' | '.join(info['alternatives'])}",
                    "data": {
                        "matched_text": match.group(),
                        "cliche_category": info["category"],
                        "alternatives": info["alternatives"],
                        "full_line": stripped
                    }
                })

    return findings


def build_report(findings: list, text: str, skill_path: str = "") -> dict:
    """Build the standard output report."""
    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        severity_counts[f["severity"]] = severity_counts.get(f["severity"], 0) + 1

    status = "pass"
    if len(findings) > 5:
        status = "warning"
    elif len(findings) > 0:
        status = "info" if len(findings) <= 2 else "warning"

    # Categorize findings
    categories = {}
    for f in findings:
        cat = f.get("data", {}).get("cliche_category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1

    return {
        "script": SCRIPT_NAME,
        "version": VERSION,
        "skill_path": skill_path,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "metrics": {
            "total_cliches_found": len(findings),
            "categories": categories
        },
        "findings": findings,
        "summary": {
            "total": len(findings),
            **severity_counts
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Detect cliche phrases in song lyrics.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s lyrics.txt
  %(prog)s --text "Fire in my soul keeps burning bright"
  %(prog)s --stdin < lyrics.txt
  %(prog)s lyrics.txt -o results.json --verbose

Exit codes: 0=no cliches, 1=cliches found, 2=error
        """
    )
    parser.add_argument("file", nargs="?", help="Path to lyrics text file")
    parser.add_argument("--text", help="Lyrics text to scan directly")
    parser.add_argument("--stdin", action="store_true", help="Read lyrics from stdin")
    parser.add_argument("-o", "--output", help="Output file path (defaults to stdout)")
    parser.add_argument("--verbose", action="store_true", help="Print diagnostics to stderr")
    parser.add_argument("--skill-path", default="", help="Skill path for report context")

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
        print(f"Scanning for cliches ({len(text.splitlines())} lines)...", file=sys.stderr)

    findings = detect_cliches(text)
    report = build_report(findings, text, args.skill_path)

    output_json = json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(output_json)
        if args.verbose:
            print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(output_json)

    sys.exit(0 if len(findings) == 0 else 1)


if __name__ == "__main__":
    main()
