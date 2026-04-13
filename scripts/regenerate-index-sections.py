#!/usr/bin/env python3
"""Regenerate the derivable sections of the Mac sidecar index.md.

Replaces the Recently Published and Catalog Status sections in
_bmad/_memory/band-manager-sidecar/index.md with content derived from
songbook frontmatter + body Status markers + playlist YAMLs.

The narrative sections (Current Work, Pending / Parked Work, Session History)
are preserved unchanged — only the derivable sections are rewritten.

Section boundaries are HTML comment markers:
    <!-- derived:recently-published:start -->
    ...auto-generated content...
    <!-- derived:recently-published:end -->

If the markers are missing from index.md, the script reports what to add and
exits non-zero without modifying the file.

Cross-platform: pure Python stdlib + PyYAML.

Usage:
    python3 scripts/regenerate-index-sections.py [project_root]
    python3 scripts/regenerate-index-sections.py --dry-run  # print diff only
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
STATUS_MARKER_RE = re.compile(
    r"\*\*Status:\s*(LOCKED|PUBLISHED|WIP)"
    r"(?:\s*[—-]\s*(?:v\d+\s+)?Published\s+(\d{4}-\d{2}-\d{2}))?"
    r"(?:\s*\((\d{4}-\d{2}-\d{2})\))?"
    r"\.?\s*(.*?)\*\*",
    re.DOTALL,
)

# How many entries to include in Recently Published
RECENT_LIMIT = 7

# Display name → band slug mapping for Catalog Status output
BAND_DISPLAY = {
    "lennys-voice": "Lenny's Voice",
    "solitary-fire": "Solitary Fire",
}


def parse_song(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    fm_match = FRONTMATTER_RE.match(text)
    if not fm_match:
        return None
    try:
        frontmatter = yaml.safe_load(fm_match.group(1)) or {}
    except yaml.YAMLError:
        return None

    body = text[fm_match.end() :]
    body_status = body_date = body_desc = None
    for m in STATUS_MARKER_RE.finditer(body):
        body_status = m.group(1)
        body_date = m.group(2) or m.group(3)
        body_desc = (m.group(4) or "").strip()

    # Truncate body_desc at the "Audio at" marker to get the short description.
    # Preserve the trailing period — the description ends on a natural sentence boundary,
    # and the caller appends " Songbook: ..." which needs the period for readability.
    if body_desc:
        audio_cut = re.search(r"\s*Audio at\b", body_desc)
        if audio_cut:
            body_desc = body_desc[: audio_cut.start()].rstrip()
        if body_desc and not body_desc.endswith((".", "!", "?")):
            body_desc += "."

    return {
        "path": path,
        "title": frontmatter.get("title", path.stem),
        "band": frontmatter.get("band_profile", ""),
        "frontmatter_status": frontmatter.get("status"),
        "frontmatter_date": str(frontmatter.get("date"))
        if frontmatter.get("date")
        else None,
        "body_status": body_status,
        "body_date": body_date,
        "body_desc": body_desc,
    }


def known_band_slugs(project_root: Path) -> set[str]:
    """Band profile YAML filenames (without extension) define valid band slugs."""
    profiles_dir = project_root / "docs" / "band-profiles"
    if not profiles_dir.is_dir():
        return set()
    return {p.stem for p in profiles_dir.glob("*.yaml")}


def load_all_songs(project_root: Path) -> list[dict]:
    songbook_root = project_root / "docs" / "songbook"
    songs = []
    if not songbook_root.is_dir():
        return songs
    valid_bands = known_band_slugs(project_root)
    for path in sorted(songbook_root.rglob("*.md")):
        song = parse_song(path)
        if song is None:
            continue
        # Songs whose band_profile doesn't match a known band profile YAML are
        # likely legacy / personal-project entries with custom metadata — they
        # shouldn't surface in catalog status or recently-published output.
        if valid_bands and song["band"] not in valid_bands:
            continue
        songs.append(song)
    return songs


def is_published(song: dict) -> bool:
    return song["frontmatter_status"] == "published" and song["body_status"] in (
        "LOCKED",
        "PUBLISHED",
    )


def publish_date(song: dict) -> str:
    """Authoritative publish date: body marker wins, frontmatter is fallback."""
    return song["body_date"] or song["frontmatter_date"] or ""


def generate_recently_published(songs: list[dict]) -> str:
    published = [s for s in songs if is_published(s)]
    published.sort(key=publish_date, reverse=True)
    published = published[:RECENT_LIMIT]

    lines = []
    for s in published:
        title = s["title"]
        date = publish_date(s)
        band_display = BAND_DISPLAY.get(s["band"], s["band"])
        desc = s["body_desc"] or f"{band_display}."
        path_display = s["path"].relative_to(s["path"].parents[3])
        lines.append(
            f"- **{title}** ({date}, PUBLISHED) — {desc} Songbook: "
            f"`{path_display.as_posix()}`."
        )
    return "\n".join(lines)


def generate_catalog_status(songs: list[dict], project_root: Path) -> str:
    # Per-band published counts
    per_band: dict[str, list[dict]] = {}
    for s in songs:
        per_band.setdefault(s["band"], []).append(s)

    lines = []
    for band_slug in sorted(per_band.keys()):
        band_display = BAND_DISPLAY.get(band_slug, band_slug)
        band_songs = per_band[band_slug]
        published = [s for s in band_songs if is_published(s)]
        published.sort(key=publish_date, reverse=True)

        # Check for a playlist YAML for this band
        playlist_path = project_root / "docs" / f"{band_slug}-playlist.yaml"
        playlist_count = None
        if playlist_path.exists():
            try:
                playlist = yaml.safe_load(playlist_path.read_text(encoding="utf-8"))
                if isinstance(playlist, dict):
                    playlist_count = len(playlist.get("tracks", []) or [])
            except yaml.YAMLError:
                pass

        # Line format depends on whether there's a playlist
        if playlist_count is not None and playlist_count > len(published):
            # Catalog with a playlist (like Solitary Fire's full album)
            lines.append(
                f"- **{band_display}:** {playlist_count}-track playlist "
                f"(songbook: {len(band_songs)} entries, {len(published)} with "
                f"complete LOCKED markers). See playlist YAML at "
                f"`docs/{band_slug}-playlist.yaml`."
            )
        else:
            # Catalog is the published list (like Lenny's Voice)
            titles = ", ".join(s["title"] for s in published)
            lines.append(
                f"- **{band_display}:** **{len(published)} published tracks** — {titles}."
            )
    return "\n".join(lines)


def replace_section(
    text: str, marker_name: str, new_content: str
) -> tuple[str, bool]:
    """Replace content between <!-- derived:NAME:start --> and :end markers.

    Returns (new_text, replaced). If markers aren't found, returns (text, False)
    so the caller can report what to add.
    """
    pattern = re.compile(
        rf"(<!--\s*derived:{re.escape(marker_name)}:start\s*-->)(.*?)"
        rf"(<!--\s*derived:{re.escape(marker_name)}:end\s*-->)",
        re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        return text, False
    replacement = f"{match.group(1)}\n\n{new_content}\n\n{match.group(3)}"
    return text[: match.start()] + replacement + text[match.end() :], True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Regenerate derivable sections of Mac sidecar index.md."
    )
    parser.add_argument(
        "project_root",
        nargs="?",
        default=".",
        help="Project root directory (default: current directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the regenerated sections without writing",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    if not project_root.is_dir():
        print(f"ERROR: project root not found: {project_root}", file=sys.stderr)
        return 2

    index_path = (
        project_root / "_bmad" / "_memory" / "band-manager-sidecar" / "index.md"
    )
    if not index_path.exists():
        print(f"ERROR: sidecar index not found at {index_path}", file=sys.stderr)
        return 2

    songs = load_all_songs(project_root)
    recently_published = generate_recently_published(songs)
    catalog_status = generate_catalog_status(songs, project_root)

    if args.dry_run:
        print("=== Recently Published ===\n")
        print(recently_published)
        print("\n=== Catalog Status ===\n")
        print(catalog_status)
        return 0

    text = index_path.read_text(encoding="utf-8")
    new_text = text
    missing_markers = []

    new_text, ok = replace_section(
        new_text, "recently-published", recently_published
    )
    if not ok:
        missing_markers.append("recently-published")

    new_text, ok = replace_section(new_text, "catalog-status", catalog_status)
    if not ok:
        missing_markers.append("catalog-status")

    if missing_markers:
        print(
            "ERROR: index.md is missing required section markers:", file=sys.stderr
        )
        for m in missing_markers:
            print(
                f"  <!-- derived:{m}:start --> ... <!-- derived:{m}:end -->",
                file=sys.stderr,
            )
        print(
            "\nAdd these markers around the sections to enable regeneration. "
            "See v1.6.5 release notes for migration guidance.",
            file=sys.stderr,
        )
        return 1

    if new_text == text:
        print("No changes needed — derivable sections already up to date.")
        return 0

    index_path.write_text(new_text, encoding="utf-8")
    print(f"Regenerated derivable sections in {index_path.relative_to(project_root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
