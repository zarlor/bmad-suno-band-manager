## Audio Analysis Workflow

**Post-publish pipeline:** When a new track is published, the Band Manager agent (Mac) orchestrates a full analysis pipeline using these scripts — see Mac's SKILL.md under "Post-Publish Analysis Pipeline" for the complete workflow covering analysis, consistent data storage, external comparison, felt BPM checks, and playlist placement. The pipeline ensures consistent data across all catalog files.

### Overview

Three complementary audio analysis approaches, each with different strengths:
- **librosa (Python)** — Programmatic analysis: BPM, key detection, tempo stability, energy arcs, section boundaries. Fast, batch-capable, objective measurements.
- **Gemini 3.1 Pro** — AI audio analysis: upload MP3, get instrument identification, genre classification, dynamic arc description, style prompt accuracy feedback. Best with two-pass workflow for fusion genres.
- **ChatGPT (with audio upload)** — AI audio analysis: upload MP3 for "blind" analysis without providing the style prompt. Useful for unbiased genre/instrument identification. May correctly identify sounds that Gemini hallucinates from seeing the style prompt text.

### Trust Hierarchy and Cross-Verification

When using multiple analysis sources, you'll often get different answers for the same field. Resolve disagreements by source authority for the field type:

**For measurable fields (BPM, key, energy levels, section boundaries, spectral balance):**
- **librosa is primary** — it measures actual audio properties from raw waveforms. Its quirks (halftime detection on slow songs, key major/minor disputes) are predictable and correctable, but it does NOT hallucinate content that isn't there.
- **Gemini and ChatGPT are secondary** — useful as cross-verification but not authoritative on measurable fields.
- **When they disagree on BPM:** default to librosa with the halftime correction for slow contemplative songs (raw 150-160 → felt 75-80). Verify with manual hi-hat counting if it matters.
- **When they disagree on key:** consider both readings, use lyric/emotional context as tiebreaker, or accept that key is uncertain. There is a documented pattern of Gemini consistently picking minor where librosa consistently picks major on the same track — without ground truth verification, neither source is automatically right.

**For instrument identification:**
- **Basic rhythm section + lead vocal (guitar, bass, drums, vocals):** Both Gemini and ChatGPT are reasonably reliable. The AI tools tend to catch what's actually present in the basic stack.
- **Anything beyond the basic stack (brass, strings, synths, atmospheric pads, additional percussion):** Hold the AI's claim loose. Verify against the actual audio before filing as fact.
- **Reverb/delay/atmospheric effects:** AI tools can misidentify these as instruments. Atmospheric production framing in the style prompt (e.g., "cathedral roominess," "intimate studio room ambience," "wide analog stereo with shimmer") increases the hallucination risk — the AI may hear "brass section" or "string pads" that are actually just reverb tails on guitars or vocals. Verify before trusting.

**For subjective fields (mood, vibe, "what works," whether a track "lands"):**
- **Human ear is primary.** AI tools can describe what they hear, but their mood/vibe interpretations are heavily influenced by prompt framing and shouldn't be trusted as the final word.
- **Avoid leading language in your AI prompts** that biases the tool toward specific moods or genre fusions. Let it describe what it actually perceives without suggestive framing.

**Don't burn cycles asking which tool to trust on settled fields.** For BPM/key/section boundaries, default to librosa. For instrument ID beyond the basic rhythm section, verify before filing. For mood, trust the human ear. This calibration is consistent across catalogs and shouldn't be relitigated for every track.

### librosa Analysis Scripts

Requirements: Python 3, librosa, numpy (`pip install librosa numpy`)

**analyze-audio.py** — Batch BPM and key detection for all MP3s in a directory. Uses Krumhansl-Kessler chroma correlation for key estimation. Outputs a summary table with BPM, key, key confidence, and duration.
```bash
python scripts/analyze-audio.py /path/to/mp3s/
```

**audio-deep-analysis.py** — Deep single-track analysis: chord progression over time, energy curve, spectral features, section boundaries, harmonic/percussive separation.
```bash
python scripts/audio-deep-analysis.py track.mp3
```

**tempo-detail.py** — Detailed tempo analysis showing BPM over time in windows. Detects tempo changes, off-beats, and stability.
```bash
python scripts/tempo-detail.py track.mp3
```

