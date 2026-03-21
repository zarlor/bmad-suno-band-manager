# Memory System for Mac

**Memory location:** `{project-root}/_bmad/_memory/band-manager-sidecar/`

## Core Principle

Tokens are expensive. Only remember what matters. Condense everything to its essence. Mac remembers your musical preferences, not every conversation.

## File Structure

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

### `patterns.md` — Learned Musical Patterns

**Load when needed.** Contains:
- User's genre tendencies and preferences discovered over time
- Vocal direction patterns (consistently prefers raw vs. polished, specific vocal characteristics)
- Production preferences (instrumentation density, mix style)
- Creativity comfort zone (how experimental they actually like to go)
- Feedback patterns (common complaints, common praise — what to optimize toward)

**Format:** Append-only, summarized regularly. Prune outdated entries.

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

## First Run

If sidecar doesn't exist, load `init.md` to create the structure.
