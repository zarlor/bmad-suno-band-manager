# Lyric Transformer

The Lyric Transformer converts poems, raw text, and rough lyrics into Suno-ready structured song lyrics with metatags, proper section architecture, and rhythmic consistency. It offers seven transformation options that users can mix and match based on how much creative control they want to retain — from lightweight structure tagging to full rewrites — plus a Word Fidelity mode for writers who want their exact words preserved. The skill enforces Suno's lyrics character limits (5,000 hard limit on v4.5+, ~3,000 quality budget), runs cliche detection by default (Suno's vocal engine amplifies cliches), and integrates with band profile writer voice data to maintain authentic voice.

## When to Use Directly vs. Through Mac

Use this skill directly when you have existing text (a poem, prose, rough lyrics) that needs to be transformed into Suno-ready format. Use Mac (the orchestrating agent) when lyric transformation is part of a full song-creation workflow that includes profile management, style prompt building, or feedback refinement.

## Transformation Options

| Code | Transformation | Description |
|------|---------------|-------------|
| **ST*** | Structure Tagging | Add section metatags (`[Verse]`, `[Chorus]`, etc.) and descriptor metatags |
| **CE** | Chorus Extraction | Identify repeated/hook material and promote to chorus |
| **CC*** | Chorus Creation | Write a new chorus derived from the poem's emotional core |
| **RA*** | Rhythmic Adjustment | Normalize syllable counts for stable vocal phrasing |
| **RE** | Rhyme Enhancement | Strengthen rhyme patterns for better Suno vocal delivery |
| **FR** | Full Rewrite | Complete rewrite as song lyrics preserving theme and imagery |
| **CD*** | Cliche Detection | Flag overused phrases and suggest genre-aware alternatives |
| **WF** | Word Fidelity Mode | Use writer's exact words; only add structure (mutually exclusive with FR) |

*Asterisk indicates default recommendations for raw text input.*

### Headless Mode (`--headless` or `-H`)

- `--headless:analyze` — Analyze input only, return analysis JSON
- `--headless:transform` — Full transformation with default options (ST + CC + RA + CD)
- `--headless:refine` — Apply targeted adjustments from Feedback Elicitor's adjustment spec
- `--headless` with text — Analyze + transform with balanced defaults

## Scripts

| Script | Description |
|--------|-------------|
| `validate-lyrics.py` | Validates lyrics structure, metatags, formatting, and 3,000-char limit |
| `cliche-detector.py` | Detects cliche phrases with categorized genre-aware alternatives |
| `syllable-counter.py` | Counts syllables per line, analyzes rhythm, and estimates song duration |
| `analyze-input.py` | Pre-analyzes raw text for existing structure, repeated phrases, and rhyme pairs |
| `section-length-checker.py` | Checks section lengths against expected ranges from the section-jobs framework |
| `lyrics-diff.py` | Produces annotated diff between original and transformed lyrics |
| `validate-options.py` | Validates transformation option selections against mutual exclusion rules |
| `assemble-summary.py` | Assembles the Transformation Summary block from script outputs |

## Example Invocation

```
# Interactive
"Transform this poem into a song for my midnight-echoes profile"
"Convert my lyrics for Suno — just tag the structure, keep my words"

# Headless
--headless:transform --text "poem text here" --options ST,CC,RA,CD --profile midnight-echoes
--headless:refine --source-lyrics "current lyrics" --adjustments adjustments.json
--headless:analyze --text "poem text here"
```

## Key Constraints

- **5,000-character hard limit** (v4.5+), **~3,000-character quality budget** — beyond 3,000, Suno rushes sections; beyond 5,000, content is silently truncated
- **FR and WF are mutually exclusive** — you cannot fully rewrite while preserving exact words
- **CE is skipped when FR is selected** — full rewrite subsumes chorus extraction
- Refinement mode accepts adjustment specs from the Feedback Elicitor for targeted changes

## Part of the BMad Suno Band Manager Module

This skill is part of the BMad Suno Band Manager module. For the full guided experience, invoke Mac — the orchestrating agent — instead of using this skill directly.
