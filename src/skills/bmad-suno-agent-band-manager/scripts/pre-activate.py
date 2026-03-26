#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Pre-activation script for Band Manager agent.

Checks first-run status, scaffolds sidecar directory if needed, and
renders the capability menu from bmad-manifest.json.

Usage:
    python3 scripts/pre-activate.py <project-root> [--scaffold] [-o OUTPUT]
    python3 scripts/pre-activate.py --help

Arguments:
    project-root    Project root directory path

Options:
    --scaffold      Create sidecar directory and static files if missing
    -o, --output    Write JSON output to file instead of stdout
"""

import argparse
import json
import sys
from pathlib import Path


def check_first_run(project_root: Path) -> bool:
    """Check if sidecar memory directory exists."""
    sidecar = project_root / "_bmad" / "_memory" / "band-manager-sidecar"
    return not sidecar.exists()


def scaffold_sidecar(project_root: Path) -> dict:
    """Create sidecar directory and static files."""
    sidecar = project_root / "_bmad" / "_memory" / "band-manager-sidecar"
    sidecar.mkdir(parents=True, exist_ok=True)

    created = []

    # access-boundaries.md - static template
    ab_path = sidecar / "access-boundaries.md"
    if not ab_path.exists():
        ab_path.write_text(
            "# Access Boundaries for Mac\n\n"
            "## Read Access\n"
            "- docs/band-profiles/\n"
            "- {project-root}/_bmad/_memory/band-manager-sidecar/\n\n"
            "## Write Access\n"
            "- {project-root}/_bmad/_memory/band-manager-sidecar/\n\n"
            "## Deny Zones\n"
            "- All other directories\n"
        )
        created.append("access-boundaries.md")

    # patterns.md - empty
    pat_path = sidecar / "patterns.md"
    if not pat_path.exists():
        pat_path.write_text("# Musical Patterns\n\nLearned preferences will appear here over time.\n")
        created.append("patterns.md")

    # chronology.md - empty
    chron_path = sidecar / "chronology.md"
    if not chron_path.exists():
        chron_path.write_text("# Session Chronology\n\nSession summaries will appear here.\n")
        created.append("chronology.md")

    return {"scaffolded": True, "files_created": created, "sidecar_path": str(sidecar)}


def render_menu(manifest_path: Path) -> str:
    """Render capability menu from bmad-manifest.json."""
    with open(manifest_path) as f:
        manifest = json.load(f)

    lines = ["What would you like to do today?\n"]
    for i, cap in enumerate(manifest.get("capabilities", []), 1):
        code = cap.get("menu-code", "??")
        desc = cap.get("description", "No description")
        lines.append(f"{i}. [{code}] {desc}")

    return "\n".join(lines)


def build_routing_table(manifest_path: Path) -> dict:
    """Build menu-code to capability routing table."""
    with open(manifest_path) as f:
        manifest = json.load(f)

    table = {}
    for i, cap in enumerate(manifest.get("capabilities", []), 1):
        code = cap.get("menu-code", "")
        entry = {"name": cap.get("name", "")}
        if "prompt" in cap:
            entry["type"] = "prompt"
            entry["target"] = cap["prompt"]
        elif "skill-name" in cap:
            entry["type"] = "skill"
            entry["target"] = cap["skill-name"]
        table[code] = entry
        table[str(i)] = entry

    return table


def main():
    parser = argparse.ArgumentParser(description="Band Manager pre-activation checks")
    parser.add_argument("project_root", help="Project root directory")
    parser.add_argument("--scaffold", action="store_true", help="Create sidecar if missing")
    parser.add_argument("-o", "--output", help="Output file path")
    args = parser.parse_args()

    project_root = Path(args.project_root)
    skill_dir = Path(__file__).parent.parent
    manifest_path = skill_dir / "bmad-manifest.json"

    result = {
        "first_run": check_first_run(project_root),
        "menu": render_menu(manifest_path),
        "routing_table": build_routing_table(manifest_path),
    }

    if args.scaffold and result["first_run"]:
        result["scaffold"] = scaffold_sidecar(project_root)

    output = json.dumps(result, indent=2)

    if args.output:
        Path(args.output).write_text(output)
        print(f"Results written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
    sys.exit(0)
