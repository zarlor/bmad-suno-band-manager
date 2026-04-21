#!/usr/bin/env python3
"""Validate the Mac sidecar index against songbook + band-profile ground truth.

Reads every songbook entry and band profile, derives the ground-truth catalog
state, and compares it against the claims in the sidecar index.md. Reports
drift as structured findings. Exits 0 on clean, 1 on drift (CI-friendly).

Cross-platform: pure Python stdlib + PyYAML (already a module dependency).

Usage:
    python3 scripts/validate-sidecar.py [project_root]
    python3 scripts/validate-sidecar.py --format json
    python3 scripts/validate-sidecar.py --warn-only  # exit 0 even with findings

Checks performed:
    1. Songbook internal consistency — frontmatter status/date vs. body status marker
    2. Audio file existence for published songs
    3. Sidecar Recently Published list matches songbook ground truth
    4. Sidecar Catalog Status counts match actual songbook counts
    5. Playlist YAML track count matches songbook count for that band
    6. Markdown cross-references in docs/ resolve to existing files

Called by:
    - pack-portable.{sh,ps1} before packing (gates sync)
    - save-memory workflow after index.md writes (validates derivation)
    - Standalone by user any time for a consistency check
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print(
        json.dumps(
            {
                "status": "error",
                "message": "PyYAML required. Install with: pip install pyyaml",
            }
        )
    )
    sys.exit(2)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class Song:
    path: Path
    band: str
    title: str
    frontmatter_status: str | None
    frontmatter_date: str | None
    body_status: str | None  # "LOCKED", "PUBLISHED", "WIP", or None
    body_date: str | None
    body_description: str | None
    audio_references: list[str] = field(default_factory=list)

    @property
    def is_published(self) -> bool:
        """Single source of truth: requires frontmatter + body to agree on published."""
        frontmatter_published = self.frontmatter_status == "published"
        body_published = self.body_status in ("LOCKED", "PUBLISHED")
        return frontmatter_published and body_published


@dataclass
class Finding:
    category: str  # "songbook_drift" | "audio_missing" | "index_drift" | "playlist_drift" | "cross_reference_missing"
    severity: str  # "error" | "warning"
    path: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "category": self.category,
            "severity": self.severity,
            "path": self.path,
            "message": self.message,
        }


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
STATUS_MARKER_RE = re.compile(
    r"\*\*Status:\s*(LOCKED|PUBLISHED|WIP)"
    r"(?:\s*[—-]\s*(?:v\d+\s+)?Published\s+(\d{4}-\d{2}-\d{2}))?"
    r"(?:\s*\((\d{4}-\d{2}-\d{2})\))?"
    r"\.?\s*(.*?)\*\*",
    re.DOTALL,
)
AUDIO_REF_RE = re.compile(r"`(docs/audio/[^`]+\.(?:mp3|wav|flac|m4a))`")


def parse_song(path: Path, project_root: Path) -> tuple[Song | None, str | None]:
    """Parse a songbook markdown file.

    Returns a (song, error) pair:
      - (Song, None)       when parsing succeeds
      - (None, None)       when the file has no frontmatter (likely not a song)
      - (None, error_msg)  when YAML frontmatter fails to parse
    """
    text = path.read_text(encoding="utf-8")
    fm_match = FRONTMATTER_RE.match(text)
    if not fm_match:
        return None, None

    try:
        frontmatter = yaml.safe_load(fm_match.group(1)) or {}
    except yaml.YAMLError as exc:
        return None, f"YAML frontmatter parse error: {exc}"

    body = text[fm_match.end() :]

    # Body status marker: walk matches and pick the last one (body markers
    # appear after Generation Log notes that may reference earlier WIP states).
    body_status = body_date = body_description = None
    for m in STATUS_MARKER_RE.finditer(body):
        body_status = m.group(1)
        body_date = m.group(2) or m.group(3)
        body_description = (m.group(4) or "").strip()

    audio_refs = AUDIO_REF_RE.findall(body)

    band = frontmatter.get("band_profile", "")
    title = frontmatter.get("title", path.stem)

    return (
        Song(
            path=path.relative_to(project_root),
            band=band,
            title=str(title),
            frontmatter_status=frontmatter.get("status"),
            frontmatter_date=str(frontmatter.get("date")) if frontmatter.get("date") else None,
            body_status=body_status,
            body_date=body_date,
            body_description=body_description,
            audio_references=audio_refs,
        ),
        None,
    )


def load_all_songs(project_root: Path) -> tuple[list[Song], list[Finding]]:
    """Load every songbook entry plus any parse-failure findings.

    Songs whose YAML frontmatter fails to parse used to be silently dropped,
    which hid songs from derived sections without surfacing any error (issue #29).
    Each parse failure now becomes a songbook_drift error so sync can't pass
    while a song is invisible to the index generator.
    """
    songbook_root = project_root / "docs" / "songbook"
    if not songbook_root.is_dir():
        return [], []
    songs: list[Song] = []
    parse_findings: list[Finding] = []
    for path in sorted(songbook_root.rglob("*.md")):
        song, error = parse_song(path, project_root)
        if song is not None:
            songs.append(song)
        elif error is not None:
            parse_findings.append(
                Finding(
                    category="songbook_drift",
                    severity="error",
                    path=str(path.relative_to(project_root)),
                    message=(
                        f"{error} — song will be skipped by derived-section "
                        "generators. Fix by quoting values containing "
                        "special YAML characters (e.g. inner brackets)."
                    ),
                )
            )
    return songs, parse_findings


# ---------------------------------------------------------------------------
# Check implementations
# ---------------------------------------------------------------------------


def check_songbook_consistency(song: Song) -> list[Finding]:
    """Frontmatter and body must agree on status + date."""
    findings: list[Finding] = []
    path = str(song.path)

    frontmatter_published = song.frontmatter_status == "published"
    body_published = song.body_status in ("LOCKED", "PUBLISHED")

    if song.body_status is None and frontmatter_published:
        # Missing marker is data incompleteness, not contradiction.
        # Warning keeps pre-existing songbook gaps from blocking sync.
        findings.append(
            Finding(
                category="songbook_drift",
                severity="warning",
                path=path,
                message="frontmatter status=published but no body Status marker found",
            )
        )
    elif frontmatter_published != body_published and song.body_status is not None:
        findings.append(
            Finding(
                category="songbook_drift",
                severity="error",
                path=path,
                message=(
                    f"frontmatter status={song.frontmatter_status!r} disagrees with "
                    f"body Status: {song.body_status}"
                ),
            )
        )

    if (
        frontmatter_published
        and body_published
        and song.frontmatter_date
        and song.body_date
        and song.frontmatter_date != song.body_date
    ):
        findings.append(
            Finding(
                category="songbook_drift",
                severity="error",
                path=path,
                message=(
                    f"frontmatter date={song.frontmatter_date} disagrees with "
                    f"body Published {song.body_date}"
                ),
            )
        )

    return findings


def check_audio_exists(song: Song, project_root: Path) -> list[Finding]:
    """Every audio reference in a published song must exist on disk."""
    if not song.is_published:
        return []
    findings: list[Finding] = []
    for rel in song.audio_references:
        audio_path = project_root / rel
        if not audio_path.exists():
            findings.append(
                Finding(
                    category="audio_missing",
                    severity="warning",
                    path=str(song.path),
                    message=f"referenced audio file not found: {rel}",
                )
            )
    return findings


def check_index_recently_published(
    index_text: str, songs: list[Song]
) -> list[Finding]:
    """Every song listed in Recently Published must match songbook ground truth."""
    findings: list[Finding] = []
    index_path = "_bmad/_memory/band-manager-sidecar/index.md"

    # Extract the Recently Published block (from that heading until the next ## heading)
    recent_match = re.search(
        r"^##\s+Recently Published\s*\n(.*?)(?=\n##\s)",
        index_text,
        re.MULTILINE | re.DOTALL,
    )
    if not recent_match:
        return []

    block = recent_match.group(1)

    # Each entry looks like: - **Title** (YYYY-MM-DD, STATUS) — ...
    entry_re = re.compile(
        r"-\s+\*\*(?P<title>[^*]+?)\*\*\s*"
        r"\((?P<date>\d{4}-\d{2}-\d{2}),\s*(?P<status>[A-Za-z]+)",
    )

    for match in entry_re.finditer(block):
        title = match.group("title").strip()
        claimed_date = match.group("date")
        claimed_status = match.group("status").upper()

        # Match title allowing for minor suffix (e.g., "Observation v2" matches "Observation").
        # Multiple songs can share a title across bands (same poem, different interpretations),
        # so disambiguate by date: prefer the song whose body or frontmatter date matches
        # what the index claims.
        candidates = [
            s for s in songs if s.title == title or title.startswith(s.title)
        ]
        matched = None
        for c in candidates:
            if c.body_date == claimed_date or c.frontmatter_date == claimed_date:
                matched = c
                break
        if matched is None and candidates:
            matched = candidates[0]
        if matched is None:
            findings.append(
                Finding(
                    category="index_drift",
                    severity="error",
                    path=index_path,
                    message=(
                        f"Recently Published lists {title!r} but no songbook entry "
                        f"has that title"
                    ),
                )
            )
            continue

        # Status must agree — index claims vs. songbook ground truth
        song_published = matched.is_published
        index_claims_published = claimed_status in ("PUBLISHED", "LOCKED")
        if song_published != index_claims_published:
            findings.append(
                Finding(
                    category="index_drift",
                    severity="error",
                    path=index_path,
                    message=(
                        f"{title!r} listed as {claimed_status} but songbook shows "
                        f"frontmatter={matched.frontmatter_status!r} "
                        f"body_marker={matched.body_status!r}"
                    ),
                )
            )

        # Date must agree with body_date (authoritative) if published
        if song_published and matched.body_date and claimed_date != matched.body_date:
            findings.append(
                Finding(
                    category="index_drift",
                    severity="error",
                    path=index_path,
                    message=(
                        f"{title!r} listed with date {claimed_date} but "
                        f"songbook Status marker says Published {matched.body_date}"
                    ),
                )
            )

    return findings


def check_index_catalog_counts(
    index_text: str, songs: list[Song], project_root: Path
) -> list[Finding]:
    """Catalog Status counts must match actual songbook + playlist ground truth."""
    findings: list[Finding] = []
    index_path = "_bmad/_memory/band-manager-sidecar/index.md"

    # Extract the Catalog Status block
    catalog_match = re.search(
        r"^##\s+Catalog Status\s*\n(.*?)(?=\n##\s)",
        index_text,
        re.MULTILINE | re.DOTALL,
    )
    if not catalog_match:
        return findings

    block = catalog_match.group(1)

    # Check claims of the form: "**Band Name:** **N published tracks**" or "**Band:** N-track playlist"
    per_band_claims = re.finditer(
        r"\*\*(?P<band>[^:*]+):\*\*\s*"
        r"(?:\*\*)?(?P<count>\d+)[-\s](?:published\s+tracks|track\s+playlist)",
        block,
        re.IGNORECASE,
    )

    # Build ground-truth counts per band (from songbook status + playlist files)
    published_per_band: dict[str, int] = {}
    all_per_band: dict[str, int] = {}
    for song in songs:
        all_per_band[song.band] = all_per_band.get(song.band, 0) + 1
        if song.is_published:
            published_per_band[song.band] = published_per_band.get(song.band, 0) + 1

    # Band name in index → band slug mapping
    band_slugs = {
        "Solitary Fire": "solitary-fire",
        "Lenny's Voice": "lennys-voice",
    }

    for match in per_band_claims:
        band_display = match.group("band").strip()
        claimed = int(match.group("count"))
        slug = band_slugs.get(band_display)
        if slug is None:
            continue

        # Figure out whether this is a "published tracks" claim or "playlist" claim
        is_playlist_claim = "playlist" in match.group(0).lower()

        if is_playlist_claim:
            # Cross-check against the playlist YAML if it exists
            playlist_path = project_root / "docs" / f"{slug}-playlist.yaml"
            if playlist_path.exists():
                try:
                    playlist = yaml.safe_load(playlist_path.read_text(encoding="utf-8"))
                    actual_tracks = len(playlist.get("tracks", []) or [])
                    if actual_tracks != claimed:
                        findings.append(
                            Finding(
                                category="index_drift",
                                severity="warning",
                                path=index_path,
                                message=(
                                    f"{band_display!r} claimed {claimed}-track playlist "
                                    f"but {playlist_path.name} has {actual_tracks} tracks"
                                ),
                            )
                        )
                except yaml.YAMLError:
                    pass
        else:
            actual_published = published_per_band.get(slug, 0)
            if actual_published != claimed:
                findings.append(
                    Finding(
                        category="index_drift",
                        severity="error",
                        path=index_path,
                        message=(
                            f"{band_display!r} claimed {claimed} published tracks "
                            f"but songbook has {actual_published} with status=published + body marker"
                        ),
                    )
                )

    return findings


def check_playlist_songbook_parity(
    songs: list[Song], project_root: Path
) -> list[Finding]:
    """Playlist YAMLs should reference songs that exist in the songbook."""
    findings: list[Finding] = []
    playlist_dir = project_root / "docs"
    if not playlist_dir.is_dir():
        return findings

    for playlist_path in sorted(playlist_dir.glob("*-playlist.yaml")):
        slug = playlist_path.name.replace("-playlist.yaml", "")
        try:
            playlist = yaml.safe_load(playlist_path.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            continue
        if not isinstance(playlist, dict):
            continue
        track_count = len(playlist.get("tracks", []) or [])
        songbook_count = sum(1 for s in songs if s.band == slug)
        if track_count != songbook_count:
            findings.append(
                Finding(
                    category="playlist_drift",
                    severity="warning",
                    path=str(playlist_path.relative_to(project_root)),
                    message=(
                        f"{track_count} tracks in playlist YAML but "
                        f"{songbook_count} songbook entries for band {slug!r}"
                    ),
                )
            )

    return findings


# ---------------------------------------------------------------------------
# Cross-reference check
# ---------------------------------------------------------------------------


# Inline-code reference: `path/to/file.md` or `path/to/file.md#anchor`
# We require at least one slash or dot-segment so bare `README.md` in running
# prose still matches but single-word code spans like `status` don't.
INLINE_CODE_REF_RE = re.compile(r"`([^`\s]+\.md(?:#[^`]*)?)`")

# Markdown link reference: [text](path.md) or [text](path.md#anchor)
# Negative lookbehind on ! avoids matching image syntax ![alt](...).
MARKDOWN_LINK_REF_RE = re.compile(
    r"(?<!!)\[[^\]]*\]\(([^)\s]+?\.md(?:#[^)\s]*)?)\)"
)


def _is_external_or_anchor(ref: str) -> bool:
    """Skip external URLs, mail links, and bare anchor references."""
    lowered = ref.strip().lower()
    if lowered.startswith(("http://", "https://", "mailto:", "ftp://", "//")):
        return True
    if lowered.startswith("#"):
        return True
    return False


def _strip_code_fences(text: str) -> str:
    """Remove fenced code blocks so references inside them are not checked.

    References inside inline backticks (single backtick spans) are still checked,
    since those are the canonical form for pointing at a file in prose. But
    multi-line ``` fences often contain examples, templates, or diffs that
    shouldn't be validated against the real filesystem.
    """
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def check_markdown_cross_references(project_root: Path) -> list[Finding]:
    """Scan every markdown file under docs/ for broken cross-references.

    Catches forward-intent references (`docs/X.md` mentioned declaratively but
    never actually created) and stale references that slipped past the delete
    reconciliation protocol.

    Scope: `docs/` only — module source references (`src/skills/...`) are out
    of scope because they follow different drift semantics (tracked in git, not
    synced machine-to-machine).

    Matches:
      - Inline code: `path/to/file.md` (single backtick spans)
      - Markdown links: [text](path/to/file.md) including relative `../` paths

    Skips:
      - External URLs (http/https/mailto/ftp)
      - Anchor-only refs (#section)
      - Self-references
      - Anything inside fenced code blocks (``` ... ```)
    """
    findings: list[Finding] = []
    docs_root = project_root / "docs"
    if not docs_root.is_dir():
        return findings

    for md_path in sorted(docs_root.rglob("*.md")):
        try:
            text = md_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        scannable = _strip_code_fences(text)
        rel_referrer = str(md_path.relative_to(project_root))
        seen: set[str] = set()

        for pattern in (INLINE_CODE_REF_RE, MARKDOWN_LINK_REF_RE):
            for match in pattern.finditer(scannable):
                raw_ref = match.group(1).strip()
                if _is_external_or_anchor(raw_ref):
                    continue

                # Strip URL-style anchor suffix for file existence check
                ref_path_part = raw_ref.split("#", 1)[0]
                if not ref_path_part:
                    continue

                # Deduplicate per-file so one broken reference reported once
                if ref_path_part in seen:
                    continue
                seen.add(ref_path_part)

                # Absolute-ish refs (starting with /) are machine paths — skip.
                if ref_path_part.startswith("/"):
                    continue

                # Glob/wildcard patterns (e.g. `per-candidate/*.md`) describe
                # a directory of files, not a single target — skip them.
                if any(c in ref_path_part for c in "*?["):
                    continue

                # References can be either parent-relative (`../foo.md`) or
                # project-root-relative (`docs/foo.md` written from inside
                # `docs/` — the user convention in this codebase). Try both
                # anchors; if either target exists, the reference is valid.
                project_abs = project_root.resolve()
                parent_resolved = (md_path.parent / ref_path_part).resolve()
                root_resolved = (project_root / ref_path_part).resolve()
                referrer_abs = md_path.resolve()

                # Self-reference check against either resolution
                if parent_resolved == referrer_abs or root_resolved == referrer_abs:
                    continue

                # Does either candidate exist under the project root?
                candidates = []
                for cand in (parent_resolved, root_resolved):
                    try:
                        cand.relative_to(project_abs)
                    except ValueError:
                        continue
                    candidates.append(cand)

                if not candidates:
                    # Both candidates escape the project root — out of scope
                    continue

                if any(c.exists() for c in candidates):
                    continue

                # Neither exists — report using the more informative target
                # (prefer project-root-relative when the reference looked like
                # one, else the parent-relative form).
                display_target = candidates[-1] if len(candidates) > 1 else candidates[0]
                try:
                    target_display = str(display_target.relative_to(project_abs))
                except ValueError:
                    target_display = str(display_target)
                findings.append(
                    Finding(
                        category="cross_reference_missing",
                        severity="warning",
                        path=rel_referrer,
                        message=(
                            f"reference to {raw_ref!r} → target not found: "
                            f"{target_display}"
                        ),
                    )
                )

    return findings


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def run_checks(project_root: Path) -> tuple[list[Finding], dict[str, int]]:
    songs, parse_findings = load_all_songs(project_root)

    findings: list[Finding] = list(parse_findings)
    for song in songs:
        findings.extend(check_songbook_consistency(song))
        findings.extend(check_audio_exists(song, project_root))

    index_path = project_root / "_bmad" / "_memory" / "band-manager-sidecar" / "index.md"
    if index_path.exists():
        index_text = index_path.read_text(encoding="utf-8")
        findings.extend(check_index_recently_published(index_text, songs))
        findings.extend(check_index_catalog_counts(index_text, songs, project_root))

    findings.extend(check_playlist_songbook_parity(songs, project_root))
    findings.extend(check_markdown_cross_references(project_root))

    stats = {
        "songs_scanned": len(songs),
        "songs_published": sum(1 for s in songs if s.is_published),
        "findings_total": len(findings),
        "findings_error": sum(1 for f in findings if f.severity == "error"),
        "findings_warning": sum(1 for f in findings if f.severity == "warning"),
    }
    return findings, stats


def format_text(findings: list[Finding], stats: dict[str, int]) -> str:
    lines = [
        "Sidecar Validation Report",
        "=" * 25,
        f"Songs scanned: {stats['songs_scanned']} "
        f"({stats['songs_published']} published)",
        f"Findings: {stats['findings_total']} "
        f"({stats['findings_error']} errors, {stats['findings_warning']} warnings)",
        "",
    ]
    if not findings:
        lines.append("PASS — no drift detected.")
        return "\n".join(lines)

    # Group by category for readable output
    by_category: dict[str, list[Finding]] = {}
    for f in findings:
        by_category.setdefault(f.category, []).append(f)

    for category, items in sorted(by_category.items()):
        lines.append(f"[{category.upper()}]")
        for f in items:
            lines.append(f"  ({f.severity}) {f.path}")
            lines.append(f"      {f.message}")
        lines.append("")

    if stats["findings_error"] > 0:
        lines.append(
            f"FAIL — {stats['findings_error']} error(s) block sidecar sync."
        )
    else:
        lines.append(
            f"PASS (with {stats['findings_warning']} warning(s)) — no blocking errors."
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Mac sidecar index against songbook ground truth."
    )
    parser.add_argument(
        "project_root",
        nargs="?",
        default=".",
        help="Project root directory (default: current directory)",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--warn-only",
        action="store_true",
        help="Exit 0 even when errors are found (for advisory runs)",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    if not project_root.is_dir():
        print(f"ERROR: project root not found: {project_root}", file=sys.stderr)
        return 2

    findings, stats = run_checks(project_root)

    if args.format == "json":
        payload: dict[str, Any] = {
            "status": "pass" if stats["findings_error"] == 0 else "fail",
            "stats": stats,
            "findings": [f.to_dict() for f in findings],
        }
        print(json.dumps(payload, indent=2))
    else:
        print(format_text(findings, stats))

    if args.warn_only:
        return 0
    return 0 if stats["findings_error"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
