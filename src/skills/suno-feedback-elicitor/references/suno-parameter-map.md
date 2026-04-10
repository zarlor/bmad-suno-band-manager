# Suno Parameter Map

> **Related references:** For the complete delivery metatag catalog, section tag behavior, and experimental tags, see `suno-lyric-transformer/references/metatag-reference.md`. For section emotional roles and poem-to-song structure decisions, see `suno-lyric-transformer/references/section-jobs.md`.
>
> **Critical zone:** The first ~200 characters of a style prompt carry disproportionate influence on generation. When recommending additions, prioritize the most impactful descriptors for the critical zone. Supplementary descriptors go after.
>
> **Last validated:** April 6, 2026 (Suno v5.5, v5, v4.5-all). Updated with corrected Voices Audio Influence ranges (JG BeatsLab testing), Weirdness-during-Extend drift finding, callback phrasing for Replace Section, Style Influence plateau note. Recommendations are based on these model versions — newer models may respond differently.

Maps feedback dimensions and emotional vocabulary to concrete Suno parameter adjustments.

## Voices & Custom Models

### Voices (User-Uploaded Vocal Identity)

When the user has a Voice active, the Voice provides the vocal identity (timbre, character, tone). Vocal *delivery* adjustments should use **delivery metatags** in the lyrics field, NOT style prompt vocal descriptors.

| Adjustment | Use This (Delivery Metatag) | NOT This (Style Prompt) |
|------------|----------------------------|------------------------|
| Softer delivery | `[Whispered]`, `[Soft]` | "whispered vocals" in style prompt |
| Powerful delivery | `[Belted]`, `[Powerful]` | "powerful singing" in style prompt |
| Emotional delivery | `[Tender]`, `[Yearning]` | "emotional vocals" in style prompt |
| Aggressive delivery | `[Aggressive]`, `[Screamed]` | "aggressive vocal style" in style prompt |

**Audio Influence with Voices — use-case dependent:**

Independent testing (JG BeatsLab, March 2026) found the practical ceiling is lower than Suno's UI range suggests. At 85%, voice resemblance only reached ~70% with increasing shimmer and vocal artifacts. Pushing the slider highest produces worse professional quality, not better.

| Goal | Range | Notes |
|------|-------|-------|
| Voice as subtle flavor | 30-40% | Gentle influence, maximum generation polish |
| Balanced voice + quality | 40-60% | **Recommended starting point** — recognizable with manageable artifacts |
| Identity-focused | 60-70% | Quality trade-off begins here |
| Maximum fidelity (caution) | 70-80% | Diminishing returns; artifacts increase faster than resemblance |

Start at 50% and iterate in 5-10% increments based on feedback. Do not exceed 70% without accepting significant quality trade-offs.

### Custom Models (User-Trained Production Models)

When the user has a Custom Model active, the model has learned a production DNA from its training catalog. Generic production adjustments (e.g., "polished production," "raw mix") may have little effect because the model defaults to its trained production style.

| Feedback | Standard Approach (May Not Work) | Custom Model Approach |
|----------|----------------------------------|-----------------------|
| "Production is too heavy" | "lighter production" | Name the specific element: "reduce distorted guitar layers, more acoustic presence" |
| "Mix sounds wrong" | "better mix" | Target specifics: "push vocals forward, pull back drum room reverb" |
| "Doesn't sound like my style" | Adjust style prompt broadly | Retrain model with better-curated catalog; use more specific prompt overrides |

**Key principle:** Adjustments need to be MORE specific to override a Custom Model's defaults. Generic descriptors get absorbed by the model's learned tendencies.

### Voice + Custom Model Combined

When both a Voice and a Custom Model are active, change **ONE variable at a time** to isolate what moved. Changing the style prompt, Voice delivery metatags, and Audio Influence simultaneously makes it impossible to determine which change caused the result.

**Isolation sequence:**
1. Adjust delivery metatags first (least disruptive — only changes vocal performance)
2. Then adjust Audio Influence if voice fidelity is the issue
3. Then adjust style prompt if the production/arrangement needs changing
4. Regenerate and evaluate after each single change

## v5.5 Workflow Paradigm

v5.5 favors an iterative **generate -> inspect -> section replace -> refine** workflow over full regeneration. This preserves good material and spends fewer credits.

### Recommended v5.5 Workflow

1. **Generate** the initial output from the song package
2. **Inspect** the full result — evaluate structure, melody, emotional angle, and production
3. **Section replace** any sections that need work (preserve sections that are good)
4. **Refine** with targeted adjustments (delivery metatags, slider tweaks, specific prompt edits)

