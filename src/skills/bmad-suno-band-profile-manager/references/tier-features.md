# Suno Tier Feature Matrix

> **Last validated:** March 2026 (Suno Free, Pro, Premier plans). Suno updates pricing, features, and tier boundaries frequently — use web search to verify against current Suno pricing page when uncertain.

**Note:** The `./scripts/tier-features.py` script is the authoritative source for this data. This reference file is provided for human readability. When updating, update the script first.

## Plan Comparison

| Feature | Free ($0) | Pro ($10/mo, $8/mo annual) | Premier ($30/mo, $24/mo annual) |
|---------|-----------|----------------------------|----------------------------------|
| **Model Access** | v4.5-all only | All models incl. v5, v5.5 | All models incl. v5.5 + Studio |
| **Credits** | 50/day (~10 songs) | 2,500/mo (~500 songs) | 10,000/mo (~2,000 songs) |
| **Credit Cost** | 10/song, 5/extend | 10/song, 5/extend | 10/song, 5/extend |
| **Song Length** | Determined by model — v4.5-all supports up to ~8 min | Determined by model — v4.5/v5 support up to ~8 min | Determined by model — v4.5/v5 support up to ~8 min |
| **Download Quality** | 128kbps MP3 | 320kbps MP3 + WAV | 320kbps MP3 + WAV |
| **Commercial Use** | No | Yes (new songs) | Yes (new songs) |
| **Personas** | No | Yes (v4.5/v5 only; replaced by Voices in v5.5) | Yes (v4.5/v5 only; replaced by Voices in v5.5) |
| **Voices** | No | Yes (v5.5 voice cloning) | Yes (v5.5 voice cloning) |
| **Custom Models** | No | Yes (up to 3 models) | Yes (up to 3 models) |
| **My Taste** | Yes (passive) | Yes (passive) | Yes (passive) |
| **Weirdness Slider** | No | Yes (0-100) | Yes (0-100) |
| **Style Influence Slider** | No | Yes (0-100) | Yes (0-100) |
| **Audio Influence Slider** | No | Yes (0-100, with audio upload) | Yes (0-100, with audio upload) |
| | | *10-15% reduces persona era-anchoring* | *10-15% reduces persona era-anchoring* |
| **Add Vocals/Instrumental** | No | Yes (beta) | Yes (beta) |
| **Covers** | No | Yes (beta) | Yes (beta) |
| **Remaster** | No | Yes | Yes |
| **Stems** | No | Up to 12 | Up to 12 |
| **Audio Upload** | 1 min | 8 min | 8 min |
| **Legacy Editor** (Replace, Extend, Crop, Fade, Rearrange) | No | Yes | Yes |
| **Studio** (full Generative Audio Workstation) | No | No | Yes |
| **Warp Markers** | No | No | Yes (Studio) |
| **Remove FX** | No | No | Yes (Studio) |
| **Alternates / Take Lanes** | No | No | Yes (Studio) |
| **EQ** (6-band per track) | No | No | Yes (Studio) |
| **Time Signature** control | No | No | Yes (Studio, editing only — not sent to generative models) |
| **Context Window** | No | No | Yes (Studio) |
| **Recording** (microphone) | No | No | Yes (Studio) |
| **Loop Recording** | No | No | Yes (Studio) |
| **Sounds Mode** (text-to-sound) | No | No | Yes (Studio, beta) |
| **Stem Cover** | No | No | Yes (Studio) |
| **Heal Edits** | No | No | Yes (Studio) |
| **MIDI Export** (10 credits/stem) | No | No | Yes |
| **MILO-1080 Sequencer** | No | No | Yes (Studio) |
| **Queue Priority** | Shared | Priority, 10 at once | Priority, 10 at once |
| **Add-on Credits** | No | Yes | Yes |

## Free Tier Available Options

- Vocal Gender selection
- Manual/Auto Lyrics mode
- Song Title

## Models

| Model | Tagline | Availability |
|-------|---------|-------------|
| v5.5 | Voices, Custom Models, My Taste | Pro/Premier |
| v5 Pro | Authentic vocals, superior audio quality and control | Pro/Premier |
| v4.5+ Pro | Advanced creation methods | Pro/Premier |
| v4.5 Pro | Intelligent prompts | Pro/Premier |
| v4.5-all | Best free model | All tiers |
| v4 Pro | Improved sound quality (legacy) | Pro/Premier |

## Profile Implications by Tier

**Free tier profiles should:**
- Set `model_preference` to "v4.5-all" (only available model)
- Omit or zero out `sliders` (not available)
- Not reference Personas or Voices (not available)
- Focus style_baseline on conversational descriptions (v4.5-all strength)
- My Taste is active passively — no profile configuration needed

