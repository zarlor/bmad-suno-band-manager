#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["librosa>=0.10", "numpy>=1.24"]
# ///
"""Batch audio analysis for a song catalog.

Extracts BPM (librosa + aubio), estimated key, and duration for all MP3s
in a directory.

Usage:
    python analyze-audio.py [audio-directory] [options]

    # Analyze default directory
    python analyze-audio.py

    # Analyze specific directory
    python analyze-audio.py /path/to/audio

    # JSON output to file
    python analyze-audio.py /path/to/audio --format json -o results.json

Exit codes:
  0 = success
  1 = invalid arguments or runtime error
  2 = missing dependencies
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "_shared"))
from audio_deps import require_audio_deps
from companion_writer import update_companion, resolve_companion_path
from json_archiver import resolve_archive_arg, write_archive

SCRIPT_NAME = "analyze-audio"
VERSION = "1.0.0"


def get_key(y, sr):
    """Estimate musical key using chroma features."""
    import numpy as np

    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_avg = np.mean(chroma, axis=1)

    pitch_classes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    # Major and minor profiles (Krumhansl-Kessler)
    major_profile = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
    minor_profile = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

    best_corr = -1
    best_key = "Unknown"

    for i in range(12):
        rolled = np.roll(chroma_avg, -i)
        maj_corr = np.corrcoef(rolled, major_profile)[0, 1]
        min_corr = np.corrcoef(rolled, minor_profile)[0, 1]

        if maj_corr > best_corr:
            best_corr = maj_corr
            best_key = f"{pitch_classes[i]} major"
        if min_corr > best_corr:
            best_corr = min_corr
            best_key = f"{pitch_classes[i]} minor"

    return best_key, best_corr


def get_aubio_bpm(filepath):
    """Get BPM using aubio."""
    import numpy as np

    try:
        from aubio import source, tempo
        samplerate = 0
        src = source(filepath, samplerate, 512)
        samplerate = src.samplerate
        t = tempo("default", 1024, 512, samplerate)

        beats = []
        total_frames = 0
        while True:
            samples, read = src()
            is_beat = t(samples)
            if is_beat:
                beats.append(t.get_last_s())
            total_frames += read
            if read < 512:
                break

        if len(beats) > 1:
            intervals = np.diff(beats)
            avg_interval = np.median(intervals)
            bpm = 60.0 / avg_interval
            return round(bpm, 1)
        return None
    except Exception as e:
        return f"error: {e}"


def analyze_file(filepath):
    """Analyze a single audio file."""
    import numpy as np

    filename = os.path.basename(filepath)

    try:
        y, sr = librosa.load(filepath, sr=22050)
        duration = librosa.get_duration(y=y, sr=sr)

        # BPM via librosa
        tempo_librosa, _ = librosa.beat.beat_track(y=y, sr=sr)
        bpm_librosa = round(float(tempo_librosa[0]) if hasattr(tempo_librosa, '__len__') else float(tempo_librosa), 1)

        # BPM via aubio
        bpm_aubio = get_aubio_bpm(filepath)

        # Key estimation
        key, confidence = get_key(y, sr)

        mins = int(duration // 60)
        secs = int(duration % 60)

        return {
            'file': filename,
            'duration': f"{mins}:{secs:02d}",
            'bpm_librosa': bpm_librosa,
            'bpm_aubio': bpm_aubio,
            'key': key,
            'key_confidence': round(confidence, 3),
        }
    except Exception as e:
        return {
            'file': filename,
            'error': str(e)
        }


def format_text_output(results, mp3_count):
    """Format results as human-readable text (original output format)."""
    lines = []
    lines.append(f"Analyzing {mp3_count} tracks...\n")
    lines.append(f"{'Track':<50} {'Duration':>8} {'BPM(lib)':>9} {'BPM(aub)':>9} {'Key':<15} {'Conf':>5}")
    lines.append("-" * 100)

    for result in results:
        if 'error' in result:
            lines.append(f"{result['file']:<50} ERROR: {result['error']}")
        else:
            lines.append(f"{result['file']:<50} {result['duration']:>8} {result['bpm_librosa']:>9} {result['bpm_aubio']:>9} {result['key']:<15} {result['key_confidence']:>5}")

    # Summary stats
    valid = [r for r in results if 'error' not in r]
    if valid:
        bpms = [r['bpm_librosa'] for r in valid]
        lines.append(f"\n{'='*100}")
        lines.append(f"BPM range (librosa): {min(bpms):.0f} - {max(bpms):.0f}")
        lines.append(f"Tracks analyzed: {len(valid)}/{mp3_count}")

    return "\n".join(lines)


def format_json_output(results, mp3_count):
    """Format results as structured JSON."""
    valid = [r for r in results if 'error' not in r]
    errors = [r for r in results if 'error' in r]
    findings = []

    for r in results:
        if 'error' in r:
            findings.append({
                "file": r["file"],
                "level": "error",
                "message": r["error"],
            })

    bpms = [r['bpm_librosa'] for r in valid] if valid else []

    return {
        "script": SCRIPT_NAME,
        "version": VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "pass" if not errors else "partial" if valid else "fail",
        "metrics": {
            "tracks_found": mp3_count,
            "tracks_analyzed": len(valid),
            "tracks_errored": len(errors),
            "bpm_range_librosa": {
                "min": min(bpms) if bpms else None,
                "max": max(bpms) if bpms else None,
            },
            "tracks": results,
        },
        "findings": findings,
        "summary": {"total": len(findings)},
    }


def main():
    require_audio_deps()

    import librosa  # noqa: E402
    import numpy as np  # noqa: E402, F401

    # Make librosa available to module-level helper functions
    globals()["librosa"] = librosa

    parser = argparse.ArgumentParser(
        description="Batch audio analysis — BPM, key, duration for all MP3s in a directory.",
    )
    parser.add_argument(
        "audio_dir",
        nargs="?",
        default="docs/audio",
        help="Directory containing MP3 files (default: docs/audio)",
    )
    parser.add_argument(
        "--format",
        choices=["json", "text"],
        default="json",
        dest="output_format",
        help="Output format (default: json)",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--archive", nargs="?", const="", default="",
        help=(
            "Persist full JSON output to a dated catalog archive. "
            "With no path: writes to docs/audio-analysis/catalog/<YYYY-MM-DD>-summary.json. "
            "Pass an explicit path to override. Default: ON."
        ),
    )
    parser.add_argument(
        "--no-archive", dest="archive", action="store_const", const=None,
        help="Skip writing the JSON archive.",
    )
    parser.add_argument(
        "--companion", nargs="?", const="", default="",
        help=(
            "Refresh the canonical Markdown companion file. "
            "With no path: writes to docs/audio-analysis-reference.md. "
            "Pass an explicit path to override. Hand-curated sections "
            "outside the AUTOGEN markers are preserved. Default: ON."
        ),
    )
    parser.add_argument(
        "--no-companion", dest="companion", action="store_const", const=None,
        help="Skip refreshing the Markdown companion file.",
    )
    args = parser.parse_args()

    audio_dir = args.audio_dir

    mp3s = sorted([
        os.path.join(audio_dir, f)
        for f in os.listdir(audio_dir)
        if f.endswith('.mp3')
    ])

    results = []
    for filepath in mp3s:
        result = analyze_file(filepath)
        results.append(result)

    json_data = format_json_output(results, len(mp3s))

    if args.output_format == "text":
        output = format_text_output(results, len(mp3s))
    else:
        output = json.dumps(json_data, indent=2)

    if args.output:
        Path(args.output).write_text(output + "\n")
    else:
        print(output)

    # JSON archive (default ON unless --no-archive). Identifier suffix "-summary"
    # to distinguish from batch-full-analysis.py's "-deep" archive.
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d") + "-summary"
    archive_target = resolve_archive_arg("catalog", today, args.archive)
    if archive_target is not None:
        res = write_archive(archive_target, json_data)
        print(f"  ARCHIVED: {res['path']} ({res['bytes_written']} bytes)", file=sys.stderr)

    # Companion .md refresh (default ON unless --no-companion). The companion
    # docs/audio-analysis-reference.md has hand-curated sections (Felt BPM
    # Corrections, LLM BPM Comparison) preserved OUTSIDE the AUTOGEN markers.
    # Title + timestamp live inside the markers so each refresh updates them.
    companion_target = resolve_companion_path(SCRIPT_NAME, args.companion)
    if companion_target is not None:
        timestamp = datetime.now(timezone.utc).isoformat()
        title_block = (
            "# Audio Analysis Reference — Catalog Summary\n"
            f"_Generated by `{SCRIPT_NAME}` on {timestamp}_\n"
            "_BPM detection: librosa beat_track | Key detection: Krumhansl-Kessler chroma correlation_\n\n"
        )
        body_lines = format_text_output(results, len(mp3s)).split("\n")
        cut = 0
        while cut < len(body_lines):
            line = body_lines[cut]
            if line.startswith("##") or (line.strip() and not line.startswith("#")):
                break
            cut += 1
        md_body = title_block + "\n".join(body_lines[cut:])
        res = update_companion(companion_target, SCRIPT_NAME, md_body)
        print(f"  COMPANION: {res['status']} {res['path']} ({res['bytes_written']} bytes)", file=sys.stderr)


if __name__ == "__main__":
    main()
