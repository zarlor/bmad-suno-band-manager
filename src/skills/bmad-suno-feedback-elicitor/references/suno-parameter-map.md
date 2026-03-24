# Suno Parameter Map

> **Critical zone:** The first ~200 characters of a style prompt carry disproportionate influence on generation. When recommending additions, prioritize the most impactful descriptors for the critical zone. Supplementary descriptors go after.
>
> **Last validated:** March 2026 (Suno v5, v4.5-all). Recommendations are based on these model versions — newer models may respond differently.

Maps feedback dimensions and emotional vocabulary to concrete Suno parameter adjustments.

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

### Word Density as Primary Tempo Control

When the user reports tempo issues, adjusting lyric line density is more reliable than BPM tags. Suno infers pacing from how much text it needs to deliver per section. Sparse, long lines push toward slower delivery; short, packed lines push toward faster delivery. Try restructuring the lyrics before adding tempo descriptors to the style prompt.

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
| "Too fast" | "slow tempo, laid-back, relaxed groove" (also try longer lyric lines — see Word Density above) | — |
| "Too slow" | "uptempo, driving rhythm, energetic pace" (also try shorter, denser lyric lines — see Word Density above) | — |
| "Not energetic enough" | "high energy, powerful, dynamic, driving" | Style Influence ↓ (loosen) |
| "Too intense" | "gentle, soft, understated, subtle" | — |
| "Energy is flat" | "building energy, dynamic shifts, crescendo" | Weirdness ↑ slightly |
| "Feels monotonous" | "dynamic arrangement, shifting textures, varied sections" | Weirdness ↑ |

### Production & Mix

| Feedback | Add to Style Prompt | Slider Adjustment |
|----------|--------------------|--------------------|
| "Too polished" | "lo-fi, raw production, analog warmth, rough edges" | Weirdness ↑ |
| "Too rough/lo-fi" | "radio-ready mix, clean production, crisp, polished" | Weirdness ↓ |
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

Prioritize 2-3 specific exclusions over filling the space. Supported syntax: 'no [element]', 'without [element]', 'exclude [element]', 'avoid [element]'. Exclusions are influential but not absolute — regeneration may still be needed. Too many negatives reduce effectiveness.

## Slider Adjustment Guide

### Weirdness (0-100, default 50) — Paid tiers only

| Current Feel | Direction | Target Range | Reasoning |
|-------------|-----------|-------------|-----------|
| Too generic/predictable | ↑ Increase | 60-80 | More unexpected choices |
| Too strange/unfocused | ↓ Decrease | 25-40 | More conventional, familiar |
| Good but could explore | ↑ Slight increase | +10-15 from current | Nudge toward discovery |

**Observations from live testing (not exhaustive — wider range testing needed):**
- Weirdness 50 (default) produced overly steady/predictable results for multi-tempo songs
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
- Hard 200-character style prompt limit — all adjustment text must be extremely concise
- Simpler model — broad genre/mood descriptors work better than nuanced ones
- No slider control, no Persona support
- If feedback requires more nuance than 200 chars allow, suggest upgrading model tier

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

**Note:** Studio features are available on Premier tier. Some features (Replace Section, Add Vocals) are available on Pro tier. Always check the user's tier before recommending Studio workflows.

## Song Length & Pacing

| Feedback | Adjustment |
|----------|-----------|
| "Song is too short" | Use Suno's extend feature; or add sections in lyrics (additional verse, bridge, instrumental break) |
| "Song is too long" | Remove repeated sections in lyrics; trim `[Outro]` content; remove `[Breakdown]` if not essential |
| "Intro goes on too long" | Shorten or remove `[Intro]` lyrics content; add `[Verse 1]` tag earlier; note: `[Intro]` tag is notoriously unreliable |
| "Outro cuts off abruptly" | Add explicit `[Outro]` section with 2-4 lines; add `[Fade Out]` descriptor metatag |
| "Middle section drags" | Add `[Energy: building]` metatags; shorten the dragging section; consider adding a `[Breakdown]` or `[Build-Up]` for variety |
| "Energy drops in extended sections" | Known limitation — 62% of extended tracks drift from original prompt. Generate shorter and extend carefully, or use v5 Studio section replacement |

## Genre Drift & Consistency

Genre drift is one of the most common issues — 62% of extended Suno tracks deviate from the original prompt.

| Feedback | Adjustment |
|----------|-----------|
| "Style changed mid-song" | Add consistent genre anchoring via `[Mood: ...]` and `[Energy: ...]` metatags before each section in lyrics |
| "Extended section sounds different" | Regenerate the extension; use v5 Studio Replace Section; or tighten style prompt with repeated key genre terms |
| "Genre fusion went wrong" | Simplify to single dominant genre; move secondary genre influence to later in style prompt (after critical zone) |
| "Sounds like a different band in the second half" | Add `[Vocal Style: ...]` tags before each section; increase Style Influence slider (65-80) for tighter adherence |

**Prevention tips:** Front-load genre identity in the first 200 chars of style prompt. Use per-section metatags. Generate 3-5 versions and cherry-pick. For extensions, match the style prompt exactly and keep extensions short (30s-1min increments).
