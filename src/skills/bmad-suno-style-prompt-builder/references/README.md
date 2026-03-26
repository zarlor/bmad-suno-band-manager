# Style Prompt Builder

The Style Prompt Builder generates model-aware Suno style prompts optimized for the user's chosen model tier, blending band profile baselines with per-song creative direction. It understands the fundamental differences between Suno model families — v4.5 wants conversational descriptions while v5 wants crisp film-brief descriptors — and produces a complete prompt package: style prompt, exclusion prompt, slider recommendations, and an optional experimental wild card variant. The skill enforces the 1,000-character limit (200 for v4 Pro) and prioritizes the critical first 200 characters where Suno's attention is strongest.

## When to Use Directly vs. Through Mac

Use this skill directly when you already have a band profile or clear musical direction and just need a style prompt built. Use Mac (the orchestrating agent) when style prompt creation is part of a larger workflow that includes profile setup, lyric transformation, or post-generation feedback refinement.

## Operations

### Interactive Mode (default)

1. **Gather Inputs** — Collects song direction, band profile, model selection, creativity mode (conservative/balanced/experimental), and specific requests
2. **Build Style Prompt** — Constructs model-specific prompt with critical zone awareness; decomposes reference tracks into concrete descriptors (never puts artist names in prompts)
3. **Build Exclusion Prompt** — Generates "Exclude Styles" content from profile defaults, user requests, and genre inference
4. **Slider Recommendations** — Weirdness, Style Influence, and Audio Influence settings based on creativity mode and tier
5. **Wild Card Variant** — Experimental alternative that pushes creative boundaries
6. **Validate & Present** — Character count validation, copy-ready output blocks, refinement loop

### Headless Mode (`--headless` or `-H`)

- `--headless:from-profile` — Generate prompt package using only profile baseline
- `--headless:custom` — Generate from provided parameters without a profile
- `--headless:refine` — Apply structured adjustments from the Feedback Elicitor to an existing prompt
- `--headless:migrate` — Reformat an existing prompt from one model's style to another
- `--headless` with profile name — Hybrid mode (profile baseline + overrides)

## Scripts

| Script | Description |
|--------|-------------|
| `validate-prompt.py` | Validates style prompt character count (model-specific limits), critical zone content, and structure |

## Example Invocation

```
# Interactive
"Build a style prompt for my midnight-echoes profile"
"Create a Suno prompt for a dreamy indie folk song on v5 Pro"

# Headless
--headless:from-profile --profile midnight-echoes
--headless:custom --model v5-pro --genre "indie folk" --mood "dreamy, introspective"
--headless:migrate --prompt "warm indie rock..." --from v4.5-pro --to v5-pro
```

## Creativity Modes

| Mode | Behavior | Weirdness Range |
|------|----------|-----------------|
| **Conservative** | Genre-pure descriptors, proven combinations | 20-35 |
| **Balanced** (default) | Standard approach, some distinctive touches | 40-60 |
| **Experimental** | Unexpected fusions, unusual descriptors | 65-85 |

## Supported Models

| Model | Prompt Style | Character Limit |
|-------|-------------|-----------------|
| v4.5-all / v4.5 Pro / v4.5+ Pro | Conversational, flowing sentences | 1,000 |
| v5 Pro | Crisp, 4-7 film-brief descriptors | 1,000 |
| v4 Pro | Simple, straightforward descriptors | 200 |

## Part of the BMad Suno Band Manager Module

This skill is part of the BMad Suno Band Manager module. For the full guided experience, invoke Mac — the orchestrating agent — instead of using this skill directly.
