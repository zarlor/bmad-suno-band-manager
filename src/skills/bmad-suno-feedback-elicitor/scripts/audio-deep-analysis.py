#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["librosa", "numpy"]
# ///
"""Deep audio analysis -- chord progression, energy over time, spectral features,
section boundaries, and harmonic/percussive separation analysis.

Usage:
    python audio-deep-analysis.py <audio-file> [options]

    # Analyze a single track
    python audio-deep-analysis.py track.mp3

    # JSON output to file
    python audio-deep-analysis.py track.mp3 --format json -o results.json

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

SCRIPT_NAME = "audio-deep-analysis"
VERSION = "1.0.0"


def format_time(seconds):
    m = int(seconds // 60)
    s = int(seconds % 60)
    frac = int((seconds % 1) * 10)
    return f"{m}:{s:02d}.{frac}"


def analyze_chords(y, sr, *, collect=False):
    """Estimate chord/key progression over time using chroma features.

    When collect=True, returns data instead of printing.
    """
    import numpy as np

    pitch_classes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    major_profile = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
    minor_profile = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    hop_length = 512
    window_seconds = 10

    frames_per_window = int(window_seconds * sr / hop_length)
    num_windows = chroma.shape[1] // frames_per_window

    results = []

    if not collect:
        print("\n=== KEY/CHORD PROGRESSION ===")
        print(f"{'Time':<15} {'Estimated Key':<15} {'Confidence':>10} {'Dominant Notes'}")
        print("-" * 65)

    for i in range(num_windows):
        start_frame = i * frames_per_window
        end_frame = (i + 1) * frames_per_window
        chunk = chroma[:, start_frame:end_frame]
        avg = np.mean(chunk, axis=1)

        best_corr = -1
        best_key = "Unknown"
        for j in range(12):
            rolled = np.roll(avg, -j)
            maj_corr = np.corrcoef(rolled, major_profile)[0, 1]
            min_corr = np.corrcoef(rolled, minor_profile)[0, 1]
            if maj_corr > best_corr:
                best_corr = maj_corr
                best_key = f"{pitch_classes[j]} major"
            if min_corr > best_corr:
                best_corr = min_corr
                best_key = f"{pitch_classes[j]} minor"

        top_3 = np.argsort(avg)[-3:][::-1]
        dominant = ", ".join([pitch_classes[p] for p in top_3])

        start_time = i * window_seconds
        end_time = (i + 1) * window_seconds

        if collect:
            results.append({
                "time_start": start_time,
                "time_end": end_time,
                "key": best_key,
                "confidence": round(best_corr, 3),
                "dominant_notes": [pitch_classes[p] for p in top_3],
            })
        else:
            print(f"{format_time(start_time)}-{format_time(end_time):<8} {best_key:<15} {best_corr:>10.3f} {dominant}")

    return results


def analyze_energy(y, sr, *, collect=False):
    """Show energy/loudness over time.

    When collect=True, returns data instead of printing.
    """
    import numpy as np

    rms = librosa.feature.rms(y=y)[0]
    hop_length = 512
    window_seconds = 5
    frames_per_window = int(window_seconds * sr / hop_length)

    max_rms = np.max(rms)
    if max_rms == 0:
        max_rms = 1

    num_windows = len(rms) // frames_per_window

    if not collect:
        print("\n=== ENERGY / LOUDNESS ARC ===")
        print(f"{'Time':<15} {'Energy':>7} {'Bar (visual)'}")
        print("-" * 60)

    energies = []
    windows = []
    for i in range(num_windows):
        start = i * frames_per_window
        end = (i + 1) * frames_per_window
        avg = np.mean(rms[start:end])
        pct = int((avg / max_rms) * 100)
        energies.append(pct)

        start_time = i * window_seconds
        if collect:
            windows.append({
                "time": start_time,
                "energy_pct": pct,
            })
        else:
            bar = "\u2588" * (pct // 2)
            print(f"{format_time(start_time):<15} {pct:>5}%  {bar}")

    # Detect significant energy shifts
    shifts = []
    if not collect:
        print("\n--- Energy Shifts (>20% change) ---")

    found = False
    for i in range(1, len(energies)):
        diff = energies[i] - energies[i-1]
        if abs(diff) > 20:
            t = i * window_seconds
            direction = "UP" if diff > 0 else "DOWN"
            if collect:
                shifts.append({
                    "time": t,
                    "direction": direction,
                    "change_pct": abs(diff),
                    "from_pct": energies[i-1],
                    "to_pct": energies[i],
                })
            else:
                print(f"  {format_time(t)} \u2014 energy {direction} {abs(diff)}% ({energies[i-1]}% \u2192 {energies[i]}%)")
            found = True

    if not collect and not found:
        print("  No dramatic energy shifts detected (all changes < 20%)")

    return {"windows": windows, "shifts": shifts}


def analyze_sections(y, sr, *, collect=False):
    """Detect section boundaries using spectral novelty.

    When collect=True, returns data instead of printing.
    """
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    bounds = librosa.segment.agglomerative(mfcc, k=8)
    bound_times = librosa.frames_to_time(bounds, sr=sr)

    results = []

    if not collect:
        print("\n=== SECTION BOUNDARIES (spectral novelty) ===")
        print("Detected section changes at:")

    for i, t in enumerate(bound_times):
        if t > 0.5:  # Skip very start
            if collect:
                results.append({
                    "section": i + 1,
                    "time": round(float(t), 2),
                })
            else:
                print(f"  Section {i+1}: {format_time(t)}")

    return results


def analyze_spectral_balance(y, sr, *, collect=False):
    """Show low vs mid vs high frequency balance over time."""
    import numpy as np

    S = np.abs(librosa.stft(y))
    freqs = librosa.fft_frequencies(sr=sr)

    low_mask = freqs < 250
    mid_mask = (freqs >= 250) & (freqs < 2000)
    high_mask = freqs >= 2000

    window_seconds = 10
    hop_length = 512
    frames_per_window = int(window_seconds * sr / hop_length)
    num_windows = S.shape[1] // frames_per_window

    if not collect:
        print("\n=== SPECTRAL BALANCE (low/mid/high) ===")
        print(f"{'Time':<15} {'Low(<250Hz)':>12} {'Mid(250-2k)':>12} {'High(>2kHz)':>12} {'Balance'}")
        print("-" * 70)

    results = []
    for i in range(num_windows):
        start = i * frames_per_window
        end = (i + 1) * frames_per_window

        chunk = S[:, start:end]
        low = np.mean(chunk[low_mask, :])
        mid = np.mean(chunk[mid_mask, :])
        high = np.mean(chunk[high_mask, :])

        total = low + mid + high
        if total == 0:
            total = 1
        l_pct = int(low / total * 100)
        m_pct = int(mid / total * 100)
        h_pct = int(high / total * 100)

        dominant = "BASS-heavy" if l_pct > 45 else "MID-heavy" if m_pct > 50 else "balanced"

        start_time = i * window_seconds
        if collect:
            results.append({
                "time": start_time,
                "low_pct": l_pct,
                "mid_pct": m_pct,
                "high_pct": h_pct,
                "balance": dominant,
            })
        else:
            print(f"{format_time(start_time):<15} {l_pct:>10}% {m_pct:>10}% {h_pct:>10}%  {dominant}")

    return results


def format_json_output(filepath, duration, energy_data, chord_data, section_data, spectral_data):
    """Build structured JSON output."""
    return {
        "script": SCRIPT_NAME,
        "version": VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "pass",
        "metrics": {
            "file": os.path.basename(filepath),
            "duration_seconds": round(duration, 2),
            "energy_arc": energy_data,
            "chord_progression": chord_data,
            "section_boundaries": section_data,
            "spectral_balance": spectral_data,
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
        description="Deep single-track audio analysis — energy, chords, sections, spectral balance.",
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

    filepath = args.audio_file
    y, sr = _librosa.load(filepath, sr=22050)
    duration = _librosa.get_duration(y=y, sr=sr)

    if args.output_format == "text":
        print(f"Loading: {os.path.basename(filepath)}")
        print(f"Duration: {int(duration//60)}:{int(duration%60):02d}\n")
        analyze_energy(y, sr)
        analyze_chords(y, sr)
        analyze_sections(y, sr)
        analyze_spectral_balance(y, sr)
    else:
        energy_data = analyze_energy(y, sr, collect=True)
        chord_data = analyze_chords(y, sr, collect=True)
        section_data = analyze_sections(y, sr, collect=True)
        spectral_data = analyze_spectral_balance(y, sr, collect=True)

        result = format_json_output(filepath, duration, energy_data, chord_data, section_data, spectral_data)
        output = json.dumps(result, indent=2)

        if args.output:
            Path(args.output).write_text(output + "\n")
        else:
            print(output)


if __name__ == "__main__":
    main()
