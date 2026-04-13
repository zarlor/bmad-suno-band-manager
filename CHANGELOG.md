# Changelog

All notable changes to the Suno Band Manager module are documented here.

---

## [1.6.5] - 2026-04-13

### Sidecar Drift Protection

A structural release that eliminates a class of bug where the Mac sidecar `index.md` could silently drift out of sync with the authoritative songbook. The drift was discovered in a real session: `index.md` still listed a published song as WIP and omitted another published track entirely — yet the catalog status section had been updated in the same save cycle. That partial-update pattern motivated the fix.

### Root Cause

`index.md` mixed two categories of facts and treated them identically:

1. **Derivable facts** — catalog count, which tracks are published, publish dates, catalog roster. These have an authoritative source (songbook frontmatter + body Status markers + playlist YAMLs). They should be machine-derived.
2. **Narrative facts** — current work focus, pending threads, session history, next steps. These live only in the narrator's head. They need to be hand-written.

Both were hand-written. When the save-memory workflow ran, Mac read the conversation and narratively updated the sections he remembered touching. Sections he didn't touch silently kept stale values. Nothing compared the written index against the ground truth, so drift accumulated invisibly. Similar drift was independently found in a songbook file's frontmatter `notes:` block and body `**Status:**` marker (both still said WIP for a song that had been published two days earlier).

### Added

- **`scripts/validate-sidecar.py`** — read-only validator that scans `docs/songbook/**/*.md`, `docs/band-profiles/*.yaml`, `docs/*-playlist.yaml`, and `_bmad/_memory/band-manager-sidecar/index.md`, then reports drift as structured findings (JSON or text output). Checks:
  - Songbook internal consistency — frontmatter `status`/`date` vs. body `**Status:**` marker
  - Audio file existence for published songs
  - Sidecar Recently Published list vs. songbook ground truth
  - Sidecar Catalog Status counts vs. actual songbook counts
  - Playlist YAML track count vs. songbook count

  Exit 0 on clean, 1 on errors (for CI-friendliness). Warnings (pre-existing content gaps like missing body markers on older songs) do not fail the run. Standalone CLI with `--format json` and `--warn-only` flags.

- **`scripts/regenerate-index-sections.py`** — writer-side companion to the validator. Reads songbook + playlist ground truth, derives the Recently Published and Catalog Status sections, rewrites them in-place in `index.md` between HTML comment markers:

  ```markdown
  <!-- derived:recently-published:start -->
  ...auto-generated content...
  <!-- derived:recently-published:end -->
  ```

  Narrative sections (Current Work, Pending / Parked Work, Session History, etc.) are preserved unchanged — only the derivable sections are rewritten. `--dry-run` prints without writing.

### Changed

- **`scripts/pack-portable.sh` and `pack-portable.ps1`** — run `validate-sidecar.py` before packing. A non-zero exit from the validator blocks the pack, preventing stale sidecar state from propagating to other machines via the sync archive. Warnings do not block. Bypass via `BMAD_SKIP_VALIDATE=1` (or `$env:BMAD_SKIP_VALIDATE=1` on PowerShell) for emergency syncs. Missing validator script or Python interpreter falls through gracefully with a note so older installs keep working. Cross-platform parity: both shell and PowerShell scripts implement the same gate with the same bypass semantics.

- **`src/skills/suno-agent-band-manager/references/save-memory.md`** — Step 4 now updates only narrative sections of `index.md`; Step 4a invokes `regenerate-index-sections.py` to rewrite derivable sections; Step 4b invokes `validate-sidecar.py` to confirm cleanliness before finalizing the save. Step 7 reconciliation narrowed to cross-file drift since sidecar-level drift is covered automatically by 4b.

### Fixed

- **`docs/songbook/lennys-voice/from-now-until.md` — frontmatter/body drift cleanup.** Frontmatter said `status: published` with `date: 2026-04-11`, but the `notes:` block and body `**Status:**` marker both still described WIP state ("Plan: re-test with Lenny - Rock clone when credits return"). The song had actually been published 2026-04-12 after Rock A/B testing — the Lenny-Soft wild card variant with "driving rock band weight" took the published slot. All three locations now agree. This drift is what motivated the release.

### Migration (one-time, per project)

Existing projects need to add the derived-section markers to `index.md` on first upgrade:

```markdown
## Recently Published

<!-- derived:recently-published:start -->

...existing content...

<!-- derived:recently-published:end -->

## Catalog Status

<!-- derived:catalog-status:start -->

...existing content...

<!-- derived:catalog-status:end -->
```