### Critical Checkpoint Questions

Before spending credits on regeneration or further iteration, ask:

- **Is the structure correct?** If yes, do NOT regenerate from scratch — use section replacement.
- **Is the melody usable?** A good melody with flawed production is worth refining. A bad melody needs regeneration.
- **Does the emotional angle justify more credits?** If the song is fundamentally heading in the right direction, refine. If the emotional core is wrong, regenerate.

### When to Use Section Replacement vs. Full Regeneration

| Situation | Recommendation |
|-----------|---------------|
| Structure and melody are good, one section has bad vocals | Section replacement |
| Structure is good, multiple sections need different fixes | Sequential section replacements |
| Melody is wrong throughout | Full regeneration |
| Overall vibe/genre is off | Full regeneration with revised style prompt |
| Good material but wrong emotional direction | Full regeneration — emotional direction is global |

## Style Prompt Mechanics

### Genre Keyword Ordering

Front-loaded terms in the style prompt dominate generation output — the first ~200 characters are the critical zone. When feedback suggests a genre element is too dominant, move that keyword later in the prompt rather than removing it. For secondary influences, use softening formulations like "with [genre] accents" or "[genre] undertones" to reduce their weight without eliminating them.

### Dynamic Arc Mismatch

When the user reports that the ending or energy arc doesn't match their intent, the style prompt likely contains unidirectional language that only describes one direction of movement. The style prompt must describe the full arc.

| Feedback Pattern | Style Prompt Problem | Fix |
|-----------------|---------------------|-----|
| "Too loud at the end" | "crescendo dynamics" or similar build-only language | Replace with "dynamic shifts loud to quiet" |
| "Builds but doesn't resolve" | "build to climax" with no release language | Replace with "slow build then fade" |
| "Ending stays loud despite descent language" | Dynamic descent stated only once | A single mention of descent isn't enough — Suno latches onto the loudest directive. State the arc TWICE: both `building from gentle to crushing then returning to gentle` AND `dynamic arc quiet to massive to quiet` |
| "All one energy level" | No dynamic language at all | Add explicit dynamic descriptors: "dynamic shifts", "quiet verses explosive chorus", etc. |

### Perceived Tempo Control (BPM Tags Are Ineffective)

**BPM tags in lyrics have ZERO detectable effect on Suno's actual output** — confirmed by librosa analysis across 31 songs. Suno picks a single steady tempo per song regardless of any BPM tags. Do not recommend BPM tags in lyrics as a solution for tempo issues.

**v5 alternative:** BPM and key specified in the style prompt (not lyrics) may be more effective in v5: e.g., `"deep house, 122 BPM, A minor, hypnotic groove"`. This is not confirmed as reliable but is worth trying when perceived tempo techniques alone are insufficient.

**"Felt BPM" vs. measured BPM:** When users report tempo issues, their perception reflects felt BPM (human-perceived tempo), not what librosa measures. librosa has genre-specific biases: reads half-time on speed metal (~50% of actual), double-time on doom/sludge (~200% of actual). ~19% of tracks have significant misreads. Always interpret tempo feedback against felt BPM and genre context, not raw librosa numbers.

When the user reports tempo issues, the recommended adjustment path uses perceived tempo techniques:

1. **Word/line density (PRIMARY):** Restructure lyrics — short fragmented lines (1-3 words) for slower perceived delivery, long packed lines with many syllables for faster perceived delivery. This is the most reliable single technique.
2. **Half-time / double-time drum feel:** Add rhythm noun metatags like `[Heavy: halftime]` or `[Double Time]` in the lyrics. Creates perception of halved or doubled tempo without actual BPM change.
3. **Instrumental density / arrangement dropout:** Use `[Energy: stripped, minimal]` to create space that feels slower. Use `[Energy: massive]` for density that feels faster.
4. **Line breaks as breath points:** More line breaks = more pauses = slower perceived delivery. Fewer breaks = longer phrases = faster feel.
5. **Rhythm nouns in style prompt:** "Halftime groove," "double-time driving," "shuffle," "breakbeat" lock feel better than "slow," "fast," or "upbeat."

Try restructuring the lyrics first (techniques 1 and 4) before modifying the style prompt or metatags.

## Descriptor Families as Adjustment Targets

