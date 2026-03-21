# /// script
# requires-python = ">=3.9"
# ///
"""Pre-analyze raw input text to extract deterministic metrics before LLM processing.

Detects existing structure, counts lines/words/characters, finds repeated phrases,
identifies potential rhyme pairs, and estimates needed structure.

Usage:
    python analyze-input.py <text-file> [options]

    # Analyze input from a file
    python analyze-input.py input.txt

    # Analyze from text argument
    python analyze-input.py --text "Some raw lyrics text"

    # Output to file
    python analyze-input.py input.txt -o results.json
"""

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_NAME = "analyze-input"
VERSION = "1.0.0"


def find_metatags(text: str) -> list[str]:
    """Find all metatag-style brackets in text."""
    return re.findall(r'\[([^\]]+)\]', text)


def find_repeated_phrases(text: str, min_words: int = 3, min_count: int = 2) -> list[dict]:
    """Find exact phrase matches of min_words+ words appearing min_count+ times."""
    lines = text.split('\n')
    # Collect all non-empty, non-tag lines
    content_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped and not re.match(r'^\[.*\]$', stripped):
            content_lines.append(stripped)

    # Build n-grams from all content
    all_words = []
    for line in content_lines:
        words = re.findall(r"[a-zA-Z']+", line.lower())
        all_words.extend(words)

    phrases = Counter()
    for n in range(min_words, min(8, len(all_words) + 1)):
        for i in range(len(all_words) - n + 1):
            phrase = " ".join(all_words[i:i + n])
            phrases[phrase] += 1

    # Filter and deduplicate (remove sub-phrases if a longer phrase has same count)
    results = {}
    for phrase, count in phrases.items():
        if count >= min_count:
            results[phrase] = count

    # Remove sub-phrases where a longer phrase has the same count
    filtered = {}
    sorted_phrases = sorted(results.keys(), key=len, reverse=True)
    for phrase in sorted_phrases:
        count = results[phrase]
        # Check if this is a sub-phrase of an already-kept longer phrase with same count
        is_sub = False
        for kept in filtered:
            if phrase in kept and filtered[kept] == count:
                is_sub = True
                break
        if not is_sub:
            filtered[phrase] = count

    return [{"phrase": p, "count": c} for p, c in sorted(filtered.items(), key=lambda x: -x[1])]


def find_rhyme_pairs(text: str) -> list[dict]:
    """Find potential rhyme pairs based on ending sounds (last 2-3 chars)."""
    lines = text.split('\n')
    content_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped and not re.match(r'^\[.*\]$', stripped):
            content_lines.append(stripped)

    # Extract last word of each line
    line_endings = []
    for i, line in enumerate(content_lines):
        words = re.findall(r"[a-zA-Z']+", line)
        if words:
            line_endings.append((i, words[-1].lower()))

    pairs = []
    seen = set()

    for idx in range(len(line_endings)):
        # Check consecutive and alternating lines
        for offset in (1, 2):
            if idx + offset < len(line_endings):
                i, word_a = line_endings[idx]
                j, word_b = line_endings[idx + offset]

                if word_a == word_b:
                    continue

                # Check if last 2 or 3 characters match
                match_len = 0
                if len(word_a) >= 2 and len(word_b) >= 2 and word_a[-2:] == word_b[-2:]:
                    match_len = 2
                if len(word_a) >= 3 and len(word_b) >= 3 and word_a[-3:] == word_b[-3:]:
                    match_len = 3

                if match_len > 0:
                    pair_key = tuple(sorted([word_a, word_b]))
                    if pair_key not in seen:
                        seen.add(pair_key)
                        pairs.append({
                            "words": [word_a, word_b],
                            "ending_match": word_a[-match_len:],
                            "pattern": "consecutive" if offset == 1 else "alternating"
                        })

    return pairs


