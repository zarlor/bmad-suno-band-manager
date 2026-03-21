---
name: create-song
description: Orchestrated song creation — gathers direction, runs Lyric Transformer + Style Prompt Builder, presents complete Suno-ready package.
menu-code: CS
---

# Create Song

The main creative workflow. Guide the user from initial inspiration to a complete Suno-ready package: structured lyrics with metatags + model-specific style prompt + exclusion prompt + parameter recommendations.

## Headless Mode

If invoked with `--headless` or structured JSON input, skip all interactive steps:

**Input contract:**
```json
{
  "source_text": "optional — poem or text to transform",
  "genre_mood": "required — genre, mood, vibe description",
  "model": "optional — default v4.5-all",
  "band_profile": "optional — profile name to load",
  "creativity_mode": "optional — conservative|balanced|experimental, default balanced",
  "instrumental": "optional — true for instrumental-only",
  "language": "optional — default English",
  "include_wild_card": "optional — default false"
}
```

**Output:** Complete Suno package as structured JSON, no interaction. Run Lyric Transformer (if source_text provided and not instrumental) and Style Prompt Builder with defaults, assemble package, return.

## Interactive Mode

## Step 1: Set the Mode

Ask the user (or infer from their energy/detail level) which mode fits this session:

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Demo** | "Just make me something," low detail, quick request | Minimal questions. Use band profile defaults (or sensible genre defaults if no profile). Get genre/mood and go. |
| **Studio** | Detailed request, specific asks, album work | Full songwriter's workshop. Ask about emotional core, story arc, the turn, the hook. Section-by-section control. |
| **Jam** | "Surprise me," experimental requests, "try something weird" | Creativity cranked up. Push boundaries. Wild card variants emphasized. Cross-genre fusion encouraged. |
| **Auto-detect** | User provides 3+ specific parameters (model, sliders, vocal direction, genre, metatags) in opening message | Implicit Studio — skip mode selection. Confirm: "Got it all — let me build your package." |

**If unclear:** Default to Demo for short requests, Studio for longer/detailed ones. Always mention the modes on first use so the user knows they exist.

**Persistence:** Defer this question to Step 5 — don't front-load administrative decisions into the creative flow.

## Step 2: Gather Direction

Collect what you need based on the mode. Not everything is required — adapt.

**Always needed (at least one):**
- **Song direction** — genre, mood, vibe, topic, feeling, "sounds like X meets Y," or raw text/poem to transform

**Valuable context:**
- **Band profile** — Ask if they want to use a saved profile. If yes, invoke `bmad-suno-band-profile-manager` to load it (or read directly from `{project-root}/docs/band-profiles/{name}.yaml` if you know the name). If no profiles exist and they seem interested, offer to create one after the song is done.
- **Source text** — Poem, raw lyrics, or text to transform. If provided, the Lyric Transformer becomes the primary skill.
- **Model/tier** — From profile, from memory (user preferences), or ask. Default: v4.5-all (free) unless profile says otherwise.
- **Reference tracks** — "Sounds like X meets Y" — capture these to pass to the Style Prompt Builder.

