**Language:** Use `{communication_language}` for all output.
**Variables:** `{project-root}`, `{communication_language}`, `{user_name}`

---
name: init
description: First-run setup — progressive preference discovery with sensible defaults.
---

# First-Run Setup for Mac

Welcome! Let's get you making music fast. Setup happens naturally — not as an interview.

## Memory Location

Creating `{project-root}/_bmad/_memory/band-manager-sidecar/` for persistent memory.

## Progressive Preference Discovery

Instead of asking four questions before any creative work, use sensible defaults and discover preferences organically:

1. **Ask only one question up front:** "What kind of music are you looking to make today?" This gets the user into creative flow immediately.

2. **Set sensible defaults silently:**
   - Suno tier: Free (unlocks paid features when the user mentions them or says "I'm on Pro")
   - Interaction mode: Demo (the gentlest starting point — teach modes through experience, not explanation)
   - Exclusions: None
   - Band profile: None

3. **Discover preferences during the first song:**
   - If they provide detailed direction → note Studio tendencies in patterns
   - If they mention Pro features → ask about their tier and update
   - If they express strong preferences ("I hate autotune") → capture as default exclusions
   - If they mention a band or project → offer to create a profile after the song is done

4. **After the first song is complete**, briefly mention what you learned: "By the way, I noticed you're pretty hands-on — Studio mode might be your speed. And I saved your preference for raw vocals. You can change any of this anytime, just tell me."

**Help with tier discovery:** If the user doesn't know their tier, help them figure it out: "When you open Suno, check the top-right — it'll say Free, Pro, or Premier. Or just tell me what you see in the interface and I'll figure it out."

## Initial Structure

Creating:
- `index.md` — your preferences, active work, essential context
- `patterns.md` — musical preferences I learn over time
- `chronology.md` — session timeline

### `index.md` template (REQUIRED marker pairs)

New sidecars MUST be born already-migrated. The `## Recently Published` and `## Catalog Status` sections are regenerated from songbook ground truth by `./scripts/regenerate-index-sections.py` (inside the agent skill), which requires HTML comment marker pairs to locate the rewrite targets. Missing markers cause every `save-memory` regeneration call and every post-unpack integration to error out until the sidecar is hand-migrated.

Include the marker pairs below verbatim when creating `index.md` for the first time. Stub content between markers is fine — the regenerator will replace it on the first `[SM]` cycle. Narrative sections (Current Work, Pending / Parked Work, Session History, User Preferences, etc.) fill in organically as sessions accumulate.

```markdown
# Band Manager Sidecar — {user_name}

## User Preferences
- Suno tier: {discovered tier or "Free (default)"}
- Interaction mode: {Demo/Studio/Jam}
- Default exclusions: {list or "none"}
- Active band profile: {name or "none"}

## Current Work
_(empty — first session)_

## Pending / Parked Work
_(empty — first session)_

## Recently Published

<!-- derived:recently-published:start -->

_(auto-generated from songbook on next save — no songs published yet)_

<!-- derived:recently-published:end -->

## Catalog Status

<!-- derived:catalog-status:start -->

_(auto-generated from songbook on next save — catalog is empty)_

<!-- derived:catalog-status:end -->

## Session History
- {YYYY-MM-DD}: First Breath — initial setup, {brief summary of discovery}
```

**Do not omit the marker pairs**, even if the catalog is empty. The regenerator treats "no songs" as a normal case and writes stub content between the markers, but it cannot insert the markers themselves.

## Access Boundaries

Create `access-boundaries.md` with:

```markdown
# Access Boundaries for Mac

## Read Access
- docs/band-profiles/
- docs/voice-context-*.md
- {project-root}/_bmad/_memory/band-manager-sidecar/

## Write Access
- {project-root}/_bmad/_memory/band-manager-sidecar/
- docs/voice-context-{user}.md (current user's file only)

## Deny Zones
- All other directories
```

## Voice File

After the first session — or any time the user shares significant personal or creative context — offer to create a voice/context file: "I'm getting to know your creative style. Want me to start a voice file so I remember all this next time? It'll live in your docs/ folder."

If yes, create `docs/voice-context-{username}.md` (username normalized: lowercase, spaces→hyphens). See `memory-system.md` for the file structure. Populate initial content from what was learned during the session.

## Ready

Setup complete! Store all discovered preferences in `index.md`. **When complete:** Return to main activation flow and present the menu.
