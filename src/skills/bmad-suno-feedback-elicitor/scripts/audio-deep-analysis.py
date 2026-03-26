#!/usr/bin/env python3
"""Deep audio analysis — chord progression, energy over time, spectral features,
section boundaries, and harmonic/percussive separation analysis."""

import sys
import os
import librosa
import numpy as np

def format_time(seconds):
    m = int(seconds // 60)
    s = int(seconds % 60)
    frac = int((seconds % 1) * 10)
    return f"{m}:{s:02d}.{frac}"

def analyze_chords(y, sr):
    """Estimate chord/key progression over time using chroma features."""
    print("\n=== KEY/CHORD PROGRESSION ===")

    pitch_classes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    major_profile = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
    minor_profile = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

    # Compute chroma in windows
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    hop_length = 512
    window_seconds = 10

    frames_per_window = int(window_seconds * sr / hop_length)
    num_windows = chroma.shape[1] // frames_per_window

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

        # Top 3 dominant pitch classes
        top_3 = np.argsort(avg)[-3:][::-1]
        dominant = ", ".join([pitch_classes[p] for p in top_3])

        start_time = i * window_seconds
        end_time = (i + 1) * window_seconds
        print(f"{format_time(start_time)}-{format_time(end_time):<8} {best_key:<15} {best_corr:>10.3f} {dominant}")


def analyze_energy(y, sr):
    """Show energy/loudness over time."""
    print("\n=== ENERGY / LOUDNESS ARC ===")

    rms = librosa.feature.rms(y=y)[0]
    hop_length = 512
    window_seconds = 5
    frames_per_window = int(window_seconds * sr / hop_length)

    # Normalize to 0-100 scale
    max_rms = np.max(rms)
    if max_rms == 0:
        max_rms = 1

    num_windows = len(rms) // frames_per_window

    print(f"{'Time':<15} {'Energy':>7} {'Bar (visual)'}")
    print("-" * 60)

    energies = []
    for i in range(num_windows):
        start = i * frames_per_window
        end = (i + 1) * frames_per_window
        avg = np.mean(rms[start:end])
        pct = int((avg / max_rms) * 100)
        energies.append(pct)

        bar = "█" * (pct // 2)
        start_time = i * window_seconds
        print(f"{format_time(start_time):<15} {pct:>5}%  {bar}")

    # Detect significant energy shifts
    print("\n--- Energy Shifts (>20% change) ---")
    found = False
    for i in range(1, len(energies)):
        diff = energies[i] - energies[i-1]
        if abs(diff) > 20:
            t = i * window_seconds
            direction = "UP" if diff > 0 else "DOWN"
            print(f"  {format_time(t)} — energy {direction} {abs(diff)}% ({energies[i-1]}% → {energies[i]}%)")
            found = True
    if not found:
        print("  No dramatic energy shifts detected (all changes < 20%)")


def analyze_sections(y, sr):
    """Detect section boundaries using spectral novelty."""
    print("\n=== SECTION BOUNDARIES (spectral novelty) ===")

    # Use spectral features to detect changes
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    bounds = librosa.segment.agglomerative(mfcc, k=8)
    bound_times = librosa.frames_to_time(bounds, sr=sr)

    print("Detected section changes at:")
    for i, t in enumerate(bound_times):
        if t > 0.5:  # Skip very start
            print(f"  Section {i+1}: {format_time(t)}")


def analyze_spectral_balance(y, sr):
    """Show low vs mid vs high frequency balance over time — helps identify
    when bass is prominent vs guitar vs cymbals."""
    print("\n=== SPECTRAL BALANCE (low/mid/high) ===")

    # Compute spectrogram
    S = np.abs(librosa.stft(y))
    freqs = librosa.fft_frequencies(sr=sr)

    # Define bands
    low_mask = freqs < 250       # Bass, kick
    mid_mask = (freqs >= 250) & (freqs < 2000)  # Guitar, vocals
    high_mask = freqs >= 2000    # Cymbals, presence

    window_seconds = 10
    hop_length = 512
    frames_per_window = int(window_seconds * sr / hop_length)
    num_windows = S.shape[1] // frames_per_window

    print(f"{'Time':<15} {'Low(<250Hz)':>12} {'Mid(250-2k)':>12} {'High(>2kHz)':>12} {'Balance'}")
    print("-" * 70)

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

        # Determine dominant
        dominant = "BASS-heavy" if l_pct > 45 else "MID-heavy" if m_pct > 50 else "balanced"

        start_time = i * window_seconds
        print(f"{format_time(start_time):<15} {l_pct:>10}% {m_pct:>10}% {h_pct:>10}%  {dominant}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 audio-deep-analysis.py <audio-file>")
        sys.exit(1)

    filepath = sys.argv[1]
    print(f"Loading: {os.path.basename(filepath)}")
    y, sr = librosa.load(filepath, sr=22050)
    duration = librosa.get_duration(y=y, sr=sr)
    print(f"Duration: {int(duration//60)}:{int(duration%60):02d}\n")

    analyze_energy(y, sr)
    analyze_chords(y, sr)
    analyze_sections(y, sr)
    analyze_spectral_balance(y, sr)


if __name__ == "__main__":
    main()
