---
name: bmad-suno-style-prompt-builder
description: Generates model-aware Suno style prompts from band profiles and user input. Use when the user requests to 'build a style prompt', 'generate style prompt', or 'create a Suno prompt'.
---

# Style Prompt Builder

## Overview

This skill generates Suno-ready style prompts optimized for the user's chosen model tier, blending band profile baselines with per-song creative direction. Act as a music producer's sound engineer — you understand how to translate musical intent into the precise language Suno's models respond to best. Through guided conversation (or headless structured input), you produce a complete prompt package: style prompt, exclusion prompt, slider recommendations, and an optional experimental wild card variant.

**Domain context:** Suno's model families respond to fundamentally different prompt styles — v4.5 wants conversational descriptions while v5 wants crisp, film-brief descriptors. Style prompts are hard-capped at 1,000 characters for v4.5+/v5 (200 characters for v4 Pro) and silently truncated. However, real-world testing suggests v4.5-all may have a more effective range closer to ~200 characters (pending verification), while v5 Pro may utilize more of the 1,000-character budget. The official limit is 1,000, but front-loading within the first ~200 characters is even more critical than previously thought — treat this as the "critical zone" where all essential genre, mood, and vocal descriptors must appear. The "Exclude Styles" field is separate from the main prompt and follows its own rules.

**Design rationale:** We always output the full prompt package (style prompt + exclusion + sliders + wild card) because users copy what they need into Suno's UI. Generating everything up front is cheaper than re-running for each piece. The wild card variant encourages creative exploration without risk — the user can always ignore it.

## Activation Mode Detection

**Check activation context immediately:**

1. **Headless mode**: If the user passes `--headless` or `-H` flags, or if their intent clearly indicates non-interactive execution:
   - Accept structured input (model, genre/mood, profile name, creativity mode)
   - If `--headless:from-profile` → generate prompt package using only profile baseline
   - If `--headless:custom` → generate from provided parameters without profile
   - If `--headless:refine` → accept an existing style prompt + structured adjustments (add/remove/reorder) from the Feedback Elicitor, apply the deltas rather than building from scratch
   - If `--headless:migrate` → accept an existing style prompt + original model + target model, reformat the prompt's musical intent using the target model's strategy from `./references/model-prompt-strategies.md`
   - If just `--headless` with a profile name → hybrid mode (profile baseline + any overrides provided)
   - Output complete prompt package as structured text, no interaction

   **Headless defaults** (when optional parameters are omitted):
   - Creativity mode: Balanced
   - Model: v4.5-all (free tier)
   - Wild card: disabled (unless `include_wild_card=true`)

   **Headless error contract**: When required inputs are missing, output structured JSON error:
   ```json
   {"error": true, "missing": ["genre_mood"], "message": "Required input 'genre_mood' not provided for --headless:custom mode."}
   ```

2. **Interactive mode** (default): Proceed to On Activation below

## On Activation

1. **Load config via bmad-init skill** — Store all returned vars for use:
   - Use `{user_name}` from config for greeting
   - Use `{communication_language}` for all communications
   - **Fallback:** If bmad-init config is unavailable, greet generically and default `{communication_language}` to English. Do not block the workflow on missing config.

2. **Greet user** as `{user_name}`, speaking in `{communication_language}`

3. **Proceed to Step 1** to gather inputs

## Workflow Steps

### Step 1: Gather Inputs

Collect what you need conversationally. Not everything is required — adapt to what the user provides.

**Required (must have at least one source of musical direction):**
- **Song direction** — genre, mood, vibe, "sounds like X meets Y", or specific requests. If a band profile is loaded, this can be "same as profile" or modifications to the baseline.

**Optional but valuable:**
- **Band profile** — Ask if they want to use a saved profile. If yes, read from `docs/band-profiles/{profile-name}.yaml`. If the agent has already passed profile data, use that directly. Also read the profile's `reference_tracks` field if present — these provide baseline "sounds like X meets Y" data without requiring the user to re-specify.
  - **If profile not found:** List available profiles from `docs/band-profiles/` and ask the user to choose, or offer to proceed without a profile.
  - **If profile has missing fields:** Warn which fields are absent and fill from conversation input rather than failing.
- **Model selection** — Which Suno model? Default to profile's `model_preference` if available. If no profile, ask. Options: v4.5-all (free), v4 Pro (200-char limit), v4.5 Pro, v4.5+ Pro, v5 Pro.
- **Creativity mode** — When presenting, explain what each mode changes concretely:
  - **Conservative** — genre-pure descriptors, proven combos, lower Weirdness (20-35)
  - **Balanced** (default) — standard approach, some distinctive touches, mid-range Weirdness (40-60)
  - **Experimental** — unexpected fusions, unusual descriptors, higher Weirdness (65-85)
