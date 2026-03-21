# Feedback Elicitor

The Feedback Elicitor guides users through a structured post-generation feedback loop after they have listened to their Suno output, translating subjective musical reactions into concrete parameter adjustments. It handles five feedback types — clear, positive, vague, contradictory, and technical — each with a tailored elicitation strategy. For vague feedback ("it just doesn't feel right"), it uses a three-phase guided elicitation sequence (binary narrowing, comparative anchoring, emotional vocabulary bridge) to draw out specifics. The skill produces structured adjustment recommendations that feed directly back into the Style Prompt Builder and Lyric Transformer.

## When to Use Directly vs. Through Mac

Use this skill directly when you have already generated a song on Suno and want to refine it based on what you heard. Use Mac (the orchestrating agent) when feedback refinement is part of a larger iterative workflow where you want seamless handoff between skills.

## Feedback Types

| Type | Signal | Strategy |
|------|--------|----------|
| **Clear** | Specific, actionable problem ("the guitar is too loud") | Direct parameter mapping |
| **Positive** | Likes the result, wants to evolve or lock in | Identify what to preserve vs. evolve |
| **Vague** | Knows something is off but cannot articulate it | Three-phase guided elicitation |
| **Contradictory** | Wants conflicting things ("more energetic but also chill") | First Principles reset; check for section contrast |
| **Technical** | Artifacts, glitches, pronunciation issues | Regeneration or Suno Studio feature recommendations |

## Workflow

1. **Receive Feedback** — Accept natural language reactions; capture everything including creative context
2. **Gather Context** — Collect original style prompt, lyrics, model, sliders, and intent as relevant
3. **Triage** — Classify feedback type (mixed feedback is handled per-component)
4. **Elicit/Map** — Apply type-specific strategy to extract actionable specifics
5. **Map to Adjustments** — Translate findings into style prompt changes, exclusion updates, slider adjustments, lyric adjustment specs, and model/Studio suggestions
6. **Present Recommendations** — Before/after narrative preview, structured adjustment package with confidence scores
7. **Handoff** — Offer to invoke Style Prompt Builder or Lyric Transformer with the adjustments; suggest band profile updates for systematic preferences

### Headless Mode (`--headless` or `-H`)

- `--headless:analyze` — Triage and categorize feedback only, return analysis JSON
- `--headless:adjustments` — Accept feedback + original prompts, return full adjustment recommendations
- `--headless` — Analyze + generate adjustments with balanced defaults

## Scripts

| Script | Description |
|--------|-------------|
| `parse-feedback.py` | Validates and extracts structured dimensions from feedback input in a single pass |
| `map-adjustments.py` | Maps feedback dimensions to Suno parameter adjustments with consistency validation |

## Example Invocation

```
# Interactive
"The vocals feel too polished on my last Suno generation"
"It just doesn't feel right — can you help me figure out what to change?"

# Headless
--headless:adjustments --feedback "vocals too polished, needs rawer feel" --style-prompt "warm indie rock..." --model v5-pro
--headless:analyze --feedback "it sounds off somehow"
```

## Output Integration

Adjustment recommendations are structured to feed directly into other skills:

- **Style prompt changes** go to the Style Prompt Builder via `--headless:refine`
- **Lyric changes** go to the Lyric Transformer via `--headless:refine` as an adjustment spec
- **Systematic preferences** can be saved back to the band profile
- **Iteration logs** can be persisted at `docs/feedback-history/` for multi-round refinement

## Part of the BMad Suno Band Manager Module

This skill is part of the [BMad Suno Band Manager](../bmad-suno-agent-band-manager/README.md) module. For the full guided experience, invoke Mac — the orchestrating agent — instead of using this skill directly.
