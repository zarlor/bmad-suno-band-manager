#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Validates file paths against access boundaries.

Usage:
    python3 scripts/validate-path.py <path> <operation> [--boundaries BOUNDARIES_FILE]
    python3 scripts/validate-path.py --help

Arguments:
    path           File path to validate
    operation      Operation type: read or write

Options:
    --boundaries   Path to access-boundaries.md (default: auto-detect from sidecar)
"""

import argparse
import json
import re
import sys
from pathlib import Path


def parse_boundaries(boundaries_path: Path) -> dict:
    """Parse access-boundaries.md into read/write/deny lists."""
    content = boundaries_path.read_text()
    boundaries = {"read": [], "write": [], "deny": []}
    current_section = None

    for line in content.splitlines():
        line = line.strip()
        if "Read Access" in line:
            current_section = "read"
        elif "Write Access" in line:
            current_section = "write"
        elif "Deny" in line:
            current_section = "deny"
        elif line.startswith("- ") and current_section and current_section != "deny":
            path_pattern = line[2:].strip()
            # Normalize: remove {project-root}/ prefix for comparison
            path_pattern = re.sub(r"\{project-root\}/?" , "", path_pattern)
            boundaries[current_section].append(path_pattern)

    return boundaries


def validate_path(file_path: str, operation: str, boundaries: dict) -> dict:
    """Check if a path is allowed for the given operation."""
    # Normalize the path
    normalized = re.sub(r"\{project-root\}/?", "", file_path)

    allowed_paths = boundaries.get(operation, [])
    for allowed in allowed_paths:
        if normalized.startswith(allowed):
            return {"allowed": True, "path": file_path, "operation": operation, "matched_rule": allowed}

    return {
        "allowed": False,
        "path": file_path,
        "operation": operation,
        "reason": f"Path not in {operation} allowlist",
        "allowed_paths": allowed_paths,
    }


def main():
    parser = argparse.ArgumentParser(description="Validate paths against access boundaries")
    parser.add_argument("path", help="File path to validate")
    parser.add_argument("operation", choices=["read", "write"], help="Operation type")
    parser.add_argument("--boundaries", help="Path to access-boundaries.md")
    args = parser.parse_args()

    if args.boundaries:
        boundaries_path = Path(args.boundaries)
    else:
        print(json.dumps({"error": True, "message": "No --boundaries file specified"}))
        sys.exit(1)

    if not boundaries_path.exists():
        print(json.dumps({"error": True, "message": f"Boundaries file not found: {boundaries_path}"}))
        sys.exit(1)

    boundaries = parse_boundaries(boundaries_path)
    result = validate_path(args.path, args.operation, boundaries)
    print(json.dumps(result, indent=2))

    if not result.get("allowed", False):
        sys.exit(1)


if __name__ == "__main__":
    main()
