# Suno Studio & Editor Reference

Comprehensive reference for Suno's post-generation editing tools. This covers **Suno Studio** (Premier-only full DAW), the **Legacy Song Editor** (Pro/Premier section-level editor), and all related features. Companion to the [Suno Reference](SUNO-REFERENCE.md) (which covers prompting, models, and generation) and the [Usage Guide](USAGE.md) (which covers Mac's workflows).

> **Last validated:** April 6, 2026 (Suno Studio v1.2, Legacy Editor, v5.5 Pro). Updated with community workflow findings for Replace Section, Heal Edits, Remaster, Remove FX, Warp Markers, EQ, and credit waste prevention. Suno updates Studio features frequently — use web search to verify capabilities against current documentation when uncertain.

---

## Two Editing Environments

Suno provides two distinct editing tools:

| Environment | Tier | Purpose |
|-------------|------|---------|
| **Legacy Song Editor** | Pro + Premier | Section-level waveform editor for quick fixes — replace, extend, crop, fade, rearrange |
| **Suno Studio** | Premier only | Full browser-based Generative Audio Workstation (GAW) — multitrack timeline, AI generation, recording, mixing, EQ, export |

**Key distinction:** The Legacy Editor works on individual songs. Studio works on multitrack projects with multiple clips, stems, and recordings on a timeline. Most Pro-tier users will use the Legacy Editor; Premier users get both.

---

## Legacy Song Editor (Pro + Premier)

### Access

From Library or Create view, click the three-dot menu (...) on any song → select **Edit**.

### Replace Section (Inpainting)

The most important editing feature. Regenerates a selected portion while preserving the rest. Suno uses surrounding audio context to blend new content seamlessly.

**How to use:**
1. Highlight a region on the waveform (**15-20 seconds** is the sweet spot for section length — under 5 seconds produces disjointed transitions, over 30 seconds and the model loses the melodic thread. 10-30 seconds works, but 15-20 is optimal (community consensus).)
2. Optionally modify lyrics in the Replace Lyrics box
3. Click "Replace Section" / "Recreate Section"
4. Two alternate versions appear in the Edits Library
5. Fine-tune transitions by dragging boundary lines on the waveform
6. Click "Generate More" for additional options

**Settings:**
- **Keep Duration / Make Same Length**: Toggle. ON = replacement matches original length. OFF = Suno has creative flexibility to extend or shorten — useful for adding solos, breaks, or drum fills.
- **Instrumental Mode**: Toggle. Removes vocals while preserving the music in the replacement.
- **Replace Lyrics**: Edit the lyrics for just the selected region.

**Tips:**
- **15-20 seconds** is the sweet spot for section length — under 5 seconds produces disjointed transitions, over 30 seconds and the model loses the melodic thread. 10-30 seconds works, but 15-20 is optimal (community consensus).
- Replace typically requires **2-5 attempts** for seamless transitions — generate multiple alternates
- Replaced sections may feel tonally mismatched; fine-tune by adjusting boundary lines
- Produces **higher vocal clarity** than Extensions due to enhanced internal blending
- "Prompt for identity, edit for reality" — prompts set genre/emotion/structure; edits fix timing, sections, and version selection
- Write 2-3 alternate lyric versions, then use Replace to hear each in context

**When to use Replace vs. full regeneration:**

| Situation | Recommendation |
|-----------|---------------|
| Structure and melody are good, one section has bad vocals | Replace Section |
| Structure is good, multiple sections need different fixes | Sequential replacements |
| Melody is wrong throughout | Full regeneration |
| Overall vibe/genre is off | Full regeneration with revised style prompt |
| Good material but wrong emotional direction | Full regeneration — emotion is global |

**Production-Tested Limitation (2026-04-29 — single-word fix attempt):**

Even at the documented sweet-spot scale (single-word / short-phrase target), Replace Section can produce **audible transition seams at the section boundaries**. Lenny's Damned If I Don't fix attempt: targeted a single word (`-ing` suffix dropped on "They call it living") with phonetic anchor `They call it liv-ing` in the Replace Lyrics box. **Both returned variations correctly fixed the targeted word** but **both also produced obviously audible joins** where the new replacement section met the surrounding original audio. Replace Section's localized-fix value is therefore bounded by transition-quality, not just by section size.

