# Changelog

All notable changes to the Suno Band Manager module are documented here.

---

## [Unreleased]

### Suno Knowledge — Three Production-Tested Findings

Three findings from 2026-04-28 production sessions (LV Mask + LV Mirror Image) folded upstream into reference docs as documentation-only updates. No version bump — accumulating for the next release that bundles enough material to warrant one.

- **`model-prompt-strategies.md` → "Brass-Out-At-Outro Limitation"** (new subsection under Three-Phase Dynamic Arc). Documents the platform limitation: brass-fade-out instructions in section tags or style prompts are unreliably honored for brass-band-fusion genres across both v5 Pro and v5.5 Pro. Two production tests on the same source song (SF swamp-metal funk-fusion 2026-03-23 + LV Galactic-style modern NOLA funk-rock-brass fusion 2026-04-28) confirmed identical failure mode despite v5.5 Pro's improved prompt accuracy + in-bracket per-section instrumentation tags + stacked absence descriptors. Pure prompt-side techniques cannot reliably engineer brass-fade-out for brass-band-fusion genres; Pro-tier users have no surgical post-gen fix without Studio tier. Architects-around guidance + 8th LV dynamic archetype emergence noted.

- **`model-prompt-strategies.md` → "Brass-Band Gravity — Aggressive Counter-Emphasis Required"** (new subsection under First-Genre Dominance). Documents that brass-band genre gravity is exceptionally strong — single-mention guitar/rhythm-section descriptors get buried in observed gens even when present in the critical zone. Production-confirmed pattern table shows progressive counter-emphasis attempts; only "Guitar-driven" framing + multiple explicit guitar mentions in the critical zone (3 mentions in 200 chars) successfully surfaces guitar in the mix. Counter-intuitive guidance: this LOOKS like over-correction but is the right level for brass-band gravity specifically.

- **`gemini-audio-analysis.md` → Camelot framework limitations** (expanded DJ Harmonic Mixing subsection). Documents that Camelot perfection is NOT a comprehensive transition-smoothness measure — it tracks key relationships only and does not capture tempo gaps, genre/style register, energy/dynamic level, or production aesthetic. Production-confirmed (LV Mirror Image placement 2026-04-28) where "Camelot-perfect" placement options were rejected in favor of a Camelot-rougher position because the listening experience was less jarring. Practical placement-evaluation rule: describe the listening experience as the primary criterion; Camelot is one input among many; flag tempo / genre-register / energy gaps explicitly when significant. Camelot is reliable for same-genre / same-tempo placements but breaks down when other dimensions diverge.

---

## [1.7.0] - 2026-04-26

### Script Reorganization + Portable Behavioral Preferences + Suno Knowledge Doctrine Fixes

Two structural threads land in this release:

1. **Script reorganization** addressing community-marketplace feedback ([bmad-code-org/bmad-plugins-marketplace#7](https://github.com/bmad-code-org/bmad-plugins-marketplace/pull/7)). Previously the module had a top-level `scripts/` folder with six scripts that didn't follow the BMad plugin install convention — skills land at `.claude/skills/{skill-name}/`, but top-level `scripts/` had no install path. Investigation showed that 4 of the 6 scripts are agent-skill-internal in practice (only ever invoked from within `suno-agent-band-manager`'s flow) and were never truly "shared" — they had simply not been placed inside the skill that owns them. They've now been moved into the agent skill's `scripts/` folder. The remaining 2 scripts (`pack-portable.{sh,ps1}`, `unpack-portable.{sh,ps1}`) are user-facing entry points that need a stable project-root path for direct user invocation, so they stay at top-level `scripts/` with documentation flagging the marketplace-install gap.

2. **Portable behavioral-preferences file + production-tested Suno-knowledge corrections** (originally tracked as the v1.6.8 unreleased work — now folded into v1.7.0). Mac had been saving user-articulated behavioral feedback (no-disclaimed-restraint, no-false-dichotomy, no-piano-forward defaults, voice-character-not-genre-gravity, etc.) to per-machine agent memory caches that don't travel via portable sync — so corrections articulated on one machine never reached the other. Fixed structurally: behavioral preferences now live in a portable file the sync carries; Suno platform knowledge corrections folded upstream into module reference docs.

### Added — Script Reorganization

- **Agent-internal scripts moved into `src/skills/suno-agent-band-manager/scripts/`** — `validate-sidecar.py`, `regenerate-index-sections.py`, `reconcile-sidecar.py`, `pipeline-guard.py` now live with the skill that owns them. Previously top-level `scripts/`. Path references updated across the agent's reference files (`activation.md`, `init.md`, `memory-system.md`, `save-memory.md`, `creed.md`) to use the skill-relative `./scripts/X.py` convention (matches the existing `pre-activate.py` / `validate-path.py` / `check-memory-health.py` invocation pattern in the same skill).

- **`pack-portable.sh` / `pack-portable.ps1` updated** to call `validate-sidecar.py` at the new agent-skill location (`$PROJECT_ROOT/.claude/skills/suno-agent-band-manager/scripts/validate-sidecar.py`).

- **`unpack-portable.sh` / `unpack-portable.ps1` updated** to call `reconcile-sidecar.py` at the new agent-skill location.

- **`suno-setup` SKILL.md `--guard-script-path` argument** updated from `scripts/pipeline-guard.py` to `.claude/skills/suno-agent-band-manager/scripts/pipeline-guard.py` so the Stop-hook command written into user `.claude/settings.local.json` points at the new location.

- **`module_greeting` in `src/skills/suno-setup/assets/module.yaml`** expanded with a brief pointer to `pack-portable.sh` and a note for marketplace-install users — surfaces the multi-machine workflow at install completion when users are most likely to read the greeting.

- **`INSTALLATION.md` "Multi-Machine Sync" section** clarifies that pack/unpack scripts are user-facing entry points distinct from agent-internal scripts, with explicit guidance for marketplace-install users on how to obtain `pack-portable.sh` / `unpack-portable.sh` (clone the repo separately, or copy the two files from the GitHub repo into their project's `scripts/` folder). Future installer release may auto-deposit these.

- **`INSTALLATION.md` Pipeline Guard section** updated with the new `pipeline-guard.py` path.

### Added — Portable Behavioral Preferences

- **`docs/mac-preferences.md` — new portable file** for user-specific Mac behavioral preferences (communication style, pacing rules, framing rules, conversation discipline). Loaded on activation by the agent. Distinct from the voice file (which covers the user as a writer/creator) and from per-machine agent memory (which doesn't travel via portable sync).
- **`activation.md` — Step 6b** added: load `docs/mac-preferences.md` if present and apply for the session.
- **`memory-system.md` — `docs/mac-preferences.md` section** added (placed before `index.md` section). Documents what goes in the file, why it lives in `docs/` rather than per-machine agent caches, when to write entries, and what does NOT belong (Suno platform knowledge → module refs upstream; musical preferences → patterns.md / voice file; band/catalog policies → band profiles / voice file).
- **`save-memory.md` — Step 2c** added: behavioral preference writes scan, ensuring corrections articulated mid-session were appended to `docs/mac-preferences.md` per "Sync at the point of change."
- **`portable-manifest.example.yaml`** includes `docs/mac-preferences.md` in default include list.

### Changed — Suno Knowledge Corrections (production-tested patterns folded upstream)

- **`metatag-reference.md` — paren-spacing rule REVERSED.** A prior version recommended "no space before opening paren tightens coupling: `word(echo)` not `word (echo)`." That was based on a single-song experimental finding (SF Distant Mourning, March 2026) that got mis-promoted to a general rule. Verified across catalog April 2026 — every working parenthetical-backing-vocal song uses spaces before the paren. The no-space form caused `(blasting)` to be skipped on DM-LV Bridge across multiple gens until spaces were added. Catalog-standard is `word (echo)` (with space). Doc now reflects this and explains the prior-rule provenance.
- **`metatag-reference.md` — paren-at-end-of-line rule** added with broken-and-fixed example. Mid-line parens (text after the closing paren on the same line) get dropped inconsistently. If the sentence continues past the paren, break the line after the closing paren.
- **`metatag-reference.md` — long-paren-fold-back data point** added. Long parentheticals (~10+ syllables) pull as primary vocal even with triple-reinforcement; short parens (1-4 syllables) land as backing-vocal interjections reliably. Boundary is approximate.
- **`metatag-reference.md` — `[Whispered, vulnerable]` context-dependent caveat** added. Reliable in folk-intimate / acoustic-singer-songwriter / ballad contexts; in theatrical-horror / voodoo-rock / dramatic-narrative contexts it can pull spoken-word delivery. Use `[Vocal Style: soft, sung]` in those genres — the explicit `sung` token defeats the spoken-word drift.
- **`metatag-reference.md` — Stretched Words section** added under Word-Formatting Effects. Documents vowel-collapse drift on hyphenated stretched words (`to-o-o-lling` → "tooling") and disambiguation techniques (insert `h`, alt-vowel spelling, double-consonant anchor, re-articulate with ellipses). DM-LV April 2026 production data point as the example.
- **`metatag-reference.md` — Section-tag content rule** added under Section Structure Tags. Em-dashed descriptive labels (`[VERSE 1 — THE ROOM]`) burn character budget for nothing — Suno has no training on them. Use parameterized syntax (`[Verse 1: hushed, tense]`) for direction Suno can act on. Applies equally to cross-band conversions.
- **`model-prompt-strategies.md` — Voice Gravity section CORRECTED.** A prior version framed v5.5 Voice clones as carrying "trained genre gravity" pulling generations toward a trained baseline. That framing was overstated. Voice cloning trains on vocal samples and captures vocal character (timbre, lilt, vibrato, attack patterns, dynamics behavior) — character is genre-neutral; Suno adapts character to the genre prompt. Section renamed to "v5.5 Voice-Character Principle" and rewritten to reflect that the captured character is what the Voice carries, the case study validates correct Audio Influence + don't-duplicate-Voice-descriptors + specify-arrangement-explicitly (NOT "voice has genre gravity"), and Voice direction should be framed as **"the captured character fits X register well"** rather than "fighting the Voice's trained gravity toward Z."

### Migration

None required. The script reorganization is transparent to users:

- **Existing dev clones** continue to work — the moved scripts are still in the repo, just at a different path. Reference files and pack-portable shell scripts have all been updated to the new paths in the same release. After pulling v1.7.0, the Stop-hook command in `.claude/settings.local.json` will need to be re-run via `python3 .claude/skills/suno-setup/scripts/configure-guard.py` (or the suno-setup skill) to update the path string from `scripts/pipeline-guard.py` to `.claude/skills/suno-agent-band-manager/scripts/pipeline-guard.py`. The hook entry can also be edited manually.
- **Marketplace-install users** get the moved scripts as part of the agent skill install (no change needed). For pack/unpack-portable, see the new INSTALLATION.md "Multi-Machine Sync" guidance — the marketplace install path doesn't currently deposit top-level `scripts/`, so users wanting portable sync need to copy `pack-portable.{sh,ps1}` and `unpack-portable.{sh,ps1}` from the GitHub repo manually until a future installer feature lands.
- **No user data changes.** `docs/` and `_bmad/` are untouched.

### Version Bumps

- `src/skills/suno-setup/assets/module.yaml`: 1.6.7 → 1.7.0
- `.claude-plugin/marketplace.json`: 1.6.7 → 1.7.0

### Marketplace Submission

The community module entry on [bmad-code-org/bmad-plugins-marketplace](https://github.com/bmad-code-org/bmad-plugins-marketplace) (`registry/community/suno-band-manager.yaml`) will be updated to point at the v1.7.0 commit SHA via a new PR so marketplace consumers see the script-reorganized version. Brian (BMad maintainer) flagged the shared-content question on PR #7 after the original merge at v1.6.7; this release addresses that feedback structurally.

---

## [1.6.7] - 2026-04-22

### Drift Protection — Round Three, plus Research Refresh

v1.6.5 and v1.6.6 put the drift-protection machinery in place (validators, regenerators, reconciliation on unpack, cross-reference scanning). Real sessions since then surfaced three gaps in the machinery itself — one of which made v1.6.5 effectively unusable without hand-editing — and a fourth at the doctrine level where the module's definition of "sync" still treated cross-file consistency as a milestone-reconciliation step rather than an edit-time invariant. This release closes all four, and folds in the production-knowledge work that piled up across the same sessions (counter-genre prompting research, wordless-chant intro technique, Package Assembly Rule hardening, a CRITICAL rule on what exclusions are actually for).

### Root Cause — Issue #31 (sync at point of change)

Issue #18 added `reconcile.md` as a milestone-propagation protocol (title changes, publishes, playlist reorders, profile edits). Issue #31 is the orthogonal gap: **non-milestone edits** — creating a new reference file, bumping a catalog count in the sidecar, marking a source closed — never trigger `reconcile.md` and create drift windows in every file that references them. `save-memory.md` Step 6's "Companion files audit" caught drift eventually, but was operating as the **primary sync mechanism** rather than a backstop, leaving files out of sync for the entire session between the edit and the save.

The doctrine-level fix: treat cross-file consistency as an invariant maintained at every write-boundary, not as a milestone reconciliation step.

### Added

- **`creed.md` — new foundational principle: "Sync at the point of change."** Joins the three existing principles (Always output everything / Meet them where they are / The magic is iteration) as a top-level rule. When editing a file, check in the same write-batch whether any other tracked file references what just changed (counts, descriptions, status markers, cross-references, file paths, companion-files tables) and update those references immediately. Audit-at-save-time is explicitly reframed as a backstop, not the primary sync mechanism. Drift windows between edit and save are unacceptable because the session may be interrupted or handed off at any point.

- **`regenerate-index-sections.py` → `--migrate` flag.** New `migrate_section()` helper locates a `## Recently Published` or `## Catalog Status` heading, finds the end of the section (next `##` heading or EOF), and wraps the body content with the required `derived:*:start/end` marker pairs in-place. One-command migration for pre-v1.6.5 sidecars and for any sidecar that somehow slipped through First Breath without markers. Migration is idempotent (skips sections that already have markers), safe under `--dry-run` (no writes), and aborts without partial writes when a heading is missing entirely (prints which heading is missing and exits 1).

- **`init.md` — `index.md` template baked into First Breath.** New sidecars are born already-migrated, with both `derived:recently-published:start/end` and `derived:catalog-status:start/end` marker pairs wrapping stub content. The template also gives the agent a concrete structure for User Preferences, Current Work, Pending / Parked Work, and Session History so First Breath output is consistent across sessions.

- **`validate-lyrics.py` — HIGH-confidence standalone-tag allowlists.** Three new recognized sets mirrored from `metatag-reference.md`: `VALID_STANDALONE_MOODS` (16 tags), `VALID_STANDALONE_ENERGY` (10 tags), `VALID_TIMING_RHYTHM` (9 tags). Wired into the existing invalid-metatag check as an `is_standalone` gate alongside `is_section` / `is_vocal_cue` / `is_descriptor`. Eliminates a class of false-positive findings that had been eroding trust in the validator.

- **`creed.md` → Package Assembly Rule: Pre-Output Self-Check (MANDATORY) + Violation Tells + Highest-Risk Contexts.** Before sending any response containing a Suno package, verify in reasoning that both `suno-style-prompt-builder` and `suno-lyric-transformer` were invoked *this turn* (or lyrics aren't needed). Violation Tells enumerate the concrete signs the pipeline was skipped: missing Title field, hand-assembled copy-ready blocks, using validation scripts as pipeline substitutes, prior-iteration framing in exclusion reasoning, "I already know what the skill would produce" reasoning. Highest-Risk Contexts call out parallel-band repackaging, minor refinements after a successful first gen, and extended direction-setting discussions — historically the contexts that trigger pipeline-skipping.

- **`model-prompt-strategies.md` — Counter-Genre Prompting section** (fixes #28). Four additions from session-14 research (2026-04-20, 15+ 2025-2026 sources surveyed):
  - *First-Genre Dominance* (under Genre Keyword Ordering) quantifies position 1 holding the strongest single signal, with genre + subgenre tags collectively carrying ~60-70% of arrangement output. Explains why counter-genre work requires the counter-target in position 1, not buried at position 3-4.
  - *Default Weirdness Normalizes Counter-Genre Prompts* (under Slider Guidelines) documents v5.5's "accept then normalize" behavior and prescribes Weirdness 60-70 for counter-genre prompts. Explicitly supersedes the prior conservative-Weirdness-for-accessibility guidance, which was self-imposed caution and not grounded in evidence.
  - *Counter-Genre Prompting* (new top-level section) with four subsections: Displacement-Budget Descriptors (role-slot filling with structurally-incompatible descriptors), Triple-Signal Tempo Stacking, 6/8 and 12/8 Compound Meter as a tempo-perception lever, and a Synthesis full-example prompt deploying all techniques.
  - *Community Research Sources* expanded with HookGenius Complete Suno Prompt Guide 2026, HookGenius Tempo BPM Guide, HookGenius Negative Prompting Guide, JG BeatsLab 7 v5.5 Behaviors, Blake Crosley v5.5 Reference, and Suno Studio 1.2 release notes.

- **`metatag-reference.md` — Wordless-chant intro + doubled-word parentheticals.** Production-tested guidance from Cities of the Dead (Lenny's Voice) generation: doubled-word parentheticals as ritualistic/trance backing technique, the exclamation-separator fix for single-word truncation, inline vs. line-separated parenthetical semantics, and a new *Establishing Non-Default Vocal Arrangements* subsection documenting the wordless-chant intro as the reliable lever when group backing vocals fail to establish on V1. `model-prompt-strategies.md` gets a paired exception: non-default vocal arrangements earn position 1 in the style prompt ahead of even genre.

### Changed

- **`save-memory.md` Step 6 — "Companion files audit" reframed as a backstop.** Previous wording implied the audit **was** the sync. New framing is explicit: the audit should normally find nothing; if it catches drift, that means a point-of-change sync was missed — fix the drift now AND note which edit missed the sync as a behavioral gap to correct going forward. Audit-time fixes are tolerated, not planned.

- **`save-memory.md` Step 5 — pre-write sync check before chronology.** Before writing the session summary to `chronology.md`, scan the session's writes for cross-referenced updates that didn't land in the same batch as their triggering edit (new `docs/` files → voice file Companion Files table; songbook add → playlist YAML + voice catalog; sidecar Key Files path change → doc references; WIP COMPLETED → sidecar Pending / Parked). The chronology write is the last narrative write of the session and is the correct moment to self-check that cross-file invariants held at each edit, not just at save time.

- **`create-song.md` Step 7 — sync at each sub-step write, not just at the Step 7 aggregate.** Per the new creed principle, Post-Publish Reconciliation is explicitly reframed as a milestone backstop. Concrete expectations at publish time: songbook entry write → voice catalog count + Companion Files entry in the same batch; playlist YAML edit → playlist ordering doc in the same batch; WIP COMPLETED → sidecar Pending / Parked drop in the same batch; title finalized → all in-session references updated in the same batch as the rename.

- **`refine-song.md` — new Sync-at-Write for Refinements section.** Refinement edits that touch **published** song attributes (key/tempo/Camelot, voice clone, voice gravity, playlist position, renames) propagate in the same write batch as the triggering edit. Refinements that touch only the current-iteration package (not yet in the songbook) are scoped out — nothing references them yet.

- **`regenerate-index-sections.py` — clearer missing-markers error.** Previous message said "See v1.6.5 release notes for migration guidance" — a cold trail from an error the agent routinely hits. New message names the `--migrate` flag as the one-command fix and points directly at the CHANGELOG 1.6.5 migration block for the exact template. `save-memory.md` Step 4a updated in parallel so the agent, on hitting the missing-markers error mid-session, reaches for `--migrate` instead of hand-editing markers in.

- **`regenerate-index-sections.py` and `validate-sidecar.py` — YAML parse errors no longer silent** (fixes #29). `regenerate-index-sections.py::parse_song()` now prints a stderr WARNING with file path + exception detail before returning None, naming the common cause (flow-sequence values with inner brackets like `[ST + CC; added [Spoken] outro]`) and pointing to issue #29. `validate-sidecar.py::parse_song()` signature changed to return `(Song|None, error_msg|None)`; `load_all_songs()` returns `(songs, parse_findings)` and converts each YAML parse error into a `songbook_drift` error-severity Finding so the pre-pack sync-gate blocks instead of silently hiding the song. Previously: songs with bracket-inner YAML quietly vanished from Recently Published + Catalog Status and the validator still reported PASS.

- **`creed.md` → Package Assembly Rule: Exclusion drift-risk CRITICAL RULE.** Excludes defend against drift risks that the CURRENT style prompt's own descriptors might introduce — nothing else. Suno is stateless; it has no knowledge of prior gens, other bands' renderings of the same lyrics, or the broader catalog. Exclusion reasoning that references "the other band's version," "the prior iteration," or "what [other band/previous gen] used" is a violation tell.

- **Root `CLAUDE.md` / `GEMINI.md` / `AGENTS.md`** trimmed to a brief cross-tool reinforcement pointing to `creed.md` as authoritative on the Package Assembly Rule. Single source of truth, no duplicated content.

### Fixed

- **Issue #27** — `validate-lyrics.py` flagged HIGH-confidence standalone bare-bracket tags (e.g. `[Low Energy]`, `[Driving]`, `[Half-Time]`, `[Building]`, `[Haunting]`) as unrecognized metatags, producing noisy false-positive findings. Now matches `metatag-reference.md`.
- **Issue #28** — counter-genre prompting knowledge from session-14 research (2026-04-20) was not reflected in the module. Now documented in `model-prompt-strategies.md`.
- **Issue #29** — songbook entries using `transformations_applied` flow-sequence YAML with inner square brackets silently failed YAML parsing and got excluded from derived sidecar sections, with validator still reporting PASS. Silent failure replaced with surfaced WARNING + blocking `songbook_drift` error.
- **Issue #30** — v1.6.5's derived-section markers were never written by any codepath in the module: First Breath (`init.md`) wrote narrative `index.md` without markers, and `pre-activate.py`'s scaffold intentionally skipped `index.md`. Every new sidecar was born un-migrated and hit the missing-markers error the first time the regenerator ran. Fixed three ways: markers baked into the First Breath template, new `--migrate` flag for one-command in-place migration, better error message naming `--migrate` as the fix.
- **Issue #31** — cross-file sync was treated as milestone-reconciliation-only; non-milestone edits created drift windows that `save-memory.md` Step 6 caught as primary sync rather than backstop. "Sync at the point of change" principle now formalized in `creed.md`, `save-memory.md` Step 6 reframed as backstop, sync-at-write expectations added to `create-song.md` Step 7 and `refine-song.md`.

### Migration

None required. All changes are additive or wording-level:
- Existing installs with pre-v1.6.5 sidecars that still lack derived-section markers can now run `python3 scripts/regenerate-index-sections.py "{project-root}" --migrate` for a one-command fix — no more hand-editing markers in.
- Existing installs that already have markers get a clean no-op from `--migrate`.
- `validate-lyrics.py` allowlist expansion only removes false positives; no existing lyrics break.
- `validate-sidecar.py` now surfaces YAML parse errors that were previously silent — this may cause a pre-pack sync-gate block on installs with bracket-inner YAML values that were silently being dropped. Fix by quoting the offending value; the surfaced message names the fix.

### Version Bumps

- `package.json`: 1.6.6 → 1.6.7
- `src/skills/suno-setup/assets/module.yaml`: 1.6.6 → 1.6.7
- `.claude-plugin/marketplace.json`: 1.6.6 → 1.6.7
- `INSTALLATION.md`: 1.6.6 → 1.6.7

### Verification

- **Issue #30 end-to-end** — fresh pre-v1.6.5 sidecar with both headings → `--migrate` wraps both sections, regenerator rewrites between markers, exit 0; re-running `--migrate` on already-migrated sidecar → clean no-op ("No changes needed"); sidecar missing one heading → `--migrate` aborts with clear message naming the missing heading, no partial writes; `--migrate --dry-run` → prints regenerated sections, does not write; production sidecar (already migrated) → `--migrate --dry-run` is a clean no-op.
- **Issue #29 exact repro** — songbook entry with `transformations_applied: [ST + CC; added [Spoken] outro]` → `validate-sidecar` emits `songbook_drift` error and exits 1; `regenerate-index-sections` emits stderr warning and continues.
- **Issue #27 smoke test** — lyrics using `[Low Energy]`, `[Driving]`, `[Half-Time]`, `[Building]`, and `[Haunting]` all pass cleanly; prior false positives eliminated.
- **First Breath template** — new sidecars scaffold with both marker pairs in place; regenerator runs clean on first save.
- **Package Assembly Rule self-check** — Pre-Output Self-Check language validated against the creed-as-authoritative architecture; root `CLAUDE.md`/`GEMINI.md`/`AGENTS.md` point at the creed with no duplicated content.

### Scope Note

This release adds **one new script flag** (`regenerate-index-sections.py --migrate`), **extends two scripts** (`validate-lyrics.py` standalone-tag allowlists; `validate-sidecar.py` + `regenerate-index-sections.py` YAML-error surfacing), and **updates seven reference docs** (`creed.md`, `save-memory.md`, `create-song.md`, `refine-song.md`, `init.md`, `model-prompt-strategies.md`, `metatag-reference.md`) plus the three root standing-orders files (`CLAUDE.md` / `GEMINI.md` / `AGENTS.md`). User data (`docs/`, `_bmad/`) is not part of the module and remains untouched by the module upgrade. No user migration required — pre-v1.6.5 sidecars have an opt-in one-command path via `--migrate`.

---

## [1.6.6] - 2026-04-16

### Drift Protection — Round Two

A follow-on to v1.6.5's Sidecar Drift Protection release. v1.6.5 closed the largest drift gap (index sections vs. songbook ground truth), but three smaller classes of drift surfaced in sessions afterward:

1. **Forward-intent cross-references.** Markdown files referencing other docs files that were never actually created — `` `docs/catalog-meta-observations.md` `` mentioned declaratively in a WIP draft, but the target file doesn't exist on disk. The v1.6.5 validator scanned songbook frontmatter/body agreement and audio file existence; it didn't scan prose for markdown cross-references.
2. **Unpack-side sidecar drift.** The pre-pack validator gates sync on the source machine, but after unpack on the receiving machine the sidecar still reflects the receiving machine's prior local state. Freshly-arrived WIP notes, session-context edits, and songbook updates don't automatically make it into the sidecar narrative — the agent has to remember to integrate them, and often didn't.
3. **Machine-specific absolute paths in access-boundaries.** The scaffold template wrote a `{project-root}/...` placeholder that users or agents sometimes expanded to an absolute `/home/.../bmm/...` path during edits, making the file non-portable. Paths in `access-boundaries.md` are conceptually relative to project root; absolute paths were vestigial.

This release closes all three.

### Added

- **`scripts/reconcile-sidecar.py`** — post-unpack reconciliation helper. Lists every `docs/**/*.md` file whose mtime is more recent than the sidecar's `index.md` (likely integration candidates), runs `validate-sidecar.py` to surface drift, and produces a punch list for the agent to walk through with the user. Exits 1 when reconciliation is needed, 0 when clean. `--format json` for programmatic consumption. Does not edit files — reconciliation itself is the agent's job.

- **`scripts/validate-sidecar.py` → `check_markdown_cross_references()`** — new check that scans every `.md` file under `docs/` for inline-code references (`` `docs/X.md` ``) and markdown-link references (`[text](X.md)`, `[text](../path/to/X.md)`) and verifies each target exists on disk. Reports findings with category `cross_reference_missing`, severity `warning`. Dual-anchor resolution (tries both parent-relative and project-root-relative) so the user convention of writing `` `docs/X.md` `` from inside a file already in `docs/` still resolves correctly. Skips external URLs, anchor-only references, self-references, glob/wildcard patterns, and anything inside fenced code blocks.

### Changed

- **`scripts/unpack-portable.sh` and `unpack-portable.ps1`** — automatically invoke `reconcile-sidecar.py` after extraction. The reconcile report prints to stderr so the agent reading the script output sees the punch list without parsing it out of a JSON stdout channel. Bypass with `BMAD_SKIP_RECONCILE=1` (or `$env:BMAD_SKIP_RECONCILE=1` on PowerShell). The reconcile call never fails the unpack — reconciliation is advisory, and the integration decisions belong to the agent and user.

- **`src/skills/suno-agent-band-manager/scripts/pre-activate.py → scaffold_sidecar()`** — `access-boundaries.md` scaffold now writes bare relative paths (`_bmad/_memory/band-manager-sidecar/`) instead of the `{project-root}/` placeholder form. Paths are all conceptually relative to project root; the placeholder was a convention artifact that sometimes got expanded to absolute paths during edits. Includes a one-line header clarifying the convention: *"All paths below are relative to the project root."*

  `validate-path.py` continues to handle both bare-relative and `{project-root}/` forms, so existing installs with the legacy placeholder keep working unchanged. Only new scaffolds change.

- **`src/skills/suno-agent-band-manager/references/activation.md` step 5** — sync package handling now requires post-unpack sidecar reconciliation before proceeding to the main menu. Previously the step said "reload affected files" which was soft and easy to skip. The new language is explicit: run `reconcile-sidecar.py`, walk every `newer_files` entry and every validator finding with the user via the Handoff Checkpoint Pattern, integrate approved changes into the narrative sections of `index.md`, regenerate derived sections, and only then proceed into the normal activation flow.

- **`src/skills/suno-agent-band-manager/references/memory-system.md`** — new *Post-Unpack Reconciliation* section documents the mandatory protocol. *Access Control* section now documents the path convention (relative to project root, no placeholder, no absolute paths — validator resolves both forms for back-compat).

- **`src/skills/suno-agent-band-manager/references/save-memory.md` step 7** — reconciliation check now also covers `cross_reference_missing` warnings from the validator. If broken cross-references are detected, surface them to the user and resolve (create target file, rephrase as future-intent, or remove the reference) before packing. The class of drift described in issue #23 gets caught automatically at save time now, not just at unpack time.

### Fixed

- **Issue #23** — `validate-sidecar.py` didn't catch declarative references to docs files that were never created. Now flagged as `cross_reference_missing` warnings.
- **Issue #25** — no post-unpack reconciliation meant the sidecar narrative could silently lag behind freshly-arrived file content. Now the agent gets a punch list automatically and the protocol requires reconciliation before proceeding.
- **Issue #26** — access-boundaries scaffold emitted `{project-root}/` placeholder paths that sometimes got expanded to absolute machine paths, breaking portability. Scaffold now writes bare relative paths. Existing files with the placeholder form keep working.

### Migration

None. All changes are additive or internal:

- Existing installs with `{project-root}/` paths in `access-boundaries.md` continue to work — `validate-path.py` normalizes both forms.
- Existing sidecars work unchanged — the reconcile script is new tooling, not a schema change.
- The cross-reference check runs automatically as part of `validate-sidecar.py`; findings are warnings, not errors, so existing drift surfaces but doesn't block syncs.

### Version Bumps

- `package.json`: 1.6.5 → 1.6.6
- `src/skills/suno-setup/assets/module.yaml`: 1.6.5 → 1.6.6
- `.claude-plugin/marketplace.json`: 1.6.5 → 1.6.6
- `INSTALLATION.md`: 1.6.5 → 1.6.6

### Verification

- **Cross-reference check on current test harness:** 7 legitimate drift findings surfaced in the test project — broken references to `outreach-tracker.md`, `sessions/2026-04-10.md`, `case-state.md`, `identity-and-context.md`, `docs/wip-contentment-poem-brainstorm.md`, `wip-categories-fragments.md`, `back-woods-rushin-city-slow.md`. Zero false positives. All legitimate — this is exactly the class of drift issue #23 described.
- **Glob-pattern filtering:** `per-candidate/*.md` glob references correctly skipped (intent-references, not single-file lookups).
- **Scaffold output:** fresh project scaffolds `access-boundaries.md` with bare relative paths and no `{project-root}/` strings anywhere in the file.
- **Back-compat:** `validate-path.py` unit-tested against a boundaries file containing both `docs/X/` and `{project-root}/docs/X/` forms — both resolve identically.
- **Unpack script:** `unpack-portable.sh` runs `reconcile-sidecar.py` automatically after extraction on Linux; report prints to stderr with the stale-files punch list.
- **Reconcile script edge cases:** returns exit 0 with `status: no_sidecar` when no sidecar exists (nothing to reconcile); returns exit 1 with populated `newer_files` when docs files are newer than `index.md`; returns exit 0 with `status: clean` when sidecar is in sync.

### Scope Note

This release adds **one new script** (`reconcile-sidecar.py`), **extends one script** (`validate-sidecar.py` gains `check_markdown_cross_references()`), and **updates two scripts + three reference docs** (`unpack-portable.sh`, `unpack-portable.ps1`, `pre-activate.py`, `activation.md`, `memory-system.md`, `save-memory.md`). User data (`docs/`, `_bmad/`) is not part of the module and remains untouched by the module upgrade. No user migration required.

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
