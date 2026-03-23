# Feedback Triage Guide

> **Last validated:** March 2026. Elicitation techniques are craft-based (not Suno-specific) and do not require frequent re-validation. The Suno parameter mappings in the opposing pairs table should be verified via web search if Suno model behavior has changed since this date.

## Classification Rules

### Clear Feedback
**Signals:** Specific nouns (guitar, vocals, bass, drums, tempo), comparative statements ("too much," "not enough," "louder," "softer"), direct requests ("add," "remove," "change").

**Examples:**
- "The electric guitar is too prominent"
- "I need a bridge between the second chorus and the outro"
- "The vocals sound too autotuned"
- "It's too fast — slow it down"
- "The drums overpower everything"

**Action:** Map directly to parameter adjustments. No elicitation needed.

### Positive Feedback
**Signals:** Approval language ("love it," "great," "perfect," "nailed it"), evolution requests ("can we try," "what if," "now make it"), preservation language ("keep the," "don't change").

**Examples:**
- "This is exactly what I wanted!"
- "Love the vocals — can we try a darker instrumental?"
- "Perfect energy. What about a version with more acoustic guitar?"
- "Keep everything but make the chorus hit harder"

**Action:** Identify what to preserve (anchor), then explore evolution direction. Suggest saving successful elements to band profile.

### Vague Feedback
**Signals:** Feeling-based language without specifics ("off," "not right," "something's missing," "doesn't feel like"), hedging ("I don't know," "hard to explain," "it's just"), negation without alternative ("I don't like it," "that's not it").

**Examples:**
- "Something about it just isn't right"
- "It doesn't feel like what I imagined"
- "I don't know, it's missing something"
- "It's close but not there yet"
- "The vibe is off"

**Action:** Three-phase guided elicitation (binary narrowing → comparative anchoring → emotional vocabulary bridge).

### Contradictory Feedback
**Signals:** Opposing descriptors in same feedback ("more X but also more Y" where X and Y conflict), sequential reversals ("actually no, I want..."), wanting everything changed but nothing changed.

**Examples:**
- "Make it more energetic but also more relaxed"
- "I want it raw and lo-fi but also radio-ready"
- "The vocals should be more prominent but also blend in more"
- "It needs to be simpler but also more interesting"

**Action:** First Principles reset — find the one anchor, rebuild from there. Reframe contradictions as potential structural insights (verse vs. chorus contrast).

### Technical/Quality Feedback
**Signals:** Quality-specific language ("glitchy," "robotic," "artifact," "clipping," "distortion," "cuts off"), timestamp references ("at 1:23"), pronunciation complaints, audio fidelity terms ("muffled," "compressed," "tinny"), generation-specific issues distinct from creative direction.

**Examples:**
- "There's a weird glitch at 1:23"
- "The vocals sound robotic in the second verse"
- "The audio quality drops toward the end"
- "It mispronounces the word 'ethereal'"
- "There's clipping in the chorus"

**Action:** Route to Suno Studio features (Replace Section, Warp Markers, Remove FX) or regeneration. These issues are typically generation-specific, not prompt-specific — try regenerating 3-5 times before modifying the prompt. See suno-parameter-map.md "Audio Quality & Artifacts" and "Suno Studio Resolution Paths" sections.

### Production Diagnostic Patterns

Common feedback patterns with non-obvious root causes. When you hear these, check the indicated sources before adjusting the style prompt.

| Feedback Pattern | Check First | Root Cause & Fix |
|-----------------|-------------|-----------------|
| "Guitar dominates / bass not prominent enough" | Genre context (rock/metal?) + instrumental sections | Bass prominence is a known Suno limitation in rock/metal. Try: remove "guitar" mentions from style prompt, add guitar to exclusions, use `[Instrument: bass]` tags (unreliable but worth trying). Bass-forward rock/metal is currently not achievable reliably. |
| "Ending is too loud / song doesn't come down" | Style prompt for unidirectional build language ("crescendo dynamics", "build to crushing climax") | The style prompt must describe the full arc, not just the build. Replace with `slow build then fade` or `dynamic shifts loud to quiet`. |
| "Wrong bass tone" | Whether "funk" appears in style prompt | "Funk" triggers slap/pop bass (Flea/Claypool style). For overdriven fingerstyle bass (Geddy Lee style), remove "funk" entirely. |
| "Song sounds too modern / wrong era" | Whether a Persona is loaded | Personas anchor sound to the era of the source song. Reduce Audio Influence to 10-15% or generate without Persona for era-specific pieces. |
| "Vocals are screaming when they shouldn't be" | Style prompt for `metal`, `sludge`, `doom`; lyrics for `!` or ALL CAPS | These are scream triggers. Fix: add explicit positive vocal instructions (e.g., "clean vocals, melodic singing"), remove triggers, use `[Vocal Style: whispered]` to reset after aggressive sections. |
| "Song loops / too much instrumental" | Source text length (under 15 lines?) + style prompt for `instrumental breaks` | Short lyrics cause looping and filler instrumentals. Suggest: double the delivery (repeat verses with variation), extract and repeat chorus, or place a hard `[End]` tag. |
| "Sound is too theatrical / too many keyboards" | Style prompt for `baroque`, `rock opera`, `cinematic`, or `orchestral` | These keywords trigger keyboard-heavy theatrical arrangements. Fix: describe desired qualities without those words; specify heavy orchestral instruments by name (cello, heavy strings, kettle drums); use "power ballad" instead of "rock opera" for dynamic range. |
| "Song doesn't come back down / ending stays loud" | Whether the dynamic arc is stated TWICE in the style prompt | A single mention of descent isn't enough — Suno latches onto the loudest directive. Both `building from gentle to crushing then returning to gentle` AND `dynamic arc quiet to massive to quiet` are needed to reliably produce a full arc. |

