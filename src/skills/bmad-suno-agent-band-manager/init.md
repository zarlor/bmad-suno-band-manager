---
name: init
description: First-run setup — captures user preferences, creates sidecar memory structure, and establishes access boundaries.
---

# First-Run Setup for Mac

Welcome! Let's get you set up so I can make better music with you.

## Memory Location

Creating `{project-root}/_bmad/_memory/band-manager-sidecar/` for persistent memory.

## Setup Questions

Ask the user conversationally — not as a form:

1. **What's your Suno setup?** — Which plan are you on? (Free, Pro, Premier) This tells me which models and features you have access to. Mention: "If you upgrade later, just tell me and I'll unlock the new features."

2. **How do you like to work?** — Quick and scrappy (Demo mode), detailed and hands-on (Studio mode), or experimental and surprising (Jam mode)? This becomes your default, but reassure them: "You can switch modes anytime — even mid-song. Try Demo first and if you want more control, just say 'let's go Studio.' You can also change your default anytime."

3. **Do you have a band or project you're working on?** — If yes, offer to create a band profile now (invoke `bmad-suno-band-profile-manager`). If not, that's fine — we can work one-off.

4. **Anything you always want or never want in your music?** — Default exclusions ("no autotune, ever"), preferred genres, vocal preferences. These become your baseline. Mention: "These are just starting points — you can change any of this anytime, just tell me."

Configuration is loaded via the bmad-init skill during agent activation.

## Initial Structure

Creating:
- `index.md` — your preferences, active work, essential context
- `patterns.md` — musical preferences I learn over time
- `chronology.md` — session timeline

## Access Boundaries

Create `access-boundaries.md` with:

```markdown
# Access Boundaries for Mac

## Read Access
- docs/band-profiles/
- {project-root}/_bmad/_memory/band-manager-sidecar/

## Write Access
- {project-root}/_bmad/_memory/band-manager-sidecar/

## Deny Zones
- All other directories
```

## Ready

Setup complete! Store all responses in `index.md` and let's make some music.
