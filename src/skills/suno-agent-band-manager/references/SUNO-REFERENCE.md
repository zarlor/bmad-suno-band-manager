# Suno Platform Reference

Quick-reference for Suno models, plans, parameters, metatags, and common pitfalls. This is a companion to the [Usage Guide](./USAGE.md) (how to use Mac), the [Studio & Editor Reference](./STUDIO-EDITOR-REFERENCE.md) (post-generation editing tools), and covers *how Suno works* for generation.

---

## Model Comparison

| Model | Style | Character Limit | Best For | Tier |
|-------|-------|----------------|----------|------|
| **v4.5-all** | Conversational descriptions | 1,000 | Free users, heavier/faster genres, longer songs (~8 min) | Free |
| **v4 Pro** | Simple descriptors | 200 | Straightforward, shorter prompts | Paid |
| **v4.5 Pro** | Conversational descriptions | 1,000 | Intelligent prompts, narrative style | Paid |
| **v4.5+ Pro** | Conversational descriptions | 1,000 | Advanced creation methods | Paid |
| **v5 Pro** | Crisp film-brief (5-8 descriptors) | 1,000 | Authentic vocals, superior audio quality, section editing | Paid |
| **v5.5 Pro** | Crisp film-brief (5-8 descriptors) | 1,000 | Most expressive model, better subtle descriptor handling, Voices, Custom Models, My Taste | Paid |

**Character limit details:**
- **v4 Pro:** 200 chars (hard limit, silently truncated)
- **v4.5+ / v5 / v5.5:** 1,000 chars (API confirmed). Front-loaded terms dominate -- the first ~200 chars are the "critical zone" with strongest influence on generation. Content beyond ~200 chars is supplementary but not wasted; v5.5's improved descriptor interpretation may extend the effective window. 5-8 descriptors is the sweet spot.

**Key differences:**
- **v4.5-all** wants flowing, conversational sentences. Example: "Create a melodic, emotional deep house song with organic textures and hypnotic rhythms."
- **v5 Pro** wants crisp descriptors and emotional language over technical. Example: "raw indie folk, yearning vocals, acoustic guitar, lo-fi tape warmth, intimate"
- **v4 Pro** has a hard 200-character limit, not 1,000.

**v5-specific behaviors:**
- Full negative prompting support (v4.5 had limited support)
- Better BPM and key recognition in style prompt (e.g., `deep house, 122 BPM, A minor`)
- Production-quality descriptors more effective (e.g., "radio-ready mix, punchy drums, wide stereo field")
- Composition-aware architecture -- uses early style/genre info for coherent section transitions
- Existing v4 prompts often work "even better" on v5

**v5.5-specific behaviors (additive update over v5):**
- Same audio engine, metatags, and character limits as v5 -- all v5 prompts work identically, often with better results
- 48kHz sample rate, up to 8 min generation, internal codename "chirp-fenix" (v5 was "chirp-crow")
- Most expressive model yet -- better at interpreting subtle and nuanced descriptors
- More varied output per generation -- each Create produces 2 songs; 2-3 Creates (20-30 credits) gives 4-6 takes to pick from
- v5.5-optimized prompts can be more specific: "deep sub 808s, glitchy hi-hat rolls, pitched vocal chops" where v5 would use simpler "808s, hi-hats"
- **Voices** (replaces Personas): actual voice cloning with anti-deepfake verification, 15s-4min audio sample required. Pro/Premier only. **Skill Level dropdown** (Beginner/Intermediate/Advanced/Professional) actively reshapes how the model interprets your voice — always select **Professional** regardless of actual ability for the most stable, usable results.
- **Custom Models**: train on 6+ original tracks, 2-5 min training time, up to 3 custom models. Pro/Premier only. **Privacy/consent note (AudioNewsRoom):** consent grants Suno permission to use your data for training their global models — not optional, not a private silo.
  - **Training data:** WAV at 44.1kHz preferred (Suno auto-normalizes with RMS leveling, DC offset removal, spectral masking, onset detection, key/scale estimation). 8-12 stylistically consistent tracks is the inferred sweet spot. Dynamic range preservation matters more than loudness since the system normalizes internally.
  - **Overfitting risk:** Training data too narrow/homogeneous produces repetitive output. Include variety within your style lane — different tempos, moods, arrangements.
  - **Prompt strategy shift with Custom Models:** Priority order changes from genre-first to **mood/production-first** since genre is already encoded in the model. Simpler natural-language prompts may outperform tag-heavy prompts because the model handles the foundational style. Core formula: MOOD + PRODUCTION TEXTURE + ENERGY/TEMPO + INSTRUMENTS + VOCAL DIRECTION.
