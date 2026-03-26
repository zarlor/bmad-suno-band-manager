# Suno Platform Reference

Quick-reference for Suno models, plans, parameters, metatags, and common pitfalls. This is a companion to the [Usage Guide](USAGE.md) — it covers *how Suno works*, while the Usage Guide covers *how to use Mac*.

---

## Model Comparison

| Model | Style | Character Limit | Best For | Tier |
|-------|-------|----------------|----------|------|
| **v4.5-all** | Conversational descriptions | 1,000 | Free users, heavier/faster genres, longer songs (~8 min) | Free |
| **v4 Pro** | Simple descriptors | 200 | Straightforward, shorter prompts | Paid |
| **v4.5 Pro** | Conversational descriptions | 1,000 | Intelligent prompts, narrative style | Paid |
| **v4.5+ Pro** | Conversational descriptions | 1,000 | Advanced creation methods | Paid |
| **v5 Pro** | Crisp film-brief (4-7 descriptors) | 1,000 | Authentic vocals, superior audio quality, section editing | Paid |

**Character limit details:**
- **v4 Pro:** 200 chars (hard limit, silently truncated)
- **v4.5+ / v5:** 1,000 chars (API confirmed), but the effective window is still ~200 chars -- front-loaded terms dominate, and content beyond ~200 chars has diminishing returns. 4-7 descriptors is the sweet spot.

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

---

## Plan Comparison

| Feature | Free ($0) | Pro ($8/mo billed yearly) | Premier ($24/mo billed yearly) |
|---------|-----------|---------------------|--------------------------|
| **Model access** | v4.5-all only | All models incl. v5 | All models + Studio |
| **Credits** | 50/day (~10 songs) | 2,500/mo (~500 songs) | 10,000/mo (~2,000 songs) |
| **Commercial use** | No | Yes (new songs) | Yes (new songs) |
| **Weirdness slider** | No | Yes (0-100) | Yes (0-100) |
| **Style Influence slider** | No | Yes (0-100) | Yes (0-100) |
| **Audio Influence slider** | No | Yes (0-100, with Persona or audio upload) | Yes (0-100, with Persona or audio upload) |
| **Exclude Styles field** | No | Yes (Early Access Beta) | Yes (Early Access Beta) |
| **Inspo** | No | Yes (v4.5+ Pro) | Yes |
| **Legacy Editor** | No | Yes (section replace, rearrange, crop, fade) | Yes |
| **Personas** | No | Yes | Yes |
| **Stems** | No | Up to 12 | Up to 12 |
| **Audio upload** | 1 min | 8 min | 8 min |
| **Add Vocals/Instrumental** | No | Yes | Yes |
| **Studio** | No | No | Yes |
| **Queue** | Shared | Priority, 10 at once | Priority, 10 at once |
| **Add-on credits** | No | Yes | Yes |

Free-tier "More Options" includes: Vocal Gender, Manual/Auto Lyrics mode, Song Title only.

Pro/Premier "More Options" additionally includes: Weirdness slider, Style Influence slider, Audio Influence slider (with Persona or audio upload), Exclude Styles, Personas, Inspo, and the Legacy Editor for section-level editing.

**Vocal consistency across songs:** Suno interprets the same style prompt differently on every generation. Descriptive prompt language (e.g., "breathy female vocal with indie folk phrasing") gets you in the right neighborhood but not an exact match. The **Persona** feature (Pro/Premier) is the only reliable way to lock in a consistent vocal identity across songs -- it reuses the vocal character from a source generation. If you are working on an album or project where songs need to sound like the same singer, Personas are essential.

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

