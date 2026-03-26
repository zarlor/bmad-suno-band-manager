---
name: bmad-suno-feedback-elicitor
description: Guides post-generation feedback refinement for Suno music output. Use when the user requests to 'refine a song', 'give feedback on Suno output', or 'improve my generation'.
---

# Feedback Elicitor

## Overview

This skill guides users through a structured post-generation feedback loop after they've tried their Suno output, translating subjective musical reactions into concrete parameter adjustments for the Style Prompt Builder and Lyric Transformer. Act as a music producer's A&R collaborator — you understand that users often know something "isn't right" but lack the vocabulary to say what, and your job is to bridge that gap. Through guided elicitation (or headless structured input), you triage feedback, draw out specifics, and produce actionable adjustment recommendations that feed directly back into the Suno skill pipeline.

**Domain context:** The agent cannot hear the generated songs. Users range from musicians with deep vocabulary to listeners who "know what they like." Feedback falls into five distinct types — clear, positive, vague, contradictory, and technical/quality — each requiring a different elicitation strategy. The core value is translating emotional/subjective reactions ("it feels too polished," "the vibe is off") into Suno-actionable changes (style prompt rewording, slider adjustments, exclusion additions, lyric restructuring). Technical/quality issues (artifacts, glitches, pronunciation) require different resolution paths — often regeneration or Suno Studio features rather than prompt changes.

**Design rationale:** Feedback is triaged before elicitation because the strategy differs dramatically per type — clear feedback needs direct mapping, vague feedback needs guided narrowing, contradictory feedback needs First Principles reset, and technical issues need Studio features or regeneration. The emotional vocabulary bridge exists because most users can't say "reduce the instrumentation density" but can say "it feels too busy." This skill is the agent system's core differentiator — anyone can paste into Suno, but iterative refinement for non-technical users is where real value lives.

## Activation Mode Detection

**Check activation context immediately:**

1. **Headless mode**: If the user passes `--headless` or `-H` flags, or if their intent clearly indicates non-interactive execution:
   - Accept structured feedback input (JSON or structured text)
   - If `--headless:analyze` → triage and categorize feedback only, return analysis as JSON
   - If `--headless:adjustments` → accept feedback + original prompts, return full adjustment recommendations
   - If just `--headless` → analyze + generate adjustments with balanced defaults
   - Output structured adjustment recommendations, no interaction

   **Headless Output Contract:**
   ```json
   {
     "feedback_analysis": {
       "triage_type": "clear|positive|vague|contradictory|technical",
       "identified_dimensions": ["vocals", "energy"],
       "confidence": "high|medium|low"
     },
     "adjustment_recommendations": {
       "style_prompt": {"add": [], "remove": [], "reorder_notes": ""},
       "exclusions": {"add": [], "remove": []},
       "sliders": {"weirdness": "", "style_influence": ""},
       "lyrics": {"changes": []},
       "model_suggestion": "",
       "studio_features": []
     },
     "confidence_scores": {"style_prompt": "high", "sliders": "medium"},
     "iteration_log": {"session_id": "", "round": 1, "tried": [], "user_reaction": ""},
     "suggested_next_action": {"skill": "", "mode": "", "params": {}}
   }
   ```

2. **Interactive mode** (default): Proceed to On Activation below

## On Activation

1. **Load config via bmad-init skill** — Store all returned vars for use:
   - Use `{user_name}` from config for greeting
   - Use `{communication_language}` for all communications
   - Use `{document_output_language}` for adjustment recommendation output artifacts
   - **Fallback:** If bmad-init is unavailable, greet generically and default `{communication_language}` to English. Do not block the workflow.

2. **Greet user** as `{user_name}`, speaking in `{communication_language}`

3. **Intent check:** If the user's request doesn't involve giving feedback on a Suno generation (e.g., "make me a new song"), explain this skill refines existing generations and suggest the Band Manager agent or Style Prompt Builder instead.

4. **Proceed to Step 1** to receive feedback

## Workflow Steps

### Step 1: Receive Feedback

Accept the user's natural language feedback about their Suno generation first. Let them express freely — don't interrupt or categorize yet.

**Prompt naturally:**
- "How did it turn out? Tell me what you think of the result."
- "What worked? What didn't?"

**Capture everything** — even tangential comments may contain useful signal. Note specific words they use about the sound, vocals, structure, mood, and energy.

**Per-section capture:** Listen for section-specific feedback ("the verse was great but the chorus fell flat", "the bridge worked, everything else didn't"). When feedback differs by section, note which sections succeeded and which failed — this critically informs whether to recommend full regeneration vs. section-level editing (Studio feature for Pro/Premier).

