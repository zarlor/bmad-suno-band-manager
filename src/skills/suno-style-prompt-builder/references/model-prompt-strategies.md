# Model-Specific Prompt Strategies

> **Related references:** Style prompts work in conjunction with lyric metatags — for the full metatag catalog (section tags, vocal delivery, effects, production tags), see `suno-lyric-transformer/references/metatag-reference.md`. For mapping user feedback to style prompt adjustments, see `suno-feedback-elicitor/references/suno-parameter-map.md`.
>
> **Last validated:** April 6, 2026 (Suno v5.5 Pro, v5 Pro, v4.5-all, v4.5 Pro, v4.5+ Pro, v4 Pro). Updated with v5.5 community testing findings: corrected Voices Audio Influence ranges (JG BeatsLab), added Skill Level dropdown, My Taste magic wand/Style Augmentation, Personas/Voices coexistence, HookGenius 1000+ prompt analysis (tag count 5-8, cinematic modifier, production tags, conflicting tags), Weirdness-during-Extend drift finding, spoken word limitations, Custom Model consent. Suno updates models and prompt behavior frequently — use web search to verify strategies against current documentation when uncertain.

## Quick Reference

| Model | Style | Sweet Spot | Strengths |
|-------|-------|-----------|-----------|
| v4.5-all (free) | Conversational sentences | Flowing descriptions, natural language | Heavier/faster genres, longer-form (~8 min) |
| v4.5 Pro | Conversational + nuanced | Like v4.5-all with more detail responsiveness | Intelligent prompt enhancement |
| v4.5+ Pro | Advanced conversational | More control over structure | Advanced creation methods |
| v5 Pro | Crisp film-brief | 5-8 descriptors, emotional > technical | Natural vocals, instrument separation, polish |
| v5.5 Pro | Crisp film-brief (same as v5) | 5-8 descriptors, can be more granular | Most expressive, Voices, Custom Models, My Taste |
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

Keep to **5-8 descriptors**. Each one should earn its place.

### Example Prompts

**Indie folk-rock:**
> indie folk-rock, melancholic warmth, acoustic guitar over ambient pads, breathy male vocal, intimate lo-fi mix with wide stereo field

**Upbeat pop:**
> modern pop, confident and bright, punchy drums, sparkling synths, female vocal with playful edge, radio-ready mix, big chorus harmonies

**Dark electronic:**
> dark electronic, industrial tension, sub-bass drones, glitchy percussion, whispered processed vocals, cinematic slow-burn

### Tips

- **Emotional descriptors beat technical ones:** "raw, yearning" > "120 BPM". Use rhythm nouns instead of BPM values: "halftime groove," "double-time driving," "shuffle feel." (v5 may respond better to BPM in style prompts than v4/v4.5 — see Universal Rules — but rhythm nouns remain more reliable.)
- **Production-quality descriptors are highly effective in v5:** "radio-ready mix", "punchy drums", "wide stereo field", "crisp high-end", "warm bass"
- **Include mix notes:** register, tone, phrasing, harmony
- **Vocals sound more natural** in v5 — breaths, phrasing, harmonies are authentic
- **Better instrument separation** — can request specific instrument prominence
- **Composition-aware architecture** — v5 uses early style/genre info to maintain coherent sections throughout the song
- **Better nuanced interpretation** of complex prompts vs. v4.5
- **Full negative prompting support** — v5 handles in-prompt negatives ("no [element]") more reliably than v4.5's limited support
- **Existing v4/v4.5 prompts often work "even better" on v5** — migration is typically seamless
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

**Confirmed Descriptor Effects (from community research):**

These descriptors produce consistent, predictable results across v5 generations:

| Descriptor | What Suno Produces |
|---|---|
| `atmospheric` | Reverb, space, ambient pads |
| `airy` | Reverb/space on vocals |
| `lo-fi warmth` | Vintage character, low-pass filtering |
| `polished radio-ready` | Clean, modern, commercial mix |
| `raw live recording` | Less processed, room sound |
| `driving` | Forward momentum, energetic basslines |
| `lush` | Layered pads, dense production |
| `punchy` | Low-end presence, tight transients |
| `wide stereo` | Spatial separation |
| `gated drums` | 80s-style drum processing |
| `vintage Rhodes` | More specific/effective than "piano" |

**Three-Pass Layered Prompting (v5 technique):**

For complex songs, build the prompt in three conceptual passes rather than trying to specify everything at once:

1. **Idea pass** — define concept, mood, genre (the style prompt core)
2. **Lyric pass** — write/refine lyrics with structural tags
3. **Performance pass** — add vocal delivery cues, energy tags, dynamics

This separates concerns and prevents overloading any single input field.

**Confirmed Suno behavior (from Gemini analysis of production outputs):**
- "NOLA funk swing" lands as syncopation, not true swing — Suno interprets swing as a syncopation instruction rather than a jazz swing feel
- "Odd time signatures" is consistently ignored in 4/4 rock/metal context — the strong 4/4 pull of rock and metal genres overrides time signature instructions
- Suno adds unscripted guitar solos regularly — expect them even when not requested, especially in rock/metal genres
- Structural/section directions embedded in long style prompts are largely ignored — Suno treats the style prompt as a tonal palette, not a roadmap. Use metatags and the editor for structural control, not the style prompt.

## v5.5 Pro

### Prompt Style: Same as v5 Pro — Crisp Film-Brief

v5.5 is an additive update over v5. It uses the same audio engine, metatags, and character limits. All v5 prompts work identically on v5.5, often with better results. No migration required.

### What Changed

- **Most expressive model yet** -- better at interpreting subtle, nuanced descriptors that v5 would flatten or ignore
- **More varied output** per generation -- generate 3-5 versions and pick the standout; the spread between "best" and "average" is wider
- **v5.5-optimized prompts can be more specific:** where v5 would use simpler terms like "808s, hi-hats," v5.5 responds well to granular detail: "deep sub 808s, glitchy hi-hat rolls, pitched vocal chops"
- 48kHz sample rate, up to 8 min generation, internal codename "chirp-fenix" (v5 was "chirp-crow")
- **Workflow paradigm shift:** v5.5 encourages generate -> inspect -> replace sections -> refine (not regenerate from scratch)

### v5.5 New Features

**Voices (replaces Personas):**
- Actual voice cloning from a 15s-4min audio sample with anti-deepfake verification
- Pro/Premier only
- **Skill Level dropdown** (Beginner/Intermediate/Advanced/Professional): NOT cosmetic — actively reshapes model interpretation. **Always select Professional** regardless of actual singing ability. Testing confirmed Professional produces the most stable, consistent results across every test.
- Drop gender descriptors ("male vocals", "female singer") when using Voices -- the Voice already defines these, freeing characters for production detail
- Audio Influence for Voices varies by goal (higher than the 25% default for Personas). Independent testing (JG BeatsLab, March 2026) found the practical ceiling is lower than Suno's UI suggests — at 85%, resemblance only reached ~70% with increasing artifacts:

  | Goal | Range | Notes |
  |------|-------|-------|
  | Voice as subtle flavor | 30-40% | Gentle influence, maximum generation polish |
  | Balanced voice + quality | 40-60% | **Recommended starting point** — recognizable with manageable artifacts |
  | Identity-focused | 60-70% | Quality trade-off begins here |
  | Maximum fidelity (caution) | 70-80% | Diminishing returns; artifacts increase faster than resemblance |

  Start at 50% and iterate in 5-10% increments. Pushing above 70% is counterproductive.
- Pairs well with delivery metatags (`[Whispered]`, `[Belted]`, `[Breathy]`, `[Raspy]` etc.) -- Voice sets *who* sings, metatags set *how*
- **Style Personas are NOT gone** — they are integrated into the Voices tab in v5.5. The button changed, but both features coexist. Personas still work on v4.5/v5/v5.5. Key difference: Voices is actual voice cloning, Personas is style essence capture.