- **My Taste**: passive personalization that shapes generation defaults based on your listening/generation history. All tiers. Takes 20-30 generations to settle. **Magic wand icon** next to the style input triggers Style Augmentation — auto-generates a personalized style description based on your My Taste profile. Detailed manual prompts always override it. Can be viewed, edited, or disabled from avatar menu > "My Taste." No documented reset mechanism beyond disable/re-enable.
- **Workflow paradigm shift:** v5.5 encourages generate -> inspect -> replace sections -> refine (not regenerate from scratch)

**v5.5 Personalization Stack** (layers from broadest to most specific):
1. **My Taste** -- shapes generation defaults passively
2. **Custom Model** -- sets production DNA and sonic identity
3. **Voice** -- applies a specific vocal tone and character
4. **Prompt** -- steers the specific song (always the most important layer)

---

## Plan Comparison

| Feature | Free ($0) | Pro ($10/mo, $8/mo annual) | Premier ($30/mo, $24/mo annual) |
|---------|-----------|---------------------|--------------------------|
| **Model access** | v4.5-all only | All models incl. v5 | All models + Studio |
| **Credits** | 50/day (~10 songs) | 2,500/mo (~500 songs) | 10,000/mo (~2,000 songs) |
| **Credit cost** | 10 credits per Create (produces 2 songs) | Same | Same |
| **Commercial use** | No | Yes (new songs) | Yes (new songs) |
| **Weirdness slider** | No | Yes (0-100) | Yes (0-100) |
| **Style Influence slider** | No | Yes (0-100) | Yes (0-100) |
| **Audio Influence slider** | No | Yes (0-100, with Persona or audio upload) | Yes (0-100, with Persona or audio upload) |
| **Exclude Styles field** | No | Yes (Early Access Beta) | Yes (Early Access Beta) |
| **Inspo** | No | Yes (v4.5+ Pro) | Yes |
| **Legacy Editor** | No | Yes (section replace, rearrange, crop, fade) | Yes |
| **Personas** | No | Yes (v4.5/v5) | Yes (v4.5/v5) |
| **Voices** | No | Yes (v5.5, succeeds Personas — both coexist in Voices tab) | Yes (v5.5, succeeds Personas — both coexist in Voices tab) |
| **Custom Models** | No | Yes (up to 3) | Yes (up to 3) |
| **My Taste** | Yes (passive) | Yes (passive) | Yes (passive) |
| **Stems** | No | Up to 12 | Up to 12 |
| **Audio upload** | 1 min | 8 min | 8 min |
| **Add Vocals/Instrumental** | No | Yes | Yes |
| **Studio** | No | No | Yes |
| **Queue** | Shared | Priority, 10 at once | Priority, 10 at once |
| **Add-on credits** | No | Yes | Yes |

**Credit model:** Every press of the Create button costs **10 credits** and produces **2 songs** (a pair to choose from — Suno always generates two takes for variety). This means: 50 credits/day = 5 Creates = 10 songs to evaluate. 2,500 credits/mo = 250 Creates = 500 songs. When budgeting credits for a session, count in **Creates (10 credits each)**, not individual songs. Replace Section and Extend also cost credits (amount varies by section length). **When daily credits run low:** Suno provides 50 bonus credits per day on all tiers, refreshing daily.

Free-tier "More Options" includes: Vocal Gender, Manual/Auto Lyrics mode, Song Title only.

Pro/Premier "More Options" additionally includes: Weirdness slider, Style Influence slider, Audio Influence slider (with Persona or audio upload), Exclude Styles, Personas, Inspo, and the Legacy Editor for section-level editing.

**Vocal consistency across songs:** Suno interprets the same style prompt differently on every generation. Descriptive prompt language (e.g., "breathy female vocal with indie folk phrasing") gets you in the right neighborhood but not an exact match. The **Persona** feature (Pro/Premier) is the only reliable way to lock in a consistent vocal identity across songs -- it reuses the vocal character from a source generation. If you are working on an album or project where songs need to sound like the same singer, Personas are essential.

**Voices (v5.5, replaces Personas):** In v5.5, the **Voices** feature succeeds Personas for vocal consistency. Key differences: Voices is actual voice cloning (from a 15s-4min audio sample with anti-deepfake verification), while Personas was style essence capture from a source generation. **Style Personas are NOT gone** — they are integrated into the Voices tab in v5.5; the button changed but both features coexist. Personas still work on v4.5/v5/v5.5. Pro/Premier only.

