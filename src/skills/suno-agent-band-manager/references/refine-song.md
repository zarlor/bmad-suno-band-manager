**Language:** Use `{communication_language}` for all output.
**Variables:** `{project-root}`, `{communication_language}`

---
name: refine-song
description: Post-generation refinement — runs Feedback Elicitor and routes adjustments back through Style Prompt Builder and/or Lyric Transformer.
menu-code: RS
---

# Refine Song

The iterative refinement loop. The user has tried their output on Suno and is back with feedback. This capability orchestrates the Feedback Elicitor to translate their reactions into concrete adjustments, then routes those adjustments back through the appropriate skills.

## Step 1: Gather Context

Check what you already know from the current session or memory:

**From current session (if create-song was run earlier):**
- Original style prompt, lyrics, parameters, model used
- Band profile (if loaded)
- Song direction and intent

**If starting fresh (user came directly to refine):**
- **Auto-lookup first:** Before asking the user for technical details, check `docs/songbook/` and `{project-root}/_bmad/_memory/band-manager-sidecar/chronology.md` for the most recent song package. If found, confirm: "Is this the one you're refining? {song title / style prompt preview}"
- If no match found, ask what they generated and what prompts they used
- Ask which model and settings
- Ask what they were going for

**Minimal context path:** If the user can't provide technical details ("I don't know, I just hit Create"), work with what they have:
- Infer model from tier if known from memory (free tier = v4.5-all)
- Don't ask about sliders if they're on free tier
- Accept emotional descriptions alone: "I pasted X and got Y, but it sounds too Z" is enough
- The Feedback Elicitor handles vague feedback — let it do its job

Pass all available context to the Feedback Elicitor — the more it knows about the original intent, the better it can diagnose issues.

### Handoff Checkpoint (before Feedback Elicitor)

Before invoking the Feedback Elicitor, surface a brief summary of the feedback interpretation to the user:

> "Here's what I'm sending to the feedback pipeline: original style prompt is **[prompt or 'unknown']**, your feedback is **[summary of what they said]**, and I'm reading this as **[clear/vague/contradictory/technical]**. Sound right?"

Wait for confirmation. If the user says "no, I meant..." — update the interpretation before proceeding. This prevents the common failure mode of vague feedback being over-interpreted into specific parameter changes the user didn't intend.

After the Feedback Elicitor returns, apply **Transparency**: surface the recommended changes and what drove them before presenting the updated package.

## Step 2: Run Feedback Elicitor

Invoke `suno-feedback-elicitor` with:
- Original style prompt (if available)
- Original lyrics (if available)
- Band profile name (if loaded)
- Model used
- Slider settings (if known)
- Creativity mode (Demo/Studio/Jam from the session)
- What they were going for (intent summary)
- Previous iteration log (if this is a repeat refinement round)

**Expected return format:** Structured adjustment recommendations (style prompt deltas, lyric changes, slider adjustments, model suggestions) — no explanatory prose. The Feedback Elicitor runs its full triage and elicitation process and returns structured recommendations across: style prompt, exclusion prompt, sliders, lyrics, Studio feature suggestions, and possibly a model suggestion.

## Step 3: Route Adjustments

Based on the Feedback Elicitor's recommendations, offer to re-run the appropriate skills:

**If style prompt adjustments recommended:**
- "Want me to rebuild the style prompt with these changes?"
- If yes: invoke `suno-style-prompt-builder` with `--headless:refine` and the style prompt adjustment deltas
- Pass the specific modifications from the Feedback Elicitor's output

**If lyric adjustments recommended:**
- "Want me to rework the lyrics based on this feedback?"
- If yes: invoke `suno-lyric-transformer` with `--headless:refine` and the lyric adjustment spec
- Pass specific section changes, metatag adjustments, structural modifications

**If both:**
- If the adjustments are independent (different dimensions — e.g., lyrics need restructuring, style prompt needs different mood), run both in parallel for speed
- If lyric changes would inform style choices (e.g., adding a bridge that needs a musical transition), run lyrics first, then style prompt
- Present the updated complete package

**If model change suggested:**
- Note the suggestion: "The Feedback Elicitor thinks v5 Pro might handle this better because of [reason]. Want to try regenerating the style prompt for v5?"

**If Studio features recommended:**
- Present the Studio workflow recommendation (e.g., "Try Replace Section on the chorus instead of regenerating the whole song")
- Note tier requirements — Studio features require Pro/Premier

## Step 4: Present Updated Package

**Present ONLY what changed**, not the full package. The user already has the rest from the previous iteration — re-presenting everything creates noise and makes it harder to spot the actual changes.

**Routing by scope of change:**

- **Lyrics only changed** (Lyric Transformer ran, Style Prompt Builder did not):
  - Present the updated lyrics block
  - Present any slider/setting changes if applicable
  - Do NOT re-present the style prompt, exclude styles, or unchanged settings

- **Style only changed** (Style Prompt Builder ran, Lyric Transformer did not):
  - Present the updated style prompt, exclude styles, and any slider changes
  - Do NOT re-present the lyrics or unchanged settings

- **Both changed** (both skills ran):
  - Present the full updated package (this is the only case where full package is appropriate)
  - Use the create-song Step 5 format

**Always include a "What Changed" bullet list at the top** regardless of scope, so the user can see the deltas at a glance:

```
## Schizo Refinement Update

### What Changed
- {Bullet list of adjustments and why}

{Only the sections that actually changed — lyrics OR style OR both}
```

**Settings/slider changes alone** (no skill re-invocation needed) should be presented as a brief note with the slider values, not as a full package re-present.

**After presenting:**
1. "Give this version a spin on Suno. Each round gets closer to what you hear in your head."
2. "Come back with feedback and we'll keep refining — that's how records get made."

## Step 5: Profile Update Check

If the feedback revealed a **systematic preference** (not just a one-song tweak), suggest updating the band profile:

- "You've mentioned wanting rawer vocals twice now — want me to update your band profile's vocal direction so future songs start from there?"
- "This exclusion list is getting dialed in — should I save it as your default?"

If yes: invoke `suno-band-profile-manager` to edit the relevant profile fields.

### Sync-at-Write for Refinements

Per the "Sync at the point of change" principle in `creed.md`, refinement edits that touch **published** song attributes propagate in the same write batch as the triggering edit — do not defer propagation to save-memory. Concrete cases that require same-batch propagation:

- Updating a published songbook entry's key/tempo/Camelot → update the playlist YAML's track metadata and any voice file catalog references in the same batch
- Updating a published song's voice clone or voice gravity setting → update the songbook entry's Settings block AND any voice context file that references the song's vocal identity in the same batch
- Reordering a published song's playlist position → update the playlist ordering doc AND the voice file catalog section in the same batch as the playlist YAML edit
- Renaming a published song → load `./references/reconcile.md` and run a full reconciliation in this same batch, not after "a few more refinements"

If a refinement touches only the **current-iteration** package (not yet written to the songbook), no cross-file sync applies — there are no references to stale yet. The rule scopes to edits that modify authoritative data other files already point at.

## Loop

The user can keep refining. Each time they return with feedback, loop back to Step 2. The Feedback Elicitor handles fresh triage each round — adjustments compound and the song converges on their vision.

**Diminishing returns:** After 2-3 refinement rounds on the same song, gently suggest a different approach: "We've been dialing this in for a few rounds — Suno's got some randomness baked in. Want me to generate a few variations of the current package so you can pick the one that clicks? Sometimes the best move is casting a wider net."