**Getting the best voice clone:**
- **Clean recording matters** -- minimal background noise, no heavy reverb. The cleaner the input, the better the clone.
- **Provide vocal range** -- include both lower and higher register in your sample. Monotone input = monotone output.
- **Natural delivery** -- Suno captures your natural vocal tone, not a performance. Sing or speak normally.
- **Multiple samples help** -- one clip works, but three clips across different moods works better for capturing range and character.

**Custom Models:**
- Train on 6+ original tracks, 2-5 min training time, up to 3 custom models per account
- Pro/Premier only
- Drop generic production descriptors your model already knows -- if your Custom Model was trained on lo-fi indie tracks, you don't need "lo-fi warmth" in every prompt
- Think of Custom Model as "producer" and the prompt as "songwriter" -- the model brings the sonic palette, the prompt brings the creative direction
- Train separate models for separate styles -- mixing genres in training data confuses the model

**Training Data Best Practices:**
- **Format:** WAV at 44.1kHz preferred. Heavily compressed MP3 at low bitrates introduces artifacts that interfere with feature extraction.
- **Loudness:** System auto-normalizes (RMS leveling, DC offset removal, spectral masking, onset detection, key/scale estimation). Dynamic range preservation matters more than loudness — streaming-standard ~-14 LUFS is a reasonable baseline. Over-limited/brick-wall-mastered tracks may lose the dynamic character the model is trying to learn.
- **Quantity:** Minimum 6 tracks. 8-12 stylistically consistent tracks is the inferred sweet spot. No documented upper limit. Emphasis from all sources is on stylistic consistency over quantity.
- **Length:** Full-length tracks (3-5 minutes) provide richer training data for arrangement pattern learning. Short clips may not contain enough structural variety.
- **Quality:** Clean, well-mixed audio with minimal background noise and no heavy reverb. The system isolates vocals from mixed audio automatically, but acapella recordings may yield higher quality vocal style capture.

**Overfitting Mitigation:**
- Training data too narrow/homogeneous causes repetitive output with reduced variety
- Include variety within your chosen style lane — different tempos, moods, arrangements, instrumentation variations
- Overly detailed prompts + tightly-trained Custom Model = 'narrow and repetitive as if the AI has fewer options'
- Keep prompts shorter/simpler when using a well-trained Custom Model — it already knows your baseline

**Retraining (documentation gap):** No sources provide clear guidance on updating existing models, deletion workflow, or whether retraining from scratch produces different results. The 3-model limit serves as both a practical constraint and a platform retention mechanism.