**Pro tier profiles can:**
- Use any model including v5 Pro and v5.5
- Set Weirdness and Style Influence sliders
- Reference Suno Personas for vocal consistency (v4.5/v5 models)
- Use Suno Voices for vocal consistency (v5.5 model — replaces Personas)
- Use Custom Models (up to 3, trained on 6+ original tracks, 2-5 min training time)
- Use crisp, descriptor-focused style for v5 Pro
- Use Audio Influence slider to manage persona era-anchoring (reduce to 10-15% when the persona's source era conflicts with the desired sound)
- When a Voice is configured, omit gender vocal descriptors from style_baseline — the Voice defines the vocal identity

**Premier tier profiles can:**
- Everything Pro can do, plus full Suno Studio (GAW)
- Set studio_preferences (BPM, key, time signature)
- Stems separation for production work
- MIDI export for DAW integration (10 credits per stem)
- Voices and Custom Models (same as Pro)
- EQ (6-band per track), Warp Markers, Remove FX, Alternates, Context Window
- Recording (microphone input), Loop Recording, Sounds Mode, Stem Cover, Heal Edits
- MILO-1080 Step Sequencer (16-track, text-to-sound, MIDI I/O)

## Production Notes

**Audio Influence as Era Control (Pro/Premier):** When a persona's era-anchoring conflicts with the desired era for a track, reducing Audio Influence from the default 25% to 10-15% helps pull the sound away from the persona's source era. This doesn't fully eliminate the anchoring — for strong era shifts, consider generating without a persona or creating an era-specific persona from an era-appropriate source song.

**Audio Influence Effective Range (Pro/Premier):** The practical range for Audio Influence is 15-25%. Values above 25% show diminishing returns — tested at 40%, it did not override an incompatible style prompt. The slider shapes the persona's contribution but cannot force the persona's character over a conflicting style direction.

**Acoustic/Ballad Tracks and Audio Influence (Pro/Premier):** When the style prompt clearly defines a non-heavy genre (ballad, acoustic, stripped-back), the persona contributes only vocal identity — it does not drag in unwanted instrumentation. Do NOT reduce Audio Influence for ballads or stripped tracks; keep it at the normal working range. The style prompt governs the arrangement; the persona governs the voice.

**Exclude Styles — Known Limitations:** The Exclude Styles field helps shape tone but does not reliably remove instruments entirely. For example, even with "guitar" in Exclude Styles, Suno still produces guitar in rock/metal contexts. Treat Exclude Styles as a nudge toward the desired balance rather than a hard instrument filter.

**Personas to Voices Transition (v5.5):** Personas are replaced by Voices in v5.5. Existing Personas still work on v4.5 and v5 models. For v5.5 generation, use a Voice instead. Voices are created from a 15-second to 4-minute audio sample and include anti-deepfake verification. Voices are private to the account that created them.

**Voices and Vocal Descriptors (v5.5, Pro/Premier):** When a Voice is active, the Voice defines the vocal identity — gender, tone, and character come from the audio sample. Omit gender vocal descriptors from the style prompt to avoid conflicts. Other vocal direction (delivery, energy, diction) can still shape performance.

**Audio Influence with Voices (v5.5, Pro/Premier):** Unlike Personas (15-25% effective range), Voices uses a wider range. The sweet spot is personal — 35-45% for subtle flavor, 55-70% balanced (default starting point), 75-85% for identity-focused work, 85-95% for maximum fidelity. Adjust up if voice is unrecognizable, down if quality suffers.

**Custom Models (v5.5, Pro/Premier):** Custom Models are trained on 6 or more original tracks and take 2-5 minutes to train. Up to 3 Custom Models per account. They capture a production style and sound signature. When a Custom Model is active, it shapes the overall production character — the style prompt should complement rather than fight the model's learned style.

**My Taste (v5.5, All Tiers):** My Taste is passive personalization derived from the user's generation history. It requires no configuration and works across all tiers including Free. It subtly shapes generation output based on patterns in what the user has created and liked.

**Legacy Editor vs. Studio (Pro vs Premier):** Pro users get the Legacy Editor — section-level editing with Replace Section, Extend, Crop, Fade, Rearrange, and Stems. Premier users additionally get Suno Studio — a full browser-based Generative Audio Workstation with multitrack timeline, EQ, Warp Markers, Alternates/Take Lanes, Remove FX, Recording, Loop Recording, Context Window, Stem Cover, Sounds Mode, Heal Edits, and MIDI Export. For complete editing workflows, see [STUDIO-EDITOR-REFERENCE.md](../../STUDIO-EDITOR-REFERENCE.md).

**Remaster (Pro/Premier):** Generates refined variations adjusting production details (instrument balance, effects, mix quality, vocal clarity) while preserving song structure. Three strength levels: Subtle, Normal, High. Does NOT change lyrics, style, or vocalist — use Cover for those. Good for final polish before export.

**Replace Section Best Practices (Pro/Premier):** Key controls: Keep Duration toggle (ON = match length, OFF = creative flexibility), Instrumental Mode toggle (removes vocals), Replace Lyrics (edit lyrics for just the selected region). Best results with 10-30 second selections; typically requires 2-5 attempts for seamless transitions.

**v5.5 Editing Paradigm:** v5.5 favors generate → inspect → section replace → refine (not regenerate from scratch). This preserves good material and spends fewer credits. For complete Studio and Editor workflows, see [STUDIO-EDITOR-REFERENCE.md](../../STUDIO-EDITOR-REFERENCE.md).
