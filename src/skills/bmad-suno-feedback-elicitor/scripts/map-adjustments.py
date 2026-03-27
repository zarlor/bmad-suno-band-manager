#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Map feedback dimension categories to Suno parameter adjustment recommendations.

Takes structured feedback dimensions (from parse-feedback.py or LLM triage)
and returns baseline parameter adjustment recommendations as structured JSON.
The LLM then refines these recommendations with contextual judgment.

Exit codes:
  0 = adjustments generated successfully
  1 = invalid input
  2 = runtime error
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "_shared"))
from suno_constants import CRITICAL_ZONE, EXCLUSION_RECOMMENDED_MAX, PAID_TIERS

# Adjustment lookup tables
# Each dimension maps to a set of possible adjustments categorized by direction

STYLE_PROMPT_ADJUSTMENTS: dict[str, dict[str, dict[str, Any]]] = {
    "instrumentation": {
        "too_much": {
            "add": ["minimal arrangement", "sparse instrumentation", "stripped-back"],
            "remove_patterns": ["lush", "layered", "full", "dense", "wall of sound"],
            "exclude_add": ["no dense layering"],
        },
        "too_little": {
            "add": ["lush arrangement", "layered instrumentation", "full sound"],
            "remove_patterns": ["minimal", "sparse", "stripped"],
            "exclude_add": [],
        },
        "wrong_type": {
            "add": [],
            "remove_patterns": [],
            "exclude_add": [],
            "note": "Specify the unwanted instrument in exclusions and desired instrument in style prompt",
        },
    },
    "vocals": {
        "too_polished": {
            "add": ["raw vocal", "imperfect delivery", "organic phrasing"],
            "remove_patterns": ["polished", "clean vocal", "perfect"],
            "exclude_add": ["no overproduced vocals"],
        },
        "too_rough": {
            "add": ["polished vocal", "smooth delivery", "clean singing"],
            "remove_patterns": ["raw", "rough", "gritty"],
            "exclude_add": ["no raspy vocals"],
        },
        "too_quiet": {
            "add": ["prominent vocals", "voice-forward mix"],
            "remove_patterns": [],
            "exclude_add": [],
        },
        "too_loud": {
            "add": ["balanced mix", "instrument-forward"],
            "remove_patterns": ["prominent vocal", "voice-forward"],
            "exclude_add": [],
        },
        "wrong_character": {
            "add": [],
            "remove_patterns": [],
            "exclude_add": [],
            "note": "Specify desired vocal character: gender, age, tone, delivery style",
        },
    },
    "energy": {
        "too_high": {
            "add": ["gentle", "soft", "understated", "subtle"],
            "remove_patterns": ["high energy", "powerful", "driving", "intense"],
            "exclude_add": [],
            "slider": {"weirdness": "unchanged", "style_influence": "unchanged"},
        },
        "too_low": {
            "add": ["high energy", "powerful", "dynamic", "driving"],
            "remove_patterns": ["gentle", "soft", "subtle", "laid-back"],
            "exclude_add": [],
            "slider": {"style_influence": "decrease_slightly"},
        },
        "flat": {
            "add": ["dynamic shifts", "building energy", "crescendo", "varied sections"],
            "remove_patterns": [],
            "exclude_add": [],
            "slider": {"weirdness": "increase_slightly"},
        },
    },
    "tempo": {
        "too_fast": {
            "add": ["slow tempo", "laid-back", "relaxed groove"],
            "remove_patterns": ["uptempo", "fast", "driving rhythm", "energetic pace"],
            "exclude_add": [],
        },
        "too_slow": {
            "add": ["uptempo", "driving rhythm", "energetic pace"],
            "remove_patterns": ["slow", "laid-back", "relaxed", "gentle pace"],
            "exclude_add": [],
        },
    },
    "production": {
        "too_polished": {
            "add": ["lo-fi", "raw production", "analog warmth", "rough edges"],
            "remove_patterns": ["radio-ready", "clean production", "crisp", "polished"],
            "exclude_add": [],
            "slider": {"weirdness": "increase"},
        },
        "too_rough": {
            "add": ["radio-ready mix", "clean production", "crisp", "polished"],
            "remove_patterns": ["lo-fi", "raw", "rough", "analog"],
            "exclude_add": [],
            "slider": {"weirdness": "decrease"},
        },
        "too_reverb": {
            "add": ["dry mix", "close mic", "intimate"],
            "remove_patterns": ["spacious", "reverb", "ambient", "atmospheric"],
            "exclude_add": [],
        },
        "too_dry": {
            "add": ["spacious", "reverb", "ambient", "atmospheric"],
            "remove_patterns": ["dry", "close mic"],
            "exclude_add": [],
        },
    },
    "vibe": {
        "too_happy": {
            "add": ["melancholic", "bittersweet", "minor key", "moody"],
            "remove_patterns": ["uplifting", "bright", "happy", "cheerful", "major key"],
            "exclude_add": [],
        },
        "too_dark": {
            "add": ["uplifting", "bright", "major key", "hopeful"],
            "remove_patterns": ["melancholic", "dark", "moody", "minor key"],
            "exclude_add": [],
        },
        "too_generic": {
            "add": ["distinctive", "unique", "unconventional"],
            "remove_patterns": ["classic", "traditional", "conventional"],
            "exclude_add": [],
            "slider": {"weirdness": "increase_significantly"},
        },
        "too_weird": {
            "add": ["familiar", "classic", "conventional", "straightforward"],
            "remove_patterns": ["experimental", "unexpected", "unconventional"],
            "exclude_add": [],
            "slider": {"weirdness": "decrease_significantly"},
        },
    },
    "music": {
        "general_issue": {
            "add": [],
            "remove_patterns": [],
            "exclude_add": [],
            "note": "Music feedback requires further narrowing — which aspect of the music? Instrumentation, tempo, energy, production?",
        },
    },
    "structure": {
        "needs_bridge": {
            "lyric_change": "Add [Bridge] section between second chorus and outro",
        },
        "chorus_weak": {
            "lyric_change": "Add [Energy: High] before chorus, consider [Build-Up] section",
        },
        "too_long": {
            "lyric_change": "Remove repeated sections or shorten verses",
        },
        "too_short": {
            "lyric_change": "Add additional verse or extend instrumental sections",
        },
    },
    "lyrics": {
        "phrasing_unnatural": {
            "lyric_change": "Run syllable counter, normalize line lengths within sections",
        },
        "content_mismatch": {
            "lyric_change": "Review lyrics against intended mood/theme, revise for alignment",
        },
        "vocal_style_inconsistent": {
            "lyric_change": "Add consistent [Vocal Style: ...] tags before each section",
        },
    },
    "quality": {
        "artifacts": {
            "note": "Audio artifacts are generation-specific. Regenerate 3-5 times before modifying prompt. If persistent, simplify style prompt.",
        },
        "robotic_vocals": {
            "add": ["natural vocal", "organic phrasing", "human delivery", "breathy"],
            "remove_patterns": [],
            "exclude_add": ["no auto-tune", "no robotic vocals"],
        },
        "clipping": {
            "add": ["clean mix", "dynamic range", "headroom"],
            "remove_patterns": ["heavy", "distorted", "loud", "wall of sound"],
            "exclude_add": [],
        },
        "muffled": {
            "add": ["crisp", "clear mix", "defined frequencies", "bright"],
            "remove_patterns": ["warm", "lo-fi", "analog"],
            "exclude_add": [],
        },
    },
    "length": {
        "too_short": {
            "lyric_change": "Add sections in lyrics (additional verse, bridge, instrumental break) or use Suno extend feature",
        },
        "too_long": {
            "lyric_change": "Remove repeated sections, trim [Outro] content, remove non-essential [Breakdown]",
        },
        "intro_too_long": {
            "lyric_change": "Shorten or remove [Intro] content, add [Verse 1] tag earlier",
        },
        "outro_cuts_off": {
            "lyric_change": "Add explicit [Outro] section with 2-4 lines, add [Fade Out] metatag",
        },
        "pacing_drags": {
            "lyric_change": "Add [Energy: building] metatags, shorten dragging sections, add [Breakdown] or [Build-Up] for variety",
        },
    },
}

