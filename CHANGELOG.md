# Changelog

All notable changes to the Suno Band Manager module are documented here.

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
