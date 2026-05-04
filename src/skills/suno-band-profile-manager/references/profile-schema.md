# Band Profile Schema

## YAML Structure

```yaml
# Band Profile — {band_name}
# Created: {date}
# Last modified: {date}

name: "Band Name Here"
version: 1  # Increment on major sound evolution
instrumental: false  # true for instrumental-only projects (skips vocal requirements)

# Sound Identity
genre: "indie folk-rock with electronic textures"
mood: "melancholic but hopeful, atmospheric"
language: "English"  # Language for lyrics and style cues
reference_tracks:
  - "Bon Iver meets Radiohead"
  - "Fleet Foxes with Massive Attack production"

# Model & Tier
model_preference: "v4.5-all"  # v4.5-all | v4 Pro (legacy) | v4.5 Pro | v4.5+ Pro | v5 Pro | v5.5
tier: "free"                   # free | pro | premier

# Style Prompt — 1,000 char limit (v4.5+/v5/v5.5; 200 for v4 Pro). Front-load essentials in first ~200 chars (critical zone).
style_baseline: >
  Indie folk-rock with electronic textures, atmospheric and layered.
  Warm analog synths underneath acoustic guitar, subtle ambient pads.
  Modern production, wide stereo field, intimate mix.
exclusion_defaults:
  - "no autotune"
  - "no screaming"
  - "no heavy metal guitar"

# Vocal Direction (required unless instrumental: true)
vocal:
  gender: "male"           # male | female | nonbinary | any
  tone: "warm, breathy"
  delivery: "intimate, conversational"
  energy: "restrained, building"
  diction: "clear, slightly slurred on emotional peaks"
  persona_reference: ""    # Suno Persona name, if exists (v4.5/v5 only; replaced by voice_id in v5.5)
  persona_source_song: ""  # Song the Persona was derived from (for recreation)
  # NOTE: Personas pull the sound toward the era/style of the source song.
  # Audio Influence at 10-15% reduces this era-anchoring but doesn't fully
  # overcome it. For era-specific pieces, consider generating without a persona,
  # or creating era-specific personas from era-appropriate source songs.
  voice_id: ""             # Suno Voice identifier (v5.5, Pro/Premier only). Replaces persona_reference for v5.5.
  # NOTE: When voice_id is set, omit gender vocal descriptors from style_baseline —
  # the Voice defines the vocal identity (gender, tone, character from the audio sample).

# Creative Settings
creativity_default: "balanced"  # conservative | balanced | experimental

# Sliders (pay-gated — only set if tier supports them)
sliders:
  weirdness: 50            # 0-100, default 50
  style_influence: 50      # 0-100, default 50
  audio_influence: null     # 0-100, only when using audio upload

# Studio Preferences (Premier tier only)
studio_preferences:
  bpm: null                # Default tempo (number)
  key: ""                  # Default key/scale (e.g., "C minor", "A major")
  time_signature: ""       # Default time signature (e.g., "4/4", "3/4")

# Custom Model (v5.5, Pro/Premier only)
custom_model_id: ""        # Suno Custom Model identifier, if user has one
custom_model_notes: ""     # What the custom model was trained on and what production style it provides

# Writer Voice (optional — populated by Analyze Writer Voice)
writer_voice:
  vocabulary: ""           # formal/casual, abstract/concrete, domain words
  rhythm: ""               # sentence length patterns, fragment use
  imagery: ""              # dominant image worlds (nature, urban, body, etc.)
  emotional_tone: ""       # raw/restrained, hopeful/melancholic, etc.
  metaphor_style: ""       # extended/quick, conventional/surprising, frequency
  repetition_patterns: ""  # anaphora, refrains, echo structures
  sample_quotes: []        # representative lines from analyzed samples

# Known Working Prompt Patterns (optional — prompt formulations that reliably produce good results)
known_working_patterns: []
  # Per-profile list of prompt patterns proven to work well for this band's sound.
  # Record specific formulations that nail the identity, especially when blending genres.
  # Examples:
  #   - "'atmospheric swamp metal accents' — best formulation for keeping band identity when another genre leads"
  #   - "'progressive heavy groove with post-rock dynamics' — captures heaviness without triggering screaming"

# Known Limitations (optional — things Suno can't reliably do for this sound)
known_limitations: []
  # Per-profile list of known limitations or failure modes for this band's genre/style.
  # Saves time by documenting dead ends and workaround-required areas.
  # Examples:
  #   - "Bass-forward rock/metal is not reliably achievable — Suno defaults to guitar-forward mixes"
  #   - "'funk metal' triggers slap/pop bass, not overdriven fingerstyle — avoid this term"
  #   - "Even with 'guitar' in Exclude Styles, Suno still produces guitar in rock/metal context"

# Generation Learnings (optional — what prompt language triggers what behavior)
generation_learnings:
  # Optional — captures what style prompt language triggers what behavior
  # for this specific band's sound. Accumulated from testing and feedback.
  # Examples:
  #   - "'metal' in style prompt triggers screaming — use 'progressive heavy groove' instead"
  #   - "'sludge' triggers harsh vocals — use 'thick, heavy' instead"
  #   - "Weirdness above 60 produces inconsistent results for this genre"

# Generation History (optional — successful generation snapshots)
generation_history: []
# Each entry:
#   - date: "2026-03-19"
#     style_prompt: "the style prompt that worked"
#     model: "v5 Pro"
#     sliders: { weirdness: 65, style_influence: 55 }
#     note: "nailed the vocal tone on this one"
```

