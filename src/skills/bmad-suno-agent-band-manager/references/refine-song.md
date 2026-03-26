**Language:** Use `{communication_language}` for all output.

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
- Ask what they generated and what prompts they used
- Ask which model and settings
- Ask what they were going for

**Minimal context path:** If the user can't provide technical details ("I don't know, I just hit Create"), work with what they have:
- Infer model from tier if known from memory (free tier = v4.5-all)
- Don't ask about sliders if they're on free tier
- Accept emotional descriptions alone: "I pasted X and got Y, but it sounds too Z" is enough
- The Feedback Elicitor handles vague feedback — let it do its job

Pass all available context to the Feedback Elicitor — the more it knows about the original intent, the better it can diagnose issues.

## Step 2: Run Feedback Elicitor

Invoke `bmad-suno-feedback-elicitor` with:
- Original style prompt (if available)
- Original lyrics (if available)
- Band profile name (if loaded)
- Model used
- Slider settings (if known)
- Creativity mode (Demo/Studio/Jam from the session)
- What they were going for (intent summary)
- Previous iteration log (if this is a repeat refinement round)

Let the Feedback Elicitor run its full triage and elicitation process. It will return structured adjustment recommendations across: style prompt, exclusion prompt, sliders, lyrics, Studio feature suggestions, and possibly a model suggestion.

## Step 3: Route Adjustments

Based on the Feedback Elicitor's recommendations, offer to re-run the appropriate skills:

**If style prompt adjustments recommended:**
- "Want me to rebuild the style prompt with these changes?"
- If yes: invoke `bmad-suno-style-prompt-builder` with `--headless:refine` and the style prompt adjustment deltas
- Pass the specific modifications from the Feedback Elicitor's output

**If lyric adjustments recommended:**
- "Want me to rework the lyrics based on this feedback?"
- If yes: invoke `bmad-suno-lyric-transformer` with `--headless:refine` and the lyric adjustment spec
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

Re-present the complete Suno package (same format as create-song Step 5) with changes highlighted:

Use the same format and field order as create-song Step 5 (Persona, Inspo, Lyrics, Style Prompt, Exclude Styles, Settings, Song Title), with a "What Changed" section at the top:

```
## Updated Suno Package

### What Changed
{Bullet list of adjustments made and why}

{Then present the full package in the same order as create-song Step 5, showing only fields that changed or all fields if the user prefers the complete view}
```

**After presenting:**
1. "Give this version a spin on Suno. Each round gets closer to what you hear in your head."
2. "Come back with feedback and we'll keep refining — that's how records get made."

## Step 5: Profile Update Check

If the feedback revealed a **systematic preference** (not just a one-song tweak), suggest updating the band profile:

- "You've mentioned wanting rawer vocals twice now — want me to update your band profile's vocal direction so future songs start from there?"
- "This exclusion list is getting dialed in — should I save it as your default?"

If yes: invoke `bmad-suno-band-profile-manager` to edit the relevant profile fields.

## Loop

The user can keep refining. Each time they return with feedback, loop back to Step 2. The Feedback Elicitor handles fresh triage each round — adjustments compound and the song converges on their vision.