**batch-full-analysis.py** — Batch full analysis across a catalog: tempo stability, energy arc, section boundaries, spectral balance. Outputs a comprehensive summary report.
```bash
python scripts/batch-full-analysis.py /path/to/mp3s/
```

#### librosa Notes

- **BPM misreads are genre-dependent and go both directions:**
  - Speed metal → reads **half-time** (e.g., reports 99 BPM when felt tempo is ~198 — reads snare on beat 3 as beat 1)
  - Doom/sludge → reads **double-time** (e.g., reports 144 BPM when felt tempo is ~72 — counts subdivisions as pulse)
  - Power ballads → overcounts (e.g., reports 96 BPM when felt is ~68)
  - Heartbeat/pulse tracks → overcounts (e.g., reports 96 when tagged 60)
- **~19% of tracks have significant BPM misreads** in production testing (31-track catalog). Always verify against genre/feel.
- **"Felt BPM"** — the human-perceived tempo vs. librosa's measurement. When a user says "it feels too fast/slow," compare their perception against felt BPM, not librosa BPM. Felt BPM is what matters for playlist sequencing and feedback triage.
- **LLM BPM estimates also diverge** — Gemini AI Studio, Gemini web, and ChatGPT produce different values for the same track. No single source is reliable for BPM; cross-reference at least two.
- Key confidence below 0.5 is low reliability
- Enharmonic equivalents: D# = Eb, C# = Db, A# = Bb, F# = Gb
- librosa is deterministic — same file always produces the same results. Use as ground truth for BPM/key baseline, but always apply genre-aware correction before acting on the number.
- **Slow contemplative songs (felt tempo 70-80 BPM) trigger halftime detection consistently.** librosa raw values around 150-160 BPM with felt tempo around 75-80 BPM is a well-documented pattern. When librosa reports 152 BPM on a song that "feels" much slower than that, the felt tempo is likely half (76). Cross-verify with hi-hat counting before trusting either value.
- **Manual hi-hat counting is the cheap reliable BPM verification** when AI tools disagree. Count hi-hat hits in a 10-second window of a steady-groove section. Most rock/pop songs play hi-hats as straight eighth notes. Calculation: `(hat hits in 10 sec ÷ 2) × 6 = quarter-note BPM`. Example: 25 hi-hat hits in 10 sec → (25 ÷ 2) × 6 = 75 BPM. When sources contest the BPM, this 30-second manual check is the tiebreaker.

### ChatGPT Audio Analysis

ChatGPT can analyze uploaded MP3 files. Key workflow difference from Gemini:

**Blind analysis (recommended first pass):** Upload the MP3 WITHOUT providing the style prompt or any context about what the song should sound like. Ask ChatGPT to describe what it hears — genre, instruments, mood, vocal style, production. This gives unbiased identification of what Suno actually produced.

**Why blind matters:** When LLMs see the style prompt alongside the audio, they tend to hear what the prompt describes rather than what's actually there. In testing, ChatGPT's blind analysis correctly identified "southern rock / blues rock with fingerstyle bass" while Gemini (which saw the style prompt) hallucinated "funk-metal party groove with slap/pop bass" on the same track.

**Calibrated follow-up:** After the blind pass, share the style prompt and ask ChatGPT to compare intent vs. reality. This two-step approach (blind → calibrated) produces the most honest assessment.

**BPM comparison:** ChatGPT's BPM estimates are rough (120-125 range estimates vs. librosa's precise 123.0). Use librosa for BPM, LLMs for subjective qualities.

#### ChatGPT Reliability Warning

**ChatGPT audio analysis is inconsistent across tracks.** In testing:
- On one track (southern rock/blues), blind analysis was accurate — correctly identified genre, instruments, and bass technique where Gemini hallucinated from the style prompt.
- On another track (brass-metal fusion), blind analysis completely failed — described "alternative rock, indie, hip-hop groove, synth pads" with no brass, no metal, and 94 BPM on a 184 BPM track. Did not hear the audio file correctly.

**Possible causes:** Free-tier ChatGPT may not reliably process all audio uploads. Track complexity, length, or encoding may affect analysis quality. More testing is needed to identify when ChatGPT audio analysis can be trusted.

