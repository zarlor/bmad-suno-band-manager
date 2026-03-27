#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["librosa", "numpy"]
# ///
"""
Batch full analysis -- tempo stability, energy arc, section boundaries,
and spectral balance for every track in a catalog directory.

Outputs a summary report in JSON or Markdown text format.

Exit codes:
  0 = analysis completed successfully
  1 = invalid arguments or no audio files found
  2 = missing dependencies (librosa/numpy)
"""

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "_shared"))
from audio_deps import require_audio_deps


def format_time(seconds):
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m}:{s:02d}"


def analyze_track(filepath):
    """Full analysis of a single track. Returns a dict of results."""
    import librosa
    import numpy as np

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


def format_json(all_results):
    """Format results as standard module JSON."""
    tracks = []
    for r in all_results:
        if 'error' in r:
            tracks.append({
                'file': r['file'],
                'status': 'error',
                'error': r['error'],
            })
            continue
        tracks.append({
            'file': r['file'],
            'duration': round(r['duration'], 1),
            'duration_display': format_time(r['duration']),
            'bpm': r['bpm'],
            'bpm_stability': r['bpm_stability'],
            'bpm_range': list(r['bpm_range']),
            'key': r['key'],
            'key_confidence': r['key_conf'],
            'dynamic_character': r['dynamic_character'],
            'energy': {
                'min': r['energy_min'],
                'max': r['energy_max'],
                'range': r['energy_range'],
                'shifts': r['energy_shifts'],
                'profile': r['energy_profile'],
            },
            'spectral_balance': {
                'low_pct': r['spectral_low'],
                'mid_pct': r['spectral_mid'],
                'high_pct': r['spectral_high'],
            },
            'sections': r['sections'],
        })

    return json.dumps({
        'script': 'batch-full-analysis',
        'status': 'ok',
        'track_count': len(all_results),
        'tracks': tracks,
    }, indent=2)


def format_text(all_results):
    """Format results as a Markdown report."""
    lines = []
    lines.append("# Catalog Audio Analysis\n")
    lines.append("## Summary Table\n")
    lines.append("| Track | Duration | BPM | Stability | Key | Dyn Range | Character |")
    lines.append("|-------|----------|-----|-----------|-----|-----------|----------|")
    for r in all_results:
        if 'error' in r:
            continue
        dur = format_time(r['duration'])
        lines.append(
            f"| {r['file'].replace('.mp3','')} | {dur} | {r['bpm']} "
            f"| {r['bpm_stability']} | {r['key']} | {r['energy_range']}% "
            f"| {r['dynamic_character']} |"
        )

    lines.append("\n## Energy Shifts (>20% jumps)\n")
    for r in all_results:
        if 'error' in r or not r.get('energy_shifts'):
            continue
        lines.append(f"### {r['file'].replace('.mp3','')}")
        for shift in r['energy_shifts']:
            lines.append(f"- {shift}")
        lines.append("")

    lines.append("\n## Section Boundaries\n")
    lines.append("| Track | Sections |")
    lines.append("|-------|----------|")
    for r in all_results:
        if 'error' in r:
            continue
        sections = r.get('sections', [])
        lines.append(f"| {r['file'].replace('.mp3','')} | {' / '.join(sections)} |")

    lines.append("\n## Spectral Balance\n")
    lines.append("| Track | Low (<250Hz) | Mid (250-2kHz) | High (>2kHz) |")
    lines.append("|-------|-------------|----------------|-------------|")
    for r in all_results:
        if 'error' in r:
            continue
        lines.append(
            f"| {r['file'].replace('.mp3','')} | {r['spectral_low']}% "
            f"| {r['spectral_mid']}% | {r['spectral_high']}% |"
        )

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="Batch audio analysis: tempo, energy, sections, spectral balance."
    )
    parser.add_argument(
        "--audio-dir", default="docs/audio",
        help="Directory containing .mp3 files (default: docs/audio)",
    )
    parser.add_argument(
        "--format", choices=["json", "text"], default="json",
        help="Output format (default: json)",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path (default: stdout)",
    )
    args = parser.parse_args()

    require_audio_deps()
    import librosa  # noqa: F401
    import numpy as np  # noqa: F401

    audio_dir = args.audio_dir
    if not os.path.isdir(audio_dir):
        print(json.dumps({
            "script": "batch-full-analysis",
            "status": "fail",
            "error": f"Audio directory not found: {audio_dir}",
        }), file=sys.stderr)
        sys.exit(1)

    mp3s = sorted([
        os.path.join(audio_dir, f)
        for f in os.listdir(audio_dir)
        if f.endswith('.mp3')
    ])

    if not mp3s:
        print(json.dumps({
            "script": "batch-full-analysis",
            "status": "fail",
            "error": f"No .mp3 files found in: {audio_dir}",
        }), file=sys.stderr)
        sys.exit(1)

    print(f"Analyzing {len(mp3s)} tracks...\n", file=sys.stderr)

    all_results = []
    for filepath in mp3s:
        print(f"  Processing: {os.path.basename(filepath)}...", end="", flush=True, file=sys.stderr)
        result = analyze_track(filepath)
        all_results.append(result)
        if 'error' in result:
            print(f" ERROR: {result['error']}", file=sys.stderr)
        else:
            print(f" done ({result['bpm']} BPM, {result['key']}, {result['dynamic_character']})", file=sys.stderr)

    # Format output
    if args.format == "json":
        output = format_json(all_results)
    else:
        output = format_text(all_results)

    # Write output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"\nReport saved to: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
