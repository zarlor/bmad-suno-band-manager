**Language:** Use `{communication_language}` for all output.
**Variables:** `{project-root}`, `{communication_language}`

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
   - Production knowledge discovered (see Step 2b)
   - Next steps to continue

   ### Handoff Checkpoint (before writes)

   Before writing to any memory files, surface a brief summary of what will be saved:

   > "Here's what I'd save: **[2-4 bullet summary of changes to index.md, patterns.md, chronology.md]**. Sound right?"

   Wait for confirmation. The user may want to exclude something or add context. This is especially important for patterns.md where personal preferences are being recorded — the user should control what gets stored as a "pattern" about them.

   ### 2b. Production knowledge check

   After create-song or refine-song cycles, check for discoverable production patterns:
   - Repeated slider settings across successful songs ("You've used Weirdness 55 on your last 3 songs — want me to note that as your sweet spot?")
   - Genre term combinations that consistently landed
   - Metatag patterns that achieved intended effects
   - What settings/approaches led to first-generation success vs. iteration

   Store these in patterns.md under the Production Knowledge section — as the user's personal findings, not universal prescriptions.

3. **Write updated index.md** — Replace content with condensed, current version

4. **Checkpoint other files if needed (parallel batch)** — These writes are independent; run in parallel:
   - `patterns.md` — Add new musical preferences discovered (genre tendencies, vocal preferences, exclusion patterns, creativity level preferences) and production knowledge (see Step 2b)
   - `chronology.md` — Add session summary if significant work was done

5. **Companion files audit** — If the user has a voice file, check whether any new `docs/` files were created during the session that aren't in the voice file's Companion Files table. If so, offer to add them: "I notice we created [file] this session — want me to add it to your companion files index?" Include: file path, one-line description, and when-to-load trigger phrase.

6. **Reference reconciliation check** — Before finalizing the save, do a quick consistency scan:
   - If any song titles, band profile names, or playlist orders changed during this session, load `./references/reconcile.md` and run reconciliation
   - Compare the values being written to index.md/chronology.md against what already exists in the voice context file and songbook — flag any inconsistencies
   - This step is fast (just a scan) and only triggers the full reconciliation handoff if stale references are actually found
   - If nothing changed this session, skip silently

## Output

Confirm save with a brief session recap in Mac's voice:

"Memory saved. Here's what we covered:
- {2-4 bullet points summarizing the session: songs created/refined, preferences discovered, profiles updated}
- Ready to pick up right here next time."

**When complete:** Return to the main menu or continue with the user's next request.
