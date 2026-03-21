# /// script
# requires-python = ">=3.9"
# ///
"""Validate transformed lyrics structure for Suno compatibility.

Checks metatag formatting, section structure, blank line separators,
style cue contamination, and reasonable song length.

Usage:
    python validate-lyrics.py <lyrics-file-or-text> [options]

    # Validate lyrics from a file
    python validate-lyrics.py lyrics.txt

    # Validate lyrics from stdin
    echo "[Verse 1]\\nHello world" | python validate-lyrics.py --stdin

    # Validate with text argument
    python validate-lyrics.py --text "[Verse 1]\\nHello world"

    # Output to file
    python validate-lyrics.py lyrics.txt -o results.json
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_NAME = "validate-lyrics"
VERSION = "1.0.0"

# Valid section metatags (case-insensitive matching)
VALID_SECTIONS = {
    "intro", "verse", "verse 1", "verse 2", "verse 3", "verse 4",
    "pre-chorus", "chorus", "bridge", "breakdown", "build-up", "buildup",
    "final chorus", "outro", "hook", "refrain", "interlude",
    "post-chorus", "solo",
    # Instrumental / solo variants
    "guitar solo", "piano solo", "sax solo", "saxophone solo",
    "drum solo", "bass solo", "instrumental",
    # Structural tags
    "build", "drop", "break", "end",
    "fade out", "fade in",
}

# Valid vocal delivery cues (inline metatags, not section tags)
VALID_VOCAL_CUES = {
    "harmonized", "hummed", "humming", "whistled", "whistling",
    "crooning", "scat", "call and response",
}

# Valid descriptor metatag prefixes
VALID_DESCRIPTORS = {"mood", "energy", "vocal style", "instrument", "tempo", "key"}

# Style cues that should NOT be in lyrics
STYLE_CONTAMINATION_PATTERNS = [
    r'\b(?:BPM|bpm)\b',
    r'\b(?:stereo|mono)\s+(?:field|mix)\b',
    r'\b(?:radio[- ]ready|lo[- ]fi|hi[- ]fi)\b',
    r'\b(?:punchy|warm|crisp)\s+(?:drums|bass|mix|production)\b',
]

# Reasonable song length bounds (in non-empty, non-tag lines)
MIN_LYRIC_LINES = 8
MAX_LYRIC_LINES = 80
RECOMMENDED_MAX_SECTIONS = 12

# Suno character limits (total text including metatags)
SUNO_CHAR_LIMIT = 3000
SUNO_CHAR_WARNING = 2700


def parse_lyrics(text: str) -> dict:
    """Parse lyrics into structured sections with line data."""
    lines = text.split('\n')
    sections = []
    current_section = None
    orphaned_descriptors = []
    all_tags = []

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Check if this is a metatag
        tag_match = re.match(r'^\[([^\]]+)\]$', stripped)
        if tag_match:
            tag_content = tag_match.group(1).strip()
            all_tags.append({"text": tag_content, "line": i})

            # Check if it's a descriptor (has a colon)
            if ':' in tag_content:
                prefix = tag_content.split(':')[0].strip().lower()
                if prefix in VALID_DESCRIPTORS:
                    if current_section is None:
                        # Global descriptor — fine
                        pass
                    # Descriptor attached to current/next section — fine
                    continue

            # Check if it's a section tag
            tag_lower = tag_content.lower()
            # Strip numbers for matching: "Verse 1" -> "verse 1", but also match base "verse"
            is_section = (tag_lower in VALID_SECTIONS or
                         tag_lower in VALID_VOCAL_CUES or
                         re.match(r'^(verse|chorus|bridge|breakdown|build-up|buildup|pre-chorus|post-chorus|hook|refrain|interlude|solo|instrumental|break|drop|build|end|fade\s*(?:out|in))\s*\d*$', tag_lower))

            if is_section:
                current_section = {
                    "tag": tag_content,
                    "line": i,
                    "lyric_lines": [],
                    "lyric_line_numbers": []
                }
                sections.append(current_section)
            continue

        # Non-tag, non-empty line
        if stripped:
            if current_section:
                current_section["lyric_lines"].append(stripped)
                current_section["lyric_line_numbers"].append(i)

    return {
        "sections": sections,
        "all_tags": all_tags,
        "total_lines": len(lines),
        "raw_text": text
    }


def validate_lyrics(text: str) -> list[dict]:
    """Validate lyrics text and return findings."""
    findings = []
    lines = text.split('\n')

    if not text.strip():
        findings.append({
            "severity": "critical",
            "category": "structure",
            "issue": "Lyrics text is empty.",
            "fix": "Provide lyrics with at least one section and content."
        })
        return findings

    parsed = parse_lyrics(text)
    sections = parsed["sections"]

    # Check for at least one section tag
    if not sections:
        findings.append({
            "severity": "high",
            "category": "structure",
            "issue": "No section metatags found. Suno uses tags like [Verse], [Chorus] to structure songs.",
            "fix": "Add section tags to define song structure."
        })

    # Check for blank lines between sections
    tag_lines = {s["line"] for s in sections}
    for section in sections:
        line_num = section["line"]
        if line_num > 1:
            prev_line = lines[line_num - 2].strip() if line_num - 1 < len(lines) else ""
            if prev_line and not prev_line.startswith('['):
                findings.append({
                    "severity": "medium",
                    "category": "structure",
                    "location": {"line": line_num},
                    "issue": f"No blank line before section tag [{section['tag']}] at line {line_num}.",
                    "fix": "Add a blank line before each section tag for cleaner Suno parsing."
                })

    # Check for style cues in lyrics
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or re.match(r'^\[.*\]$', stripped):
            continue
        for pattern in STYLE_CONTAMINATION_PATTERNS:
            if re.search(pattern, stripped, re.IGNORECASE):
                findings.append({
                    "severity": "high",
                    "category": "structure",
                    "location": {"line": i},
                    "issue": f"Possible style cue in lyrics at line {i}: '{stripped[:60]}...'",
                    "fix": "Style descriptions belong in the style prompt, not in lyrics."
                })
                break

    # Check for asterisks
    for i, line in enumerate(lines, 1):
        if '*' in line:
            findings.append({
                "severity": "medium",
                "category": "structure",
                "location": {"line": i},
                "issue": f"Asterisk found in lyrics at line {i}. Suno doesn't use markdown.",
                "fix": "Remove asterisks from lyrics."
            })

    # Count actual lyric lines (non-empty, non-tag)
    lyric_lines = [l.strip() for l in lines if l.strip() and not re.match(r'^\[.*\]$', l.strip())]
    lyric_count = len(lyric_lines)

    if lyric_count < MIN_LYRIC_LINES:
        findings.append({
            "severity": "low",
            "category": "structure",
            "issue": f"Very short lyrics ({lyric_count} lines). May produce a very short song.",
            "fix": "Consider adding more content or sections for a full-length song."
        })

    # Character count check (Suno counts everything including metatags)
    char_count = len(text)
    if char_count > SUNO_CHAR_LIMIT:
        findings.append({
            "severity": "high",
            "category": "structure",
            "issue": f"Total character count ({char_count}) exceeds Suno's {SUNO_CHAR_LIMIT}-character limit. Suno will truncate your lyrics.",
            "fix": "Trim lyrics to stay under 3000 characters total."
        })
    elif char_count > SUNO_CHAR_WARNING:
        findings.append({
            "severity": "medium",
            "category": "structure",
            "issue": f"Total character count ({char_count}) is approaching Suno's {SUNO_CHAR_LIMIT}-character limit.",
            "fix": "Consider trimming to leave some headroom below 3000 characters."
        })

    if lyric_count > MAX_LYRIC_LINES:
        findings.append({
            "severity": "medium",
            "category": "structure",
            "issue": f"Very long lyrics ({lyric_count} lines). Suno may not render all content.",
            "fix": "Consider trimming to a more standard song length (20-50 lyric lines)."
        })

    # Check section count
    if len(sections) > RECOMMENDED_MAX_SECTIONS:
        findings.append({
            "severity": "low",
            "category": "structure",
            "issue": f"High section count ({len(sections)}). Songs typically have 6-10 sections.",
            "fix": "Consider consolidating sections for a cleaner structure."
        })

    # Check for invalid metatags
    for tag_info in parsed["all_tags"]:
        tag_text = tag_info["text"]
        tag_lower = tag_text.lower()
        # Is it a valid section?
        is_section = (tag_lower in VALID_SECTIONS or
                     re.match(r'^(verse|chorus|bridge|breakdown|build-up|buildup|pre-chorus|post-chorus|hook|refrain|interlude|solo|instrumental|break|drop|build|end|fade\s*(?:out|in))\s*\d*$', tag_lower))
        # Is it a valid vocal delivery cue?
        is_vocal_cue = tag_lower in VALID_VOCAL_CUES
        # Is it a valid descriptor?
        is_descriptor = ':' in tag_text and tag_text.split(':')[0].strip().lower() in VALID_DESCRIPTORS

        if not is_section and not is_vocal_cue and not is_descriptor:
            findings.append({
                "severity": "low",
                "category": "consistency",
                "location": {"line": tag_info["line"]},
                "issue": f"Unrecognized metatag [{tag_text}] at line {tag_info['line']}. May not be interpreted by Suno.",
                "fix": f"Use standard section tags or descriptor tags (Mood/Energy/Vocal Style/Instrument)."
            })

    # Punctuation density check
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or re.match(r'^\[.*\]$', stripped):
            continue
        words = stripped.split()
        word_count = len(words)
        if word_count == 0:
            continue
        # Count commas, dashes, semicolons, colons, ellipses
        punct_count = (
            stripped.count(',') + stripped.count('-') + stripped.count(';')
            + stripped.count(':') + stripped.count('...')
        )
        density = punct_count / word_count
        if density > 0.5:
            findings.append({
                "severity": "low",
                "category": "rhythm",
                "location": {"line": i},
                "issue": f"Heavy punctuation density ({density:.2f}) at line {i}: '{stripped[:60]}'. Heavy punctuation can confuse Suno's cadence.",
                "fix": "Simplify punctuation to let Suno interpret natural phrasing."
            })

    # Check for empty sections
    for section in sections:
        if not section["lyric_lines"]:
            findings.append({
                "severity": "low",
                "category": "structure",
                "location": {"line": section["line"]},
                "issue": f"Empty section [{section['tag']}] at line {section['line']}.",
                "fix": "Add lyrics to this section or remove the tag if it's meant to be instrumental."
            })

    return findings


def build_report(findings: list, text: str, skill_path: str = "") -> dict:
    """Build the standard output report."""
    for f in findings:
        if "location" not in f:
            f["location"] = {"file": "lyrics"}

    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        severity_counts[f["severity"]] = severity_counts.get(f["severity"], 0) + 1

    status = "pass"
    if severity_counts["critical"] > 0:
        status = "fail"
    elif severity_counts["high"] > 0:
        status = "warning"

    parsed = parse_lyrics(text)
    lyric_lines = [l.strip() for l in text.split('\n')
                   if l.strip() and not re.match(r'^\[.*\]$', l.strip())]

    return {
        "script": SCRIPT_NAME,
        "version": VERSION,
        "skill_path": skill_path,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "metrics": {
            "total_lines": parsed["total_lines"],
            "lyric_lines": len(lyric_lines),
            "character_count": len(text),
            "section_count": len(parsed["sections"]),
            "sections": [s["tag"] for s in parsed["sections"]]
        },
        "findings": findings,
        "summary": {
            "total": len(findings),
            **severity_counts
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Validate transformed lyrics structure for Suno compatibility.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s lyrics.txt
  %(prog)s --text "[Verse 1]\\nHello world"
  %(prog)s --stdin < lyrics.txt
  %(prog)s lyrics.txt -o results.json --verbose

Exit codes: 0=pass, 1=fail/warning, 2=error
        """
    )
    parser.add_argument("file", nargs="?", help="Path to lyrics text file")
    parser.add_argument("--text", help="Lyrics text to validate directly")
    parser.add_argument("--stdin", action="store_true", help="Read lyrics from stdin")
    parser.add_argument("-o", "--output", help="Output file path (defaults to stdout)")
    parser.add_argument("--verbose", action="store_true", help="Print diagnostics to stderr")
    parser.add_argument("--skill-path", default="", help="Skill path for report context")

    args = parser.parse_args()

    text = ""
    if args.text is not None:
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
        print(f"Validating lyrics ({len(text)} chars, {len(text.splitlines())} lines)...", file=sys.stderr)

    findings = validate_lyrics(text)
    report = build_report(findings, text, args.skill_path)

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