SLIDER_DIRECTION_MAP = {
    "increase_slightly": "+5-10 from current",
    "increase": "+15-20 from current",
    "increase_significantly": "+25-35 from current (cap at 85)",
    "decrease_slightly": "-5-10 from current",
    "decrease": "-15-20 from current",
    "decrease_significantly": "-25-35 from current (floor at 15)",
    "unchanged": "no change recommended",
}


def generate_adjustments(
    dimensions: list[dict[str, str]],
    current_tier: str = "",
) -> dict[str, Any]:
    """Generate adjustment recommendations from feedback dimensions."""
    style_add: list[str] = []
    style_remove: list[str] = []
    exclude_add: list[str] = []
    slider_adjustments: dict[str, str] = {}
    lyric_changes: list[str] = []
    notes: list[str] = []

    for dim_entry in dimensions:
        dimension = dim_entry.get("dimension", "")
        direction = dim_entry.get("direction", "")

        if dimension not in STYLE_PROMPT_ADJUSTMENTS:
            notes.append(f"Unknown dimension '{dimension}' — requires LLM judgment")
            continue

        dim_adjustments = STYLE_PROMPT_ADJUSTMENTS[dimension]
        if direction not in dim_adjustments:
            available = list(dim_adjustments.keys())
            notes.append(
                f"Unknown direction '{direction}' for dimension '{dimension}'. "
                f"Available: {', '.join(available)}"
            )
            continue

        adj = dim_adjustments[direction]

        if "add" in adj:
            style_add.extend(adj["add"])
        if "remove_patterns" in adj:
            style_remove.extend(adj["remove_patterns"])
        if "exclude_add" in adj:
            exclude_add.extend(adj["exclude_add"])
        if "slider" in adj:
            for slider_name, slider_dir in adj["slider"].items():
                slider_adjustments[slider_name] = SLIDER_DIRECTION_MAP.get(
                    slider_dir, slider_dir
                )
        if "lyric_change" in adj:
            lyric_changes.append(adj["lyric_change"])
        if "note" in adj:
            notes.append(adj["note"])

    is_paid = current_tier.lower() in PAID_TIERS if current_tier else False

    result: dict[str, Any] = {
        "style_prompt": {
            "add_descriptors": list(dict.fromkeys(style_add)),  # dedupe preserving order
            "remove_patterns": list(dict.fromkeys(style_remove)),
        },
        "exclusions": {
            "add": list(dict.fromkeys(exclude_add)),
        },
    }

    if slider_adjustments:
        if is_paid:
            result["sliders"] = slider_adjustments
        else:
            result["sliders"] = {
                "note": "Slider adjustments recommended but not available on free tier. Compensate through style prompt wording.",
                "recommended_if_upgraded": slider_adjustments,
            }

    if lyric_changes:
        result["lyrics"] = {"changes": lyric_changes}

    if notes:
        result["notes"] = notes

    consistency_warnings = check_adjustment_consistency(result)
    if consistency_warnings:
        if "notes" not in result:
            result["notes"] = []
        result["consistency_warnings"] = consistency_warnings

    return result