Sources: [Custom Models — Suno Help](https://help.suno.com/en/articles/11362497) | [Blake Crosley: Suno Definitive Reference](https://blakecrosley.com/guides/suno) | [AudioNewsRoom: Suno v5.5](https://audionewsroom.net/2026/03/suno-v5-5-what-you-give-up-to-make-it-yours.html)

- **Voice + Custom Model is the most powerful combo:** who sings (Voice) + what style (Custom Model) + detailed prompt (creative direction)
- **Privacy/consent note (AudioNewsRoom):** The consent required to use Voices and Custom Models grants Suno permission to use your data for training their global models. This is NOT optional and NOT a private silo — you are uploading your creative fingerprint to their infrastructure.

**Voices limitations:** Voices is directional influence, not true vocal reproduction — the output drifts across generations and lacks true identity consistency (JG BeatsLab testing). Realistic for demo vocals, pre-production emotional direction, and hearing yourself in new compositions. **Not suitable for** spoken word/narration (Voices drifts toward singing patterns, inconsistent tone between sections, unnatural pacing in longer spoken passages — Suno remains music-first).

**My Taste:**
- Passive personalization that shapes generation defaults based on your listening/generation history
- All tiers (including free), enabled by default
- Takes 20-30 generations to show noticeable influence
- **Magic wand / Style Augmentation:** Click the **magic wand icon** next to the style input in the Create form — Suno auto-generates a personalized style description from your My Taste profile. This is the primary way My Taste manifests.
- **Detailed manual prompts always override My Taste** — if you provide your own style prompt, My Taste is subordinate
- **Controls:** Avatar menu > "My Taste" to view, edit, or disable. No documented reset mechanism beyond disabling.

### v5.5 Personalization Stack

Layers from broadest to most specific:
1. **My Taste** -- shapes generation defaults passively
2. **Custom Model** -- sets production DNA and sonic identity
3. **Voice** -- applies a specific vocal tone and character
4. **Prompt** -- steers the specific song (always the most important layer)

### Tips

- All v5 Pro tips above still apply -- v5.5 is additive, not a replacement
- Lean into specificity: replace broad descriptors with granular ones where you have a clear sonic vision
- When using Voices, reallocate the characters you save from dropping gender/vocal descriptors toward production detail
- When using Custom Models, reallocate the characters you save from dropping generic production descriptors toward song-specific creative direction
- The generate -> replace sections -> refine loop is more efficient than regenerating from scratch on v5.5

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

1. **Character limits** — v4 Pro: 200-char hard limit. v4.5+/v5/v5.5: 1,000-char hard limit (API confirmed). All silently truncated at their respective limits.
2. **Critical zone (first ~200 chars)** — front-loaded terms have the strongest influence on generation. Front-load all essential genre, mood, and vocal descriptors within the first ~200 characters. Content beyond ~200 chars is supplementary but not wasted — it adds nuance and specificity. v5.5's improved descriptor interpretation may extend the effective window beyond 200 chars. A concise 100-char prompt can outperform a cluttered 200-char one, but a well-crafted 250-char prompt with specific descriptors can outperform a generic 150-char one. This is a priority guide, not a character limit.
3. **Word order is weighted** — front-loaded terms dominate generation. Priority order: Genre → Mood/Energy → Instruments → Vocals → Production. Whatever appears first sets the primary sound; everything after is progressively more "flavoring."
4. **5-8 descriptors is the sweet spot** (HookGenius 1000+ prompt analysis, April 2026) — fewer than 4 produces generic results; exceeding 10 causes conflicting signals and quality degradation. Each descriptor should earn its place.
5. **Hyper-specific beats generic** — "1980s synth-pop" not "pop"; "distorted electric guitar, power chords" not "guitar." Era descriptors instead of artist names: "late 70s disco" not an artist name.
6. **Genre and mood always go first** — they're the strongest signal (see rule 3)
7. **Never put style cues inside lyrics** — style prompt and lyrics are separate inputs
8. **No asterisks or special formatting** in style prompts
9. **Never put artist names in style prompts** — Suno does not reliably replicate named artists. Decompose references into concrete sonic descriptors instead.
10. **Negative/exclusion prompts go at the END of the style prompt** — positive descriptors first, cleanup last. "no [element]" is the most reliable in-prompt phrasing. Alternatively, use the separate Exclude Styles field. v5 handles in-prompt negatives better than v4.5.
11. **Comma separation works across all models** — consistent delimiter
12. **Describe, don't command** — "dreamy shoegaze with female vocals" over "Create a dreamy shoegaze song." (v4.5 examples use "Create a..." which matches Suno's own v4.5 docs, but descriptive style generally works better.)
13. **Production tags are the most underused category** (HookGenius analysis) — adding even one production descriptor ("radio-ready mix", "punchy drums", "wide stereo") meaningfully improves output distinctiveness. Most users rely only on genre + mood.
14. **"Cinematic" is a universal quality modifier** — HookGenius's 1000+ prompt analysis found it consistently elevates production quality across every tested genre. Most versatile single tag for enhancing output. (Note: in guitar/bass-led arrangements, "cinematic" can pull keyboard/synth — see Dangerous Words above.)
15. **Conflicting tags produce bland compromise** — "aggressive, peaceful" or similar contradictions cause Suno to default to a generic middle ground, not an interesting hybrid. Opposing descriptors cancel out.
16. **Callback phrasing during Replace Section** — when using Replace Section or Extend, re-inject genre/mood and use callback phrases like "continue same chorus energy" every 1-2 extends to prevent drift.
13. **BPM in style prompts — model-dependent** — on v4/v4.5, BPM tags have zero detectable effect on Suno's output (confirmed by librosa analysis: songs tagged 60 BPM were delivered at 95.7 BPM; songs tagged 65-150 BPM across sections were delivered at a steady 123 BPM). On v5, BPM and key in the style prompt may be more effective than lyric tags (e.g., `"deep house, 122 BPM, A minor, hypnotic groove"`), though rhythm nouns remain more reliable for most use cases. Suno still picks its own tempo based on genre context and arrangement.
14. **Use rhythm nouns for tempo feel** — "halftime groove," "double-time driving," "shuffle," "breakbeat" lock rhythmic feel far more reliably than BPM numbers or tempo adjectives like "slow" or "fast." These describe specific drum patterns Suno can interpret.
15. **Perceived tempo is controlled through lyrics, not the style prompt** — Suno delivers a single steady BPM per song. Perceived tempo changes come from lyrical density (short fragmented lines = slower feel, packed lines = faster feel), arrangement dynamics (instrument dropout = slower feel), and half-time/double-time drum patterns. The style prompt can request rhythm nouns and "tempo changes" as priming, but the actual perceived control lives in the lyrics field.

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