Beyond `[Mood: ...]`, `[Energy: ...]`, `[Vocal Style: ...]`, and `[Instrument: ...]`, these additional descriptor families are available as adjustment targets in the lyrics field:

| Descriptor Family | Examples | Use When Feedback Says |
|-------------------|---------|----------------------|
| `[Atmosphere: ...]` | `[Atmosphere: Dreamy]`, `[Atmosphere: Cyberpunk]`, `[Atmosphere: Medieval]` | "The vibe/setting feels wrong", "needs more atmosphere" |
| `[Texture: ...]` | `[Texture: Grainy]`, `[Texture: Velvet]` | "The sound quality/feel is wrong", "too smooth/rough" |
| `[Effect: ...]` | `[Effect: Lo-fi]`, `[Effect: Reverb: Hall]`, `[Effect: Delay: Ping-pong]`, `[Effect: Distortion]`, `[Effect: Sidechain]`, `[Effect: Radio Filter]` | "Too much/little reverb", "needs effects", "too dry/wet" |

These families provide more targeted control than style prompt descriptors alone. Place them before the section they should affect.

## Parameterized Section Tags

Section tags can include per-section arrangement instructions using colon (`:`) or pipe (`|`) syntax. This enables per-section fixes without changing the overall style prompt.

```
[Verse: whispered vocals, acoustic guitar only]
[Chorus: full band, powerful vocals]
[Bridge: stripped back, piano only]
[Chorus | Half-Time]
[Chorus | Double-Time]
```

| Feedback | Parameterized Section Tag Fix |
|----------|-------------------------------|
| "The verse is too loud/busy" | `[Verse: stripped back, minimal arrangement]` |
| "The chorus doesn't hit hard enough" | `[Chorus: full band, powerful vocals, high energy]` |
| "The bridge needs a different feel" | `[Bridge: acoustic guitar only, intimate]` |
| "The chorus tempo feels wrong" | `[Chorus | Half-Time]` or `[Chorus | Double-Time]` |

This is often more effective than global style prompt changes when the issue is section-specific.

## Inline Performance Modifiers

Parenthetical cues placed after lyric lines control vocal delivery on a per-line basis. Distinct from the backing-vocal parentheses technique — these are performance directions.

```
I can't stop thinking about you (breathy)
HOLD ON (belt)
wait for me... (breath)
stay with me (hold)
```

| Feedback | Inline Modifier |
|----------|----------------|
| "Vocals too forceful on this line" | Add `(breathy)` or `(soft)` after the line |
| "This line needs more power" | Add `(belt)` after the line |
| "Needs a pause/breath feel here" | Add `(breath)` after the line |
| "The note should sustain longer" | Add `(hold)` after the line |

Use sparingly — these are line-level adjustments, not section-level.

## Confirmed Descriptor Effects

These style prompt descriptors have confirmed, predictable effects on Suno output:

| Descriptor | Produces |
|-----------|----------|
| "atmospheric" | Reverb, space, ambient pads |
| "airy" | Reverb/space on vocals |
| "lo-fi warmth" | Vintage character, low-pass filtering |
| "polished radio-ready" | Clean, modern, commercial mix |
| "raw live recording" | Less processed, room sound |
| "driving" | Forward momentum, energetic basslines |
| "lush" | Layered pads, dense production |
| "punchy" | Low-end presence, tight transients |
| "wide stereo" | Spatial separation |
| "gated drums" | 80s-style drum processing |
| "vintage Rhodes" | More specific/effective than "piano" |

Use these as precise adjustment tools when feedback maps to one of these effects.

## Three-Pass Layered Prompting

For complex adjustments that touch multiple dimensions (arrangement, lyrics, and delivery), use a three-pass approach rather than trying to fix everything at once:

1. **Idea pass** — adjust the concept, mood, and genre in the style prompt
2. **Lyric pass** — revise lyrics with structural tags, section tags, and arrangement cues
3. **Performance pass** — add vocal delivery cues (inline modifiers), energy tags, and dynamics metatags

This reduces the chance of conflicting instructions and makes it easier to isolate which change fixed (or broke) something.

## Style Prompt Adjustment Patterns

### Instrumentation & Arrangement

