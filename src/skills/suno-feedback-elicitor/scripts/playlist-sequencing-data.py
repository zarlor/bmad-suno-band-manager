#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["librosa>=0.10", "numpy>=1.24", "pyyaml>=6.0"]
# ///
"""
Generate playlist sequencing data: Camelot codes, entry/exit keys,
energy levels, and transition compatibility for an audio catalog.

When given a --playlist YAML config, uses the specified track order and
album name. Without a config, auto-discovers all .mp3 files in the
audio directory (sorted alphabetically).

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
from companion_writer import update_companion, resolve_companion_path
from json_archiver import resolve_archive_arg, write_archive

SCRIPT_NAME = "playlist-sequencing-data"

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


def detect_key(chroma_segment):
    """Detect key from a chroma segment."""
    import numpy as np

    MAJOR_PROFILE = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
    MINOR_PROFILE = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

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
    import librosa
    import numpy as np

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


def load_playlist(playlist_path):
    """Load playlist config from a YAML file. Returns (album_name, track_list)."""
    import yaml

    with open(playlist_path, 'r') as f:
        config = yaml.safe_load(f)

    album = config.get('album', 'Audio Analysis')
    tracks = [
        (t['name'], t['file'])
        for t in config.get('tracks', [])
    ]
    return album, tracks


def discover_tracks(audio_dir):
    """Auto-discover .mp3 files in a directory. Returns (album_name, track_list)."""
    mp3s = sorted(f for f in os.listdir(audio_dir) if f.endswith('.mp3'))
    tracks = [
        (os.path.splitext(f)[0], f)
        for f in mp3s
    ]
    return "Audio Analysis", tracks


def format_json(album_name, results):
    """Format results as standard module JSON."""
    tracks = []
    for i, r in enumerate(results):
        if 'error' in r:
            tracks.append({
                'position': i + 1,
                'name': r['name'],
                'status': 'error',
                'error': r['error'],
            })
            continue
        entry = {
            'position': i + 1,
            'name': r['name'],
            'duration': round(r['duration'], 1),
            'duration_display': format_time(r['duration']),
            'bpm': r['bpm'],
            'key': {
                'overall': r['overall_key'],
                'overall_confidence': r['overall_conf'],
                'overall_camelot': r['overall_camelot'],
                'entry': r['entry_key'],
                'entry_confidence': r['entry_conf'],
                'entry_camelot': r['entry_camelot'],
                'exit': r['exit_key'],
                'exit_confidence': r['exit_conf'],
                'exit_camelot': r['exit_camelot'],
            },
            'energy': {
                'level': r['energy_level'],
                'intro_pct': r['intro_energy_pct'],
                'outro_pct': r['outro_energy_pct'],
            },
        }
        # Add transition data if available
        if 'transition' in r:
            entry['transition_to_next'] = r['transition']
        tracks.append(entry)

    return json.dumps({
        'script': 'playlist-sequencing-data',
        'status': 'ok',
        'album': album_name,
        'track_count': len(results),
        'tracks': tracks,
    }, indent=2)


def format_text(album_name, results):
    """Format results as a Markdown report."""
    lines = []
    lines.append(f"# {album_name} -- Playlist Sequencing Data")
    lines.append("# Generated via librosa analysis + Camelot wheel mapping\n")

    lines.append("## Track Data (Playlist Order)\n")
    lines.append("| # | Track | BPM | Key | Camelot | Entry Key | Exit Key | Energy | Intro% | Outro% |")
    lines.append("|---|-------|-----|-----|---------|-----------|----------|--------|--------|--------|")
    for i, r in enumerate(results):
        if 'error' in r:
            continue
        lines.append(
            f"| {i+1} | {r['name']} | {r['bpm']} | {r['overall_key']} "
            f"| {r['overall_camelot']} | {r['entry_key']} ({r['entry_camelot']}) "
            f"| {r['exit_key']} ({r['exit_camelot']}) | {r['energy_level']} "
            f"| {r['intro_energy_pct']}% | {r['outro_energy_pct']}% |"
        )

    lines.append("\n## Transition Analysis\n")
    lines.append("| From | To | Key Distance | BPM Change | Quality |")
    lines.append("|------|----|-------------|------------|---------|")
    for i in range(len(results) - 1):
        if 'error' in results[i] or 'error' in results[i+1]:
            continue
        r = results[i]
        n = results[i+1]
        cam_dist = camelot_distance(r['exit_camelot'], n['entry_camelot'])
        bpm_change = abs(r['bpm'] - n['bpm'])
        bpm_pct = bpm_change / r['bpm'] * 100 if r['bpm'] > 0 else 0
        key_q = "PERFECT" if cam_dist <= 0.5 else "GOOD" if cam_dist <= 1 else "OK" if cam_dist <= 2 else "JARRING"
        bpm_q = "smooth" if bpm_pct < 3 else "ok" if bpm_pct < 6 else f"jump ({bpm_pct:.0f}%)"
        lines.append(
            f"| {r['name']} | {n['name']} | {cam_dist} "
            f"({r['exit_camelot']}->{n['entry_camelot']}) "
            f"| {bpm_change:.0f} ({bpm_q}) | {key_q} |"
        )

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="Playlist sequencing analysis: keys, Camelot codes, energy, transitions."
    )
    parser.add_argument(
        "--playlist",
        help="Path to YAML playlist config file (for ordered analysis with album metadata).",
    )
    parser.add_argument(
        "--audio-dir", default="docs/audio",
        help="Directory containing .mp3 files (default: docs/audio).",
    )
    parser.add_argument(
        "--format", choices=["json", "text"], default="json",
        help="Output format (default: json).",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path (default: stdout).",
    )
    parser.add_argument(
        "--archive", nargs="?", const="", default="",
        help=(
            "Persist full JSON output to a per-playlist archive. "
            "With no path: writes to docs/audio-analysis/playlists/<album>.json. "
            "Pass an explicit path to override. Default: ON."
        ),
    )
    parser.add_argument(
        "--no-archive", dest="archive", action="store_const", const=None,
        help="Skip writing the JSON archive.",
    )
    parser.add_argument(
        "--companion", nargs="?", const="", default="",
        help=(
            "Refresh the canonical Markdown companion file. "
            "With no path: writes to docs/playlist-sequencing-data.md. "
            "Pass an explicit path to override. Default: ON."
        ),
    )
    parser.add_argument(
        "--no-companion", dest="companion", action="store_const", const=None,
        help="Skip refreshing the Markdown companion file.",
    )
    args = parser.parse_args()

    require_audio_deps()
    import librosa  # noqa: F401
    import numpy as np  # noqa: F401

    # Build track list from playlist config or auto-discovery
    if args.playlist:
        if not os.path.isfile(args.playlist):
            print(json.dumps({
                "script": "playlist-sequencing-data",
                "status": "fail",
                "error": f"Playlist config not found: {args.playlist}",
            }), file=sys.stderr)
            sys.exit(1)
        album_name, track_list = load_playlist(args.playlist)
    else:
        if not os.path.isdir(args.audio_dir):
            print(json.dumps({
                "script": "playlist-sequencing-data",
                "status": "fail",
                "error": f"Audio directory not found: {args.audio_dir}",
            }), file=sys.stderr)
            sys.exit(1)
        album_name, track_list = discover_tracks(args.audio_dir)

    if not track_list:
        print(json.dumps({
            "script": "playlist-sequencing-data",
            "status": "fail",
            "error": "No tracks found.",
        }), file=sys.stderr)
        sys.exit(1)

    print(f"Analyzing playlist sequencing data for: {album_name}\n", file=sys.stderr)

    results = []
    for track_name, filename in track_list:
        filepath = os.path.join(args.audio_dir, filename)
        if not os.path.exists(filepath):
            print(f"  MISSING: {filename}", file=sys.stderr)
            results.append({'name': track_name, 'error': 'file not found'})
            continue
        print(f"  {track_name}...", end="", flush=True, file=sys.stderr)
        data = analyze_track(filepath)
        data['name'] = track_name
        results.append(data)
        print(
            f" {data['bpm']} BPM | {data['overall_key']} ({data['overall_camelot']}) "
            f"| Entry: {data['entry_camelot']} | Exit: {data['exit_camelot']} "
            f"| E:{data['energy_level']}",
            file=sys.stderr,
        )

    # Compute transition data for JSON output
    for i in range(len(results) - 1):
        if 'error' in results[i] or 'error' in results[i+1]:
            continue
        r = results[i]
        n = results[i+1]
        cam_dist = camelot_distance(r['exit_camelot'], n['entry_camelot'])
        bpm_pct = abs(r['bpm'] - n['bpm']) / r['bpm'] * 100 if r['bpm'] > 0 else 0
        key_quality = "PERFECT" if cam_dist <= 0.5 else "GOOD" if cam_dist <= 1 else "OK" if cam_dist <= 2 else "JARRING"
        bpm_quality = "smooth" if bpm_pct < 3 else "ok" if bpm_pct < 6 else f"jump ({bpm_pct:.0f}%)"
        r['transition'] = {
            'to': n['name'],
            'camelot_distance': cam_dist,
            'key_quality': key_quality,
            'bpm_change': round(abs(r['bpm'] - n['bpm']), 1),
            'bpm_quality': bpm_quality,
        }

    # Format output
    if args.format == "json":
        output = format_json(album_name, results)
    else:
        output = format_text(album_name, results)

    # Write output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"\nReport saved to: {args.output}", file=sys.stderr)
    else:
        print(output)

    # JSON archive (default ON unless --no-archive)
    archive_target = resolve_archive_arg("playlists", album_name, args.archive)
    if archive_target is not None:
        try:
            json_data = json.loads(format_json(album_name, results))
        except Exception as exc:
            print(f"  WARN: archive skipped — JSON build failed: {exc}", file=sys.stderr)
        else:
            res = write_archive(archive_target, json_data)
            print(f"  ARCHIVED: {res['path']} ({res['bytes_written']} bytes)", file=sys.stderr)

    # Companion .md refresh (default ON unless --no-companion).
    # The body includes its own title + timestamp at the top so each refresh
    # updates them. Hand-curated sections live OUTSIDE the AUTOGEN markers
    # in the companion file and are preserved across refreshes.
    # Per-album companion path: docs/{album-slug}-playlist-sequencing.md so
    # multiple bands don't overwrite each other's companions.
    companion_target = resolve_companion_path(SCRIPT_NAME, args.companion, album=album_name)
    if companion_target is not None:
        from datetime import datetime, timezone as _tz
        timestamp = datetime.now(_tz.utc).isoformat()
        title_block = (
            f"# {album_name} — Playlist Sequencing Data\n"
            f"_Generated by `{SCRIPT_NAME}` on {timestamp}_\n\n"
        )
        # Drop the script's built-in title (first 2 lines) and keep the rest
        body_lines = format_text(album_name, results).split("\n")
        cut = 0
        while cut < len(body_lines):
            line = body_lines[cut]
            if line.startswith("##") or (line.strip() and not line.startswith("#")):
                break
            cut += 1
        md_body = title_block + "\n".join(body_lines[cut:])
        res = update_companion(companion_target, SCRIPT_NAME, md_body)
        print(f"  COMPANION: {res['status']} {res['path']} ({res['bytes_written']} bytes)", file=sys.stderr)


if __name__ == "__main__":
    main()
