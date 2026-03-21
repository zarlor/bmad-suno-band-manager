# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# [tool.script.metadata]
# name = "diff-profiles"
# version = "1.0.0"
# description = "Compares two band profile YAML files and returns a structured diff of changes"
# ///

"""Compare two band profile YAML files and return structured differences.

Takes an original and modified profile, compares field-by-field,
and returns a structured JSON diff showing changed, added, and
removed fields. Handles nested structures (vocal, sliders, etc.).
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml


def flatten_dict(d: dict, prefix: str = "") -> dict:
    """Flatten a nested dict into dot-notation keys."""
    items = {}
    for k, v in d.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, key))
        else:
            items[key] = v
    return items


def diff_profiles(original_path: Path, modified_path: Path) -> dict:
    """Compare two profile YAML files and return structured diff."""
    script_name = "diff-profiles"
    errors = []

    for label, path in [("original", original_path), ("modified", modified_path)]:
        if not path.exists():
            errors.append(f"{label} file does not exist: {path}")

    if errors:
        return {
            "script": script_name,
            "version": "1.0.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "fail",
            "errors": errors,
        }

    try:
        with open(original_path) as f:
            original = yaml.safe_load(f) or {}
        with open(modified_path) as f:
            modified = yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        return {
            "script": script_name,
            "version": "1.0.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "fail",
            "errors": [f"YAML parse error: {e}"],
        }

    if not isinstance(original, dict) or not isinstance(modified, dict):
        return {
            "script": script_name,
            "version": "1.0.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "fail",
            "errors": ["Both files must be YAML mappings"],
        }

    flat_orig = flatten_dict(original)
    flat_mod = flatten_dict(modified)

    all_keys = set(flat_orig.keys()) | set(flat_mod.keys())

    changed = []
    added = []
    removed = []

    for key in sorted(all_keys):
        in_orig = key in flat_orig
        in_mod = key in flat_mod

        if in_orig and in_mod:
            if flat_orig[key] != flat_mod[key]:
                changed.append({
                    "field": key,
                    "old": flat_orig[key],
                    "new": flat_mod[key],
                })
        elif in_mod and not in_orig:
            added.append({
                "field": key,
                "value": flat_mod[key],
            })
        elif in_orig and not in_mod:
            removed.append({
                "field": key,
                "value": flat_orig[key],
            })

    has_changes = bool(changed or added or removed)

    return {
        "script": script_name,
        "version": "1.0.0",
        "original": str(original_path),
        "modified": str(modified_path),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "pass",
        "has_changes": has_changes,
        "changed": changed,
        "added": added,
        "removed": removed,
        "summary": {
            "total_changes": len(changed) + len(added) + len(removed),
            "fields_changed": len(changed),
            "fields_added": len(added),
            "fields_removed": len(removed),
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Compare two band profile YAML files and return a structured diff.",
        epilog="Exit codes: 0=success, 1=fail"
    )
    parser.add_argument("original", help="Path to the original profile YAML file")
    parser.add_argument("modified", help="Path to the modified profile YAML file")
    parser.add_argument("-o", "--output", help="Output file (defaults to stdout)")
    parser.add_argument("--verbose", action="store_true", help="Print diagnostics to stderr")
    args = parser.parse_args()

    original_path = Path(args.original)
    modified_path = Path(args.modified)

    if args.verbose:
        print(f"Comparing: {original_path} -> {modified_path}", file=sys.stderr)

    result = diff_profiles(original_path, modified_path)
    output = json.dumps(result, indent=2)

    if args.output:
        Path(args.output).write_text(output)
        if args.verbose:
            print(f"Results written to {args.output}", file=sys.stderr)
    else:
        print(output)

    sys.exit(0 if result["status"] == "pass" else 1)


if __name__ == "__main__":
    main()