| Feedback | Add to Style Prompt | Add to Exclusions |
|----------|--------------------|--------------------|
| "Too busy/cluttered" | "minimal arrangement, sparse instrumentation" | "no dense layering, no wall of sound" |
| "Too empty/thin" | "lush arrangement, layered instrumentation, full sound" | — |
| "Guitar too loud" | "subtle guitar, background guitar" | "no guitar solo, no heavy guitar" |
| "Needs more guitar" | "prominent guitar, guitar-driven" | — |
| "Too electronic" | "organic, acoustic, live instruments" | "no synthesizer, no electronic beats" |
| "Too acoustic" | "electronic elements, synth textures, modern production" | — |
| "Drums overpower" | "soft percussion, gentle drums, restrained beat" | "no heavy drums, no pounding drums" |
| "Needs more drums" | "driving drums, prominent beat, rhythmic" | — |
| "Second line drums sound like hip-hop" | "second line drums" only produces NOLA parade groove when the surrounding context is up-tempo + energetic + celebratory. Without that context, Suno defaults to hip-hop patterns. Add "New Orleans parade", "celebratory", "up-tempo" to the style prompt. | — |
| "Piano feels wrong" | — | "no piano" (or specify: "no classical piano") |
| "Bass too heavy" | "light bass, subtle low end" | "no heavy bass, no bass drops" |

**Keyword Triggers to Avoid**

Certain style prompt keywords reliably trigger unwanted arrangement choices. When the user reports theatrical, keyboard-heavy, or orchestral results they didn't want, check for these first.

| Keyword | What Suno Produces | Alternative Approach |
|---------|--------------------|---------------------|
| "baroque" | Disney/theatrical arrangements | Describe desired qualities directly; specify instruments by name |
| "rock opera" | Keyboard-heavy, theatrical arrangements | Use "power ballad" for dynamic range without keyboards |
| "cinematic" | Orchestral/soundtrack feel | Specify desired instruments by name (cello, heavy strings, kettle drums) |
| "orchestral" | Light strings/flutes, not the heavy orchestral sound users typically intend | Name the specific orchestral instruments desired (cello, heavy strings, kettle drums) |

### Vocal Direction

| Feedback | Add to Style Prompt | Add to Exclusions |
|----------|--------------------|--------------------|
| "Vocals too polished" | "raw vocal, imperfect delivery, organic phrasing" | "no perfect pitch, no overproduced vocals" |
| "Vocals too rough" | "polished vocal, smooth delivery, clean singing" | "no raspy vocals, no rough vocals" |
| "Voice doesn't match" | Specify: "male/female voice, [age] years old, [tone] delivery" | Exclude the unwanted: "no [gender] vocals" |
| "Too much vibrato" | "steady vocal, straight tone" | "no heavy vibrato" |
| "Vocals too quiet" | "prominent vocals, voice-forward mix" | — |
| "Vocals too loud" | "balanced mix, instrument-forward" | — |
| "Singing sounds robotic" | "natural phrasing, breathy, human vocal" | "no robotic vocals" |
| "Want harmonies" | "vocal harmonies, layered vocals, backing harmonies" | — |
| "Too much harmony" | "solo vocal, single voice, unison" | "no harmonies, no backing vocals" |

### Energy & Tempo

| Feedback | Add to Style Prompt | Slider Adjustment |
|----------|--------------------|--------------------|
| "Too fast" | "halftime groove, laid-back, relaxed groove" (also restructure lyrics: short fragmented lines, more line breaks — see Perceived Tempo Control above). Do NOT add BPM tags — they have no effect. | — |
| "Too slow" | "double-time driving, driving rhythm, energetic pace" (also restructure lyrics: pack more syllables per line, fewer line breaks — see Perceived Tempo Control above). Do NOT add BPM tags — they have no effect. | — |
| "Not energetic enough" | "high energy, powerful, dynamic, driving" | Style Influence ↓ (loosen) |
| "Too intense" | "gentle, soft, understated, subtle" | — |
| "Energy is flat" | "building energy, dynamic shifts, crescendo" | Weirdness ↑ slightly |
| "Feels monotonous" | "dynamic arrangement, shifting textures, varied sections" | Weirdness ↑ |

### Production & Mix

| Feedback | Add to Style Prompt | Slider Adjustment |
|----------|--------------------|--------------------|
| "Too polished" | "lo-fi, raw production, analog warmth, rough edges" | Weirdness ↑ |
| "Too rough/lo-fi" | "radio-ready mix, clean production, crisp, polished" (v5 responds well to production-quality descriptors like "punchy drums, wide stereo field, crisp high-end, warm bass") | Weirdness ↓ |
| "Sounds compressed" | "dynamic range, open mix, breathing room" | — |
| "Too much reverb" | "dry mix, close mic, intimate" | — |
| "Too dry" | "spacious, reverb, ambient, atmospheric" | — |
| "Stereo feels narrow" | "wide stereo field, panoramic, expansive" | — |
| "Sounds dated" | "modern production, contemporary sound, current" | — |