def estimate_structure(line_count: int) -> dict:
    """Estimate structure category and needed sections from line count."""
    if line_count < 16:
        return {
            "estimated_structure": "short",
            "estimated_sections_needed": max(3, line_count // 4)
        }
    elif line_count <= 30:
        return {
            "estimated_structure": "medium",
            "estimated_sections_needed": max(5, line_count // 5)
        }
    else:
        return {
            "estimated_structure": "long",
            "estimated_sections_needed": max(7, line_count // 5)
        }


def analyze_input(text: str) -> dict:
    """Analyze input text and extract metrics."""
    lines = text.split('\n')
    non_empty_lines = [l for l in lines if l.strip()]
    content_lines = [l.strip() for l in lines if l.strip() and not re.match(r'^\[.*\]$', l.strip())]

    # Detect metatags
    existing_tags = find_metatags(text)
    has_existing_structure = any(
        re.match(r'^(verse|chorus|bridge|intro|outro|pre-chorus|hook|refrain|breakdown|build-up)', tag.lower())
        for tag in existing_tags
    )

    # Counts
    word_count = sum(len(line.split()) for line in content_lines)
    char_count = len(text)

    # Repeated phrases
    repeated = find_repeated_phrases(text)

    # Rhyme pairs
    rhymes = find_rhyme_pairs(text)

    # Structure estimate (based on content lines)
    structure = estimate_structure(len(content_lines))

    return {
        "has_existing_structure": has_existing_structure,
        "existing_tags": existing_tags,
        "line_count": len(lines),
        "non_empty_line_count": len(non_empty_lines),
        "word_count": word_count,
        "character_count": char_count,
        "repeated_phrases": repeated,
        "potential_rhyme_pairs": rhymes,
        **structure
    }


def build_report(analysis: dict, text: str, skill_path: str = "") -> dict:
    """Build the standard output report."""
    findings = []

    if analysis["has_existing_structure"]:
        findings.append({
            "severity": "info",
            "category": "structure",
            "issue": "Input already contains section metatags.",
            "fix": "May need restructuring rather than initial structuring."
        })

    if analysis["character_count"] > 3000:
        findings.append({
            "severity": "medium",
            "category": "length",
            "issue": f"Character count ({analysis['character_count']}) exceeds typical Suno budget.",
            "fix": "Consider trimming to stay within Suno's character limits."
        })

    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        severity_counts[f["severity"]] = severity_counts.get(f["severity"], 0) + 1

    status = "pass"
    if severity_counts["medium"] > 0:
        status = "info"

    return {
        "script": SCRIPT_NAME,
        "version": VERSION,
        "skill_path": skill_path,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "metrics": {
            "has_existing_structure": analysis["has_existing_structure"],
            "existing_tags": analysis["existing_tags"],
            "line_count": analysis["line_count"],
            "non_empty_line_count": analysis["non_empty_line_count"],
            "word_count": analysis["word_count"],
            "character_count": analysis["character_count"],
            "repeated_phrases": analysis["repeated_phrases"],
            "potential_rhyme_pairs": analysis["potential_rhyme_pairs"],
            "estimated_structure": analysis["estimated_structure"],
            "estimated_sections_needed": analysis["estimated_sections_needed"],
        },
        "findings": findings,
        "summary": {
            "total": len(findings),
            **severity_counts
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Pre-analyze raw input text to extract deterministic metrics.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.txt
  %(prog)s --text "Some raw lyrics\\nAnother line"
  %(prog)s --stdin < input.txt
  %(prog)s input.txt -o results.json --verbose

Metrics extracted:
  - Existing metatags and structure detection
  - Line, word, and character counts
  - Repeated phrases (3+ words, 2+ occurrences)
  - Potential rhyme pairs (shared endings)
  - Estimated structure size (short/medium/long)

Exit codes: 0=pass, 1=issues, 2=error
        """
    )
    parser.add_argument("file", nargs="?", help="Path to text file")
    parser.add_argument("--text", help="Text to analyze directly")
    parser.add_argument("--stdin", action="store_true", help="Read text from stdin")
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
        print(f"Analyzing input ({len(text)} chars, {len(text.splitlines())} lines)...", file=sys.stderr)

    analysis = analyze_input(text)
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
