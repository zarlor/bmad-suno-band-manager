#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["librosa", "numpy"]
# ///
"""Detailed tempo analysis -- shows BPM over time to detect tempo changes
and off-beats.

Usage:
    python tempo-detail.py <audio-file> [options]

    # Analyze a single track
    python tempo-detail.py track.mp3

    # JSON output to file
    python tempo-detail.py track.mp3 --format json -o results.json

Exit codes:
  0 = success
  1 = invalid arguments or runtime error
  2 = missing dependencies
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "_shared"))
from audio_deps import require_audio_deps

SCRIPT_NAME = "tempo-detail"
VERSION = "1.0.0"


def analyze_tempo_text(filepath):
    """Run tempo analysis with text output (original format)."""
    import numpy as np

    print(f"Loading: {filepath}")
    y, sr = librosa.load(filepath, sr=22050)
    duration = librosa.get_duration(y=y, sr=sr)
    print(f"Duration: {int(duration//60)}:{int(duration%60):02d}")

    # Overall tempo
    tempo_overall, beats = librosa.beat.beat_track(y=y, sr=sr)
    tempo_val = float(tempo_overall[0]) if hasattr(tempo_overall, '__len__') else float(tempo_overall)
    print(f"\nOverall BPM: {tempo_val:.1f}")

    # Beat times
    beat_times = librosa.frames_to_time(beats, sr=sr)

    if len(beat_times) < 4:
        print("Too few beats detected for detailed analysis.")
        return

    # Inter-beat intervals
    ibis = np.diff(beat_times)
    local_bpms = 60.0 / ibis

    # Show tempo in ~15-second windows
    print(f"\n{'Time Window':<20} {'Avg BPM':>8} {'Min BPM':>8} {'Max BPM':>8} {'Stability':>10}")
    print("-" * 60)

    window_size = 15  # seconds
    num_windows = int(np.ceil(duration / window_size))

    for i in range(num_windows):
        start = i * window_size
        end = min((i + 1) * window_size, duration)

        mask = (beat_times[:-1] >= start) & (beat_times[:-1] < end)
        window_bpms = local_bpms[mask]

        if len(window_bpms) > 0:
            avg = np.mean(window_bpms)
            mn = np.min(window_bpms)
            mx = np.max(window_bpms)
            std = np.std(window_bpms)
            stability = "steady" if std < 5 else "slight variation" if std < 15 else "TEMPO CHANGE"

            time_label = f"{int(start//60)}:{int(start%60):02d}-{int(end//60)}:{int(end%60):02d}"
            print(f"{time_label:<20} {avg:>8.1f} {mn:>8.1f} {mx:>8.1f} {stability:>10}")

    # Detect significant tempo shifts between consecutive beats
    print("\n--- Potential Tempo Events ---")
    found = False
    for i in range(len(local_bpms) - 1):
        diff = abs(local_bpms[i+1] - local_bpms[i])
        if diff > 20:
            t = beat_times[i+1]
            print(f"  {int(t//60)}:{int(t%60):02d}.{int((t%1)*10)} \u2014 BPM jumps from {local_bpms[i]:.0f} to {local_bpms[i+1]:.0f} (\u0394{diff:.0f})")
            found = True

    if not found:
        print("  No significant tempo shifts detected (all beat-to-beat changes < 20 BPM)")

    # Odd time / irregular beat detection
    print("\n--- Beat Regularity ---")
    median_ibi = np.median(ibis)
    irregular = []
    for i, ibi in enumerate(ibis):
        ratio = ibi / median_ibi
        if ratio < 0.75 or ratio > 1.33:
            t = beat_times[i]
            pct = (ratio - 1) * 100
            irregular.append((t, ratio, pct))

    if irregular:
        print(f"  {len(irregular)} irregular beats detected (>33% deviation from median):")
        for t, ratio, pct in irregular[:15]:
            label = "shorter" if ratio < 1 else "longer"
            print(f"    {int(t//60)}:{int(t%60):02d}.{int((t%1)*10)} \u2014 beat is {abs(pct):.0f}% {label} than expected")
    else:
        print("  All beats within normal variance \u2014 consistent 4/4 feel")


def analyze_tempo_json(filepath):
    """Run tempo analysis and return structured data for JSON output."""
    import numpy as np

    y, sr = librosa.load(filepath, sr=22050)
    duration = librosa.get_duration(y=y, sr=sr)

    tempo_overall, beats = librosa.beat.beat_track(y=y, sr=sr)
    tempo_val = float(tempo_overall[0]) if hasattr(tempo_overall, '__len__') else float(tempo_overall)

    beat_times = librosa.frames_to_time(beats, sr=sr)

    if len(beat_times) < 4:
        return {
            "script": SCRIPT_NAME,
            "version": VERSION,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "pass",
            "metrics": {
                "file": str(Path(filepath).name),
                "duration_seconds": round(duration, 2),
                "bpm_overall": round(tempo_val, 1),
                "beats_detected": len(beat_times),
                "note": "Too few beats for detailed analysis",
            },
            "findings": [],
            "summary": {"total": 0},
        }

    ibis = np.diff(beat_times)
    local_bpms = 60.0 / ibis

    # Tempo windows
    window_size = 15
    num_windows = int(np.ceil(duration / window_size))
    windows = []

    for i in range(num_windows):
        start = i * window_size
        end = min((i + 1) * window_size, duration)

        mask = (beat_times[:-1] >= start) & (beat_times[:-1] < end)
        window_bpms = local_bpms[mask]

        if len(window_bpms) > 0:
            avg = float(np.mean(window_bpms))
            mn = float(np.min(window_bpms))
            mx = float(np.max(window_bpms))
            std = float(np.std(window_bpms))
            stability = "steady" if std < 5 else "slight_variation" if std < 15 else "tempo_change"

            windows.append({
                "time_start": start,
                "time_end": round(end, 2),
                "avg_bpm": round(avg, 1),
                "min_bpm": round(mn, 1),
                "max_bpm": round(mx, 1),
                "std_bpm": round(std, 2),
                "stability": stability,
            })

    # Tempo events (>20 BPM jump)
    tempo_events = []
    for i in range(len(local_bpms) - 1):
        diff = abs(local_bpms[i+1] - local_bpms[i])
        if diff > 20:
            t = float(beat_times[i+1])
            tempo_events.append({
                "time": round(t, 2),
                "from_bpm": round(float(local_bpms[i]), 1),
                "to_bpm": round(float(local_bpms[i+1]), 1),
                "delta": round(float(diff), 1),
            })

    # Beat regularity
    median_ibi = float(np.median(ibis))
    irregular_beats = []
    for i, ibi in enumerate(ibis):
        ratio = ibi / median_ibi
        if ratio < 0.75 or ratio > 1.33:
            t = float(beat_times[i])
            pct = (ratio - 1) * 100
            irregular_beats.append({
                "time": round(t, 2),
                "ratio": round(float(ratio), 3),
                "deviation_pct": round(float(abs(pct)), 1),
                "direction": "shorter" if ratio < 1 else "longer",
            })

    return {
        "script": SCRIPT_NAME,
        "version": VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "pass",
        "metrics": {
            "file": str(Path(filepath).name),
            "duration_seconds": round(duration, 2),
            "bpm_overall": round(tempo_val, 1),
            "beats_detected": len(beat_times),
            "median_inter_beat_interval": round(median_ibi, 4),
            "tempo_windows": windows,
            "tempo_events": tempo_events,
            "irregular_beats": irregular_beats,
            "irregular_beat_count": len(irregular_beats),
        },
        "findings": [],
        "summary": {"total": 0},
    }


def main():
    require_audio_deps()

    import librosa as _librosa  # noqa: E402
    import numpy as np  # noqa: E402, F401

    # Make librosa available to module-level helper functions
    globals()["librosa"] = _librosa

    parser = argparse.ArgumentParser(
        description="Detailed tempo analysis -- BPM over time, stability, beat regularity.",
    )
    parser.add_argument(
        "audio_file",
        help="Path to the audio file to analyze",
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
    args = parser.parse_args()

    if args.output_format == "text":
        analyze_tempo_text(args.audio_file)
    else:
        result = analyze_tempo_json(args.audio_file)
        output = json.dumps(result, indent=2)

        if args.output:
            Path(args.output).write_text(output + "\n")
        else:
            print(output)


if __name__ == "__main__":
    main()