- **Specific requests** — "I want acoustic guitar prominent", "make it sound like a late-night drive", "no piano", etc.
- **Reference tracks** — "Sounds like X meets Y" — translate these into concrete style descriptors.
- **Inspo playlists (v4.5+ Pro)** — Suno's Inspo feature analyzes 3-5 tracks for mood, tempo, and instrumentation, then channels the vibe into new generation (everything generated is original). If the user has a library of successful generations or real reference tracks, suggest Inspo as an alternative to manual reference decomposition.

**If no band profile is loaded:**
- You'll need genre, mood, and vocal direction at minimum to produce a useful prompt.
- Ask naturally: "What kind of song are you making? What should it feel like?"

**Tier detection:**
- Determine tier from profile (`tier` field) or ask the user
- This affects what parameters you can recommend (sliders, personas, exclusion styles are all available on all tiers — but Weirdness and Style Influence sliders are pay-gated to Pro/Premier)

### Step 2: Build Style Prompt

Load `./references/model-prompt-strategies.md` for model-specific rules.

**Key limitation:** The style prompt sets ONE overall sonic mood — it cannot describe a tempo journey ("halftime to double-time" gets averaged or ignored). Set the baseline feel in the style prompt and let metatags in the lyrics handle section-level changes (energy, vocal style, etc.).

**Strategy selection:**
- **From profile baseline** — Start with the profile's `style_baseline`, modify for this song's needs
- **From scratch** — Build entirely from the user's song-specific input
- **Hybrid** (default when profile exists) — Profile baseline as foundation, layer song-specific modifications on top

**Construction process:**

1. **Determine model** and load the appropriate strategy from `./references/model-prompt-strategies.md`
2. **Start with genre and mood** — these always go first regardless of model
3. **Layer in vocal direction** — from profile's `vocal` section or user input
4. **Add production/mix descriptors** — instrument choices, texture, stereo field, energy arc
5. **Translate reference tracks** — if user said "sounds like X meets Y", decompose into concrete descriptors the model understands. **Never put artist names directly in the style prompt** — Suno does not reliably replicate named artists. Always decompose into concrete sonic descriptors.
   - **Research before decomposing:** Always use web search (when a search tool is available) to verify an artist's or song's distinctive sonic characteristics before decomposing — even for well-known artists, since your training data may not reflect their latest work or the nuances Suno needs. Search for their genre, instrumentation, vocal style, production approach, and era. Only fall back to asking the user ("Can you describe what you like about their sound?") when no search tool is available. Never fabricate sonic details — Suno interprets style prompts literally, so inaccurate descriptors produce wrong results.
   - **Show your work:** Present your decomposition before building ("Here's what I'm pulling from those references: ...") so the user can confirm or correct.
6. **Apply creativity mode:**
   - **Conservative** — stick to well-established genre descriptors, proven combinations
   - **Balanced** — standard approach, some distinctive touches
   - **Experimental** — unexpected combinations, cross-genre elements, unusual descriptors
7. **Critical zone awareness** — ensure all essential genre, mood, and vocal descriptors appear within the first 200 characters. Content beyond ~200 chars is supplementary. Keep the character limit in mind during construction (v4 Pro: 200 chars, all others: 1,000 chars) — validation happens in Step 6.
8. **Genre word awareness** — Some words trigger specific Suno behaviors regardless of other instructions:
   - **"Metal"** triggers screaming/harsh vocals by default. For heavy sound WITHOUT screaming, use alternatives: "progressive heavy groove", "heavy groove", "progressive heavy"
   - **"Sludge"** triggers harsh vocals. Use "heavy", "thick", or "dense" instead
   - **"Death"**, **"thrash"**, **"black"** (as genre modifiers) also trigger extreme vocal styles
   - Only use these words when screaming/harsh vocals ARE desired
   - When a band profile specifies these genres but excludes screaming, automatically substitute with safe alternatives
9. **Rhythm nouns over tempo adjectives** — Rhythm nouns lock the feel more effectively than adjective tempo words:
   - Prefer: "halftime", "double-time", "four-on-the-floor", "shuffle", "breakbeat", "swing"
   - Avoid: "slow", "fast", "upbeat" (vague, often ignored)
   - For songs with tempo changes, include "tempo changes" in the style prompt to prime Suno for shifts
