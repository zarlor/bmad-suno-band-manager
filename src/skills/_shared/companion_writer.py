#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Companion-doc writer: refresh canonical Markdown companion files in place.

Audio analysis scripts have canonical companion `.md` files that capture
their output as the project's authoritative reference. Without an
explicit refresh step, these files drift relative to the actual catalog
state — the scripts emit JSON to stdout and the `.md` companions stay
stale until someone manually refreshes them.

This helper makes the refresh a single function call. Scripts pass their
fresh Markdown content; the helper writes it into the companion file
between AUTOGEN markers, preserving any hand-curated sections that live
outside the markers.

Marker convention (HTML comments, valid in Markdown):

    <!-- AUTOGEN-START: <script-name> -->
    ...generated content...
    <!-- AUTOGEN-END -->

If the file does not yet have markers, this helper creates them on first
run, wrapping any existing content as auto-generated. To preserve a
hand-curated section, edit the file manually to move that section
outside the markers before the next refresh.
"""

import os
import sys
from pathlib import Path
from typing import Optional


MARKER_START_FMT = "<!-- AUTOGEN-START: {script} -->"
MARKER_END = "<!-- AUTOGEN-END -->"


def update_companion(
    companion_path: str,
    script_name: str,
    new_content: str,
    header: Optional[str] = None,
) -> dict:
    """Write `new_content` to the companion file between AUTOGEN markers.

    Args:
        companion_path: Path to the .md file (e.g., docs/playlist-sequencing-data.md)
        script_name: Identifier for the AUTOGEN marker (e.g., "playlist-sequencing-data")
        new_content: The fresh Markdown content to write inside the markers.
        header: Optional Markdown content to write ABOVE the markers (e.g., a
            title + generation timestamp). Only applied when creating the file
            from scratch.

    Returns:
        dict with keys: status ("created" | "refreshed" | "wrapped"),
        path, bytes_written.

    Behavior:
        - If file does not exist: create with header + markers + new_content.
        - If file exists with markers: replace content between markers, keep
          everything outside untouched.
        - If file exists without markers: wrap existing content in markers
          (status "wrapped"), then refresh content between markers with
          new_content. Hand-curated sections inside the wrapped block move
          along with it; user can edit afterward to split.
    """
    marker_start = MARKER_START_FMT.format(script=script_name)

    # Ensure parent dir exists
    parent = Path(companion_path).parent
    parent.mkdir(parents=True, exist_ok=True)

    if not os.path.exists(companion_path):
        # Create from scratch
        parts = []
        if header:
            parts.append(header.rstrip() + "\n\n")
        parts.append(marker_start + "\n")
        parts.append(new_content.rstrip() + "\n")
        parts.append(MARKER_END + "\n")
        body = "".join(parts)
        with open(companion_path, "w") as f:
            f.write(body)
        return {
            "status": "created",
            "path": companion_path,
            "bytes_written": len(body),
        }

    with open(companion_path, "r") as f:
        existing = f.read()

    if marker_start in existing and MARKER_END in existing:
        # Replace content between markers
        before = existing.split(marker_start)[0]
        after = existing.split(MARKER_END, 1)[1]
        body = (
            before
            + marker_start + "\n"
            + new_content.rstrip() + "\n"
            + MARKER_END
            + after
        )
        with open(companion_path, "w") as f:
            f.write(body)
        return {
            "status": "refreshed",
            "path": companion_path,
            "bytes_written": len(body),
        }

    # File exists but no markers — wrap existing content
    parts = []
    if header:
        parts.append(header.rstrip() + "\n\n")
    parts.append(marker_start + "\n")
    parts.append(new_content.rstrip() + "\n")
    parts.append(MARKER_END + "\n")
    parts.append("\n<!-- Previous content preserved below — edit to split out hand-curated sections -->\n\n")
    parts.append(existing)
    body = "".join(parts)
    with open(companion_path, "w") as f:
        f.write(body)
    return {
        "status": "wrapped",
        "path": companion_path,
        "bytes_written": len(body),
        "note": "Existing content preserved below the AUTOGEN block. Edit manually to move hand-curated sections.",
    }


# Canonical companion-file paths per script.
# When a script is invoked with --companion (no path arg), it uses these.
CANONICAL_COMPANION = {
    "playlist-sequencing-data": "docs/playlist-sequencing-data.md",
    "batch-full-analysis": "docs/catalog-analysis-report.md",
    "analyze-audio": "docs/audio-analysis-reference.md",
}


def resolve_companion_path(script_name: str, arg_value: Optional[str]) -> Optional[str]:
    """Resolve --companion arg value into an actual path.

    `arg_value` semantics:
        None       -> companion mode not requested
        ""         -> use canonical path (argparse `nargs="?", const=""`)
        "<path>"   -> use the user-supplied path
    """
    if arg_value is None:
        return None
    if arg_value == "":
        path = CANONICAL_COMPANION.get(script_name)
        if path is None:
            print(
                f"ERROR: no canonical companion path registered for {script_name!r}. "
                f"Pass an explicit --companion <path>.",
                file=sys.stderr,
            )
            sys.exit(1)
        return path
    return arg_value
