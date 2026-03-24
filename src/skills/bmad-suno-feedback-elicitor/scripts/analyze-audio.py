#!/usr/bin/env python3
"""Batch audio analysis for Solitary Fire catalog.
Extracts BPM (librosa + aubio), estimated key, and duration for all MP3s."""

import os
import sys
import librosa
import numpy as np

def get_key(y, sr):
    """Estimate musical key using chroma features."""
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


def main():
    audio_dir = sys.argv[1] if len(sys.argv) > 1 else "docs/audio"

    mp3s = sorted([
        os.path.join(audio_dir, f)
        for f in os.listdir(audio_dir)
        if f.endswith('.mp3')
    ])

    print(f"Analyzing {len(mp3s)} tracks...\n")
    print(f"{'Track':<50} {'Duration':>8} {'BPM(lib)':>9} {'BPM(aub)':>9} {'Key':<15} {'Conf':>5}")
    print("-" * 100)

    results = []
    for filepath in mp3s:
        result = analyze_file(filepath)
        results.append(result)

        if 'error' in result:
            print(f"{result['file']:<50} ERROR: {result['error']}")
        else:
            print(f"{result['file']:<50} {result['duration']:>8} {result['bpm_librosa']:>9} {result['bpm_aubio']:>9} {result['key']:<15} {result['key_confidence']:>5}")

    # Summary stats
    valid = [r for r in results if 'error' not in r]
    if valid:
        bpms = [r['bpm_librosa'] for r in valid]
        print(f"\n{'='*100}")
        print(f"BPM range (librosa): {min(bpms):.0f} - {max(bpms):.0f}")
        print(f"Tracks analyzed: {len(valid)}/{len(mp3s)}")


if __name__ == "__main__":
    main()
