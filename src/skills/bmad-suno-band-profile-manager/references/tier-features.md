# Suno Tier Feature Matrix

> **Last validated:** March 2026 (Suno Free, Pro, Premier plans). Suno updates pricing, features, and tier boundaries frequently — use web search to verify against current Suno pricing page when uncertain.

**Note:** The `./scripts/tier-features.py` script is the authoritative source for this data. This reference file is provided for human readability. When updating, update the script first.

## Plan Comparison

| Feature | Free ($0) | Pro ($10/mo, $8/mo annual) | Premier ($30/mo, $24/mo annual) |
|---------|-----------|----------------------------|----------------------------------|
| **Model Access** | v4.5-all only | All models incl. v5 | All models + Studio |
| **Credits** | 50/day (~10 songs) | 2,500/mo (~500 songs) | 10,000/mo (~2,000 songs) |
| **Credit Cost** | 10/song, 5/extend | 10/song, 5/extend | 10/song, 5/extend |
| **Song Length** | Determined by model — v4.5-all supports up to ~8 min | Determined by model — v4.5/v5 support up to ~8 min | Determined by model — v4.5/v5 support up to ~8 min |
| **Download Quality** | 128kbps MP3 | 320kbps MP3 + WAV | 320kbps MP3 + WAV |
| **Commercial Use** | No | Yes (new songs) | Yes (new songs) |
| **Personas** | No | Yes | Yes |
| **Weirdness Slider** | No | Yes (0-100) | Yes (0-100) |
| **Style Influence Slider** | No | Yes (0-100) | Yes (0-100) |
| **Audio Influence Slider** | No | Yes (0-100, with audio upload) | Yes (0-100, with audio upload) |
| | | *10-15% reduces persona era-anchoring* | *10-15% reduces persona era-anchoring* |
| **Add Vocals/Instrumental** | No | Yes | Yes |
| **Stems** | No | Up to 12 | Up to 12 |
| **Audio Upload** | 1 min | 8 min | 8 min |
| **Advanced Editing** | No | Yes | Yes |
| **Studio** | No | No | Yes |
| **Studio 1.2 Features** | No | No | Yes (Warp Markers, Remove FX, Alternates, Time Signature) |
| **MIDI Export** | No | No | Yes |
| **Queue Priority** | Shared | Priority, 10 at once | Priority, 10 at once |
| **Add-on Credits** | No | Yes | Yes |

## Free Tier Available Options

- Vocal Gender selection
- Manual/Auto Lyrics mode
- Song Title

## Models

| Model | Tagline | Availability |
|-------|---------|-------------|
| v5 Pro | Authentic vocals, superior audio quality and control | Pro/Premier |
| v4.5+ Pro | Advanced creation methods | Pro/Premier |
| v4.5 Pro | Intelligent prompts | Pro/Premier |
| v4.5-all | Best free model | All tiers |
| v4 Pro | Improved sound quality (legacy) | Pro/Premier |

## Profile Implications by Tier

**Free tier profiles should:**
- Set `model_preference` to "v4.5-all" (only available model)
- Omit or zero out `sliders` (not available)
- Not reference Personas (not available)
- Focus style_baseline on conversational descriptions (v4.5-all strength)

**Pro tier profiles can:**
- Use any model including v5 Pro
- Set Weirdness and Style Influence sliders
- Reference Suno Personas for vocal consistency
- Use crisp, descriptor-focused style for v5 Pro
- Use Audio Influence slider to manage persona era-anchoring (reduce to 10-15% when the persona's source era conflicts with the desired sound)

**Premier tier profiles can:**
- Everything Pro can do, plus Studio features
- Set studio_preferences (BPM, key, time signature)
- Stems separation for production work
- MIDI export for DAW integration

## Production Notes

**Audio Influence as Era Control (Pro/Premier):** When a persona's era-anchoring conflicts with the desired era for a track, reducing Audio Influence from the default 25% to 10-15% helps pull the sound away from the persona's source era. This doesn't fully eliminate the anchoring — for strong era shifts, consider generating without a persona or creating an era-specific persona from an era-appropriate source song.

**Audio Influence Effective Range (Pro/Premier):** The practical range for Audio Influence is 15-25%. Values above 25% show diminishing returns — tested at 40%, it did not override an incompatible style prompt. The slider shapes the persona's contribution but cannot force the persona's character over a conflicting style direction.

**Acoustic/Ballad Tracks and Audio Influence (Pro/Premier):** When the style prompt clearly defines a non-heavy genre (ballad, acoustic, stripped-back), the persona contributes only vocal identity — it does not drag in unwanted instrumentation. Do NOT reduce Audio Influence for ballads or stripped tracks; keep it at the normal working range. The style prompt governs the arrangement; the persona governs the voice.

**Exclude Styles — Known Limitations:** The Exclude Styles field helps shape tone but does not reliably remove instruments entirely. For example, even with "guitar" in Exclude Styles, Suno still produces guitar in rock/metal contexts. Treat Exclude Styles as a nudge toward the desired balance rather than a hard instrument filter.
