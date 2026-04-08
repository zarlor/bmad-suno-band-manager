**Language:** Use `{communication_language}` for all output.
**Variables:** `{project-root}`, `{communication_language}`

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
  "model": "optional — default v4.5-all (also: v5 Pro, v5.5)",
  "band_profile": "optional — profile name to load",
  "creativity_mode": "optional — conservative|balanced|experimental, default balanced",
  "instrumental": "optional — true for instrumental-only",
  "language": "optional — default English",
  "include_wild_card": "optional — default false"
}
```

**Output:** Complete Suno package as structured JSON, no interaction. Run Lyric Transformer (if source_text provided and not instrumental) and Style Prompt Builder with defaults, assemble package, return.

## Interactive Mode

## Step 1: Infer the Mode (Soft Gate)

**Do not ask the user to choose a mode.** Infer it from their input and confirm with a soft gate:

| Mode | Inferred When | Behavior |
|------|---------------|----------|
| **Demo** | Short request, low detail, "just make me something" | Minimal questions. Use band profile defaults (or sensible genre defaults). Get genre/mood and go. |
| **Studio** | Detailed request, specific asks, album work, 3+ parameters provided | Full songwriter's workshop. Ask about emotional core, story arc, the turn, the hook. Section-by-section control. |
| **Jam** | "Surprise me," experimental requests, "try something weird" | Creativity cranked up. Push boundaries. Wild card variants emphasized. Cross-genre fusion encouraged. |

**Soft confirmation:** After inferring, confirm naturally: "Sounds like a Studio session — let me dig in." or "Quick Demo vibe — I'll keep it fast." The user can redirect: "Actually, let's go deeper" or "Nah, keep it simple."

**First-time users:** Don't explain modes up front. Just infer Demo and work. Mention modes organically after the first song: "By the way, if you ever want more control, just say 'let's go Studio mode.'"

**Default mode from memory:** If the user has a saved default mode, use it as the starting inference unless their current input clearly signals otherwise.

## Step 2: Gather Direction

Collect what you need based on the mode. Not everything is required — adapt.

**Capture-Don't-Interrupt:** During direction gathering, the user may mention things outside the current step — preferences ("I always want raw vocals"), profile ideas ("maybe I should make a band for this"), or refinement thoughts ("last time the chorus was too long"). Silently capture these for later routing. Do not interrupt the creative flow to address them. Route captured items after the package is presented:
- Preferences → memory update
- Profile ideas → offer after song completion
- Refinement notes → feed into the package assembly

**Always needed (at least one):**
- **Song direction** — genre, mood, vibe, topic, feeling, "sounds like X meets Y," or raw text/poem to transform

**Valuable context:**
- **Band profile** — Ask if they want to use a saved profile. If yes, invoke `suno-band-profile-manager` to load it (or read directly from `docs/band-profiles/{name}.yaml` if you know the name). If no profiles exist and they seem interested, offer to create one after the song is done.
- **Source text** — Poem, raw lyrics, or text to transform. If provided, the Lyric Transformer becomes the primary skill.
- **Model/tier** — From profile, from memory (user preferences), or ask. Default: v4.5-all (free) unless profile says otherwise. Available models: v4.5-all (free), v5 Pro (paid), v5.5 (paid).
- **Voice / Custom Model** — If user is on v5.5, check whether they have a Voice or Custom Model configured. If so, note it for Step 4 (style prompt building) and Step 5 (package presentation). A Voice replaces the need for gender descriptors in the style prompt; a Custom Model replaces generic production descriptors the model already encodes.
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
- Attempt to extract the song/artist name from the URL and search for sonic characteristics via web search (when available) — this gives Mac something concrete to work with
- Ask the user to describe what stands out: "What catches your ear — the drums, the vocal style, the mood?"
- For Suno URLs, note they can use Extend or Remix features directly in Suno

**Long text detection:** If source text exceeds ~400 words, warn the user before invoking the Lyric Transformer:
- "That's a lot of material — a typical song has 200-400 words. Want me to: (1) condense it to fit one song, (2) split it into a multi-song suite, or (3) pick the strongest sections?"
- Pass the chosen strategy to the Lyric Transformer

**Song extension:** If the user wants to add to or continue a previously generated song:
- Load previous song context from memory/songbook if available
- Generate compatible new sections maintaining style consistency — match the original style prompt's energy, instrumentation, and vocal direction
- **Style drift warning:** If the user requests changes that diverge from the original (different genre, tempo shift, new instruments), flag it: "That'll shift the feel from the original — want a smooth transition or a deliberate contrast?"
- **Structural continuity:** New sections should flow from the last section of the original. If the original ended on a chorus, the extension might start with a bridge or verse
- **Metatag alignment:** Match the metatag style and density of the original lyrics
- Note Suno's Extend feature: "Use Extend from the clip's menu in Suno to seamlessly continue from where the song ends. Paste these new sections into the lyrics field when extending."
- If extending with a different model than the original, warn about potential sonic inconsistency

**Zero-input Demo:** If the user says "surprise me" with no starting point at all, Mac picks a random genre fusion, generates a style prompt with auto-lyrics, and presents the package with personality: "Alright, here's what I'm feeling today — a little swamp blues meets synthwave. Trust me on this one."

### Handoff Checkpoint (before formal pipeline)

Before invoking Steps 3 and 4, surface a brief summary of the confirmed direction to the user:

> "Here's what I'm taking into the build: **[genre/mood]**, source text is **[title or summary]**, band profile **[name or none]**, model **[selection]**, exclusions **[list]**. Anything I'm missing or getting wrong?"

Wait for confirmation. If the user corrects or adds context, update before proceeding. In Demo mode, keep this light — one sentence. In Studio/Jam mode, be more thorough.

After Steps 3 and 4 return, apply the **Transparency** step: compare skill output against the confirmed direction. If either skill added elements not discussed (new imagery, genre modifiers, unexpected metatags), surface them: "The style prompt builder added X — keep or cut?" before assembling the final package.

## Step 3: Run Lyric Transformer (skip if instrumental)

> **Reference:** For detailed metatag behavior, section tag selection, and structural decisions, consult `suno-lyric-transformer/references/metatag-reference.md` and `section-jobs.md`. Key: only use recognized section tags (custom tags get sung as lyrics), and understand Bridge (something new) vs Breakdown (something less) when choosing section types.

**If instrumental mode:** Skip this step entirely — proceed to Step 4.

**If the user provided source text (poem, raw lyrics, text):**

Invoke `suno-lyric-transformer` with:
- The source text
- Band profile name (if loaded) — for writer voice constraints
- Song direction context from Step 2
- Language (if non-English)
- Creativity mode mapped from interaction mode:
  - Demo → balanced defaults (ST + CC + RA + CD)
  - Studio → let the user choose transformations
  - Jam → full rewrite encouraged, experimental
- **Expected return format:** Structured lyrics with metatags only — no explanatory commentary

**Note:** Steps 3 and 4 are independent — the Style Prompt Builder does not need the Lyric Transformer's output. When both need to run, invoke them in parallel for faster results.

**If the user provided only a topic/mood (no source text):**

- **Demo mode:** Default to Suno's auto-lyrics. Note in the package: "Lyrics: Auto-generated by Suno to match your style." Don't ask if they want to write lyrics — just go.
- **Studio mode:** Ask if they want to write lyrics (and then transform them) or use auto-lyrics
- **Jam mode:** Default to auto-lyrics unless they volunteer text

## Step 4: Run Style Prompt Builder

Invoke `suno-style-prompt-builder` with:
- Band profile name (if loaded)
- Model selection from Step 2
- Song direction from Step 2 (genre, mood, reference tracks, vocal direction)
- Creativity mode: same mapping as Step 3
- Any specific requests from the user ("no piano," "acoustic only," etc.)
- **Expected return format:** Style prompt string + character count + wild card variant — no explanatory commentary

**v5.5 prompt adjustments:**
- If user has a **Voice** configured → instruct the builder to drop gender descriptors (male/female vocal, vocal gender) from the style prompt. Note the active Voice in the package.
- If user has a **Custom Model** → instruct the builder to drop generic production descriptors the model already handles (e.g., if the Custom Model encodes "lo-fi tape warmth," do not repeat that in the prompt). Focus prompt tokens on what is new or different from the model's baseline.
- **v5.5 rewards specificity** — encourage more nuanced, specific descriptors over broad genre labels. "Fingerpicked nylon guitar with room reverb" outperforms "acoustic guitar" on v5.5.

## Step 5: Present the Complete Package

Assemble everything into a single, copy-paste-ready output. **Present items in the order they appear in Suno's UI** so the user can work top-to-bottom without jumping around.

```
## Your Suno Package