### Era Tags as Sonic Targets

Era-specific descriptors in the style prompt give Suno a production aesthetic target that single descriptors can't match. Use instead of artist names to evoke a period's sound.

| Era Tag | What Suno Produces | Notes |
|---|---|---|
| `80s synth` | Analog synthesizers, gated reverb, drum machines | Pairs well with synthwave, new wave |
| `90s grunge` | Distorted Seattle-sound guitars, raw production | Alternative rock territory |
| `90s hip-hop` / `90s boom bap` | Golden age sampling, hard drums, vinyl texture | Classic hip-hop production |
| `90s R&B` | New jack swing era production | Smooth, polished, Motown-adjacent |
| `2000s emo` | MySpace-era emotional rock | Pop punk, confessional |
| `2010s trap` | Atlanta trap wave, 808s, hi-hats | Modern hip-hop production |
| `60s psychedelic` | Summer of love sound, analog warmth | Reverb-heavy, experimental |
| `70s disco` / `70s soul` | Dance floor funk, Blaxploitation-era warmth | Groove-heavy, warm production |
| `vintage` / `retro` | General throwback sound | Broad — pair with a decade for specificity |

**Practical rule:** Era tags are stronger than individual production descriptors. `90s R&B` achieves more than listing "smooth, warm, polished, swing drums" individually. Combine era tags with genre for maximum precision: `90s boom bap, conscious rap` or `80s synth, darkwave`.

### Dangerous Words and Keyboard Triggers

Certain words reliably pull Suno into unwanted instrumental territory — typically theatrical, keyboard/synth-heavy, or cinematic-light arrangements. Avoid these when guitars and bass should lead.

| Word/Phrase | What Suno Does | Fix |
|---|---|---|
| `baroque` | Maps to theatrical/classical keyboard territory — Disney-adjacent | Describe Baroque qualities without the word: Bach counterpoint = `intricate interlocking guitar and bass melodies`; minor key ornamentation = `dark minor key, precise and ornate` |
| `orchestral`, `orchestral accents` | Defaults to light/cinematic strings, not heavy | Specify HEAVY orchestral instruments explicitly: `cello, heavy strings, kettle drums` — these live in metal's frequency range |
| `cinematic` | Pulls keyboard/synth-heavy arrangements | Use `dynamic shifts`, `building from gentle to crushing` instead |
| `rock opera` | Pulls keyboard/synth-heavy, theatrical arrangements | Use `power ballad`, `dynamic shifts`, `building from gentle to crushing` instead |

