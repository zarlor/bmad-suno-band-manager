# BMad Suno Band Manager -- Usage Guide

This guide covers everything you need to know about working with Mac, the BMad Suno Band Manager agent.

---

## Table of Contents

1. [Getting Started](#1-getting-started)
2. [Interaction Modes](#2-interaction-modes)
3. [Creating Songs](#3-creating-songs-the-main-workflow)
4. [Band Profiles](#4-band-profiles)
5. [Refining Songs](#5-refining-songs-the-feedback-loop)
6. [Direct Skill Access](#6-direct-skill-access)
7. [Songbook & Memory](#7-songbook--memory)
8. [Headless/Automation](#8-headlessautomation)
9. [Troubleshooting](#9-troubleshooting)

---

## 1. Getting Started

### First-Run Experience

The very first time you invoke Mac, he runs through a setup flow to learn how you work. Here is what happens under the hood:

1. Mac checks whether `{project-root}/_bmad/_memory/band-manager-sidecar/` exists.
2. If it does not exist, Mac runs `./scripts/pre-activate.py` to scaffold the directory.
3. Mac loads `./references/init.md` and walks you through the first-run setup.

### The 4 Setup Questions

Mac asks these conversationally -- not as a form:

| # | Question | Why It Matters |
|---|----------|----------------|
| 1 | **What's your Suno setup?** (Free, Pro, Premier) | Determines which models, sliders, and features Mac can recommend. Free users get v4.5-all only; Pro/Premier unlock v5 Pro, Weirdness/Style Influence sliders, Personas, and more. If you upgrade later, just tell Mac. |
| 2 | **How do you like to work?** (Demo, Studio, Jam) | Sets your default interaction mode. You can switch modes anytime -- even mid-song. Try Demo first and explore from there. You can change your default anytime by telling Mac. |
| 3 | **Do you have a band or project?** | If yes, Mac offers to create a band profile right away. If not, you can work one-off. |
| 4 | **Anything you always want or never want?** | Captures your baseline exclusions ("no autotune, ever"), preferred genres, and vocal preferences. These are just starting points -- you can change any of this anytime. |

All of these preferences are changeable through conversation at any time -- no need to edit config files or re-run the installer.

### What Gets Created

After setup, Mac creates three files in the sidecar memory directory:

| File | Purpose |
|------|---------|
| `index.md` | Your preferences, active work, essential context |
| `patterns.md` | Musical preferences Mac learns over time |
| `chronology.md` | Session timeline |

Mac also creates `access-boundaries.md`, which defines where the agent can read and write:

- **Read access:** `docs/band-profiles/` and the sidecar memory folder
- **Write access:** Sidecar memory folder only
- **Deny zones:** Everything else

---

## 2. Interaction Modes

Mac has three interaction modes plus auto-detection. Each one changes how much Mac asks you before generating output.

### Demo Mode

**When to use:** You want something fast. "Just make me a song." Minimal questions, maximum speed.

**What Mac does:**
- Asks for genre/mood at most
- Uses band profile defaults (or sensible genre defaults)
- Defaults to Suno's auto-lyrics if you do not provide text
- Skips the songwriter's workshop questions

**Example interaction:**

```
You: Make me something moody and electronic.
Mac: Got it -- moody electronic it is. Let me put together your package.
     [Generates complete Suno package with no further questions]
```

### Studio Mode

**When to use:** You want full creative control. Album work, specific vision, detailed customization.

**What Mac does:** Runs the full songwriter's workshop. Expect questions like:
- "What's the emotional core of this song? What feeling should someone walk away with?"
- "Is there a story arc -- a beginning, middle, turn?"
- "What's the one line you want stuck in people's heads?"
- "Any specific instruments, textures, or production choices you hear in your head?"
- "Vocal direction -- who's singing this? What do they sound like?"

**Example interaction:**

```
You: I want to build a track around a poem I wrote about leaving home.
Mac: Great material for a song. Let's dig in --
     What's the emotional core here? Is it loss, freedom, nostalgia, or something more complicated?
You: It's bittersweet -- sad to leave but excited about what's next.
Mac: Love that tension. Is there a turn in the poem -- a moment where the mood shifts from one to the other?
```

### Jam Mode

**When to use:** You want to experiment. "Surprise me." Push boundaries, try weird combinations.

**What Mac does:**
- Asks one question: "Give me a starting point -- a word, a feeling, a weird mashup idea -- and I'll run with it."
- Cranks creativity up. Cross-genre fusion encouraged.
- Wild card variants emphasized.
- If you say "surprise me" with zero input, Mac picks a random genre fusion and runs with it.

**Example interaction:**

```
You: Surprise me.
Mac: Alright, here's what I'm feeling today -- a little swamp blues meets synthwave.
     Trust me on this one.
     [Generates full package with an experimental edge]
```

### Auto-Detect

If your opening message includes 3 or more specific parameters (model, sliders, vocal direction, genre, metatags), Mac skips mode selection and goes straight to Studio mode:

```
You: I need a v5 Pro style prompt for a dreamy indie folk song with breathy female vocals,
     acoustic guitar, and lo-fi tape saturation. Weirdness around 45.
Mac: Got it all -- let me build your package.
```

### Switching Modes Mid-Session

Say "let's go Studio mode," "switch to Demo," or "let's jam" at any point. Mac acknowledges the switch and adjusts immediately.

If Mac notices you consistently prefer a different mode than your default, he'll offer to update it: "You've been vibing with Studio mode lately -- want me to make that your default?"

You can also change your default directly: "Make Studio my default mode." Mac updates memory immediately.

### Changing Preferences

You can update any preference by telling Mac during conversation. Changes take effect immediately and persist across sessions.

| Change | What to Say | What Mac Does |
|--------|------------|---------------|
| **Upgrade tier** | "I upgraded to Pro" | Updates memory, announces newly available features, offers to update band profiles |
| **Change default mode** | "Make Studio my default" | Updates memory immediately |
| **Add exclusions** | "I never want autotune" | Updates memory, notes if band profiles are affected |
| **Remove exclusions** | "Stop excluding piano" | Updates memory |
| **Any ongoing preference** | State it as a general preference, not a one-song request | Updates memory via write-through |

---

## 3. Creating Songs (the Main Workflow)

Creating a song is Mac's core capability (menu code: **CS**). Here is the full workflow, step by step.

### Step 1: Providing Song Direction

Mac needs at least one source of musical direction. You have several options:

**Genre and mood:**
```
You: Warm indie rock with a melancholy edge
```

**Reference tracks ("sounds like X meets Y"):**
```
You: Something that sounds like Dr. John meets Bon Iver
```

When you provide reference tracks, Mac decomposes each into concrete sonic descriptors (instrumentation, vocal style, production, energy, era) and shows you the breakdown before building the prompt. If Mac does not confidently know the artist, he will ask you to describe what you like about their sound rather than guessing.

**Band profile baseline:**
```
You: Use my Midnight Porch band profile
```

**Combination of all three:**
```
You: Use my Midnight Porch profile but make it darker -- sounds like Portishead meets trip-hop
```

### Step 2: Providing Source Text

If you have a poem, raw lyrics, or text to transform, paste it in. Mac will route it through the Lyric Transformer.

- **Demo mode:** Applies balanced defaults (Structure Tagging + Chorus Creation + Rhythmic Adjustment + Cliche Detection)
- **Studio mode:** Lets you choose which transformations to apply
- **Jam mode:** Pushes toward full rewrite, experimental

If you do not provide source text:
- **Demo/Jam mode:** Defaults to Suno's auto-lyrics
- **Studio mode:** Asks if you want to write lyrics or use auto-lyrics

### Instrumental-Only Songs

```
You: Make me an instrumental -- ambient electronic, something for studying
```

Mac skips the Lyric Transformer entirely, auto-populates exclusion defaults ("no vocals, no humming, no choirs, instrumental only"), and notes the Instrumental toggle for paid-tier users.

### Non-English Lyrics

```
You: I have a poem in French I want to turn into a song
```

Mac acknowledges the language, adds it as a style prompt element ("sung in French"), and warns that metatag reliability may vary with non-Latin scripts.

### Long Text Handling

If your source text exceeds roughly 400 words, Mac warns you before proceeding:

```
Mac: That's a lot of material -- a typical song has 200-400 words.
     Want me to: (1) condense it to fit one song, (2) split it into a multi-song suite,
     or (3) pick the strongest sections?
```

### The Output Package

Every song creation produces a complete, copy-paste-ready package. The wild card variant is included by default -- it takes your core song intent but twists one or two major elements (genre fusion, era shift, mood inversion, unusual instrumentation). You can use it, ignore it, or cherry-pick elements from it. The wild card is skipped if you explicitly request conservative mode.

Here is a full example:

```
## Your Suno Package

### Lyrics
[Mood: bittersweet]
[Vocal Style: intimate]

[Verse 1]
The porch light flickers on the empty street
Where summer left its footprints in the heat
I count the cracks along the garden wall
And wonder if you heard me when I called

[Chorus]
[Belted]
Come back to the house where the jasmine grows
Where the screen door swings and the evening slows
I left a light on, I left a chair
I left a song hanging in the air

[Verse 2]
[Instrument: acoustic guitar, upright bass]
The radio still hums your favorite tune
The moths are dancing underneath the moon
I saved the letters, pressed between the pages
Of a book that's older than our ages

[Chorus]
Come back to the house where the jasmine grows
Where the screen door swings and the evening slows
I left a light on, I left a chair
I left a song hanging in the air

[Bridge]
[Whispered]
Maybe the distance isn't miles --
Maybe it's just the space between two smiles

[Final Chorus]
[Energy: building]
[Belted]
Come back to the house where the jasmine grows
Where the screen door swings and the evening slows
I left a light on, I left a chair
I left a song hanging in the air

[Outro]
[Hummed]
[Fade Out]

### Style Prompt (v4.5-all)
187/1,000 characters

Warm indie folk, bittersweet Americana, intimate lo-fi production, acoustic guitar
fingerpicking, soft brush drums, upright bass, breathy female vocal, porch-recording
warmth, tape saturation, evening atmosphere, nostalgic

### Exclude Styles
electric guitar, autotune, heavy drums, synths

### Settings
- Vocal Gender: Female
- Lyrics Mode: Manual
- Note: Weirdness, Style Influence, and Audio Influence sliders are available on Pro/Premier plans

### Song Title
Jasmine House

### Wild Card Variant -- The Unexpected Take
Dusty lo-fi hip-hop beat, jazz piano chords with vinyl crackle, spoken-word female vocal
over muted trumpet, late-night FM radio atmosphere, downtempo soul groove

"What if we took this folk ballad and ran it through a lo-fi hip-hop filter?
The nostalgia stays, but the delivery shifts from porch to late-night headphones."
```

For a field-by-field mapping of where each component goes in Suno's UI, see [Suno Reference — Package Field Mapping](./SUNO-REFERENCE.md#package-field-mapping).

### Tips for Using the Output in Suno

Mac includes this guidance on your first song or in Demo mode:

1. Switch to **Custom Mode** in Suno
2. Select your **Persona** (if recommended, Pro/Premier only)
3. Set **Inspo** playlist (if recommended, v4.5+ Pro only)
4. Paste **Lyrics** into the Lyrics field (set Lyrics Mode to Manual)
5. Paste the **Style Prompt** into the "Style of Music" field
6. Add **Exclude Styles** as a comma-separated list (Pro/Premier)
7. Under **More Options**, set Vocal Gender and sliders (if on Pro/Premier)
8. Add your **Song Title**
9. Hit **Create** and generate **3-5 versions** -- Suno interprets the same inputs differently each time

**A note on tempo control:** BPM tags in lyrics (e.g., `[Verse: 65 BPM]`) have no detectable effect on Suno's output -- confirmed by librosa analysis across multiple songs. Perceived tempo is actually controlled through how lyrics are written: short fragmented lines feel slow, packed lines feel fast, and line breaks control where the singer breathes. For drum feel changes, use metatags like `[Heavy: halftime]` rather than BPM values. Mac handles this automatically when building your lyrics package.

---

## 4. Band Profiles

### What a Band Profile Is

A band profile is the sonic equivalent of a brand book. It captures the DNA of a musical project: genre, vocal character, production style, creative boundaries, language, and optionally the songwriter's authentic writing voice. Once created, it serves as a foundation that all skills draw from to maintain consistency across songs.

### Why You Would Want One

- Consistent sound across multiple songs (album/EP work)
- Skip re-explaining your preferences every time
- Store your "sounds like" references for reuse
- Capture slider values and exclusions that work for you
- Preserve your writing voice when Mac transforms lyrics

**A note on vocal consistency:** Band profiles maintain consistency in your *prompts* -- genre, style, exclusions, and vocal direction. However, Suno interprets the same style prompt differently on every generation. The only way to get a truly consistent vocal identity across songs is with the **Persona** feature (Pro/Premier plans), which locks in a specific vocal character from a source song. Without a Persona, you are relying on descriptive prompt language, which gets you in the right neighborhood but not an exact match. If consistent vocal identity across an album or project matters to you, a Pro plan with Personas is strongly recommended.

### Creating Your First Profile

Through Mac's menu, select **MB** (Manage Bands), or say "I want to create a band profile."

Mac (via the Band Profile Manager skill) walks you through a conversational discovery:

1. **Band name** -- What is this project called?
2. **Instrumental or vocal?** -- Skips vocal direction if instrumental
3. **Genre and mood baseline** -- Open-ended: "What does this band sound like?"
4. **Reference tracks** -- "Name 2-3 artists or songs that capture the vibe." Mac decomposes them into concrete sonic descriptors and stores both.
5. **Language** -- What language will the lyrics be in?
6. **Model and tier** -- Which Suno model/plan do you use?
7. **Vocal direction** (if vocal) -- Gender, tone, delivery, energy, diction. Specific is better: "warm, breathy female vocal with indie folk phrasing" not just "female vocals."
8. **Style prompt baseline** -- Built from your answers. Mac shows a draft and iterates with you.
9. **Exclusion defaults** -- What should never appear? Max 5 recommended.
10. **Creative settings** -- Conservative/balanced/experimental. Slider preferences if on a paid tier.
11. **Persona reference** -- Do you have an existing Suno Persona to link?
12. **Writer voice** -- Optional. Analyze your writing style now or skip for later.

Between sections, Mac asks "Anything else to add, or move on?" -- he does not auto-advance.

After discovery, Mac:
- Assembles the profile YAML
- Validates the structure
- Generates a **Band Identity Card** (3-4 sentence natural language summary)
- Presents both for review
- Saves to `docs/band-profiles/{profile-name}.yaml` on approval

### Writer Voice Analysis

If you choose to analyze your writing voice, provide 3 or more writing samples (poems, lyrics, prose -- 10 lines or more each). The more samples you provide, the more accurate the analysis. Pick pieces that feel most like you.

You can paste samples directly into the conversation, or point Mac to files on disk -- a text file, a PDF, a folder of poems. Mac will read and analyze them.

Mac extracts patterns across:
- **Vocabulary preferences** -- formal/casual, abstract/concrete
- **Sentence rhythm** -- short punchy vs. long flowing, fragment use
- **Imagery tendencies** -- nature, urban, body, celestial, domestic
- **Emotional tone** -- raw/restrained, hopeful/melancholic
- **Metaphor style** -- extended vs. quick, conventional vs. surprising
- **Repetition patterns** -- anaphora, refrains, echo structures

Mac shows the analysis with example quotes from your samples, so you can confirm or correct. This gets stored as the `writer_voice` section of your band profile and constrains lyric generation to match your authentic voice.

### Loading and Switching Profiles

```
You: Load my Midnight Porch profile
You: Switch to my Neon Drift profile
You: Use Midnight Porch for this song
```

If Mac has a profile loaded from a previous session, he will offer continuity: "Your band profile Midnight Porch is still loaded -- keeping that?"

### Editing Profiles

```
You: Edit my Midnight Porch profile -- make it more aggressive
You: Update Neon Drift to use v5 Pro
You: Add "no synth pads" to my exclusions
```

Mac loads the profile, applies your changes, re-validates, shows a structured diff of changes, and saves on confirmation. If genre or mood change, Mac suggests updating the style prompt baseline to match.

**Tier drift detection:** When loading a profile, Mac compares the profile's stored tier against your current tier. If they differ, he offers to unlock new features.

### Duplicating Profiles

```
You: Duplicate Midnight Porch as Midnight Porch v2
You: Fork Neon Drift for an acoustic experiment
```

Creates a copy as a starting point for a new version, side project, or sound evolution experiment.

### Health Check

```
You: Is my Midnight Porch profile good?
You: Check my profile
```

Mac assesses completeness and quality beyond structural validation:
- Is the style baseline specific enough?
- Is writer voice populated?
- Are reference tracks present?
- Are exclusion defaults thoughtful?
- Is vocal direction detailed?
- Any successful generation snapshots saved?

Presented as friendly recommendations, not failures: "Your profile is valid and usable. Here is how to make it even better..."

---

## 5. Refining Songs (the Feedback Loop)

The refinement loop (menu code: **RS**) is where songs get great. After generating a package and trying it on Suno, come back to Mac with feedback.

### How to Start a Refinement

**If you are in the same session as create-song:**
```
You: The vocals sound too polished -- I wanted something rawer
```
Mac handles light adjustments directly for clear, simple tweaks. For deeper feedback, he routes to the Feedback Elicitor.

**If you are starting fresh:**
Select **RS** from the menu or say "I want to refine a song." Mac asks what you generated, what prompts you used, and what you were going for.

### The Five Feedback Types

Mac (via the Feedback Elicitor) triages your feedback into one of five categories, each handled differently:

| Type | Your Signal | Example | Mac's Approach |
|------|------------|---------|----------------|
| **Clear** | Specific, actionable | "The guitar is too loud" | Direct mapping to parameter changes |
| **Positive** | You like it, want to evolve | "This is great! Can we try a darker version?" | Identify what to keep vs. evolve |
| **Vague** | Something is off but you cannot say what | "It just doesn't feel right" | Guided elicitation (see below) |
| **Contradictory** | Conflicting desires | "More energetic but also more chill" | First Principles reset |
| **Technical** | Audio quality issues | "There's a weird glitch" | Regeneration or Studio feature recommendations |

Mixed feedback is handled component by component -- clear and technical parts first, since resolving concrete issues often clarifies vague ones.

### How Mac Handles Vague Feedback

This is the feedback loop's core differentiator. When you know something is off but cannot articulate what, Mac uses a three-phase elicitation sequence:

**Phase 1: Binary Narrowing**
Reduces the problem space through yes/no questions across dimensions: music/production, vocals, energy, structure, lyrics, vibe. One question at a time.

```
Mac: Let's narrow this down. Is the issue more with the music/production,
     or with the vocals/lyrics?
You: The music, I think.
Mac: Okay -- is the instrumentation wrong, or is it more the energy/mood of the track?
You: The energy feels off.
```

**Phase 2: Comparative Anchoring**
Uses reference points to calibrate. Does not require musical knowledge.

```
Mac: On a scale of 1-10, where 1 is a quiet coffee shop and 10 is a packed arena,
     where does the current track land? And where do you want it?
You: It's at like a 7, and I want it at a 4.
```

**Phase 3: Emotional Vocabulary Bridge**
Presents opposing pairs so you can place the current output and your target on the spectrum:

```
Mac: Think of the production as a spectrum:
     Polished ←————→ Raw
     Where's the current track, and where do you want it?
You: It's way too polished -- I want it about 70% toward raw.
```

**Escape hatch:** If narrowing does not converge after 3-4 questions, Mac pivots: "Instead of narrowing down -- can you name a song or artist that sounds like what you wanted? I'll work backwards from there."

**Non-convergence fallback:** If elicitation still does not converge, Mac suggests generating 2-3 variants with different parameter profiles and letting you compare. This turns an elicitation problem into a selection problem.

### What the Adjustment Recommendations Look Like

After elicitation, Mac presents a structured recommendation package:

```
## Feedback Summary
You want rawer, less polished vocals with more intimate production -- closer to
a demo recording than a studio mix.

## Before/After Preview
Current sound: A polished indie folk track with clean, studio-mixed vocals and
full production.
Target sound: A raw, intimate porch recording with rough-edged vocals, minimal
processing, and room ambience.

## Style Prompt Adjustments
Current: "Warm indie folk, intimate lo-fi production..."
Recommended: "Raw indie folk, demo recording quality, rough-edged vocals..."
Changes:
- Replaced "intimate lo-fi" with "demo recording quality" for rawer production
- Added "room ambience, single-mic feel" for less polish
Confidence: High -- direct from your feedback

## Exclusion Prompt Adjustments
Recommended: "no heavy reverb, no studio polish, no auto-tune"

## Strategy Note
Generate 3-5 versions with the adjusted prompt -- Suno's randomness means one
may nail it without further changes.
```

### Profile Update Suggestions

If Mac notices a systematic preference (not just a one-song tweak), he suggests updating your band profile:

```
Mac: You've mentioned wanting rawer vocals twice now -- want me to update your
     band profile's vocal direction so future songs start from there?
```

### The Iteration Loop

You can keep refining. Each time you return with feedback, Mac loops back through the Feedback Elicitor for fresh triage. Adjustments compound, and the song converges on your vision.

```
Round 1: "Too polished" → Raw up the production
Round 2: "Better, but the chorus needs more impact" → Adjust chorus energy
Round 3: "That's it." → Save successful elements to profile
```

---

## 6. Direct Skill Access

Mac orchestrates four specialized skills. You can use them directly through Mac's menu or invoke them independently via slash commands.

**Slash commands:**
- `/bmad-suno-agent-band-manager` -- Talk to Mac (the orchestrating agent)
- `/bmad-suno-band-profile-manager` -- Manage band profiles directly
- `/bmad-suno-style-prompt-builder` -- Build style prompts directly
- `/bmad-suno-lyric-transformer` -- Transform lyrics directly
- `/bmad-suno-feedback-elicitor` -- Feedback analysis directly

### When to Use Skills Directly vs. Through Mac

| Use Mac When... | Use Skills Directly When... |
|-----------------|---------------------------|
| You want the full guided experience | You know exactly what you need |
| You want mode selection (Demo/Studio/Jam) | You want to skip the conversation |
| You want a complete package (lyrics + style + params) | You only need one piece (just a style prompt, just lyrics) |
| You are iterating and want Mac to track context | You are scripting/automating |

### Skill Quick Reference

| Menu Code | Skill | Standalone Use Case |
|-----------|-------|-------------------|
| **SP** | Style Prompt Builder | You already have lyrics and just need the sound description |
| **TL** | Lyric Transformer | You have text to convert and don't need a style prompt |
| **FE** | Feedback Elicitor | You want structured feedback handling without Mac's full orchestration |
| **MB** | Band Profile Manager | You want to create, edit, list, duplicate, or delete profiles directly |

### Lyric Transformer Options

| Code | Transformation | What It Does |
|------|---------------|--------------|
| ST | Structure Tagging | Adds section metatags (`[Verse]`, `[Chorus]`, etc.) |
| CE | Chorus Extraction | Finds existing hook material and promotes to chorus |
| CC | Chorus Creation | Writes a new chorus from the poem's emotional core |
| RA | Rhythmic Adjustment | Normalizes syllable counts for vocal phrasing |
| RE | Rhyme Enhancement | Strengthens rhyme patterns |
| FR | Full Rewrite | Complete rewrite as song lyrics (preserves theme) |
| CD | Cliche Detection | Flags overused phrases and suggests alternatives |
| WF | Word Fidelity Mode | Uses your exact words, only adds structure |

Note: FR and WF are mutually exclusive.

### Audio Analysis with External Tools

For detailed audio analysis of Suno output, three complementary tools are available:
- **librosa scripts** (included in the Feedback Elicitor) — programmatic BPM, key detection, tempo stability, and energy arc analysis. Run `analyze-audio.py` on a directory of MP3s for batch analysis, or `audio-deep-analysis.py` on individual tracks for deep dives. Requires Python 3 with librosa and numpy.
- **Gemini 3.1 Pro** — upload MP3 to Google AI Studio for AI-powered instrument identification, genre classification, and style prompt accuracy feedback. A two-pass workflow is mandatory for fusion genres.
- **ChatGPT** — upload MP3 for "blind" analysis (without the style prompt) to get unbiased genre and instrument identification. Useful for catching cases where the style prompt intent diverges from what Suno actually produced.

See the Feedback Elicitor's audio-analysis-workflow reference for detailed setup and prompting guidance.

### Improving Your Suno Prompting with A/B Testing

For users who want to systematically improve their style prompts, Gemini audio analysis enables a powerful A/B testing workflow:

1. Generate 2-3 versions of a song on Suno
2. Run each through Gemini blind (no style prompt provided) at 0.5 temp
3. Compare what Gemini hears to what you prompted
4. Change ONE variable (word position, tag, slider value), regenerate, and analyze again
5. Document what moved and what didn't

This replaces gut-feel prompt tweaking with systematic iteration. Mac can suggest this as an optional step after presenting a Suno package — just ask "can we A/B test this prompt?"

### Playlist Sequencing

Mac can assist with playlist/album ordering using both data and creative judgment. The workflow combines:

- **librosa scripts** — `playlist-sequencing-data.py` generates BPM, key (with Camelot wheel codes), energy levels, and transition quality ratings between adjacent tracks. `chord-progression.py` analyzes key centers over time within individual tracks.
- **Camelot wheel harmonic mixing** — key compatibility scoring based on DJ harmonic mixing principles (+/-1 number = safe, relative major/minor = mood shift, beyond +2 = intentional contrast)
- **Narrative sequencing** — Mac considers thematic arcs, emotional progression, and lyrical connections between songs alongside the sonic data

Tell Mac "help me order my playlist" or "sequence these songs for an album" and provide the audio files or sequencing data. Mac balances sonic flow (BPM transitions, key compatibility, timbral variety) with narrative progression (thematic arc, emotional journey) to suggest an ordering.

See the Feedback Elicitor's audio-analysis-workflow reference for the full sequencing methodology and Camelot wheel details.

---

## 7. Songbook & Memory

### Browse Songbook (menu code: SB)

The songbook is your creative portfolio -- past songs, successful prompts, iteration history, and creative evolution.

Mac scans these locations:
- `docs/songbook/` -- Saved lyrics from the Lyric Transformer
- `docs/feedback-history/` -- Iteration logs from the Feedback Elicitor
- `{project-root}/_bmad/_memory/band-manager-sidecar/chronology.md` -- Session timeline

Songbook entries should include a **Listening Notes** section — 2-3 lines capturing what the generation actually sounds like (how the intro opens, overall feel, standout sonic moments). Style prompts describe intent; listening notes describe reality. These diverge frequently and are critical for playlist ordering.

Songs are grouped by band profile (or "Unaffiliated" for one-offs). For each song, you can:
- **View details** -- Full lyrics, style prompt, parameters, iteration history
- **Reuse** -- Use a style prompt as a starting point for a new song
- **Compare** -- Side-by-side comparison of two songs
- **Export** -- All data in a copy-ready format

If your songbook is empty, Mac lets you know and offers to start your first song.

### How Mac Remembers Your Preferences

Mac stores learned preferences in `patterns.md` within the sidecar memory. Over time, this captures:
- Genre tendencies
- Vocal preferences
- Exclusions you consistently use
- Slider values that produce results you like
- Feedback patterns (e.g., you always want rawer vocals)

### How Session Memory Works

During a session, Mac tracks:
- Which band profile is loaded
- What songs you have created or refined
- Your interaction mode
- Creative context you have shared

The `index.md` file stores active work and essential context between sessions.

### Saving and Resuming Sessions

At the end of a song creation, Mac asks: "Good session. Want me to remember your preferences for next time?" If yes, he saves session context via the save-memory capability (menu code: **SM**).

When you return, Mac checks memory for active sessions or recent work and offers continuity:
- "Your band profile Midnight Porch is still loaded -- keeping that?"
- "Last time we were working on 'Jasmine House.' Want to continue, or start something new?"

---

## 8. Headless/Automation

> **This section is for scripting and batch workflows.** If you use Mac interactively, skip to [Troubleshooting](#9-troubleshooting).

All skills support headless (non-interactive) operation for scripting, batch processing, and automation.

### Headless Create-Song

**Input contract (JSON):**

```json
{
  "source_text": "optional -- poem or text to transform",
  "genre_mood": "required -- genre, mood, vibe description",
  "model": "optional -- default v4.5-all",
  "band_profile": "optional -- profile name to load",
  "creativity_mode": "optional -- conservative|balanced|experimental, default balanced",
  "instrumental": "optional -- true for instrumental-only",
  "language": "optional -- default English",
  "include_wild_card": "optional -- default false"
}
```

**Output:** Complete Suno package as structured JSON with no interaction. The Lyric Transformer runs if `source_text` is provided and `instrumental` is not true; the Style Prompt Builder runs with defaults; the package is assembled and returned.

### Headless Modes for Each Skill

**Style Prompt Builder:**
- `--headless` with profile name -- hybrid mode (profile baseline + overrides)
- `--headless:from-profile` -- generate from profile baseline only
- `--headless:custom` -- generate from provided parameters without profile
- `--headless:refine` -- accept existing prompt + adjustment deltas from Feedback Elicitor
- `--headless:migrate` -- reformat a prompt from one model to another

**Lyric Transformer:**
- `--headless` with text -- analyze + transform with balanced defaults
- `--headless:analyze` -- analyze input only, return analysis JSON
- `--headless:transform` -- full transformation with default options
- `--headless:refine` -- accept adjustment spec, apply targeted changes

**Feedback Elicitor:**
- `--headless` -- analyze + generate adjustments with balanced defaults
- `--headless:analyze` -- triage and categorize feedback only
- `--headless:adjustments` -- accept feedback + original prompts, return full adjustment recommendations

**Band Profile Manager:**
- `--headless` -- list all profiles as JSON array
- `--headless:create` -- create profile from provided YAML
- `--headless:validate` -- validate an existing profile
- `--headless:load <name>` -- read and return profile as JSON
- `--headless:edit <name>` -- accept YAML field overrides, apply and save
- `--headless:delete <name>` -- delete without confirmation
- `--headless:duplicate <source> <new_name>` -- copy profile

### Headless Error Contract

When required inputs are missing, headless mode returns structured JSON errors:

```json
{
  "error": true,
  "missing": ["genre_mood"],
  "message": "Required input 'genre_mood' not provided for --headless:custom mode."
}
```

### Batch Processing Concept

Headless modes enable batch workflows. Example: generate style prompts for multiple genre/mood combinations using a script that calls the Style Prompt Builder with `--headless:custom` for each entry, collecting the results.

---

## 9. Troubleshooting

### Common Issues and Solutions

| Issue | Likely Cause | Solution |
|-------|-------------|----------|
| Mac does not recognize my band profile | Profile name mismatch or missing file | Say "list profiles" to see available names. Profiles live in `docs/band-profiles/` as YAML files. |
| Style prompt is too long | Exceeded 1,000 characters (or 200 for v4 Pro) | Mac warns about this. Ask him to trim it. The critical zone is the first 200 characters. |
| Lyrics exceed Suno's limit | Over 3,000 characters | Ask Mac to condense. The Lyric Transformer tracks character budgets. |
| Mac asks too many questions | You are in Studio mode | Say "let's switch to Demo mode" for a faster experience. |
| Mac does not ask enough questions | You are in Demo mode | Say "let's go Studio mode" for the full songwriter's workshop. |
| Mac forgot my preferences | Session was not saved | Select SM (Save Memory) before ending your session. |
| Profile says wrong tier | Your Suno plan changed | Tell Mac "I upgraded to Pro" -- he updates memory and offers to update your profiles. Mac also detects tier drift when loading profiles. |
| Mutually exclusive transformation error | Selected FR + WF or other conflicts | Full Rewrite and Word Fidelity cannot be used together. Chorus Extraction is skipped if Full Rewrite is selected. |

### What to Do When Skills Are Unavailable

If an external skill fails to load, Mac informs you and offers a degraded path:

```
Mac: I can't reach my style prompt specialist right now, so I'll do my best --
     but you'll get better results once it's back.
```

Mac handles the work inline (e.g., generates a basic style prompt without model-specific optimization). He never silently fails or fabricates skill output.

### Suno-Specific Issues

For detailed troubleshooting of Suno platform issues (prompt formatting, audio quality, vocal artifacts, instrument bleed, metatag behavior), see the [Suno Reference — Troubleshooting](./SUNO-REFERENCE.md#troubleshooting-suno-issues).

### Getting Unstuck

If you are not sure what to do:
- Say "help" or describe what you are trying to accomplish -- Mac redirects gracefully
- If Mac seems confused about your intent, try stating it differently: "I want to make a new song" vs. "I want to refine an existing one"
- Check the menu -- select a capability by its code (CS, RS, MB, SP, TL, FE, SB, SM)
- For Suno-specific questions Mac cannot answer, consult [Suno's help center](https://help.suno.com)

---

## Quick Reference: Menu Codes

| Code | Capability | Description |
|------|-----------|-------------|
| **CS** | Create Song | Full song creation workflow |
| **RS** | Refine Song | Post-generation refinement |
| **SM** | Save Memory | Save session context |
| **MB** | Manage Bands | Band profile CRUD |
| **SP** | Build Prompt | Direct style prompt generation |
| **TL** | Transform Lyrics | Direct lyric transformation |
| **FE** | Elicit Feedback | Direct feedback analysis |
| **SB** | Browse Songbook | Browse past songs and history |
