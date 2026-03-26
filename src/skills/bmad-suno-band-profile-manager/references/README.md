# Band Profile Manager

The Band Profile Manager handles CRUD operations for band identity profiles — the sonic equivalent of a brand book for your musical projects. It captures genre, vocal character, production style, creative boundaries, language, and songwriter voice into persistent YAML profiles stored at `docs/band-profiles/`. These profiles serve as the foundation that the Style Prompt Builder, Lyric Transformer, and Feedback Elicitor draw from to maintain consistency across songs.

## When to Use Directly vs. Through Mac

Use this skill directly when you need to manage profiles independently — creating, editing, duplicating, or analyzing writer voice outside of a song-creation workflow. Use Mac (the orchestrating agent) when profile work is part of a larger session that includes building style prompts, transforming lyrics, or refining Suno output.

## Operations

### Interactive Mode (default)

| Operation | Description |
|-----------|-------------|
| **Create** | Guided conversational discovery to build a complete band profile |
| **List** | Show all saved profiles with name, genre, model, language, and vocal/instrumental status |
| **Load** | Display a profile in readable format with tier drift detection |
| **Edit** | Apply natural language changes to an existing profile |
| **Delete** | Remove a profile with explicit confirmation |
| **Duplicate** | Clone a profile as a starting point for versioning or forks |
| **Analyze Voice** | Extract writer voice patterns from 3-5 writing samples |
| **Health Check** | Assess profile completeness and quality with friendly recommendations |

### Headless Mode (`--headless` or `-H`)

- `--headless:create` — Create from provided YAML, validate, save
- `--headless:validate` — Validate an existing profile against schema
- `--headless:load <name>` — Return profile as structured JSON
- `--headless:edit <name>` — Apply YAML field overrides to an existing profile
- `--headless:delete <name>` — Delete without confirmation
- `--headless:duplicate <source> <new_name>` — Copy profile to new name
- `--headless` (no subcommand) — List all profiles as JSON array

## Scripts

| Script | Description |
|--------|-------------|
| `validate-profile.py` | Validates band profile YAML against schema; supports `--derive-filename` for kebab-case naming |
| `list-profiles.py` | Scans `docs/band-profiles/` and returns profile summaries; supports `--check` to verify a specific profile |
| `tier-features.py` | Returns available/unavailable Suno features for a given tier |
| `diff-profiles.py` | Compares two profile YAML files and returns a structured JSON diff |

## Example Invocation

```
# Interactive
"Create a new band profile"
"Analyze my writing voice for the midnight-echoes profile"
"Health check the velvet-haze profile"

# Headless
--headless:create < profile.yaml
--headless:validate --profile midnight-echoes
--headless:edit midnight-echoes --field tier=pro
```

## Profiles Storage

Profiles are stored as YAML files at `docs/band-profiles/{profile-name}.yaml`. The schema is defined in `./references/profile-schema.md`.

## Part of the BMad Suno Band Manager Module

This skill is part of the BMad Suno Band Manager module. For the full guided experience, invoke Mac — the orchestrating agent — instead of using this skill directly.
