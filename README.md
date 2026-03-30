# BMad Suno Agent — Mac, the Band Manager

An AI-powered music production assistant that helps you create professional Suno-ready song packages through guided creative conversation. Mac orchestrates four specialized skills into a seamless workflow: from initial inspiration to a complete package — style prompt, lyrics, and parameter recommendations — that you can paste directly into Suno.

## Features

You talk to Mac like you'd talk to a producer. Tell Mac what kind of song you want — a genre, a mood, a poem, a feeling, a reference track — and Mac produces a complete package:

- **Style Prompt** — Model-specific, optimized for your chosen Suno model (v4.5-all, v5 Pro, etc.)
- **Structured Lyrics** — With Suno metatags (`[Verse]`, `[Chorus]`, etc.), rhythmic consistency, and cliché detection
- **Exclusion Prompt** — What Suno should avoid
- **Parameter Recommendations** — Slider values, vocal gender, persona references (tier-aware)
- **Wild Card Variant** — An experimental alternative to push creative boundaries

After you try the output on Suno, Mac helps you refine through a structured feedback loop — translating subjective reactions ("it doesn't feel right") into concrete parameter adjustments.

### Highlights

- **Three Interaction Modes** — Demo (quick and scrappy), Studio (deep customization), Jam (experimental)
- **Band Profiles** — Persistent sonic identity across songs (genre, vocal direction, style baseline, writer voice)
- **Writer Voice Preservation** — Analyzes your writing samples to maintain your authentic voice when transforming lyrics
- **Tier-Aware** — Knows what's available on Free, Pro, and Premier plans; never shows features you can't access
- **Feedback Loop** — Five-type feedback triage with guided elicitation for users who can't articulate what's wrong
- **Instrumental Support** — Dedicated workflow for instrumental-only tracks
- **Non-English Support** — Language detection with Suno-specific guidance
- **Memory System** — Remembers your preferences, musical patterns, and creative history across sessions

## Quick Start

1. **Invoke Mac** — Use the trigger phrase "talk to Mac," "Band Manager," or "create a song for Suno"
2. **Tell Mac what you want** — "Make me a sad indie folk song" or paste a poem
3. **Get your package** — Mac produces a complete style prompt + lyrics + parameters
4. **Try it on Suno** — Paste into Suno's Custom Mode fields
5. **Come back and refine** — Tell Mac what worked and what didn't

For detailed documentation on all features, interaction modes, band profiles, the feedback loop, direct skill access, and headless/automation modes, see the [Usage Guide](USAGE.md).

## Architecture

Mac is an orchestrating agent that coordinates four specialized skills:

```
                        ┌─────────────────────┐
                        │   Mac (Band Manager) │
                        │   Orchestrating Agent │
                        └──────────┬──────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                     │
    ┌─────────┴────────┐ ┌────────┴────────┐ ┌─────────┴────────┐
    │  Band Profile    │ │ Style Prompt    │ │ Lyric            │
    │  Manager         │ │ Builder         │ │ Transformer      │
    └──────────────────┘ └─────────────────┘ └──────────────────┘
                                   │
                         ┌─────────┴────────┐
                         │ Feedback         │
                         │ Elicitor         │
                         └──────────────────┘
```

The orchestrating agent and each skill have their own documentation:

| Component | Purpose | Key Scripts |
|-----------|---------|-------------|
| [**Mac (Band Manager)**](src/skills/bmad-suno-agent-band-manager/references/README.md) | Orchestrating agent — guides the full song creation workflow across all skills | `pre-activate.py`, `validate-path.py`, `check-memory-health.py` |
| [**Band Profile Manager**](src/skills/bmad-suno-band-profile-manager/references/README.md) | CRUD for band identity profiles, writer voice analysis, tier feature awareness | `validate-profile.py`, `list-profiles.py`, `tier-features.py`, `diff-profiles.py` |
| [**Style Prompt Builder**](src/skills/bmad-suno-style-prompt-builder/references/README.md) | Model-aware style prompt generation with creativity modes and wild card variants | `validate-prompt.py` |
| [**Lyric Transformer**](src/skills/bmad-suno-lyric-transformer/references/README.md) | Poem/text to Suno-ready structured lyrics with metatags and cliché detection | `validate-lyrics.py`, `cliche-detector.py`, `syllable-counter.py`, `analyze-input.py`, `section-length-checker.py`, `lyrics-diff.py` |
| [**Feedback Elicitor**](src/skills/bmad-suno-feedback-elicitor/references/README.md) | Post-generation feedback triage and guided refinement with musical vocabulary translation | `parse-feedback.py`, `map-adjustments.py` |