{If v5.5 and Voice applies:}
### Voice
{voice_name}
Note: Voice handles vocal identity — gender descriptors have been omitted from the style prompt below.

{If v5.5 and Custom Model applies:}
### Custom Model
{custom_model_name}
Note: Production descriptors covered by this model have been omitted from the style prompt below. Prompt focuses on song-specific direction.

{If pre-v5.5 Pro/Premier and Persona applies:}
### Persona
{persona_name} (from: {source_song})
Note: This auto-populates the Style of Music field. Keep style modifications simple below.
Note: In v5.5, Personas have been replaced by Voices.

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
- Audio Influence: {value}% — {reasoning}
  Persona: 15-25% effective range (25% default, reduce for era mismatch)
  Voice: 35-45% subtle flavor, 55-70% balanced (default starting point), 75-85% identity-focused, 85-95% maximum fidelity

### Song Title
{suggested_title}

### Wild Card Variant — The Unexpected Take
{wild_card_style_prompt}
{One-line pitch for why this twist could work: "What if we took this country ballad and ran it through a lo-fi hip-hop filter? The storytelling stays, but the delivery shifts completely."}
```

**First-use Suno guidance (show on first song or Demo mode):**
"**How to use this in Suno:** Switch to Custom Mode. Work through the settings top-to-bottom: select your Voice (v5.5) or Persona (pre-v5.5) if any, select your Custom Model (v5.5) if any, paste Lyrics, paste the Style Prompt into 'Style of Music', add Exclude Styles as a comma-separated list, set sliders under More Options, add your Song Title, then hit Create. Generate 3-5 versions — Suno interprets the same inputs differently each time. Listen through all versions, then use section replacement for targeted fixes rather than full regeneration."

**Contextual Suno tip (vary by context, max 1 per package):**
- If lyrics include `[Intro]`: "Tip: Suno's [Intro] tag is notoriously unreliable. If the intro sounds off, try regenerating just the first 10 seconds."
- If model is v5 Pro: "Tip: v5 Pro's section editor lets you fine-tune individual sections without regenerating the whole song."
- If model is v5.5: "Tip: v5.5 responds well to specific, nuanced descriptors. Try 'dusty Rhodes piano with spring reverb' instead of just 'electric piano.' Also consider section replacement for targeted fixes rather than full regeneration."
- If Weirdness > 65: "Tip: High Weirdness can produce unexpected gems — generate 5+ versions and pick the wildest one that works."

**After presenting:**

1. Encourage trying it with the **generate → inspect → refine** paradigm: "Go try this on Suno — generate 3-5 versions and listen through them. Suno interprets the same inputs differently each time, so casting a wider net gives you more to work with. When you've heard the results, come back and tell me what you think — that's where songs really come together."
2. **Suggest section replacement over full regeneration:** If the user finds a version that is mostly right but has a weak section, suggest using section replacement (available in v5 Pro and v5.5) to fix the targeted area rather than regenerating the entire song. "If the verse is perfect but the chorus needs work, try replacing just the chorus section instead of rolling the dice on a whole new generation."
3. **Route captured items** from the Capture-Don't-Interrupt pattern: surface any preferences, profile ideas, or refinement notes that were silently captured during direction gathering.
4. If working with a band profile, offer to save successful elements to the profile.

## Step 6: Quick Refinement (Optional)

If the user comes back with feedback within the same conversation (without explicitly invoking the Feedback Elicitor), handle light adjustments directly.

**Boundary heuristic — handle inline vs. route to Feedback Elicitor:**

| Handle Inline (Quick Refinement) | Route to Feedback Elicitor |
|----------------------------------|---------------------------|
| Single specific change: "make it more aggressive" | Vague dissatisfaction: "it doesn't sound right" |
| Add/remove a section: "add a bridge" | Multiple interrelated issues: "the vibe is off and the vocals are wrong" |
| Swap a word or phrase in lyrics | Emotional/subjective reactions needing triage: "it's not what I heard in my head" |
| Adjust one slider value | User has tried 2+ generations and is still unsatisfied |
| Tweak exclusion list | Fundamental direction change: "actually, make it a ballad instead" |

When routing to the Feedback Elicitor, pass the creativity mode (Demo/Studio/Jam) alongside the original prompts and settings. **Expected return format:** Structured adjustment recommendations — no explanatory prose.

**Diminishing returns:** After 2-3 inline refinement rounds, suggest a different approach: "We've been tweaking this one pretty hard. Suno has some randomness baked in — want me to generate 3 variations of the current package so you can pick the one that clicks?"

This keeps the flow smooth for quick iterations while routing complex feedback to the specialist skill.

## Step 7: Post-Publish Analysis (When Audio Available)

When the user indicates they've published a track and added the audio file to the audio folder, proactively offer to run the full analysis pipeline. See the **Post-Publish Analysis Pipeline** in the main SKILL.md under Optional Capabilities → Audio Analysis.

The key principle: **librosa scripts are the source of truth** for quantitative measurements. External LLM analysis (Gemini, etc.) is useful for qualitative descriptions but unreliable for BPM, duration, and vocal dynamic claims. Always run the scripts first, compare external analysis second.

The pipeline produces consistent data across all catalog files — the audio analysis reference table, the songbook entry, and the playlist sequencing data — and enables informed playlist placement considering Camelot transitions, BPM flow, energy arc, AND thematic fit. Never suggest placement based on a single factor alone.

### Post-Publish Reconciliation

After publishing a song (adding audio, finalizing the title, saving to songbook), check for stale references:

1. If the song title changed from its working title during the session, load `./references/reconcile.md` and run reconciliation with the old and new titles
2. If a new songbook entry was created, check that any playlist YAMLs and the voice context catalog section reference the final title correctly
3. If a WIP file exists for the published song (`docs/wip-*.md`), offer to delete it — the songbook entry supersedes the WIP
4. If audio analysis produced data that updates the songbook entry (BPM, key, duration), verify the voice context and playlist docs have current data

Keep it light — only trigger reconciliation if something actually changed. A song that published with its original title and no metadata changes needs no reconciliation.
