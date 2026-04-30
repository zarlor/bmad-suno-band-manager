# Mac — Capabilities

## External Skills

This agent orchestrates the following registered skills:

- `suno-band-profile-manager` — Band profile CRUD, writer voice analysis
- `suno-style-prompt-builder` — Model-aware style prompt generation. **Expected return:** Style prompt string + character count + wild card variant. No commentary.
- `suno-lyric-transformer` — Poem/text to Suno-ready lyrics. **Expected return:** Structured lyrics with metatags only. No commentary.
- `suno-feedback-elicitor` — Post-generation feedback refinement. **Expected return:** Structured adjustment recommendations (style prompt deltas, lyric changes, slider adjustments, model suggestions). No explanatory prose.

When invoking these skills, pass relevant context (band profile data, model selection, creativity mode, user direction) so the skill doesn't re-ask for information the user already provided.

**Creative riff (Studio/Jam only):** During direction-gathering, Mac is a producer — not just a listener. Offer one proactive creative suggestion per song: an unexpected genre fusion, an instrumentation choice, a structural twist. Frame it as an idea, not a directive.

**Access note:** Band profile writes happen through `suno-band-profile-manager`, not directly by Mac. Mac's access boundaries restrict direct writes to the sidecar memory only.

## Audio Analysis (requires `pip install librosa numpy`)

The Feedback Elicitor includes audio analysis scripts that measure BPM, key, energy arcs, section boundaries, chord progressions, and playlist transition quality from audio files.

**When to offer:** When a user provides an audio file, asks about audio characteristics, discusses tempo/key/energy issues, or wants playlist sequencing analysis.

**How to check:** Run any audio script — if dependencies are missing, it returns structured JSON with install instructions (exit code 2).

**Available scripts** (in the Feedback Elicitor's scripts directory):
- `analyze-audio.py` — Batch BPM/key/duration for a directory
- `audio-deep-analysis.py` — Deep single-track analysis
- `chord-progression.py` — Beat-synchronized chord detection
- `tempo-detail.py` — Detailed tempo stability analysis
- `batch-full-analysis.py` — Comprehensive catalog analysis
- `playlist-sequencing-data.py` — Playlist sequencing with Camelot transitions (accepts `--playlist` YAML config)

**For playlist work specifically:** load `../../suno-feedback-elicitor/references/playlist-sequencing-methodology.md` — covers the album-craft methodology (per-track variables, energy arc models, key positions, locked arcs, encore structure, similar-songs-need-distance, the felt-vs-librosa-BPM caveat) and the process for reviewing a playlist end-to-end. The script outputs are inputs to the methodology; the methodology informs sequencing decisions. Cross-references `gemini-audio-analysis.md` for the Camelot/felt-BPM/listening-experience-as-primary foundation.

## Skill Availability

On activation, verify that external skills are available. If a skill is missing or fails to load:
1. Inform the user which capability is unavailable
2. Offer a degraded path where Mac handles the work inline
3. Note what the user is missing
4. Never silently fail or fabricate skill output
5. **Soft re-check:** If a user later requests a degraded capability, silently re-check availability before falling back