**Studio mode additional questions (songwriter's workshop):**
- "What's the emotional core of this song? What feeling should someone walk away with?"
- "Is there a story arc — a beginning, middle, turn?"
- "What's the one line you want stuck in people's heads?"
- "Any specific instruments, textures, or production choices you hear in your head?"
- "Vocal direction — who's singing this? What do they sound like?"

**Demo mode:** Skip the workshop. Infer what you can from the request + profile.

**Jam mode:** Ask one question: "Give me a starting point — a word, a feeling, a weird mashup idea — and I'll run with it."

**Instrumental detection:** If the user requests an instrumental ("make me an instrumental," "no vocals," "background music"), set instrumental mode:
- Skip Step 3 (Lyric Transformer) entirely
- Auto-populate exclusion defaults: "no vocals, no humming, no choirs, instrumental only"
- Note the Instrumental toggle for paid-tier users (Pro/Premier)
- Adjust package output to show "Lyrics: Instrumental (no vocals)" instead of a lyrics block

**Non-English detection:** If source text is not in English or user specifies a language:
- Acknowledge the language and note any known Suno behavior for that language
- Add the language as a style prompt element (e.g., "sung in French")
- Warn that metatag reliability may differ with non-Latin scripts
- Pass language context to the Lyric Transformer for adjusted analysis

**Reference track decomposition:** When the user provides "sounds like X meets Y" references:
- Decompose each reference into concrete sonic descriptors (instrumentation, vocal style, production, energy, era) — **show your work** before building so the user can confirm
- If you don't confidently know the artist, ask the user to describe what they like about their sound rather than guessing
- Store the decomposition alongside band profile data for reuse

**URL/audio detection:** If the user pastes a URL (YouTube, Spotify, Suno link):
- Acknowledge it and explain Mac cannot listen to audio
- Ask the user to describe what stands out: "What catches your ear — the drums, the vocal style, the mood?"
- For Suno URLs, note they can use Extend or Remix features directly in Suno

**Long text detection:** If source text exceeds ~400 words, warn the user before invoking the Lyric Transformer:
- "That's a lot of material — a typical song has 200-400 words. Want me to: (1) condense it to fit one song, (2) split it into a multi-song suite, or (3) pick the strongest sections?"
- Pass the chosen strategy to the Lyric Transformer

**Song extension:** If the user wants to add to or continue a previously generated song:
- Load previous song context from memory if available
- Generate compatible new sections maintaining style consistency
- Note Suno's Extend feature: "Use Extend from the clip's menu in Suno to seamlessly continue from where the song ends"

**Zero-input Demo:** If the user says "surprise me" with no starting point at all, Mac picks a random genre fusion, generates a style prompt with auto-lyrics, and presents the package with personality: "Alright, here's what I'm feeling today — a little swamp blues meets synthwave. Trust me on this one."

## Step 3: Run Lyric Transformer (skip if instrumental)

**If instrumental mode:** Skip this step entirely — proceed to Step 4.

**If the user provided source text (poem, raw lyrics, text):**

Invoke `bmad-suno-lyric-transformer` with:
- The source text
- Band profile name (if loaded) — for writer voice constraints
- Song direction context from Step 2
- Language (if non-English)
- Creativity mode mapped from interaction mode:
  - Demo → balanced defaults (ST + CC + RA + CD)
  - Studio → let the user choose transformations
  - Jam → full rewrite encouraged, experimental

**Note:** Steps 3 and 4 are independent — the Style Prompt Builder does not need the Lyric Transformer's output. When both need to run, invoke them in parallel for faster results.

**If the user provided only a topic/mood (no source text):**

- **Demo mode:** Default to Suno's auto-lyrics. Note in the package: "Lyrics: Auto-generated by Suno to match your style." Don't ask if they want to write lyrics — just go.
- **Studio mode:** Ask if they want to write lyrics (and then transform them) or use auto-lyrics
- **Jam mode:** Default to auto-lyrics unless they volunteer text

## Step 4: Run Style Prompt Builder

Invoke `bmad-suno-style-prompt-builder` with:
- Band profile name (if loaded)
- Model selection from Step 2
- Song direction from Step 2 (genre, mood, reference tracks, vocal direction)
- Creativity mode: same mapping as Step 3
- Any specific requests from the user ("no piano," "acoustic only," etc.)

## Step 5: Present the Complete Package

Assemble everything into a single, copy-paste-ready output. **Present items in the order they appear in Suno's UI** so the user can work top-to-bottom without jumping around.

```
## Your Suno Package

{If Pro/Premier and Persona applies:}
### Persona
{persona_name} (from: {source_song})
Note: This auto-populates the Style of Music field. Keep style modifications simple below.

{If v4.5+ Pro and Inspo applies:}
### Inspo
Recommended Inspo playlist: {list of 3-5 reference tracks}
Note: Use Inspo to channel this vibe before setting other parameters.

### Lyrics
{Complete transformed lyrics with metatags from Lyric Transformer}
{Or: "Lyrics: Auto-generated by Suno — set Lyrics Mode to Auto" if no lyrics created}
{Or: "Lyrics: Instrumental (no vocals)" if instrumental mode}

### Style Prompt ({model_name})
{character_count}/{limit} characters

{style_prompt}

{If character_count > limit: "⚠ This prompt exceeds Suno's {limit}-character limit and will be silently truncated. The last {overage} characters will be lost. Want me to trim it?"}

### Exclude Styles
{If Pro/Premier:}
{comma-separated list, e.g.: screaming vocals, steel guitar, autotune, heavy distortion}

{If Free tier:}
Not available on Free tier — exclusions are handled through positive phrasing in the style prompt above.

### Settings
{If free tier:}
- Vocal Gender: {recommendation}
- Lyrics Mode: {Manual or Auto}
- Note: Weirdness, Style Influence, and Audio Influence sliders are available on Pro/Premier plans

{If paid tier:}
- Vocal Gender: {recommendation}
- Lyrics Mode: {Manual or Auto}
- Weirdness: {value}% — {reasoning} (controls creative deviation: lower = safer, higher = more experimental)
- Style Influence: {value}% — {reasoning} (controls prompt adherence: lower = looser interpretation, higher = tighter to your style prompt)
{If Persona selected:}
- Audio Influence: {value}% — {reasoning} (controls resemblance to Persona source: 25-40% preserves character with musical freedom, 60-75% for closer voice match but may introduce artifacts at very high values)

### Song Title
{suggested_title}

### Wild Card Variant — The Unexpected Take
{wild_card_style_prompt}
{One-line pitch for why this twist could work: "What if we took this country ballad and ran it through a lo-fi hip-hop filter? The storytelling stays, but the delivery shifts completely."}
```

**First-use Suno guidance (show on first song or Demo mode):**
"**How to use this in Suno:** Switch to Custom Mode. Work through the settings top-to-bottom: select your Persona (if any), paste Lyrics, paste the Style Prompt into 'Style of Music', add Exclude Styles as a comma-separated list, set sliders under More Options, add your Song Title, then hit Create. Generate 3-5 versions — Suno interprets the same inputs differently each time."

**Contextual Suno tip (vary by context, max 1 per package):**
- If lyrics include `[Intro]`: "Tip: Suno's [Intro] tag is notoriously unreliable. If the intro sounds off, try regenerating just the first 10 seconds."
- If model is v5 Pro: "Tip: v5 Pro's section editor lets you fine-tune individual sections without regenerating the whole song."
- If Weirdness > 65: "Tip: High Weirdness can produce unexpected gems — generate 5+ versions and pick the wildest one that works."

**After presenting:**

1. Encourage trying it: "Go try this on Suno! When you've heard the result, come back and tell me what you think — that's where songs really come together."
2. **Persistence check (deferred from Step 1):** "Good session. Want me to remember your preferences for next time?" If yes, offer to save session context via save-memory.
3. If working with a band profile, offer to save successful elements to the profile.

## Step 6: Quick Refinement (Optional)

If the user comes back with feedback within the same conversation (without explicitly invoking the Feedback Elicitor), handle light adjustments directly:

- **Clear, simple tweaks** ("make the style prompt more aggressive," "add a bridge to the lyrics") — adjust and re-present
- **Deeper feedback** ("it doesn't sound right," "the vibe is off," vague reactions) — route to `bmad-suno-feedback-elicitor` for structured elicitation, passing the creativity mode (Demo/Studio/Jam) alongside the original prompts and settings

This keeps the flow smooth for quick iterations while routing complex feedback to the specialist skill.
