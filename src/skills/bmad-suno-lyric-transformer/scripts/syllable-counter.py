# /// script
# requires-python = ">=3.9"
# ///
"""Count syllables per line and analyze rhythmic consistency in lyrics.

Uses a heuristic syllable counting algorithm (vowel cluster method with
common English adjustments). Not perfect, but reliable enough for
songwriting guidance — consistent to within +/- 1 syllable per line.

Usage:
    python syllable-counter.py <lyrics-file> [options]

    # Count syllables in a file
    python syllable-counter.py lyrics.txt

    # Count from text argument
    python syllable-counter.py --text "Walking through the fog of morning"

    # Output to file
    python syllable-counter.py lyrics.txt -o results.json
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_NAME = "syllable-counter"
VERSION = "1.0.0"

# Common words with known syllable counts that the algorithm gets wrong
SYLLABLE_OVERRIDES = {
    "the": 1, "every": 3, "different": 3, "evening": 3, "heaven": 2,
    "beautiful": 3, "comfortable": 3, "interesting": 4, "chocolate": 3,
    "fire": 2, "hour": 2, "flower": 2, "power": 2, "tower": 2,
    "desire": 3, "inspire": 3, "higher": 2, "liar": 2, "wire": 2,
    "quiet": 2, "lion": 2, "riot": 2, "diary": 3, "science": 2,
    "poem": 2, "being": 2, "seeing": 2, "doing": 2, "going": 2,
    "cruel": 2, "fuel": 2, "jewel": 2, "real": 1, "deal": 1,
    "people": 2, "little": 2, "middle": 2, "simple": 2, "able": 2,
    "maybe": 2, "somewhere": 2, "nowhere": 2, "everywhere": 3,
    "i'm": 1, "you're": 1, "we're": 1, "they're": 1, "he's": 1,
    "she's": 1, "it's": 1, "don't": 1, "won't": 1, "can't": 1,
    "couldn't": 2, "wouldn't": 2, "shouldn't": 2, "didn't": 2,
    "isn't": 2, "wasn't": 2, "aren't": 2, "weren't": 2,
}


def count_syllables(word: str) -> int:
    """Count syllables in a single word using vowel cluster heuristic."""
    word = word.lower().strip()

    # Remove non-alpha except apostrophes
    word = re.sub(r"[^a-z']", "", word)

    if not word:
        return 0

    # Check overrides first
    if word in SYLLABLE_OVERRIDES:
        return SYLLABLE_OVERRIDES[word]

    # Vowel cluster counting with adjustments
    vowels = "aeiouy"
    count = 0
    prev_vowel = False

    for i, char in enumerate(word):
        is_vowel = char in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel

    # Adjustments
    # Silent e at end
    if word.endswith('e') and not word.endswith(('le', 'ce', 'se', 'ge', 'ze', 'ne', 'me', 've', 'te', 'de', 'be', 'fe', 'he', 'ke', 'pe', 'we', 'ye')):
        count -= 1
    elif word.endswith('e') and len(word) > 3 and word[-2] not in vowels:
        count -= 1

    # -ed ending (usually not a syllable unless preceded by t or d)
    if word.endswith('ed') and len(word) > 3:
        if word[-3] not in ('t', 'd'):
            count -= 1

    # -le at end is usually a syllable
    if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
        count += 1

    # -es ending
    if word.endswith('es') and len(word) > 3:
        if word[-3] in ('s', 'z', 'x', 'ch', 'sh'):
            pass  # -es IS a syllable here
        elif word[-3] not in vowels:
            count -= 1

    # Ensure at least 1 syllable for any word
    return max(1, count)


def count_line_syllables(line: str) -> int:
    """Count total syllables in a line of text."""
    # Remove metatags
    line = re.sub(r'\[.*?\]', '', line)
    words = line.split()
    return sum(count_syllables(w) for w in words)


def estimate_duration(total_lines: int, avg_syllables: float, sections: list = None) -> tuple:
    """Estimate song duration based on lyrics structure and instrumental sections.

    Returns (min_seconds, max_seconds) tuple.

    Factors:
    - Lyric lines: ~3-5 seconds per line depending on syllable density
    - Instrumental sections (Intro, Outro, Solo, Breakdown, Build-Up):
      add time with no lyric lines
    - Suno typically generates 2-4 min songs from moderate lyrics

    NOTE: This is a rough estimate. Actual Suno output varies significantly
    based on tempo, model, style prompt, and generation randomness.
    """
    if total_lines == 0:
        return (0, 0)

    # Base time from lyric lines
    # Denser syllables = faster delivery = less time per line
    if avg_syllables > 10:
        secs_per_line_min, secs_per_line_max = 2.5, 4.0
    elif avg_syllables > 7:
        secs_per_line_min, secs_per_line_max = 3.0, 4.5
    else:
        secs_per_line_min, secs_per_line_max = 3.5, 5.5

    lyric_min = round(total_lines * secs_per_line_min)
    lyric_max = round(total_lines * secs_per_line_max)

    # Add time for instrumental sections
    # These appear as section tags but contribute no lyric lines
    INSTRUMENTAL_TAGS = {
        "intro": (5, 15),
        "outro": (8, 20),
        "guitar solo": (10, 25),
        "solo": (10, 25),
        "instrumental": (10, 25),
        "breakdown": (8, 20),
        "build-up": (5, 15),
        "interlude": (8, 20),
        "drum solo": (8, 20),
        "sax solo": (10, 25),
        "piano solo": (10, 25),
    }

    instrumental_min = 0
    instrumental_max = 0
    if sections:
        for section in sections:
            section_name = section.get("name", "").strip("[]").lower()
            for tag, (t_min, t_max) in INSTRUMENTAL_TAGS.items():
                if tag in section_name:
                    instrumental_min += t_min
                    instrumental_max += t_max
                    break

    # Also check for [Hummed] or empty-content sections that still take time
    if sections:
        for section in sections:
            section_name = section.get("name", "").strip("[]").lower()
            if "hummed" in section_name or "whistled" in section_name:
                instrumental_min += 5
                instrumental_max += 15

    min_seconds = lyric_min + instrumental_min
    max_seconds = lyric_max + instrumental_max

    return (min_seconds, max_seconds)


def format_duration(seconds: int) -> str:
    """Format seconds as M:SS."""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"


def format_duration_range(min_seconds: int, max_seconds: int) -> str:
    """Format a duration range as 'M:SS-M:SS'."""
    return f"{format_duration(min_seconds)}-{format_duration(max_seconds)}"


def analyze_lyrics(text: str) -> dict:
    """Analyze lyrics for syllable counts and rhythmic consistency."""
    lines = text.split('\n')
    line_data = []
    sections = []
    current_section = {"name": "ungrouped", "lines": []}

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Check for section tag
        tag_match = re.match(r'^\[([^\]:]+?)(?:\s*\d*)?\]$', stripped)
        if tag_match and ':' not in stripped:
            # Start new section
            if current_section["lines"]:
                sections.append(current_section)
            current_section = {"name": stripped, "lines": []}
            continue

        # Skip empty lines and descriptor metatags
        if not stripped or re.match(r'^\[.*:.*\]$', stripped):
            continue

        syllables = count_line_syllables(stripped)
        entry = {
            "line_number": i,
            "text": stripped,
            "syllables": syllables,
            "word_count": len(stripped.split())
        }
        line_data.append(entry)
        current_section["lines"].append(entry)

    # Don't forget last section
    if current_section["lines"]:
        sections.append(current_section)

    # Analyze per-section consistency
    section_analysis = []
    findings = []

    for section in sections:
        if not section["lines"]:
            continue

        counts = [line["syllables"] for line in section["lines"]]
        avg = sum(counts) / len(counts)
        min_c = min(counts)
        max_c = max(counts)
        spread = max_c - min_c

        analysis = {
            "section": section["name"],
            "line_count": len(counts),
            "syllable_counts": counts,
            "average": round(avg, 1),
            "min": min_c,
            "max": max_c,
            "spread": spread
        }
        section_analysis.append(analysis)

        # Flag high variance within a section (spread > 2x the average line)
        if spread > avg and len(counts) > 2:
            findings.append({
                "severity": "low",
                "category": "rhythm",
                "location": {"section": section["name"]},
                "issue": f"High syllable variance in {section['name']}: range {min_c}-{max_c} (avg {avg:.0f}). This may cause uneven vocal phrasing.",
                "fix": f"Try to keep lines within a {int(avg)-2}-{int(avg)+2} syllable range for smoother singing.",
                "data": {"section": section["name"], "counts": counts, "average": round(avg, 1)}
            })

    # Overall metrics
    all_counts = [entry["syllables"] for entry in line_data]
    overall_avg = sum(all_counts) / len(all_counts) if all_counts else 0

    # Duration estimation (accounts for instrumental sections)
    min_sec, max_sec = estimate_duration(len(line_data), overall_avg, sections)
    duration_info = {
        "min_seconds": min_sec,
        "max_seconds": max_sec,
        "formatted": format_duration_range(min_sec, max_sec),
        "note": "Rough estimate — actual Suno output varies based on tempo, model, style prompt, and generation randomness. Instrumental sections, solos, and intros/outros add time beyond what lyrics alone suggest."
    }

    return {
        "line_data": line_data,
        "section_analysis": section_analysis,
        "overall": {
            "total_lyric_lines": len(line_data),
            "total_syllables": sum(all_counts),
            "average_syllables_per_line": round(overall_avg, 1),
            "min_syllables": min(all_counts) if all_counts else 0,
            "max_syllables": max(all_counts) if all_counts else 0,
            "estimated_duration": duration_info
        },
        "findings": findings
    }


def build_report(analysis: dict, text: str, skill_path: str = "") -> dict:
    """Build the standard output report."""
    findings = analysis["findings"]

    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        severity_counts[f["severity"]] = severity_counts.get(f["severity"], 0) + 1

    status = "pass"
    if severity_counts["high"] > 0:
        status = "warning"

    return {
        "script": SCRIPT_NAME,
        "version": VERSION,
        "skill_path": skill_path,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "metrics": analysis["overall"],
        "line_data": analysis["line_data"],
        "section_analysis": analysis["section_analysis"],
        "findings": findings,
        "summary": {
            "total": len(findings),
            **severity_counts
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Count syllables per line and analyze rhythmic consistency in lyrics.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s lyrics.txt
  %(prog)s --text "Walking through the fog of morning"
  %(prog)s --stdin < lyrics.txt
  %(prog)s lyrics.txt -o results.json --verbose

Exit codes: 0=pass, 1=rhythm issues found, 2=error
        """
    )
    parser.add_argument("file", nargs="?", help="Path to lyrics text file")
    parser.add_argument("--text", help="Lyrics text to analyze directly")
    parser.add_argument("--stdin", action="store_true", help="Read lyrics from stdin")
    parser.add_argument("-o", "--output", help="Output file path (defaults to stdout)")
    parser.add_argument("--verbose", action="store_true", help="Print diagnostics to stderr")
    parser.add_argument("--skill-path", default="", help="Skill path for report context")
    parser.add_argument("--estimate-duration", action="store_true", help="Show estimated duration prominently")

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
        print(f"Analyzing syllables ({len(text.splitlines())} lines)...", file=sys.stderr)

    analysis = analyze_lyrics(text)
    report = build_report(analysis, text, args.skill_path)

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
