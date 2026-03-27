# Suno Metatag Reference

Metatags are keywords in square brackets `[ ]` placed in the lyrics field to guide Suno's generation. This reference covers all known working tags as of March 2026. Suno evolves frequently — when uncertain about a tag's effectiveness, use web search to verify against current documentation.

**Confidence Levels:** Tags are marked HIGH (multiple sources confirm), MEDIUM/Experimental (1-2 sources, may not work consistently), or unmarked (established/proven). HIGH-confidence new additions from March 2026 research are integrated into existing sections. MEDIUM-confidence tags are marked with "(Experimental)" throughout.

## Section Structure Tags

Core tags that define song structure. Suno uses these to organize musical sections.

| Tag | Usage | Notes |
|-----|-------|-------|
| `[Intro]` | Instrumental or minimal vocal opening | Notoriously unreliable — keep short or omit |
| `[Verse]` / `[Verse 1]` / `[Verse 2]` | Narrative/story sections | Number if multiple |
| `[Pre-Chorus]` | Transitional build before chorus | Short — 2-4 lines, creates lift |
| `[Chorus]` | Main hook/payoff section | Short repeated hooks > long novel choruses |
| `[Post-Chorus]` | Section immediately after chorus | Extends the chorus energy or provides a cooldown |
| `[Bridge]` | Contrasting section | Usually appears once, offers new perspective |
| `[Outro]` | Closing section | Fade, resolution, or final statement |
| `[End]` | Hard stop | Use to signal a definitive ending |
| `[Final Chorus]` | Last chorus iteration | Often bigger/louder than standard chorus |
| `[Hook]` | Short catchy phrase | Distinct from chorus — can be a repeated motif |
| `[Refrain]` | Repeated line or phrase | Simpler than a full chorus |
| `[Instrumental Intro]` | Instrumental-only opening | More reliable than bare `[Intro]` for ensuring no vocals (HIGH) |
| `[Instrumental Break]` | Explicit instrumental mid-song break | Clearer intent than `[Break]` alone (HIGH) |
| `[Drum Break]` | Percussion-only break section | Strips everything except drums (HIGH) |
| `[Percussion Break]` | Percussion-focused break | Similar to Drum Break but may include auxiliary percussion (HIGH) |
| `[Build]` | Rising energy section | Shorthand for `[Build-Up]`; confirmed on v5 (HIGH) |
| `[Big Finish]` | Grand climactic ending section | Signals a big, climactic ending (HIGH) |
| `[Chorus x2]` | Repeat chorus twice | Chorus doubling without rewriting lyrics (HIGH) |

## Instrumental & Solo Section Tags

Tags that create instrumental moments with no lyrics. These add duration to the song beyond what lyric lines alone suggest.

| Tag | Usage | Typical Duration |
|-----|-------|-----------------|
| `[Instrumental]` | General instrumental section | 10-25 sec |
| `[Interlude]` | Musical bridge between sections | 8-20 sec |
| `[Solo]` | Generic instrumental solo | 10-25 sec |
| `[Guitar Solo]` | Guitar-focused solo section | 10-25 sec |
| `[Piano Solo]` | Piano-focused solo section | 10-25 sec |
| `[Sax Solo]` / `[Saxophone Solo]` | Saxophone solo | 10-25 sec |
| `[Drum Solo]` | Drum-focused solo section | 8-20 sec |
| `[Bass Solo]` | Bass-focused solo section | 8-20 sec |
| `[Break]` | Brief pause or stripped-back moment | 5-15 sec |
| `[Breakdown]` | Stripped-back section, reduces energy | 8-20 sec |
| `[Build-Up]` / `[Buildup]` | Rising energy, leads into a climax | 5-15 sec |
| `[Drop]` | Sudden energy release (EDM/electronic) | 10-20 sec |
| `[Synth Solo]` | Synthesizer solo section (HIGH) | 10-25 sec |
| `[Violin Solo]` | Violin solo section (HIGH) | 10-25 sec |
| `[Bass Drop]` | Sudden heavy bass entry, EDM style (HIGH) | 5-15 sec |
| `[Strings Rise]` | Strings gradually build/swell (HIGH) | 8-20 sec |

## Vocal Delivery Tags

Control how Suno's vocal engine performs specific sections. Place right before the section tag or between the section tag and the first lyric line. Use one primary delivery cue per section — stacking reduces effectiveness.

### Volume & Intensity
| Tag | Effect |
|-----|--------|
| `[Whispered]` / `[Whisper]` | Soft, breathy, intimate delivery |
| `[Soft]` / `[Gentle]` / `[Quiet]` | Subdued, low-volume singing |
| `[Spoken]` / `[Spoken Word]` | Spoken rather than sung |
| `[Powerful]` / `[Intense]` | Full-force, emotional delivery |
| `[Belted]` / `[Belting]` | Powerful, full-voice, high-energy singing |
| `[Shouted]` / `[Screamed]` | Aggressive, loud delivery |
| `[Growled]` / `[Growl]` | Low, guttural vocal delivery |
| `[Gritty]` | Gritty, rough vocal tone (HIGH) |
| `[Monotone]` | Flat, monotone delivery (HIGH) |
| `[Breathless]` | Breathless, urgent delivery (HIGH) |