def check_adjustment_consistency(adjustments: dict[str, Any]) -> list[dict[str, Any]]:
    """Check for internal contradictions in adjustment recommendations."""
    warnings = []

    style_add = set(adjustments.get("style_prompt", {}).get("add_descriptors", []))
    style_remove = set(adjustments.get("style_prompt", {}).get("remove_patterns", []))
    exclude_add = set(adjustments.get("exclusions", {}).get("add", []))

    # Check for add/remove conflicts
    conflicts = style_add & style_remove
    if conflicts:
        warnings.append({
            "type": "add_remove_conflict",
            "detail": f"Descriptors appear in both add and remove: {', '.join(conflicts)}",
        })

    # Check for add/exclude conflicts
    for add_desc in style_add:
        for excl in exclude_add:
            # Simple substring check
            if add_desc.lower() in excl.lower() or excl.replace("no ", "").lower() in add_desc.lower():
                warnings.append({
                    "type": "add_exclude_conflict",
                    "detail": f"Adding '{add_desc}' conflicts with exclusion '{excl}'",
                })

    # Check style prompt estimated length
    total_add_chars = sum(len(d) + 2 for d in style_add)  # +2 for ", " separator
    if total_add_chars > CRITICAL_ZONE:
        warnings.append({
            "type": "critical_zone_overflow",
            "detail": f"Added descriptors total ~{total_add_chars} chars — prioritize most important for the first {CRITICAL_ZONE} chars of style prompt (critical zone)",
        })

    # Check exclusion estimated length
    total_excl_chars = sum(len(e) + 2 for e in exclude_add)
    if total_excl_chars > EXCLUSION_RECOMMENDED_MAX:
        warnings.append({
            "type": "exclusion_overflow",
            "detail": f"Exclusion additions total ~{total_excl_chars} chars — keep total exclusions under ~{EXCLUSION_RECOMMENDED_MAX} chars, prioritize 2-3 most important",
        })

    return warnings