### Mood & Vibe

| Feedback | Add to Style Prompt | Slider Adjustment |
|----------|--------------------|--------------------|
| "Too happy/upbeat" | "melancholic, bittersweet, minor key, moody" | — |
| "Too dark/sad" | "uplifting, bright, major key, hopeful" | — |
| "Too generic" | "distinctive, unique, unconventional" | Weirdness ↑ (65-80) |
| "Too weird" | "familiar, classic, conventional, straightforward" | Weirdness ↓ (25-35) |
| "Not emotional enough" | "emotional, yearning, deeply felt, passionate" | Style Influence ↑ |
| "Too dramatic" | "understated, subtle, restrained, casual" | — |

## Confirmed Suno Behavior

- "NOLA funk swing" lands as syncopation not true swing; "Odd time signatures" consistently ignored in 4/4 rock/metal context
- Suno adds unscripted guitar solos regularly
- Structural/section directions in long style prompts are largely ignored (style prompt sets overall mood, metatags handle sections imperfectly)

## Exclusion Guidance

Prioritize 2-3 specific exclusions over filling the space. Supported syntax: 'no [element]', 'without [element]', 'exclude [element]', 'avoid [element]'. The Exclude Styles field (Pro/Premier only) and in-prompt negatives both function as **probability reduction, not hard bans** — excluded elements may still appear, and regeneration may be needed. Limit to 2-3 most important exclusions; too many destabilizes the arrangement and reduces overall effectiveness.

## Slider Adjustment Guide

### Weirdness (0-100, default 50) — Paid tiers only

| Current Feel | Direction | Target Range | Reasoning |
|-------------|-----------|-------------|-----------|
| Too generic/predictable | ↑ Increase | 60-80 | More unexpected choices |
| Too strange/unfocused | ↓ Decrease | 25-40 | More conventional, familiar |
| Good but could explore | ↑ Slight increase | +10-15 from current | Nudge toward discovery |

**Observations from live testing (not exhaustive — wider range testing needed):**
- Weirdness 50 (default) produced overly steady/predictable results for multi-tempo songs (note: actual BPM does not change — Weirdness affects rhythmic feel and arrangement variation, not tempo)
- Weirdness 60 improved rhythmic variation
- Weirdness 65 produced the best tempo/rhythm variation in testing so far
- Higher values (70+) have not been tested and may produce interesting results for experimental work
- These observations are from v5 Pro with Style Influence 70 — results may differ on other models
- **Sliders don't control tempo, dynamics, or vocal delivery** — they control predictability (Weirdness) and prompt adherence (Style Influence). Don't recommend them as solutions for tempo/vocal issues.

**Confirmed slider combinations by song type (from production use):**

| Song Type | Weirdness | Style Influence | Notes |
|-----------|-----------|-----------------|-------|
| Structured songs (chorus, clear sections) | 50-55 | 75-80 | Higher SI keeps sections well-defined |
| Through-composed with tempo shifts | 55-60 | 70-75 | Slightly looser to allow tempo variation |
| Funk-forward | 60 | 65-70 | Funk needs room to breathe |
| Post-metal / atmospheric | 60-65 | 65 | Balanced exploration with genre grounding |
| Prog with odd time signatures | 65-75 | 65 | High Weirdness helps with non-standard meters |
| Circular / agitated | 75 | 65 | Near the structural ceiling — use [End] tags |
| Acoustic tracks | 40 | 80 | Audio Influence 25%. Persona safe at full AI when style prompt clearly defines non-heavy genre |
| Bass prominence attempts | Any | High SI (85) did not force bass prominence; low Audio Influence (15%) slightly shifted era feel instead | Bass-forward rock/metal remains a Suno limitation |

**Upper limit findings (from live testing):**
- Weirdness 75 is the practical ceiling for structured songs — still experimental but respects section boundaries and [End] tags
- Weirdness 85 causes structural breakdown: [End] tags ignored, songs continue past lyrics with instrumental/gibberish meandering
- At Weirdness 85, coherence loss increases in longer songs — shorter songs or songs with strong repeating structure (chorus anchors) survive higher Weirdness better
- **Recommendation:** Cap at 75 for songs needing structural compliance. Reserve 80+ for jam/experimental mode only.
- Always use [Fade Out] + [End] combo at high Weirdness values — more reliable stop signal than [End] alone

