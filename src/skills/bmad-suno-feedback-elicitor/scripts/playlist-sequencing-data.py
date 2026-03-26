#!/usr/bin/env python3
"""Generate playlist sequencing data: Camelot codes, entry/exit keys,
energy levels, and transition compatibility for the full catalog."""

import os
import sys
import librosa
import numpy as np

PITCH_CLASSES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Camelot wheel mapping
CAMELOT = {
    'C major': '8B', 'A minor': '8A',
    'G major': '9B', 'E minor': '9A',
    'D major': '10B', 'B minor': '10A',
    'A major': '11B', 'F# minor': '11A',
    'E major': '12B', 'C# minor': '12A',
    'B major': '1B', 'G# minor': '1A',
    'F# major': '2B', 'D# minor': '2A',
    'C# major': '3B', 'A# minor': '3A',
    'G# major': '4B', 'F minor': '4A',
    'D# major': '5B', 'C minor': '5A',
    'A# major': '6B', 'G minor': '6A',
    'F major': '7B', 'D minor': '7A',
    # Enharmonic equivalents
    'Db major': '3B', 'Bb minor': '3A',
    'Ab major': '4B', 'Eb minor': '2A',
    'Eb major': '5B', 'Bb major': '6B',
    'Gb major': '2B',
}

MAJOR_PROFILE = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MINOR_PROFILE = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


def detect_key(chroma_segment):
    """Detect key from a chroma segment."""
    avg = np.mean(chroma_segment, axis=1)
    best_corr = -1
    best_key = "Unknown"
    for i in range(12):
        rolled = np.roll(avg, -i)
        for profile, mode in [(MAJOR_PROFILE, "major"), (MINOR_PROFILE, "minor")]:
            corr = np.corrcoef(rolled, profile)[0, 1]
            if corr > best_corr:
                best_corr = corr
                best_key = f"{PITCH_CLASSES[i]} {mode}"
    return best_key, best_corr


def get_camelot(key):
    """Convert key name to Camelot code."""
    return CAMELOT.get(key, "??")


def camelot_distance(code1, code2):
    """Calculate distance on Camelot wheel. 0=same, 1=adjacent, etc."""
    if code1 == "??" or code2 == "??":
        return -1
    num1, letter1 = int(code1[:-1]), code1[-1]
    num2, letter2 = int(code2[:-1]), code2[-1]

    # Same position
    if code1 == code2:
        return 0
    # Relative major/minor (same number, different letter)
    if num1 == num2:
        return 0.5
    # Adjacent numbers, same letter
    num_dist = min(abs(num1 - num2), 12 - abs(num1 - num2))
    if letter1 == letter2 and num_dist == 1:
        return 1
    if letter1 == letter2 and num_dist == 2:
        return 2
    # Different letter + different number
    return num_dist + 0.5


def format_time(seconds):
    return f"{int(seconds//60)}:{int(seconds%60):02d}"


