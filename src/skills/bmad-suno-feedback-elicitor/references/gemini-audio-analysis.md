## Gemini 3.1 Audio Analysis Workflow

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
