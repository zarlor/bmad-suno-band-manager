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
- **Files are deleted** (WIP files, old voice files, obsolete references) — stale entries pointing to deleted files need cleanup in companion files tables, sidecar index, chronology, and any docs that listed them

## Authoritative Sources

| Data | Authoritative Source | May Be Referenced In |
|------|---------------------|---------------------|
| Song title | Songbook entry (`docs/songbook/{band}/{song}.md`) | Per-band playlist YAML, playlist ordering doc, voice context, sidecar index/chronology, WIP files, companion files |
| Song status (WIP/published) | Songbook entry | Voice context (WIP sections, catalog), sidecar index, per-band playlist YAML, WIP files that should be deleted |
| Playlist order & track numbers | **Per-band playlist YAML** (`docs/{band-slug}-playlist.yaml`) — authoritative as of v1.7.2 | Playlist ordering doc (derived narrative companion), voice context (catalog section), songbook placement notes, sidecar position references, script-generated companion at `docs/{band-slug}-playlist-sequencing.md` |
| Band profile (genre, vocal, name) | Band profile YAML (`docs/band-profiles/*.yaml`) | Voice context, songbook entries referencing profile values, sidecar index. **Note:** the band profile YAML must NOT carry a `playlist:` block as of v1.7.2 — playlist data lives in the per-band playlist YAML to avoid drift. |
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
- `docs/{band-slug}-playlist.yaml` — **canonical per-band playlist YAML files** (one per band; iterate all `docs/*-playlist.yaml` matches)
- `docs/*-playlist-ordering.md` — playlist ordering docs (derived narrative companions; not authoritative)
- `docs/*-playlist-sequencing.md` — script-generated per-band sequencing companions (auto-refreshed; do not hand-edit between AUTOGEN markers)
- `docs/voice-context-*.md` — voice/context files (including the Companion Files table)
- `docs/wip-*.md` — WIP files (may need deletion if song published)
- Any companion files listed in the voice file's Companion Files table — discover dynamically from that table rather than guessing patterns
- `{project-root}/_bmad/_memory/band-manager-sidecar/` — index.md, chronology.md, patterns.md

Use exact string matching first, then check for variations:
- Title with/without subtitle
- Different casing
- Partial matches (e.g., just the first word of a multi-word title)
- Working title vs. final title

**Also check for stale FILE REFERENCES:** Any table, list, or inline mention of a file path should have that file verified to exist. Broken references (pointing to deleted files) are stale even if the content hasn't "changed" — the referent no longer exists. Common places for stale file refs:
- Voice context Companion Files table (the highest-priority check — this is the most likely source of breakage)
- Sidecar index Key Files section
- Songbook entries referencing WIP files in their source notes
- Chronology entries mentioning files that were later deleted

**Also check for stale COUNTS:** Numbers in descriptions (e.g., "34 tracks", "577 lines", "98 pages") may have been accurate when written but drift as content changes. Flag any count-bearing descriptions for verification when the underlying content has changed.

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
3. For WIP files of published songs: **apply the COMPLETED WIP convention** (see below) — preserve the file as historical record, do NOT delete
4. Write the updated file
5. Report what was changed: "Updated 3 files, marked 1 WIP file COMPLETED"

### Special Cases

**Playlist reordering:** When track numbers change, update ALL track number references in the voice context catalog section. This is a bulk update — present the full before/after for the catalog section rather than individual line changes.

**WIP → Published:** Check for `docs/wip-*` files that reference the published song. **Apply the COMPLETED WIP convention (below)** to mark them resolved — do NOT delete them. The fragments are the historical record of the brainstorming that led to the song. The marker ensures they don't appear as active work on future sessions while preserving their content for reference.

**Band profile rename:** This is the widest-impact change — every songbook entry references the profile by name in frontmatter. Surface the scope before proceeding.

## The COMPLETED WIP convention

When a song is published from a WIP fragments file, mark the file with a standard COMPLETED block at the top — immediately after the title heading, before the original content. This preserves the brainstorming record while signaling to future sessions (and future machines after a portable sync) that the file is not active work. Do NOT delete the file — fragments are creative history (brainstorming that didn't make the song, direction changes, cut images, working-title evolution).

### The exact marker format

Apply this block at the top of the WIP file, immediately after the `#` title heading and any `## WIP —` date line, separated by a `---` horizontal rule above and below:

```markdown
# <Original WIP title>
## WIP — <original dates>

---

## STATUS: COMPLETED as "<Published Song Title>" — published <YYYY-MM-DD>

This fragments file is preserved as historical record. The song was completed
as **<Published Song Title>** on <YYYY-MM-DD> <brief context: what session,
what band, what musical direction>. See the songbook entry at
`docs/songbook/<band>/<song-slug>.md` for the finished form, style prompt,
exclude styles, settings, and the full generation log.

**This WIP file is NOT active work — do not list it in pending/parked work.**

---

<original fragments content continues here, unchanged>
```

**Key elements** (all required):
1. A `## STATUS: COMPLETED as "<title>" — published <date>` heading — this is the machine-readable marker that pending/parked listings should grep for
2. One paragraph of context pointing to the songbook entry (absolute path within the repo)
3. The explicit "NOT active work — do not list in pending/parked work" line — this is the instruction to future Mac sessions
4. A `---` horizontal rule below to separate the marker block from the original fragments

### Listing discipline (sidecar index maintenance)

When building or updating the "Pending / Parked Work" section of the sidecar `index.md`, Mac MUST:

1. **Scan every `docs/wip-*.md` file** for the `## STATUS: COMPLETED` marker before listing it
2. **Skip files with the marker** — they are resolved, not pending
3. **When including resolved WIPs in the index for historical reference**, put them under a separate "Resolved WIP fragments (historical record only — not active work)" subsection, clearly delineated from active pending/parked work, with a pointer to the songbook entry they became

The sidecar index's Pending / Parked Work section is the primary place a future Mac session looks to decide what to work on next. A stale WIP listed there will be picked up as a candidate. The scan-before-list rule prevents this.

### Applying the marker to existing unmarked WIPs

If you encounter a WIP file without a COMPLETED marker but you can confirm the song is published (by finding the songbook entry), apply the marker in context — surface it as a cleanup: "I noticed `docs/wip-X.md` is for a song that's already published as Y. Marking it COMPLETED so it doesn't get picked up next session." Then apply the block and confirm.

Do NOT guess — if you're not sure the song is published, ask. The marker is a positive assertion that the WIP resolved into a specific published song; applying it to a still-active WIP would lose work.

## Scope Boundaries

- Only search within Mac's access boundaries (docs/ and sidecar memory)
- Never modify files outside the known document locations
- If a reference is ambiguous (partial match, could refer to something else), ask rather than assume
- Keep it lightweight — this is a quick consistency check, not a full audit
- Reconciliation is a SERVICE, not a gate — never block the user's workflow to force reconciliation. Offer it, run it if accepted, report results
