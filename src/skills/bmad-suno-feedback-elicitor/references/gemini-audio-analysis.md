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

- BPM may read double-time on faster tracks (e.g., 184 BPM may actually be ~92 half-time)
- Key confidence below 0.5 is low reliability
- Enharmonic equivalents: D# = Eb, C# = Db, A# = Bb, F# = Gb
- librosa is deterministic — same file always produces the same results. Use as ground truth for BPM/key, cross-reference with LLM analysis for subjective qualities.

### ChatGPT Audio Analysis

ChatGPT can analyze uploaded MP3 files. Key workflow difference from Gemini:

**Blind analysis (recommended first pass):** Upload the MP3 WITHOUT providing the style prompt or any context about what the song should sound like. Ask ChatGPT to describe what it hears — genre, instruments, mood, vocal style, production. This gives unbiased identification of what Suno actually produced.

**Why blind matters:** When LLMs see the style prompt alongside the audio, they tend to hear what the prompt describes rather than what's actually there. In testing, ChatGPT's blind analysis correctly identified "southern rock / blues rock with fingerstyle bass" while Gemini (which saw the style prompt) hallucinated "funk-metal party groove with slap/pop bass" on the same track.

**Calibrated follow-up:** After the blind pass, share the style prompt and ask ChatGPT to compare intent vs. reality. This two-step approach (blind → calibrated) produces the most honest assessment.

**BPM comparison:** ChatGPT's BPM estimates are rough (120-125 range estimates vs. librosa's precise 123.0). Use librosa for BPM, LLMs for subjective qualities.

### Gemini 3.1 Audio Analysis

### Setup
- Use Google AI Studio (not gemini.google.com) for primary analysis — direct model access, upload audio, control parameters
- Settings: Gemini 3.1 Pro, Thinking: High, Temperature: 0.3, everything else off (no grounding, search, code execution, or structured output)
- Export from Suno as MP3 — sufficient for analysis, WAV offers no practical benefit
- New context per song — prevents bleed between analyses
- Note: gemini.google.com may outperform AI Studio for fusion/atmospheric genres — its default (likely higher) temperature gives more room to describe nuance. Consider testing 0.5-0.7 in AI Studio as well
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

### Integration with Feedback Elicitor
- Style Prompt Accuracy as feedback loop: compare what was prompted vs. what Gemini hears → identify what Suno ignores, misinterprets, or adds unbidden → adjust future prompts
- A/B prompt testing: change one variable, generate both, analyze both, compare. Quantifies what prompt changes actually do.
- Batch analysis for playlist ordering: BPM, key, and dynamic arc data across catalog enables data-informed playlist decisions

### Preferred Workflow
Opus 4.6 (Claude) as primary prompter/orchestrator, Gemini 3.1 as audio analysis assistant. Claude builds Suno packages, Gemini analyzes resulting audio, Claude interprets analysis to inform next iteration.
