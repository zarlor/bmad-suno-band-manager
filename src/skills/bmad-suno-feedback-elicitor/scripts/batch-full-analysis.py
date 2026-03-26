#!/usr/bin/env python3
"""Batch full analysis — tempo stability, energy arc, section boundaries, and spectral balance
for every track in the catalog. Outputs a summary report."""

import os
import sys
import librosa
import numpy as np

def format_time(seconds):
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m}:{s:02d}"

def analyze_track(filepath):
    """Full analysis of a single track. Returns a dict of results."""
    filename = os.path.basename(filepath)
    results = {'file': filename}

    try:
        y, sr = librosa.load(filepath, sr=22050)
        duration = librosa.get_duration(y=y, sr=sr)
        results['duration'] = duration

        # === BPM & TEMPO STABILITY ===
        tempo_overall, beats = librosa.beat.beat_track(y=y, sr=sr)
        bpm = float(tempo_overall[0]) if hasattr(tempo_overall, '__len__') else float(tempo_overall)
        results['bpm'] = round(bpm, 1)

        beat_times = librosa.frames_to_time(beats, sr=sr)
        if len(beat_times) > 3:
            ibis = np.diff(beat_times)
            local_bpms = 60.0 / ibis
            bpm_std = np.std(local_bpms)
            results['bpm_stability'] = "steady" if bpm_std < 5 else "slight variation" if bpm_std < 15 else "TEMPO CHANGES"
            results['bpm_range'] = (round(np.percentile(local_bpms, 10), 0), round(np.percentile(local_bpms, 90), 0))
        else:
            results['bpm_stability'] = "too few beats"
            results['bpm_range'] = (0, 0)

        # === KEY ===
        pitch_classes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        major_profile = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
        minor_profile = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        chroma_avg = np.mean(chroma, axis=1)
        best_corr = -1
        best_key = "Unknown"
        for i in range(12):
            rolled = np.roll(chroma_avg, -i)
            for profile, mode in [(major_profile, "major"), (minor_profile, "minor")]:
                corr = np.corrcoef(rolled, profile)[0, 1]
                if corr > best_corr:
                    best_corr = corr
                    best_key = f"{pitch_classes[i]} {mode}"
        results['key'] = best_key
        results['key_conf'] = round(best_corr, 3)

        # === ENERGY ARC ===
        rms = librosa.feature.rms(y=y)[0]
        hop_length = 512
        max_rms = np.max(rms) if np.max(rms) > 0 else 1

        # 5-second windows for energy
        window_frames = int(5 * sr / hop_length)
        num_windows = len(rms) // window_frames
        energies = []
        for i in range(num_windows):
            avg = np.mean(rms[i*window_frames:(i+1)*window_frames])
            pct = int((avg / max_rms) * 100)
            energies.append(pct)

        results['energy_min'] = min(energies) if energies else 0
        results['energy_max'] = max(energies) if energies else 0
        results['energy_range'] = results['energy_max'] - results['energy_min']

        # Detect significant energy shifts
        shifts = []
        for i in range(1, len(energies)):
            diff = energies[i] - energies[i-1]
            if abs(diff) > 20:
                t = i * 5
                direction = "UP" if diff > 0 else "DOWN"
                shifts.append(f"{format_time(t)} {direction} {abs(diff)}%")
        results['energy_shifts'] = shifts
        results['energy_profile'] = energies

        # Classify dynamic character
        if results['energy_range'] < 20:
            results['dynamic_character'] = "FLAT — minimal dynamics"
        elif results['energy_range'] < 40:
            results['dynamic_character'] = "MODERATE — some dynamic range"
        elif len(shifts) >= 3:
            results['dynamic_character'] = "HIGHLY DYNAMIC — big swings"
        else:
            results['dynamic_character'] = "DYNAMIC — wide range"

        # === SPECTRAL BALANCE ===
        S = np.abs(librosa.stft(y))
        freqs = librosa.fft_frequencies(sr=sr)
        low_mask = freqs < 250
        mid_mask = (freqs >= 250) & (freqs < 2000)
        high_mask = freqs >= 2000

        low = np.mean(S[low_mask, :])
        mid = np.mean(S[mid_mask, :])
        high = np.mean(S[high_mask, :])
        total = low + mid + high
        if total == 0:
            total = 1
        results['spectral_low'] = int(low / total * 100)
        results['spectral_mid'] = int(mid / total * 100)
        results['spectral_high'] = int(high / total * 100)

        # === SECTION BOUNDARIES ===
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        n_sections = min(8, max(3, int(duration / 30)))  # Scale sections by duration
        bounds = librosa.segment.agglomerative(mfcc, k=n_sections)
        bound_times = librosa.frames_to_time(bounds, sr=sr)
        results['sections'] = [format_time(t) for t in bound_times if t > 0.5]

    except Exception as e:
        results['error'] = str(e)

    return results


