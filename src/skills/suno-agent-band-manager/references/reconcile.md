**Language:** Use `{communication_language}` for all output.
**Variables:** `{project-root}`, `{communication_language}`

---
name: reconcile
description: Reconcile stale references across docs and sidecar files after authoritative data changes.
---

# Reconcile References

When authoritative data changes in one file, stale references may persist in other files. This reference defines how to detect and fix them.

## When to Run

Reconciliation is triggered after these events:
- A song title changes (rename in songbook, working title → final title)
- A song publishes (WIP → published, audio file added)
- A playlist reorders or adds/removes tracks
- A band profile name or key attributes change
- A WIP is abandoned or superseded
- Tier/preference changes (Free → Pro, default mode changes)

## Authoritative Sources

| Data | Authoritative Source | May Be Referenced In |
|------|---------------------|---------------------|
| Song title | Songbook entry (`docs/songbook/{band}/{song}.md`) | Playlist YAML, playlist ordering doc, voice context, sidecar index/chronology, WIP files, companion files |
| Song status (WIP/published) | Songbook entry | Voice context (WIP sections, catalog), sidecar index, WIP files that should be deleted |
| Playlist order & track numbers | Playlist ordering doc (`docs/*-playlist-ordering.md`) | Voice context (catalog section), songbook placement notes |
| Band profile (genre, vocal, name) | Band profile YAML (`docs/band-profiles/*.yaml`) | Voice context, songbook entries referencing profile values, sidecar index |
| Tier/preferences | Sidecar index / config (`_bmad/config*.yaml`) | Voice context (Suno Setup section), band profile tier field |
| Voice file location | The file itself (`docs/voice-context-*.md`) | Pre-activate expectations, sidecar index (Key Files section) |

## Process

### Step 1: Identify the Change

Determine what changed and what the old vs. new values are. The trigger context (create-song post-publish, save-memory, profile edit, etc.) provides this. Note:
- **What** changed (song title, status, playlist order, profile attribute)
- **Old value** (the value being replaced)
- **New value** (the authoritative current value)
- **Source file** (where the authoritative change was made)

### Step 2: Search for Stale References

Search these locations for the OLD value:

- `docs/songbook/` — all .md files
- `docs/band-profiles/` — all .yaml files
- `docs/*-playlist-ordering.md` — playlist ordering docs
- `docs/*.yaml` — playlist YAML files
- `docs/voice-context-*.md` — voice/context files
- `docs/wip-*.md` — WIP files (may need deletion if song published)
- `docs/*-family-history-*.md` — companion files
- `{project-root}/_bmad/_memory/band-manager-sidecar/` — index.md, chronology.md, patterns.md

Use exact string matching first, then check for variations:
- Title with/without subtitle
- Different casing
- Partial matches (e.g., just the first word of a multi-word title)
- Working title vs. final title

### Step 3: Handoff Checkpoint

Surface all proposed updates to the user before writing anything:

> "I found references to **[old value]** in these files:
> - `[file1]` line [N]: [context snippet]
> - `[file2]` line [N]: [context snippet]
>
> Want me to update them all to **[new value]**? I can also do them one by one if you want to review each."

Wait for confirmation. The user may want to:
- Update all at once
- Review and approve each individually
- Skip some (the old reference may be intentional — historical context, "formerly known as")
- Skip entirely

### Step 4: Apply Updates

For each confirmed update:
1. Read the target file
2. Replace the old value with the new value **in context** — understand the surrounding structure, don't blind find-replace
3. For WIP files of published songs: offer to delete the WIP file entirely (the songbook entry is the authoritative record now)
4. Write the updated file
5. Report what was changed: "Updated 3 files, deleted 1 WIP file"

### Special Cases

**Playlist reordering:** When track numbers change, update ALL track number references in the voice context catalog section. This is a bulk update — present the full before/after for the catalog section rather than individual line changes.

**WIP → Published:** Check for `docs/wip-*` files that reference the published song. Offer to delete them — the songbook entry supersedes the WIP. If the WIP contains creative context not in the songbook (brainstorm notes, unused fragments), ask whether to preserve it or archive relevant parts into the songbook notes.

**Band profile rename:** This is the widest-impact change — every songbook entry references the profile by name in frontmatter. Surface the scope before proceeding.

## Scope Boundaries

- Only search within Mac's access boundaries (docs/ and sidecar memory)
- Never modify files outside the known document locations
- If a reference is ambiguous (partial match, could refer to something else), ask rather than assume
- Keep it lightweight — this is a quick consistency check, not a full audit
- Reconciliation is a SERVICE, not a gate — never block the user's workflow to force reconciliation. Offer it, run it if accepted, report results