Each skill can be invoked directly for standalone use — see the linked READMEs for details, headless modes, and examples.

## Prerequisites

- **Claude Code** with a model that supports tool use (Claude Sonnet 4+, Claude Opus 4+)
- **BMad Method (BMB module)** installed — Mac is built as a BMad module
- **Suno account** (free tier works; Pro/Premier unlocks additional features)

### Optional: Audio Analysis

For objective audio measurements (BPM, key, energy, chord progressions, playlist sequencing), install:

```bash
pip install librosa numpy
```

These are optional — the full song creation and refinement workflow works without them. Mac will offer to help install if you try to use audio analysis features without them.

## Installation

**Requires [BMad Method](https://github.com/bmad-code-org/BMAD-METHOD/) (v6.2.0+).**

1. Copy the skill folders from `src/skills/` into your project's `.claude/skills/` directory (or use your preferred installation method).

2. Run the setup skill to configure the module:

```
/bmad-suno-setup
```

3. The setup skill will ask you to configure:
   - **Suno tier** — Free, Pro, or Premier (determines available features)
   - **Default interaction mode** — Demo, Studio, or Jam
   - **Band profiles folder** — Where to store band identity files
   - **Songbook folder** — Where to store saved songs

4. The setup skill registers all capabilities with the help system and creates the necessary directories.

5. On first activation, Mac will greet you and confirm your setup. All preferences are changeable anytime through conversation — just tell Mac "I upgraded to Pro" or "make Studio my default mode."

## Updating

If you installed via symlinks (the default), `git pull` is all you need — your symlinks pick up all changes automatically, including the new setup skill.

To reconfigure settings or migrate legacy config to the new format, run:

```
/bmad-suno-setup
```

The setup skill detects any existing config (including from the old `npx bmad-method install` format) and uses your saved values as defaults. It writes both the shared config format (`_bmad/config.yaml`) and per-module config files (`_bmad/core/config.yaml`, `_bmad/suno/config.yaml`) that `bmad-init` reads at runtime. Your preferences, band profiles, songbook, and memory are all preserved.

## Suno Model Compatibility

Mac supports Suno models from v4 through v5.5 Pro, with model-specific prompt optimization and character limit enforcement. See the [Suno Reference](SUNO-REFERENCE.md) for models, plans, and prompting, and the [Studio & Editor Reference](STUDIO-EDITOR-REFERENCE.md) for post-generation editing (Legacy Editor, Studio, Stems, Warp Markers, and more).

## File Structure

```
src/skills/
├── bmad-suno-setup/                # Module setup and configuration
│   ├── SKILL.md                    # Setup skill — config collection and registration
│   ├── assets/
│   │   ├── module.yaml             # Module metadata and config variables
│   │   └── module-help.csv         # Capability registry (v1.4.0 format)
│   └── scripts/
│       ├── merge-config.py         # Config file merge + init-compatible output
│       ├── merge-help-csv.py       # Help CSV merge
│       └── cleanup-legacy.py       # Legacy file cleanup
├── bmad-suno-agent-band-manager/   # Mac — orchestrating agent
│   ├── SKILL.md                    # Agent persona, activation, orchestration
│   ├── bmad-skill-manifest.yaml    # Skill type identifier
│   ├── references/
│   │   ├── create-song.md          # Main song creation workflow
│   │   ├── refine-song.md          # Post-generation refinement loop
│   │   ├── browse-songbook.md      # Creative history browsing
│   │   ├── save-memory.md          # Session persistence
│   │   ├── init.md                 # First-run setup
│   │   ├── memory-system.md        # Memory discipline and structure
│   │   ├── SUNO-REFERENCE.md       # Suno platform reference
│   │   └── STUDIO-EDITOR-REFERENCE.md
│   └── scripts/
│       ├── pre-activate.py         # First-run detection, scaffolding, menu rendering
│       ├── validate-path.py        # Access boundary enforcement
│       └── check-memory-health.py  # Memory file size monitoring
├── bmad-suno-band-profile-manager/ # Band profile CRUD and writer voice analysis
├── bmad-suno-style-prompt-builder/ # Model-aware style prompt generation
├── bmad-suno-lyric-transformer/    # Poem/text to Suno-ready lyrics
├── bmad-suno-feedback-elicitor/    # Post-generation feedback refinement
└── _shared/                        # Shared Python utilities
```

## License

MIT — see [LICENSE](LICENSE) for details.

## Credits

Built with the [BMad Method](https://github.com/bmad-code-org/BMAD-METHOD/) — Build More, Architect Dreams.