**Voices Skill Level dropdown:** When setting up a Voice, you select Beginner, Intermediate, Advanced, or Professional. This is **NOT cosmetic** — it actively reshapes how the model interprets your voice. Testing found Professional produced the most stable, consistent, most usable results across every test. **Always set to Professional** regardless of actual singing ability.

**Voices limitations:** Voices is directional influence, not true vocal reproduction — the output drifts across generations and lacks true identity consistency (JG BeatsLab testing). Realistic for demo vocals, pre-production emotional direction, and hearing yourself in new compositions. **Not suitable for** final release vocal identity branding, or spoken word/narration (Voices drifts toward singing patterns, inconsistent tone between sections, unnatural pacing in longer spoken passages — Suno remains music-first).

**Audio Influence with Voices:** Unlike Personas (15-25% effective range), Voices uses a wider range — but independent testing (JG BeatsLab, March 2026) found the practical ceiling is lower than initially documented. At 85% Audio Influence, voice resemblance only reached ~70% with increasing artifacts. The instinct to maximize is counterproductive.

| Goal | Range | Notes |
|------|-------|-------|
| Voice as subtle flavor | 30-40% | Gentle influence, maximum generation polish |
| Balanced voice + quality | 40-60% | **Recommended starting point** — recognizable voice with manageable artifacts |
| Identity-focused | 60-70% | Noticeable quality trade-off begins here |
| Maximum fidelity (use with caution) | 70-80% | Diminishing returns; artifacts increase faster than resemblance |

Start at 50% and iterate in 5-10% increments. Pushing above 70% produces worse professional quality, not better.

---

## Package Field Mapping

Where each component of Mac's output package goes in Suno's Custom Mode:

| Component | What It Is | Where It Goes in Suno |
|-----------|-----------|----------------------|
| **Persona** (Pro/Premier) | Vocal identity from a source song | Persona selector (if applicable) |
| **Inspo** (v4.5+ Pro) | Playlist analysis for vibe channeling | Inspo feature (if applicable) |
| **Lyrics** | Structured text with metatags | Lyrics field (Custom Mode) |
| **Style Prompt** | Sound description optimized for your model | Style of Music field |
| **Exclude Styles** (Pro/Premier) | Comma-separated list of what to avoid | Exclude Styles field |
| **Vocal Gender** | Male/Female voice selection | Under More Options |
| **Lyrics Mode** | Manual (your lyrics) or Auto (Suno generates) | Lyrics toggle |
| **Weirdness** (Pro/Premier) | Creative deviation: lower = safer, higher = experimental | Under More Options |
| **Style Influence** (Pro/Premier) | Prompt adherence: lower = looser, higher = tighter | Under More Options |
| **Audio Influence** (Pro/Premier) | Persona/upload resemblance (appears with Persona or audio upload) | Under More Options |
| **Song Title** | Title for the generation | Title field |
| **Wild Card Variant** | An experimental alternative style prompt | Optional -- try it if you want |

---

## Style Prompt Best Practices

