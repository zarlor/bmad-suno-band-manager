#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Checks memory file sizes and recommends maintenance.

Usage:
    python3 scripts/check-memory-health.py <sidecar-path> [-o OUTPUT]
    python3 scripts/check-memory-health.py --help

Arguments:
    sidecar-path    Path to the sidecar memory directory

Options:
    -o, --output    Write JSON output to file instead of stdout
"""

import argparse
import json
import sys
from pathlib import Path

# Thresholds in characters
THRESHOLDS = {
    "index.md": 3000,
    "patterns.md": 5000,
    "chronology.md": 8000,
}


def check_health(sidecar_path: Path) -> dict:
    """Check memory file sizes and flag maintenance needs."""
    files = {}
    needs_pruning = []

    for name, threshold in THRESHOLDS.items():
        file_path = sidecar_path / name
        if file_path.exists():
            size = len(file_path.read_text())
            files[name] = {"size_chars": size, "threshold": threshold, "over_threshold": size > threshold}
            if size > threshold:
                needs_pruning.append(name)
        else:
            files[name] = {"exists": False}

    return {
        "sidecar_path": str(sidecar_path),
        "files": files,
        "needs_pruning": needs_pruning,
        "maintenance_recommended": len(needs_pruning) > 0,
        "recommendation": (
            f"Files exceeding size thresholds: {', '.join(needs_pruning)}. "
            "Consider condensing verbose entries and archiving old content."
            if needs_pruning
            else "Memory files are within healthy size limits."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description="Check memory file health")
    parser.add_argument("sidecar_path", help="Path to sidecar memory directory")
    parser.add_argument("-o", "--output", help="Output file path")
    args = parser.parse_args()

    sidecar = Path(args.sidecar_path)
    if not sidecar.exists():
        result = {"error": True, "message": f"Sidecar directory not found: {sidecar}"}
    else:
        result = check_health(sidecar)

    output = json.dumps(result, indent=2)

    if args.output:
        Path(args.output).write_text(output)
        print(f"Results written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