**"Baroque" workaround in detail:** If the song concept calls for Baroque-influenced metal, never use the word. Instead, describe the specific qualities you want — `intricate interlocking guitar and bass melodies` for counterpoint, `dark minor key, precise and ornate` for ornamentation. For orchestral weight, specify instruments that live in metal's frequency range: `cello, heavy strings, kettle drums`. Avoid `orchestral` as a standalone descriptor.

## Exclude Styles Field

The Exclude Styles field (Pro/Premier only) is a separate input from the style prompt. Key behaviors:

- **Functions as probability reduction, not a hard ban** — excluded elements are less likely but can still appear. Treat it as strong guidance, not a guarantee.
- **In-prompt negatives also work:** "no [element]" at the end of the style prompt is an alternative or supplement. v5 handles these more reliably than v4.5.
- **Limit to 2-3 most important exclusions** — too many exclusions destabilize the arrangement and produce unpredictable results. Prioritize the exclusions that matter most for the song.
- **Combine with positive instructions** — telling Suno what you DO want is more reliable than only excluding what you don't. Use Exclude Styles as a safety net alongside positive vocal/instrument guidance in the style prompt.

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

### Instrument Bleed-Through

The style prompt sets a GLOBAL instrument palette. Instruments mentioned anywhere in the style prompt bleed into ALL sections regardless of section-level `[Instrument: ...]` tags. This is a fundamental Suno limitation:

- Section-level `[Instrument: ...]` tags CANNOT introduce instruments not in the style prompt — they can only emphasize instruments already in the palette
- Adding "accents" after instrument names (e.g., "brass accents") reduces but does not eliminate bleed
- Placing section-specific instruments at the very END of the prompt minimizes but does not prevent bleed
- **Recommended workflow for section-specific instrumentation:** (1) Generate with all instruments in the prompt (accepting bleed), (2) Extract stems (Suno Pro splits into up to 12 stems including a dedicated brass stem), (3) Mute/remove unwanted instrument stems per section in a DAW like Audacity
- **Note:** External DAW editing is a one-way operation — once you edit outside Suno, you lose Suno's editing capabilities on that version

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

**Weirdness is strongest during Extend and Bridge generation** — this is the primary cause of style drift in extended tracks. High Weirdness during Extend is more destabilizing than during initial generation. Keep Weirdness conservative during Extend operations; too-high Weirdness during Replace Section can also cause Persona/Voice identity shifts. Use callback phrasing ("continue same chorus energy") and re-inject genre/mood every 1-2 extends to prevent drift.

**Style Influence above ~80 plateaus** — increasing further rarely improves genre accuracy, and can reduce vocal phrasing variation especially in vocals.

## Persona Style Prompt Integration

The Persona auto-populates the Style of Music field. Song-specific prompts should **build on** this base, not replace it. The Style Prompt Builder should assume the Persona's Styles content is already present and add song-specific elements on top. The Persona's Styles field contains universal band DNA — the sonic identity that should be consistent across all songs. Song-specific elements (odd time signatures, tempo changes, brass accents, genre departures) get layered per-song on top of that foundation.

### Persona Interaction Guidelines

- **Edit the auto-filled Style of Music intentionally** — the Persona populates it, but don't just leave it and pile on. Review and trim.
- **Keep style simple when Persona is active:** 1-2 genres, 1 mood, 2-4 instruments max. The Persona already carries vocal identity and character — the style prompt is the producer brief, not the artist identity.
- **Change ONE variable at a time** — adjust either the music direction OR the Persona settings, not both simultaneously. This isolates what's working vs. what's not.
- **Mental model:** Persona = artist identity (vocals, character); Style prompt = producer brief (sonic direction for this specific song).

### Voices Interaction Guidelines (v5.5, replaces Personas)

