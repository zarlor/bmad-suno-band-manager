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
model_preference: "v4.5-all"  # v4.5-all | v4 Pro (legacy) | v4.5 Pro | v4.5+ Pro | v5 Pro
tier: "free"                   # free | pro | premier

# Style Prompt — front-load essentials in first 200 chars (critical zone)
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
  persona_reference: ""    # Suno Persona name, if exists
  persona_source_song: ""  # Song the Persona was derived from (for recreation)

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

# Writer Voice (optional — populated by Analyze Writer Voice)
writer_voice:
  vocabulary: ""           # formal/casual, abstract/concrete, domain words
  rhythm: ""               # sentence length patterns, fragment use
  imagery: ""              # dominant image worlds (nature, urban, body, etc.)
  emotional_tone: ""       # raw/restrained, hopeful/melancholic, etc.
  metaphor_style: ""       # extended/quick, conventional/surprising, frequency
  repetition_patterns: ""  # anaphora, refrains, echo structures
  sample_quotes: []        # representative lines from analyzed samples

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
| `model_preference` | Yes | string | One of: v4.5-all, v4 Pro (legacy), v4.5 Pro, v4.5+ Pro, v5 Pro |
| `tier` | Yes | string | One of: free, pro, premier |
| `style_baseline` | Yes | string | Max 1000 chars (v4.5+/v5). Max 200 chars for v4 Pro. Front-load essentials in first 200 chars |
| `exclusion_defaults` | No | list of strings | Keep each entry concise and specific. Max 5 entries recommended |
| `vocal.gender` | Yes* | string | One of: male, female, nonbinary, any. *Optional if `instrumental: true` |
| `vocal.tone` | Yes* | string | Non-empty. *Optional if `instrumental: true` |
| `vocal.delivery` | Yes* | string | Non-empty. *Optional if `instrumental: true` |
| `vocal.energy` | Yes* | string | Non-empty. *Optional if `instrumental: true` |
| `vocal.diction` | No | string | Optional refinement |
| `vocal.persona_reference` | No | string | Suno Persona name if exists (Pro/Premier only) |
| `vocal.persona_source_song` | No | string | Song the Persona was derived from (for recreation if lost) |
| `creativity_default` | No | string | One of: conservative, balanced, experimental. Defaults to balanced |
| `sliders.weirdness` | No | integer | 0-100, only valid for pro/premier tiers |
| `sliders.style_influence` | No | integer | 0-100, only valid for pro/premier tiers |
| `sliders.audio_influence` | No | integer | 0-100, only appears when using audio upload (pro/premier) |
| `studio_preferences.bpm` | No | number | Default tempo. Only valid for premier tier |
| `studio_preferences.key` | No | string | Default key/scale. Only valid for premier tier |
| `studio_preferences.time_signature` | No | string | Default time signature. Only valid for premier tier |
| `writer_voice.*` | No | string/list | All writer_voice fields are optional |
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

## Notes for Downstream Skills

- **Style Prompt Builder** reads: `style_baseline`, `reference_tracks`, `vocal`, `exclusion_defaults`, `sliders`, `creativity_default`, `model_preference`, `language`, `instrumental`
- **Lyric Transformer** reads: `writer_voice`, `language`
- **Feedback Elicitor** reads: `style_baseline`, `sliders`, `model_preference`; writes to `generation_history` via headless:edit
- When a Persona is active, its style auto-populates the Style of Music field — keep additional style modifications simple (1-2 genres, 1 mood, 2-4 instruments max)