### Vocal Style & Technique
| Tag | Effect |
|-----|--------|
| `[Falsetto]` / `[Head Voice]` | High, airy vocal register |
| `[Chest Voice]` | Full, resonant lower register |
| `[Breathy]` | Airy, breath-heavy vocal |
| `[Raspy]` | Rough, textured vocal |
| `[Smooth]` / `[Soulful]` | Polished, warm delivery |
| `[Operatic]` | Classical vocal technique |
| `[Crooning]` | Soft, intimate jazz-style singing |
| `[Nasal]` | Nasal-toned delivery |
| `[Airy]` | Light, ethereal vocal |
| `[Harmonies]` / `[Harmonized]` | Multi-voice harmony layering |
| `[Ad-libs]` / `[Ad-lib]` | Improvised vocal fills and runs |
| `[Vocal Run]` / `[Melisma]` | Extended note runs across syllables |
| `[Vibrato]` | Oscillating pitch on sustained notes |
| `[Staccato]` | Short, detached vocal phrasing |
| `[Legato]` | Smooth, connected vocal phrasing |
| `[Call and Response]` | Back-and-forth vocal pattern |
| `[Chant]` | Rhythmic, repetitive vocal pattern |
| `[Choir]` / `[Choir Vocals]` | Full choir sound |
| `[Scat]` | Improvised nonsense syllables (jazz) |
| `[Hummed]` / `[Humming]` | Hummed melody, no words |
| `[Whistled]` / `[Whistling]` | Whistled melody |
| `[Backing Vocals]` | Explicit backing vocal layer (distinct from parentheses technique) (HIGH) |
| `[Stacked Harmonies]` | Dense layered harmonies (HIGH) |
| `[Gospel Choir]` | Gospel-style choir (HIGH) |
| `[Narrator]` / `[Female Narrator]` | Narration voice, distinct from `[Spoken Word]` (HIGH) |
| `[Announcer]` / `[Reporter]` | Announcer or reporter voice style (HIGH) |
| `[Primal Scream]` | Raw, primal scream vocal (Experimental) |
| `[Diva Solo]` | Big diva-style vocal moment (Experimental) |
| `[Vocaloid]` | Vocaloid-style synthetic vocal (Experimental) |
| `[Gregorian Chant]` | Gregorian chant style (Experimental) |
| `[Androgynous Vocals]` | Gender-ambiguous voice (Experimental) |

### Rap & Hip-Hop Delivery
| Tag | Effect |
|-----|--------|
| `[Rapped]` / `[Rap]` | Rhythmic spoken delivery |
| `[Fast Rap]` / `[Double Time]` | High-speed rap delivery |
| `[Slow Flow]` | Deliberate, spaced-out rap |
| `[Melodic Rap]` | Singing-rapping hybrid |
| `[Trap Flow]` | Trap-style cadence with hi-hat patterns |
| `[Boom Bap Flow]` | Classic hip-hop rhythmic delivery |
| `[Mumble Rap]` | Mumbled, indistinct rap delivery (HIGH) |

### Vocal Identity
| Tag | Effect |
|-----|--------|
| `[Male Vocal]` / `[Male Vocalist]` / `[Man]` | Male voice |
| `[Female Vocal]` / `[Female Vocalist]` / `[Woman]` | Female voice |
| `[Boy]` / `[Girl]` | Younger-sounding voice |
| `[Duet]` | Two distinct voices alternating |

### Vocal Effects
| Tag | Effect |
|-----|--------|
| `[Reverb]` | Reverberant vocal treatment |
| `[Delay]` | Echo/delay on vocals |
| `[AutoTune]` / `[No AutoTune]` | Add or prevent pitch correction |
| `[Distorted Vocals]` | Distortion effect on voice |
| `[Filtered Vocals]` | Filtered/muffled vocal sound |
| `[Vocoder]` | Robotic/synthesized vocal effect |
| `[Telephone Effect]` | Lo-fi phone-quality vocal |
| `[Glitch]` | Glitch effect on vocals (Experimental) |

### Vocal Emotion
| Tag | Effect |
|-----|--------|
| `[Vulnerable]` | Fragile, exposed delivery |
| `[Defiant]` | Strong, resistant tone |
| `[Sultry]` | Sensual, low-energy seduction |
| `[Joyful]` | Bright, happy delivery |
| `[Melancholic]` | Sad, wistful tone |
| `[Aggressive]` | Forceful, combative delivery |

## Descriptor Metatags

Provide guidance to Suno's interpretation. Keep text short: 1-3 words.

### Core Descriptor Tags (Established)
| Tag | Example | Placement |
|-----|---------|-----------|
| `[Mood: ...]` | `[Mood: haunting]` | Top (global) or before section (local) |
| `[Energy: ...]` | `[Energy: building]` | Before section |
| `[Vocal Style: ...]` | `[Vocal Style: whispered]` | Before section |
| `[Instrument: ...]` | `[Instrument: solo piano]` | Before section |

### Additional Descriptor Families (HIGH confidence — colon syntax)
These follow the same `[Category: value]` pattern as the core descriptors above:

| Tag | Examples | Notes |
|-----|---------|-------|
| `[Atmosphere: ...]` | `[Atmosphere: Dreamy]`, `[Atmosphere: Cyberpunk]`, `[Atmosphere: Medieval]` | Sets environmental/spatial context |
| `[Texture: ...]` | `[Texture: Grainy]`, `[Texture: Velvet]` | Controls sonic texture quality |
| `[Effect: ...]` | `[Effect: Lo-fi]`, `[Effect: Reverb: Hall]`, `[Effect: Delay: Ping-pong]`, `[Effect: Distortion]`, `[Effect: Sidechain]`, `[Effect: Radio Filter]` | Production effects — supports nested colon syntax for specificity |
| `[Harmony: ...]` | `[Harmony: High]` | Harmony register/style guidance |
| `[Voice: ...]` | `[Voice: Auto-tune]` | Vocal processing direction |
| `[Vibe: ...]` | `[Vibe: Cinematic]` | Overall vibe/feel — similar to Mood but more production-oriented |
| `[Tempo: ...]` | `[Tempo: slow]` | Tempo suggestion (note: BPM-specific tags remain ineffective — see Experimental Section Tags) |

### Standalone Mood Tags (bare bracket — no colon needed) (HIGH)
These work as simple bracket tags without the `[Mood: ...]` prefix:

`[Uplifting]`, `[Haunting]`, `[Dark]`, `[Nostalgic]`, `[Somber]`, `[Romantic]`, `[Dreamy]`, `[Peaceful]`, `[Anxious]`, `[Euphoric]`, `[Mysterious]`, `[Playful]`, `[Epic]`, `[Intimate]`, `[Bittersweet]`, `[Triumphant]`

### Standalone Energy Tags (bare bracket — no colon needed) (HIGH)
These work as simple bracket tags without the `[Energy: ...]` prefix:

`[High Energy]`, `[Medium Energy]`, `[Low Energy]`, `[Chill]`, `[Driving]`, `[Explosive]`, `[Building]`, `[Relaxed]`, `[Frantic]`, `[Steady]`

**Mood word effectiveness:** Vivid, visceral words work better than polite ones. `[Mood: Mardi Gras]`, `[Mood: wild, party]`, `[Mood: dark, haunting]` are more effective than `[Mood: festive]` or `[Mood: celebratory]`. Suno responds to emotional intensity in tag language.

### Energy Tags — Production-Confirmed Behavior
These energy and vocal style descriptors have been tested in production and produce reliable results:

| Tag | Observed Effect |
|-----|-----------------|
| `[Energy: stripped, minimal]` | Reliably reduces instrumentation |
| `[Energy: massive]` | Reliably adds full band weight |
| `[Energy: building]` | Works for gradual intensity increase |
| `[Vocal Style: whispered]` | More reliably quiet than `[Vocal Style: clean, distant]` — use as the go-to for quiet sections |
| `[Vocal Style: acapella]` | Sometimes works, sometimes Suno adds light instrumentation anyway |
| `[Whispered, vulnerable]` | The most reliable quiet-section tag confirmed across multiple songs — use for descent/resolution sections |

### Three-Phase Dynamic Arcs (Up, Peak, Down)
For songs that need to build UP and come back DOWN, place descent tags at the **transition point**, not just the outro. The mistake is saving all the quiet tags for `[Outro]` — by then the energy has already carried through. Instead:

1. Place `[Energy: minimal, fading to silence]` and `[Vocal Style: whispered, vulnerable]` **before** the final lines, at the moment the song should begin its descent.
2. `[Whispered, vulnerable]` is the single most reliable quiet-section tag — confirmed across multiple songs. Prefer it over `[Soft]` or `[Gentle]` when you need a guaranteed drop.
3. The descent tag placement matters more than the outro tags. If the transition into the final section is already quiet, the outro follows naturally.

### Vocal Style Findings — Harmonized as Sweet Spot
`[Vocal Style: gritty]` combined with high energy and high Weirdness produces screaming even with Exclude Styles set to block it. `[Vocal Style: clean]` removes too much edge — it strips the character out of the vocals. **`[Vocal Style: harmonized]` on all sections is the sweet spot for dual-vocalist work** — it blends both voices naturally without pushing into scream territory or losing grit. "Raw gritty melodic singing" in the style prompt works fine when paired with `[Vocal Style: harmonized]` in the metatags — the style prompt provides the tonal character while the metatag controls the delivery mode.

### Structural Metaphor via Time Signature Changes
Using different time signatures for different section types creates structural metaphor where musical form embodies lyrical meaning. For example: odd time signatures for verses (chaos, instability) paired with straight 4/4 for choruses (resolution, arrival). This is a powerful technique for prog — the musical structure itself becomes a storytelling device. Implement via experimental time signature tags (e.g., `[Verse 1: 7/8]`, `[Chorus: 4/4]`), acknowledging these are inconsistently respected but worth attempting for the payoff when they land. Note: BPM tags are confirmed ineffective (see Experimental Section Tags), but time signature tags are a separate mechanism worth trying.

### Dual Vocals — What Works and What Doesn't
- `dual male vocals harmonized and gritty` in the style prompt produces harmony/doubling on choruses — confirmed working.
- `dual vocals trading` does NOT reliably make two voices trade lines.
- True call-and-response between distinct voices is not reliably achievable through tags alone.
- The best dual-voice effect comes from using parenthetical backing vocals (see Parentheses section below).

## Dynamic & Transition Tags

Tags that control energy flow and transitions within the song.

