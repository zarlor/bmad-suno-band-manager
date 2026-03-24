# Model-Specific Prompt Strategies

> **Last validated:** March 2026 (Suno v5 Pro, v4.5-all, v4.5 Pro, v4.5+ Pro, v4 Pro). Suno updates models and prompt behavior frequently — use web search to verify strategies against current documentation when uncertain.

## Quick Reference

| Model | Style | Sweet Spot | Strengths |
|-------|-------|-----------|-----------|
| v4.5-all (free) | Conversational sentences | Flowing descriptions, natural language | Heavier/faster genres, longer-form (~8 min) |
| v4.5 Pro | Conversational + nuanced | Like v4.5-all with more detail responsiveness | Intelligent prompt enhancement |
| v4.5+ Pro | Advanced conversational | More control over structure | Advanced creation methods |
| v5 Pro | Crisp film-brief | 4-7 descriptors, emotional > technical | Natural vocals, instrument separation, polish |
| v4 Pro | Simple descriptors | Keep it straightforward | Improved sound quality over v3 |

## v4.5 Family (v4.5-all, v4.5 Pro, v4.5+ Pro)

### Prompt Style: Conversational

Write style prompts as flowing, descriptive sentences. The model responds well to narrative descriptions of the sound.

### Construction Pattern

```
[Genre and mood sentence]. [Instrumentation and texture sentence]. [Production and mix sentence]. [Energy and dynamics sentence].
```

### Example Prompts

**Indie folk-rock:**
> Create a melodic, emotional indie folk-rock song with organic textures and warm analog production. Acoustic guitar layered with subtle electronic elements, gentle percussion building through the song. Intimate male vocals with clear diction and restrained delivery, opening up on choruses.

**Upbeat pop:**
> Energetic, feel-good pop with a modern radio-ready sound. Bright synths, punchy drums, and a driving bass line. Female vocals with a confident, playful delivery. Big chorus with layered harmonies and a catchy hook.

**Dark electronic:**
> Deep, brooding electronic track with industrial textures and a slow-burning build. Heavy sub-bass, glitchy percussion, distorted synth drones. Minimal vocals — whispered, processed, barely human. Tension throughout, no release until the final drop.

### Tips

- Can be more verbose than v5 — the model handles longer descriptions well
- Conversational tone works: "Create a..." or "This should sound like..."
- Good for describing energy arcs: "begins with soft ambient layers, builds to..."
- Prompt Enhancement helper available in the UI — mention this to users

## v5 Pro

### Prompt Style: Crisp Film-Brief

Write style prompts as tight, evocative descriptors — like a creative brief for a film soundtrack. Emotional and textural language over technical specifications.

### Construction Pattern

```
[genre], [mood/emotion], [2-3 key sonic textures], [vocal character], [production quality notes]
```

Keep to **4-7 descriptors**. Each one should earn its place.

### Example Prompts

**Indie folk-rock:**
> indie folk-rock, melancholic warmth, acoustic guitar over ambient pads, breathy male vocal, intimate lo-fi mix with wide stereo field

**Upbeat pop:**
> modern pop, confident and bright, punchy drums, sparkling synths, female vocal with playful edge, radio-ready mix, big chorus harmonies

**Dark electronic:**
> dark electronic, industrial tension, sub-bass drones, glitchy percussion, whispered processed vocals, cinematic slow-burn

### Tips

- **Emotional descriptors beat technical ones:** "raw, yearning" > "120 BPM"
- **Production-quality descriptors work well:** "radio-ready mix", "wide stereo field", "punchy drums"
- **Include mix notes:** register, tone, phrasing, harmony
- **Vocals sound more natural** in v5 — breaths, phrasing, harmonies are authentic
- **Better instrument separation** — can request specific instrument prominence
- **Section-level editing** available in editor — structure control shifted from prompt to editor
- Don't waste characters on things the editor handles (song structure, section ordering)

**Tested v5 Pro descriptors (from live testing):**
- "down-tuned" and "crushing" — effective for pushing v5 from rock toward metal weight
- "raw melodic singing" — key phrasing for gritty-but-not-screaming vocals (overcorrects less than "clean singing with grit on peaks")
- "dual gritty male vocals" + "raw melodic singing" — achieved gritty-but-melodic without triggering screaming
- "heavy swamp metal" with Exclude Styles blocking screaming — got heavy without full scream on v5
- NOLA funk elements came through well across multiple sections on v5
- v5 had more dynamism and better section transitions than v4.5+ Pro for complex multi-tempo songs
- "NOLA funk groove" functions as BOTH a genre descriptor AND a rhythmic looseness instruction — NOLA funk and jazz are inherently rhythmically loose (swing, syncopation, playing around the beat). This makes it a better vehicle for odd time signatures and time changes than pure metal, which tends to be metronomically precise. Non-obvious but powerful finding.

