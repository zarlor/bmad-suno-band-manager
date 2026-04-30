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
- MISSING: manifest entry exists but local file does not
- SIZE_MISMATCH: local file exists but bytes differ (different gen of same song)
- EXTRA: local file exists but no manifest entry (orphan / abandoned gen)

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
import sys
from pathlib import Path

SCRIPT_NAME = "verify-audio-files"
SCRIPT_VERSION = "1.0.0"

DEFAULT_AUDIO_DIR = "docs/audio"
DEFAULT_MANIFEST_PATH = "docs/audio-files-manifest.yaml"

AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".m4a", ".ogg", ".opus"}


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

    missing = []
    size_mismatch = []
    extra = []
    matched = []

    for name, entry in expected.items():
        if name not in local:
            item = {
                "name": name,
                "expected_size_bytes": entry.get("size_bytes"),
            }
            if name in playlist_ctx:
                item["playlist_context"] = playlist_ctx[name]
            missing.append(item)
        elif local[name] != entry.get("size_bytes"):
            item = {
                "name": name,
                "expected_size_bytes": entry.get("size_bytes"),
                "local_size_bytes": local[name],
                "delta_bytes": local[name] - (entry.get("size_bytes") or 0),
            }
            if name in playlist_ctx:
                item["playlist_context"] = playlist_ctx[name]
            size_mismatch.append(item)
        else:
            matched.append(name)

    for name, size in local.items():
        if name not in expected:
            item = {"name": name, "local_size_bytes": size}
            if name in playlist_ctx:
                item["playlist_context"] = playlist_ctx[name]
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
            "missing": len(missing),
            "size_mismatch": len(size_mismatch),
            "extra": len(extra),
        },
        "missing": missing,
        "size_mismatch": size_mismatch,
        "extra": extra,
    }

    print(json.dumps(result, indent=2))
    sys.exit(1 if has_mismatches else 0)


if __name__ == "__main__":
    main()