- **1,000-character limit** (200 for v4 Pro) -- content beyond this is silently truncated. The first ~200 chars are the "critical zone" where front-loaded terms have strongest influence. Content beyond ~200 is supplementary, not wasted — v5.5 may interpret more effectively. **5-8 descriptors is the sweet spot** (HookGenius 1000+ prompt analysis, April 2026 — fewer than 4 produces generic results; exceeding 10 causes conflicting signals and quality degradation).
- **Word order is weighted** -- front-loaded terms dominate. Priority order: Genre > Mood/Energy > Instruments > Vocals > Production. Treat the first ~200 characters as the "critical zone."
- **Hyper-specific beats generic** -- "1980s synth-pop" not "pop"; "distorted electric guitar, power chords" not "guitar"
- **BPM and key in style prompt (v5)** -- may work better in v5 than in lyric tags: `deep house, 122 BPM, A minor, hypnotic groove`. Still ineffective in v4/v4.5.
- **Production descriptors (v5)** -- "radio-ready mix, punchy drums, wide stereo field, crisp high-end, warm bass" are effective in v5
- **Never put artist names in the style prompt** -- Suno does not reliably replicate named artists. Decompose into concrete sonic descriptors instead.
- **Never put sound cues, asterisks, or style descriptions inside lyrics** -- the style prompt and lyrics are separate inputs
- **Negative/exclusion prompts go in the Exclude Styles field**, not in the main style prompt. In-prompt negatives ("no [element]" at the end) also work as a fallback.
- **Style prompt sets ONE overall mood** -- Suno does NOT actually shift tempo within a song. "Tempo change" / "tempo shift" prompts produce arrangement-density variation (instrumentation pullback for halftime feel, compression for double-time feel), not actual BPM change. Underlying tempo stays constant; felt-shift is dynamic/arrangement-driven. Use lyric density and rhythm noun metatags (`[Heavy: halftime]`, `[Double Time]`) for perceived section-level tempo changes.
- **Negative prompts are unreliable** -- "no screaming" in the style prompt often gets ignored. Use the Exclude Styles field (Pro/Premier) or translate to positive instructions ("clean singing with grit on peaks").
- **Genre keyword ordering matters** -- front-loaded terms dominate. Whatever appears first sets the primary sound. When a genre should be secondary/flavoring, use "accents" or "undertones": e.g., `atmospheric swamp metal accents`.
- **Genre words trigger specific behaviors** -- "metal" alone triggers screaming, "sludge" triggers harsh vocals, "doom" risks harsh vocals. Always pair heavy genre terms with explicit positive vocal instructions ("clean singing with grit", "raw melodic singing"). Use alternatives ("progressive heavy groove") when screaming is not desired.
- **Style prompt controls the full dynamic arc** -- `slow massive build to crushing climax` makes Suno build ALL the way through, ignoring quiet tags at the end. If the song needs to come down, the style prompt MUST acknowledge the descent: `slow build then fade`, `dynamic shifts loud to quiet`.
- **Rhythm nouns beat tempo adjectives** -- "halftime groove", "double-time driving", "shuffle", "breakbeat" lock feel better than "slow" or "fast". These describe specific drum patterns Suno can interpret.
- **Never use BPM values in style prompts or lyrics** -- BPM tags have ZERO detectable effect on Suno's output (confirmed by librosa analysis: a song tagged 60 BPM was delivered at 95.7 BPM; a song tagged 65-150 BPM across sections was delivered at a steady 123 BPM). Suno picks its own tempo. Use rhythm nouns and lyric density instead.
- **Perceived tempo is controlled through lyrical density, not BPM** -- Suno delivers a single steady BPM per song. Short fragmented lines (1-3 words) = slower perceived delivery. Long packed lines with many syllables = faster perceived delivery. Half-time/double-time drum feel (`[Heavy: halftime]`, `[Double Time]`) and arrangement density changes provide additional perceived tempo control.
- **Instrument ordering matters** -- instruments in the first ~200 chars appear globally; instruments at the end of the prompt are more section-specific when reinforced with `[Instrument: ...]` metatags in lyrics.
- **Bass-forward rock/metal is a known limitation** -- Suno cannot reliably produce bass-led sound in rock/metal context. Even "bass and drums only, no guitar" with guitar in excludes still produces guitar. "Funk metal" triggers slap/pop bass (Flea), not overdriven fingerstyle (Geddy Lee).
- **Personas anchor to their source era** -- a persona sourced from a modern song will pull "late 1970s" prompts toward a modern sound. Reduce Audio Influence to 10-15% or generate without a persona for era-specific pieces.
- **"Baroque" triggers Disney** -- do NOT use the word "baroque" in style prompts. Suno maps it to light, Disney-esque orchestration. Describe the qualities instead: `intricate interlocking guitar and bass melodies`, `dark minor key, precise and ornate`. Specify heavy orchestral instruments by name (`cello, heavy strings, kettle drums`) -- the word `orchestral` alone defaults to light/cinematic.
- **"Rock Opera" and "Cinematic" are keyboard triggers** -- both terms pull keyboard/synth arrangements into the mix. Use `power ballad`, `dynamic shifts` instead when you want drama without keyboards. **Exception:** "cinematic" is also a **universal quality modifier** — HookGenius's 1000+ prompt analysis found it consistently elevates production quality results across every tested genre. If keyboards aren't a concern, it's the single most versatile tag for enhancing output.
- **Production tags are the most underused category** — HookGenius analysis found that adding even one production descriptor ("radio-ready mix", "punchy drums", "wide stereo") meaningfully improves output distinctiveness. Most users rely only on genre + mood.
- **Conflicting tags produce bland compromise, not interesting hybrids** — "aggressive, peaceful" or similar contradictions cause Suno to default to a generic middle ground. Opposing descriptors cancel out rather than creating creative tension.
- **Three-phase dynamic arc needs double-stating** -- songs that go quiet → massive → quiet need the arc stated TWICE in the style prompt: once as a narrative description (`building from gentle to crushing then returning to gentle`) and once as a shorthand (`dynamic arc quiet to massive to quiet`). A single mention is not enough — Suno tends to flatten or ignore the return to quiet without the reinforcement.
- **Suno adds unscripted guitar solos regularly** -- three of four analyzed tracks had solos not in the lyrics. Plan for this or use [End] tags to prevent post-vocal noodling.
- **Anchor note restating during Extend** — always restate genre, mood, key, and instrument palette in a 1-2 sentence anchor note with each extension. Example: 'Keep the exact current groove, instrument palette, key, and tempo. Do not introduce new drums or leads.'
- **Forbidden element phrasing** — stating what NOT to add during Extend is more effective than positive instruction alone: 'No new hooks,' 'No new drums,' 'No new riffs,' 'no risers'
- **Limit extension chains to 2-3 maximum** — beyond that, audio quality degrades ('muddy' or 'lo-fi' artifacts). If quality degrades, use the **Cover feature** to re-synthesize the audio from scratch, effectively 'cleaning' the signal path.
- **Personas historically cannot be used reliably with Extend** — using Extend to keep generating with the same Persona has been unstable. Reuse exact vocal descriptor tags from the original prompt alongside the Persona to reinforce consistency.
- **Section-by-section instructions in style prompts are largely ignored** -- Suno delivered consistently fast, dense tracks despite detailed per-section directions (slow intro, tempo drops, sparse bridge). Style prompt sets overall mood; metatags handle sections (imperfectly).