**Confirmed Suno behavior (from Gemini analysis of production outputs):**
- "NOLA funk swing" lands as syncopation, not true swing — Suno interprets swing as a syncopation instruction rather than a jazz swing feel
- "Odd time signatures" is consistently ignored in 4/4 rock/metal context — the strong 4/4 pull of rock and metal genres overrides time signature instructions
- Suno adds unscripted guitar solos regularly — expect them even when not requested, especially in rock/metal genres
- Structural/section directions embedded in long style prompts are largely ignored — Suno treats the style prompt as a tonal palette, not a roadmap. Use metatags and the editor for structural control, not the style prompt.

## v4 Pro

### Prompt Style: Simple Descriptors

Straightforward genre + mood + basic production notes. Less nuanced than v4.5+ models.

**IMPORTANT: v4 Pro has a 200-character hard limit** (not 1,000 like v4.5+/v5). Every word must earn its place.

### Construction Pattern

```
[genre], [mood], [key instruments], [vocal type], [one production note]
```

### Example

> indie folk-rock, melancholic, acoustic guitar and ambient synths, male vocals, warm production

### Tips

- **200-character hard limit** — be extremely concise
- Keep it simpler than v4.5/v5
- Don't over-describe — diminishing returns on detail
- Focus on genre accuracy and mood

## Universal Rules (All Models)

1. **Character limits** — v4 Pro: 200 chars. v4.5+/v5: 1,000 chars. All silently truncated.
2. **Critical zone (first 200 chars)** — community testing suggests content beyond ~200 characters may have diminished influence on generation, even for v4.5+/v5. Front-load all essential genre, mood, and vocal descriptors within the first 200 characters. Content beyond this is supplementary.
3. **Genre and mood always go first** — they're the strongest signal
4. **Never put style cues inside lyrics** — style prompt and lyrics are separate inputs
5. **No asterisks or special formatting** in style prompts
6. **Never put artist names in style prompts** — Suno does not reliably replicate named artists. Decompose references into concrete sonic descriptors instead.
7. **Negative/exclusion prompts go in the separate Exclude Styles field**, not in the main prompt. Exception: a single "no X" in the main prompt is sometimes effective for emphasis (v5 handles in-prompt negatives better than v4.5), but keep exclusions in the dedicated field.
8. **Comma separation works across all models** — consistent delimiter
9. **Describe, don't command** — "dreamy shoegaze with female vocals" over "Create a dreamy shoegaze song." (v4.5 examples use "Create a..." which matches Suno's own v4.5 docs, but descriptive style generally works better.)

## Genre Keyword Ordering

Front-loaded terms dominate the generation. Whatever genre term appears first in the style prompt sets the primary sound — Suno treats it as the anchor, and everything after it is progressively more "flavoring."

When a genre should act as a secondary influence rather than the core sound, append qualifier words like "accents" or "undertones" to push it into the background. For example, `atmospheric swamp metal accents` tells Suno to use swamp metal as coloring rather than the main genre.

**Practical rule:** Put your dominant genre first. Demote secondary genres with "accents," "undertones," "influences," or "elements."

### Genre Term Behavior Table

Specific genre terms produce specific results. This table documents what Suno actually generates for common genre keywords, based on production testing.