def main():
    parser = argparse.ArgumentParser(
        description="Map feedback dimensions to Suno parameter adjustment recommendations.",
        epilog="""
Input JSON schema:
  Required:
    dimensions (array of objects) - Each with:
      dimension (string) - Feedback dimension (instrumentation, vocals, energy, tempo, production, vibe, music, structure, lyrics)
      direction (string) - Direction of the issue within the dimension

  Optional:
    tier (string) - User's Suno tier (free, pro, premier) — affects slider recommendations

Dimension/Direction combinations:
  instrumentation: too_much, too_little, wrong_type
  vocals: too_polished, too_rough, too_quiet, too_loud, wrong_character
  energy: too_high, too_low, flat
  tempo: too_fast, too_slow
  production: too_polished, too_rough, too_reverb, too_dry
  vibe: too_happy, too_dark, too_generic, too_weird
  music: general_issue
  structure: needs_bridge, chorus_weak, too_long, too_short
  lyrics: phrasing_unnatural, content_mismatch, vocal_style_inconsistent

Example:
  echo '{"dimensions": [{"dimension": "vocals", "direction": "too_polished"}, {"dimension": "energy", "direction": "too_low"}], "tier": "pro"}' | python3 map-adjustments.py --stdin
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--input", "-i", help="Path to dimensions JSON file")
    input_group.add_argument("--stdin", action="store_true", help="Read JSON from stdin")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output to stderr")

    args = parser.parse_args()

    try:
        if args.stdin:
            raw = sys.stdin.read()
        else:
            with open(args.input, "r") as f:
                raw = f.read()

        data = json.loads(raw)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(json.dumps({
            "script": "map-adjustments",
            "version": "1.0.0",
            "status": "fail",
            "findings": [{
                "severity": "critical",
                "category": "structure",
                "issue": str(e),
                "fix": "Provide valid JSON input",
            }],
            "summary": {"total": 1, "critical": 1, "high": 0, "medium": 0, "low": 0},
        }, indent=2))
        sys.exit(1)

    if not isinstance(data, dict) or "dimensions" not in data:
        print(json.dumps({
            "script": "map-adjustments",
            "version": "1.0.0",
            "status": "fail",
            "findings": [{
                "severity": "critical",
                "category": "structure",
                "issue": "Input must be a JSON object with a 'dimensions' array",
                "fix": 'Provide {"dimensions": [{"dimension": "...", "direction": "..."}]}',
            }],
            "summary": {"total": 1, "critical": 1, "high": 0, "medium": 0, "low": 0},
        }, indent=2))
        sys.exit(1)

    dimensions = data["dimensions"]
    tier = data.get("tier", "")

    adjustments = generate_adjustments(dimensions, tier)

    result = {
        "script": "map-adjustments",
        "version": "1.0.0",
        "status": "pass",
        "adjustments": adjustments,
        "input_dimensions": len(dimensions),
        "findings": [],
        "summary": {"total": 0, "critical": 0, "high": 0, "medium": 0, "low": 0},
    }

    if args.verbose:
        print(f"[map-adjustments] Processed {len(dimensions)} dimensions", file=sys.stderr)

    output_json = json.dumps(result, indent=2)
    if args.output:
        with open(args.output, "w") as f:
            f.write(output_json)
    else:
        print(output_json)

    sys.exit(0)


if __name__ == "__main__":
    main()
