#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["librosa", "numpy"]
# ///
"""Chord/key progression analysis -- shows estimated chords over time
using chroma features with beat-synchronized analysis for cleaner results.

Usage:
    python chord-progression.py <audio-file> [options]

    # Analyze a single track
    python chord-progression.py track.mp3

    # JSON output to file
    python chord-progression.py track.mp3 --format json -o results.json

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

SCRIPT_NAME = "chord-progression"
VERSION = "1.0.0"

PITCH_CLASSES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def _build_chord_templates():
    """Build chord templates. Requires numpy, so called after dependency check."""
    import numpy as np

    templates = {}
    for i, note in enumerate(PITCH_CLASSES):
        # Major triad: root, major 3rd, perfect 5th
        major = np.zeros(12)
        major[i] = 1.0
        major[(i + 4) % 12] = 0.8
        major[(i + 7) % 12] = 0.8
        templates[f"{note}"] = major

        # Minor triad: root, minor 3rd, perfect 5th
        minor = np.zeros(12)
        minor[i] = 1.0
        minor[(i + 3) % 12] = 0.8
        minor[(i + 7) % 12] = 0.8
        templates[f"{note}m"] = minor

        # Power chord (5th): root, perfect 5th
        power = np.zeros(12)
        power[i] = 1.0
        power[(i + 7) % 12] = 0.9
        templates[f"{note}5"] = power

    return templates


def match_chord(chroma_vector, chord_templates):
    """Match a chroma vector to the best chord template."""
    import numpy as np

    best_score = -1
    best_chord = "?"
    norm = np.linalg.norm(chroma_vector)
    if norm < 0.001:
        return "silence", 0.0

    chroma_norm = chroma_vector / norm

    for name, template in chord_templates.items():
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


def analyze_chords_text(filepath, chord_templates):
    """Run chord analysis with text output (original format)."""
    import numpy as np

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
        chord, conf = match_chord(measure_chroma, chord_templates)
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
            print(f"  {format_time(t)} \u2014 {from_c} \u2192 {to_c}")
    else:
        print("No chord changes detected (single chord throughout)")

    # Key center summary
    print(f"\n{'='*50}")
    print("KEY CENTER SUMMARY (by section)")
    print("=" * 50)

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


def analyze_chords_json(filepath, chord_templates):
    """Run chord analysis and return structured data for JSON output."""
    import numpy as np

    y, sr = librosa.load(filepath, sr=22050)
    duration = librosa.get_duration(y=y, sr=sr)

    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)

    measure_size = 4
    prev_chord = None
    chord_sequence = []
    measures = []

    for i in range(0, len(beats) - measure_size, measure_size):
        start_frame = beats[i]
        end_frame = beats[min(i + measure_size, len(beats) - 1)]

        if start_frame >= chroma.shape[1] or end_frame >= chroma.shape[1]:
            break

        measure_chroma = np.mean(chroma[:, start_frame:end_frame], axis=1)
        chord, conf = match_chord(measure_chroma, chord_templates)
        start_time = float(beat_times[i])

        top_3_idx = np.argsort(measure_chroma)[-3:][::-1]
        top_3 = [PITCH_CLASSES[p] for p in top_3_idx]

        measures.append({
            "time": round(start_time, 2),
            "chord": chord,
            "confidence": round(float(conf), 3),
            "dominant_notes": top_3,
            "is_change": chord != prev_chord and prev_chord is not None,
        })

        chord_sequence.append((start_time, chord, conf))
        prev_chord = chord

    # Chord changes
    transitions = []
    for i in range(1, len(chord_sequence)):
        if chord_sequence[i][1] != chord_sequence[i-1][1]:
            transitions.append({
                "time": round(chord_sequence[i][0], 2),
                "from": chord_sequence[i-1][1],
                "to": chord_sequence[i][1],
            })

    # Key centers by section
    section_size = 30
    num_sections = int(np.ceil(duration / section_size))
    major_profile = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
    minor_profile = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

    key_centers = []
    for s in range(num_sections):
        start_sec = s * section_size
        end_sec = min((s + 1) * section_size, duration)
        sf = int(start_sec * sr / 512)
        ef = min(int(end_sec * sr / 512), chroma.shape[1])

        if sf >= ef:
            break

        section_chroma = np.mean(chroma[:, sf:ef], axis=1)
        best_corr = -1
        best_key = "Unknown"
        for i in range(12):
            rolled = np.roll(section_chroma, -i)
            for profile, mode in [(major_profile, "major"), (minor_profile, "minor")]:
                corr = np.corrcoef(rolled, profile)[0, 1]
                if corr > best_corr:
                    best_corr = corr
                    best_key = f"{PITCH_CLASSES[i]} {mode}"

        key_centers.append({
            "time_start": start_sec,
            "time_end": round(end_sec, 2),
            "key": best_key,
            "confidence": round(float(best_corr), 3),
        })

    tempo_val = float(tempo[0]) if hasattr(tempo, '__len__') else float(tempo)

    return {
        "script": SCRIPT_NAME,
        "version": VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "pass",
        "metrics": {
            "file": os.path.basename(filepath),
            "duration_seconds": round(duration, 2),
            "bpm": round(tempo_val, 1),
            "total_measures_analyzed": len(measures),
            "chord_changes": len(transitions),
            "measures": measures,
            "transitions": transitions,
            "key_centers": key_centers,
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

    chord_templates = _build_chord_templates()

    parser = argparse.ArgumentParser(
        description="Beat-synchronized chord/key progression analysis.",
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
        analyze_chords_text(args.audio_file, chord_templates)
    else:
        result = analyze_chords_json(args.audio_file, chord_templates)
        output = json.dumps(result, indent=2)

        if args.output:
            Path(args.output).write_text(output + "\n")
        else:
            print(output)


if __name__ == "__main__":
    main()