def analyze_track(filepath):
    """Extract sequencing data for a single track."""
    y, sr = librosa.load(filepath, sr=22050)
    duration = librosa.get_duration(y=y, sr=sr)

    # Overall key
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    overall_key, overall_conf = detect_key(chroma)

    # Entry key (first 30 seconds)
    entry_frames = int(30 * sr / 512)
    entry_key, entry_conf = detect_key(chroma[:, :min(entry_frames, chroma.shape[1])])

    # Exit key (last 30 seconds)
    exit_start = max(0, chroma.shape[1] - entry_frames)
    exit_key, exit_conf = detect_key(chroma[:, exit_start:])

    # BPM
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    bpm = float(tempo[0]) if hasattr(tempo, '__len__') else float(tempo)

    # Energy level (normalize to 1-10 scale)
    rms = librosa.feature.rms(y=y)[0]
    avg_energy = np.mean(rms)
    max_possible = np.max(rms) * 1.2  # leave headroom
    energy_pct = avg_energy / max_possible if max_possible > 0 else 0
    energy_level = max(1, min(10, int(energy_pct * 10) + 3))  # offset for rock/metal bias

    # Intro energy (first 15 sec)
    intro_frames = int(15 * sr / 512)
    intro_energy = np.mean(rms[:min(intro_frames, len(rms))])
    intro_pct = intro_energy / (np.max(rms) if np.max(rms) > 0 else 1) * 100

    # Outro energy (last 15 sec)
    outro_start = max(0, len(rms) - intro_frames)
    outro_energy = np.mean(rms[outro_start:])
    outro_pct = outro_energy / (np.max(rms) if np.max(rms) > 0 else 1) * 100

    return {
        'duration': duration,
        'bpm': round(bpm, 1),
        'overall_key': overall_key,
        'overall_conf': round(overall_conf, 3),
        'overall_camelot': get_camelot(overall_key),
        'entry_key': entry_key,
        'entry_conf': round(entry_conf, 3),
        'entry_camelot': get_camelot(entry_key),
        'exit_key': exit_key,
        'exit_conf': round(exit_conf, 3),
        'exit_camelot': get_camelot(exit_key),
        'energy_level': energy_level,
        'intro_energy_pct': round(intro_pct),
        'outro_energy_pct': round(outro_pct),
    }


# Playlist order mapping: track name -> audio filename
PLAYLIST_ORDER = [
    ("Global Boxing", "Global Boxing.mp3"),
    ("Whatever It Is", "Whatever it Is.mp3"),
    ("Back Woods Rushin', City Slow", "Backwoods Rushin', City Slow.mp3"),
    ("The Mask", "The Mask.mp3"),
    ("Mirror Image", "egamI rorriM_Mirror Image.mp3"),
    ("Players, Inc.", "Players, Inc..mp3"),
    ("Bloodlust", "Bloodlust.mp3"),
    ("Distant Mourning", "Distant Mourning.mp3"),
    ("Unseen Reality", "Unseen Reality.mp3"),
    ("The Undeniable Rightness of Being", "The Undeniable Rightness of Being.mp3"),
    ("On a Silent Rock", "On a silent rock.mp3"),
    ("Science Fiction", "Science Fiction.mp3"),
    ("Obviously", "Obviously.mp3"),
    ("Damned If I Don't", "Damned If I Don't.mp3"),
    ("The Grey (Version 1)", "The Grey (1).mp3"),
    ("Eyes", "Eyes.mp3"),
    ("From Now Until...", "From now until....mp3"),
    ("Distant--", "Distant—.mp3"),
    ("Breast Feeding", "Breast Feeding.mp3"),
    ("The Fire That Never Stops", "The Fire That Never Stops.mp3"),
    ("The Life of Walther Who?", "The Life of Walther Who_.mp3"),
    ("Promotion of Outer Chaos", "Promotion of Outer Chaos from Inner Order.mp3"),
    ("Sightless Black", "Sightless Black.mp3"),
    ("Spiraling Prophecies?", "Spiraling Prophecies_.mp3"),
    ("Always Right", "Always Right.mp3"),
    ("Want", "Want.mp3"),
    ("Solitary Soul Search", "Solitary Soul Search.mp3"),
    ("Look Into the Cracks", "Look Into the Cracks.mp3"),
    ("Contradictions", "Contradictions.mp3"),
    ("The Grey (Version 2)", "The Grey.mp3"),
    ("The Final Bows", "The Final Bows.mp3"),
]