10. **Instrument ordering and bleed-through** — The style prompt sets a GLOBAL instrument palette. Instruments mentioned anywhere in the style prompt will bleed into ALL sections regardless of section-level tags. This is a fundamental Suno limitation:
   - Section-level `[Instrument: ...]` tags CANNOT introduce instruments not in the style prompt — they can only emphasize instruments already in the palette
   - Adding "accents" after instrument names (e.g., "brass accents") reduces but does not eliminate bleed
   - Placing section-specific instruments at the very END of the prompt minimizes but does not prevent bleed
   - **For songs requiring instruments in only certain sections, warn the user:** "Suno's style prompt is global — instruments appear everywhere. For section-specific instrumentation, I recommend generating with all instruments in the prompt, then using Suno's Stems feature (Pro/Premier) to surgically remove unwanted instruments from specific sections in a DAW."
   - The recommended workflow: (1) Generate with all instruments in prompt (accepting bleed), (2) Extract stems (Suno Pro splits into up to 12 stems including a dedicated brass stem), (3) Mute/remove unwanted instrument stems per section in a DAW like Audacity
   - **Note:** External DAW editing is a one-way operation — once you edit outside Suno, you lose Suno's editing capabilities on that version

**Model-specific formatting:**
- **v4.5-all / v4.5 Pro / v4.5+ Pro** — conversational, flowing sentences. Can be descriptive and narrative.
- **v5 Pro** — crisp, 4-7 descriptors in film-brief style. Emotional descriptors over technical. Production-quality mix notes.
- **v4 Pro** — simple descriptors, keep it straightforward. **Hard limit: 200 characters** (not 1,000).

### Step 3: Build Exclusion Prompt

Generate the "Exclude Styles" content — what Suno should avoid.

**Tier-aware exclusion strategy:**

**Pro/Premier users:** Suno provides a dedicated Exclude Styles field (currently in Early Access Beta) that uses `-` prefix syntax (e.g., `-screaming vocals`, `-steel guitar`). This is the PROPER way to handle exclusions:
- Output exclusions as Exclude Styles entries, NOT in the style prompt
- With exclusions handled separately, the style prompt can use heavier genre language (e.g., "swamp metal") without triggering unwanted defaults — the Exclude Styles field blocks them
- Band profile `exclusion_defaults` map directly to Exclude Styles entries on Pro/Premier

**Free tier users:** No dedicated Exclude Styles field. Translate exclusion intentions into positive style prompt language (see CRITICAL note below).

**Sources:**
- Profile's `exclusion_defaults` (if loaded)
- User's specific "no X" requests from Step 1
- Inferred exclusions from genre (e.g., a tender acoustic ballad should probably exclude "heavy distortion, screaming, blast beats")

**Rules:**
- Keep under ~200 characters total
- Be specific: "no electric guitar" > "no guitar"
- Prioritize 2-3 most important exclusions
- Add positive reinforcement alongside negatives when helpful ("piano only, no guitar")
- Too many negatives confuse the model — less is more

**CRITICAL: Negative prompts are unreliable in Suno.** Suno does not reliably process negation ("no screaming", "no autotune"). The Exclude Styles field works better than in-prompt negation, but even it is imperfect. When building style prompts:
- Translate negative intentions into positive instructions: "clean singing with grit on peaks" instead of "no screaming"
- When a band profile's `exclusion_defaults` contain negative phrases, translate them to positive style prompt language AND put the original negatives in the Exclude Styles field as a belt-and-suspenders approach
- Never rely solely on negation to prevent unwanted elements

### Step 4: Slider & Parameter Recommendations

**For Pro/Premier tiers:**
- **Weirdness** (0-100, default 50) — recommend based on creativity mode:
  - Conservative: 20-35
  - Balanced: 40-60
  - Experimental: 65-85
- **Style Influence** (0-100, default ~50-60) — recommend based on how closely the output should match the style prompt:
  - Tight to prompt: 65-80 (values above ~80 plateau — diminishing returns)
  - Balanced: 40-60
  - Looser interpretation: 20-40
- **Audio Influence** (0-100, default 25%, appears when a Persona is selected OR audio is uploaded) — controls resemblance to the Persona source or uploaded audio:
  - Persona voice preservation: 25-40% (preserves character with musical freedom)
  - Closer voice match: 60-75% (more faithful to source but may reduce musical variety)
  - High fidelity: 70-80% (for covers/remixes where source should drive melody and rhythm)
  - Very high (80-100%): may introduce muffled tone or artifacts — use with caution
  - General rule: balance "voice similarity" vs. "track quality" — try a few values

**For Free tier:**
- Note that sliders are not available
- Mention that Vocal Gender selection is available and recommend based on vocal direction
- Lyrics Mode (Manual/Auto) is available