The regenerator reports clearly if markers are missing and exits without modifying the file, so a missed migration can't corrupt the index.

### Impact

| Previously | After v1.6.5 |
|---|---|
| `index.md` Recently Published and Catalog Status hand-written → could silently skip updates | Regenerated from songbook ground truth every save → can't drift |
| No mechanism to detect sidecar inconsistency | Validator reports drift with exit code + JSON for CI |
| Stale sidecar could propagate to other machines via sync | Pre-sync gate blocks packs that fail validation |
| Songbook internal drift (frontmatter vs. body marker) invisible | Validator surfaces it as structured findings |
| Windows and Linux/macOS used independent sync paths | Both platforms run the validator identically |

### Verification

- **Validator on current state:** 0 errors, 14 warnings — all warnings are pre-existing content gaps (older Solitary Fire songbook entries missing body `**Status:**` markers, and a 2-track count mismatch between the SF playlist YAML and the SF songbook directory). These are legitimate drift findings; the validator correctly flags them as warnings rather than blocking errors since they predate v1.6.5.
- **Regenerator dry-run:** produces clean Recently Published list (7 most recent published songs) and Catalog Status (per-band counts + playlist integration) from songbook frontmatter alone.
- **Pre-sync gate on Linux:** packs correctly when validator passes; `BMAD_SKIP_VALIDATE=1` bypass works.
- **Cross-platform parity:** bash and PowerShell implementations of the pre-sync gate inspected side-by-side for identical exit semantics and bypass behavior.

### Version Bumps

- `package.json`: 1.6.4 → 1.6.5
- `src/skills/suno-setup/assets/module.yaml`: 1.6.4 → 1.6.5
- `.claude-plugin/marketplace.json`: 1.6.4 → 1.6.5
- `INSTALLATION.md`: 1.6.4 → 1.6.5

### Additionally (reference doc refinements)

Two small in-flight documentation refinements are also folded into this release since they were already staged:

- **`SUNO-REFERENCE.md` — Credit model clarifications.** Replaces the older "generate 3-5 versions" framing with budgeting in **Creates** (10 credits, 2 songs per press) to match how users actually think about Suno spending. Adds an explicit credit-cost row to the tier comparison table, a dedicated "Credit model" paragraph explaining that 50 credits/day = 5 Creates = 10 songs to evaluate, and a note on the 50 bonus credits/day that refresh on all tiers. Updates the Common Pitfalls table entries to reference Creates rather than individual generations. No behavior change — it's a framing update that brings the reference in line with how Pro users budget sessions.

- **`persona.md` — Adds "Dawlin'" to the NOLA vocabulary list.** Captures the distinctive Yat/Marigny/Bywater/9th Ward pronunciation (the `aw` diphthong) as separate from generic Southern "darlin'" so Mac uses the correct form.

### Scope Note

This release adds **two new scripts** (`validate-sidecar.py`, `regenerate-index-sections.py`) and **modifies several existing module files** (`pack-portable.sh`, `pack-portable.ps1`, `save-memory.md`, plus the two reference doc refinements above). User data (`docs/`, `_bmad/`) is not part of the module and remains untouched by the module upgrade. One-time project migration (adding derived-section markers to `index.md`) is the only user-facing action required.

---

## [1.6.4] - 2026-04-11

### pack-portable.sh Bug Fixes (Linux/macOS)

A bugfix release for the bash portable-sync packer. Two distinct bugs caused users to silently lose files from their sync archives. PowerShell users were unaffected by the core bugs (the PS1 implementation was already correct) but get a small parity consistency fix.

### Fixed

- **`pack-portable.sh` manifest parser silently ignored every pattern.** The sed extraction pulled manifest lines with their original leading indentation intact (`  - "docs/..."` with 2-space YAML indent), but the shell parameter expansion `${line#- }` only strips `- ` from the very start of a string — it does not handle leading whitespace. Result: every pattern in every manifest became garbage text, every glob matched zero files, and `pack-portable.sh` returned `{"status": "empty", "message": "No portable files found to pack."}` with no diagnostic. Users following `portable-manifest.example.yaml` (which demonstrates standard 2-space YAML indentation) would hit this immediately on their first manifest run.

  **Fix:** Replaced the shell-expansion parser with a robust sed one-liner that strips leading whitespace + `- `, inline `# ...` comments, and surrounding quotes (both `"` and `'`) in a single pass. Manifests with standard YAML indentation, inline comments, and either quote style now parse correctly.

