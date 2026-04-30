#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6.0"]
# ///

"""Validate a band profile YAML file against the expected schema.

Checks required fields, value constraints, tier/model consistency,
instrumental mode, style_baseline length, and new fields (language,
creativity_default, generation_history, studio_preferences).
Returns structured JSON findings.

Also supports --derive-filename to convert a band name to kebab-case filename.
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "_shared"))
from suno_constants import VALID_MODELS, VALID_TIERS, STYLE_PROMPT_LIMITS, STYLE_PROMPT_DEFAULT_MAX, FREE_TIER_MODEL

VALID_GENDERS = {"male", "female", "nonbinary", "any"}
VALID_CREATIVITY = {"conservative", "balanced", "experimental"}
STYLE_BASELINE_MAX = STYLE_PROMPT_DEFAULT_MAX
STYLE_BASELINE_MAX_V4 = STYLE_PROMPT_LIMITS["v4 Pro"]
MAX_GENERATION_HISTORY = 10


def derive_filename(band_name: str) -> str:
    """Convert a band name to kebab-case filename."""
    name = band_name.strip().lower()
    name = re.sub(r"[^a-z0-9\s-]", "", name)
    name = re.sub(r"[\s_]+", "-", name)
    name = re.sub(r"-+", "-", name)
    name = name.strip("-")
    return f"{name}.yaml"


def validate_profile(profile_path: Path) -> dict:
    """Validate a profile YAML file and return structured findings."""
    findings = []
    script_name = "validate-profile"

    if not profile_path.exists():
        return {
            "script": script_name,
            "version": "2.0.0",
            "skill_path": str(profile_path),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "fail",
            "findings": [{
                "severity": "critical",
                "category": "structure",
                "location": {"file": str(profile_path)},
                "issue": "Profile file does not exist",
                "fix": f"Create the profile at {profile_path}"
            }],
            "summary": {"total": 1, "critical": 1, "high": 0, "medium": 0, "low": 0}
        }

    try:
        with open(profile_path) as f:
            profile = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return {
            "script": script_name,
            "version": "2.0.0",
            "skill_path": str(profile_path),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "fail",
            "findings": [{
                "severity": "critical",
                "category": "structure",
                "location": {"file": str(profile_path)},
                "issue": f"Invalid YAML: {e}",
                "fix": "Fix YAML syntax errors"
            }],
            "summary": {"total": 1, "critical": 1, "high": 0, "medium": 0, "low": 0}
        }

    if not isinstance(profile, dict):
        return {
            "script": script_name,
            "version": "2.0.0",
            "skill_path": str(profile_path),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "fail",
            "findings": [{
                "severity": "critical",
                "category": "structure",
                "location": {"file": str(profile_path)},
                "issue": "Profile is not a YAML mapping",
                "fix": "Profile must be a YAML dictionary/mapping at the top level"
            }],
            "summary": {"total": 1, "critical": 1, "high": 0, "medium": 0, "low": 0}
        }

    is_instrumental = profile.get("instrumental", False) is True

    # Required top-level string fields
    for field in ["name", "genre", "mood", "model_preference", "tier", "style_baseline"]:
        val = profile.get(field)
        if not val or not isinstance(val, str) or not val.strip():
            findings.append({
                "severity": "critical",
                "category": "structure",
                "location": {"file": str(profile_path), "field": field},
                "issue": f"Required field '{field}' is missing or empty",
                "fix": f"Add a non-empty '{field}' field to the profile"
            })

    # model_preference validation
    model = profile.get("model_preference", "")
    if model and model not in VALID_MODELS:
        findings.append({
            "severity": "high",
            "category": "consistency",
            "location": {"file": str(profile_path), "field": "model_preference"},
            "issue": f"Invalid model_preference '{model}'",
            "fix": f"Must be one of: {', '.join(sorted(VALID_MODELS))}"
        })

    # tier validation
    tier = profile.get("tier", "")
    if tier and tier not in VALID_TIERS:
        findings.append({
            "severity": "high",
            "category": "consistency",
            "location": {"file": str(profile_path), "field": "tier"},
            "issue": f"Invalid tier '{tier}'",
            "fix": f"Must be one of: {', '.join(sorted(VALID_TIERS))}"
        })

    # style_baseline length — model-aware
    baseline = profile.get("style_baseline", "")
    if isinstance(baseline, str):
        max_len = STYLE_BASELINE_MAX_V4 if model == "v4 Pro" else STYLE_BASELINE_MAX
        if len(baseline) > max_len:
            findings.append({
                "severity": "high",
                "category": "consistency",
                "location": {"file": str(profile_path), "field": "style_baseline"},
                "issue": f"style_baseline is {len(baseline)} chars (max {max_len} for {model or 'this model'})",
                "fix": f"Trim style_baseline to {max_len} characters. Front-load essential descriptors in the first 200 chars."
            })

    # vocal section — skip required checks if instrumental
    vocal = profile.get("vocal", {})
    if not is_instrumental:
        if not isinstance(vocal, dict):
            findings.append({
                "severity": "high",
                "category": "structure",
                "location": {"file": str(profile_path), "field": "vocal"},
                "issue": "'vocal' must be a mapping",
                "fix": "Define vocal as a YAML mapping with gender, tone, delivery, energy fields"
            })
        else:
            for vfield in ["gender", "tone", "delivery", "energy"]:
                val = vocal.get(vfield)
                if not val or not isinstance(val, str) or not val.strip():
                    findings.append({
                        "severity": "high",
                        "category": "structure",
                        "location": {"file": str(profile_path), "field": f"vocal.{vfield}"},
                        "issue": f"Required vocal field '{vfield}' is missing or empty",
                        "fix": f"Add a non-empty 'vocal.{vfield}' field (or set instrumental: true for instrumental projects)"
                    })

            gender = vocal.get("gender", "")
            if gender and gender not in VALID_GENDERS:
                findings.append({
                    "severity": "medium",
                    "category": "consistency",
                    "location": {"file": str(profile_path), "field": "vocal.gender"},
                    "issue": f"Invalid vocal gender '{gender}'",
                    "fix": f"Must be one of: {', '.join(sorted(VALID_GENDERS))}"
                })
    elif isinstance(vocal, dict):
        # Instrumental but vocal present — validate gender if provided
        gender = vocal.get("gender", "")
        if gender and gender not in VALID_GENDERS:
            findings.append({
                "severity": "medium",
                "category": "consistency",
                "location": {"file": str(profile_path), "field": "vocal.gender"},
                "issue": f"Invalid vocal gender '{gender}'",
                "fix": f"Must be one of: {', '.join(sorted(VALID_GENDERS))}"
            })

    # Tier-model consistency
    if tier == "free" and model and model != FREE_TIER_MODEL:
        findings.append({
            "severity": "medium",
            "category": "consistency",
            "location": {"file": str(profile_path), "field": "model_preference"},
            "issue": f"Free tier can only use '{FREE_TIER_MODEL}', but profile specifies '{model}'",
            "fix": f"Change model_preference to '{FREE_TIER_MODEL}' or upgrade tier"
        })

    # Slider warnings for free tier
    sliders = profile.get("sliders", {})
    if tier == "free" and isinstance(sliders, dict) and sliders:
        has_values = any(
            k in ("weirdness", "style_influence") and v is not None and v != 50
            for k, v in sliders.items()
        )
        if has_values:
            findings.append({
                "severity": "medium",
                "category": "consistency",
                "location": {"file": str(profile_path), "field": "sliders"},
                "issue": "Slider values set but free tier does not support Weirdness/Style Influence sliders",
                "fix": "Remove sliders section or upgrade to Pro/Premier tier"
            })

    # Slider range validation
    if isinstance(sliders, dict):
        for sname in ["weirdness", "style_influence", "audio_influence"]:
            sval = sliders.get(sname)
            if sval is not None:
                if not isinstance(sval, (int, float)) or sval < 0 or sval > 100:
                    findings.append({
                        "severity": "medium",
                        "category": "consistency",
                        "location": {"file": str(profile_path), "field": f"sliders.{sname}"},
                        "issue": f"Slider '{sname}' value {sval} out of range",
                        "fix": "Must be an integer between 0 and 100"
                    })

    # Exclusion defaults length check
    exclusions = profile.get("exclusion_defaults", [])
    if isinstance(exclusions, list):
        if len(exclusions) > 5:
            findings.append({
                "severity": "low",
                "category": "consistency",
                "location": {"file": str(profile_path), "field": "exclusion_defaults"},
                "issue": f"{len(exclusions)} exclusions defined (recommended max 5)",
                "fix": "Too many negatives can confuse the model. Prioritize the most important."
            })

    # creativity_default validation
    creativity = profile.get("creativity_default")
    if creativity is not None:
        if not isinstance(creativity, str) or creativity not in VALID_CREATIVITY:
            findings.append({
                "severity": "medium",
                "category": "consistency",
                "location": {"file": str(profile_path), "field": "creativity_default"},
                "issue": f"Invalid creativity_default '{creativity}'",
                "fix": f"Must be one of: {', '.join(sorted(VALID_CREATIVITY))}"
            })

    # language validation
    language = profile.get("language")
    if language is not None:
        if not isinstance(language, str) or not language.strip():
            findings.append({
                "severity": "low",
                "category": "consistency",
                "location": {"file": str(profile_path), "field": "language"},
                "issue": "language field is present but empty",
                "fix": "Provide a language value (e.g., 'English', 'Spanish') or remove the field"
            })

    # generation_history validation
    gen_history = profile.get("generation_history")
    if gen_history is not None:
        if not isinstance(gen_history, list):
            findings.append({
                "severity": "low",
                "category": "structure",
                "location": {"file": str(profile_path), "field": "generation_history"},
                "issue": "generation_history must be a list",
                "fix": "Set generation_history to a list of snapshot entries"
            })
        elif len(gen_history) > MAX_GENERATION_HISTORY:
            findings.append({
                "severity": "low",
                "category": "consistency",
                "location": {"file": str(profile_path), "field": "generation_history"},
                "issue": f"generation_history has {len(gen_history)} entries (max {MAX_GENERATION_HISTORY})",
                "fix": f"Keep only the {MAX_GENERATION_HISTORY} most recent or significant entries"
            })

    # studio_preferences validation — warn if not premier
    studio = profile.get("studio_preferences", {})
    if isinstance(studio, dict) and any(v is not None and v != "" for v in studio.values()):
        if tier and tier != "premier":
            findings.append({
                "severity": "medium",
                "category": "consistency",
                "location": {"file": str(profile_path), "field": "studio_preferences"},
                "issue": f"Studio preferences set but '{tier}' tier does not support Studio features",
                "fix": "Remove studio_preferences or upgrade to Premier tier"
            })
        # Validate BPM if present
        bpm = studio.get("bpm")
        if bpm is not None and not isinstance(bpm, (int, float)):
            findings.append({
                "severity": "low",
                "category": "consistency",
                "location": {"file": str(profile_path), "field": "studio_preferences.bpm"},
                "issue": f"BPM must be a number, got {type(bpm).__name__}",
                "fix": "Set bpm to a numeric value (e.g., 120)"
            })

    # Build summary
    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for f in findings:
        severity_counts[f["severity"]] = severity_counts.get(f["severity"], 0) + 1

    # Per-band playlist YAML check: if the band has any songbook entries,
    # `docs/{band-slug}-playlist.yaml` MUST exist as the canonical source of
    # truth for playlist sequencing. Multi-band projects need this to keep
    # bands independent (see playlist-sequencing-methodology.md "Per-Band
    # Playlist YAML" section).
    band_slug = profile_path.stem  # e.g., docs/band-profiles/lennys-voice.yaml -> lennys-voice
    project_root = profile_path.parent.parent.parent  # band-profiles -> docs -> project_root
    songbook_dir = project_root / "docs" / "songbook" / band_slug
    playlist_yaml = project_root / "docs" / f"{band_slug}-playlist.yaml"
    if songbook_dir.is_dir() and any(songbook_dir.glob("*.md")):
        if not playlist_yaml.exists():
            findings.append({
                "severity": "high",
                "category": "structure",
                "location": {"file": str(profile_path), "expected_file": str(playlist_yaml)},
                "issue": (
                    f"Band has songbook entries at {songbook_dir} but no canonical "
                    f"playlist YAML at {playlist_yaml}. Per-band playlist YAML is the "
                    f"single source of truth for sequencing."
                ),
                "fix": (
                    f"Run `python3 src/skills/suno-band-profile-manager/scripts/scaffold-playlist.py "
                    f"{band_slug} --from-songbook` to bootstrap from songbook entries, then fill in "
                    f"audio file names and order. See profile-schema.md 'Per-Band Playlist YAML' section."
                ),
            })

    # Deprecated: in-profile `playlist:` block. Per v1.7.2 the band profile
    # should NOT carry playlist data — that lives in docs/{band-slug}-playlist.yaml.
    if "playlist" in profile and isinstance(profile["playlist"], dict):
        findings.append({
            "severity": "medium",
            "category": "deprecation",
            "location": {"file": str(profile_path), "field": "playlist"},
            "issue": (
                "The `playlist:` block in the band profile is DEPRECATED as of v1.7.2. "
                "Playlist data must live in docs/{band-slug}-playlist.yaml as the single "
                "source of truth, otherwise the two locations drift independently."
            ),
            "fix": (
                f"Move authoritative track list to docs/{band_slug}-playlist.yaml (or run "
                f"scaffold-playlist.py to bootstrap), then remove the `playlist:` block "
                f"from this profile YAML. Sequencing-history narrative notes can move to "
                f"the band's playlist-ordering.md if you maintain one."
            ),
        })

    # Re-tally severity counts after the playlist checks above
    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for f in findings:
        sev = f.get("severity", "low")
        if sev in severity_counts:
            severity_counts[sev] += 1

    status = "pass"
    if severity_counts["critical"] > 0:
        status = "fail"
    elif severity_counts["high"] > 0:
        status = "fail"
    elif severity_counts["medium"] > 0:
        status = "warning"

    return {
        "script": script_name,
        "version": "2.1.0",
        "skill_path": str(profile_path),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "findings": findings,
        "summary": {
            "total": len(findings),
            **severity_counts
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Validate a band profile YAML file against the profile schema.",
        epilog="Exit codes: 0=pass, 1=fail, 2=error"
    )
    parser.add_argument("profile_path", nargs="?", help="Path to the band profile YAML file")
    parser.add_argument("-o", "--output", help="Output file (defaults to stdout)")
    parser.add_argument("--verbose", action="store_true", help="Print diagnostics to stderr")
    parser.add_argument(
        "--derive-filename",
        metavar="BAND_NAME",
        help="Convert a band name to kebab-case filename and exit"
    )
    args = parser.parse_args()

    if args.derive_filename:
        result = {
            "band_name": args.derive_filename,
            "filename": derive_filename(args.derive_filename),
        }
        output = json.dumps(result, indent=2)
        if args.output:
            Path(args.output).write_text(output)
        else:
            print(output)
        sys.exit(0)

    if not args.profile_path:
        parser.error("profile_path is required when not using --derive-filename")

    profile_path = Path(args.profile_path)

    if args.verbose:
        print(f"Validating profile: {profile_path}", file=sys.stderr)

    result = validate_profile(profile_path)
    output = json.dumps(result, indent=2)

    if args.output:
        Path(args.output).write_text(output)
        if args.verbose:
            print(f"Results written to {args.output}", file=sys.stderr)
    else:
        print(output)

    if result["status"] == "fail":
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