- **1,000-character limit** (200 for v4 Pro) -- content beyond this is silently truncated. Effective window is ~200 chars; 4-7 descriptors is the sweet spot.
- **Word order is weighted** -- front-loaded terms dominate. Priority order: Genre > Mood/Energy > Instruments > Vocals > Production. Treat the first ~200 characters as the "critical zone."
- **Hyper-specific beats generic** -- "1980s synth-pop" not "pop"; "distorted electric guitar, power chords" not "guitar"
- **BPM and key in style prompt (v5)** -- may work better in v5 than in lyric tags: `deep house, 122 BPM, A minor, hypnotic groove`. Still ineffective in v4/v4.5.
- **Production descriptors (v5)** -- "radio-ready mix, punchy drums, wide stereo field, crisp high-end, warm bass" are effective in v5
- **Never put artist names in the style prompt** -- Suno does not reliably replicate named artists. Decompose into concrete sonic descriptors instead.
- **Never put sound cues, asterisks, or style descriptions inside lyrics** -- the style prompt and lyrics are separate inputs
- **Negative/exclusion prompts go in the Exclude Styles field**, not in the main style prompt. In-prompt negatives ("no [element]" at the end) also work as a fallback.
- **Style prompt sets ONE overall mood** -- it cannot describe a tempo journey ("halftime to double-time" gets averaged). Suno delivers a single steady BPM per song. Use lyric density and rhythm noun metatags (`[Heavy: halftime]`, `[Double Time]`) in lyrics for perceived section-level tempo changes.
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
- **"Rock Opera" and "Cinematic" are keyboard triggers** -- both terms pull keyboard/synth arrangements into the mix. Use `power ballad`, `dynamic shifts` instead when you want drama without keyboards.
- **Three-phase dynamic arc needs double-stating** -- songs that go quiet → massive → quiet need the arc stated TWICE in the style prompt: once as a narrative description (`building from gentle to crushing then returning to gentle`) and once as a shorthand (`dynamic arc quiet to massive to quiet`). A single mention is not enough — Suno tends to flatten or ignore the return to quiet without the reinforcement.
- **Suno adds unscripted guitar solos regularly** -- three of four analyzed tracks had solos not in the lyrics. Plan for this or use [End] tags to prevent post-vocal noodling.
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

### Section Tags

| Tag | Job |
|-----|-----|
| `[Intro]` | Opening (unreliable -- may need regeneration) |
| `[Verse]` | Setup -- establishes story, scene, or emotion |
| `[Pre-Chorus]` | Lift -- builds tension before the payoff |
| `[Chorus]` | Payoff -- the hook, the memorable part |
| `[Bridge]` | Contrast -- new perspective, musical shift |
| `[Breakdown]` | Strip-down -- reduces instrumentation |
| `[Build-Up]` | Escalation -- increases energy toward a peak |
| `[Final Chorus]` | Closing payoff -- often bigger than earlier choruses |
| `[Outro]` | Resolution -- brings the song to a close |
| `[Instrumental]` | Instrumental section -- no vocals |
| `[Interlude]` | Musical bridge between sections |
| `[Solo]` / `[Guitar Solo]` | Instrumental solo section |
| `[Break]` | Brief pause or stripped-back moment |
| `[Drop]` | Sudden energy release (EDM/electronic) |
| `[Build]` / `[Build-Up]` | Escalation toward a peak |
| `[Hook]` | Short catchy phrase or motif |
| `[Post-Chorus]` | Extends or cools down chorus energy |
| `[Fade Out]` | Gradual volume decrease |

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
- Suno lyrics field has a hard limit of ~3,000 characters (silently truncated)

### Formatting as Suno Controls

- `!` (exclamation) = bark/attack trigger -- bleeds forward into subsequent sections. Avoid in clean/quiet sections.
- ALL CAPS = loudness ceiling -- save for the absolute peak moment only
- `(parentheses)` = backing vocals/texture, not lead melody
- Short lines (1-3 words) = slower delivery; long packed lines = faster delivery (PRIMARY tempo control — more reliable than any tag or slider). Line breaks act as breath points: more breaks = slower feel, fewer breaks = faster feel.
- Half-time / double-time drum feel via metatags (`[Heavy: halftime]`, `[Double Time]`) creates perceived tempo shifts without actual BPM change
- **BPM tags are confirmed ineffective** — do not use `[Verse: 65 BPM]` or similar tags. They have zero effect on output (librosa-confirmed).
- `[Instrument: ...]` before a section specifies instruments for that section -- use to crowd out unwanted instruments rather than trying to exclude them

---

## Troubleshooting Suno Issues

This table covers problems with Suno's output. For issues with Mac itself (wrong mode, missing profiles, skill errors), see the [Usage Guide Troubleshooting](USAGE.md#9-troubleshooting).

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

### Creative Issues

| Issue | What Happens | Fix |
|-------|-------------|-----|
| **Single generation** | One generation rarely nails it | Always generate 3-5 versions with the same prompt |
| **Same prompt, wildly different results** | Normal Suno behavior | This is expected. Generate 3-5 versions and pick the best. For v5 Pro, results vary more -- that is a feature, not a bug. |
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
