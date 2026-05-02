#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6.0"]
# ///
"""
Verify Audio Files — compare local audio files against the canonical
audio-files-manifest.yaml and report mismatches.

Companion to audio-files-manifest.py. The manifest is generated on the
canonical machine (whichever has the latest published audio) and travels
in the portable sync archive. This script runs on a non-canonical machine
after unpack to detect which audio files need to be re-downloaded from Suno.

Three failure modes are detected:
- MISSING: no local file matches the manifest entry, even under fuzzy
  filename normalization (no audio for this song at all)
- SIZE_MISMATCH: a local file matches by song identity but bytes differ
  beyond the size tolerance (likely a different gen — re-download from
  Suno if the gen matters)
- EXTRA: local file with no manifest entry under any normalization
  (orphan / abandoned gen)

Filename matching is normalization-aware (since v1.1.0): variations like
`Foo.mp3` vs `Foo-Redux.mp3` vs `Foo (NSFW).mp3`, em-dash vs ascii hyphen,
equals-sign-as-separator, repeated underscore-hyphen runs are all treated
as the same song. Band suffixes like `-Lenny` are NOT normalized away
because they distinguish different bands' gens of the same poem. When a
fuzzy match is used, the entry includes `filename_variant: true` and a
`local_filename` field showing the actual on-disk name.

Size matching is tolerance-aware (since v1.2.0). Suno's MP3 downloads
carry per-download ID3 metadata variance (timestamps, cover art presence,
encoded-by strings) that produces small byte differences across machines
and download events even for the SAME audio gen. Default tolerance of
1024 bytes absorbs this metadata noise so the script doesn't false-
positive identical audio as "different gen." Real gen differences are
typically tens of KB or larger. Override with `--tolerance-bytes`.

Output is JSON, structured so Mac can present a download list to the user
or auto-fix orphans on confirmation.

Optional --playlist-context flag enriches mismatch entries with playlist
position info so the report can be presented in playlist order rather
than alphabetical filename order.

Usage:
  # Default: read docs/audio-files-manifest.yaml, scan docs/audio/
  verify-audio-files.py PROJECT_ROOT

  # Use a custom manifest path
  verify-audio-files.py PROJECT_ROOT --manifest docs/custom-manifest.yaml

  # Use a custom audio dir
  verify-audio-files.py PROJECT_ROOT --audio-dir docs/audio

  # Enrich with playlist position from per-band playlist YAMLs
  verify-audio-files.py PROJECT_ROOT --playlist-context

Exit codes:
  0 = no mismatches detected (all files match manifest)
  1 = mismatches detected (see JSON output for details)
  2 = invalid arguments, manifest not found, or missing dependencies
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

SCRIPT_NAME = "verify-audio-files"
SCRIPT_VERSION = "1.2.0"

DEFAULT_AUDIO_DIR = "docs/audio"
DEFAULT_MANIFEST_PATH = "docs/audio-files-manifest.yaml"
DEFAULT_SIZE_TOLERANCE_BYTES = 1024  # absorbs ID3 metadata variance from Suno re-downloads

AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".m4a", ".ogg", ".opus"}


def normalize_for_match(name: str) -> str:
    """Normalize a filename for fuzzy song-identity matching.

    Strips/normalizes filename variations that don't change song identity:
    - File extension (.mp3, .wav, etc.)
    - Version qualifiers (-Redux, -v2, -alt — common Suno post-publish naming)
    - Parenthetical annotations ((NSFW), (clean), (explicit), etc.)
    - Em-dash (—) / en-dash (–) collapsed to ascii hyphen
    - Equals sign (=, occasionally used as separator in mangled Suno-default names) → hyphen
    - Repeated separator runs (-_, _-, --, __) collapsed to single hyphen
    - Whitespace + leading/trailing hyphens trimmed, lowercase

    NOT stripped (preserved as meaningful):
    - `-Lenny` and other band-suffix patterns. The band suffix distinguishes
      different bands' gens of the same poem (e.g., `Distant Mourning.mp3` is
      Solitary Fire, `Distant Mourning-Lenny.mp3` is Lenny's Voice — these are
      different audio files of the same lyrics).

    The goal: recognize that filenames like `Foo.mp3`, `Foo-Redux.mp3`,
    `Foo (NSFW).mp3` all refer to the same song; while `Foo.mp3` (SF) and
    `Foo-Lenny.mp3` (LV) are different songs by band-suffix convention.
    """
    s = name.lower()
    # Strip audio extension
    s = re.sub(r"\.(mp3|wav|flac|m4a|ogg|opus)$", "", s)
    # Strip version qualifiers (must come before separator collapse)
    s = re.sub(r"-(redux|v\d+|alt|alternate)\b", "", s)
    # Strip parentheticals (e.g., "(NSFW)", "(clean)", "(explicit)")
    s = re.sub(r"\s*\([^)]*\)\s*", " ", s)
    # Normalize unicode dashes
    s = s.replace("—", "-").replace("–", "-")
    # Equals sign as separator → hyphen
    s = s.replace("=", "-")
    # Collapse repeated separators (-_, _-, --, __) to single hyphen
    s = re.sub(r"[-_]+", "-", s)
    # Collapse whitespace
    s = re.sub(r"\s+", " ", s).strip()
    # Strip leading/trailing hyphens
    s = s.strip("-")
    return s


def require_yaml():
    try:
        import yaml  # noqa: F401
        return yaml
    except ImportError:
        print(
            json.dumps({
                "script": SCRIPT_NAME,
                "version": SCRIPT_VERSION,
                "status": "error",
                "error": "missing-dependency",
                "message": "pyyaml is required. Install with: pip install pyyaml",
            }),
            file=sys.stdout,
        )
        sys.exit(2)


def load_playlist_context(project_root: Path, yaml_module) -> dict[str, dict]:
    """Map filename -> {band, position, track_name} from per-band playlist YAMLs."""
    context = {}
    docs = project_root / "docs"
    if not docs.is_dir():
        return context
    for yaml_path in sorted(docs.glob("*-playlist.yaml")):
        try:
            data = yaml_module.safe_load(yaml_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        album = data.get("album", yaml_path.stem.replace("-playlist", ""))
        # band slug = the filename stem minus -playlist suffix
        band_slug = yaml_path.stem
        if band_slug.endswith("-playlist"):
            band_slug = band_slug[:-len("-playlist")]
        for idx, track in enumerate(data.get("tracks") or [], start=1):
            if not isinstance(track, dict):
                continue
            file = track.get("file")
            name = track.get("name")
            if not file:
                continue
            context[file] = {
                "band": album,
                "band_slug": band_slug,
                "position": idx,
                "track_name": name,
            }
    return context


def main():
    parser = argparse.ArgumentParser(description="Verify local audio files against canonical manifest")
    parser.add_argument("project_root", help="Project root directory")
    parser.add_argument(
        "--manifest",
        default=DEFAULT_MANIFEST_PATH,
        help=f"Manifest path relative to project root (default: {DEFAULT_MANIFEST_PATH})",
    )
    parser.add_argument(
        "--audio-dir",
        default=DEFAULT_AUDIO_DIR,
        help=f"Audio directory relative to project root (default: {DEFAULT_AUDIO_DIR})",
    )
    parser.add_argument(
        "--playlist-context",
        action="store_true",
        help="Enrich mismatch entries with playlist position from per-band playlist YAMLs",
    )
    parser.add_argument(
        "--tolerance-bytes",
        type=int,
        default=DEFAULT_SIZE_TOLERANCE_BYTES,
        help=(
            f"Size-difference tolerance in bytes (default: {DEFAULT_SIZE_TOLERANCE_BYTES}). "
            f"Files differing by less than this are treated as matched. Suno's per-download "
            f"ID3 metadata variance (timestamps, cover art) produces small byte differences "
            f"even for the same audio gen; this absorbs that noise. Set to 0 for strict "
            f"byte-exact matching."
        ),
    )
    args = parser.parse_args()

    yaml = require_yaml()

    project_root = Path(args.project_root).resolve()
    manifest_path = project_root / args.manifest
    audio_dir = project_root / args.audio_dir

    if not manifest_path.is_file():
        print(
            json.dumps({
                "script": SCRIPT_NAME,
                "version": SCRIPT_VERSION,
                "status": "error",
                "error": "manifest-not-found",
                "manifest_path": str(manifest_path),
                "hint": "Generate the manifest on the canonical machine first via audio-files-manifest.py, then sync.",
            })
        )
        sys.exit(2)

    if not audio_dir.is_dir():
        print(
            json.dumps({
                "script": SCRIPT_NAME,
                "version": SCRIPT_VERSION,
                "status": "error",
                "error": "audio-dir-not-found",
                "audio_dir": str(audio_dir),
            })
        )
        sys.exit(2)

    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    expected = {entry["name"]: entry for entry in (manifest.get("files") or [])}

    # Walk local audio dir
    local = {}
    for path in sorted(audio_dir.iterdir()):
        if not path.is_file():
            continue
        if path.suffix.lower() not in AUDIO_EXTENSIONS:
            continue
        if ":" in path.name:
            continue
        local[path.name] = path.stat().st_size

    playlist_ctx = load_playlist_context(project_root, yaml) if args.playlist_context else {}

    # Augment playlist_ctx with normalized-key lookup so fuzzy-matched local
    # filenames can still find their playlist context (since the playlist YAML
    # has the canonical filename and the local file may differ).
    playlist_ctx_by_norm: dict[str, dict] = {}
    for fname, ctx in playlist_ctx.items():
        playlist_ctx_by_norm[normalize_for_match(fname)] = ctx

    # Build normalized → list of (name, size) maps for both sides. Multiple
    # entries can collide on a single normalized key when a manifest carries
    # both `Foo.mp3` and `Foo-Redux.mp3` — both legitimate gens, distinguished
    # by size.
    local_by_norm: dict[str, list[tuple[str, int]]] = {}
    for name, size in local.items():
        local_by_norm.setdefault(normalize_for_match(name), []).append((name, size))

    missing = []
    size_mismatch = []
    extra = []
    matched = []

    # Track which (norm_key, local_name) pairs have been claimed by a manifest
    # entry so we don't double-match and can detect orphans afterward.
    claimed_local: set[tuple[str, str]] = set()

    def lookup_playlist_ctx(canonical_name: str, local_name: str | None) -> dict | None:
        """Find playlist context for an entry by exact name first, then normalized."""
        if canonical_name in playlist_ctx:
            return playlist_ctx[canonical_name]
        if local_name and local_name in playlist_ctx:
            return playlist_ctx[local_name]
        norm = normalize_for_match(canonical_name)
        return playlist_ctx_by_norm.get(norm)

    for name, entry in expected.items():
        expected_size = entry.get("size_bytes")
        norm = normalize_for_match(name)

        # Find a local match. Prefer exact filename match, then best size match
        # among normalized-key candidates that haven't already been claimed.
        candidates = local_by_norm.get(norm, [])
        best: tuple[str, int] | None = None
        best_score: float = float("inf")
        for local_name, local_size in candidates:
            if (norm, local_name) in claimed_local:
                continue
            if local_name == name:
                # Exact name match always wins
                best = (local_name, local_size)
                best_score = -1
                break
            # Otherwise pick the closest size match
            score = abs(local_size - (expected_size or 0))
            if score < best_score:
                best = (local_name, local_size)
                best_score = score

        if best is None:
            # No local file under the canonical name OR any fuzzy variant
            item = {"name": name, "expected_size_bytes": expected_size}
            ctx = lookup_playlist_ctx(name, None)
            if ctx:
                item["playlist_context"] = ctx
            missing.append(item)
            continue

        local_name, local_size = best
        claimed_local.add((norm, local_name))
        is_variant = local_name != name

        delta = local_size - (expected_size or 0)
        within_tolerance = abs(delta) <= args.tolerance_bytes

        if local_size == expected_size or within_tolerance:
            entry_out: dict = {"name": name}
            if is_variant:
                entry_out["filename_variant"] = True
                entry_out["local_filename"] = local_name
            if delta != 0 and within_tolerance:
                entry_out["delta_bytes"] = delta
                entry_out["within_tolerance"] = True
                entry_out["note"] = (
                    f"Local size differs by {delta:+d} bytes (within {args.tolerance_bytes}-byte "
                    f"tolerance — likely ID3 metadata variance, not a different audio gen)"
                )
            matched.append(entry_out)
        else:
            item = {
                "name": name,
                "expected_size_bytes": expected_size,
                "local_size_bytes": local_size,
                "delta_bytes": delta,
            }
            if is_variant:
                item["filename_variant"] = True
                item["local_filename"] = local_name
            ctx = lookup_playlist_ctx(name, local_name)
            if ctx:
                item["playlist_context"] = ctx
            size_mismatch.append(item)

    # Anything not claimed is an orphan
    for name, size in local.items():
        norm = normalize_for_match(name)
        if (norm, name) not in claimed_local:
            item = {"name": name, "local_size_bytes": size}
            ctx = lookup_playlist_ctx(name, name)
            if ctx:
                item["playlist_context"] = ctx
            extra.append(item)

    has_mismatches = bool(missing or size_mismatch or extra)

    result = {
        "script": SCRIPT_NAME,
        "version": SCRIPT_VERSION,
        "status": "mismatch" if has_mismatches else "ok",
        "manifest_path": str(manifest_path.relative_to(project_root)),
        "audio_dir": args.audio_dir,
        "manifest_generated_at": manifest.get("generated_at"),
        "summary": {
            "expected": len(expected),
            "local": len(local),
            "matched": len(matched),
            "matched_byte_exact": sum(1 for m in matched if isinstance(m, dict) and not m.get("within_tolerance")),
            "matched_within_tolerance": sum(1 for m in matched if isinstance(m, dict) and m.get("within_tolerance")),
            "matched_filename_variants": sum(1 for m in matched if isinstance(m, dict) and m.get("filename_variant")),
            "missing": len(missing),
            "size_mismatch": len(size_mismatch),
            "size_mismatch_filename_variants": sum(1 for m in size_mismatch if m.get("filename_variant")),
            "extra": len(extra),
            "tolerance_bytes": args.tolerance_bytes,
        },
        "missing": missing,
        "size_mismatch": size_mismatch,
        "extra": extra,
    }

    print(json.dumps(result, indent=2))
    sys.exit(1 if has_mismatches else 0)


if __name__ == "__main__":
    main()