**Practical takeaway:** Even within Replace Section's documented sweet-spot, expect to evaluate transition smoothness alongside content correctness. If the fix lands the content but the seams are obvious, the song-level result may not be acceptable — fall back to Cover (full re-render preserving structure) or full re-gen with phonetic anchor in lyric source. Cover and re-gen produce single-coherent audio without seams; Replace Section's localized scope means transition seams are an inherent risk.

**Cost:** Pro and Premier currently receive free replacements up to 1,000 sections daily. After promotional period, each replacement costs 5 credits per Suno's documentation (4 credits / 2 variations observed in production 2026-04-29 — verify current cost via Suno UI before estimating credit budget).

### Extend

Adds new musical content as a continuation of the existing track.

**How to use:**
1. Click the plus icon at the far right of the track
2. Enter a custom prompt or select "Quick Extend" for seamless continuation
3. Use structural metatags (`[Chorus]`, `[Outro]`, `[Bridge]`) to guide what type of section is generated

**Tips:**
- Extensions generate ~30-60 seconds of additional content
- Extend first, then refine problem areas using Replace Section
- **62% of extended tracks drift from the original prompt** — keep extensions short (30s-1min increments) and match the style prompt exactly
- Include metatags to control section type

### Crop / Remove

Trims songs by selecting waveform ranges. Does NOT regenerate audio — it only removes portions.

**How to use:** Three-dot menu → Edit → Crop Song. Click and drag to highlight the portion to keep, then click "Crop Song." Edited version auto-saves to Library.

**Tips:**
- Good for removing long intros/outros, isolating sections, creating short-form clips
- Auto-fade is applied when cropping the end of a song
- Non-destructive to original — a new version is created

### Fade In / Fade Out

**How to use:** Fade In/Out icons appear in the bottom corners of the first and last sections. Click once to create a fade, hover to highlight the faded area, click and drag to adjust length.

**Tips:**
- For generation-level fades (built into the audio itself), use `[Fade Out]` paired with `[End]` tags in lyrics
- Using `[Fade Out]` alone may produce abrupt or incomplete endings — always pair with `[End]`
- Editor fades are applied post-generation and are more controllable

### Rearrange

**How to use:** Hover over a section name to see the grab tool, then click and drag to move the section. A plus icon between sections creates new content areas.

**Tips:**
- Good for swapping verses, moving choruses, reordering bridges
- Transitions may sound rough after rearranging — use Replace Section on the transition points to smooth them

### Split

Available via the More Actions button (three dots) on any section. Splits a section at a specific point, allowing independent editing of each half.

### Edit Displayed Lyrics

Controls publicly visible lyrics without changing audio. Fixes transcription errors, removes duplicated lines, cleans formatting. Typically a final polish step.

### Edits Library

The right panel that collects all alternate versions generated during editing. Browse, preview, and select the best take for each section. Click "Generate More" to create additional options.

---

## Suno Studio (Premier Only)

### Access

Select the **Studio** icon under **Create** in the left sidebar at suno.com. Desktop only.

### What It Is

A browser-based multitrack workspace that merges traditional DAW functionality with AI-powered generation. Built on technology from WavTool (acquired by Suno in June 2025). Think of it as a DAW where your instruments are AI generators, recordings, uploads, and stems.

### Interface Overview

- **Timeline**: Main multitrack workspace. Spacebar = play/pause.
- **Context Bar** (bottom): Dynamic toolbar — Create Panel (generate new), Library Panel (import existing), Upload Audio (import files).
- **Details Panel** (right side): Opens when selecting items. Remix/Edit options, individual stem insertion controls, Clip Settings.
- **Transport Bar** (bottom): Playback controls, record functionality, upload options.

### Clip Settings

When selecting a clip in Studio, the Details Panel offers:
- **Color**: Visual organization
- **On Beat** toggle: Locks clip to grid tempo vs. original timing
- **Transposition**: Semitone adjustments (pitch shift)
- **Speed**: Playback speed adjustment
- **Volume**: Per-clip volume control