**Recommendation:** Treat ChatGPT audio analysis as a supplementary data point, not a reliable source. Cross-reference with Gemini and librosa. When ChatGPT's blind analysis agrees with librosa's objective measurements, it's likely accurate. When it diverges significantly (wrong genre family, wrong BPM by >30%), discard it. The blind analysis technique remains valuable in principle — just verify the output makes basic sense before acting on it.

### Gemini 3.1 Audio Analysis

### Setup
- Use Google AI Studio (not gemini.google.com) for primary analysis — direct model access, upload audio, control parameters
- Settings: Gemini 3.1 Pro, Thinking: High, **Temperature: 0.5** (see Temperature Findings below), everything else off (no grounding, search, code execution, or structured output)
- Export from Suno as MP3 — sufficient for analysis, WAV offers no practical benefit
- New context per song — prevents bleed between analyses
- gemini.google.com rate limit is separate from AI Studio — alternate between them when daily limits are hit

### Two-Pass Workflow (Mandatory for Fusion Genres)
- Gemini's first pass flattens fusion genres into nearest pure genre (e.g., NOLA brass-metal → "ska-punk", groove-funk-metal → "sludge")
- First pass prompt must include calibration: (a) distinguish tempo changes from volume/intensity dynamics, (b) describe what's actually present without manufacturing genre fusions or instruments that aren't there, (c) verify BPM by tapping the most consistent rhythmic pulse (kick/snare/hi-hat) and reporting the quarter-note pulse, not subdivisions or "felt" impressions
- Second pass (follow-up in same context) is mandatory. Ask specifically about: mood/feel vs. heaviness, volume/intensity dynamics without tempo change, bass techniques and independent role, stereo panning placement
- Before/after improvement is dramatic — example: first pass = "NWOBHM speed metal, zero funk, bass follows guitar." Follow-up = "funk-metal party groove, standout slap bass, Les Claypool comparison." Same audio.

### Prompt Templates

These prompts were refined across 30+ song analyses and consistently produce the most useful output.

#### First Pass — Structured Blind Analysis

Use this for the initial analysis. The blind approach (no style prompt) prevents Gemini from hearing what the prompt describes rather than what's actually there. For cataloging workflows where you want the accuracy comparison in one pass, include the Style Prompt Accuracy section at the end with the style prompt.

```
You are analyzing a track from the band [BAND NAME] for cataloging purposes. Listen to the full track carefully before responding.

IMPORTANT LISTENING NOTES:
- Distinguish between tempo changes (BPM actually shifts) and dynamic changes (volume/intensity shifts without tempo change). A song can get quieter or sparser without slowing down. Report both separately.
- Describe the genre or genres you actually hear without assuming a fusion is present. If the track is in a single sub-genre, name that single sub-genre. If you hear multiple genre influences blended together, name all the ingredients you actually hear — but do NOT manufacture a fusion that isn't present in the audio.
- Only describe instruments and elements you can clearly identify. Do NOT manufacture content that isn't there. If you're uncertain whether something is an actual instrument or a production effect (reverb tails, delay echoes, atmospheric pads, ambient swells), describe what you hear without assigning it to a specific instrument category. Reverb-heavy production can sound similar to brass or strings in places — don't guess.
- For BPM, tap along to the most consistent rhythmic pulse (usually kick/snare or hi-hat). Report the underlying quarter-note pulse, not subdivision rates (don't count eighth notes or sixteenths as the BPM). Do NOT adjust your BPM estimate to fit a "feels fast" or "feels slow" impression — report what your tap-along count actually gives you, then separately note if the song feels different from that count.

Provide your analysis in this exact format:

## Technical
- **Estimated BPM:** [BPM or range if it shifts, note where shifts occur]
- **Estimated Key:** [key/scale]
- **Time Signature:** [detected, note any changes with approximate timestamps]
- **Duration:** [mm:ss]

## Sonic Profile
- **Intro (first 15 seconds):** [exactly what instruments enter, in what order, what they're doing]
- **Overall Genre Feel:** [describe the blend of genre influences you hear — this band fuses multiple styles, so name all the ingredients, not just the dominant one]
- **Guitar:** [tone, style, notable techniques — clean/distorted, riff-driven/atmospheric, any solos and where]
- **Bass:** [how prominent, tone, role — following guitar or independent, any standout moments]
- **Drums:** [style, energy, notable fills or pattern changes, cymbal work]
- **Vocals:** [delivery style, grit level, harmonization, how many voices, any spoken/whispered sections]
- **Other Instruments:** [brass, keys, strings, anything else present]

## Dynamic Arc
Describe how the energy moves through the song from start to finish. Note builds, drops, peaks, and transitions with approximate timestamps. Separately note any volume/intensity shifts that occur WITHOUT tempo changes.
- [0:00-0:xx] — [what's happening]
- [0:xx-0:xx] — [what's happening]
(continue through the full track)

## Outro
- **How it ends:** [fade, hard stop, instrumental tail, final hit — be specific about the last 10 seconds]

## Notable Moments
List 3-5 specific timestamps where something musically interesting happens:
- [timestamp] — [what happens and why it's notable]

## Style Prompt Accuracy
Compare what you hear to what was requested in the generation prompt below. Note:
- What the prompt asked for that IS clearly present in the audio
- What the prompt asked for that is NOT present or only weakly present
- Anything notable in the audio that was NOT in the prompt

Style prompt used: "[PASTE STYLE PROMPT]"
Exclude styles requested: "[PASTE EXCLUDES]"
```

