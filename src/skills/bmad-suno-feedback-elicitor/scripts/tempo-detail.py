#!/usr/bin/env python3
"""Detailed tempo analysis — shows BPM over time to detect tempo changes and off-beats."""

import sys
import librosa
import numpy as np

def analyze_tempo_detail(filepath):
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

        # Find beats in this window
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
        if diff > 20:  # More than 20 BPM jump between consecutive beats
            t = beat_times[i+1]
            print(f"  {int(t//60)}:{int(t%60):02d}.{int((t%1)*10)} — BPM jumps from {local_bpms[i]:.0f} to {local_bpms[i+1]:.0f} (Δ{diff:.0f})")
            found = True

    if not found:
        print("  No significant tempo shifts detected (all beat-to-beat changes < 20 BPM)")

    # Odd time / irregular beat detection
    print("\n--- Beat Regularity ---")
    median_ibi = np.median(ibis)
    irregular = []
    for i, ibi in enumerate(ibis):
        ratio = ibi / median_ibi
        if ratio < 0.75 or ratio > 1.33:  # Beat is notably shorter or longer than expected
            t = beat_times[i]
            pct = (ratio - 1) * 100
            irregular.append((t, ratio, pct))

    if irregular:
        print(f"  {len(irregular)} irregular beats detected (>33% deviation from median):")
        for t, ratio, pct in irregular[:15]:  # Show first 15
            label = "shorter" if ratio < 1 else "longer"
            print(f"    {int(t//60)}:{int(t%60):02d}.{int((t%1)*10)} — beat is {abs(pct):.0f}% {label} than expected")
    else:
        print("  All beats within normal variance — consistent 4/4 feel")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 tempo-detail.py <audio-file>")
        sys.exit(1)
    analyze_tempo_detail(sys.argv[1])
