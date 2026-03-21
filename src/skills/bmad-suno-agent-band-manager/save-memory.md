---
name: save-memory
description: Explicitly save current session context to memory
menu-code: SM
---

# Save Memory

Immediately persist the current session context to memory.

## Process

1. **Read current index.md** — Load existing context from `{project-root}/_bmad/_memory/band-manager-sidecar/index.md`

2. **Update with current session:**
   - Active song work (style prompt, lyrics, parameters, model, band profile in use)
   - User preferences discovered or changed this session
   - Current interaction mode preference
   - Any band profile updates pending
   - Next steps to continue

3. **Write updated index.md** — Replace content with condensed, current version

4. **Checkpoint other files if needed:**
   - `patterns.md` — Add new musical preferences discovered (genre tendencies, vocal preferences, exclusion patterns, creativity level preferences)
   - `chronology.md` — Add session summary if significant work was done

## Output

Confirm save with brief summary: "Memory saved. {brief-summary-of-what-was-updated}"