- **`pack-portable.sh` default band-profiles pattern silently excluded top-level files.** The default pattern `docs/band-profiles/**/*.yaml` used `find -path` for matching. In `find -path`, `*` matches any sequence including `/` (there is no special `**` globstar), so the pattern was functionally equivalent to `docs/band-profiles/*/*.yaml` — it required a literal `/` between `band-profiles/` and the `*.yaml` tail, which meant files had to be in a SUBDIRECTORY of `band-profiles/`. Every band profile following the standard convention (files placed directly in `docs/band-profiles/`, like `solitary-fire.yaml`) was silently excluded from the default pack.

  **Fix:** Refactored `add_glob` in the bash script to match the PowerShell version's recursive `**` handling — when a pattern contains `**`, the script splits at the first `**`, uses the prefix as a base directory and the suffix as a filename filter, and calls `find -name -type f` (which naturally includes the starting directory). This matches standard shell globstar semantics and the PowerShell implementation, producing identical cross-platform behavior for patterns like `docs/band-profiles/**/*.yaml`, `docs/songbook/**/*.md`, and `docs/inspiration/**/*.txt`. Non-`**` patterns continue to use `find -path` unchanged.

### Changed (parity / consistency)

- **`pack-portable.ps1` manifest parser now handles single-quoted YAML patterns.** The previous regex `^\s*-\s*"?([^"#]+?)"?\s*(#.*)?$` excluded only `"` and `#` from the capture group, so manifest entries using single quotes (`  - 'docs/file.md'`) would capture the single quotes as part of the pattern and fail to match files. The parser is now a two-step approach (match the payload between `- ` and optional `#`, then `.Trim().Trim('"').Trim("'")`) that handles whitespace, inline comments, and both quote styles identically to the bash implementation. This is a minor consistency fix — the PS1 implementation was already correct for the common double-quoted YAML case used in `portable-manifest.example.yaml`.

### Impact

- **Linux/macOS users** using `pack-portable.sh` WITH a manifest — were hitting silent empty-pack failures. **Fixed.** Existing manifests that follow `portable-manifest.example.yaml` formatting now work correctly without modification.
- **Linux/macOS users** using `pack-portable.sh` WITHOUT a manifest (defaults only) — were silently losing their top-level band profiles from the pack. **Fixed.** Defaults now capture both top-level and nested band profiles via `docs/band-profiles/**/*.yaml` with the new recursive handler.
- **Windows users** using `pack-portable.ps1` — were not hitting either core bug (the PS1 implementation used separate correct logic paths for both). **Single-quote edge case in the manifest parser fixed** as a consistency improvement. Existing double-quoted manifests are unaffected.
- **`portable-manifest.example.yaml`** — no changes needed. The existing example is correct and now works on both platforms as advertised.

### Verification

- **With manifest (Linux):** 54 files packed from a real project manifest including band profiles, companion docs, playlist artifacts, and session findings. All customized inclusions present.
- **Without manifest, defaults only (Linux):** 42 files packed, including both top-level band profiles (`lennys-voice.yaml` and `solitary-fire.yaml`). Before the fix, band profiles were silently excluded.
- **PowerShell:** regex change validated by inspection for single-quote handling. No behavior change for double-quoted patterns.

### Version Bumps

- `package.json`: 1.6.3 → 1.6.4
- `src/skills/suno-setup/assets/module.yaml`: 1.6.3 → 1.6.4
- `.claude-plugin/marketplace.json`: 1.6.3 → 1.6.4
- `INSTALLATION.md`: 1.6.3 → 1.6.4

### Scope Note

This is a **bash and PowerShell script-only release** — no reference doc changes, no schema changes, no new files created. Safe drop-in replacement for v1.6.3. Existing `portable-manifest.yaml` files do not need to be updated; they will start working correctly on Linux/macOS with no changes.

---

## [1.6.3] - 2026-04-10

### v5.5 Voice Gravity Principle + Production Observations

An additive findings release capturing new knowledge discovered during a live Voice track production session (song: *Observation*, an adult alternative / heartland southern rock track using a v5.5 Voice clone trained on soft rock / folk material). No bug fixes, no API changes — three reference files gain new production-validated guidance.

### Added

