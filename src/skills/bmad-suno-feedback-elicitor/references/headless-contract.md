# Headless Output Contract

```json
{
  "feedback_analysis": {
    "triage_type": "clear|positive|vague|contradictory|technical",
    "identified_dimensions": ["vocals", "energy"],
    "confidence": "high|medium|low"
  },
  "adjustment_recommendations": {
    "style_prompt": {"add": [], "remove": [], "reorder_notes": ""},
    "exclusions": {"add": [], "remove": []},
    "sliders": {"weirdness": "", "style_influence": ""},
    "lyrics": {"changes": []},
    "model_suggestion": "",
    "studio_features": []
  },
  "confidence_scores": {"style_prompt": "high", "sliders": "medium"},
  "iteration_log": {"session_id": "", "round": 1, "tried": [], "user_reaction": "", "reasoning_chain": ""},
  "suggested_next_action": {"skill": "", "mode": "", "params": {}}
}
```

## Headless Input Contract

| Flag | Required | Description |
|------|----------|-------------|
| `--feedback` | Yes | Text string or JSON with feedback content |
| `--style-prompt` | Recommended | Original style prompt used for generation |
| `--model` | Optional | Suno model used (v4.5-all, v4 Pro, v4.5 Pro, v4.5+ Pro, v5 Pro, v5.5 Pro) |
| `--sliders` | Optional | JSON with Weirdness/StyleInfluence values |
| `--lyrics` | Optional | File path to original lyrics |
| `--band-profile` | Optional | Profile name for context loading |
| `--iteration-log` | Optional | File path to previous round's iteration log |