### Context Window (v1.1)

A visually marked region above tracks that determines what audio Suno considers when generating new clips. Content outside this region is ignored.

**How to use:** Drag edges to expand or shrink the context region. On Mac, hold modifier key to disable snap-to-grid for precise adjustments.

**Why it matters:** This is critical for targeted generation — you can generate a drum variation that only listens to a specific bar, or protect earlier sections from influencing later generations. Without understanding the Context Window, users may get unexpected results from Studio generation.

### Automatic Saving

Studio auto-saves projects with timestamped **Versions** accessible through the Project Menu. No manual saves needed.

---

## Studio Features

### Warp Markers (Studio v1.2, Premier)

Enables timing adjustments on audio clips with minimal distortion via time-stretching. Corrects drift, tightens choruses, aligns phrasing — all without regeneration and without altering pitch.

**How to use:**
1. Enable **Edit Mode** on a clip
2. Click the waveform to add markers at points you want to adjust
3. Drag markers to shift audio timing at that specific point

**Modes:**
- **Manual**: Click directly on the waveform at the adjustment point
- **Auto**: Automatically sets markers on each transient (beat/hit)

**Quantize**: After placing warp markers, use the **Quantize** function to lock timing to the grid so everything aligns to the tempo.

**Best use cases:**
- Tightening a chorus by locking drums and bass to the grid
- Fixing gradual tempo drift or slip
- Correcting rushed vocals with subtle nudges
- Groove shaping (use cautiously — artifacts expose here)

**Limitations:**
- Time-stretching creates artifacts, especially with extreme corrections or sharp transients
- Start conservative and audition before exporting
- If corrections are extreme, regeneration is better than warping

**Genre-specific quantize guidance:**

| Genre | Tightness | Approach |
|-------|-----------|----------|
| EDM | Very tight | Medium-to-strong quantize OK |
| Trap | Medium | Maintain bounce; avoid full lock |
| Afrobeat | Light-medium | Small warp edits; preserve groove |
| Soul/R&B | Light | Prioritize feel; minimal changes |

