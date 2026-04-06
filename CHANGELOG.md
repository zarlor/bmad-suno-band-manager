# Changelog

All notable changes to the Suno Band Manager module are documented here.

---

## [1.4.1] - 2026-04-06

### Suno v5.5 Community Research Update

Comprehensive reference documentation update integrating independent community testing results from JG BeatsLab, HookGenius (1000+ prompt analysis), AudioNewsRoom, JackRighteous, BlakeCrosley, GenxNotes, and others. All findings sourced and linked for independent verification.

### Corrections

- **v5.5 model codename** — Fixed from "chirp-crow" (that's v5) to the correct "chirp-fenix"
- **Voices Audio Influence ranges** — Corrected based on JG BeatsLab testing. Real sweet spot is 40-60%, not 55-70%. Quality degrades above 70%; at 85% resemblance only reaches ~70% with increasing artifacts. Updated across SUNO-REFERENCE, model-prompt-strategies, and suno-parameter-map.
- **Style Personas are NOT gone** — Clarified that Personas coexist with Voices in the v5.5 Voices tab. The button changed but both features remain available.
- **Descriptor count sweet spot** — Updated from "4-7" to "5-8" based on HookGenius 1000+ prompt analysis across all reference files and quick-reference tables.

### New Findings — v5.5 Features

- **Voices Skill Level dropdown** — Beginner/Intermediate/Advanced/Professional setting is NOT cosmetic; actively reshapes model interpretation. Always use Professional for most stable results.
- **Voices limitations** — Directional influence, not true reproduction. Not suitable for spoken word/narration (drifts toward singing). Realistic for demos and pre-production.
- **My Taste magic wand / Style Augmentation** — Documented the wand icon in Create form that auto-generates personalized style prompts. Manual prompts always override. Can be viewed/edited/disabled from avatar menu.
- **Custom Model training best practices** — WAV at 44.1kHz preferred, 8-12 consistent tracks sweet spot, auto-normalization pipeline (RMS leveling, DC offset removal, spectral masking, onset detection, key/scale estimation), overfitting mitigation guidance.
- **Custom Model prompt strategy shift** — With Custom Models, priority changes from genre-first to mood/production-first. Formula: MOOD + PRODUCTION TEXTURE + ENERGY/TEMPO + INSTRUMENTS + VOCAL DIRECTION.
- **Custom Model consent/privacy** — Grants Suno permission to use data for global model training (not optional, not private).

### New Findings — Style Prompt Strategies

- **"Cinematic" as universal modifier** — Consistently elevates production quality across every tested genre.
- **Production tags most underused** — Adding even one meaningfully improves distinctiveness.
- **Conflicting tags produce bland compromise** — Opposing descriptors cancel out, not creative tension.
- **Callback phrasing during Replace/Extend** — "Continue same chorus energy" anchors consistency.
- **Style Influence above ~80 plateaus** — Rarely improves accuracy, can reduce vocal phrasing variation.

### New Findings — Extend Drift Solutions

- **Weirdness strongest during Extend/Bridge** — Primary cause of style drift. Keep conservative during Extend.
- **Anchor note restating** — Restate genre, mood, key, instrument palette with each extension.
- **Forbidden element phrasing** — "No new hooks/drums/riffs" more effective than positive instruction alone.
- **2-3 extension chain limit** — Quality degrades beyond that. Cover feature re-synthesizes to clean signal path.
- **Persona instability with Extend** — Personas historically unreliable during Extend operations.
- **Extend Anti-Drift Toolkit** — 7-technique ranked guide added to suno-parameter-map.
- **Genre-specific outro templates** — Gospel, Rock, Lo-fi, EDM, Reggae ending patterns.

### New Findings — Metatags

- **Asterisk sound effect syntax** — `*rainfall*`, `*vinyl crackle*` etc. confirmed working as inline sound effects. Exception to "no asterisks" rule.
- **New Effect tags** — `[Effect: Bitcrusher]`, `[Effect: Autopan]`, `[Effect: Sidechain]`
- **`[Callback: ...]` upgraded** — HIGH reliability for Extend/Replace workflows (community-validated). Experimental for standard generation.
- **Ending tag variants** — `[Soft End]`, `[Dramatic End]`, `[Instrumental End]`, `[Slow Fade Out]`, `[Fast Fade Out]`, `[Instrumental Fade Out]`, `[Cinematic Fade Out]`
- **Noodling-prevention combo** — `[Outro] descriptive text [End]` stacking more effective than either alone.
- **Accelerando/Ritardando grid-loss warning** — Can lose rhythmic grid for remainder of track. BPM tag as recalibration anchor after disruption.
- **Three-layer vocal specification** — Character + Delivery + Effects for maximum vocal control.
- **Vocal delivery reliability tiers** — HIGH/MEDIUM/LOW classification from HookGenius 300+ tag testing.
- **Non-functional tags documented** — `[Bilingual]`, `[Spanglish]`, `[Live Version]`, `[Mono]`, `[Wide Stereo]`, `[Clean Lyrics]`/`[Explicit]` confirmed ineffective.
- **Falsetto confirmed LOW reliability** — Style prompt phrasing more effective than metatag.

### New Findings — Studio & Editing

- **Replace Section sweet spot 15-20 seconds** — Under 5 = disjointed, over 30 = model loses thread.
- **Heal Edits technique** — Apply on the following section after Replace to blend timbre shifts.
- **Remaster is full regeneration** — Not a filter. Instrumentals benefit more than vocals. "Improved fidelity with reduced soul." One pass usually sufficient.
- **Remove FX boosts loudness up to 5 LUFS** — Check levels after applying.
- **EQ for AI shimmer** — Roll off ultra-highs on stems with generation artifacts.
- **Genre-specific Warp Marker quantize** — EDM tight, Trap medium, Afrobeat light-medium, Soul/R&B light.
- **Credit waste prevention framework** — 0-50 learning, 50-80 discipline, 80+ stop and export.
- **Known bugs** — "Scratched CD" loop effect, Lyric Cache bug on Replace Section.
- **Aggressive mastering limiter** — Export raw stems for professional release.

### Documentation

- Added community research sources with URLs to SUNO-REFERENCE, model-prompt-strategies, metatag-reference, STUDIO-EDITOR-REFERENCE, and suno-parameter-map
- Updated validation dates across all reference files to April 6, 2026
- Created CHANGELOG.md

### Files Changed

- `suno-agent-band-manager/references/SUNO-REFERENCE.md`
- `suno-agent-band-manager/references/STUDIO-EDITOR-REFERENCE.md`
- `suno-style-prompt-builder/references/model-prompt-strategies.md`
- `suno-feedback-elicitor/references/suno-parameter-map.md`
- `suno-lyric-transformer/references/metatag-reference.md`
- `package.json`

---

## [1.4.0] - 2026-04-02

Update to BMB v1.5.0 standards, rename module from bmad-suno-* to suno-*.

---

## [1.1.3] and earlier

See git history for prior releases.