def main():
    audio_dir = sys.argv[1] if len(sys.argv) > 1 else "docs/audio"

    mp3s = sorted([
        os.path.join(audio_dir, f)
        for f in os.listdir(audio_dir)
        if f.endswith('.mp3')
    ])

    print(f"Analyzing {len(mp3s)} tracks...\n")

    all_results = []
    for filepath in mp3s:
        print(f"  Processing: {os.path.basename(filepath)}...", end="", flush=True)
        result = analyze_track(filepath)
        all_results.append(result)
        if 'error' in result:
            print(f" ERROR: {result['error']}")
        else:
            print(f" done ({result['bpm']} BPM, {result['key']}, {result['dynamic_character']})")

    # === SUMMARY REPORT ===
    print("\n" + "=" * 120)
    print("CATALOG SUMMARY REPORT")
    print("=" * 120)

    print(f"\n{'Track':<45} {'Dur':>5} {'BPM':>6} {'Stability':<18} {'Key':<12} {'Dyn Range':>9} {'Character'}")
    print("-" * 120)

    for r in all_results:
        if 'error' in r:
            print(f"{r['file']:<45} ERROR")
            continue
        dur = format_time(r['duration'])
        print(f"{r['file']:<45} {dur:>5} {r['bpm']:>6} {r['bpm_stability']:<18} {r['key']:<12} {r['energy_range']:>7}%  {r['dynamic_character']}")

    # Energy shifts detail
    print(f"\n{'='*80}")
    print("ENERGY SHIFTS (>20% jumps)")
    print("=" * 80)
    for r in all_results:
        if 'error' in r or not r.get('energy_shifts'):
            continue
        print(f"\n{r['file']}:")
        for shift in r['energy_shifts']:
            print(f"  {shift}")

    # Section boundaries
    print(f"\n{'='*80}")
    print("SECTION BOUNDARIES")
    print("=" * 80)
    for r in all_results:
        if 'error' in r:
            continue
        sections = r.get('sections', [])
        if sections:
            print(f"{r['file']:<45} {' | '.join(sections)}")

    # Spectral balance
    print(f"\n{'='*80}")
    print("SPECTRAL BALANCE (Low / Mid / High)")
    print("=" * 80)
    for r in all_results:
        if 'error' in r:
            continue
        print(f"{r['file']:<45} Low:{r['spectral_low']:>3}%  Mid:{r['spectral_mid']:>3}%  High:{r['spectral_high']:>3}%")

    # Write machine-readable summary
    report_path = "docs/catalog-analysis-report.md"
    with open(report_path, 'w') as f:
        f.write("# Solitary Fire — Full Catalog Audio Analysis\n")
        f.write("# Generated via librosa 0.11.0 batch analysis\n\n")

        f.write("## Summary Table\n\n")
        f.write("| Track | Duration | BPM | Stability | Key | Dyn Range | Character |\n")
        f.write("|-------|----------|-----|-----------|-----|-----------|----------|\n")
        for r in all_results:
            if 'error' in r:
                continue
            dur = format_time(r['duration'])
            f.write(f"| {r['file'].replace('.mp3','')} | {dur} | {r['bpm']} | {r['bpm_stability']} | {r['key']} | {r['energy_range']}% | {r['dynamic_character']} |\n")

        f.write("\n## Energy Shifts (>20% jumps)\n\n")
        for r in all_results:
            if 'error' in r or not r.get('energy_shifts'):
                continue
            f.write(f"### {r['file'].replace('.mp3','')}\n")
            for shift in r['energy_shifts']:
                f.write(f"- {shift}\n")
            f.write("\n")

        f.write("\n## Section Boundaries\n\n")
        f.write("| Track | Sections |\n")
        f.write("|-------|----------|\n")
        for r in all_results:
            if 'error' in r:
                continue
            sections = r.get('sections', [])
            f.write(f"| {r['file'].replace('.mp3','')} | {' / '.join(sections)} |\n")

        f.write("\n## Spectral Balance\n\n")
        f.write("| Track | Low (<250Hz) | Mid (250-2kHz) | High (>2kHz) |\n")
        f.write("|-------|-------------|----------------|-------------|\n")
        for r in all_results:
            if 'error' in r:
                continue
            f.write(f"| {r['file'].replace('.mp3','')} | {r['spectral_low']}% | {r['spectral_mid']}% | {r['spectral_high']}% |\n")

    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()
