#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Parse and validate structured feedback input for headless mode.

Accepts JSON feedback input and extracts structured dimensions for
the Feedback Elicitor skill. Validates required fields and normalizes
the input structure for downstream processing.

Exit codes:
  0 = valid input, structured output returned
  1 = validation failed (invalid structure or missing required fields)
  2 = runtime error
"""

import argparse
import json
import sys
from typing import Any

VALID_DIMENSIONS = [
    "music",
    "vocals",
    "energy",
    "structure",
    "lyrics",
    "vibe",
    "production",
    "tempo",
    "instrumentation",
    "length",
    "quality",
]

# Known models — used for enrichment, not hard validation
VALID_MODELS = [
    "v4.5-all",
    "v4 Pro",
    "v4.5 Pro",
    "v4.5+ Pro",
    "v5 Pro",
]

VALID_FEEDBACK_TYPES = ["clear", "positive", "vague", "contradictory", "technical"]


def validate_feedback_input(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Validate structured feedback input and return findings."""
    findings = []

    # feedback_text is required
    if "feedback_text" not in data or not data["feedback_text"].strip():
        findings.append({
            "severity": "critical",
            "category": "structure",
            "location": {"field": "feedback_text"},
            "issue": "Missing or empty feedback_text field",
            "fix": "Provide feedback_text with the user's feedback about their Suno generation",
        })

    # Validate optional fields if present
    if "model" in data and data["model"] not in VALID_MODELS:
        findings.append({
            "severity": "info",
            "category": "consistency",
            "location": {"field": "model"},
            "issue": f"Unrecognized model '{data['model']}' — recommendations may not be model-optimized. Known models: {', '.join(VALID_MODELS)}",
            "fix": "This is informational — the model name will be passed through. Known models receive model-specific recommendations.",
        })

    if "dimensions" in data:
        if not isinstance(data["dimensions"], list):
            findings.append({
                "severity": "high",
                "category": "structure",
                "location": {"field": "dimensions"},
                "issue": "dimensions must be an array",
                "fix": "Provide dimensions as an array of strings",
            })
        else:
            for dim in data["dimensions"]:
                if dim not in VALID_DIMENSIONS:
                    findings.append({
                        "severity": "low",
                        "category": "consistency",
                        "location": {"field": "dimensions", "value": dim},
                        "issue": f"Unknown dimension '{dim}'. Valid: {', '.join(VALID_DIMENSIONS)}",
                        "fix": f"Use one of: {', '.join(VALID_DIMENSIONS)}",
                    })

    if "feedback_type" in data and data["feedback_type"] not in VALID_FEEDBACK_TYPES:
        findings.append({
            "severity": "medium",
            "category": "consistency",
            "location": {"field": "feedback_type"},
            "issue": f"Unknown feedback_type '{data['feedback_type']}'. Valid: {', '.join(VALID_FEEDBACK_TYPES)}",
            "fix": f"Use one of: {', '.join(VALID_FEEDBACK_TYPES)}",
        })

    if "slider_settings" in data:
        sliders = data["slider_settings"]
        if not isinstance(sliders, dict):
            findings.append({
                "severity": "medium",
                "category": "structure",
                "location": {"field": "slider_settings"},
                "issue": "slider_settings must be an object",
                "fix": "Provide as {\"weirdness\": 50, \"style_influence\": 50}",
            })
        else:
            for key in ["weirdness", "style_influence"]:
                if key in sliders:
                    val = sliders[key]
                    if not isinstance(val, (int, float)) or val < 0 or val > 100:
                        findings.append({
                            "severity": "medium",
                            "category": "consistency",
                            "location": {"field": f"slider_settings.{key}"},
                            "issue": f"{key} must be a number between 0 and 100",
                            "fix": f"Set {key} to a value between 0 and 100",
                        })

    return findings


def extract_structured_output(data: dict[str, Any]) -> dict[str, Any]:
    """Extract and normalize structured feedback for downstream processing."""
    output = {
        "feedback_text": data.get("feedback_text", "").strip(),
        "context": {
            "original_style_prompt": data.get("original_style_prompt", ""),
            "original_lyrics": data.get("original_lyrics", ""),
            "band_profile": data.get("band_profile", ""),
            "model": data.get("model", ""),
            "slider_settings": data.get("slider_settings", {}),
            "intent": data.get("intent", ""),
        },
        "pre_categorized": {
            "feedback_type": data.get("feedback_type", ""),
            "dimensions": data.get("dimensions", []),
        },
    }

    # Strip empty context fields
    output["context"] = {k: v for k, v in output["context"].items() if v}
    output["pre_categorized"] = {k: v for k, v in output["pre_categorized"].items() if v}

    return output