Source: [Fix Timing with Warp + Quantize — Jack Righteous](https://jackrighteous.com/en-us/blogs/guides-using-suno-ai-music-creation/fix-timing-warp-quantize-suno-studio-1-2)

**Decision rule:** Edit timing if the musical idea works but the execution fails. Regenerate if the concept itself is wrong.

**Troubleshooting:** "After quantize, sounds weird" → Undo, re-quantize lighter, target only the worst region, use manual markers for specific hits, or regenerate and audition alternates.

### Alternates / Take Lanes (Studio v1.2, Premier)

An improved system for creating, previewing, and selecting between multiple generated variations of a section on a single track.

**How to use:**
1. Generate new content — two versions appear as **Take Lanes**
2. The main track shows Version 1
3. Use speaker icons to audition alternatives
4. Preview alternates in the Edits Library on the right
5. Click "Generate More" for additional options

**Comping:** Select preferred portions from each take version. Copy chosen edits to the Main Track. This allows combining the best parts of different takes.

**Best practices:**
- Generate 2-6 alternates with **one controlled change each** (e.g., "bigger melody / simpler drums" or "same hook / stronger rhythm")
- Audition in context (not solo) for the best selection
- Select the best overall take, then comp micro-details if needed
- Single-change alternates prevent losing song identity during comping
- "Too many versions, stuck?" → Choose the version that best supports the song's message, not the coolest individual detail. Commit and move forward.

### Remove FX (Studio v1.2, Premier)

Strips reverb and delay effects from audio clips, generating a dry version placed on the timeline.

**How to use:** Right-click any clip in Studio → select **"Remove FX"**

**Best use cases:**
- Wet vocal rescue when reverb drowns clarity
- Stem cleanup before mastering in an external DAW
- Rebuilding space with your own reverb/delay settings for emotional control
- "Dry first, then add space" workflow

**Limitations:**
- Results vary — heavily "printed" character from generation may partially persist
- Sometimes sounds thinner (spatial effects add perceived body)
- Works best on clips where effects were added during generation rather than being baked into the performance character
- **Can increase loudness by up to 5 LUFS** — check clip levels after applying to avoid clipping
- **Recommended workflow**: 'Prompt moderately dry, Remove FX only where needed, export multitrack, rebuild FX chain intentionally' (Jack Righteous)

**Troubleshooting:** "Remove FX sounds thinner" → Expected sometimes. Export and rebuild with EQ, compression, and custom reverb in your DAW. Or blend the original (wet) with the cleaned (dry) clip.

### EQ (Studio v1.1, Premier)

6-band per-track parametric equalizer for tonal shaping without leaving Studio.

**How to access:** Select a track → click **"Track"** in the Details Panel → EQ controls.

**Specifications:**
- 6 selectable bands (numbered 1-6), individually enable/disable
- Toggle switch (top-left) enables/disables EQ processing
- Frequency response graph with draggable control points
- Live spectrum analyzer
- 11 presets: Flat/Reset, High-pass, Vocal, Warm, Presence, Bass Boost, Air, Clarity, Fullness, Lo-fi, Modern

**Filter types:** Bell/Peak, High-pass, Low-pass, High-shelf, Low-shelf, Notch

**Parameters per band:**
- **Freq**: Center frequency
- **Gain**: -12dB to +12dB
- **Res (Q Factor)**: Narrow (surgical) to wide (musical)

**Tips:**
- Start with subtle adjustments (+/-3dB)
- Prefer cuts over boosts for natural results
- Common moves: cut 200-400Hz for mud, boost 2-5kHz for presence, cut 3-4kHz for harshness, boost >10kHz for air
- **AI shimmer artifacts**: Roll off ultra-highs on stems where noticeable — Suno's generation can produce high-frequency shimmer that EQ can tame
- Use the Vocal preset as a starting point for vocal clarity, then fine-tune

### Time Signature (Studio v1.2, Premier)

Allows composing beyond standard 4/4 time. Supports signatures like 6/8, 7/8, 11/4, and other meters.

**How to access:** Time signature picker in the bottom info panel of Studio. Set numerator (1-99 beats per bar) and denominator (beat duration).

**IMPORTANT limitation:** This setting is **NOT yet sent to generative models** when creating new clips. It affects the grid, metronome display, and editing alignment — but does NOT influence AI generation. You still need to prompt for the desired meter via style prompt or lyric metatags.

**Best practices:**
- Set meter early so edits and quantize decisions stay coherent
- Useful for: 6/8 worship feels, odd-meter tension (7/8, 11/4), syncopated hooks where grid precision matters

### Heal Edits (Premier)

Smooths transitions at edit/cut points where audio clips meet.

**How to use:** Right-click a region → **"Heal Edits"**

**When to use:** After cropping, rearranging, or replacing sections where the transition sounds rough or has artifacts at the cut point.

**Technique:** After committing a Replace Section, apply Heal Edits on the **following** section (not just the edit point) to blend tonal shifts and timbre changes between edited and original audio. If the voice timbre shifts, run Heal Edits and trim its range to target just the boundary area.

**Limitations:** Subtle effect — some users report not noticing a difference. Works best on regions where two different takes/generations meet. Can be targeted to specific parts of regions rather than whole sections.

### Recording (Premier)

Record audio directly into Studio via microphone.

**How to use:**
1. Add a track → select Input → choose microphone
2. Grant browser permissions
3. Use headphones (prevents feedback)
4. Enable metronome if desired
5. Arm track (red Record button) → press Record on Transport
6. Recorded audio uploads to Timeline after recording completes

**Transforms:** Drag recorded audio into the Create panel to generate new material. Example: a sung melody becomes a string orchestra, finger taps become drums. Adjust Audio Influence in Advanced Options to control how closely the generation follows the recording.

### Loop Recording (Studio v1.1, Premier)

Continuous recording of multiple takes over the same time range.

**How to use:**
1. Enable loop icon in transport controls
2. Set loop start and end points
3. Press Record — each pass creates a separate take/layer
4. Access all takes via "Show Take Lanes" icon

**Use cases:** Vocal takes, instrument solos, bass lines, layering multiple performances.

### Sounds Mode (Premier, Beta)

Generate custom sound effects, samples, and loops from text prompts.

**How to access:** Create → Custom mode → select **"Sounds"** from dropdown.

**Settings:**
- **Type**: One Shot vs. Loop
- **BPM**: Lock to tempo
- **Key**: Lock to key

Generates two options per prompt. Categories include: sound effects, ambient backgrounds, foley, animal sounds, musical samples (808 kicks, snares, loops).

### Stem Cover (Premier)

Takes any clip in Studio and covers it into a different sound/instrument while retaining melody and rhythm.

**How to use:** Select a clip in Studio → apply Cover function with desired instrument/sound prompt. Receive two generations per prompt in Take Lanes.

**Example:** Covering finger taps into a 70s soul drum fill. Covering a guitar stem into a synth pad.

**Cover vs. Recreate:** Cover references the original source audio used to generate a clip (even if you cover a guitar stem that came from a ukulele, it references the original ukulele). Recreate uses the currently selected audio as the source — enabling iteration on already-covered stems.

### Studio Export Options

| Export Type | What It Does |
|-------------|-------------|
| **Full Song** | Complete mix of all tracks and processing |
| **Selected Time Range** | Only the chosen timeline section |
| **Multitrack** | All tracks as separate stems within the Studio mix context |
| **Individual Clip** | Right-click any clip → "Download .WAV" |
| **Wave Tempo Locked** | Stems set to average BPM for DAW alignment |
| **WAV + MIDI bundle** | Audio + MIDI data together |

All exports are high-quality WAV files.

### MILO-1080 Step Sequencer (March 2026, Premier)

A 16-track step sequencer and synth designer:
- Text-to-sound generation for creating samples
- Pull clips from Suno track library
- Built-in synth engine for manual sound design
- MIDI input/output for hardware integration
- Targets experienced producers and beatmakers

---

## Stems (Pro + Premier)

### What It Does

AI-powered separation of a mixed track into individual component tracks. Suno exports individual generation layers directly rather than performing post-hoc source separation, yielding cleaner results than third-party tools like LALAL.AI or Demucs.

### Two Modes

| Mode | Output | Tier |
|------|--------|------|
| **2-stem** | Vocals + Instrumental | Pro + Premier |
| **12-stem** | Up to 12 individual parts | Pro + Premier |

### 12-Stem Categories

Vocals, Backing Vocals, Drums, Bass, Guitar, Keys, Strings, **Brass**, Woodwinds, Percussion, Synth, FX.

**Note:** Brass separates well as a dedicated stem — this makes stems the recommended approach for songs requiring section-specific instrumentation (e.g., brass only in the outro).

### How to Access

- **Library/Workspace**: Click More Actions (...) → hover over "Get Stems" → choose 2-stem or 12-stem
- **Legacy Editor**: "Get Stems" icon at top right
- **Studio**: Stems panel — click arrow icons next to each stem to add to Timeline. Click three dots next to any stem's arrow for additional options. "Insert All" adds all stems at once.

### Processing

Takes 30-60 seconds depending on track length. Progress indicator shown. After completion, solo/mute individual stems during playback preview.

### Export Formats

- MP3
- WAV
- **Tempo-Locked WAVs** (stems set to average BPM of the song)
- MIDI files (10 credits per stem, Premier only)
- WAV + MIDI bundles

### The Stems Workflow for Section-Specific Instrumentation

When a song needs different instruments in different sections and prompting alone can't achieve it:

1. **Generate** with ALL desired instruments in the style prompt (accepting bleed into all sections)
2. **Extract stems** — up to 12 individual tracks
3. **Edit in a DAW** (e.g., Audacity) — mute/remove unwanted instrument stems per section
4. **Export** the final mix

**IMPORTANT:** External DAW editing is a one-way operation. Once you edit outside Suno, you lose Suno's editing capabilities (Replace Section, Extend, etc.) on that version. Complete all Suno edits BEFORE exporting to a DAW. Always keep the original Suno generation as a source of truth.

**Mastering note:** Suno applies an aggressive mastering limiter. For professional release, export raw stems and mix in a dedicated DAW for proper EQ, compression, and spatial processing.

---

## Remaster (Pro + Premier)

### What It Does

Generates refined variations of existing clips by adjusting production details (instrument balance, audio effects, mix quality, sonic character, vocal clarity/pronunciation) while preserving core song structure.

### How to Access

Click three-dot menu on any clip → Create → **Remaster**.

### Variation Strength

| Strength | Effect |
|----------|--------|
| **Subtle** | Very close to original — only small acoustic/production details changed |
| **Normal** (default) | Maintains duration and style with minor musical adjustments |
| **High** | More noticeable differences, including possible changes to musical elements and vocals |

### What Remaster Does NOT Do

- Change lyrics
- Drastically alter musical style
- Replace the vocalist (use Cover instead)
- Modify timing or arrangement

### Community Observations

- Remaster is a **full regeneration** using the current model — NOT an EQ pass or filter. Creates 2 new versions and consumes standard credits.
- **'Improved fidelity with reduced soul'** — instrumentals benefit more than vocal tracks. Vocals can lose emotional intensity or edge.
- **Stacking** (remastering remastered tracks): Helpful for instrumentals and ambient/cinematic music. Hurts lead vocal clarity, emotional phrasing, and lyrical intelligibility.
- **Genre softening**: Aggressive styles (metal, punk) may lose their edge after remastering. Minor tonal drift after multiple passes.
- **One pass is usually sufficient.** 'Always trust the version that resonates' — don't chase fidelity at the expense of emotional feel.

Sources: [Suno Remaster Guide — Jack Righteous](https://jackrighteous.com/en-us/blogs/guides-using-suno-ai-music-creation/suno-ai-remaster-guide-v4)

### Remaster vs. Cover

**Remaster** = subtle production polish (same identity). **Cover** = significant transformation (new genre, vocalist, arrangement).

### When to Use

- The song is 90% there but the mix feels rough
- Vocal clarity or pronunciation needs a nudge
- You want production polish without touching lyrics, melody, or structure
- Before exporting to ensure the best possible audio quality

---

## Add Vocals / Add Instrumental (Pro + Premier, Beta)

### Add Vocals

Layers a custom AI-generated vocal based on lyrics you provide onto an instrumental track.

**How to access:** Library or Workspaces → More Actions (...) on a valid instrumental track → "Add Vocals" → input lyrics → Create.

**Compatible tracks:** Uploaded instrumentals, generated instrumentals (via Instrumental toggle), or stems extracted from existing songs.

**Audio Strength slider** (Advanced Options): Determines how much the new vocal adheres to the existing instrumental. For best results, describe the existing instrumental + desired vocal characteristics in the style box.

### Add Instrumental

Generates instrumentation behind an existing vocal track.

**How to access:** Create → click audio button → upload your vocal track → trim if needed → hover over Remix/Edit → "Add Instrumental."

**Audio Influence** (Advanced Options): Set up to 100% for maximum adherence to original vocals. Suno transcribes lyrics automatically.

---

## MIDI Export (Premier Only)

### What It Does

Extracts MIDI data from audio stems, generating standard MIDI files representing melodic or rhythmic content.

### How to Access

1. Extract stems from your clip using the Stems panel
2. Click on the stem you want
3. Select **"Get MIDI"** from the context menu

### Cost

**10 credits per stem** for MIDI extraction.

### Export Formats

Standard MIDI files compatible with any DAW. Available as standalone MIDI or WAV + MIDI bundles.

### Use Cases

- Recreating melodies with different instruments in your DAW
- Analyzing harmonic progressions
- Building new arrangements from Suno generations
- Hardware integration via MIDI

---

## Covers in Editor Context (Pro + Premier, Beta)

### Standard Covers

Recreates an existing song in a new musical style while preserving melody and structure. Generates a full re-performance, not a remix of the existing recording.

**How to access:** Three-dot menu → Create → **Cover Song**. Describe the new style. Optionally adjust lyrics.

**Compatible inputs:** Suno-generated songs, uploaded audio (demos, voice memos, loops), instrumentals, vocal tracks.

**CRITICAL:** Covers are **NOT eligible for commercial use** — even on your own songs. For commercial releases, create a fresh generation instead.

### Stem Cover (Studio, Premier)

Covers individual stems into different instruments/sounds while keeping melody and rhythm. See the Stem Cover section under Studio Features above.

---

## Creative Sliders in Studio Context

When generating within Studio, the sliders behave the same as in standard generation but with these practical ranges:

| Slider | Conservative | Balanced | Experimental |
|--------|-------------|----------|--------------|
| **Weirdness** | 35-45 | ~50 | 55-70 |
| **Style Influence** | 70-85 | 60-70 | 45-60 |
| **Audio Influence** | 60-75 (dominant upload) | 40-60 | 20-40 (texture only) |

Audio Influence is only active when an upload or recording is used as a source.

---

## v5.5 Editing Workflow Paradigm

v5.5 favors an iterative **generate → inspect → section replace → refine** workflow over full regeneration. This preserves good material and spends fewer credits.

### Recommended Workflow

1. **Generate** the initial output from the song package
2. **Inspect** the full result — evaluate structure, melody, emotional angle, and production
3. **Section replace** any sections that need work (preserve sections that are good)
4. **Refine** with targeted adjustments (delivery metatags, slider tweaks, specific prompt edits)

### Critical Checkpoint Questions

Before spending credits on regeneration:
- **Is the structure correct?** If yes, do NOT regenerate from scratch — use section replacement.
- **Is the melody usable?** A good melody with flawed production is worth refining. A bad melody needs regeneration.
- **Does the emotional direction justify more credits?** If heading the right way, refine. If the emotional core is wrong, regenerate.

### Credit Waste Prevention

Track your credit spend per song to avoid diminishing returns:
- **0-50 credits**: Learning and experimentation phase — explore freely
- **50-80 credits**: Apply discipline — target specific problems, stop perfection-chasing
- **80+ credits**: Stop editing and export — you're past the point of meaningful improvement

'Prompt for identity, edit for reality' — use generation for genre/emotion/structure, use Studio tools for execution problems (timing, wetness, take selection, arrangement).

Source: [Cut Credit Waste — Jack Righteous](https://jackrighteous.com/en-us/blogs/guides-using-suno-ai-music-creation/suno-studio-1-2-reduce-credit-waste)

---

## Tier Summary

| Feature | Free | Pro ($10/mo) | Premier ($30/mo) |
|---------|------|-------------|------------------|
| **Legacy Editor** (Replace, Extend, Crop, Fade, Rearrange) | No | Yes | Yes |
| **Stems** (2-stem and 12-stem) | No | Yes | Yes |
| **Add Vocals / Add Instrumental** | No | Yes (beta) | Yes (beta) |
| **Covers** | No | Yes (beta) | Yes (beta) |
| **Remaster** | No | Yes | Yes |
| **Suno Studio** (full GAW) | No | No | Yes |
| **Warp Markers** | No | No | Yes |
| **Remove FX** | No | No | Yes |
| **Alternates / Take Lanes** | No | No | Yes |
| **EQ** (6-band per track) | No | No | Yes |
| **Time Signature** control | No | No | Yes |
| **Context Window** | No | No | Yes |
| **Recording** (microphone) | No | No | Yes |
| **Loop Recording** | No | No | Yes |
| **Sounds Mode** (text-to-sound) | No | No | Yes |
| **Stem Cover** | No | No | Yes |
| **Heal Edits** | No | No | Yes |
| **MIDI Export** (10 credits/stem) | No | No | Yes |
| **MILO-1080 Sequencer** | No | No | Yes |

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Replaced section sounds tonally mismatched | Context blending imperfect | Fine-tune boundary lines; try 2-5 more replacements; reduce section size |
| Extended section drifts from style | 62% of extensions drift from prompt | Keep extensions short (30s-1min); match style prompt exactly; use metatags |
| Cover truncates around 3 minutes | Known Cover limitation | Generate shorter source; use Extend after covering |
| Remaster artifacts persist | Baked-in generation artifacts | Try Remaster at different strength levels; or regenerate from scratch |
| Warp markers sound weird after quantize | Over-correction | Undo, re-quantize lighter, target worst region only, use manual markers |
| Remove FX sounds thin | Spatial effects add perceived body | Export and rebuild with your own reverb/EQ in a DAW; blend wet + dry |
| MIDI export doesn't match audio | MIDI extraction is approximate | Use as a starting point; hand-edit in your DAW |
| Time signature doesn't affect generation | Not yet sent to generative models | Set for grid/editing alignment only; prompt for desired meter |
| Studio generation ignores earlier sections | Context Window too narrow | Expand the Context Window to include the sections you want Suno to reference |
| 'Scratched CD' effect — track loops/skips | v5 bug: repetitive loop in first 20 seconds | Regenerate — no known fix beyond regeneration |
| Replace Section lyrics don't update | 'Lyric Cache' bug on subsequent attempts | Use Cover on original source track with Persona selected to reinforce vocal identity, then generate new material |

---

## Sources

- [Introduction to Studio — Suno Help](https://help.suno.com/en/articles/7940161)
- [Introducing Suno Studio 1.2 — Suno Help](https://help.suno.com/en/articles/10625089)
- [How to Use: Song Editor — Suno Help](https://help.suno.com/en/articles/6141505)
- [Editing in Studio — Suno Help](https://help.suno.com/en/articles/8041473)
- [Can I replace a section of a song? — Suno Help](https://help.suno.com/en/articles/3271873)
- [How to use: Stem Extraction — Suno Help](https://help.suno.com/en/articles/6141441)
- [Remaster — Suno Help](https://help.suno.com/en/articles/8105281)
- [Exporting from Studio — Suno Help](https://help.suno.com/en/articles/8128193)
- [How To Use EQ in Studio — Suno Help](https://help.suno.com/en/articles/8935873)
- [Introducing Studio v1.1 — Suno Help](https://help.suno.com/en/articles/8967489)
- [Add Vocals — Suno Help](https://help.suno.com/en/articles/6882817)
- [Suno Sounds: Generate Custom Audio Samples — Suno Help](https://help.suno.com/en/articles/10625537)
- [Recording in Studio — Suno Help](https://help.suno.com/en/articles/8640385)
- [Loop Recording in Studio — Suno Help](https://help.suno.com/en/articles/8936897)
- [How to Use Stem Cover in Studio — Suno Help](https://help.suno.com/en/articles/9819905)
- [What's New in Suno Studio 1.2 — Suno Blog](https://suno.com/blog/studio1_2)
- [Introducing Suno Studio — Suno Blog](https://suno.com/blog/suno-studio)
- [A Whole New Level of Creative Control — Suno Blog](https://suno.com/blog/songeditor)
- [Suno Studio 1.2 Master Guide — Jack Righteous](https://jackrighteous.com/en-us/blogs/guides-using-suno-ai-music-creation/suno-studio-1-2-master-guide)
- [Suno Studio v5 Complete Guide — Jack Righteous](https://jackrighteous.com/en-us/blogs/guides-using-suno-ai-music-creation/suno-studio-v5-complete-guide)
- [HookGenius: Suno Studio Tutorial](https://hookgenius.app/learn/suno-studio-tutorial/)
- [Fix Timing with Warp + Quantize — Jack Righteous](https://jackrighteous.com/en-us/blogs/guides-using-suno-ai-music-creation/fix-timing-warp-quantize-suno-studio-1-2)
- [Cut Credit Waste in Studio 1.2 — Jack Righteous](https://jackrighteous.com/en-us/blogs/guides-using-suno-ai-music-creation/suno-studio-1-2-reduce-credit-waste)
- [Suno AI Remaster Guide — Jack Righteous](https://jackrighteous.com/en-us/blogs/guides-using-suno-ai-music-creation/suno-ai-remaster-guide-v4)
- [Suno Studio 1.2 — GenxNotes](https://blog.genxnotes.com/en/suno-studio-1-2-update/)
- [MIDI Export from Studio — GenxNotes](https://blog.genxnotes.com/en/suno-studio-audio-to-midi-function/)
- [How to Actually Use Replace Section — AIDIY](https://www.aidiy.tech/post/how-to-actually-use-suno-s-new-replace-section-feature-instructions-plus-bonus-the-arrow-song)
