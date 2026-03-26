**Language:** Use `{communication_language}` for all output.

---
name: browse-songbook
description: Browse past songs, successful prompts, and creative history.
menu-code: SB
---

# Browse Songbook

Browse your creative portfolio — past songs, successful prompts, iteration history, and creative evolution.

## Step 1: Scan Available Content

Check these locations for saved work:
- `{project-root}/docs/songbook/` — Saved lyrics from Lyric Transformer
- `{project-root}/docs/feedback-history/` — Iteration logs from Feedback Elicitor
- `{project-root}/_bmad/_memory/band-manager-sidecar/chronology.md` — Session timeline

If no saved work exists, let the user know: "Your songbook is empty — it'll grow as you create and save songs. Want to start your first one?"

## Step 2: Present Overview

Group by band profile (or "Unaffiliated" for one-offs):

```
## Your Songbook

### {Band Profile Name}
- {Song Title} — {date}, {transformations applied}, {model used}
  Style prompt: {first 80 chars}...

### Unaffiliated
- {Song Title} — {date}
```

## Step 3: Interact

The user can:
- **View details** — Show full lyrics, style prompt, parameters, and iteration history for a song
- **Reuse** — "Use this style prompt as a starting point for a new song" → route to create-song with pre-loaded context
- **Compare** — Show two songs side-by-side to see how their sound evolved
- **Export** — Present all data for a song in a copy-ready format

## Output

Keep it conversational — this is Mac browsing the record collection, not a database query.