- **`suno-style-prompt-builder/references/model-prompt-strategies.md`** — Major expansion of the "Getting the best voice clone" section and new subsection "The v5.5 Voice Gravity Principle" with six practical rules and a validated case study. Key additions:
  - **Voice Gravity Principle:** v5.5 Voice clones carry trained genre gravity and pull generations toward their training baseline on their own. When a song's target genre differs from the Voice's trained direction, the style prompt must actively fight against that gravity rather than describing the target.
  - **Six practical rules:** (1) drop descriptors the Voice already delivers, (2) load descriptors pulling against the Voice's direction, (3) Style Influence 65+ for Voice-genre mismatch, (4) never specify Vocal Gender when a Voice is active, (5) Voice-aware exclusion strategy (drop harsh-vocal protections when the clean Voice can't produce them), (6) Audio Influence floor caution for non-Professional Voices.
  - **Consistency-vs-variety resolution:** Reconciles the apparent tension between JG BeatsLab's "consistency within a clip wins" and HookGenius's "three clips across moods helps" — both are correct at different scales. Consistency within a single sample, variety across multiple Voice profiles.
  - **Re-recording guidance:** 20-30 sec optimal length per clip, Professional skill level mandatory (not cosmetic — cannot be changed after recording), preserve vocal quirks rather than smoothing them, sibilance mic-technique solution (off-axis positioning 15-30°).
  - **Validated case study:** Documents the specific iteration path from a failed first attempt (folk-descriptors-duplicating-Voice + Audio Influence 20% + keyboards + unhurried tempo) to the working solution (heartland southern rock + overdriven guitar + Audio Influence 55% + keyboards killed + rock urgency).

- **`suno-style-prompt-builder/references/model-prompt-strategies.md`** — Three new entries in the Genre Term Behavior Table:
  - **`heartland rock`** — safe rock term for Voice tracks (no harsh vocal trigger)
  - **`southern rock`** — safe vocal-wise; may pull slide/steel guitar (exclude if unwanted)
  - **`heartland southern rock`** — validated combined term for Voice tracks needing rock presence without metal pull

- **`suno-lyric-transformer/references/metatag-reference.md`** — New subsection "Isolated parentheticals as performed speech" documenting production observation that parentheticals placed on their own indented lines (not attached as `word(echo)`) are often delivered as **spoken interjections** rather than sung backing vocals. Works with v5.5 Voices despite the docs cautioning against spoken-word use — brief interjections are a different case from sustained `[Spoken Word]` sections.

- **`suno-band-profile-manager/references/profile-schema.md`** — Expanded "Voices (v5.5)" Notes for Downstream Skills bullet with the six Voice Gravity Principle rules (profile-schema form) and a new "Multi-profile Voice strategy" note explaining how profiles can reference multiple Voice IDs for projects with several Voice recordings (e.g., "Narrative Rock," "Ballad Intimate," "Speak-Sing Confessional"), with consistency-within-sample + variety-across-samples as the guiding principle.

### Sources