**Blind vs. style-prompted:** For diagnostic workflows (investigating why a song sounds wrong), remove the Style Prompt Accuracy section and style prompt from the first pass entirely. Share the style prompt in a separate follow-up only. For cataloging workflows where you want the comparison in one pass, keep the section as-is.

#### Second Pass — Calibrated Follow-Up (Same Context)

Send this as a follow-up in the same conversation after the first pass:

```
Good analysis. A few areas I'd like you to listen again more carefully for:

1. **Mood/feel vs. heaviness:** How does this track feel — describe what you actually perceive. Heavy instrumentation doesn't predict mood; a heavy song can feel many ways and so can a light one. Don't pick from a suggested list — describe what's there.
2. **Volume/intensity dynamics:** Are there moments where the band gets noticeably quieter or sparser WITHOUT the tempo changing? Describe those shifts.
3. **Bass specifics:** Listen to the bass independently. Is it using any specific techniques — slap/pop, fingerstyle, pick attack, melodic runs independent of guitar? Does it ever take a lead role?
4. **Stereo placement:** Are any instruments panned notably left or right, especially in the intro?
```

#### Non-Band-Specific Variant

For songs not part of a band project (solo work, one-offs), replace the opening line:

```
You are analyzing an AI-generated music track for cataloging purposes. Listen to the full track carefully before responding.
```

And adjust the genre note:

```
- Describe the genre or genres you actually hear without assuming a fusion is present. If the track is in a single sub-genre, name that single sub-genre. If you hear multiple genre influences blended together, name them — but do not manufacture a fusion that isn't present in the audio.
```