## Field Definitions

| Field | Required | Type | Constraints |
|-------|----------|------|-------------|
| `name` | Yes | string | Non-empty, used as display name |
| `version` | No | integer | Defaults to 1, increment on major changes |
| `instrumental` | No | boolean | Defaults to false. When true, vocal fields become optional |
| `genre` | Yes | string | Non-empty |
| `mood` | Yes | string | Non-empty |
| `language` | No | string | Defaults to "English". Passed to Lyric Transformer and Style Prompt Builder |
| `reference_tracks` | No | list of strings | Free-form "sounds like" descriptions |
| `model_preference` | Yes | string | One of: v4.5-all, v4 Pro (legacy), v4.5 Pro, v4.5+ Pro, v5 Pro, v5.5 |
| `tier` | Yes | string | One of: free, pro, premier |
| `style_baseline` | Yes | string | Max 1000 chars (v4.5+/v5/v5.5). Max 200 chars for v4 Pro. Front-load essentials in first ~200 chars (critical zone — strongest influence). Content beyond 200 is supplementary, not wasted. |
| `exclusion_defaults` | No | list of strings | Keep each entry concise and specific. Max 5 entries recommended |
| `vocal.gender` | Yes* | string | One of: male, female, nonbinary, any. *Optional if `instrumental: true` |
| `vocal.tone` | Yes* | string | Non-empty. *Optional if `instrumental: true` |
| `vocal.delivery` | Yes* | string | Non-empty. *Optional if `instrumental: true` |
| `vocal.energy` | Yes* | string | Non-empty. *Optional if `instrumental: true` |
| `vocal.diction` | No | string | Optional refinement |
| `vocal.persona_reference` | No | string | Suno Persona name if exists (Pro/Premier only). v4.5/v5 models only; replaced by `voice_id` for v5.5 |
| `vocal.persona_source_song` | No | string | Song the Persona was derived from (for recreation if lost) |
| `vocal.voice_id` | No | string | Suno Voice identifier (Pro/Premier only, v5.5). Replaces `persona_reference` for v5.5. When set, omit gender vocal descriptors from `style_baseline` |
| `creativity_default` | No | string | One of: conservative, balanced, experimental. Defaults to balanced |
| `sliders.weirdness` | No | integer | 0-100, only valid for pro/premier tiers |
| `sliders.style_influence` | No | integer | 0-100, only valid for pro/premier tiers |
| `sliders.audio_influence` | No | integer | 0-100, only appears when using audio upload (pro/premier) |
| `studio_preferences.bpm` | No | number | Default tempo. Only valid for premier tier |
| `studio_preferences.key` | No | string | Default key/scale. Only valid for premier tier |
| `studio_preferences.time_signature` | No | string | Default time signature. Only valid for premier tier |
| `custom_model_id` | No | string | Suno Custom Model identifier (Pro/Premier only, v5.5). Up to 3 models per account, trained on 6+ original tracks |
| `custom_model_notes` | No | string | Description of what the custom model was trained on and what production style it provides |
| `writer_voice.*` | No | string/list | All writer_voice fields are optional |
| `known_working_patterns` | No | list of strings | Prompt formulations proven to reliably produce good results for this band's sound. Record specific wording that nails the identity. |
| `known_limitations` | No | list of strings | Known failure modes or dead ends for this band's genre/style in Suno. Saves time by documenting things that don't work. |
| `generation_learnings` | No | list of strings | Accumulated observations about what prompt language triggers what Suno behavior for this band's genre/style. Updated from testing and feedback sessions. |
| `generation_history` | No | list of objects | Max 10 entries. Each entry: date, style_prompt, model, sliders, note |