def main():
    parser = argparse.ArgumentParser(
        description="Parse and validate structured feedback input for Suno Feedback Elicitor headless mode.",
        epilog="""
Input JSON schema:
  Required:
    feedback_text (string) - The user's feedback about their Suno generation

  Optional context:
    original_style_prompt (string) - Style prompt used for generation
    original_lyrics (string) - Lyrics used for generation
    band_profile (string) - Band profile name used
    model (string) - Suno model used (v4.5-all, v4 Pro, v4.5 Pro, v4.5+ Pro, v5 Pro)
    slider_settings (object) - {weirdness: 0-100, style_influence: 0-100}
    intent (string) - What the user was going for

  Optional pre-categorization:
    feedback_type (string) - clear, positive, vague, contradictory
    dimensions (array) - Problem dimensions: music, vocals, energy, structure, lyrics, vibe, production, tempo, instrumentation

Example:
  echo '{"feedback_text": "The guitar is too loud", "model": "v5 Pro"}' | python3 parse-feedback.py --stdin
  python3 parse-feedback.py --input feedback.json
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--input", "-i", help="Path to feedback JSON file")
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
    except json.JSONDecodeError as e:
        result = {
            "script": "parse-feedback",
            "version": "1.0.0",
            "status": "fail",
            "findings": [{
                "severity": "critical",
                "category": "structure",
                "location": {"field": "root"},
                "issue": f"Invalid JSON: {e}",
                "fix": "Provide valid JSON input",
            }],
            "summary": {"total": 1, "critical": 1, "high": 0, "medium": 0, "low": 0, "info": 0},
        }
        output_json = json.dumps(result, indent=2)
        if args.output:
            with open(args.output, "w") as f:
                f.write(output_json)
        else:
            print(output_json)
        sys.exit(1)
    except FileNotFoundError:
        print(json.dumps({
            "script": "parse-feedback",
            "version": "1.0.0",
            "status": "fail",
            "findings": [{
                "severity": "critical",
                "category": "structure",
                "location": {"field": "input"},
                "issue": f"File not found: {args.input}",
                "fix": "Provide a valid file path",
            }],
            "summary": {"total": 1, "critical": 1, "high": 0, "medium": 0, "low": 0, "info": 0},
        }, indent=2))
        sys.exit(1)

    if not isinstance(data, dict):
        result = {
            "script": "parse-feedback",
            "version": "1.0.0",
            "status": "fail",
            "findings": [{
                "severity": "critical",
                "category": "structure",
                "location": {"field": "root"},
                "issue": "Input must be a JSON object",
                "fix": "Provide a JSON object with at least a feedback_text field",
            }],
            "summary": {"total": 1, "critical": 1, "high": 0, "medium": 0, "low": 0, "info": 0},
        }
        output_json = json.dumps(result, indent=2)
        if args.output:
            with open(args.output, "w") as f:
                f.write(output_json)
        else:
            print(output_json)
        sys.exit(1)

    findings = validate_feedback_input(data)

    has_critical = any(f["severity"] == "critical" for f in findings)
    has_high = any(f["severity"] == "high" for f in findings)
    has_actionable = any(f["severity"] in ("critical", "high", "medium", "low") for f in findings)

    if has_critical or has_high:
        status = "fail"
    elif has_actionable:
        status = "warning"
    else:
        status = "pass"

    structured_output = extract_structured_output(data) if not has_critical else None

    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        sev = f["severity"]
        if sev in severity_counts:
            severity_counts[sev] += 1

    result = {
        "script": "parse-feedback",
        "version": "1.0.0",
        "status": status,
        "findings": findings,
        "summary": {
            "total": len(findings),
            **severity_counts,
        },
    }

    if structured_output:
        result["parsed"] = structured_output

    if args.verbose:
        print(f"[parse-feedback] Status: {status}, Findings: {len(findings)}", file=sys.stderr)

    output_json = json.dumps(result, indent=2)
    if args.output:
        with open(args.output, "w") as f:
            f.write(output_json)
        if args.verbose:
            print(f"[parse-feedback] Output written to {args.output}", file=sys.stderr)
    else:
        print(output_json)

    sys.exit(0 if status in ("pass", "warning") else 1)


if __name__ == "__main__":
    main()