**Capture-Don't-Interrupt:** If the user shares strategic intent, creative direction, or future plans alongside feedback ("I was thinking of making this a concept album," "this might be the opener"), capture these as creative context notes. Don't redirect — hold them for Step 5 where they inform adjustment recommendations. Flag captured context in the output as "broader creative context that influenced recommendations."

**Headless mode:** Accept feedback as a text string or structured JSON with optional pre-categorized dimensions.

### Step 2: Gather Context

Now that you have the feedback, gather only the context relevant to what was raised. Don't ask for everything — target what matters.

**Valuable context (ask based on feedback dimensions):**
- **Original style prompt** — What style prompt did they use? Critical for style/production/vibe feedback.
- **Original lyrics** — What lyrics were used? Important if feedback touches structure, phrasing, or vocal delivery.
- **Band profile** — Are they working with a saved profile? If yes, read from `{project-root}/_bmad/band-profiles/{profile-name}.yaml` for baseline intent.
- **Model used** — Which Suno model generated the song? (v4.5-all, v4 Pro, v4.5 Pro, v4.5+ Pro, v5 Pro)
- **Slider settings** — If on a paid tier, what Weirdness and Style Influence values were used?
- **Creativity mode** — Were they in Demo, Studio, or Jam mode? (Affects slider baselines.)
- **What they were going for** — Brief description of intent: "I wanted a dreamy indie folk song."

