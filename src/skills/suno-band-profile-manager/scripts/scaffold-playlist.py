#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Scaffold a per-band playlist YAML.

Each band in the project owns exactly one canonical
`docs/{band-slug}-playlist.yaml` that lists the tracks in their playlist
order with a name → audio-file mapping. This file is the authoritative
input to `playlist-sequencing-data.py` and the single source of truth for
sequencing decisions.

This script bootstraps that YAML for a band that doesn't yet have one. It
runs in two modes:

  --empty (default)
      Write a template with no tracks listed. The user fills in the order.

  --from-songbook
      Scan `docs/songbook/{band-slug}/` for published songbook entries and
      pre-populate the tracks list with their titles. Audio file fields
      are left as TODO comments — the user must fill in actual filenames
      from `docs/audio/` because songbook frontmatter does not reliably
      track the audio filename.

Usage:
    scaffold-playlist.py <band-slug> [--from-songbook] [--project-root PATH]

Exit codes:
  0 = playlist YAML written (or already existed and --force not passed)
  1 = error (band-slug invalid, project root missing, etc.)
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


def _band_name_from_slug(slug: str) -> str:
    """Convert kebab-case slug to a Title-Cased album name as a default.
    Users typically edit this after scaffolding."""
    parts = slug.replace("_", "-").split("-")
    return " ".join(p.capitalize() for p in parts if p)


def _extract_title_from_songbook(md_path: Path) -> str | None:
    """Read a songbook .md file's frontmatter and return its `title` field.
    Returns None if the file lacks a frontmatter title."""
    try:
        with open(md_path, "r") as f:
            content = f.read()
    except OSError:
        return None
    if not content.startswith("---"):
        return None
    end = content.find("\n---", 3)
    if end < 0:
        return None
    fm = content[3:end]
    for line in fm.splitlines():
        m = re.match(r'^\s*title\s*:\s*"?(.*?)"?\s*$', line)
        if m:
            return m.group(1).strip()
    return None


def _is_published(md_path: Path) -> bool:
    """Heuristic: check frontmatter for `status: published` or similar."""
    try:
        with open(md_path, "r") as f:
            content = f.read()
    except OSError:
        return False
    if not content.startswith("---"):
        return False
    end = content.find("\n---", 3)
    if end < 0:
        return False
    fm = content[3:end].lower()
    return "status: published" in fm or "status: \"published\"" in fm


def discover_songbook_tracks(project_root: Path, band_slug: str) -> list[dict]:
    """Find published songbook entries for the band and return their titles."""
    band_dir = project_root / "docs" / "songbook" / band_slug
    if not band_dir.is_dir():
        return []
    tracks = []
    for md_path in sorted(band_dir.glob("*.md")):
        if not _is_published(md_path):
            continue
        title = _extract_title_from_songbook(md_path)
        if title:
            tracks.append({"name": title, "songbook_path": str(md_path.relative_to(project_root))})
    return tracks


def render_playlist_yaml(album_name: str, tracks: list[dict], from_songbook: bool) -> str:
    """Render the playlist YAML content as a string."""
    lines = []
    lines.append(f"# Playlist order for {album_name} — authoritative source.")
    lines.append("# This file is the SINGLE source of truth for the band's track sequence.")
    lines.append("# Do NOT duplicate this list in other files (band profile YAML, ordering doc,")
    lines.append("# voice context). Those files derive from or reference this YAML.")
    lines.append("#")
    lines.append("# When a song is published, add it to this file in the same write batch as")
    lines.append("# the songbook entry. When the order changes, update this file first; the")
    lines.append("# sequencing script's per-album companion .md is auto-refreshed from this.")
    lines.append(f'album: "{album_name}"')
    lines.append("tracks:")
    if not tracks:
        lines.append("  # Add tracks below as they are published. Each track needs:")
        lines.append('  #   - name: "<song title as it appears in the songbook>"')
        lines.append('  #     file: "<exact filename in docs/audio/, e.g. My Song.mp3>"')
        lines.append("  # Order in this list = playlist order.")
    else:
        for t in tracks:
            lines.append(f'  - name: "{t["name"]}"')
            if from_songbook:
                # We discovered the song from songbook but don't know the audio filename.
                # User must fill this in.
                lines.append("    file: \"\"  # TODO: set to the actual filename in docs/audio/")
                if t.get("songbook_path"):
                    lines.append(f"    # songbook: {t['songbook_path']}")
            else:
                lines.append('    file: ""')
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a per-band playlist YAML at docs/{band-slug}-playlist.yaml.",
    )
    parser.add_argument(
        "band_slug",
        help="The band's filename slug (kebab-case). Matches the band profile filename: docs/band-profiles/{band-slug}.yaml.",
    )
    parser.add_argument(
        "--from-songbook",
        action="store_true",
        help="Pre-populate tracks from existing songbook entries at docs/songbook/{band-slug}/.",
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Project root (default: current directory).",
    )
    parser.add_argument(
        "--album-name",
        help="Album/band name to use in the YAML (default: derived from slug).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing playlist YAML if present.",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    if not project_root.is_dir():
        print(json.dumps({"status": "error", "message": f"Project root not found: {project_root}"}))
        sys.exit(1)

    slug = args.band_slug.strip()
    if not re.match(r"^[a-z0-9][a-z0-9_-]*$", slug):
        print(json.dumps({
            "status": "error",
            "message": (
                f"Invalid band slug {slug!r}. Use lowercase kebab-case "
                f"(letters, digits, hyphens, underscores; must start with letter/digit)."
            ),
        }))
        sys.exit(1)

    target = project_root / "docs" / f"{slug}-playlist.yaml"
    if target.exists() and not args.force:
        print(json.dumps({
            "status": "exists",
            "message": f"Playlist YAML already exists at {target}. Use --force to overwrite.",
            "path": str(target.relative_to(project_root)),
        }))
        sys.exit(0)

    album_name = args.album_name or _band_name_from_slug(slug)
    tracks: list[dict] = []
    if args.from_songbook:
        tracks = discover_songbook_tracks(project_root, slug)

    body = render_playlist_yaml(album_name, tracks, from_songbook=args.from_songbook)
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "w") as f:
        f.write(body)

    print(json.dumps({
        "status": "created" if not args.force else "overwritten",
        "path": str(target.relative_to(project_root)),
        "album": album_name,
        "tracks_seeded": len(tracks),
        "from_songbook": args.from_songbook,
        "note": (
            "Audio filenames left as empty strings — fill in from docs/audio/ before "
            "running the sequencing script."
        ) if tracks else (
            "Empty template written. Add tracks as you publish them."
        ),
    }))


if __name__ == "__main__":
    main()
