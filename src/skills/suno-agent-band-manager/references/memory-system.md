# Memory System for Mac

**Memory location:** `{project-root}/_bmad/_memory/band-manager-sidecar/`

## Core Principle

Tokens are expensive. Only remember what matters. Condense everything to its essence. Mac remembers your musical preferences, not every conversation.

## File Structure

### `voice-context-{username}.md` — User Voice & Context (in `docs/`)

**Load on activation** (before greeting). This is the user's durable creative identity file — the "slow memory" that persists across sessions and machines. Lives in `docs/` alongside the user's other files, visible and portable.

**Contains:**
- **Who I Am** — Personal history, creative background, identity, what drives them
- **How I Write** — Form, themes, emotional drivers, stylistic evolution, influences
- **How to Work With Me** — Communication preferences, what to avoid, what works best
- **Creative Catalog** — Songs created, albums, key production notes, playlist structure
- **Suno Preferences** — Tier, models, persona/voice, default slider settings, exclusions, personal sonic preferences (e.g. bass-forward, always include Audio Influence). Production learnings (metatag behavior, style prompt engineering, model quirks) belong in skills reference docs and sidecar `patterns.md`, not here.
- **Session History** — Condensed timeline of sessions and milestones
- **Current Creative State** — Active WIPs, directions being explored, threads to pick up

**Multi-user:** One file per user, named by normalized username (lowercase, spaces→hyphens): `voice-context-alex.md`, `voice-context-bob-smith.md`. Mac writes only to the current user's file.

**Update discipline:** Only when genuinely new durable context emerges — new personal history, new creative work, significant preference changes, production breakthroughs. Not after every minor exchange.

**Relationship to sidecar:** The voice file is the "slow memory" (who the user IS). The sidecar index is the "fast memory" (what the user is DOING right now). Both are loaded on activation. Over time, sidecar `patterns.md` and `chronology.md` content should migrate into the voice file — Mac offers this during save prompts.

**Size management:** If file exceeds ~2000 lines, offer to compact: summarize older session history, consolidate redundant entries, but preserve personal/voice sections in full.

**Companion Files table:** The voice file should include a **Companion Files — Load On Demand** section near the top (after the opening instruction, before the main content). This table indexes satellite documents that extend the voice file with depth that doesn't live in every session's context:

| File | What | When to load |
|------|------|-------------|
| `docs/example-deep-dive.md` | Detailed context on [topic] | When discussing [trigger] |

When the agent creates a satellite document during a session, add a reference entry at creation time. At session-end save, audit for new `docs/` files not yet in the table. Each entry needs: file path, one-line description, and when-to-load trigger. The voice file is loaded at session start; companion files are loaded only when the topic calls for them.

### `index.md` — Primary Source

**Load on activation.** Contains:
- User's Suno tier and model preference
- Default interaction mode (Demo/Studio/Jam)
- Default exclusions and vocal preferences
- Active band profile (if any)
- Current session state (if saved mid-work)
- Quick reference to other files if needed

**Update:** When essential context changes (immediately for critical data).

### `access-boundaries.md` — Access Control (Required)

**Load on activation.** Contains:
- **Read access** — `docs/band-profiles/`, sidecar memory
- **Write access** — sidecar memory only
- **Deny zones** — Everything else

**Critical:** On every activation, load these boundaries first. Before any file operation (read/write), verify the path is within allowed boundaries. If uncertain, ask user.

### `patterns.md` — Learned Musical Patterns & Production Knowledge

**Load when needed.** Contains:

**Musical Patterns** (creative preferences):
- User's genre tendencies and preferences discovered over time
- Vocal direction patterns (consistently prefers raw vs. polished, specific vocal characteristics)
- Production preferences (instrumentation density, mix style)
- Creativity comfort zone (how experimental they actually like to go)
- Feedback patterns (common complaints, common praise — what to optimize toward)

**Production Knowledge** (what works for THIS user on Suno):
- Slider preferences by song type (e.g., "Weirdness 55 + Style Influence 75 for structured songs")
- Genre term combinations that produced desired results (e.g., "'progressive groove metal' works better than 'progressive metal' for my sound")
- Metatag effectiveness (which tags reliably achieved the intended effect)
- Generation patterns (settings/approaches that led to first-gen success vs. needed iteration)
- Model-specific notes (differences the user noticed between v5 and v5.5 for their music)

**Format:** Append-only, summarized regularly. Prune outdated entries. Each production knowledge entry should include: the finding, the context (which song/date), and a confidence note (one song vs. consistent across multiple). These are the user's personal findings — not universal prescriptions for all users.

### `chronology.md` — Timeline

**Load when needed.** Contains:
- Session summaries (what was created, what was refined)
- Band profile evolution (when profiles were created/modified)
- Significant breakthroughs (when a song really clicked — what worked)

**Format:** Append-only. Prune regularly; keep only significant events.

## Memory Persistence Strategy

### Write-Through (Immediate Persistence)

Persist immediately when:
1. **User preferences change** — tier, default mode, exclusions
2. **First-run setup completes** — all initial preferences
3. **User requests save** — explicit `[SM] - Save Memory` capability

### Checkpoint (Periodic Persistence)

Update periodically after:
- Completing a create-song or refine-song flow
- User explicitly switches interaction modes or updates preferences mid-session
- When file grows beyond target size

### Save Triggers

**After these events, always update memory:**
- First-run setup completion
- User changes default preferences (tier, mode, exclusions)
- User explicitly requests save

**Memory is updated via the `[SM] - Save Memory` capability which:**
1. Reads current index.md
2. Updates with current session context
3. Writes condensed, current version
4. Checkpoints patterns.md and chronology.md if needed

## Write Discipline

**Handoff checkpoint:** Before writing to any memory file, apply the Handoff Checkpoint Pattern — surface what will be written, get user confirmation, then write. This is especially important for patterns.md where personal preferences and production knowledge are being recorded. The user controls what gets stored as a "pattern" about them.

Before writing to memory, ask:

1. **Is this worth remembering?**
   - If no -> skip
   - If yes -> continue

2. **What's the minimum tokens that capture this?**
   - Condense to essence
   - No fluff, no repetition

3. **Which file?**
   - `index.md` -> essential context, active work, preferences
   - `patterns.md` -> musical quirks, recurring feedback patterns
   - `chronology.md` -> session summaries, significant events

4. **Does this require index update?**
   - If yes -> update `index.md` to point to it

## Memory Maintenance

Regularly (every few sessions or when files grow large):
1. **Condense verbose entries** — Summarize to essence
2. **Prune outdated content** — Move old items to chronology or remove
3. **Consolidate patterns** — Merge similar musical preference entries
4. **Update chronology** — Archive significant past events

## State Checkpoints (Context Compaction Resilience)

After each complete create-song or refine-song cycle, write a lightweight state checkpoint to index.md containing:
- Current song: title, style prompt (first 100 chars), model, band profile
- Active mode (Demo/Studio/Jam)
- Refinement round count (if refining)

This ensures that if context compaction drops earlier conversation, Mac can recover essential state from memory.

## First Run

If sidecar doesn't exist, load `./references/init.md` to create the structure.
