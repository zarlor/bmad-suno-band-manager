## Audio Analysis Workflow

### Overview

Three complementary audio analysis approaches, each with different strengths:
- **librosa (Python)** — Programmatic analysis: BPM, key detection, tempo stability, energy arcs, section boundaries. Fast, batch-capable, objective measurements.
- **Gemini 3.1 Pro** — AI audio analysis: upload MP3, get instrument identification, genre classification, dynamic arc description, style prompt accuracy feedback. Best with two-pass workflow for fusion genres.
- **ChatGPT (with audio upload)** — AI audio analysis: upload MP3 for "blind" analysis without providing the style prompt. Useful for unbiased genre/instrument identification. May correctly identify sounds that Gemini hallucinates from seeing the style prompt text.

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
- First pass prompt must include calibration: (a) distinguish tempo changes from volume/intensity dynamics, (b) describe genre blend not nearest pure genre, (c) verify BPM by tapping kick/snare pulse not subdivisions
- Second pass (follow-up in same context) is mandatory. Ask specifically about: mood/feel vs. heaviness, volume/intensity dynamics without tempo change, bass techniques and independent role, stereo panning placement
- Before/after improvement is dramatic — example: first pass = "NWOBHM speed metal, zero funk, bass follows guitar." Follow-up = "funk-metal party groove, standout slap bass, Les Claypool comparison." Same audio.

### What Gemini Does Well
- Instrument identification — reliably catches what's present
- Genre classification at macro level — right family even if specific fusion label is wrong
- Style Prompt Accuracy feedback — the most valuable output. Honest about what Suno delivered vs. what was requested
- Structural timeline with timestamps — dynamic arc breakdowns useful for songbook documentation
- Stereo placement (when asked) — catches hard-panned guitars, center-anchored bass/drums

### What Gemini Misses or Gets Wrong
- Cannot hear fusion — rounds to nearest pure genre even after calibration. Needs directed follow-up
- Misses mood/irony — reads heaviness as aggression by default. Cannot detect playful or ironic energy in heavy music
- BPM unreliable — may read subdivisions as pulse. Treat estimates as approximate
- Misses volume dynamics on first pass — describes tracks as "consistently dense" when they have significant intensity shifts
- Cannot parse detailed endings — fine detail on last 10 seconds is unreliable
- Misses bass techniques on first pass — slap/pop, melodic runs, lead bass consistently missed until follow-up

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