## Validation Rules

1. `name` must be non-empty
2. `genre` must be non-empty
3. `mood` must be non-empty
4. `model_preference` must be one of the allowed values
5. `tier` must be one of: free, pro, premier
6. `style_baseline` must not exceed 1000 characters (200 for v4 Pro)
7. If `instrumental` is not true: `vocal.gender` must be one of: male, female, nonbinary, any
8. If `instrumental` is not true: `vocal.tone`, `vocal.delivery`, `vocal.energy` must be non-empty
9. If `instrumental` is true: vocal section is optional; if present, fields are not required
10. If `tier` is "free", `sliders` should not be present or should warn that values won't be usable
11. If `tier` is "free" and `model_preference` is not "v4.5-all", warn about mismatch
12. If `tier` is not "premier" and `studio_preferences` has values, warn they won't be usable
13. If `creativity_default` is present, must be one of: conservative, balanced, experimental
14. If `language` is present, must be a non-empty string
15. `generation_history` must not exceed 10 entries
16. Profile filename must be kebab-case matching the band name (spaces to hyphens, lowercase)
17. If `vocal.voice_id` is set, warn if `vocal.gender` is also set — the Voice defines vocal identity, gender descriptors should be omitted from `style_baseline`
18. If `vocal.voice_id` is set but `model_preference` is not "v5.5", warn that Voices require v5.5
19. If `custom_model_id` is set but `tier` is "free", warn that Custom Models require Pro or Premier tier

## Notes for Downstream Skills

- **Style Prompt Builder** reads: `style_baseline`, `reference_tracks`, `vocal`, `exclusion_defaults`, `sliders`, `creativity_default`, `model_preference`, `language`, `instrumental`
- **Lyric Transformer** reads: `writer_voice`, `language`
- **Feedback Elicitor** reads: `style_baseline`, `sliders`, `model_preference`; writes to `generation_history` via headless:edit
- When a Persona is active (v4.5/v5), its style auto-populates the Style of Music field — keep additional style modifications simple (1-2 genres, 1 mood, 2-4 instruments max)
- **Persona Era-Anchoring (v4.5/v5):** Personas pull the sound toward the era/style of the source song. Audio Influence at 10-15% reduces this but doesn't eliminate it. For era-specific pieces, generate without a persona or create era-specific personas from era-appropriate source songs.
- **Voices (v5.5):** Voices replace Personas for v5.5. When `voice_id` is set, the Voice defines the vocal identity — omit gender vocal descriptors from `style_baseline`. The style prompt should focus on instrumentation, production, and mood rather than vocal character.
- **v5.5 Voice-Character Principle:** Voices capture vocal *character* — timbre, lilt, vibrato tendencies, attack patterns, dynamics behavior, mic artifacts. They don't carry trained genre gravity; Suno adapts the captured character to whatever genre the prompt directs. Six practical rules for Voice-aware profiles (see `suno-style-prompt-builder/references/model-prompt-strategies.md` for full details and validated case study):
  1. **Drop descriptors that duplicate what the Voice already delivers** — if the Voice captures vulnerable-breathy delivery, drop "warm," "vulnerable," "clean," "storytelling vocal" from `style_baseline`. They're redundant and can conflict with the captured character.
  2. **Load descriptors that specify what the song needs from the arrangement.** The style prompt drives arrangement (instrumentation, genre, production, dynamics); the Voice provides vocal character. Be explicit about arrangement — "overdriven rhythm guitar with crunch," "driving mid-tempo rock groove" — rather than relabeling what the Voice does.
  3. **Keep Style Influence tight (65+)** so the prompt leads the arrangement firmly. Profiles using a Voice for cross-genre work should bump `sliders.style_influence` to 65 as the default.
  4. **Leave `vocal.gender` empty** when `voice_id` is set — the schema already warns about this (rule 17).
  5. **Voice-aware `exclusion_defaults`** — when the Voice physically cannot produce harsh/screamed vocals, harsh-vocal exclusions are wasted Exclude Styles space. Focus exclusions on production/genre-direction protection (`heavy metal`, `heavy distortion`, `steel guitar`, `autotune`, `pop sheen`). The clean Voice IS the guardrail against harsh vocals.
  6. **Audio Influence floor caution** — 55-60% is the recommended default for Voice profiles. The 30-40% "subtle flavor" range works with Professional-level Voices; for non-Professional Voices, dropping below ~40% can trigger a robotic-timbre failure mode.