| Genre Term(s) | What Suno Produces | Notes |
|---|---|---|
| `progressive metal` | Dream Theater-style technical shred | Avoid unless you specifically want technical wankery |
| `progressive groove metal` | Mastodon-adjacent pocket grooves | Better choice for most prog-metal needs |
| `prog rock` | Softer, more atmospheric progressive sound | Good for builds, dynamics, and patient arrangements |
| `heavy swamp metal` | Down/Crowbar-style low-end weight | Reliable for southern heaviness |
| `heavy swamp metal power ballad` | Gentle verses that build to heavy | Communicates "power ballad with weight" without invoking theatrical/keyboard territory |
| `dark alternative rock, slow and heavy, raw emotional weight, spacious oppressive mix, claustrophobic atmosphere` | Non-metal heaviness with emotional devastation | Good for pushing a metal band into non-metal territory; works for songs about powerlessness rather than power |
| `post-metal, post-hardcore` | Isis/Cult of Luna patient builds | Adding post-hardcore introduces off-tempo, prog-adjacent moments |
| `speed metal` | Fast, aggressive, thrash-adjacent | Straightforward — does what it says |
| `hard rock` | Straightforward driving energy | Clean, uncomplicated rock foundation |
| `hard rock` + `NOLA second line groove` + `brass band accents` | NOLA parade groove with rock weight | The combination pulls toward parade-style rhythms |
| `crushing slow heavy swamp metal` + `pounding heartbeat kick drum` | Heavy, deliberate, single-tempo weight | Stacking slow/heavy modifiers locks Suno into a plodding pace |
| `prog rock` + `slow build then fade` | Atmospheric with proper decrescendo | One of the few reliable ways to get Suno to actually come back down |
| `Acoustic, intimate, solo voice with gentle guitar, bluesy, swampy, sparse and warm, quiet reflection, raw clean vocals, stripped down, empty room atmosphere` | Acoustic track that retains band identity | `bluesy, swampy` keeps NOLA identity; `empty room atmosphere` = reverb/space; explicitly exclude `heavy guitars, drums` in Exclude Styles |

### Dangerous Words and Keyboard Triggers

Certain words reliably pull Suno into unwanted instrumental territory — typically theatrical, keyboard/synth-heavy, or cinematic-light arrangements. Avoid these when guitars and bass should lead.

| Word/Phrase | What Suno Does | Fix |
|---|---|---|
| `baroque` | Maps to theatrical/classical keyboard territory — Disney-adjacent | Describe Baroque qualities without the word: Bach counterpoint = `intricate interlocking guitar and bass melodies`; minor key ornamentation = `dark minor key, precise and ornate` |
| `orchestral`, `orchestral accents` | Defaults to light/cinematic strings, not heavy | Specify HEAVY orchestral instruments explicitly: `cello, heavy strings, kettle drums` — these live in metal's frequency range |
| `cinematic` | Pulls keyboard/synth-heavy arrangements | Use `dynamic shifts`, `building from gentle to crushing` instead |
| `rock opera` | Pulls keyboard/synth-heavy, theatrical arrangements | Use `power ballad`, `dynamic shifts`, `building from gentle to crushing` instead |

**"Baroque" workaround in detail:** If the song concept calls for Baroque-influenced metal, never use the word. Instead, describe the specific qualities you want — `intricate interlocking guitar and bass melodies` for counterpoint, `dark minor key, precise and ornate` for ornamentation. For orchestral weight, specify instruments that live in metal's frequency range: `cello, heavy strings, kettle drums`. Avoid `orchestral` as a standalone descriptor.

## Vocal Behavior and Triggers

### Scream/Harsh Vocal Triggers

Certain words reliably trigger unwanted screaming or harsh vocals, even when the intent is melodic:

- `metal` on its own (without melodic vocal guidance)
- `sludge`
- `doom`
- `!` in lyrics (exclamation marks push vocal delivery toward shouting/screaming)

**Fix:** Always pair heavy genre terms with explicit positive vocal instructions. For example, `heavy swamp metal, raw melodic singing` or `sludge metal, gritty male vocals, no screaming` (plus "screaming" in Exclude Styles). Telling Suno what you DO want from the vocals is more reliable than only excluding what you don't.

### "Technical" as a Modifier

The word "technical" behaves differently depending on what it modifies:

- `technical guitar riffs` → produces shreddy, noodly guitar work
- `rocking guitar riffs` → better choice for most heavy songs that need energy without wankery
- `driving technical bass` → produces slightly more interesting bass lines without going overboard; worth including as a standard ingredient in bass-heavy arrangements

## Instrument-Specific Guidance

### Drum Programming

Drum descriptors are highly context-dependent — the same term produces different results depending on surrounding genre and energy keywords.

- **"Second line" drums** shift meaning based on context: paired with slow + atmospheric terms, they produce a hip-hop pocket feel; paired with up-tempo + energetic + hard rock terms, they produce a NOLA parade groove
- **Splitting funk from drums:** To get funky bass and guitars without funk drums, describe the funk in the bass/guitar descriptors and keep the drum descriptors in metal territory (e.g., `funky bass groove, driving metal drums`)
- **Swing and groove patterns:**
  - `swinging drums` + `blues-metal intensity` → Bill Ward-style groove (loose, behind-the-beat swagger)
  - `pounding drums` → rigid, mechanical, metronomic feel (use when you want deliberate, machine-like precision)