- [JG BeatsLab — Suno v5.5 Voices Tested (Day One Findings)](https://www.jgbeatslab.com/ai-music-lab-blog/suno-v5-5-voices-tested)
- [HookGenius — Suno v5.5 Guide: Voices, Custom Models & My Taste](https://hookgenius.app/learn/suno-v5-5-guide/)
- [Suno Knowledge Base — Use Your Voice in Suno](https://help.suno.com/en/articles/11362369)
- [Suno — How to Use Suno AI Voice Cloning (2026 Guide)](https://suno.com/hub/ai-voice-cloning)
- Production observation from *Observation* song iteration (2026-04-10) — validated fix path documented as case study

### Version Bumps

- `package.json`: 1.6.2 → 1.6.3
- `src/skills/suno-setup/assets/module.yaml`: 1.6.2 → 1.6.3
- `.claude-plugin/marketplace.json`: 1.6.2 → 1.6.3
- `INSTALLATION.md`: 1.6.2 → 1.6.3

### Scope Note

This is a **reference-file-only release** — no script behavior changes, no new files created, no schema changes. Purely additive documentation of production-validated Voice-track findings. Safe to pull as a drop-in replacement for v1.6.2 with no migration needed.

---

## [1.6.2] - 2026-04-10

### Reference File Consolidation & Broken Link Cleanup

A small architectural cleanup that addresses the v1.6.1 known follow-up. The marketplace PR ([bmad-code-org/bmad-plugins-marketplace#7](https://github.com/bmad-code-org/bmad-plugins-marketplace/pull/7)) is being updated to point at this release.

### Removed

- **Three root-level reference duplicates** — `SUNO-REFERENCE.md`, `USAGE.md`, and `STUDIO-EDITOR-REFERENCE.md` previously existed both at the repo root and inside `src/skills/suno-agent-band-manager/references/`. They had silently drifted out of sync between releases (the v1.6.0 wording fix only landed in some copies, requiring the v1.6.1 sync). The `src/skills/suno-agent-band-manager/references/` versions are now the **only** canonical copies, eliminating the drift class entirely.

### Updated

- **`README.md`** — Markdown links to the reference docs now point at the canonical `src/skills/suno-agent-band-manager/references/...` paths. Added `USAGE.md` to the references directory tree (it was already there on disk; the diagram just hadn't listed it).
- **`INSTALLATION.md`** — Aider command updated to read the canonical paths:
  ```bash
  aider \
    --read src/skills/suno-agent-band-manager/references/SUNO-REFERENCE.md \
    --read src/skills/suno-agent-band-manager/references/USAGE.md
  ```
- **`CLAUDE.md` / `GEMINI.md` / `AGENTS.md`** — cross-reference list updated to use the canonical USAGE.md path.

### Fixed (pre-existing broken links discovered during the audit)

- **`src/skills/suno-feedback-elicitor/references/suno-parameter-map.md`** — `[STUDIO-EDITOR-REFERENCE.md](../../STUDIO-EDITOR-REFERENCE.md)` resolved to `src/skills/STUDIO-EDITOR-REFERENCE.md`, which has never existed at that path. Now points at `../../suno-agent-band-manager/references/STUDIO-EDITOR-REFERENCE.md`.
- **`src/skills/suno-band-profile-manager/references/tier-features.md`** — Same broken pattern, same fix.

These had been broken since the references/ folder layout, but were never noticed because nothing automatic exercised the markdown links.

### Marketplace Submission

The community module PR will be rebased to point at the v1.6.2 commit SHA so reviewers see the consolidated version with no drift risk.

---

## [1.6.1] - 2026-04-10

### Cross-Platform Hardening & Stale Reference Cleanup

A follow-up release to v1.6.0 closing two open issues that surfaced after the marketplace submission. The marketplace PR ([bmad-code-org/bmad-plugins-marketplace#7](https://github.com/bmad-code-org/bmad-plugins-marketplace/pull/7)) is being updated to point at this release.

### Fixes

- **Fixes #21** — **Gemini CLI: skills not discoverable and activation protocol not followed.** Two layered fixes:
  - **`link-skills.sh` and `link-skills.ps1`** now create symlinks in `.gemini/skills/` in addition to `.claude/skills/` and `.agents/skills/`. Gemini CLI's glob does not always follow symlinks under `.agents/skills/`, so a native scan path is required for reliable skill discovery.
  - **New standing-order files at the repo root** — `CLAUDE.md`, `GEMINI.md`, `AGENTS.md` (identical content) — make the skill activation discipline explicit and tool-agnostic. They mandate: running pre-activate scripts, reading persona/creed/capabilities/activation/memory-system reference files, presenting the dynamic menu from script output (not improvising from `SKILL.md` text), loading voice context before greeting, and the Suno Pipeline Rule. Previously, this discipline lived only inside individual `SKILL.md` files in a declarative style that Claude Code's harness compensated for but Gemini CLI / Codex CLI / OpenCode interpret more literally. The standing-order files are auto-loaded by each respective LLM CLI on every session.
  - The deeper imperative-style refactor of individual `SKILL.md` files (a recommendation in the issue) is intentionally deferred to a future release — the standing-order approach addresses the symptom directly with much less surface area to maintain.

- **Fixes #22** — **Inconsistent character limit guidance and stale research findings across module.** Comprehensive sweep of remaining stale references after the v1.6.0 wording fixes:
  - **Synced three duplicate file pairs** — `SUNO-REFERENCE.md`, `USAGE.md`, and `STUDIO-EDITOR-REFERENCE.md` exist as both top-level files (read by Aider via `--read`) and inside `src/skills/suno-agent-band-manager/references/`. They had drifted out of sync, causing the v1.6.0 wording fix to land in only one copy of each pair. All three pairs are now identical and reflect the canonical v5.5 critical-zone wording.
  - **Updated three stale "4-7 descriptors" references** to "5-8 descriptors" — the v1.4.1 HookGenius update changed the sweet spot but didn't propagate to `src/skills/suno-style-prompt-builder/SKILL.md`, `src/skills/suno-style-prompt-builder/references/README.md`, or `src/skills/suno-agent-band-manager/references/README.md`.
  - The two specific complaints in issue #22 about `suno-parameter-map.md` lines 372/375 and `SKILL.md` lines 116/162 were verified as **false alarms** — those lines are correctly scoped to v4 Pro (which DOES have a 200-char hard limit) and the Exclude Styles input field (separate constraint), respectively. No edits needed.

### Known Follow-Ups

- **Duplicate file pairs** between root and `src/skills/suno-agent-band-manager/references/` (`SUNO-REFERENCE.md`, `USAGE.md`, `STUDIO-EDITOR-REFERENCE.md`) are kept in sync manually as of v1.6.1. A future release should consolidate to a single canonical location and update Aider documentation accordingly.

### Marketplace Submission

The community module PR ([bmad-code-org/bmad-plugins-marketplace#7](https://github.com/bmad-code-org/bmad-plugins-marketplace/pull/7)) will be rebased to point at the v1.6.1 commit SHA so reviewers see the cross-platform-hardened version.

---

## [1.6.0] - 2026-04-09

### BMad Plugins Marketplace Submission

This release packages the module for submission to the [BMad Plugins Marketplace](https://github.com/bmad-code-org/bmad-plugins-marketplace) as a community module under `design-and-creative` / `audio`. Version `1.6.0` consolidates the unreleased v1.5.0/v1.5.1/v1.5.2 work plus marketplace-prep cleanup.

### Marketplace Packaging

- **Added `.claude-plugin/marketplace.json`** at repo root, registering all six skills (suno-agent-band-manager, suno-band-profile-manager, suno-style-prompt-builder, suno-lyric-transformer, suno-feedback-elicitor, suno-setup) under the BMad Builder distribution format.
- **Module quality validation pass** — Re-ran `bmad-module-builder` Validate Module against `src/skills`. All structural checks pass; CSV registration audited against actual skill behavior.

### Privacy & Repo Hygiene

- **Expanded `.gitignore`** — `docs/`, `.claude/`, `.gemini/`, `.agents/`, `_bmad/`, `_bmad-output/`, and `portable-manifest.yaml` are now properly excluded so personal user content (voice files, songbook, band profiles, audio, WIP files) stays out of the repo.
- **Removed `docs/solitary-fire-playlist.yaml`** from tracked files. Personal album content should never have been tracked.
- **Genericized personal references** in source: `analyze-audio.py` docstring, `memory-system.md` example name, `reconcile.md` companion-file pattern guidance now uses dynamic discovery via the voice file's Companion Files table rather than hardcoded family-history wildcards.

### Cross-Platform Support

- **PowerShell counterparts** for all three shell utilities:
  - `link-skills.ps1` — Windows symlink installer (uses Developer Mode or elevation)
  - `scripts/pack-portable.ps1` — Windows portable archive creator
  - `scripts/unpack-portable.ps1` — Windows portable archive extractor
- **`INSTALLATION.md` Windows guidance** — bash and PowerShell command pairs for Standalone, BMad Method, and Update flows. Updated Windows symlink troubleshooting note.

### Portable Sync Improvements

- **`pack-portable.sh` defaults trimmed** to documented module conventions only (`docs/voice-context-*.md`, `docs/songbook/**/*.md`, `docs/band-profiles/**/*.yaml`, `docs/wip-*.md`). User-specific patterns moved to manifest examples.
- **New `portable-manifest.example.yaml`** at repo root — copy to `portable-manifest.yaml` and customize. Clearly documents the manifest format with commented examples for companion files, playlist artifacts, session findings, and other custom patterns.
- **New "Multi-Machine Sync" section** in `INSTALLATION.md` explaining the pack/unpack workflow and manifest customization.

### CSV Registration Fixes

- **`suno-feedback-elicitor`** — cleared the `before` column. Previously it duplicated the `after` column (`suno-style-prompt-builder:build-style-prompt,suno-lyric-transformer:transform-lyrics`), creating a logical cycle. Feedback elicitor runs *after* the builders; the iteration loop back during refinement is implicit in the refine flow, not a CSV ordering relationship.
- **`suno-lyric-transformer`** — removed `analyze` from the Transform Lyrics (TL) headless args list. The dedicated Analyze Lyrics (AL) row is the canonical analyze entry; TL now cleanly maps to `transform|refine`.
- **`suno-style-prompt-builder`** — enriched description to surface wild card variants, exclusion prompts, and creativity modes (previously a generic "model-aware Suno style prompts" line that hid these capabilities).

### Version Drift Resolved

Three different version values were floating across the module before this release:

- `module.yaml` was at `1.4.0`
- `package.json` was at `1.4.1`
- Latest git tag was `v1.5.2`

All four locations now sync to `1.6.0`: `module.yaml`, `package.json`, `.claude-plugin/marketplace.json`, and the `INSTALLATION.md` config example.

### Includes Unreleased Work from v1.5.0 / v1.5.1 / v1.5.2

The intermediate v1.5.x tags shipped without changelog entries. Notable work folded into this release:

- **Pipeline guard hook (v1.5.1)** — Stop hook script `scripts/pipeline-guard.py` enforces mandatory skill invocation; blocks responses containing a Suno package when `suno-style-prompt-builder` and `suno-lyric-transformer` weren't run during the session.
- **State reconciliation (v1.5.2)** — `reconcile.md` workflow for detecting and fixing stale references across docs and sidecar files when authoritative data changes.
- **Cross-platform pipeline guard setup (v1.5.2)** — `suno-setup` offers to configure the Stop hook and AGENTS.md standing order automatically.
- **NOLA voice / section tag guidance / cross-skill references (v1.5.0)** — Reference doc updates for vocal direction patterns and metatag conventions.
- **Dual-voice limitation documentation** — Suno v5/v5.5 cannot reliably produce two distinct same-gender voices; documented workarounds (Persona OFF + Replace Section, gender contrast, nu-metal/metalcore framing).
- **Bidirectional companion files audit** — Stale file reference detection in `reconcile.md`.
- **Pipeline guard transcript parsing fix** — Now correctly parses nested `tool_use` entries.
- **Package assembly headless mode** — Parallel execution and suppression of intermediate output when running the full pipeline non-interactively.
- **Refinement presentation cleanup** — Show only what changed in refinement output, not the full package.

---

## [1.4.1] - 2026-04-06

### Suno v5.5 Community Research Update

Comprehensive reference documentation update integrating independent community testing results from JG BeatsLab, HookGenius (1000+ prompt analysis), AudioNewsRoom, JackRighteous, BlakeCrosley, GenxNotes, and others. All findings sourced and linked for independent verification.

### Corrections

- **v5.5 model codename** — Fixed from "chirp-crow" (that's v5) to the correct "chirp-fenix"
- **Voices Audio Influence ranges** — Corrected based on JG BeatsLab testing. Real sweet spot is 40-60%, not 55-70%. Quality degrades above 70%; at 85% resemblance only reaches ~70% with increasing artifacts. Updated across SUNO-REFERENCE, model-prompt-strategies, and suno-parameter-map.
- **Style Personas are NOT gone** — Clarified that Personas coexist with Voices in the v5.5 Voices tab. The button changed but both features remain available.
- **Descriptor count sweet spot** — Updated from "4-7" to "5-8" based on HookGenius 1000+ prompt analysis across all reference files and quick-reference tables.

### New Findings — v5.5 Features

- **Voices Skill Level dropdown** — Beginner/Intermediate/Advanced/Professional setting is NOT cosmetic; actively reshapes model interpretation. Always use Professional for most stable results.
- **Voices limitations** — Directional influence, not true reproduction. Not suitable for spoken word/narration (drifts toward singing). Realistic for demos and pre-production.
- **My Taste magic wand / Style Augmentation** — Documented the wand icon in Create form that auto-generates personalized style prompts. Manual prompts always override. Can be viewed/edited/disabled from avatar menu.
- **Custom Model training best practices** — WAV at 44.1kHz preferred, 8-12 consistent tracks sweet spot, auto-normalization pipeline (RMS leveling, DC offset removal, spectral masking, onset detection, key/scale estimation), overfitting mitigation guidance.
- **Custom Model prompt strategy shift** — With Custom Models, priority changes from genre-first to mood/production-first. Formula: MOOD + PRODUCTION TEXTURE + ENERGY/TEMPO + INSTRUMENTS + VOCAL DIRECTION.
- **Custom Model consent/privacy** — Grants Suno permission to use data for global model training (not optional, not private).

### New Findings — Style Prompt Strategies

- **"Cinematic" as universal modifier** — Consistently elevates production quality across every tested genre.
- **Production tags most underused** — Adding even one meaningfully improves distinctiveness.
- **Conflicting tags produce bland compromise** — Opposing descriptors cancel out, not creative tension.
- **Callback phrasing during Replace/Extend** — "Continue same chorus energy" anchors consistency.
- **Style Influence above ~80 plateaus** — Rarely improves accuracy, can reduce vocal phrasing variation.

### New Findings — Extend Drift Solutions

- **Weirdness strongest during Extend/Bridge** — Primary cause of style drift. Keep conservative during Extend.
- **Anchor note restating** — Restate genre, mood, key, instrument palette with each extension.
- **Forbidden element phrasing** — "No new hooks/drums/riffs" more effective than positive instruction alone.
- **2-3 extension chain limit** — Quality degrades beyond that. Cover feature re-synthesizes to clean signal path.
- **Persona instability with Extend** — Personas historically unreliable during Extend operations.
- **Extend Anti-Drift Toolkit** — 7-technique ranked guide added to suno-parameter-map.
- **Genre-specific outro templates** — Gospel, Rock, Lo-fi, EDM, Reggae ending patterns.

### New Findings — Metatags

- **Asterisk sound effect syntax** — `*rainfall*`, `*vinyl crackle*` etc. confirmed working as inline sound effects. Exception to "no asterisks" rule.
- **New Effect tags** — `[Effect: Bitcrusher]`, `[Effect: Autopan]`, `[Effect: Sidechain]`
- **`[Callback: ...]` upgraded** — HIGH reliability for Extend/Replace workflows (community-validated). Experimental for standard generation.
- **Ending tag variants** — `[Soft End]`, `[Dramatic End]`, `[Instrumental End]`, `[Slow Fade Out]`, `[Fast Fade Out]`, `[Instrumental Fade Out]`, `[Cinematic Fade Out]`
- **Noodling-prevention combo** — `[Outro] descriptive text [End]` stacking more effective than either alone.
- **Accelerando/Ritardando grid-loss warning** — Can lose rhythmic grid for remainder of track. BPM tag as recalibration anchor after disruption.
- **Three-layer vocal specification** — Character + Delivery + Effects for maximum vocal control.
- **Vocal delivery reliability tiers** — HIGH/MEDIUM/LOW classification from HookGenius 300+ tag testing.
- **Non-functional tags documented** — `[Bilingual]`, `[Spanglish]`, `[Live Version]`, `[Mono]`, `[Wide Stereo]`, `[Clean Lyrics]`/`[Explicit]` confirmed ineffective.
- **Falsetto confirmed LOW reliability** — Style prompt phrasing more effective than metatag.

### New Findings — Studio & Editing

- **Replace Section sweet spot 15-20 seconds** — Under 5 = disjointed, over 30 = model loses thread.
- **Heal Edits technique** — Apply on the following section after Replace to blend timbre shifts.
- **Remaster is full regeneration** — Not a filter. Instrumentals benefit more than vocals. "Improved fidelity with reduced soul." One pass usually sufficient.
- **Remove FX boosts loudness up to 5 LUFS** — Check levels after applying.
- **EQ for AI shimmer** — Roll off ultra-highs on stems with generation artifacts.
- **Genre-specific Warp Marker quantize** — EDM tight, Trap medium, Afrobeat light-medium, Soul/R&B light.
- **Credit waste prevention framework** — 0-50 learning, 50-80 discipline, 80+ stop and export.
- **Known bugs** — "Scratched CD" loop effect, Lyric Cache bug on Replace Section.
- **Aggressive mastering limiter** — Export raw stems for professional release.

### Documentation

- Added community research sources with URLs to SUNO-REFERENCE, model-prompt-strategies, metatag-reference, STUDIO-EDITOR-REFERENCE, and suno-parameter-map
- Updated validation dates across all reference files to April 6, 2026
- Created CHANGELOG.md

### Files Changed

- `suno-agent-band-manager/references/SUNO-REFERENCE.md`
- `suno-agent-band-manager/references/STUDIO-EDITOR-REFERENCE.md`
- `suno-style-prompt-builder/references/model-prompt-strategies.md`
- `suno-feedback-elicitor/references/suno-parameter-map.md`
- `suno-lyric-transformer/references/metatag-reference.md`
- `package.json`

---

## [1.4.0] - 2026-04-02

Update to BMB v1.5.0 standards, rename module from bmad-suno-* to suno-*.

---

## [1.1.3] and earlier

See git history for prior releases.