| Tag | Effect |
|-----|--------|
| `[Fade In]` | Gradual volume increase at start |
| `[Fade Out]` / `[Fade]` | Gradual volume decrease |
| `[Swell]` | Gradual intensity increase |
| `[Crescendo]` | Building volume/intensity |
| `[Decrescendo]` | Decreasing volume/intensity |
| `[Silence]` | Brief moment of silence |
| `[Stop]` | Abrupt stop |
| `[End]` | Hard stop — prevents trailing instrumental generation after lyrics |
| `[Soft End]` | Gentle ending variation (HIGH) |
| `[Dramatic End]` | Dramatic ending variation (HIGH) |
| `[Big Finish]` | Grand climactic ending (HIGH) — also works as a section tag |
| `[Unresolved tension]` | Avoids tonic resolution, ends on suspended chord (HIGH) |
| `[Key Change]` / `[Key Modulation]` | Signal a key change, usually upward for a lift (HIGH) |
| `[Metric Modulation]` | Rhythmic shift changing perceived tempo (HIGH) |
| `[Accelerando]` | Gradually speed up tempo (HIGH) |
| `[Ritardando]` | Gradually slow down tempo (HIGH) |

## Sound Effect Tags

Environmental and ambient sounds Suno can generate. Use sparingly — these work best as brief textures, not sustained effects.

| Tag | Examples |
|-----|---------|
| **Nature** | `[Rain]`, `[Thunder]`, `[Wind]`, `[Ocean Waves]`, `[Birds Chirping]`, `[Forest]` |
| **Urban** | `[City Ambience]`, `[Phone Ringing]`, `[Beeping]`, `[Static]` |
| **Human** | `[Applause]`, `[Cheering]`, `[Clapping]`, `[Chuckles]`, `[Giggles]`, `[Sighs]`, `[Screams]`, `[Cough]`, `[Clears Throat]` |
| **Music** | `[Record Scratch]`, `[Bell Dings]`, `[Fire Crackling]` |
| **Animals** | `[Barking]`, `[Squawking]`, `[Howling]` |
| **Meta** | `[Censored]` (bleep sound) |

## Production & Mix Tags (HIGH)

Tags that control production quality and mix effects. Place before sections or at top for global effect.

| Tag | Effect |
|-----|--------|
| `[Lo-fi]` | Lo-fi production quality |
| `[Reverb Tail]` | Extended reverb decay effect |
| `[Echo]` | Echo effect |
| `[Vinyl Crackle]` / `[Vinyl Hiss]` | Vinyl texture overlay |
| `[Distant Voices]` | Distant/far-away vocal texture |

## Timing & Rhythm Tags (HIGH)

Tags that control rhythmic feel and timing within sections. These are distinct from BPM tags (which remain ineffective — see Experimental Section Tags). These tags describe rhythmic patterns and feels that Suno can interpret.

| Tag | Effect |
|-----|--------|
| `[Half-Time]` | Half-time feel — slower, heavier beat |
| `[Swung Feel]` / `[Shuffle]` | Swing/shuffle rhythm |
| `[Triplet Feel]` | Triplet-based rhythmic feel |
| `[Syncopated]` | Syncopated rhythm |
| `[Straight]` | Straight (non-swung) rhythm |
| `[Four on the Floor]` | Steady kick on every beat |
| `[Polyrhythmic]` | Multiple simultaneous rhythms |
| `[Breakbeat]` | Breakbeat rhythm pattern |

**Rhythm nouns over tempo adjectives:** "Halftime," "double-time," "shuffle," "breakbeat" lock rhythmic feel better than "slow," "fast," "upbeat." These nouns describe specific drum patterns Suno can interpret; adjectives are vague and often ignored.

## Standalone Instrument Tags (HIGH)

These work as bare bracket tags in the lyrics field — not just via `[Instrument: ...]` colon syntax. Place before a section to feature that instrument, or use as section tags for solos/features.

### Keys
`[Piano]`, `[Electric Piano]`, `[Rhodes]`, `[Wurlitzer]`, `[Organ]`, `[Hammond Organ]`, `[Harpsichord]`, `[Clavinet]`, `[Mellotron]`

### Synths
`[Synth]`, `[Analog Synth]`, `[Moog Synth]`, `[Synth Pad]`, `[Lead Synth]`, `[Synth Stabs]`, `[Pad]`, `[Pluck Synth]`, `[Arpeggiated Synth]`, `[Synth Bass]`, `[Acid Bass]`, `[Supersaw]`, `[Wobbly Bass]`

### Strings
`[Acoustic Guitar]`, `[Electric Guitar]`, `[Distorted Guitar]`, `[Clean Guitar]`, `[Jangly Guitar]`, `[Fingerpicked Guitar]`, `[Slide Guitar]`, `[12-String Guitar]`, `[Classical Guitar]`, `[Bass Guitar]`, `[Slap Bass]`, `[Upright Bass]`, `[Fretless Bass]`, `[Violin]`, `[Viola]`, `[Strings]`, `[String Quartet]`, `[String Section]`, `[Cello]`, `[Double Bass]`, `[Pizzicato]`, `[Harp]`, `[Ukulele]`, `[Banjo]`, `[Mandolin]`, `[Sitar]`

### Brass & Winds
`[Saxophone]`, `[Tenor Sax]`, `[Alto Sax]`, `[Trumpet]`, `[Trombone]`, `[French Horn]`, `[Tuba]`, `[Brass Section]`, `[Flute]`, `[Clarinet]`, `[Oboe]`, `[Harmonica]`, `[Accordion]`, `[Bagpipes]`, `[Didgeridoo]`