### Exclude Styles (Pro/Premier)

The Exclude Styles field is a dedicated exclusion input separate from the style prompt. It functions as **probability reduction** -- guidance, not a hard ban.

- Format as a **comma-separated list** for easy copy-paste: `screaming vocals, steel guitar, autotune`
- Be specific: "screaming vocals" is better than "screaming"
- **Limit to 2-3 most important exclusions** -- too many destabilizes the arrangement
- In-prompt negatives also work: add "no [element]" at the end of your style prompt as a supplement
- With Exclude Styles handling exclusions, the style prompt can focus entirely on POSITIVE instructions
- Heavier genre words ("metal", "sludge") become usable in the style prompt when the Exclude Styles field blocks their unwanted defaults
- **Note:** Exclude Styles is currently in Early Access Beta and may not be 100% reliable for all instrument exclusions

**Free tier:** No Exclude Styles field. Translate exclusion intentions into positive style prompt language -- "clean singing with grit on peaks" instead of "no screaming."

---

## Metatag Reference

> This is Mac's quick reference. For comprehensive metatag documentation, consult the Lyric Transformer's detailed references — invoke `suno-lyric-transformer` or read its reference files directly:
> - **Full metatag catalog:** `suno-lyric-transformer/references/metatag-reference.md` — all known tags with confidence levels, production findings, and detailed usage notes
> - **Section job framework:** `suno-lyric-transformer/references/section-jobs.md` — what each section does emotionally, poem-to-song mapping guide, structural metaphor techniques

### Section Tags

**Only use recognized tags.** Custom tags like `[The Questions]` or `[Reflection]` are ignored or **sung as lyrics**. Map non-standard sections to recognized tags and use parameterized syntax to shape the feel.

| Tag | Job |
|-----|-----|
| `[Intro]` | Opening (unreliable -- may need regeneration) |
| `[Verse]` | Setup -- establishes story, scene, or emotion |
| `[Pre-Chorus]` | Lift -- builds tension/anticipation before chorus (2-4 lines). Creates a distinct musical moment with added percussion and vocal intensity |
| `[Chorus]` | Payoff -- the hook, the memorable part |
| `[Post-Chorus]` | Extension or cooldown after chorus. Best in pop/EDM; may blend with chorus in rock/metal |
| `[Bridge]` | Something NEW -- new chords, new melody, new perspective. Introduces harmonic content the song hasn't heard yet |
| `[Breakdown]` | Something LESS -- strips instruments, spotlights vocals or a motif. In metal, forces tempo drop and heavy rhythm. Creates maximum contrast before a high-energy section |
| `[Build-Up]` / `[Build]` | Escalation -- increases energy toward a peak |
| `[Final Chorus]` | Closing payoff -- often bigger than earlier choruses |
| `[Outro]` | Resolution -- brings the song to a close |
| `[Instrumental]` | Instrumental section -- no vocals |
| `[Interlude]` | Transitional palette cleanser -- defaults instrumental, lighter treatment if lyrics provided |
| `[Solo]` / `[Guitar Solo]` | Instrumental solo section |
| `[Break]` | Brief pause or stripped-back moment. Useful as energy-bleed buffer between aggressive and clean sections |
| `[Drop]` | Sudden energy release (EDM/electronic) |
| `[Hook]` | Short catchy phrase or motif |
| `[Fade Out]` | Gradual volume decrease |
| `[End]` | Signal to stop the song |