### Bass Prominence (Known Limitation)

Suno cannot reliably produce bass-forward rock or metal mixes. This has been tested extensively:

- Requesting "bass-forward" or "prominent bass" in the style prompt produces marginal results at best — bass remains buried in the mix
- `bass and drums only, no guitar` combined with guitar in the Exclude Styles field was the most effective approach found, but this requires removing guitar entirely rather than simply featuring bass
- `funk metal` as a genre term triggers slap/pop bass (Flea-style), NOT overdriven fingerstyle (Geddy Lee-style) — there is currently no reliable way to get prominent overdriven bass in a full-band rock/metal context

**Treat bass-forward rock/metal as a known platform limitation.** If a song concept depends on prominent bass, consider the "bass and drums only" approach or accept that bass will sit in a typical supporting-instrument position in the mix.

## Dynamic Control via Style Prompt

Style prompt directives for energy and dynamics override lyric-level energy tags (like `[Building]` or `[Fade]`). This is powerful but requires careful handling.

### Build and Climax

- `slow massive build to crushing climax` makes Suno build ALL the way through the song, steadily increasing intensity. It will ignore any fade or cooldown tags in the lyrics — the style prompt's arc instruction wins.

### Decrescendo and Comedowns

Getting Suno to bring energy back down is harder than building up. Patterns that work:

- `slow build then fade` — tells Suno the arc goes up AND comes back down
- `dynamic shifts loud to quiet` — encourages contrast rather than one-directional energy
- `prog rock` + `slow build then fade` — the prog rock genre context supports patient dynamics, making the fade instruction more effective

**Key insight:** If a song needs to come DOWN after a peak, the decrescendo instruction must be in the style prompt. Lyric tags alone are not enough to counteract a style prompt that implies continuous build.

### Three-Phase Dynamic Arc (Quiet → Massive → Quiet)

Getting Suno to execute a full quiet-to-massive-to-quiet arc requires redundancy. State the arc **twice** in the style prompt using different phrasing: `building from gentle to crushing then returning to gentle` AND `dynamic arc quiet to massive to quiet`. One statement is not enough — Suno latches onto "crushing" and rides it out through the end of the song. The redundancy forces Suno to register the full arc rather than just the peak.

## Slider Guidelines

### Weirdness and Style Influence by Song Type

These are starting-point ranges based on production testing. Adjust per song, but these give a reliable baseline.

| Song Type | Weirdness | Style Influence | Notes |
|---|---|---|---|
| Acoustic/stripped | 40 | 80 | Lower Weirdness for compliance; high SI to honor the style prompt's genre descriptors |
| Structured songs (verse-chorus) | 50-55 | 75-80 | Higher Style Influence keeps structure tight |
| Dark alternative | 50-55 | 75-80 | Standard settings; may need lower Weirdness for compliance when pushing a metal band into non-metal territory |
| Through-composed | 55-60 | 70-75 | Slightly looser to allow organic flow |
| Funk-forward | 60 | 65-70 | Weirdness adds rhythmic surprise; lower SI lets funk breathe |
| Post-metal | 60-65 | 65 | Needs room for patient builds and textural exploration |
| Prog | 65-75 | 65 | Higher Weirdness encourages unexpected transitions |
| Circular / agitated | 75 | 65 | High Weirdness for unsettling, looping energy |

**General principle:** Weirdness adds unpredictability and non-obvious choices. Style Influence controls how tightly Suno follows the prompt versus doing its own thing. For conventional songs, keep SI high. For experimental work, back SI off and let Weirdness drive.

## Persona Style Prompt Integration

The Persona auto-populates the Style of Music field. Song-specific prompts should **build on** this base, not replace it. The Style Prompt Builder should assume the Persona's Styles content is already present and add song-specific elements on top. The Persona's Styles field contains universal band DNA — the sonic identity that should be consistent across all songs. Song-specific elements (odd time signatures, tempo changes, brass accents, genre departures) get layered per-song on top of that foundation.

## Cover Feature

Cover re-performs an existing song in a new style — it preserves the melody, lyrics, and structure while changing genre, instrumentation, vocal character, and production. Cover prompts use production language, clear genre descriptors, and specific instrumentation.