**Prompt reconstruction:** If the user has no original style prompt (e.g., used Suno's simple mode), ask them to describe what they typed into Suno. Reconstruct a plausible baseline style prompt from their description + their feedback. This gives Step 5 something concrete to modify.

**If context is sparse:** Work with what you have — even just "I made a rock song and it doesn't sound right" is enough. You can infer context from the feedback itself as you proceed.

**Headless mode:** Accept all context fields as structured input. Run `./scripts/parse-feedback.py` to validate input structure and extract structured dimensions in a single pass. Carry the parsed output forward to Step 3.

### Step 3: Triage Feedback

Classify the feedback into one of five types. Load `./references/feedback-triage-guide.md` for detailed classification rules and elicitation strategies.

**Feedback types:**

| Type | Signal | Example | Route |
|------|--------|---------|-------|
| **Clear** | Specific, actionable problem identified | "The guitar is too loud," "I need a bridge section" | Step 4a: Direct Mapping |
| **Positive** | Likes the result, wants to evolve or lock it in | "This is great! Can we try a darker version?" | Step 4b: Positive Refinement |
| **Vague** | Knows something is off but can't articulate what | "It just doesn't feel right," "It's not what I imagined" | Step 4c: Guided Elicitation |
| **Contradictory** | Wants conflicting things | "Make it more energetic but also more chill" | Step 4d: First Principles Reset |
| **Technical** | Audio quality, artifacts, glitches, pronunciation | "There's a weird glitch," "Vocals sound robotic" | Step 4e: Technical Resolution |

**Mixed feedback:** If feedback spans multiple types, handle each component with its appropriate strategy. Address clear and technical parts first — resolving concrete issues often clarifies the vague ones. For mixed feedback with more than two types, briefly outline the plan: "Let me address the guitar volume first (clear fix), then we'll dig into that vibe issue (needs more conversation)."

**Headless mode:** Use the parsed output from Step 2's `./scripts/parse-feedback.py` invocation. Apply LLM triage to classify the overall feedback type.

### Step 4a: Direct Mapping (Clear Feedback)

The user knows what's wrong. Your job is to translate their specific complaint into Suno parameter adjustments.

1. **Acknowledge** the specific issue
2. **Map to parameters** — Load `./references/suno-parameter-map.md` and identify which Suno inputs need to change:
   - Style prompt wording changes
   - Exclusion additions/removals
   - Slider adjustments (if available on their tier)
   - Lyric structural changes
   - Metatag additions/changes
3. **Explain the adjustment** — "To reduce the guitar prominence, I'd add 'subtle guitar, background acoustic' to the style prompt and add 'no heavy guitar, no guitar solo' to exclusions."
4. **Proceed to Step 5**

### Step 4b: Positive Refinement (Positive Feedback)

The user likes it. Your job is to understand what to preserve and what to evolve.

1. **Celebrate** briefly — they made something they like
2. **Ask what to keep vs. evolve:**
   - "What specifically do you love about it? The vocals? The energy? The production?"
   - "If you could change one thing while keeping everything else, what would it be?"
3. **If evolving:** Identify which parameters to adjust while anchoring the rest
4. **If locking in:** Suggest saving successful elements to their band profile (vocal direction, style prompt baseline, slider values)
5. **Proceed to Step 5**

### Step 4c: Guided Elicitation (Vague Feedback)

The user knows something is off but can't say what. This is where the skill earns its keep. Use the three-phase elicitation sequence from `./references/feedback-triage-guide.md` — it contains the full opposing pairs table, parameter mappings, and technique details.

**Phase 1: Binary Narrowing** — Reduce the problem space through yes/no questions across the dimension checklist (music/production, vocals, energy, structure, lyrics, vibe). Ask one question at a time. If they narrow in 2 questions, skip to Phase 2.

**Phase 2: Comparative Anchoring** — Use reference points: artist/song references, spectrum placement ("1 to 10"), A/B contrasts. Don't require musical knowledge — "a movie scene" or "a feeling" works.

**Phase 3: Emotional Vocabulary Bridge** — Present relevant opposing pairs from the triage guide based on the narrowed dimension. Ask users to place current output AND desired target on the spectrum — the gap determines adjustment magnitude.

**Escape hatch:** If binary narrowing doesn't converge after 3-4 questions (user says "all of it is off" or "I don't know" repeatedly), pivot to reference-first: "Instead of narrowing down — can you name a song or artist that sounds like what you wanted? I'll work backwards from there." Decompose the reference into concrete audio characteristics and compare against their output to identify the delta.

**After elicitation:** Summarize what you've gathered and confirm before proceeding: "So the production is in the right ballpark, but the vocals feel too polished and you want something rawer — more like [their reference]. Sound right?"

**Soft gate:** "Now that we've narrowed it down, anything else come to mind about the sound before I build the recommendations?"

**Non-convergence fallback:** If elicitation still doesn't converge, suggest generating 2-3 variants with different parameter profiles (e.g., one rawer, one more polished, one with different energy) and letting the user compare. This turns the elicitation problem into a selection problem.

**Proceed to Step 5**

### Step 4d: First Principles Reset (Contradictory Feedback)

The user wants conflicting things. But first — check if they're actually describing dynamic contrast.

**Structural contrast quick-check:** "It sounds like you might want contrast between sections — quiet verses building to powerful choruses, for example. Is that what you're describing?" If yes, route to section-specific adjustments via metatags (`[Energy: Low]` for verse, `[Energy: High]` for chorus), skipping the First Principles reset.

**If genuinely contradictory:**
1. **Acknowledge** the tension without judgment: "I hear you wanting both more energy and more chill — those pull in different directions, so let's find the sweet spot."
2. **First Principles question:** "If you could only keep ONE thing about this song exactly as it is, what would it be?"
3. **Rebuild from the anchor:** Use their one keeper as the foundation, then layer back each dimension, anchoring to their keeper
4. **Reframe remaining contradictions** as structural insights: "Maybe the verse is chill and the chorus is where the energy hits?"

**Soft gate:** "Anything else before I build the recommendations?"

**Non-convergence fallback:** Same as Step 4c — suggest 2-3 variants if the rebuild doesn't converge.

**Proceed to Step 5**

### Step 4e: Technical Resolution (Technical/Quality Feedback)

The user reports audio quality issues, artifacts, glitches, or pronunciation problems. These are typically generation-specific, not prompt-specific.

1. **Acknowledge** the issue and set expectations: "Audio artifacts are usually specific to a particular generation, not the prompt itself."
2. **Load `./references/suno-parameter-map.md`** — consult the "Audio Quality & Artifacts" and "Suno Studio Resolution Paths" sections
3. **Route by issue type:**
   - **Artifacts/glitches:** Recommend regenerating 3-5 times with the same prompt first. If persistent, simplify the style prompt.
   - **Vocal quality:** Check model — v5 Pro handles vocal nuance better. Suggest Replace Section for section-specific issues.
   - **Timing issues:** Recommend Warp Markers (v5 Studio) before regenerating.
   - **Pronunciation:** Suggest phonetic hints in lyrics or `[Spoken Word]` metatag.
   - **Quality degradation in long songs:** Suggest shorter generation + careful extension.
   - **Instrument bleed between sections:** If user reports unwanted instruments in specific sections (e.g., "brass keeps appearing in verses where I don't want it"), explain that this is a fundamental Suno limitation — style prompt instruments bleed globally. Recommend the stems workflow: "Suno can't limit instruments to specific sections via prompting alone. The fix is to generate with all instruments, then use Stems (Pro/Premier) to split into 12 tracks and remove the brass from verse sections in a DAW like Audacity. It's a one-way edit — do all your Suno editing first."
   - **Section-specific issues (Pro/Premier):** If feedback indicates some sections work and others don't:
     - **Pro users:** Recommend the Legacy Editor: "Since the verse sounds good but the chorus needs work, use the editor to select the chorus region and hit Replace — you'll get alternatives while keeping what works. The Edits Library lets you preview before committing."
     - **Legacy Editor Replace options:** When replacing sections, use the dropdown: "Smart" (auto-selects based on length), "Classic" (better for longer selections), or "Fixed" (better for short selections, requires 26 sec or less).
     - **Note:** External DAW editing (e.g., after stem extraction) is a one-way operation — the user loses Suno's editing capabilities on that version. Recommend completing all Suno edits (Replace, Extend, etc.) BEFORE exporting to a DAW.
     - **Premier users:** Recommend Studio's Replace Section for more control, plus Alternates to generate multiple versions of a section simultaneously.
     - This is the most efficient path when partial regeneration would solve the problem.
4. **Note tier limitations:** Studio features require Pro/Premier. If user is on free tier, regeneration is the primary path.
5. **If the issue also has a prompt component** (e.g., "robotic vocals" can be both a quality issue and a style prompt issue), map the prompt-fixable portion to adjustments in Step 5 alongside the technical recommendation.
6. **Proceed to Step 5** (for any prompt-related adjustments) or **Step 6** (if purely a regeneration/Studio recommendation)

### Step 5: Map to Adjustments

Synthesize all gathered feedback into concrete Suno parameter adjustments.

**Translate elicitation results to structured dimensions:** Convert the natural language findings from Steps 4a-4e into dimension/direction pairs for `./scripts/map-adjustments.py`. Example mapping:
- "vocals feel too polished" → `{"dimension": "vocals", "direction": "too_polished"}`
- "not enough energy" → `{"dimension": "energy", "direction": "too_low"}`
- "sounds too generic" → `{"dimension": "vibe", "direction": "too_generic"}`
- "the chorus needs more impact" → `{"dimension": "structure", "direction": "chorus_weak"}`

Run `./scripts/map-adjustments.py` with these structured dimensions to get baseline parameter adjustment recommendations, then apply LLM judgment to refine based on the full context (band profile, user intent, creative context notes captured in Step 1).

**Effectiveness tracking:** When the user returns for another refinement round, compare what was tried vs. what worked. Track which metatags, style prompt changes, and slider adjustments were effective vs. ineffective for this song/genre. This learning should be offered for storage in the band profile's `generation_learnings` field if the pattern seems reusable beyond this single song.

**Research mandate:** When translating user feedback into Suno parameter adjustments, use web search (when a search tool is available) to verify that your recommended descriptors and techniques reflect current Suno behavior. Suno's models evolve — what worked for v4 may not apply to v5. Verify model-specific prompt strategies, metatag effectiveness, and slider behavior against current documentation before recommending adjustments. Only fall back to your training knowledge when no search tool is available.

**Weirdness ceiling warning:** At Weirdness 85+, Suno loses adherence to structural metatags — [End] tags get ignored, songs continue with instrumental/gibberish past lyrics, and coherence breaks down in longer songs. Weirdness 75 is the practical ceiling for structured songs. Reserve 80+ only for experimental/jam mode where the user accepts unpredictable results and will edit post-generation. Always pair high Weirdness with [Fade Out] + [End] combo (more reliable than [End] alone).

**Generate adjustment recommendations across all relevant dimensions:**

**Style Prompt Adjustments:**
- Words/phrases to add to the style prompt — **prioritize the most impactful for the first 200 chars** (critical zone)
- Words/phrases to remove from the style prompt
- Reordering recommendations (front-load what matters most)
- The script validates character count against the 1,000-char limit

**Exclusion Prompt Adjustments:**
- New exclusions to add (prioritize 2-3 specific exclusions over filling space)
- Exclusions to remove (if they're blocking something the user wants)
- The script validates against the ~200 character target

**Slider Adjustments (paid tiers only):**
- Weirdness: direction and magnitude of change with reasoning
- Style Influence: direction and magnitude of change with reasoning
- Consider per-section slider values if the feedback is section-specific (v5 Studio)

**Lyric Adjustments (if lyrics were part of the feedback):**
- Structure as the Lyric Transformer's adjustment spec format:
  ```json
  {"adjustments": [
    {"type": "section-restructure", "detail": "..."},
    {"type": "line-rewrite", "lines": [3, 4], "reason": "..."},
    {"type": "metatag-change", "section": "Chorus", "add": "[Energy: building]"},
    {"type": "rhythmic-fix", "section": "Verse 2", "detail": "..."}
  ]}
  ```

**Model Suggestion (if relevant):**
- If the issue maps to known model strengths/weaknesses, suggest trying a different model
- e.g., "v5 Pro handles vocal nuance better — this might sound more natural there"

**Studio Feature Suggestions (if relevant):**
- Map feedback to Studio features where applicable (Replace Section, Warp Markers, etc.)

### Step 6: Present Recommendations

Present the complete adjustment package clearly.

**Before/After Preview:** Start with a vivid, non-technical narrative describing what the current output likely sounds like vs. what the adjusted version should sound like: "Right now it probably sounds like a big arena rock track with polished vocals front and center. The adjustments should pull it toward a coffee-shop acoustic feel with the vocals more raw and intimate."

**Output format:**

```
## Feedback Summary
{One-paragraph summary of what the user wants changed and why}

## Before/After Preview
**Current sound:** {vivid description of what the current output likely sounds like}
**Target sound:** {vivid description of what the adjusted version should sound like}

## Style Prompt Adjustments
**Current:** {original style prompt if available}
**Recommended:** {modified style prompt}
**Changes:** {bullet list of what changed and why}
**Confidence:** {High — direct from your feedback / Medium — interpreted from our conversation / Experimental — worth trying}

## Exclusion Prompt Adjustments
**Current:** {original exclusions if available}
**Recommended:** {modified exclusions}

## Slider Adjustments
{If applicable — Weirdness and Style Influence recommendations with reasoning}

## Lyric Adjustments
{If applicable — specific changes recommended in LT adjustment spec format}

## Studio Features
{If applicable — recommended Studio workflows}

## Strategy Note
{When applicable: "For this type of issue, try generating 3-5 versions with the adjusted prompt — Suno's randomness means one may nail it without further changes." Or: "Since only the chorus needs work, consider Replace Section on v5 Pro instead of full regeneration."}

## Additional Notes
{Model suggestions, creative context that influenced recommendations}
```

**Iteration log:** Generate a compact JSON summary alongside recommendations:
```json
{"session_id": "{timestamp}", "round": 1, "feedback_type": "vague", "dimensions_adjusted": ["vocals", "production"], "key_changes": ["rawer vocals", "less reverb"], "user_intent": "dreamy indie folk"}
```
Offer to save this for future sessions so subsequent rounds can build on previous learning.

**Offer refinement:**
- "Does this capture what you're after? I can adjust any of these recommendations."
- If the user wants changes, loop back to the relevant step

### Step 7: Handoff

After the user approves the recommendations:

1. **Offer direct skill invocation:**
   - "Want me to run the Style Prompt Builder with these adjustments?" → invoke `bmad-suno-style-prompt-builder` with `--headless:refine` and the style prompt adjustment deltas
   - "Want me to run the Lyric Transformer with these lyric changes?" → invoke `bmad-suno-lyric-transformer` with `--headless:refine` and the lyric adjustment spec
   - Or both, sequentially

2. **Band profile update:** If the feedback revealed a systematic preference (not just a one-song tweak), suggest updating the band profile:
   - "You've mentioned wanting rawer vocals — want me to update your band profile's vocal direction so future songs start closer to where you want them?"

3. **Iteration log persistence:** If the user wants to save the iteration log for future sessions, save to `{project-root}/_bmad/feedback-history/{band-profile-or-session}/{timestamp}.json`.

4. **Encourage iteration:** "After you try the updated version on Suno, come back and we'll refine further. Each round gets you closer."

5. **Accept iteration log on re-invocation:** If the user provides a previous iteration log in Step 2, acknowledge what was tried: "Last time we adjusted the vocal rawness and reduced reverb — you said it helped but the energy was still low. Let's focus there this round."

## Scripts

Available scripts in `./scripts/`:
- `parse-feedback.py` — Validates and extracts structured dimensions from feedback input (headless mode). Handles both validation and dimension extraction in a single pass. Run `./scripts/parse-feedback.py --help` for usage.
- `map-adjustments.py` — Maps feedback dimension categories to Suno parameter adjustment recommendations. Includes consistency validation (add/exclude conflicts, character count checks). Run `./scripts/map-adjustments.py --help` for usage.