In v5.5, **Voices** succeeds Personas for vocal identity. Voices is actual voice cloning (from a 15s-4min audio sample with anti-deepfake verification), while Personas is style essence capture from a source generation. **Style Personas are NOT gone** — they coexist within the Voices tab in v5.5. Both features work on v5.5; Personas also work on v4.5/v5.

- **Drop gender descriptors when using Voices** — "male vocals", "female singer", etc. are redundant because the Voice already defines these. This frees characters for production detail.
- **Audio Influence for Voices is use-case dependent** — start at 40-60% for balanced voice + quality. Go higher (60-70%) if voice identity is paramount, lower (30-40%) if voice is just flavoring. Do not exceed 70% without accepting quality trade-offs — see the Voices Audio Influence table in the v5.5 Pro section above.
- **Pairs well with delivery metatags** — `[Whispered]`, `[Belted]`, `[Breathy]`, `[Raspy]` etc. Voice sets *who* sings, metatags set *how* they deliver each section.
- **15s-4min audio sample required** plus anti-deepfake verification (you must prove you own or have rights to the voice).

### Custom Model Interaction Guidelines (v5.5)

Custom Models let you train Suno on your own tracks to establish a production DNA. Think of the Custom Model as "producer" and the prompt as "songwriter."

- **Drop generic production descriptors your model already knows** — if your Custom Model was trained on lo-fi indie tracks, "lo-fi warmth" is redundant in every prompt. Use those characters for song-specific direction instead.
- **Train separate models for separate styles** — mixing genres in training data confuses the model. A "dark electronic" model and an "acoustic folk" model will each outperform a single model trained on both.
- **Voice + Custom Model is the most powerful combo** — who sings (Voice) + what style (Custom Model) + detailed prompt (creative direction). This is the full v5.5 personalization stack in action.

**Prompt strategy shift with Custom Models:**
When a Custom Model is active, the priority order changes from genre-first to **mood/production-first** since genre is already encoded in the model. Simpler, more natural-language prompts may produce better results than highly detailed tag-heavy prompts because the model already handles foundational style characteristics.

**Optimal formula with Custom Models:** MOOD + PRODUCTION TEXTURE + ENERGY/TEMPO + SPECIFIC INSTRUMENTS + VOCAL DIRECTION

**What becomes redundant:** Base genre tags, broad stylistic descriptors matching training data, foundation-level production characteristics. Use that freed prompt budget for mood modifiers, production specifications, and contextual modifiers like 'cinematic', 'anthemic', 'intimate'.

- **Privacy/consent note:** Voices and Custom Models consent grants Suno permission to use your data for training their global models. Not optional, not a private silo.

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

**Note on Voices (v5.5):** Voices replaces Personas in v5.5. Because Voices is actual voice cloning rather than style essence capture, it carries less era bias than Personas -- the Voice contributes vocal tone without dragging production aesthetics from a source song. This makes Voices more flexible for era-specific work.

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

## Community Research Sources

> **Last updated:** April 6, 2026. These informed the v5.5 findings above. Verify against current Suno behavior.

- [HookGenius: 1000+ Prompt Analysis](https://hookgenius.app/learn/suno-style-tag-research/) — Tag count sweet spot (5-8), "cinematic" modifier, production tag findings, conflicting tag behavior
- [JG BeatsLab: Voices Day One Testing](https://www.jgbeatslab.com/ai-music-lab-blog/suno-v5-5-voices-tested) — Voices Audio Influence real-world ranges, Skill Level dropdown
- [AudioNewsRoom: Voices/Custom Models Consent](https://audionewsroom.net/2026/03/suno-v5-5-what-you-give-up-to-make-it-yours.html) — Privacy analysis
- [JackRighteous: Creative Control Sliders](https://jackrighteous.com/en-us/blogs/guides-using-suno-ai-music-creation/creative-control-sliders-suno-v5) — Genre-specific slider ranges, Extend drift findings
- [Suno Official v5.5 Docs](https://help.suno.com/en/articles/11362305) — What's New, Voices, Custom Models, My Taste
