# Suno Metatag Reference

Metatags are keywords in square brackets `[ ]` placed in the lyrics field to guide Suno's generation. This reference covers all known working tags as of March 2026. Suno evolves frequently — when uncertain about a tag's effectiveness, use web search to verify against current documentation.

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

### Rap & Hip-Hop Delivery
| Tag | Effect |
|-----|--------|
| `[Rapped]` / `[Rap]` | Rhythmic spoken delivery |
| `[Fast Rap]` / `[Double Time]` | High-speed rap delivery |
| `[Slow Flow]` | Deliberate, spaced-out rap |
| `[Melodic Rap]` | Singing-rapping hybrid |
| `[Trap Flow]` | Trap-style cadence with hi-hat patterns |
| `[Boom Bap Flow]` | Classic hip-hop rhythmic delivery |

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

| Tag | Example | Placement |
|-----|---------|-----------|
| `[Mood: ...]` | `[Mood: haunting]` | Top (global) or before section (local) |
| `[Energy: ...]` | `[Energy: building]` | Before section |
| `[Vocal Style: ...]` | `[Vocal Style: whispered]` | Before section |
| `[Instrument: ...]` | `[Instrument: solo piano]` | Before section |

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
Using different time signatures for different section types creates structural metaphor where musical form embodies lyrical meaning. For example: odd time signatures for verses (chaos, instability) paired with straight 4/4 for choruses (resolution, arrival). This is a powerful technique for prog — the musical structure itself becomes a storytelling device. Implement via experimental BPM/time signature tags (e.g., `[Verse 1: 7/8]`, `[Chorus: 4/4]`), acknowledging these are inconsistently respected but worth attempting for the payoff when they land.

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

## Experimental Section Tags

These are partially supported and may not work consistently across all models. Worth including but don't rely on them alone.

| Tag Syntax | Purpose | Notes |
|-----------|---------|-------|
| `[Verse 1: 65 BPM]` | BPM hint per section | Inconsistently respected on v4.5-all; may work better on v5 |
| `[Verse 1: 65 BPM, 6/8]` | BPM + time signature | Studio 1.2's time signature picker does NOT yet send to generative models — in-lyric tags are currently the only way to attempt this |

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

### Line Density as Tempo Control
This is the **PRIMARY mechanism** for controlling perceived tempo in Suno-generated vocals.

| Technique | Effect | Example |
|-----------|--------|---------|
| Short fragmented lines (1-3 words) | Slower delivery — each line gets its own phrase | `Fall` / `apart` / `slowly` |
| Single words on their own line | Slows and strips down — creates dramatic pauses | `Gone` |
| Long packed lines (many syllables) | Faster delivery — Suno compresses to fit | `Running through the city streets with nothing left to lose tonight` |
| Sparse words, long lines | Slow, spacious feel | `Drifting... on... the... tide` |
| Line breaks | Musical breaths — write breaks where you want the singer to breathe | |

**Key insight:** Word density is more reliable than BPM tags for tempo control. Energy metatags alone (`[Energy: high]`) do NOT reliably drive actual BPM shifts. They signal intensity but not tempo. Must be combined with line density strategy and style prompt priming with "tempo changes" for multi-tempo songs.

**Recommended multi-technique approach for tempo contrast (from v5 Pro testing):**
The most effective tempo contrast uses ALL of these together — no single technique is reliable alone:
1. **Line density** — short fragmented lines for slow sections, packed lines for fast
2. **BPM tags** — `[Verse: 65 BPM]` for slow, `[Chorus: 130 BPM]` for fast (partially supported)
3. **Energy metatags** — `[Energy: low]` / `[Energy: high]` to signal intensity shifts
4. **Style prompt priming** — include "tempo changes" in the style prompt
5. **Weirdness slider** (Pro/Premier) — higher values (60-65+ tested) encourage rhythmic variation

Each technique reinforces the others. Relying on any single one produces inconsistent results.

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
- **Parentheses signal backing vocals** — not lead melody
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
- [Musci.io: Suno Tags List Complete Guide (2026)](https://musci.io/blog/suno-tags)
- [Suno Wiki: List of Metatags](https://sunoaiwiki.com/resources/2024-05-13-list-of-metatags/)
- [SunoMetaTagCreator: Complete Guide (1000+ tags)](https://sunometatagcreator.com/metatags-guide)