- **Multi-profile Voice strategy** — profiles can reference multiple Voice IDs when the project uses several Voice recordings (e.g., "Narrative Rock" for mid-tempo rock tracks, "Ballad Intimate" for tender songs, "Speak-Sing Confessional" for literary/narrative tracks). Each Voice should be internally consistent (single stable character, 20-30 sec per recording, Skill Level Professional mandatory). Variety lives across Voices, not within one Voice sample. Document the mapping and per-Voice use cases in the profile.
- **Custom Models (v5.5):** When `custom_model_id` is set, the Style Prompt Builder should complement the model's learned production style rather than fight it. Include `custom_model_notes` context when building prompts.
- **Inspo Playlist Guidance:** Using your own songs as Inspo homogenizes the catalog sound. Drop Inspo when a song needs its own identity within the same band — let the style prompt and persona/voice do the work instead.

---

## Per-Band Playlist YAML (the canonical playlist source)

Each band in the project owns exactly **one** canonical playlist file:

```
docs/{band-slug}-playlist.yaml
```

The slug matches the band profile filename — `docs/band-profiles/solitary-fire.yaml` pairs with `docs/solitary-fire-playlist.yaml`. This file is the single source of truth for the band's track sequence; **do not duplicate the track list elsewhere.** Other files (sidecar narrative, voice context, ordering doc) reference or derive from this YAML.

### Schema

```yaml
album: "<Band display name>"
tracks:
  - name: "<Song title (must match the songbook entry's frontmatter title)>"
    file: "<exact filename in docs/audio/, e.g. My Song.mp3>"
  - name: "<next song>"
    file: "<next file>"
  # ...
```

The two required fields per track are `name` (the human-readable song title — must match the songbook entry's frontmatter `title`) and `file` (the audio filename in `docs/audio/`, used as the input to `playlist-sequencing-data.py`).

### Bootstrapping

If a band already has songbook entries but no playlist YAML, scaffold one:

```bash
python3 src/skills/suno-band-profile-manager/scripts/scaffold-playlist.py {band-slug} --from-songbook
```

This writes `docs/{band-slug}-playlist.yaml` with discovered song titles populated and `file:` fields left as empty strings (TODO: fill in from `docs/audio/`). The user reviews, fills in audio filenames, sets the order, and saves.

For a brand new band with no songbook entries yet, run without `--from-songbook` to write an empty template.

### Auto-creation on band profile creation

When a new band profile is created via `suno-band-profile-manager`, the playlist YAML scaffold MUST be created in the same write batch. New bands without a playlist YAML are caught by `validate-profile.py` once they have any songbook entries.

### The `playlist:` block in band profile YAML is invalid

The band profile YAML must NOT contain a `playlist:` block. `validate-profile.py` warns on profiles that carry one. Authoritative track-list data lives in `docs/{band-slug}-playlist.yaml`; sequencing-history narrative notes belong in a band-specific ordering doc (`docs/{band-slug}-playlist-ordering.md`) if maintained.

### Workflow rules (apply in same write batch)

- **On song publish:** the band's `docs/{band-slug}-playlist.yaml` MUST be updated alongside the songbook entry.
- **On track reorder:** edit `docs/{band-slug}-playlist.yaml` first; the script's per-album companion `docs/{band-slug}-playlist-sequencing.md` auto-refreshes from this on the next run.
- **On track removal/rename:** update the YAML, the songbook (if renaming), the sidecar narrative, and any ordering doc all in the same write batch.

See also `suno-feedback-elicitor/references/playlist-sequencing-methodology.md` for the album-craft methodology that consumes this file's data.
