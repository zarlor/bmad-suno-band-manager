# Quality Report: bmad-suno-lyric-transformer

**Scanned:** 2026-03-26T093154
**Skill Path:** /home/zarlor/bmm/_bmad-output/bmad-suno-band-manager-module/src/skills/bmad-suno-lyric-transformer
**Report:** /home/zarlor/bmm/_bmad-output/bmad-suno-band-manager-module/src/skills/reports/bmad-suno-lyric-transformer/quality-scan/2026-03-26T093154/quality-report.md
**Performed By** QualityReportBot-9001

## Executive Summary

- **Total Issues:** 38
- **Critical:** 2 | **High:** 14 | **Medium:** 9 | **Low:** 13
- **Overall Quality:** Good
- **Overall Cohesion:** cohesive
- **Craft Assessment:** Well-crafted domain-expert skill with strong overview, good intelligence placement, and proper reference extraction. Primary issue is monolithic SKILL.md needing extraction and ~240 tokens of domain knowledge duplicated between Step 3 and the metatag reference.

The bmad-suno-lyric-transformer is a songwriter's workshop collaborator that transforms poems and text into Suno-ready structured lyrics. It demonstrates exceptionally mature architecture with 8 supporting scripts, a best-in-class headless mode with three sub-modes, and production-tested Suno domain knowledge. The most significant structural gap is three missing required agent sections (Identity, Communication Style, Principles), and the most pervasive standards issue is bare internal paths without the `./` prefix across 23 locations in SKILL.md.

### Issues by Category

| Category | Critical | High | Medium | Low |
|----------|----------|------|--------|-----|
| Structure & Capabilities | 0 | 4 | 2 | 2 |
| Prompt Craft | 0 | 1 | 4 | 3 |
| Execution Efficiency | 0 | 0 | 0 | 2 |
| Path & Script Standards | 2 | 6 | 0 | 0 |
| Agent Cohesion | 0 | 0 | 2 | 1 |
| Creative | -- | -- | 8 | 5 |

---

## Agent Identity

- **Persona:** A songwriter's workshop collaborator that understands both songwriting craft and Suno's AI music generation quirks. Approaches transformation as a menu of options rather than all-or-nothing, respecting the writer's attachment to their words while offering expert-level structural and rhythmic guidance.
- **Primary Purpose:** Transform poems, raw text, and rough lyrics into Suno-ready structured song lyrics with metatags, proper section architecture, and rhythmic consistency.
- **Capabilities:** 8

---

## Strengths

*What this agent does well -- preserve these during optimization:*

**Domain Expertise & Production Knowledge**
- Deep domain expertise woven throughout with production-tested knowledge (scream bleed-through prevention, exclamation point bark triggers, ALL CAPS as loudness ceiling, parentheses as backing vocals, line density as primary tempo control, BPM tags confirmed ineffective). The metatag-reference.md is practically a standalone Suno production bible. *(agent-cohesion)*
- Section-jobs framework is practical and production-informed, including very-short-poem handling strategies (double delivery, chorus extraction, thesis isolation) and the "let the words decide" duration philosophy. *(agent-cohesion, enhancement-opportunities)*
- Metatag reference includes production-tested findings and confirmed failures, not just documentation -- grounded in actual Suno behavior rather than theoretical documentation. *(enhancement-opportunities)*

**Architecture & Design**
- Comprehensive headless mode with three distinct sub-modes (analyze, transform, refine), a structured JSON output contract, and a refinement spec format for targeted changes. One of the best headless implementations seen in a HITL skill. *(structure, enhancement-opportunities)*
- Exceptionally well-designed transformation menu with clear granularity -- seven transformation options plus WF mode at exactly the right level of abstraction with non-overlapping purposes and thoughtful mutual exclusion rules. *(agent-cohesion)*
- Complete user journey from raw text to Suno-ready output with handoff guidance. No dead ends -- every step feeds forward. *(agent-cohesion)*
- Word Fidelity Mode respects writer attachment to their original language, acknowledging varying levels of creative ownership. *(enhancement-opportunities)*

**Prompt Craft & Intelligence**
- Overview provides excellent domain context and design rationale -- concise but rich enough for informed judgment. *(structure, prompt-craft)*
- Description follows two-part format with quoted trigger phrases enabling reliable activation. *(structure)*
- Good intelligence placement -- scripts handle deterministic work (syllable counting, validation, cliche detection), prompts handle judgment (emotional arc mapping, chorus creation, voice matching). *(prompt-craft)*
- Compaction survival block is a good defensive pattern for context compaction resilience. *(prompt-craft)*
- SKILL.md is self-contained with zero back-references and zero suggestive loading patterns. *(prompt-craft)*
- Capture-don't-interrupt pattern is explicitly built into Step 1 for creative context. *(enhancement-opportunities)*