### Audio Influence (0-100%, default 25%) — Persona-dependent

Audio Influence controls how much the loaded Persona's source audio shapes the generation. This parameter should never be omitted from song packages when a Persona is active.

| Scenario | Recommended Range | Notes |
|----------|-------------------|-------|
| Standard tracks | 25% | Default. Reliable baseline for most genres. |
| Acoustic tracks | 25% | Persona is safe at full Audio Influence when style prompt clearly defines a non-heavy genre. |
| Genre-pushing tracks | 20% | Drop 5% when pushing outside the Persona's native genre to give the style prompt more room. |
| Era mismatch (song sounds too modern/dated) | 10-15% | High Audio Influence anchors to the Persona's era. Reduce to let style prompt control era feel. |

**Effective range is 15-25%.** Above 25% shows diminishing returns — the generation doesn't become noticeably more Persona-like, but style prompt influence decreases. Below 15%, the Persona contributes minimal character.

### Style Influence (0-100, default ~50-60) — Paid tiers only

| Current Feel | Direction | Target Range | Reasoning |
|-------------|-----------|-------------|-----------|
| Doesn't match the prompt | ↑ Increase | 65-80 | Tighter adherence to style prompt |
| Too literal/constrained | ↓ Decrease | 25-40 | More creative interpretation |
| Prompt is vague, output is scattered | ↑ Increase + rewrite prompt | 60-70 | Better prompt + tighter adherence |

**Observations from live testing:**
- Style Influence 70 gave enough room for metal weight while staying in the genre lane
- Lower values (45-65) allowed more creative interpretation on bridges and contrasting sections
- These are observations from limited testing, not definitive optimal values

### Per-Section Slider Strategy (v5 Studio)

v5 Studio enables per-section regeneration. Different slider values can be applied to different song sections:

| Section Type | Weirdness | Style Influence | Reasoning |
|-------------|-----------|-----------------|-----------|
| Verse | 35-50 | 55-70 | Stable foundation, moderate adherence |
| Chorus/Hook | 25-40 | 70-85 | Tighter adherence for memorable hooks |
| Bridge | 55-70 | 45-65 | More exploration for contrast |
| Intro/Outro | 40-60 | 50-65 | Balanced — sets/closes the tone |
| Breakdown | 60-80 | 35-55 | Looser interpretation for texture |

## Model-Specific Feedback Patterns

### v4 Pro
- Hard 200-character style prompt limit (silently truncated) — all adjustment text must be extremely concise
- Simpler model — broad genre/mood descriptors work better than nuanced ones
- No slider control, no Persona support
- If feedback requires more nuance than 200 chars allow, suggest upgrading to v4.5+ or higher (1,000-char limit)

### v4.5-all (Free Tier)
- Limited vocal control — voice issues are harder to fix without Persona
- Conversational style prompts work — can be more descriptive in adjustments
- No slider control — all adjustments must go through style prompt and exclusions
- Suggest trying different generation seeds (make again) before changing prompt

### v4.5 Pro / v4.5+ Pro
- Same prompting behavior as v4.5-all but with slider access and Persona support
- Slider adjustments available — use them before expanding the style prompt
- v4.5+ Pro offers advanced creation methods — section-level control improves with this model
- Personas can lock vocal direction more reliably than style prompt alone

### v5 Pro
- Better vocal nuance — vocal adjustments are more likely to work
- Crisp descriptors respond better — keep style prompt adjustments concise
- Section-level editing available — can adjust specific parts without regenerating
- Warp Markers allow fine-grained timing fixes
- If vocals are the only issue, suggest "Replace Section" or "Add Vocals" before full regeneration

## Lyric-to-Metatag Feedback Patterns

| Feedback | Lyric Adjustment |
|----------|-----------------|
| "Chorus doesn't hit hard enough" | Add `[Energy: High]` before chorus, consider `[Build-Up]` section before it |
| "Verse feels wrong" | Check syllable count consistency, add `[Mood: ...]` descriptor |
| "Song structure feels off" | Review section ordering, consider adding/removing Pre-Chorus or Bridge |
| "Vocals change style mid-song" | Add consistent `[Vocal Style: ...]` tags before each section |
| "Instrumental section too long/short" | Adjust `[Intro]`, `[Breakdown]`, or `[Outro]` tag placement and content |
| "Phrasing feels unnatural" | Run syllable counter, normalize line lengths within sections |

