# /// script
# requires-python = ">=3.9"
# dependencies = []
# [tool.script.metadata]
# name = "tier-features"
# version = "2.0.0"
# description = "Returns available and unavailable Suno features for a given subscription tier"
# ///

"""Return Suno feature availability for a given subscription tier.

Maps each tier (free, pro, premier) to its available and unavailable features,
helping the agent and user understand what profile options are valid.
"""

import argparse
import json
import sys
from datetime import datetime, timezone


TIER_FEATURES = {
    "free": {
        "available": [
            "v4.5-all model",
            "50 credits/day (~10 songs)",
            "Vocal Gender selection",
            "Manual/Auto Lyrics mode",
            "Song Title",
            "1 min audio upload",
            "Song length determined by model — v4.5-all supports up to ~8 min",
            "128kbps MP3 download",
        ],
        "unavailable": [
            "v5 Pro and other paid models",
            "Commercial use",
            "Personas (consistent voice reuse)",
            "Weirdness slider (0-100)",
            "Style Influence slider (0-100)",
            "Audio Influence slider (0-100)",
            "Add Vocals / Add Instrumental",
            "Stems separation",
            "Advanced editing",
            "Studio features",
            "Studio 1.2 (Warp Markers, Remove FX, Alternates, Time Signature)",
            "MIDI export",
            "Priority queue",
            "Add-on credits",
            "320kbps MP3 / WAV download",
        ],
        "models": ["v4.5-all"],
        "sliders_available": False,
        "personas_available": False,
        "audio_influence_available": False,
        "studio_available": False,
        "song_length_max": "Determined by model — v4.5-all supports up to ~8 min",
        "download_quality": "128kbps MP3",
        "credit_cost": {"generation": 10, "extension": 5},
        "pricing": {"monthly": 0, "annual_monthly": 0},
    },
    "pro": {
        "available": [
            "All models including v5 Pro",
            "2,500 credits/month (~500 songs)",
            "Commercial use (new songs)",
            "Personas (consistent voice reuse)",
            "Weirdness slider (0-100)",
            "Style Influence slider (0-100)",
            "Audio Influence slider (0-100, with audio upload)",
            "Add Vocals / Add Instrumental",
            "Up to 12 stems",
            "8 min audio upload",
            "Advanced editing",
            "Priority queue (10 concurrent)",
            "Add-on credits",
            "Song length determined by model — v4.5/v5 support up to ~8 min",
            "320kbps MP3 + WAV download",
        ],
        "unavailable": [
            "Studio features",
            "Studio 1.2 (Warp Markers, Remove FX, Alternates, Time Signature)",
            "MIDI export",
        ],
        "models": ["v4.5-all", "v4 Pro", "v4.5 Pro", "v4.5+ Pro", "v5 Pro"],
        "legacy_models": ["v4 Pro"],
        "sliders_available": True,
        "personas_available": True,
        "audio_influence_available": True,
        "studio_available": False,
        "song_length_max": "Determined by model — v4.5/v5 support up to ~8 min",
        "download_quality": "320kbps MP3 + WAV",
        "credit_cost": {"generation": 10, "extension": 5},
        "pricing": {"monthly": 10, "annual_monthly": 8},
    },
    "premier": {
        "available": [
            "All models including v5 Pro + Studio",
            "10,000 credits/month (~2,000 songs)",
            "Commercial use (new songs)",
            "Personas (consistent voice reuse)",
            "Weirdness slider (0-100)",
            "Style Influence slider (0-100)",
            "Audio Influence slider (0-100, with audio upload)",
            "Add Vocals / Add Instrumental",
            "Up to 12 stems",
            "8 min audio upload",
            "Advanced editing",
            "Studio features (stems, warp markers)",
            "Studio 1.2 (Warp Markers, Remove FX, Alternates, Time Signature)",
            "MIDI export",
            "Priority queue (10 concurrent)",
            "Add-on credits",
            "Song length determined by model — v4.5/v5 support up to ~8 min",
            "320kbps MP3 + WAV download",
        ],
        "unavailable": [],
        "models": ["v4.5-all", "v4 Pro", "v4.5 Pro", "v4.5+ Pro", "v5 Pro"],
        "legacy_models": ["v4 Pro"],
        "sliders_available": True,
        "personas_available": True,
        "audio_influence_available": True,
        "studio_available": True,
        "song_length_max": "Determined by model — v4.5/v5 support up to ~8 min",
        "download_quality": "320kbps MP3 + WAV",
        "credit_cost": {"generation": 10, "extension": 5},
        "pricing": {"monthly": 30, "annual_monthly": 24},
    },
}


def get_tier_features(tier: str) -> dict:
    """Return feature availability for the given tier."""
    script_name = "tier-features"
    tier_lower = tier.lower().strip()

    if tier_lower not in TIER_FEATURES:
        return {
            "script": script_name,
            "version": "2.0.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "fail",
            "error": f"Unknown tier '{tier}'. Must be one of: free, pro, premier",
        }

    features = TIER_FEATURES[tier_lower]
    return {
        "script": script_name,
        "version": "2.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "pass",
        "tier": tier_lower,
        **features,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Return available/unavailable Suno features for a given subscription tier.",
        epilog="Exit codes: 0=success, 1=invalid tier"
    )
    parser.add_argument("tier", choices=["free", "pro", "premier"], help="Suno subscription tier")
    parser.add_argument("-o", "--output", help="Output file (defaults to stdout)")
    parser.add_argument("--verbose", action="store_true", help="Print diagnostics to stderr")
    args = parser.parse_args()

    if args.verbose:
        print(f"Getting features for tier: {args.tier}", file=sys.stderr)

    result = get_tier_features(args.tier)
    output = json.dumps(result, indent=2)

    if args.output:
        from pathlib import Path
        Path(args.output).write_text(output)
        if args.verbose:
            print(f"Results written to {args.output}", file=sys.stderr)
    else:
        print(output)

    sys.exit(0 if result["status"] == "pass" else 1)


if __name__ == "__main__":
    main()