**Execution Efficiency**
- Step 1 input analysis uses explicit parallel batching (analyze-input.py, syllable-counter.py, and reference loading). *(execution-efficiency)*
- Step 4 quality check scripts run as a parallel batch (validate-lyrics.py, syllable-counter.py, section-length-checker.py). *(execution-efficiency)*
- Syllable counter results reused when RA was already applied -- prevents redundant script execution. *(execution-efficiency)*
- Reference files strategically pre-loaded in Step 1 for Step 3 use. *(execution-efficiency)*
- Activation sequence is logically ordered with graceful fallback when bmad-init is unavailable. *(structure)*

**Script Ecosystem**
- Mutual exclusion validation correctly delegated to validate-options.py script. *(script-opportunities)*
- Excellent pre-processing pattern: analyze-input.py and syllable-counter.py run as pre-pass before LLM analysis. *(script-opportunities)*
- Quality check step runs three validation scripts in parallel batch. *(script-opportunities)*
- Lyrics diff comparison delegated to lyrics-diff.py script. *(script-opportunities)*
- All scripts document --help usage pattern in SKILL.md -- LLM can invoke --help at runtime instead of inlining full interface documentation. *(script-opportunities)*

---

## Truly Broken or Missing

*Issues that prevent the agent from working correctly:*

### CRITICAL: {project-root} used for non-_bmad paths (2 locations)
**Source:** path-standards | **File:** SKILL.md

`{project-root}` is only valid for `{project-root}/_bmad/...` paths. Two locations use it for non-_bmad paths:

| File | Line | Context |
|------|------|---------|
| SKILL.md | 74 | Band profile path: `{project-root}/docs/band-profiles/{profile}` |
| SKILL.md | 299 | Songbook save path: `{project-root}/...` |

**Action:** Replace with the correct path variable or restructure these paths to use `{project-root}/_bmad/...`.

### HIGH: Missing required agent sections (3 sections)
**Source:** structure | **File:** SKILL.md

Three required agent sections are missing from SKILL.md:

| Missing Section | Embedded Hints Found | Impact |
|----------------|---------------------|--------|
| ## Identity | Line 10: "Act as a songwriter's workshop collaborator" | Weaker behavioral priming without dedicated section |
| ## Communication Style | Line 94: "Use the songwriter's workshop voice" | Inconsistent tone across interactions |
| ## Principles | Scattered throughout workflow steps | No consolidated decision framework |

