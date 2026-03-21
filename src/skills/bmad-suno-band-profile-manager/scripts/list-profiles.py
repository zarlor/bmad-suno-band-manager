# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# [tool.script.metadata]
# name = "list-profiles"
# version = "2.0.0"
# description = "Scans docs/band-profiles/ and returns summary of all saved band profiles"
# ///

"""List all band profiles in docs/band-profiles/.

Scans the directory for YAML files, extracts key fields from each,
and returns a structured JSON summary. Supports --check for single
profile existence verification.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml


def check_profile(profiles_dir: Path, profile_name: str) -> dict:
    """Check if a specific profile exists and return its metadata."""
    script_name = "list-profiles"

    # Try exact filename first, then derive from name
    candidates = [
        profiles_dir / profile_name,
        profiles_dir / f"{profile_name}.yaml",
        profiles_dir / f"{profile_name}.yml",
    ]

    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            stat = candidate.stat()
            try:
                with open(candidate) as f:
                    data = yaml.safe_load(f)
                name = data.get("name", candidate.stem) if isinstance(data, dict) else candidate.stem
            except (yaml.YAMLError, OSError):
                name = candidate.stem

            return {
                "script": script_name,
                "version": "2.0.0",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "status": "pass",
                "exists": True,
                "file": candidate.name,
                "path": str(candidate),
                "name": name,
                "size_bytes": stat.st_size,
                "last_modified": datetime.fromtimestamp(
                    stat.st_mtime, tz=timezone.utc
                ).isoformat(),
            }

    return {
        "script": script_name,
        "version": "2.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "pass",
        "exists": False,
        "query": profile_name,
        "profiles_dir": str(profiles_dir),
    }


def list_profiles(profiles_dir: Path) -> dict:
    """Scan profiles directory and return structured summary."""
    script_name = "list-profiles"

    if not profiles_dir.exists():
        return {
            "script": script_name,
            "version": "2.0.0",
            "profiles_dir": str(profiles_dir),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "pass",
            "profiles": [],
            "count": 0,
            "message": "No profiles directory found. No band profiles have been created yet."
        }

    yaml_files = sorted(profiles_dir.glob("*.yaml")) + sorted(profiles_dir.glob("*.yml"))
    profiles = []

    for yf in yaml_files:
        try:
            with open(yf) as f:
                data = yaml.safe_load(f)
            if not isinstance(data, dict):
                continue
            profiles.append({
                "file": yf.name,
                "name": data.get("name", yf.stem),
                "genre": data.get("genre", "unknown"),
                "mood": data.get("mood", ""),
                "model_preference": data.get("model_preference", "unknown"),
                "tier": data.get("tier", "unknown"),
                "instrumental": data.get("instrumental", False),
                "language": data.get("language", "English"),
                "creativity_default": data.get("creativity_default", "balanced"),
                "has_writer_voice": bool(data.get("writer_voice", {}).get("vocabulary")),
                "has_generation_history": bool(data.get("generation_history")),
                "version": data.get("version", 1)
            })
        except (yaml.YAMLError, OSError) as e:
            print(f"Warning: Could not read {yf}: {e}", file=sys.stderr)
            continue

    return {
        "script": script_name,
        "version": "2.0.0",
        "profiles_dir": str(profiles_dir),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "pass",
        "profiles": profiles,
        "count": len(profiles)
    }


def main():
    parser = argparse.ArgumentParser(
        description="List all band profiles in a directory.",
        epilog="Exit codes: 0=success, 2=error"
    )
    parser.add_argument(
        "profiles_dir",
        nargs="?",
        default="docs/band-profiles",
        help="Path to band profiles directory (default: docs/band-profiles)"
    )
    parser.add_argument("-o", "--output", help="Output file (defaults to stdout)")
    parser.add_argument("--verbose", action="store_true", help="Print diagnostics to stderr")
    parser.add_argument(
        "--check",
        metavar="PROFILE_NAME",
        help="Check if a specific profile exists and return its metadata"
    )
    args = parser.parse_args()

    profiles_dir = Path(args.profiles_dir)

    if args.verbose:
        print(f"Scanning: {profiles_dir}", file=sys.stderr)

    if args.check:
        result = check_profile(profiles_dir, args.check)
    else:
        result = list_profiles(profiles_dir)

    output = json.dumps(result, indent=2)

    if args.output:
        Path(args.output).write_text(output)
        if args.verbose:
            print(f"Results written to {args.output}", file=sys.stderr)
    else:
        print(output)

    sys.exit(0)


if __name__ == "__main__":
    main()