**CRITICAL: Covers are NOT eligible for commercial use — even on your own songs.** For commercial releases, create a fresh generation instead. This is a Suno platform restriction, not a suggestion.

## Persona and Inspo Playlist Behavior

### Inspo Playlist Warning

Using your own songs as Inspo playlist entries homogenizes the sound across generations. Suno pulls tonal and structural patterns from Inspo tracks, which flattens out the distinctiveness of new songs. **Drop Inspo when a song needs its own identity** — particularly for songs that are meant to stand apart from the rest of a catalog.

### Persona / Audio Influence on Era

Personas pull the overall sound toward the era of the source song used to create them. A persona built from a 70s-sounding track will drag new generations toward 70s production aesthetics, even when the style prompt targets a different era.

- Reducing Audio Influence to 10-15% helps but does not fully overcome the era pull
- For era-specific pieces where production style matters, consider generating without a persona entirely
- Alternatively, create era-specific personas — a "modern" persona and a "vintage" persona, for example — rather than fighting a single persona's baked-in era bias

### Audio Influence Slider Behavior

The Audio Influence slider controls how strongly the persona's source audio shapes the generation. The effective range is **15-25%** — values outside this range are either too detached or produce diminishing returns.

| Audio Influence | Behavior |
|---|---|
| 15% | Nearly loses persona identity — too detached for most uses |
| 20% | Holds identity loosely — allows significant genre departure. Use for experimental tracks or era-specific pieces where the persona's default era would interfere |
| 25% (default) | Strong persona anchor — the standard setting for both typical tracks AND acoustic/stripped songs |
| Above 25% | Diminishing returns — 40% tested, did not override an incompatible style prompt |

**Critical finding:** Acoustic and stripped-down songs can handle full 25% Audio Influence. The style prompt's genre descriptors override the persona's instrumental heaviness — the persona contributes only vocal identity. Only reduce Audio Influence when pushing into a different *heavy* genre where the persona's heaviness would compete with the target genre's heaviness.

## Iteration Best Practices

- **Generate 3-5 versions** per prompt before modifying — v5 produces more varied results than v4.5, and the desired result often appears on the 2nd or 3rd generation
- **Change only 1-2 variables** per iteration — isolate what works vs. what doesn't
- **Style Influence above ~80 plateaus** — increasing further rarely improves genre accuracy
- **For v5 Pro users:** Suno Studio offers section editing, stem separation (up to 12 stems), alternates, and warp markers. For structural problems (wrong arrangement, bad section), use Studio editing rather than re-prompting entirely

## Reference Track Translation Guide

When a user says "sounds like X meets Y," decompose into concrete attributes. **Never put artist names directly into the style prompt** — describe the sonic qualities of the era and style instead.

### Confidence Check (Critical — Prevents Hallucination)

Before decomposing any reference, honestly assess: **do you confidently know this artist/song well enough to accurately describe their distinctive sonic characteristics?**

- **If confident** — proceed with decomposition using the extraction framework below
- **If uncertain** (obscure artist, very recent release, regional/niche genre, or you're unsure of specific details) — **use web search first** (if a search tool is available) to research the artist's sound, genre, instrumentation, vocal style, and production approach. Then decompose from researched facts, not guesses.
- **If uncertain and no search available** — tell the user honestly: "I'm not confident I know [artist] well enough to describe their sound accurately. Can you tell me what you like about their sound — the vibe, the instruments, the vocals?" Then decompose from the user's description instead.

**Never fabricate sonic details for an artist you don't confidently know.** A wrong decomposition produces a style prompt that sounds nothing like what the user intended — and they won't know why until they hear the result.

### What to Extract from a Reference

- **Genre/subgenre** — what musical tradition?
- **Era/production style** — vintage analog? modern digital? lo-fi?
- **Vocal character** — what makes their voice distinctive?
- **Instrumentation signature** — what instruments define their sound?
- **Energy/dynamics** — how does the song move? build? stay flat? explode?
- **Emotional tone** — what feeling does it evoke?

### Example Decomposition

- "Bon Iver meets Radiohead" → falsetto vocals, ambient electronics, acoustic guitar foundation, experimental song structures, melancholic beauty with electronic tension, lo-fi warmth with glitchy textures
- "Dolly Parton meets Daft Punk" → country storytelling over electronic production, warm female vocals with robotic harmonies, acoustic meets synthesized, playful but polished

Always show the user your decomposition before building the prompt so they can confirm or correct your interpretation.