### Percussion
`[Drums]`, `[Acoustic Drums]`, `[Electronic Drums]`, `[Brushed Drums]`, `[Live Drums]`, `[808s]`, `[808 Bass]`, `[808 Drums]`, `[Drum Machine]`, `[TR-909]`, `[Trap Hi-Hats]`, `[Taiko Drums]`, `[Congas]`, `[Bongos]`, `[Tambourine]`, `[Shaker]`, `[Handclaps]`, `[Claps]`, `[Gong]`, `[Timpani]`, `[Cinematic Percussion]`

### Orchestral
`[Orchestra]`, `[Full Orchestra]`, `[Chamber Orchestra]`, `[Brass Stabs]`

## Per-Section Instrument Control

Suno does NOT support per-section instrument exclusion — there is no `[No Brass]` or `[Instrument: exclude X]` tag. The Exclude Styles field is global and inconsistent for instrument exclusion. Instead, use these strategies:

### Strategy 1: Positive Instrument Filling
Tell Suno what instruments a section SHOULD have — this fills the "instrument attention" and crowds out unwanted elements:
```
[Verse 3]
[Instrument: heavy distorted guitar, crushing bass]
```
By specifying the instruments you want, there's less room for unwanted instruments to creep in.

### Strategy 2: Style Prompt Instrument Ordering
Place instruments you want throughout the song in the first ~200 characters of the style prompt. Place instruments you only want in specific sections (e.g., "NOLA funk brass") at the very END of the prompt — later content has less global influence, so it's more likely to appear only where metatags reinforce it.

### Strategy 3: Section-Specific Generation (Pro/Premier)
Use the Legacy Editor (Pro) or Studio (Premier) to generate different sections separately with different style prompts. For example:
- Generate verses with a style prompt that has NO brass references
- Generate the outro/finale with brass in the style prompt
- Splice together using the editor

### Strategy 4: Reinforce with Energy + Instrument Tags Together
Pair `[Instrument: ...]` with `[Energy: ...]` tags for stronger section differentiation:
```
[Verse 3]
[Energy: building]
[Instrument: distorted guitar, pounding drums]

[Outro]
[Energy: celebratory]
[Instrument: brass section, funk bass, horns]
```

### Key Limitation
Even with these strategies, Suno's instrument control is probabilistic — the style prompt sets a global palette, and section-level tags nudge within that palette. For dramatic instrument changes between sections, section-by-section generation (Strategy 3) is the most reliable approach.

### The Stems Solution (Pro/Premier)

Per-section instrument control via prompting alone is unreliable. The most reliable workflow for songs requiring different instruments in different sections:

1. **Generate** with ALL desired instruments in the style prompt (accepting that they'll bleed into all sections)
2. **Extract stems** — Suno Pro splits into up to 12 stems: vocals, backing vocals, drums, bass, guitar, keys, strings, **brass**, woodwinds, percussion, synth, FX
3. **Edit in a DAW** (e.g., Audacity) — mute/remove unwanted instrument stems per section
4. **Export** the final mix

Brass separates well as a dedicated stem. This is the recommended approach for songs with section-specific instrumentation.

**Important:** External DAW editing is a one-way operation. Once you edit outside Suno, you lose Suno's editing capabilities (Replace Section, Extend, etc.) on that version. Plan your Suno edits BEFORE exporting to a DAW.

## Parameterized Section Tags (HIGH — MAJOR v5 Feature)

Section tags support inline arrangement instructions via colon (`:`) or pipe (`|`) syntax. This allows per-section arrangement control directly in the section tag itself, without needing separate descriptor tags.

### Colon Syntax — Arrangement Instructions
```
[Verse: whispered vocals, acoustic guitar only]
[Chorus: full band, powerful vocals]
[Bridge: stripped back, piano only]
[Verse 2: lo-fi, distant vocals, minimal drums]
```

### Pipe Syntax — Rhythmic/Feel Modifiers
```
[Chorus | Half-Time]
[Chorus | Double-Time]
[Verse 3 | Swung Feel]
```

Both syntaxes are confirmed working on v5. The colon syntax is more flexible (accepts comma-separated arrangement descriptions), while the pipe syntax is cleaner for single modifiers. These can be combined with separate descriptor tags on subsequent lines for maximum control, but the inline approach is often sufficient and saves character budget.

**Relationship to BPM tags:** Note that `[Verse 1: 65 BPM]` style BPM parameterization remains ineffective (see Experimental Section Tags below). The parameterized syntax works for arrangement/feel instructions, not for tempo numbers.

## Experimental Section Tags

These are partially supported and may not work consistently across all models.

| Tag Syntax | Purpose | Notes |
|-----------|---------|-------|
| `[Verse 1: 7/8]` / `[Chorus: 4/4]` | Time signature hint per section | Inconsistently respected but worth attempting for prog/experimental work. Studio 1.2's time signature picker does NOT yet send to generative models — in-lyric tags are currently the only way to attempt this |
| `[Callback: ...]` | During Extend/Replace, references a prior section's feel (Experimental) | e.g., `[Callback: Verse 1 energy]` — useful for maintaining continuity across generations |

### BPM Tags — Confirmed Ineffective

**BPM tags in lyrics have ZERO detectable effect on Suno's actual output.** This was tested across 5 songs with librosa analysis:
- "Want" tagged at 60 BPM throughout — Suno delivered 95.7 BPM
- "Back Woods" tagged 65-150 BPM across sections — Suno delivered 123 BPM steady, no variation

Tags like `[Verse: 65 BPM]` or `[Chorus: 130 BPM]` are ignored by the generative model. Suno picks its own tempo based on genre, style prompt, and arrangement context. **Do not use BPM tags in lyrics — they waste character budget and create false expectations.**

For actual tempo/pacing control, see "Line Density as Tempo Control" and "Half-Time / Double-Time Drum Feel" below.

## Lyric Formatting as Suno Controls

These are NOT metatags but critical formatting techniques that directly control Suno's vocal and rhythmic interpretation.

### Punctuation Effects
| Character | Effect | Guidance |
|-----------|--------|----------|
| `,` (comma) | Breath pause | Use to shape natural phrasing |
| `—` / `--` (dash) | Hard pause / extended syllable linkage | Creates a harder pause than comma or ellipsis |
| `...` (ellipsis) | Micro-pause / trailing delivery | Suggests trailing off — more subtle than a dash |
| `!` (exclamation) | **BARK/ATTACK TRIGGER** | Tells Suno's vocal engine to attack/bark that word. Bleeds forward into subsequent sections. **NEVER use in sections that should be clean/quiet.** Use sparingly even in aggressive sections. Avoid in metal context — bleeds forward aggressively. |
| `?` (question mark) | Interrogative delivery | Generally respected — Suno lifts intonation at the end |
| No punctuation | Suno decides phrasing | Can be useful for intentional ambiguity — let the model choose |

### Capitalization Effects
| Style | Effect | Guidance |
|-------|--------|----------|
| Sentence case | Normal delivery | Use throughout as baseline |
| ALL CAPS | **Loudness ceiling** | Confirmed: ALL CAPS words are sung with more passion/volume. If you cap words in Verse 1, you've already hit the ceiling — nowhere to build. Save caps for the absolute peak moment only (one word, one line, in the climax). |

### Parentheses
| Format | Effect |
|--------|--------|
| `(words in parentheses)` | Interpreted as **backing vocals/texture**, not lead melody. Useful for dual vocal interplay: lead line with (backing harmonies). |

**Parenthetical Backing Vocals — Production-Tested Details:**
- No space before opening paren tightens coupling: `word(echo)` not `word (echo)`.
- Build echo density as intensity climbs — selective use beats every-line use.
- Works best as single-word echoes in early verses, full-phrase echoes in later verses.
- Confirmed working: Suno rendered `(blasting)` as a distinct backing vocal layer.
- This is the most reliable way to get a dual-voice effect (more reliable than `[Duet]` or style prompt dual vocals).

### Inline Performance Modifiers (HIGH)
Parenthetical performance cues placed at the END of a lyric line to direct vocal delivery for that specific line. **This is a SEPARATE use of parentheses from backing vocals** — context determines interpretation. Backing vocals typically echo/repeat a word from the line; performance modifiers are delivery instructions.

| Cue | Effect | Example |
|-----|--------|---------|
| `(breathy)` | Breathy delivery on that line | `I can't stop thinking about you (breathy)` |
| `(belt)` | Belted/powerful delivery | `HOLD ON (belt)` |
| `(breath)` | Audible breath/pause | `wait for me... (breath)` |
| `(hold)` | Sustained/held note | `stay with me (hold)` |

**Disambiguation from backing vocals:** Backing vocal parentheses contain lyric words that Suno sings as a second voice — e.g., `running through the fire(fire)`. Performance modifiers contain delivery instructions — e.g., `running through the fire (breathy)`. When in doubt, the presence of a recognizable delivery keyword (`breathy`, `belt`, `hold`, `breath`) signals a performance modifier.

### Structural Timing in Lyrics (HIGH)
Direct timing instructions can be embedded in the lyrics field to control when vocals begin or end relative to the track duration:

```
lyrics begin at 0:15; instrumental only after 1:45
```

Place at the very top of the lyrics field before any section tags. This tells Suno to generate instrumental content before vocals start and/or after vocals end, providing explicit control over song structure timing.

### Line Density as Tempo Control
This is the **PRIMARY mechanism** for controlling perceived tempo in Suno-generated vocals.

| Technique | Effect | Example |
|-----------|--------|---------|
| Short fragmented lines (1-3 words) | Slower delivery — each line gets its own phrase | `Fall` / `apart` / `slowly` |
| Single words on their own line | Slows and strips down — creates dramatic pauses | `Gone` |
| Long packed lines (many syllables) | Faster delivery — Suno compresses to fit | `Running through the city streets with nothing left to lose tonight` |
| Sparse words, long lines | Slow, spacious feel | `Drifting... on... the... tide` |
| Line breaks | Musical breaths — write breaks where you want the singer to breathe | |

**Key insight:** Word density is the PRIMARY mechanism for controlling perceived tempo. BPM tags have zero effect (confirmed by librosa — see Experimental Section Tags above). Energy metatags alone (`[Energy: high]`) do NOT reliably drive actual BPM shifts — they signal intensity but not tempo. Suno picks a single steady BPM for the entire song regardless of tags; what changes is *perceived* tempo through delivery density and arrangement.

**Why it works:** Librosa analysis confirms that BPM does not actually change between sections, even when sections *feel* dramatically different in speed. A "hustle bustle" section with packed syllables feels like acceleration, but the underlying tempo is identical. The perception of speed comes from how much vocal content Suno must deliver per beat.

**Recommended multi-technique approach for perceived tempo contrast:**
The most effective tempo contrast uses these together — line density is the most reliable single technique:
1. **Line density (PRIMARY)** — short fragmented lines for slow sections, packed lines for fast. Most reliable mechanism.
2. **Half-time / double-time drum feel** — use rhythm nouns in metatags: `[Heavy: halftime]`, `[Double Time]`. Creates perception of halved or doubled tempo without BPM change. See below.
3. **Instrumental density / arrangement dropout** — pulling instruments out creates space that feels slower. Adding everything back feels like acceleration. Use `[Energy: stripped, minimal]` for slow feel, `[Energy: massive]` for fast feel.
4. **Line breaks as breath points** — more line breaks = more pauses = slower perceived delivery. Fewer breaks = longer phrases = faster feel. Write breaks where you want the singer to breathe.
5. **Energy metatags** — `[Energy: low]` / `[Energy: high]` to signal intensity shifts (affects feel, not actual BPM)
6. **Style prompt priming** — include "tempo changes" in the style prompt
7. **Weirdness slider** (Pro/Premier) — higher values (60-65+ tested) encourage rhythmic variation

**Do NOT use BPM tags** — they are confirmed ineffective (see above). Each of the above techniques reinforces the others. Line density alone produces the most consistent results.

### Half-Time / Double-Time Drum Feel

Drums can switch to half-time snare patterns without the actual BPM changing, creating the perception of halved tempo. This is one of the most effective perceived tempo control techniques after line density.

| Tag | Effect | Notes |
|-----|--------|-------|
| `[Heavy: halftime]` | Half-time drum feel — snare on beat 3 only | Creates perception of halved tempo. Powerful for heavy/slow sections. |
| `[Double Time]` | Double-time drum feel — snare on every beat | Creates perception of doubled tempo. Good for energy surges. |
| `[Breakdown]` + halftime language | Stripped-back half-time section | Combine with short fragmented lines for maximum slow-down effect |

**Rhythm nouns over tempo adjectives:** "Halftime," "double-time," "shuffle," "breakbeat" lock rhythmic feel better than "slow," "fast," "upbeat." These nouns describe specific drum patterns Suno can interpret; adjectives like "slow" are vague and often ignored.

### Scream Bleed-Through Prevention
Once Suno enters aggressive/scream mode, it tends to carry that energy forward into subsequent sections. Prevention strategies:

1. `[Vocal Style: whispered]` is a **harder vocal reset** than `[Vocal Style: clean]` — use after aggressive sections
2. Every section after an aggressive one needs an explicit vocal style reset tag
3. Never use `!` or ALL CAPS in sections immediately following an aggressive section
4. Consider adding a `[Break]` or `[Instrumental]` buffer between aggressive and clean sections

### Spaced-Out Letters as Vocal Effect
Placing spaces between every letter of a word — e.g., `R I G H T N E S S` — is a coin flip. Sometimes Suno spells out each letter individually, creating a powerful wall-of-sound moment. Sometimes it just sings the word normally. Not reliable enough to depend on. Worth trying for high-impact single words where a spelled-out delivery would be dramatic, but always have a fallback plan if Suno ignores it.

### Whispered Repeat as Closer
Adding a final whispered repeat of the last word or phrase after the poem ends creates a powerful closing echo-into-silence effect. Suno handles this well — it's a good standard technique for closing tracks.
```
[Outro]
Final lyric line here

[Whispered]
Forever

[End]
```
The `[Whispered]` tag before the single repeated word, followed by `[End]`, produces a natural fade-to-silence moment. Use the most resonant word from the final line or the song's central image.

### Vowel Stretching & Syllable Manipulation
| Technique | Effect |
|-----------|--------|
| `loooove`, `feeeel` | Nudges cadence — extended vowels suggest held/sustained delivery |
| `to-o-o-lling` | Hyphenated vowel extension can stretch a word for dramatic effect — results vary |
| Use sparingly | Test iteratively — results are inconsistent |

### Pronunciation / Phonetics
Suno has no dictionary — it guesses pronunciation from spelling patterns. This creates problems with homographs and unusual words.

- **Homographs are the biggest problem:** `lives` (verb "he lives" vs noun "our lives"), `read`, `lead` — Suno picks one pronunciation and may guess wrong.
- **Context from surrounding words does NOT reliably help** Suno pick the right pronunciation.
- **Phonetic spelling fixes:** `through` to `thru`, `lives` (verb) to `livz`, `Breaths` (verb) to `Breethz`.
- **Hyphenation forces syllable breaks:** `to-night`, `liv-uz`.
- **Only use phonetic spelling where a word has more than one valid reading** — don't phonetically spell unambiguous words.
- **Keep original spelling in the songbook** and note the phonetic substitution in the Suno lyrics version.
- **Post-generation lyric editing works** for pronunciation fixes — generate, listen, then fix spellings and re-generate if needed.

### Open-Ended Instrumental Sections Are Dangerous
Instrumental tags without clear boundaries cause Suno to generate excessive instrumental content:

- `[Guitar Solo]` works if followed by more vocals or `[End]`.
- `[Instrumental section — full prog, complex]` = Suno noodles indefinitely.
- Multiple `[Instrumental break]` tags = the song becomes mostly instrumental.
- **Always put `[End]` hard after the final vocal section or solo** to prevent trailing generation.

## Placement Rules

1. **Global descriptors** at the TOP of the lyrics — these set the overall tone
2. **Section-specific descriptors** RIGHT BEFORE the section they apply to — these override/refine the global
3. Section-specific tags are more effective than global tags
4. Don't over-tag — 1-2 descriptors per section maximum, fewer is often better
5. Metatags work best when short: 1-3 words, not full sentences
6. Tags are most impactful in the first 20-30 words and around section changes

## Formatting Rules

- Blank line between every section (including between tag and previous section)
- No style descriptions inside lyrics text (those go in the style prompt)
- No asterisks or markdown formatting in lyrics
- Commas create breath pauses, dashes create connected delivery, ellipses create micro-pauses — use intentionally
- **Exclamation points trigger bark/attack delivery** — avoid in clean sections
- **ALL CAPS sets the loudness ceiling** — save for peak moments only
- **Parentheses signal backing vocals** — not lead melody (but also used for inline performance modifiers like `(breathy)`, `(belt)` — see Inline Performance Modifiers section)
- Consistent line lengths within a section improve phrasing stability
- Line density (short vs long lines) is the primary tempo control mechanism

## Example with Instrumental Sections

```
[Mood: bittersweet]
[Vocal Style: intimate]

[Intro]

[Verse 1]
Walking through the fog of early morning light
Counting all the windows still awake
Every shadow holds a name I used to know
Every corner bends but doesn't break

[Pre-Chorus]
And I keep reaching for the thread
That ties me to some other when

[Chorus]
[Belted]
Come undone, come undone
Let the weight fall where it may

[Interlude]
[Guitar Solo]

[Verse 2]
[Whispered]
Fingerprints on glass that someone cleaned away
Letters folded into paper cranes

[Chorus]
Come undone, come undone
Let the weight fall where it may

[Bridge]
[Energy: stripped back]
Maybe what we lost was just the frame
And the picture's hanging somewhere still

[Final Chorus]
[Energy: building]
[Belted]
Come undone, come undone
Let the weight fall where it may
We were never meant to stay

[Outro]
[Hummed]
[Fade Out]
```

## Sources

- [Suno Help: How long will my song be?](https://help.suno.com/en/articles/2409473)
- [HookGenius: All Suno Metatags Complete List (2026)](https://hookgenius.app/learn/suno-metatags-complete-list/)
- [HookGenius: The Art of Prompting Suno](https://hookgenius.app/learn/art-of-prompting-suno/)
- [HookGenius: Suno Negative Prompting Guide](https://hookgenius.app/learn/suno-negative-prompting/)
- [HookGenius: Suno v5 Complete Guide](https://hookgenius.app/learn/suno-v5-complete-guide/)
- [HookGenius: Suno Character Limits](https://hookgenius.app/learn/suno-character-limits/)
- [Musci.io: Suno Tags List Complete Guide (2026)](https://musci.io/blog/suno-tags)
- [Suno Wiki: List of Metatags](https://sunoaiwiki.com/resources/2024-05-13-list-of-metatags/)
- [SunoMetaTagCreator: Complete Guide (1000+ tags)](https://sunometatagcreator.com/metatags-guide)
- [OpenMusicPrompt: 500+ Pro Tags & Templates (2026)](https://openmusicprompt.com/blog/suno-ai-metatags-guide)
- [BlakeCrosley: Suno AI Definitive Technical Reference](https://blakecrosley.com/guides/suno)
- [Lilys/Suno Prompting Secrets](https://lilys.ai/notes/en/suno-ai-v5-20251020/suno-prompting-secrets-powerful-metatags)
- [StokeMcToke: Complete Suno AI Meta Tags Guide](https://stokemctoke.com/the-complete-suno-ai-meta-tags-guide/)
- [JackRighteous: Suno AI Meta Tags Guide](https://jackrighteous.com/en-us/pages/suno-ai-meta-tags-guide)
- [CometAPI: How to Instruct Suno v5 with Lyrics](https://www.cometapi.com/how-to-instruct-suno-v5-with-lyrics/)
- [MusicSmith: AI Music Generation Prompts Best Practices](https://musicsmith.ai/blog/ai-music-generation-prompts-best-practices)
- [howtopromptsuno.com: Voice Tags Guide](https://howtopromptsuno.com/making-music/voice-tags)
- [Plain English: 10 Suno v5 Prompt Patterns That Never Miss](https://plainenglish.io/blog/i-made-10-suno-v5-prompt-patterns-that-never-miss)
- [HookGenius: Suno v5.5 Guide — Voices, Custom Models & My Taste](https://hookgenius.app/learn/suno-v5-5-guide/)
- [HookGenius: 300+ Suno Style Tags That Actually Work (2026)](https://hookgenius.app/learn/suno-style-tags-guide/)
- [HookGenius: Suno Prompts Complete Guide](https://hookgenius.app/learn/suno-prompts-complete-guide/)
- [Suno API Docs: Character Limits by Model (sunoapi.org)](https://docs.sunoapi.org/suno-api/generate-music)
- [iFlow.bot: Suno v5 Secrets](https://iflow.bot/suno-v5-secrets-crafting-ai-generated-songs/)
