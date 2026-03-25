#!/usr/bin/env python3
"""Chord/key progression analysis — shows estimated chords over time
using chroma features with beat-synchronized analysis for cleaner results."""

import sys
import os
import librosa
import numpy as np

PITCH_CLASSES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Common chord templates (root position triads)
CHORD_TEMPLATES = {}
for i, note in enumerate(PITCH_CLASSES):
    # Major triad: root, major 3rd, perfect 5th
    major = np.zeros(12)
    major[i] = 1.0
    major[(i + 4) % 12] = 0.8
    major[(i + 7) % 12] = 0.8
    CHORD_TEMPLATES[f"{note}"] = major

    # Minor triad: root, minor 3rd, perfect 5th
    minor = np.zeros(12)
    minor[i] = 1.0
    minor[(i + 3) % 12] = 0.8
    minor[(i + 7) % 12] = 0.8
    CHORD_TEMPLATES[f"{note}m"] = minor

    # Power chord (5th): root, perfect 5th
    power = np.zeros(12)
    power[i] = 1.0
    power[(i + 7) % 12] = 0.9
    CHORD_TEMPLATES[f"{note}5"] = power


def match_chord(chroma_vector):
    """Match a chroma vector to the best chord template."""
    best_score = -1
    best_chord = "?"
    norm = np.linalg.norm(chroma_vector)
    if norm < 0.001:
        return "silence", 0.0

    chroma_norm = chroma_vector / norm

    for name, template in CHORD_TEMPLATES.items():
        t_norm = template / np.linalg.norm(template)
        score = np.dot(chroma_norm, t_norm)
        if score > best_score:
            best_score = score
            best_chord = name

    return best_chord, best_score


def format_time(seconds):
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m}:{s:02d}"


def analyze_chords(filepath):
    print(f"Loading: {os.path.basename(filepath)}")
    y, sr = librosa.load(filepath, sr=22050)
    duration = librosa.get_duration(y=y, sr=sr)
    print(f"Duration: {format_time(duration)}\n")

    # Beat-synchronous chroma for cleaner chord detection
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)

    # Use CQT chroma (better for music)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)

    # Aggregate chroma by measures (every 4 beats)
    print(f"{'Time':<10} {'Chord':<8} {'Conf':>5}  {'Chroma Profile'}")
    print("-" * 70)

    measure_size = 4  # beats per measure
    prev_chord = None
    chord_sequence = []

    for i in range(0, len(beats) - measure_size, measure_size):
        start_frame = beats[i]
        end_frame = beats[min(i + measure_size, len(beats) - 1)]

        if start_frame >= chroma.shape[1] or end_frame >= chroma.shape[1]:
            break

        measure_chroma = np.mean(chroma[:, start_frame:end_frame], axis=1)
        chord, conf = match_chord(measure_chroma)
        start_time = beat_times[i]

        # Show top 3 pitch classes
        top_3_idx = np.argsort(measure_chroma)[-3:][::-1]
        top_3 = [PITCH_CLASSES[p] for p in top_3_idx]

        marker = " <<<" if chord != prev_chord and prev_chord is not None else ""
        print(f"{format_time(start_time):<10} {chord:<8} {conf:>5.2f}  [{', '.join(top_3)}]{marker}")

        chord_sequence.append((start_time, chord, conf))
        prev_chord = chord

    # Summary: chord changes
    print(f"\n{'='*50}")
    print("CHORD CHANGE SUMMARY")
    print("=" * 50)

    changes = []
    for i in range(1, len(chord_sequence)):
        if chord_sequence[i][1] != chord_sequence[i-1][1]:
            changes.append((
                chord_sequence[i][0],
                chord_sequence[i-1][1],
                chord_sequence[i][1]
            ))

    if changes:
        print(f"{len(changes)} chord changes detected:\n")
        for t, from_c, to_c in changes:
            print(f"  {format_time(t)} — {from_c} → {to_c}")
    else:
        print("No chord changes detected (single chord throughout)")

    # Key center summary
    print(f"\n{'='*50}")
    print("KEY CENTER SUMMARY (by section)")
    print("=" * 50)

    # Group into ~30 second sections
    section_size = 30
    num_sections = int(np.ceil(duration / section_size))

    major_profile = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
    minor_profile = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

    for s in range(num_sections):
        start_sec = s * section_size
        end_sec = min((s + 1) * section_size, duration)
        start_frame = int(start_sec * sr / 512)
        end_frame = int(end_sec * sr / 512)
        end_frame = min(end_frame, chroma.shape[1])

        if start_frame >= end_frame:
            break

        section_chroma = np.mean(chroma[:, start_frame:end_frame], axis=1)

        best_corr = -1
        best_key = "Unknown"
        for i in range(12):
            rolled = np.roll(section_chroma, -i)
            for profile, mode in [(major_profile, "major"), (minor_profile, "minor")]:
                corr = np.corrcoef(rolled, profile)[0, 1]
                if corr > best_corr:
                    best_corr = corr
                    best_key = f"{PITCH_CLASSES[i]} {mode}"

        print(f"  {format_time(start_sec)}-{format_time(end_sec)}: {best_key} (conf: {best_corr:.3f})")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 chord-progression.py <audio-file>")
        sys.exit(1)
    analyze_chords(sys.argv[1])