### What Gemini Does Well
- Instrument identification (basic rhythm section + lead vocal) — reliably catches guitar, bass, drums, and vocals when they're actually present. Less reliable for non-basic instruments (brass, strings, synths, ambient pads) — see "What Gemini Misses or Gets Wrong."
- Genre classification at macro level — right family even if specific fusion label is wrong (with the caveat that prompting Gemini to "look for fusion" will cause it to manufacture fusions that aren't there)
- Style Prompt Accuracy feedback — the most valuable output. Honest about what Suno delivered vs. what was requested
- Structural timeline with timestamps — dynamic arc breakdowns useful for songbook documentation
- Stereo placement (when asked) — catches hard-panned guitars, center-anchored bass/drums

### What Gemini Misses or Gets Wrong
- Cannot hear fusion when present — rounds to nearest pure genre even after calibration. Needs directed follow-up to surface real fusions
- Misses mood/irony — reads heaviness as aggression by default. Cannot detect playful or ironic energy in heavy music without explicit prompting
- BPM unreliable — may read subdivisions as pulse, or be biased by "feels fast/slow" leading language in prompts. Treat estimates as approximate; verify with manual hi-hat counting when it matters
- Misses volume dynamics on first pass — describes tracks as "consistently dense" when they have significant intensity shifts
- Cannot parse detailed endings — fine detail on last 10 seconds is unreliable
- Misses bass techniques on first pass — slap/pop, melodic runs, lead bass consistently missed until follow-up
- **Hallucinates atmospheric/effect content as instruments** — reverb tails, delay echoes, and ambient pads on guitars/vocals can be misidentified as brass section, string pads, or other instruments that aren't actually present. Atmospheric production framing in the style prompt ("cathedral roominess," "intimate studio room ambience," "wide analog stereo," "shimmer") increases hallucination risk. When Gemini reports a non-basic instrument, verify against the actual audio before filing as fact. **Documented case:** Gemini reported a "very prominent brass section" on a track with no brass at all — what it heard was reverb tails on the vocals and guitars from an atmospheric production stack.
- **Inconsistent key detection vs. librosa** — there is a documented pattern of Gemini consistently leaning toward minor-key readings while librosa consistently leans toward major-key readings on the same track. Without ground truth verification (perfect-pitch listener, manual chord identification), neither source is automatically correct. Use lyric content / emotional context as a tiebreaker, or accept that key is uncertain and document both readings.
- **Sensitive to leading language in prompts** — phrases like "this band plays genre fusion" or "a heavy song can feel upbeat, playful, or ironic" prime Gemini to invent content matching those framings. Use neutral, descriptive prompt language that asks Gemini to describe what it perceives without suggesting what categories to find. The prompt templates in this doc have been progressively de-led to minimize these effects.

### Temperature Findings — 0.5 Outperforms 0.3

A/B testing on the same track (brass-metal fusion) with blind prompts at different temperatures:

**Gemini at 0.5 temp (blind, no style prompt):**
- Genre: "Progressive metal, ska-core, hard rock, swing/jazz, dark cabaret" — best genre description from any LLM
- Brass: Correctly detected on blind prompt (trumpet, trombone, saxophone)
- Dynamics: Verse dropouts well captured — guitars drop out, sparse mix, builds for choruses
- Bass (first pass): "Punchy, metallic, pick-driven, walking lines" — reasonable
- BPM: ~145 (closer to librosa's 184.6 half-time than 0.3 temp's 165)

**Gemini at 0.3 temp (with style prompt + follow-up calibration):**
- Genre: "Manic carnival-punk, ska-core, funk-metal" — decent but needed follow-up to get there
- Brass: Detected but classified as ska-punk rather than NOLA brass-metal
- Bass: Hallucinated "slap/pop funk-metal techniques" — likely influenced by seeing "NOLA funk groove" in the style prompt
- BPM: ~165 (same as a completely different track — unreliable)

**Key takeaway:** 0.5 temp with a blind prompt produced better genre description, more accurate instrument detection, and fewer hallucinations than 0.3 temp with the style prompt provided. The extra temperature gives Gemini room to describe what it actually hears rather than fitting output into narrow categories.

**Persistent gaps at both temperatures:**
- Ending detail remains unreliable — neither caught the a capella moment, vocal yell, triple snare strike, or final brass blast
- Intro accuracy: 0.5 temp said full band at 0:00 when actually brass-only for first 10 seconds
- Follow-up prompts can trigger hallucinations — asking specifically about bass at 0.5 temp produced "slap and pop, lead melodic role" when bass was actually hidden behind guitar/tubas

**Updated recommendation:** Use **0.5 temperature** in AI Studio as the default. Use **blind prompts** (no style prompt) for the first pass. Only share the style prompt in a calibrated follow-up. Be cautious with follow-up questions about specific instruments — they can trigger hallucinations where the first pass was accurate.

### Integration with Feedback Elicitor
- Style Prompt Accuracy as feedback loop: compare what was prompted vs. what Gemini hears → identify what Suno ignores, misinterprets, or adds unbidden → adjust future prompts
- A/B prompt testing: change one variable, generate both, analyze both, compare. Quantifies what prompt changes actually do.
- Batch analysis for playlist ordering: BPM, key, and dynamic arc data across catalog enables data-informed playlist decisions

### Gemini as Suno Prompt Engineering Feedback Loop

The highest-value use of Gemini audio analysis is **real-time A/B testing of Suno prompts during song creation**, not retrospective catalog analysis. Retrospective analysis of already-published songs is limited — you have one audio snapshot per song and no controlled comparison. The real power is testing prompt changes as you make them.

**Recommended workflow for prompt improvement:**
1. Write style prompt + lyrics package
2. Generate 2-3 versions on Suno
3. Run each through Gemini blind at 0.5 temp (NO style prompt in the analysis request)
4. Compare what Gemini hears across versions to what was prompted
5. Identify what the prompt actually controlled vs. what Suno ignored
6. Adjust ONE variable (word position, tag, slider value), regenerate, analyze again
7. Document what moved and what didn't in the songbook generation log

**A/B testing discipline:** Change ONE variable per test. Move "art rock" from position 1 to position 3? Generate both, analyze both, compare. Add "driving technical bass"? Generate with and without, analyze both. This is the only way to systematically learn what Suno actually responds to vs. what it ignores.

**Why Gemini's strengths align with this workflow:** It reliably detects instrument presence, dynamic arc, mood/energy, and stereo placement — exactly the things prompt changes are trying to influence. Its weaknesses (BPM, bass technique, endings) don't matter for A/B comparisons because they'd be equally wrong on both versions.

### Preferred Workflow
Opus 4.6 (Claude) as primary prompter/orchestrator, Gemini 3.1 as audio analysis assistant. Claude builds Suno packages, Gemini analyzes resulting audio, Claude interprets analysis to inform next iteration. Mac can suggest A/B testing as an optional step after presenting a Suno package: "Want to test this prompt? Generate 2-3 versions, run them through Gemini, and I'll tell you what landed and what didn't."

---

## Playlist Sequencing

### Methodology

Playlist ordering requires balancing two dimensions simultaneously:
- **Sonic flow** — BPM transitions, key compatibility (Camelot wheel), energy arcs, timbral variety
- **Lyrical/narrative progression** — thematic arc across songs, emotional journey, story sequencing

Neither dimension alone is sufficient. Adjacent tracks need to work musically AND thematically.

### Sequencing Principles

**Album sequencing fundamentals:**
- Opener must grab attention — front-loading engaging material is critical in the streaming era
- Variety within cohesion — avoid two songs with similar arrangement density, instrumentation, or timbral character back-to-back
- Similar thematic songs need distance — tracks covering the same ground blur when adjacent
- Sonic palette contrast is essential for maintaining interest
- Silence between tracks is itself a sequencing decision — spacing signals mood group shifts

**DJ Harmonic Mixing (Camelot Wheel):**
- Same key (8A→8A): Perfect but monotonous if overused
- +/-1 number, same letter (8A→7A or 9A): Most common professional move, changes one scale note
- Relative major/minor (8A→8B): Mood shift without changing harmonic center. Minor→major lifts; major→minor darkens
- +2 numbers: Energy boost, more noticeable — use sparingly
- Beyond +2: Risk audible clashing — use only for intentional dramatic contrast

**BPM takes priority over key:** A harmonically perfect transition with a 20 BPM jump sounds worse than a minor key clash at the same tempo. Double/half time relationships (70 BPM ↔ 140 BPM) share the same pulse grid and can work together.

**Concert setlist design (W-Shape model):**
- Featured songs at three peaks (beginning, middle, end) with complementary songs providing changes in key, tempo, timbre, and mood between them
- Multiple peaks and valleys rather than a single arc
- Peak-end rule: audiences remember the best moment and the final moment most vividly
- Encore: a planned 3-5 song mini-set at high energy following a breath-catching break

### Playlist Sequencing Scripts

**playlist-sequencing-data.py** — Generates a full sequencing report: BPM, overall/entry/exit keys, Camelot codes, energy levels, intro/outro energy percentages, and transition quality ratings between adjacent tracks.
```bash
python scripts/playlist-sequencing-data.py /path/to/mp3s/
```

**chord-progression.py** — Analyzes chord changes and key centers in 30-second windows within a single track. Measure-by-measure detection is too noisy with distorted guitars, but 30-second key center summaries are useful.
```bash
python scripts/chord-progression.py track.mp3
```

**Camelot wheel mapping** is embedded in the sequencing script — all 24 keys (12 major, 12 minor) mapped to codes 1A-12A (minor) and 1B-12B (major).