## Audio Quality & Artifacts

Common quality issues that cannot be resolved through style prompt changes alone.

| Feedback | Resolution Path |
|----------|----------------|
| "Sounds robotic/glitchy" | Regenerate (try 3-5 times with same prompt); if persistent, simplify style prompt or switch models |
| "Audio quality drops at the end" | Generate shorter (under 2 min), extend carefully; quality degrades in long generations |
| "Weird artifacts/noise" | Regenerate; if persistent, remove problematic descriptors from style prompt |
| "Pronunciation is wrong" | Add phonetic hints in lyrics, or use `[Spoken Word]` metatag for problem lines |
| "Vocals sound auto-tuned" | Add "natural vocal, organic phrasing, imperfect delivery" to style prompt; add "no auto-tune" to exclusions |
| "Clipping/distortion (unwanted)" | Add "clean mix, headroom, dynamic range" to style prompt; reduce layering descriptors |
| "Frequency mud / sounds muffled" | Add "crisp, clear mix, defined frequencies" to style prompt; v5 Remove FX can help |

**External DAW editing (Audacity, etc.) is a one-way operation** — once you edit outside Suno, you lose Suno's editing capabilities on that version. Always keep the original Suno generation as a source of truth.

**Key principle:** Audio quality issues are often generation-specific, not prompt-specific. Always try regenerating 3-5 times before modifying the prompt. Suno's randomness means the same prompt can produce both clean and artifact-heavy outputs.

## Suno Studio Resolution Paths (v5 Pro / Premier)

When feedback maps to Studio features rather than prompt changes.

| Feedback Pattern | Studio Feature | How |
|-----------------|----------------|-----|
| "The timing feels off in the chorus" | Warp Markers | Adjust timing of specific sections without regenerating |
| "Verse 2 vocals are bad but the rest is great" | Replace Section | Regenerate only the problem section, preserving everything else |
| "I want to hear different versions of the chorus" | Alternates | Generate multiple versions of a specific section and compare |
| "Too much reverb/effects on the vocals" | Remove FX | Strip effects from the vocal track |
| "The vocal melody is great but the lyrics are wrong" | Add Vocals | Re-record vocals over the existing instrumental |
| "I need the instrumental without vocals" | Stems | Extract up to 12 stems including isolated instrumental |
| "The song is great but I want to try different words" | Replace Section + Lyrics edit | Change lyrics for specific sections while preserving melody |

### Additional Studio Capabilities (v5.5)

| Feature | What It Does | Key Limitation |
|---------|-------------|----------------|
| Warp Markers | Fix timing post-generation without pitch shift — correct rushed or dragging sections | Timing adjustment only; does not affect pitch or melody. Artifacts with extreme corrections. |
| Remove FX | Strip reverb/delay from the generation for external DAW processing | One-way: stripping FX is for export. May sound thinner — rebuild space with your own reverb in a DAW. |
| Alternates | Generate 2-6 variations of a section, audition in context, comp the best parts | Single-change alternates prevent losing song identity. |
| EQ | 6-band per-track parametric EQ with 11 presets and spectrum analyzer | Start subtle (+/-3dB). Cut > boost for natural results. |
| Remaster | Polish production (Subtle/Normal/High strength) without changing lyrics or structure | Does NOT change style, vocalist, or arrangement — use Cover for those. |
| Heal Edits | Smooth transitions at edit/cut points | Use after rearranging or replacing sections. |
| Time Signature | Grid/metronome alignment for editing | Editing-only — does NOT affect the generative model. Prompt for desired meter instead. |

**Tier mapping:** Legacy Editor features (Replace Section, Extend, Crop, Fade, Rearrange, Stems, Remaster) are available on **Pro and Premier**. Full Studio features (Warp Markers, Remove FX, Alternates, EQ, Heal Edits, Context Window, Recording, MIDI Export) are **Premier only**. Always check the user's tier before recommending.

**For complete Studio & Editor workflows, tips, and troubleshooting:** See [STUDIO-EDITOR-REFERENCE.md](../../STUDIO-EDITOR-REFERENCE.md).

## Song Length & Pacing