---

## Elicitation Techniques

### Binary Narrowing
Rapid yes/no or A/B questions to reduce the problem space. Goal: identify which dimension(s) need adjustment in under 5 questions.

**Dimension checklist:**
1. Music/production vs. vocals/singing
2. Energy level (too high / too low / right)
3. Structure (sections, flow, length)
4. Lyrics (content, delivery, phrasing)
5. Overall vibe/mood (right neighborhood or wrong direction)

**Rules:**
- Ask one question at a time
- Accept partial answers — "kind of both" is useful signal
- If they narrow to a single dimension in 2 questions, skip ahead to Phase 2

### Comparative Anchoring
Use reference points the user knows to triangulate what they want.

**Techniques:**
- **Artist/song reference:** "Name a song that has the feel you're going for"
- **Spectrum placement:** "If 1 is [extreme A] and 10 is [extreme B], where is it now and where do you want it?"
- **A/B contrast:** Suggest two contrasting descriptions and ask which is closer to their vision
- **Temporal reference:** "Think of the last song that made you feel the way this one should — what was it?"

**Rules:**
- Don't require musical knowledge — "a movie scene" or "a feeling" works too
- If they give a reference, decompose it into concrete audio characteristics (instrumentation, tempo, vocal style, production quality, energy)

### Emotional Vocabulary Bridge
Map subjective feelings to Suno-actionable parameters.

**Core opposing pairs and their Suno parameter mappings:**

| Pair | Low End → Suno | High End → Suno |
|------|----------------|-----------------|
| Heavy ↔ Light | Dense instrumentation, layered, bass-heavy, thick | Sparse arrangement, airy, minimal, delicate |
| Fast ↔ Slow | Driving rhythm, uptempo, energetic beat | Slow tempo, laid-back groove, gentle pace |
| Polished ↔ Raw | Radio-ready mix, clean production, crisp | Lo-fi, organic, rough edges, imperfect |
| Familiar ↔ Weird | Classic genre conventions, traditional | Experimental, unexpected, genre-bending (↑ Weirdness slider) |
| Warm ↔ Cold | Analog warmth, rich tones, close mics | Crystalline, digital, distant, sterile |
| Intimate ↔ Epic | Close, quiet, small room, whispered | Wide stereo, big reverb, anthemic, soaring |
| Smooth ↔ Gritty | Clean vocals, flowing melody, polished | Raspy, distorted, textured, rough |
| Bright ↔ Dark | Major key feel, uplifting, shimmering | Minor key feel, moody, deep, shadowy |
| Tight ↔ Loose | Precise timing, quantized, controlled | Swing, human feel, organic timing, relaxed |
| Simple ↔ Complex | Minimal arrangement, few instruments, straightforward | Layered, intricate arrangement, multiple textures (↑ Weirdness slider) |
| Organic ↔ Synthetic | Live instruments, acoustic, natural, analog warmth | Electronic, digital, synthesized, programmed beats |

**Rules:**
- Only present pairs relevant to the narrowed dimension
- Ask them to place the current output AND their desired target on the spectrum
- The gap between "where it is" and "where they want it" determines adjustment magnitude
- If binary narrowing does not converge after 4 questions, pivot to reference-first: "Name a song that sounds like what you wanted — I'll work backwards from there." Reference decomposition is often easier than dimensional analysis for non-musicians.
- If elicitation still does not converge, suggest generating 2-3 variants with different parameter profiles and letting the user compare (turns an elicitation problem into a selection problem).

### First Principles Fallback
When feedback is contradictory or elicitation isn't converging.

**The anchor question:** "If you could only keep ONE thing about this song exactly as it is, what would it be?"

**Rebuild sequence:**
1. Lock the anchor — this does not change
2. For each remaining dimension, offer two options anchored to the keeper
3. Build up layer by layer, checking for contradiction at each step
4. If a new contradiction emerges, reframe as structural contrast (verse vs. chorus, intro vs. drop)

**Borrowed from:** Socratic Questioning, 5 Whys, First Principles Analysis (BMad Advanced Elicitation methods).