def main():
    audio_dir = sys.argv[1] if len(sys.argv) > 1 else "docs/audio"

    print("Analyzing playlist sequencing data...\n")

    results = []
    for track_name, filename in PLAYLIST_ORDER:
        filepath = os.path.join(audio_dir, filename)
        if not os.path.exists(filepath):
            print(f"  MISSING: {filename}")
            results.append({'name': track_name, 'error': 'file not found'})
            continue
        print(f"  {track_name}...", end="", flush=True)
        data = analyze_track(filepath)
        data['name'] = track_name
        results.append(data)
        print(f" {data['bpm']} BPM | {data['overall_key']} ({data['overall_camelot']}) | Entry: {data['entry_camelot']} | Exit: {data['exit_camelot']} | E:{data['energy_level']}")

    # Sequencing report
    print(f"\n{'='*130}")
    print("PLAYLIST SEQUENCING ANALYSIS")
    print(f"{'='*130}\n")

    print(f"{'#':>2} {'Track':<40} {'BPM':>5} {'Key':<12} {'Cam':>4} {'Entry':>5} {'Exit':>5} {'E':>2} {'In%':>4} {'Out%':>4} {'Transition'}")
    print("-" * 130)

    for i, r in enumerate(results):
        if 'error' in r:
            print(f"{i+1:>2} {r['name']:<40} — MISSING —")
            continue

        # Calculate transition quality to next track
        transition = ""
        if i < len(results) - 1 and 'error' not in results[i+1]:
            next_r = results[i+1]
            # Key transition (exit of current → entry of next)
            cam_dist = camelot_distance(r['exit_camelot'], next_r['entry_camelot'])
            bpm_pct = abs(r['bpm'] - next_r['bpm']) / r['bpm'] * 100

            key_quality = "PERFECT" if cam_dist <= 0.5 else "GOOD" if cam_dist <= 1 else "OK" if cam_dist <= 2 else "JARRING"
            bpm_quality = "smooth" if bpm_pct < 3 else "ok" if bpm_pct < 6 else f"jump({bpm_pct:.0f}%)"

            transition = f"→ Key:{key_quality}({cam_dist:.0f}) BPM:{bpm_quality}"

        print(f"{i+1:>2} {r['name']:<40} {r['bpm']:>5} {r['overall_key']:<12} {r['overall_camelot']:>4} {r['entry_camelot']:>5} {r['exit_camelot']:>5} {r['energy_level']:>2} {r['intro_energy_pct']:>3}% {r['outro_energy_pct']:>3}%  {transition}")

    # Save report
    report_path = "docs/playlist-sequencing-data.md"
    with open(report_path, 'w') as f:
        f.write("# Solitary Fire — Playlist Sequencing Data\n")
        f.write("# Generated via librosa analysis + Camelot wheel mapping\n\n")

        f.write("## Track Data (Playlist Order)\n\n")
        f.write("| # | Track | BPM | Key | Camelot | Entry Key | Exit Key | Energy | Intro% | Outro% |\n")
        f.write("|---|-------|-----|-----|---------|-----------|----------|--------|--------|--------|\n")
        for i, r in enumerate(results):
            if 'error' in r:
                continue
            f.write(f"| {i+1} | {r['name']} | {r['bpm']} | {r['overall_key']} | {r['overall_camelot']} | {r['entry_key']} ({r['entry_camelot']}) | {r['exit_key']} ({r['exit_camelot']}) | {r['energy_level']} | {r['intro_energy_pct']}% | {r['outro_energy_pct']}% |\n")

        f.write("\n## Transition Analysis\n\n")
        f.write("| From | To | Key Distance | BPM Change | Quality |\n")
        f.write("|------|----|-------------|------------|--------|\n")
        for i in range(len(results) - 1):
            if 'error' in results[i] or 'error' in results[i+1]:
                continue
            r = results[i]
            n = results[i+1]
            cam_dist = camelot_distance(r['exit_camelot'], n['entry_camelot'])
            bpm_change = abs(r['bpm'] - n['bpm'])
            bpm_pct = bpm_change / r['bpm'] * 100
            key_q = "PERFECT" if cam_dist <= 0.5 else "GOOD" if cam_dist <= 1 else "OK" if cam_dist <= 2 else "JARRING"
            bpm_q = "smooth" if bpm_pct < 3 else "ok" if bpm_pct < 6 else f"jump ({bpm_pct:.0f}%)"
            f.write(f"| {r['name']} | {n['name']} | {cam_dist} ({r['exit_camelot']}→{n['entry_camelot']}) | {bpm_change:.0f} ({bpm_q}) | {key_q} |\n")

    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()