**Action:** Add all three sections. Extract the identity statement from Overview, consolidate the scattered voice guidance with 3-5 concrete examples, and consolidate key principles (preserve writer's voice, respect 3000-char budget, verify claims against script output, etc.).

### HIGH: Monolithic SKILL.md at 312 lines / ~6525 tokens
**Source:** prompt-craft | **File:** SKILL.md:1

SKILL.md contains the full workflow inline rather than delegating detail to capability prompt files. At 312 lines it exceeds the ~250 line guideline. The transformation sub-steps (3a-3g) alone span ~95 lines.

**Action:** Extract Step 3 (Transform) into a dedicated capability prompt file (e.g., transform.md). Consider also extracting Refinement Mode and the Headless Output Contract.

### HIGH: README.md prompt file at skill root
**Source:** path-standards | **File:** README.md

All progressive disclosure content must be in `./references/` -- only SKILL.md belongs at root.

**Action:** Move README.md to `references/README.md`.

### HIGH: Parent directory reference (../) in README.md
**Source:** path-standards | **File:** README.md:66

Parent directory references are fragile and break with reorganization.

**Action:** Remove or replace the `../` reference with a stable cross-reference mechanism.

### HIGH: README.md missing progression condition keywords
**Source:** structure | **File:** README.md:67

No progression condition keywords found. Without them, the prompt cannot signal when to advance or complete its task.

**Action:** Add progression conditions (e.g., "when complete", "proceed when", "if satisfied") to define clear exit criteria.

### HIGH: Bare internal paths without ./ prefix (23 locations)
**Source:** path-standards | **File:** SKILL.md

23 instances of bare `scripts/` and `references/` paths without the `./` prefix. The `./` prefix distinguishes skill-internal paths from `{project-root}` paths.

| Category | Lines |
|----------|-------|
| `scripts/...` references | 26, 85, 86, 135, 202, 233, 244, 245, 246, 282, 303, 304, 305, 306, 307, 308, 309, 310, 311 |
| `references/...` references | 87, 87, 146, 146 |

**Action:** Add `./` prefix to all internal `scripts/` and `references/` paths (e.g., `./scripts/analyze-input.py`, `./references/metatag-reference.md`).

### HIGH: Python lint issues across 3 scripts (10 findings)
**Source:** scripts | **Files:** analyze-input.py, syllable-counter.py, validate-lyrics.py

| Issue | File | Lines |
|-------|------|-------|
| E741: Ambiguous variable name `l` | analyze-input.py | 155, 156 |
| E741: Ambiguous variable name `l` | syllable-counter.py | 239, 268 |
| E741: Ambiguous variable name `l` | validate-lyrics.py | 203, 324 |
| F841: Unused variable `instrumental_seconds` | syllable-counter.py | 142 |
| F841: Unused variable `orphaned_descriptors` | validate-lyrics.py | 81 |
| F841: Unused variable `tag_lines` | validate-lyrics.py | 161 |
| F541: f-string without placeholders | validate-lyrics.py | 266 |

**Action:** Rename `l` to `line` or similar descriptive name. Remove unused variable assignments. Remove extraneous `f` prefix.

---

## Detailed Findings by Category

### 1. Structure & Capabilities

**Agent Metadata:**
- Sections found: Overview, Activation Mode Detection, On Activation, Workflow Steps, Scripts
- Capabilities: 8
- Memory sidecar: No
- Headless mode: Yes (strong -- multiple sub-modes, output contract, refinement spec)
- Structure assessment: Structurally functional with strong domain grounding, but missing three required sections

#### Medium

**Name does not follow standard agent naming pattern**
*File:* SKILL.md:1 | *Source:* structure

The skill name "bmad-suno-lyric-transformer" uses a non-standard convention. Expected patterns: `bmad-{code}-agent-{name}` or `bmad-agent-{name}`.

*Action:* Evaluate whether this is intentional for a skill (vs agent) naming convention, or rename to follow the standard pattern.

**README.md prompt file missing config header**
*File:* README.md:1 | *Source:* structure

The README.md prompt file has no config header defining language variables.

*Action:* Add a config header to README.md with relevant language variables.

#### Low

**Embedded identity in Overview should be extracted**
*File:* SKILL.md:10 | *Source:* structure

The phrase "Act as a songwriter's workshop collaborator" functions as an identity statement but is buried in the Overview paragraph.

*Action:* Extract to a dedicated ## Identity section placed between ## Overview and ## Activation Mode Detection.

**Scattered voice guidance should be consolidated**
*File:* SKILL.md:94 | *Source:* structure

Line 94 mentions "Use the songwriter's workshop voice" but this is the only style guidance and it appears mid-workflow.

*Action:* Move to a ## Communication Style section and add 2-4 more examples covering different interaction types.

### 2. Prompt Craft

**Agent Assessment:**
- Agent type: domain-expert
- Overview quality: appropriate
- Progressive disclosure: needs-extraction
- Persona context: appropriate
- Notes: Overview is concise and well-crafted. SKILL.md is monolithic at 312 lines. Reference documents are properly extracted but their content is partially duplicated inline (~240 tokens of redundancy). The songwriter's workshop persona voice is appropriate and not excessive.

**Prompt Health:** 0/1 prompts with config header | 0/1 with progression conditions | 0/1 self-contained

#### Medium

**Step 3 Transform contains dense domain knowledge that duplicates reference content**
*File:* SKILL.md:144 | *Source:* prompt-craft

Lines 159-217 contain detailed Suno-specific metatag behavior guidance that substantially overlaps with content already documented in references/metatag-reference.md. The same domain knowledge is loaded twice.

*Action:* Replace inline Suno behavior guidance in Step 3 with a mandatory reference load directive. Keep only transformation-specific procedural instructions.

**Duplicated scream bleed-through prevention guidance**
*File:* SKILL.md:163 | *Sources:* prompt-craft, agent-cohesion

Lines 167-170 describe scream bleed-through prevention. This exact guidance appears in references/metatag-reference.md lines 332-337. ~80 tokens of duplication, risks divergence.

*Action:* Remove inline bullet points from Step 3b; add a single reference line: "Apply scream bleed-through prevention per metatag-reference.md after any aggressive section."

**Duplicated line density as tempo control guidance**
*File:* SKILL.md:210 | *Sources:* prompt-craft, agent-cohesion

Lines 210-215 describe line density as tempo control. The same content appears in metatag-reference.md lines 292-317 with more depth. ~100 tokens of redundancy.

*Action:* Replace with reference directive. Keep only: "Use line density variation between sections for tempo contrast (see metatag-reference.md). Normalize syllable counts WITHIN sections, not across them."

**Duplicated ALL CAPS and parentheses guidance**
*File:* SKILL.md:216 | *Source:* prompt-craft

Lines 216-217 describe ALL CAPS as loudness ceiling and parentheses as backing vocals. Both topics covered in metatag-reference.md lines 274-290. ~60 tokens of redundancy.

*Action:* Remove inline guidance from Step 3d. The metatag reference is already mandated to be pre-loaded at Step 1.

#### Low

**Wall of text in Headless Output Contract area**
*File:* SKILL.md:33 | *Source:* prompt-craft

The pre-pass flagged a wall of text from lines 33-47. The JSON block is fenced, but surrounding context (lines 20-31) is a dense numbered list with nested bullets.

*Action:* No strict action required; the JSON block is already fenced. The surrounding content is dense but functionally appropriate.

**Genre-aware section length relaxation could be more concise**
*File:* SKILL.md:171 | *Source:* prompt-craft

The instruction to relax section length expectations for prog/metal/experimental genres is slightly verbose.

*Action:* Consider condensing to: "For prog/metal/experimental genres, relax section length expectations -- a 16-line verse is normal for these genres."

**Harmonized vocal style sweet spot duplicated**
*File:* SKILL.md | *Source:* agent-cohesion

The harmonized vocal sweet spot guidance appears in both SKILL.md Step 3b and metatag-reference.md Vocal Style Findings.

*Action:* Keep authoritative detail in reference, brief application note in SKILL.md.

### 3. Execution Efficiency

#### Low

**Transformation option validation could batch with analysis in headless mode**
*File:* SKILL.md:135 | *Source:* execution-efficiency

In headless mode, validate-options.py could be batched with the Step 1 analysis scripts when options are known upfront, saving one sequential tool call round-trip.

*Action:* In headless mode, batch validate-options.py with the Step 1 analysis scripts rather than running it separately in Step 2.

**lyrics-diff.py and assemble-summary.py could run in parallel**
*File:* SKILL.md:282 | *Source:* execution-efficiency

These are independent operations in Step 5 but the skill does not explicitly instruct parallel execution.

*Action:* Add explicit instruction to run lyrics-diff.py and assemble-summary.py in a single parallel batch.

### 4. Path & Script Standards

**Script Inventory:** 8 scripts (python: 8) | Missing tests: none

All critical and high path-standards findings are covered in the Truly Broken section above.

### 5. Agent Cohesion

**Cohesion Analysis:**

| Dimension | Score | Notes |
|-----------|-------|-------|
| Persona Alignment | strong | The workshop collaborator persona is thoroughly embodied -- informs design decisions like transformation menus, iteration coaching, and respecting creative ownership |
| Capability Completeness | mostly-complete | Core workflow is thorough. Gaps at edges: non-English support, version tracking, multi-song workflow |
| Redundancy Level | some-overlap | Three content areas duplicated between SKILL.md and metatag-reference.md |
| External Integration | intentional | Three external integrations (bmad-init, Style Prompt Builder, Feedback Elicitor) all serve the workflow. Functions standalone or as pipeline component |
| User Journey | complete-end-to-end | User can accomplish real work end-to-end with no dead ends. Headless mode enables programmatic orchestration |

**Consolidation Opportunities:**

1. **Scream bleed-through prevention** (SKILL.md Step 3b + metatag-reference.md): Keep detailed guidance in metatag-reference.md only; SKILL.md references it with a brief pointer.
2. **Line density as tempo control** (SKILL.md Step 3d + metatag-reference.md): Keep comprehensive multi-technique framework in metatag-reference.md; SKILL.md Step 3d focuses only on RA-specific application.
3. **Harmonized vocal sweet spot** (SKILL.md Step 3b + metatag-reference.md Vocal Style Findings): Same pattern -- authoritative detail in reference, brief application note in SKILL.md.

#### Medium

**No explicit multi-language lyric transformation guidance**
*File:* SKILL.md | *Source:* agent-cohesion

The skill claims structure tagging and chorus creation "work across languages" without language-specific guidance. For non-English users, the skill degrades without adapting.

*Action:* Add multi-language transformation guidance, or narrow the skill description to English-primary.

**No versioning or history tracking for iterative refinement loops**
*File:* SKILL.md | *Source:* agent-cohesion

No mechanism to track versions across multiple refinement passes. For a skill that supports iterative loops, this is a workflow gap.

*Action:* Add version tracking to songbook save -- append version number/timestamp, maintain changelog in frontmatter.

#### Low

**No guidance for collaborative or multi-song workflows**
*File:* SKILL.md | *Source:* agent-cohesion

No album mode or batch transformation capability. Edge case but relevant for the serious songwriter this skill targets.

*Action:* Add a note that for multi-song consistency, users should establish a band profile first. Future enhancement could support batch headless transformation.

**Creative Suggestions:**

1. **Emotional arc visualization could enhance the transformation preview** -- Present the emotional arc visually to help users understand WHY sections were placed where they were. Could be a simple text diagram showing energy flow across sections. *(agent-cohesion)*

2. **A/B variant generation could leverage Suno's inherent randomness** -- Offer to generate 2-3 metatag-varied versions of approved lyrics (same words, different delivery/energy tags) for structured variation rather than relying on Suno's randomness. *(agent-cohesion)*

3. **Manifest could expose transformation options as sub-capabilities** -- Exposing the seven transformation types as parameters in bmad-manifest.json would allow Mac to make more targeted invocations without parsing SKILL.md. *(agent-cohesion)*

### 6. Creative (Edge-Case & Experience Innovation)

**Agent Understanding:**
- **Purpose:** Transform poems, raw text, and rough lyrics into Suno-ready structured song lyrics with metatags, section architecture, and rhythmic consistency -- while preserving writer voice and intent
- **Primary User:** Songwriters and poets who want to convert existing text into songs via Suno AI, ranging from first-timers pasting a poem to experienced producers with band profiles
- **Key Assumptions:**
  - Users have source text to transform (not creating from scratch)
  - Users have access to Suno and understand its two-field input model
  - The scripts directory contains working Python scripts that produce reliable analysis
  - Band profiles exist in a predictable file location when referenced
  - English is the primary language for script-based analysis
  - Users complete the transformation in a single session or can re-invoke with saved songbook output

**Enhancement Findings:**

#### High Opportunity

**No graceful path for non-Latin script languages**
*File:* SKILL.md:68 | *Source:* enhancement-opportunities

For Mandarin, Japanese, or Arabic, syllable counting, rhyme detection, and cliche detection are fundamentally inapplicable. A user who says "yes, run the scripts anyway" gets misleading data.

*Action:* Add script-type detection in analyze-input.py (Latin vs CJK vs Arabic vs Cyrillic). Auto-skip inapplicable analyses and present the skip positively.

**Refinement Mode lacks feedback loop confirmation**
*File:* SKILL.md:96 | *Source:* enhancement-opportunities

When invoked via --headless:refine, there is no structured accounting of which adjustments were applied, partially applied, or skipped.

*Action:* Extend the Headless Output Contract with an `adjustments_applied` array mapping each input adjustment to its outcome.

**Compaction survival block emitted once but never refreshed after transformations**
*File:* SKILL.md:148 | *Source:* enhancement-opportunities

The compaction block captures initial state but diverges as transformations proceed. If compaction fires mid-refinement, the agent loses the current draft state.

*Action:* Re-emit updated compaction survival block after each refinement loop and after transformations that change section structure. Include a draft hash for drift detection.

#### Medium Opportunity

**Band profile file not found produces no defined recovery path**
*File:* SKILL.md:72 | *Source:* enhancement-opportunities

If the profile file doesn't exist, there's no guidance. A first-timer would hit a dead end.

*Action:* List available profiles, offer fuzzy matching, offer to proceed without a profile.

**Transformation menu could suggest combinations based on input analysis**
*File:* SKILL.md:124 | *Source:* enhancement-opportunities

The menu presents static default recommendations. The input analysis already knows whether the text has structure, rhyme patterns, and character count -- the menu could be personalized.

*Action:* Dynamically adjust defaults based on Step 1 analysis results with 1-sentence rationale per option.

**Presentation format lacks copy-ready block**
*File:* SKILL.md:259 | *Source:* enhancement-opportunities

The user's next action is to paste lyrics into Suno, but they must mentally separate lyrics from the surrounding summary.

*Action:* Add a clearly labeled "Copy-Ready Lyrics" section containing ONLY raw lyrics with metatags.

**Refinement loop lacks soft-gate elicitation**
*File:* SKILL.md:282 | *Source:* enhancement-opportunities

"Want to adjust anything?" doesn't guide the user toward what might need adjusting. A first-timer might not know how to articulate feedback.

*Action:* Offer 2-3 specific refinement suggestions based on quality check data.

**Handoff misses opportunity to generate starter style prompt snippet**
*File:* SKILL.md:296 | *Source:* enhancement-opportunities

The Lyric Transformer already knows genre, mood, energy arc, and vocal delivery cues -- it could generate a starter style prompt to save the user from re-explaining to the Style Prompt Builder.

*Action:* Generate a starter style prompt at Step 6 handoff that captures the musical decisions embedded in the transformed lyrics.

**File input validation not defined**
*File:* SKILL.md:68 | *Source:* enhancement-opportunities

No guidance for invalid file paths, empty files, binary files, or enormous files when accepting file path input.

*Action:* Add file input validation before passing to scripts: check exists, readable, text, under reasonable size.

**Skill assumes users understand Suno**
*File:* SKILL.md:10 | *Source:* enhancement-opportunities

The entire skill is built around Suno-specific concepts but never explains what Suno is.

*Action:* Add a brief "New to Suno?" detection in the greeting phase with a 30-second optional orientation.

**Metatag reference has no programmatic index for headless validation**
*File:* references/metatag-reference.md | *Source:* enhancement-opportunities

If validate-lyrics.py maintains its own hardcoded tag list, it will drift from the reference document.

*Action:* Extract a metatag-registry.json that both the reference doc and validate-lyrics.py consume as a single source of truth.

#### Low Opportunity

**Songbook save could capture the transformation journey**
*File:* SKILL.md:299 | *Source:* enhancement-opportunities

The save doesn't preserve original source text, analysis results, or refinement history.

*Action:* Extend songbook format to optionally include a transformation-log section.

**bmad-init fallback is silent -- degraded experience not characterized**
*File:* SKILL.md:52 | *Source:* enhancement-opportunities

When falling back, the user doesn't know WHY the greeting is generic or that features are missing.

*Action:* Briefly note: "I wasn't able to load your preferences, so I'll use defaults."

**Vocal delivery cue suggestions could use audio-imagination references**
*File:* SKILL.md:162 | *Source:* enhancement-opportunities

Abstract descriptions of vocal dynamics (whispered into belted) could reference well-known songs for visceral understanding.

*Action:* When suggesting vocal delivery cues, offer genre-appropriate references.

**Character budget warning doesn't account for metatag overhead**
*File:* SKILL.md:240 | *Source:* enhancement-opportunities

The 3000-char budget check doesn't distinguish between lyric content and metatag overhead.

*Action:* Break out character budget display: "Lyrics: X chars / Metatags: Y chars / Total: Z/3000."

**Top Insights:**

1. **The skill's greatest untapped opportunity is bridging the gap between Lyric Transformer output and Style Prompt Builder input.** By the time the Lyric Transformer finishes, it knows everything needed to generate a starter style prompt. Currently the user has to re-explain all of this to the Style Prompt Builder. *Action:* Generate a starter style prompt at Step 6 handoff.

2. **Compaction survival is designed but fragile under iteration.** The block is emitted once and never updated. In a skill designed for iterative refinement, a stale compaction block could cause the agent to lose 3-4 rounds of refinement work. *Action:* Re-emit after every state-changing operation with a draft hash.

3. **Script failure resilience is the single biggest hostile-environment gap.** The skill depends on 8 Python scripts. If any fails, there is no defined fallback behavior. The LLM can perform most analyses at lower precision. *Action:* Add a fallback clause for each script invocation with LLM-based degradation.

---

## User Journeys

*How different user archetypes experience this agent:*

### First-Timer

A poet who heard they can turn poems into songs with AI. They paste their poem and are guided through transformation options. The experience is rich but potentially overwhelming -- seven transformation codes, mutual exclusions, and Suno-specific terminology. The greeting is warm, the capture-creative-context step draws out their intent, and the impact preview in Step 3c is genuinely helpful.

**Friction Points:**
- Transformation menu presents 8 options with codes -- intimidating for someone who just wants "make my poem a song"
- No explanation of what Suno is or how the lyrics field works until Step 6 handoff
- Technical terms (metatags, descriptor tags, syllable normalization) are not contextualized for non-musicians
- If bmad-init fails silently, user doesn't know features are degraded

**Bright Spots:**
- Creative context capture lets them share emotional intent naturally
- Impact preview shows structural changes visually before applying
- Default recommendations (ST + CC + RA + CD) are sensible -- user can just say "yes"
- Word Fidelity Mode gives anxious writers a safety net

### Expert

An experienced Suno user with a band profile who knows exactly which transformations they want. They can specify options upfront, reference their profile, and skip the discovery phase. The headless mode lets them bypass all interaction. The refinement loop lets them iterate quickly.

**Friction Points:**
- Cannot skip the analysis presentation in Step 1 -- expert already knows their text
- No "fast mode" that accepts all inputs in the first message and jumps to output
- Refinement requires re-stating context that the skill should remember from the initial pass

**Bright Spots:**
- Headless mode with sub-modes is excellent for power users
- Band profile integration preserves voice constraints automatically
- Script-based validation catches issues the expert might miss
- Songbook save preserves work for future reference

### Confused

A user who was told "use the Lyric Transformer" but actually wants to write a song from scratch, wants an instrumental track, or wants to edit an existing Suno generation. The intent check in Step 1 catches the "no source text" case and redirects.

**Friction Points:**
- User with existing Suno output wanting refinement is treated as a new transformation rather than a revision
- Redirect to other skills assumes the user knows what those skills are
- No "I'm lost, what can you actually do?" help command

**Bright Spots:**
- Intent check catches the most common mismatch (no source text) early
- Instrumental-only redirect is thoughtful and offers an alternative

### Edge-Case

A user with technically valid but unexpected input: a 5000-word short story, song lyrics in Mandarin, a poem with existing but incorrect metatags, or text that is 90% stage directions.

**Friction Points:**
- Very long input (well over 3000 chars) isn't flagged until after analysis -- should warn upfront
- Mixed content (stage directions + lyrics) would confuse the analyzer
- Existing but malformed metatags (typos like [Vrese]) are not explicitly handled
- Non-Latin script languages get unreliable script output with no auto-skip

**Bright Spots:**
- Pre-structured input detection adapts defaults intelligently
- Character budget tracking prevents silent Suno truncation
- Non-English warning is honest about script limitations

### Hostile Environment

Scripts fail to execute, band profile directory doesn't exist, bmad-init is unavailable, or context compaction fires mid-transformation.

**Friction Points:**
- No defined fallback when any of the 8 scripts fail
- Compaction survival block is write-once, goes stale during refinement loops
- No offline mode -- web search mandate for Suno claims fails without connectivity
- If band profile YAML is malformed, no error handling is specified

**Bright Spots:**
- bmad-init fallback is clean and non-blocking
- Compaction survival block exists at all -- many skills don't consider this
- Research mandate acknowledges uncertainty when search is unavailable

### Automator

A CI pipeline or another skill (like the Feedback Elicitor) invoking the Lyric Transformer headlessly. The headless mode is exceptionally well-designed.

**Friction Points:**
- No error schema in the headless output contract -- what does failure look like?
- Refinement mode adjustments_applied outcomes aren't reported back
- No way to pass communication_language or document_output_language as headless parameters

**Bright Spots:**
- Three headless sub-modes cover all programmatic use cases
- Adjustment spec from Feedback Elicitor is a clean inter-skill protocol
- validate-options.py prevents invalid transformation combinations programmatically
- Output contract includes original_hash for change tracking

---

## Autonomous Readiness

- **Overall Potential:** headless-ready
- **HITL Interaction Points:** 5
- **Auto-Resolvable:** 4
- **Needs Input:** 1
- **Suggested Output Contract:** Already defined: JSON with transformed_lyrics, transformation_summary, cliche_report, validation_result, and original_hash
- **Required Inputs:** source text (required), transformation options (defaults available: ST+CC+RA+CD), band profile name (optional), song direction/genre (optional), language (optional, defaults to English)
- **Notes:** This skill is already headless-ready with a well-designed output contract and three sub-modes. The only HITL point that truly requires human input is transformation option selection when the user wants non-default options. The main enhancement would be adding error reporting to the headless contract.

---

## Script Opportunities

**Existing Scripts:** validate-lyrics.py, cliche-detector.py, syllable-counter.py, validate-options.py, section-length-checker.py, analyze-input.py, lyrics-diff.py, assemble-summary.py

**Compaction state summary could be script-assembled** (SKILL.md:148)
Determinism: certain | Savings: ~150 tokens | Complexity: trivial
All values (source_hash, character_budget, transform codes) are deterministic and available from existing script outputs.
*Action:* Create build-compaction-state.py that accepts existing script outputs and emits the formatted comment block.

**Character budget mid-step check is redundant with validation** (SKILL.md:238)
Determinism: certain | Savings: ~100 tokens | Complexity: trivial
validate-lyrics.py already checks character count. The mid-step instruction asks the LLM to count characters.
*Action:* Add --quick-charcount mode to validate-lyrics.py, or rely on Step 4 validation and remove the mid-step instruction.

**Headless output contract JSON is mostly deterministic data** (SKILL.md:39)
Determinism: high | Savings: ~300 tokens | Complexity: moderate
Most fields are deterministic from script outputs. Only transformed_lyrics requires LLM output.
*Action:* Extend assemble-summary.py to produce the complete headless output contract JSON. LLM provides only the transformed_lyrics string.

**Transformation Summary presentation block from script outputs** (SKILL.md:260)
Determinism: certain | Savings: ~200 tokens | Complexity: trivial
assemble-summary.py already exists and partially covers this.
*Action:* Verify assemble-summary.py output matches Step 5 template exactly. If so, update Step 5 to just invoke and present its output.

**LLM computes original_hash that a script could provide** (SKILL.md:46)
Determinism: certain | Savings: ~50 tokens | Complexity: trivial
LLMs cannot reliably compute sha256 hashes.
*Action:* Add --include-hash flag to analyze-input.py.

**Exclamation points, ALL CAPS, and parenthetical detection** (SKILL.md:167, 217)
Determinism: certain | Savings: ~120 tokens | Complexity: trivial
These are simple regex operations the LLM should not spend tokens finding.
*Action:* Extend validate-lyrics.py with specific findings for !, ALL CAPS, and unintentional parenthetical usage.

**Songbook save file could be script-generated** (SKILL.md:299)
Determinism: high | Savings: ~100 tokens | Complexity: moderate
All frontmatter fields except "notes" are deterministic.
*Action:* Create save-to-songbook.py that generates the file with proper YAML frontmatter.

**Token Savings:** ~1,020 tokens estimated per invocation | Highest value: Extend assemble-summary.py for complete headless output contract (~300 tokens) | Prepass opportunities: 2 (hash computation, compaction state block)

---

## Quick Wins (High Impact, Low Effort)

| Issue | File | Effort | Impact |
|-------|------|--------|--------|
| Add `./` prefix to all 23 bare internal paths | SKILL.md | Low (search-replace) | High -- fixes path ambiguity |
| Rename ambiguous variable `l` to `line` in 3 scripts | analyze-input.py, syllable-counter.py, validate-lyrics.py | Low | High -- fixes lint errors |
| Remove 3 unused variable assignments | syllable-counter.py:142, validate-lyrics.py:81,161 | Low | Medium -- cleans lint |
| Remove duplicated domain knowledge from Step 3 (~240 tokens) | SKILL.md:159-217 | Low | Medium -- reduces tokens and divergence risk |
| Add --include-hash to analyze-input.py | analyze-input.py | Low | Medium -- LLMs cannot compute sha256 |
| Add transparent fallback message for bmad-init failure | SKILL.md:52 | Low | Medium -- better first-timer experience |

---

## Optimization Opportunities

**Token Efficiency:**
Approximately 240 tokens of domain knowledge are duplicated between SKILL.md Step 3 and metatag-reference.md (scream bleed-through ~80, line density ~100, ALL CAPS/parentheses ~60). Removing these inline duplicates in favor of reference directives is the lowest-effort token savings available. Additionally, ~1,020 tokens per invocation could be saved by extending scripts to handle deterministic assembly tasks (headless output contract, presentation block, compaction state, hash computation). The highest-value script extension is making assemble-summary.py produce the complete headless output contract (~300 tokens/invocation).

**Performance:**
The skill already parallelizes its two main independent operation groups well. Two incremental improvements: batch validate-options.py with Step 1 analysis in headless mode (saves one round-trip), and explicitly batch lyrics-diff.py with assemble-summary.py in Step 5. Extracting Step 3 (Transform) into a capability prompt file would also improve performance by reducing the initial context load.

**Maintainability:**
The three content duplications between SKILL.md and metatag-reference.md are the primary maintenance risk -- updates to one location may not propagate. Extracting a metatag-registry.json as a single source of truth for both the reference document and validate-lyrics.py would prevent tag list drift. Adding the three missing agent sections (Identity, Communication Style, Principles) would consolidate scattered behavioral guidance into maintainable locations.

---

## Recommendations

1. **Add the three missing required sections (Identity, Communication Style, Principles)** -- These are the structural foundation for consistent agent behavior. The content already exists scattered throughout the skill; it just needs consolidation into dedicated sections.

2. **Fix the two {project-root} non-_bmad path violations and add ./ prefix to all 23 bare internal paths** -- These are the most pervasive standards issues and the ./ prefix fix is a simple search-replace operation.

3. **Remove duplicated domain knowledge from Step 3 and extract it into a capability prompt file** -- This addresses both the monolithic SKILL.md issue and the ~240 tokens of redundancy, while improving progressive disclosure.

4. **Fix Python lint issues across the three scripts** -- 10 lint issues including ambiguous variable names, unused variables, and an f-string without placeholders. All are trivial to fix.

5. **Define script failure fallback behavior and refresh compaction survival block during iteration** -- These are the two highest-risk resilience gaps for real-world usage where conversations run long or environments are imperfect.
