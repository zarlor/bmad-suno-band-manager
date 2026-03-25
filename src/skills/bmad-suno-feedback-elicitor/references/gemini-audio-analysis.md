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

### Preferred Workflow
Opus 4.6 (Claude) as primary prompter/orchestrator, Gemini 3.1 as audio analysis assistant. Claude builds Suno packages, Gemini analyzes resulting audio, Claude interprets analysis to inform next iteration.
