#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6.0"]
# ///
"""
Audio Files Manifest — generate a checksum-free file-size manifest for
audio files in a project's docs/audio/ directory.

Audio files are too large to travel in the portable sync archive, so they
stay machine-local. This means two machines can have DIFFERENT audio for the
same canonical filename (e.g. v1 on machine A, v2 on machine B). Audio
analysis output for the same filename will then disagree across machines —
exactly the drift class we observed with SF Distant Mourning's local file
showing 4:34 / C minor / 143.55 BPM while Desktop's published v2 was
3:49 / D# minor / 95.7 BPM.

This manifest captures size_bytes (and mtime as informational metadata) for
every audio file present on the machine that runs this script. It travels
in the portable sync archive (small, machine-readable). The companion script
verify-audio-files.py compares local files against the manifest and reports
which files are missing, size-mismatched, or extra — so Mac can tell the
user exactly which audio files need to be re-downloaded from Suno to bring
the local audio dir in line with the canonical version.

WHY size, not hash:
- File size is fast to compute (single os.stat call, no read)
- Different MP3 encodes from Suno are byte-for-byte non-deterministic, so
  re-encodings of the same source produce different sizes — size is a
  reliable mismatch detector for our use case
- We don't need cryptographic certainty here; we need to detect "different
  gen of the same song" with high confidence and zero false-positive risk
  on the legitimate "same exact file" case

Workflow:
- Run on the canonical machine (whichever has the latest published audio)
  after any publish/regen that changes audio files
- Manifest writes to docs/audio-files-manifest.yaml
- Travels in sync archive per portable-manifest.yaml
- Other machines run verify-audio-files.py after unpack to detect mismatches

Usage:
  # Generate manifest using default audio dir (docs/audio/)
  audio-files-manifest.py PROJECT_ROOT

  # Specify a different audio dir
  audio-files-manifest.py PROJECT_ROOT --audio-dir docs/audio

  # Write manifest to a custom path
  audio-files-manifest.py PROJECT_ROOT --output docs/custom-manifest.yaml

  # Print to stdout instead of writing to disk
  audio-files-manifest.py PROJECT_ROOT --stdout

Exit codes:
  0 = manifest written successfully
  1 = invalid arguments or audio dir not found
  2 = missing dependencies (pyyaml)
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_NAME = "audio-files-manifest"
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


def collect_audio_files(audio_dir: Path) -> list[dict]:
    """Walk audio_dir and return entries sorted by filename."""
    entries = []
    for path in sorted(audio_dir.iterdir()):
        if not path.is_file():
            continue
        if path.suffix.lower() not in AUDIO_EXTENSIONS:
            continue
        # Skip Windows Zone.Identifier files
        if ":" in path.name:
            continue
        st = path.stat()
        entries.append({
            "name": path.name,
            "size_bytes": st.st_size,
            "mtime_iso": datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).isoformat(),
        })
    return entries


def main():
    parser = argparse.ArgumentParser(description="Generate audio files manifest")
    parser.add_argument("project_root", help="Project root directory")
    parser.add_argument(
        "--audio-dir",
        default=DEFAULT_AUDIO_DIR,
        help=f"Audio directory relative to project root (default: {DEFAULT_AUDIO_DIR})",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_MANIFEST_PATH,
        help=f"Output manifest path relative to project root (default: {DEFAULT_MANIFEST_PATH})",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print YAML to stdout instead of writing to disk",
    )
    parser.add_argument(
        "--format",
        choices=["yaml", "json"],
        default="yaml",
        help="Output format (default: yaml)",
    )
    args = parser.parse_args()

    yaml = require_yaml()

    project_root = Path(args.project_root).resolve()
    audio_dir = project_root / args.audio_dir
    if not audio_dir.is_dir():
        print(
            json.dumps({
                "script": SCRIPT_NAME,
                "version": SCRIPT_VERSION,
                "status": "error",
                "error": "audio-dir-not-found",
                "audio_dir": str(audio_dir),
            }),
            file=sys.stdout,
        )
        sys.exit(1)

    entries = collect_audio_files(audio_dir)

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": SCRIPT_NAME,
        "version": SCRIPT_VERSION,
        "audio_dir": args.audio_dir,
        "file_count": len(entries),
        "files": entries,
    }

    if args.format == "json":
        text = json.dumps(manifest, indent=2)
    else:
        text = yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True)

    if args.stdout:
        print(text)
    else:
        out_path = project_root / args.output
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
        print(
            json.dumps({
                "script": SCRIPT_NAME,
                "version": SCRIPT_VERSION,
                "status": "ok",
                "manifest_path": str(out_path.relative_to(project_root)),
                "file_count": len(entries),
            })
        )


if __name__ == "__main__":
    main()