**Bridge vs Breakdown:** Bridge gives you something NEW (new chords, perspective). Breakdown gives you LESS (strips arrangement). Need both? Use `[Bridge | Half-Time]` + `[Energy: stripped, minimal]`.

### Dual Voices — Known Limitation

Suno v5/v5.5 cannot reliably produce two genuinely distinct male voices trading lines in a single generation. `[Duet]`, voice numbering tags (`[Voice 1]`/`[Voice 2]`), and descriptive "dual male vocals trading" in the style prompt all fail to produce true voice separation — you get doubling, harmonizing, or one voice averaged from the descriptors. Personas actively lock single-voice consistency (that's their design purpose).

**Workarounds for songs that need distinct dual voices:**
1. **Persona OFF is mandatory** — rebuild the band sound from scratch in the style prompt
2. **Multi-stage Studio Replace Section** — generate with main voice only, Replace Section each intrusive part with different vocal character prompts (most reliable)
3. **Nu-metal/rapcore framing** — Mr. Bungle / System of a Down / Mike Patton territory tolerates rapid vocal-character shifts. Best aesthetic match for "manic/unhinged" intrusive characters
4. **Metalcore clean/harsh** — `[Clean Vocal]` / `[Harsh Vocal]` contrast works but produces scream not manic speech
5. **Lead + Adlibs** — main voice dominant, intrusive voice as 3-6 word interjections max with `[adlibs: ...]` tags

**Gender contrast is the easiest path** — `[Male]`/`[Female]` per-line is the only reliably working duet technique. Same-gender dual voicing is the hardest case. For songs that genuinely need male/male dual distinct voices, plan for multi-stage Studio workflow from the start.

See `suno-lyric-transformer/references/metatag-reference.md` "Dual Vocals" section for full workarounds and ranked reliability.

### Parameterized Section Tags

Section tags can include per-section arrangement instructions using colon or pipe syntax:

- `[Verse: whispered vocals, acoustic guitar only]`
- `[Chorus: full band, powerful vocals]`
- `[Bridge: stripped back, piano only]`
- `[Chorus | Half-Time]`

This allows section-specific arrangement control directly in the tag itself, rather than relying solely on separate descriptor tags.

### Descriptor Tags

`[Mood: ...]`, `[Energy: ...]`, `[Vocal Style: ...]`, `[Instrument: ...]`

### Key Rules

- Keep metatag text short: 1-3 words
- Tags at the **top** of lyrics are global; tags **right before** a section are local (and more effective)
- Blank lines between sections improve parsing
- Consistent line lengths and syllable counts improve vocal phrasing stability
- Short repeated hooks sing better than long novel choruses
- Commas create breath pauses; dashes create sharp breaks; ellipses create trailing delivery
- Suno lyrics field has a hard limit of **5,000 characters** on v4.5+/v5/v5.5 (3,000 on v4). Silently truncated beyond the limit. **Quality budget: ~3,000 chars** — beyond this, Suno may rush through sections or cut content. Treat 3,000 as the practical working ceiling.

### Formatting as Suno Controls

- `!` (exclamation) = bark/attack trigger -- bleeds forward into subsequent sections. Avoid in clean/quiet sections.
- ALL CAPS = loudness ceiling -- save for the absolute peak moment only
- `(parentheses)` = backing vocals/texture, not lead melody
- Short lines (1-3 words) = slower delivery; long packed lines = faster delivery (PRIMARY tempo control — more reliable than any tag or slider). Line breaks act as breath points: more breaks = slower feel, fewer breaks = faster feel.
- Half-time / double-time drum feel via metatags (`[Heavy: halftime]`, `[Double Time]`) creates perceived tempo shifts without actual BPM change
- **BPM tags are confirmed ineffective** — do not use `[Verse: 65 BPM]` or similar tags. They have zero effect on output (librosa-confirmed).
- `[Instrument: ...]` before a section specifies instruments for that section -- use to crowd out unwanted instruments rather than trying to exclude them
- `[Soft End]`, `[Dramatic End]`, `[Instrumental End]` — ending style variants
- `[Slow Fade Out]`, `[Fast Fade Out]`, `[Instrumental Fade Out]`, `[Cinematic Fade Out]` — fade style variants (genre-specific: Slow for ambient/cinematic, Fast for dance/shortform, Instrumental for pop, Cinematic for orchestral)
- **Noodling-prevention combo**: `[Outro] long instrumental outro, soft keys, slow fade [End]` — stacking both 'winding down' and 'stop here' signals is more effective than either alone

---

## Troubleshooting Suno Issues

This table covers problems with Suno's output. For issues with Mac itself (wrong mode, missing profiles, skill errors), see the [Usage Guide Troubleshooting](./USAGE.md#9-troubleshooting).

### Prompt and Formatting Issues

| Issue | What Happens | Fix |
|-------|-------------|-----|
| **Silent truncation** | Style prompts over the character limit are cut off without warning | Keep within limits; front-load important content |
| **"Metal" in style prompt** | Triggers screaming/harsh vocals by default | Use "progressive heavy groove" if screaming not desired |
| **Negative prompts ignored** | "No screaming" in style prompt is unreliable | Use Exclude Styles field (Pro) or positive language |
| **Brass/instrument bleed** | Instruments in style prompt appear globally | Move section-specific instruments to end of prompt; use `[Instrument: ...]` metatags |
| **Exclamation points** | `!` triggers bark/attack vocal delivery | Remove from clean sections; bleeds into following sections |
| **ALL CAPS everywhere** | Sets loudness ceiling in early sections | Use sentence case; save caps for one peak moment |
| **Dense punctuation** | Heavy punctuation confuses vocal cadence | Simplify; use commas and dashes intentionally |
| **Scream bleed-through** | Aggressive vocals carry into subsequent sections | Add `[Vocal Style: whispered]` reset after aggressive sections |
| **Sections sound flat despite energy tags** | Energy metatags alone don't drive tempo changes | Combine with line density changes (short lines = slow, packed lines = fast), half-time/double-time drum metatags (`[Heavy: halftime]`, `[Double Time]`), arrangement density changes, and Weirdness slider. Do NOT use BPM tags — they are confirmed ineffective. |
| **Persona style conflicts** | Persona's auto-style clashes with your style prompt | Persona auto-fills Style of Music -- keep additions simple (1-2 genres, 1 mood, 2-4 instruments max). Change ONE variable at a time (music direction OR Persona, not both). |
| **Unwanted instrument in wrong section** | Suno's style prompt is global | Move section-specific instruments to end of prompt, use `[Instrument: ...]` metatags, or generate sections separately via Legacy Editor (Pro) |

### Audio Quality Issues

| Issue | What Happens | Fix |
|-------|-------------|-----|
| **Vocal artifacts** | Robotic or glitchy vocals | Try v5 Pro (better vocal nuance), or regenerate |
| **Audio artifacts or glitches** | Random audio issues | Regenerate 3-5 times with the same prompt. If persistent, simplify the style prompt. |
| **Pronunciation issues** | Words sung incorrectly | Add phonetic hints in lyrics or use the `[Spoken Word]` metatag |
| **Timing feels wrong** | Rhythm or pacing issues | Use Warp Markers (v5 Studio, Premier tier) |
| **Long song degradation** | Quality drops in extended generations | Generate shorter segments and use Extend carefully |
| **Voices spoken word/narration** | Voice drifts toward singing, inconsistent tone between sections, unnatural pacing | Suno remains music-first. Voices is not suitable for spoken word or narration — consider narration as a separate recording edited in via DAW |
| **Voices vocal artifacts at high Audio Influence** | Shimmer, warble, or robotic quality above 70% | Reduce Audio Influence to 40-60% range. Higher is not better — see Voices Audio Influence table |

### Creative Issues

| Issue | What Happens | Fix |
|-------|-------------|-----|
| **Single Create** | One Create (2 songs) rarely nails it | 2-3 Creates (4-6 songs, 20-30 credits) is the practical minimum for finding a keeper |
| **Same prompt, wildly different results** | Normal Suno behavior | This is expected — each Create produces 2 different takes from the same inputs. Budget accordingly. |
| **Cliche amplification** | Subtle lyrical cliches become obvious when sung | Run cliche detection before submitting lyrics |
| **`[Intro]` unreliability** | Suno's `[Intro]` tag often produces unexpected results | Regenerate just the first 10 seconds, or skip the tag |
| **"Not what I imagined"** | Output doesn't match your vision | Use the Refine Song flow (RS). Mac's feedback elicitation helps you articulate what needs to change. |

---

## Covers, Remixes, and Inspo

### Cover Feature
- Cover re-performs an existing song in a new style while preserving melody, lyrics, and structure
- Works with any Suno-generated song, uploaded audio, instrumentals or vocal tracks
- Step-by-step: three-dot menu → Create → Cover Song → describe the new style → generate
- **CRITICAL: Covers are NOT eligible for commercial use** — even on your own songs. For commercial releases, use the original lyrics and create a fresh generation instead.
- Stacking Covers (re-covering within the same genre) can smooth cohesion

### Remix Umbrella — Four Workflows
- **Cover** — re-sing in a different style/genre (preserves melody)
- **Extend** — add more to an existing song
- **Reuse** — reuse the prompt/settings from an existing song
- **Speed** — adjust playback speed

### v4.5+ Pro Additional Tools
- **Instrumental Flip** — rebuilds backing track while preserving vocal structure
- **Vocal Swap** — changes vocal persona while retaining melody and timing
- **Spark from Playlist** — uses a reference playlist to shape mood/tempo/instrumentation

### Cover vs Remix vs Inspo Decision Matrix

| Tool | Use When | What It Does |
|------|----------|-------------|
| Cover | "Play this same song in a different style" | Re-performs with new style, keeps melody/lyrics/structure |
| Remix (general) | "Tweak/transform this song" | Various transformations within same song identity |
| Inspo | "Make something NEW inspired by these" | Analyzes a playlist, generates entirely new material |

---

## Community Research Sources & Further Reading

> **Last updated:** April 6, 2026. These sources informed the v5.5-specific findings in this reference. Suno evolves fast — verify claims against current platform behavior.

### Official Suno Documentation
- [What's New in v5.5](https://help.suno.com/en/articles/11362305)
- [Voices: Use Your Voice in Suno](https://help.suno.com/en/articles/11362369)
- [Voices FAQ](https://help.suno.com/en/articles/11362433)
- [Custom Models in v5.5](https://help.suno.com/en/articles/11362497)
- [My Taste](https://help.suno.com/en/articles/11362561)
- [Creative Sliders](https://help.suno.com/en/articles/6141377)

### Independent Testing & Analysis
- [JG BeatsLab: Voices Day One Testing](https://www.jgbeatslab.com/ai-music-lab-blog/suno-v5-5-voices-tested) — Voices Audio Influence real-world ranges, Skill Level dropdown impact, vocal resemblance ceiling findings
- [HookGenius: Suno v5.5 Guide](https://hookgenius.app/learn/suno-v5-5-guide/) — Comprehensive v5.5 feature walkthrough
- [HookGenius: 1000+ Prompt Analysis](https://hookgenius.app/learn/suno-style-tag-research/) — Data-driven findings on tag count sweet spots, "cinematic" as universal modifier, production tag underuse, conflicting tag behavior
- [AudioNewsRoom: What You Give Up to Make It Yours](https://audionewsroom.net/2026/03/suno-v5-5-what-you-give-up-to-make-it-yours.html) — Privacy/consent analysis for Voices and Custom Models
- [JackRighteous: How Has v5.5 Gone For You](https://jackrighteous.com/en-us/blogs/guides-using-suno-ai-music-creation/how-has-suno-v5-5-update-gone-for-you) — Genre-specific slider ranges, section-specific strategy
- [JackRighteous: Creative Control Sliders in v5](https://jackrighteous.com/en-us/blogs/guides-using-suno-ai-music-creation/creative-control-sliders-suno-v5) — Detailed slider behavior analysis
- [JackRighteous: v5.5 Features Explained](https://jackrighteous.com/en-us/blogs/guides-using-suno-ai-music-creation/suno-v5-5-features-explained-workflow-changes-studio-editing-creator-guide) — Workflow paradigm shift documentation
- [JackRighteous: Spoken Narration Workflow](https://jackrighteous.com/en-us/blogs/guides-using-suno-ai-music-creation/suno-ai-spoken-narration-workflow) — Spoken word limitations with Voices
- [Suno v5 vs v5.5 Comparison](https://suno-v5.com/blog/suno-v5-5-vs-v5-what-actually-changed) — What actually changed between versions

### API Reference
- [CometAPI: v5.5 API Guide](https://www.cometapi.com/suno-v5-5-what-is-new-and-how-to-use-it-via-api--studio/) — API model parameter `mv: "chirp-fenix"` for v5.5
