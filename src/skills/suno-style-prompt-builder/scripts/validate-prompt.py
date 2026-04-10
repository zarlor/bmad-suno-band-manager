#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Validate Suno style prompt output for character limits and structure.

Validates:
- Style prompt character count (model-specific: v4 Pro=200, v4.5+/v5=1,000)
- Critical zone check (first 200 chars should contain all essentials)
- Exclusion prompt character count (recommended max ~200)
- Required fields present in prompt package
- Front-loading check (genre/mood should appear early)

Usage:
    python validate-prompt.py <prompt-file-or-text> [options]

    # Validate a prompt text directly
    python validate-prompt.py --style "indie folk-rock, warm..." --exclude "no autotune"

    # Validate with model-specific limits
    python validate-prompt.py --style "indie folk-rock..." --model "v4 Pro"

    # Validate from a file (expects YAML with style_prompt and exclusion_prompt fields)
    python validate-prompt.py prompt-output.yaml

    # Output to file
    python validate-prompt.py --style "..." -o results.json
"""

import argparse
import json
import sys
import re
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "_shared"))
from suno_constants import STYLE_PROMPT_LIMITS, STYLE_PROMPT_DEFAULT_MAX, CRITICAL_ZONE, EXCLUSION_RECOMMENDED_MAX, EXCLUSION_HARD_MAX

SCRIPT_NAME = "validate-prompt"
VERSION = "1.1.0"


def get_limit_for_model(model: str) -> int:
    """Return the style prompt character limit for a given Suno model."""
    return STYLE_PROMPT_LIMITS.get(model, STYLE_PROMPT_DEFAULT_MAX)


def validate_style_prompt(text: str, model: str = "") -> list[dict]:
    """Validate a style prompt and return findings."""
    findings = []
    char_count = len(text)
    limit = get_limit_for_model(model) if model else STYLE_PROMPT_DEFAULT_MAX

    # Character limit check (model-specific)
    if char_count > limit:
        findings.append({
            "severity": "critical",
            "category": "structure",
            "issue": f"Style prompt exceeds {limit:,} character limit for {model or 'default'} ({char_count} chars). Suno will silently truncate.",
            "fix": f"Trim {char_count - limit} characters. Cut from the end — genre/mood at the start are most important.",
            "data": {"char_count": char_count, "limit": limit, "over_by": char_count - limit, "model": model}
        })
    elif char_count > limit * 0.9:
        findings.append({
            "severity": "low",
            "category": "structure",
            "issue": f"Style prompt is near the {limit:,} character limit ({char_count} chars). Limited room for iteration.",
            "fix": "Consider trimming less essential descriptors to leave room for refinement.",
            "data": {"char_count": char_count, "limit": limit}
        })

    # Critical zone check — first 200 chars have strongest influence
    if char_count > CRITICAL_ZONE:
        first_segment = text[:CRITICAL_ZONE]
        remaining = text[CRITICAL_ZONE:]
        # Warn if substantial content exists beyond the critical zone
        if len(remaining.strip()) > 100:
            findings.append({
                "severity": "low",
                "category": "consistency",
                "issue": f"Style prompt has {len(remaining.strip())} chars beyond the critical zone (first {CRITICAL_ZONE} chars). Front-loaded terms have strongest influence on generation. Content beyond ~200 chars is supplementary but not wasted — v5.5 may interpret more of the prompt effectively.",
                "fix": "Ensure essential genre, mood, and vocal descriptors appear within the first 200 characters. Content beyond this zone adds nuance. This is a priority guide, not a character limit.",
                "data": {"critical_zone": CRITICAL_ZONE, "beyond_zone_chars": len(remaining.strip())}
            })

    # Empty check
    if not text.strip():
        findings.append({
            "severity": "critical",
            "category": "structure",
            "issue": "Style prompt is empty.",
            "fix": "Provide at minimum a genre and mood description."
        })
        return findings

    # Front-loading check — genre/mood keywords should appear in first 200 chars
    first_segment = text[:200].lower()
    genre_signals = ["rock", "pop", "folk", "jazz", "blues", "electronic", "hip hop", "r&b",
                     "country", "classical", "metal", "punk", "indie", "soul", "funk",
                     "ambient", "lo-fi", "lofi", "dance", "edm", "house", "techno",
                     "rap", "acoustic", "orchestral", "cinematic", "reggae", "latin",
                     "alternative", "grunge", "shoegaze", "post-punk", "synth", "disco"]
    has_genre = any(g in first_segment for g in genre_signals)
    if not has_genre:
        findings.append({
            "severity": "medium",
            "category": "consistency",
            "issue": "No obvious genre keyword found in the first 200 characters. Genre should be front-loaded.",
            "fix": "Move genre and mood descriptors to the beginning of the style prompt."
        })

    # Style cue contamination check (things that belong in lyrics, not style prompt)
    style_contamination = re.findall(r'\[(?:Verse|Chorus|Bridge|Intro|Outro|Pre-Chorus)\]', text, re.IGNORECASE)
    if style_contamination:
        findings.append({
            "severity": "high",
            "category": "structure",
            "issue": f"Lyric metatags found in style prompt: {style_contamination}. These belong in lyrics, not the style prompt.",
            "fix": "Remove all section tags ([Verse], [Chorus], etc.) from the style prompt. These go in the lyrics input."
        })

    # Asterisk check
    if '*' in text:
        findings.append({
            "severity": "medium",
            "category": "structure",
            "issue": "Asterisks found in style prompt. Suno does not use markdown formatting in style prompts.",
            "fix": "Remove all asterisks from the style prompt."
        })

    return findings


def validate_exclusion_prompt(text: str) -> list[dict]:
    """Validate an exclusion prompt and return findings."""
    findings = []

    if not text.strip():
        findings.append({
            "severity": "info",
            "category": "structure",
            "issue": "No exclusion prompt provided. This is optional but can improve results.",
            "fix": "Consider adding 2-3 specific exclusions to prevent unwanted elements."
        })
        return findings

    char_count = len(text)

    if char_count > EXCLUSION_HARD_MAX:
        findings.append({
            "severity": "high",
            "category": "structure",
            "issue": f"Exclusion prompt is very long ({char_count} chars). Too many negatives can confuse the model.",
            "fix": "Trim to 2-3 most important exclusions. Prioritize the elements you most want to avoid.",
            "data": {"char_count": char_count, "recommended_max": EXCLUSION_RECOMMENDED_MAX}
        })
    elif char_count > EXCLUSION_RECOMMENDED_MAX:
        findings.append({
            "severity": "low",
            "category": "structure",
            "issue": f"Exclusion prompt is above recommended length ({char_count} chars, recommended ~{EXCLUSION_RECOMMENDED_MAX}).",
            "fix": "Consider trimming to the most impactful exclusions.",
            "data": {"char_count": char_count, "recommended_max": EXCLUSION_RECOMMENDED_MAX}
        })

    # Count exclusion items
    items = [i.strip() for i in re.split(r'[,;]', text) if i.strip()]
    if len(items) > 5:
        findings.append({
            "severity": "medium",
            "category": "consistency",
            "issue": f"Too many exclusion items ({len(items)}). More than 3-5 exclusions can confuse the model.",
            "fix": "Reduce to 2-3 most critical exclusions."
        })

    # Vagueness check
    vague_terms = ["no music", "no sound", "no instruments", "no singing", "nothing bad"]
    for term in vague_terms:
        if term.lower() in text.lower():
            findings.append({
                "severity": "medium",
                "category": "consistency",
                "issue": f"Vague exclusion term found: '{term}'. Be specific about what to exclude.",
                "fix": "Replace with specific terms: 'no electric guitar' instead of 'no instruments'."
            })

    return findings


def build_report(style_findings: list, exclusion_findings: list, style_text: str, exclusion_text: str, skill_path: str = "") -> dict:
    """Build the standard output report."""
    all_findings = []
    for f in style_findings:
        f["location"] = {"field": "style_prompt"}
        all_findings.append(f)
    for f in exclusion_findings:
        f["location"] = {"field": "exclusion_prompt"}
        all_findings.append(f)

    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in all_findings:
        severity_counts[f["severity"]] = severity_counts.get(f["severity"], 0) + 1

    status = "pass"
    if severity_counts["critical"] > 0:
        status = "fail"
    elif severity_counts["high"] > 0:
        status = "warning"

    return {
        "script": SCRIPT_NAME,
        "version": VERSION,
        "skill_path": skill_path,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "metrics": {
            "style_prompt_chars": len(style_text),
            "style_prompt_limit": STYLE_PROMPT_DEFAULT_MAX,
            "critical_zone": CRITICAL_ZONE,
            "exclusion_prompt_chars": len(exclusion_text) if exclusion_text else 0,
            "exclusion_recommended_max": EXCLUSION_RECOMMENDED_MAX
        },
        "findings": all_findings,
        "summary": {
            "total": len(all_findings),
            **severity_counts
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Validate Suno style prompt output for character limits and structure.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --style "indie folk-rock, warm analog..." --exclude "no autotune"
  %(prog)s prompt-output.yaml
  %(prog)s --style "..." -o results.json --verbose
        """
    )
    parser.add_argument("file", nargs="?", help="YAML file with style_prompt and exclusion_prompt fields")
    parser.add_argument("--style", help="Style prompt text to validate")
    parser.add_argument("--exclude", default="", help="Exclusion prompt text to validate")
    parser.add_argument("--model", default="", help="Suno model name for model-specific limits (e.g., 'v4 Pro', 'v5 Pro')")
    parser.add_argument("-o", "--output", help="Output file path (defaults to stdout)")
    parser.add_argument("--verbose", action="store_true", help="Include debug information")
    parser.add_argument("--skill-path", default="", help="Skill path for report context")

    args = parser.parse_args()

    style_text = ""
    exclusion_text = ""

    if args.file:
        # Read from YAML file
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(2)
        try:
            import yaml
        except ImportError:
            # Fallback: simple key-value parsing for basic YAML
            content = file_path.read_text()
            for line in content.splitlines():
                if line.startswith("style_prompt:"):
                    style_text = line.split(":", 1)[1].strip().strip('"').strip("'")
                elif line.startswith("exclusion_prompt:"):
                    exclusion_text = line.split(":", 1)[1].strip().strip('"').strip("'")
        else:
            data = yaml.safe_load(file_path.read_text())
            style_text = data.get("style_prompt", "")
            exclusion_text = data.get("exclusion_prompt", "")
    elif args.style:
        style_text = args.style
        exclusion_text = args.exclude
    else:
        parser.print_help()
        sys.exit(2)

    if args.verbose:
        print(f"Validating style prompt ({len(style_text)} chars)...", file=sys.stderr)
        if exclusion_text:
            print(f"Validating exclusion prompt ({len(exclusion_text)} chars)...", file=sys.stderr)

    model = args.model
    if not model and args.file:
        # Try to extract model from YAML file
        try:
            if 'data' in dir() and isinstance(data, dict):
                model = data.get("model", "")
        except Exception:
            pass

    style_findings = validate_style_prompt(style_text, model=model)
    exclusion_findings = validate_exclusion_prompt(exclusion_text)
    report = build_report(style_findings, exclusion_findings, style_text, exclusion_text, args.skill_path)

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