| Feedback | Adjustment |
|----------|-----------|
| "Song is too short" | Use Suno's extend feature; or add sections in lyrics (additional verse, bridge, instrumental break) |
| "Song is too long" | Remove repeated sections in lyrics; trim `[Outro]` content; remove `[Breakdown]` if not essential |
| "Intro goes on too long" | Shorten or remove `[Intro]` lyrics content; add `[Verse 1]` tag earlier; note: `[Intro]` tag is notoriously unreliable |
| "Outro cuts off abruptly" | Add explicit `[Outro]` section with 2-4 lines; add `[Fade Out]` descriptor metatag |
| "Middle section drags" | Add `[Energy: building]` metatags; shorten the dragging section; consider adding a `[Breakdown]` or `[Build-Up]` for variety |
| "Energy drops in extended sections" | Known limitation — 62% of extended tracks drift from original prompt. **Weirdness is strongest during Extend and Bridge generation** — this is the primary drift cause. Keep Weirdness conservative during Extend. Use callback phrasing ("continue same chorus energy") and re-inject genre/mood every 1-2 extends. |

## Genre Drift & Consistency

Genre drift is one of the most common issues — 62% of extended Suno tracks deviate from the original prompt. **The Weirdness slider has the strongest destabilizing effect during Extend and Bridge generation** — high Weirdness during Extend is more disruptive than during initial generation.

| Feedback | Adjustment |
|----------|-----------|
| "Style changed mid-song" | Add consistent genre anchoring via `[Mood: ...]` and `[Energy: ...]` metatags before each section in lyrics |
| "Extended section sounds different" | Regenerate the extension; use v5 Studio Replace Section; keep Weirdness conservative during Extend; use callback phrasing ("continue same chorus energy") and re-inject genre/mood every 1-2 extends |
| "Genre fusion went wrong" | Simplify to single dominant genre; move secondary genre influence to later in style prompt (after critical zone) |
| "Sounds like a different band in the second half" | Add `[Vocal Style: ...]` tags before each section; increase Style Influence slider (65-80) for tighter adherence |
| "Voice/Persona shifted during Replace Section" | Keep Weirdness conservative during Replace operations — high Weirdness can cause Persona/Voice identity shifts |

**Prevention tips:** Front-load genre identity in the first 200 chars of style prompt. Use per-section metatags. Generate 3-5 versions and cherry-pick. For extensions, match the style prompt exactly, keep extensions short (30s-1min increments), and **keep Weirdness lower during Extend than during initial generation**. Use callback phrasing ("continue same chorus energy", "maintain verse mood") to anchor the extension to the existing material.

### Extend Anti-Drift Toolkit

Techniques for maintaining consistency during Extend operations, ordered by effectiveness:

1. **Anchor note restating** — restate genre, mood, key, and instrument palette with each extension in 1-2 sentences. Example: 'Keep the exact current groove, instrument palette, key, and tempo.'
2. **Forbidden element phrasing** — 'No new hooks,' 'No new drums,' 'No new riffs,' 'no risers.' Negative constraints are more effective than positive instruction alone during Extend.
3. **Structural metatag at start** — include `[Chorus]`, `[Bridge]`, `[Outro]` etc. at the beginning of every extension prompt to guide section type.
4. **Energy alignment** — specify energy relative to existing material: 'Bridge energy: 80% of chorus; lower drums...'
5. **Short blocks (30 seconds preferred)** — catch drift before it compounds. Limit to 2-3 extensions maximum per song.
6. **Cover as signal cleaner** — if quality degrades after multiple extensions, use Cover to re-synthesize the audio from scratch, resetting the signal path.
7. **Custom Extend over Quick Extend** — always use Custom Extend for anything you care about. Quick Extend is for rapid prototyping only.

**Verification:** Loop playback at 2x speed to confirm join seams and style consistency.

**Genre-specific outro templates:**
- Gospel/Worship: soft organ and distant choir pad
- Rock/Anthem: final guitar sustain and cymbal swell
- Lo-fi: soft piano motif and vinyl texture
- EDM: filtered synth tail
- Reggae: softening skank guitar

Sources: [Suno 4.5 Plus Extend — Jack Righteous](https://jackrighteous.com/en-us/blogs/guides-using-suno-ai-music-creation/suno-45-plus-extend-tool) | [Outro Prompts — Jack Righteous](https://jackrighteous.com/en-us/blogs/guides-using-suno-ai-music-creation/suno-ai-outro-prompt-guide) | [End Prompts — Jack Righteous](https://jackrighteous.com/en-us/blogs/guides-using-suno-ai-music-creation/suno-ai-end-prompt-guide) | [Fade Out Prompts — Jack Righteous](https://jackrighteous.com/en-us/blogs/guides-using-suno-ai-music-creation/suno-ai-fade-out-prompt-guide)