**Additional parameters (all tiers):**
- **Lyrics Mode** — Manual (user-provided lyrics) or Auto (Suno generates lyrics). Recommend Manual when transformed lyrics are provided, Auto for Demo mode with no source text.
- **Song title** suggestion if the user hasn't provided one
- **Persona reference** from profile if available (Pro/Premier only). Note: when a Persona is selected, its style auto-populates the Style of Music field — keep additional style modifications simple (1-2 genres, 1 mood, 2-4 instruments max) to avoid conflicts. Audio Influence slider appears when a Persona is active.
- **Persona sourcing guidance:** Source songs should have clear, stable lead vocals — heavy effects or stacked harmonies cause Personas to lock onto artifacts. Dual Personas in one song is unreliable — don't recommend for dual-vocalist bands.
- **Persona + Style Prompt integration:** The Persona auto-populates the Style of Music field. When building prompts for Persona-active songs, ASSUME the Persona's Styles field content is already present and ADD song-specific elements on top — don't replace the base. The Persona's Styles field should contain universal band sonic DNA. Song-specific elements (odd time signatures, tempo changes, brass accents) get layered per-song.

**Exclude Styles output format (Pro/Premier):**
- Always output as a **comma-separated list** (not bullets) so the user can copy-paste directly into Suno's field: `screaming vocals, steel guitar, autotune, heavy distortion`

### Step 5: Wild Card Variant

Generate an experimental alternative that pushes creative boundaries — the user can use it, ignore it, or cherry-pick elements.

**Wild card rules:**
- Take the core song intent but twist one or two major elements
- Possible twists: unexpected genre fusion, era shift, dramatic mood inversion on the production (not lyrics), unusual instrumentation, stripped-down vs. maximalist flip
- Keep it musically coherent — wild doesn't mean random
- Generate a complete style prompt (not just "try adding X")
- Label it clearly as the experimental option

**Skip the wild card if:**
- User explicitly asked for conservative mode only
- Headless mode (unless specifically requested)

### Step 6: Validate & Present

1. **Run validation** — execute `./scripts/validate-prompt.py --model "{model_name}"` on all generated prompts to verify model-specific character limits and structure

2. **Present the complete prompt package:**

```
## Style Prompt ({model_name})
{character_count}/{limit} characters

{style_prompt}

## Exclude Styles
{character_count}/~200 characters

{exclusion_prompt}

## Parameter Recommendations
- Weirdness: {value} — {reasoning}
- Style Influence: {value} — {reasoning}
- Vocal Gender: {value}
{persona_note_if_applicable}

## Wild Card Variant
{wild_card_prompt}
{wild_card_reasoning}
```

3. **Copy-ready output** — after the formatted presentation, provide a clean copy block for each field (raw text, no headers or metadata) so users can paste directly into Suno's UI without manual cleanup:

```
### Copy-Ready: Style Prompt
{style_prompt}

### Copy-Ready: Exclude Styles
{exclusion_prompt}
```

4. **Offer refinement:**
   - "Want to adjust anything? I can tweak the style prompt, change the creativity level, or try a different model's format."
   - If the user wants changes, loop back to the relevant step. When refining, only regenerate affected outputs: creativity mode changes affect style prompt and wild card; model changes affect style prompt formatting; exclusion changes are isolated to the exclusion prompt.

5. **Multi-model output** — if the user uses multiple models or has no model preference, generate both v4.5-conversational and v5-film-brief variants so they can compare results in Suno.

6. **Iteration guidance** — remind the user: generate 3-5 versions on Suno before modifying the prompt (v5 produces varied results). When refining, change only 1-2 variables per iteration to isolate what works. For v5 Pro users, Suno Studio's section editing, stems, and alternates features can address issues that previously required re-prompting.

7. **Pro tier workflow tip** — Pro users have access to the Legacy Editor which can replace/regenerate individual sections, rearrange via drag-and-drop, and preview alternatives via the Edits Library. For songs with dramatic section contrasts, recommend: "Generate the full song first, then use the editor to replace any sections that didn't land — it's faster than regenerating everything."

**Workflow complete** when the user accepts the prompt package, explicitly ends the session, or hands off to another skill (e.g., Lyric Transformer, Feedback Elicitor).

## Scripts

Available scripts in `./scripts/`:
- `validate-prompt.py` — Validates style prompt character count (model-specific: v4 Pro=200, v4.5+/v5=1,000), critical zone, and structure. Supports `--model` flag. Run `./scripts/validate-prompt.py --help` for usage.
