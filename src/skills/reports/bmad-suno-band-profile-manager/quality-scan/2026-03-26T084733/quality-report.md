# Quality Report: bmad-suno-band-profile-manager

**Scanned:** 2026-03-26T08:47:33
**Skill Path:** /home/zarlor/bmm/_bmad-output/bmad-suno-band-manager-module/src/skills/bmad-suno-band-profile-manager
**Report:** /home/zarlor/bmm/_bmad-output/bmad-suno-band-manager-module/src/skills/reports/bmad-suno-band-profile-manager/quality-scan/2026-03-26T084733/quality-report.md
**Performed By** QualityReportBot-9001

## Executive Summary

- **Total Issues:** 34
- **Critical:** 0 | **High:** 28 | **Medium:** 4 | **Low:** 2
- **Overall Quality:** Good
- **Overall Cohesion:** cohesive
- **Craft Assessment:** Well-crafted domain expert skill with strong Overview, appropriate progressive disclosure, and correct intelligence placement. Token usage is efficient with no waste patterns.

This agent embodies a music producer's assistant persona that is exceptionally well-matched to its capabilities, managing persistent band identity profiles as the sonic DNA for Suno music generation. The architecture is strong -- comprehensive headless mode, well-designed operation routing, and deep Suno platform knowledge baked into the workflows. The most significant finding is that 21 bare skill-internal paths lack the `./` prefix required by path standards, which is a high-severity but mechanical fix. Structurally, three missing agent sections (Identity, Communication Style, Principles) weaken behavioral consistency for what is fundamentally a conversational-discovery skill.

### Issues by Category

| Category | Critical | High | Medium | Low |
|----------|----------|------|--------|-----|
| Structure & Capabilities | 0 | 4 | 2 | 1 |
| Prompt Craft | 0 | 0 | 0 | 2 |
| Execution Efficiency | 0 | 0 | 1 | 3 |
| Path & Script Standards | 0 | 24 | 0 | 0 |
| Agent Cohesion | 0 | 0 | 2 | 3 |
| Creative | — | — | — | — |

---

## Agent Identity

- **Persona:** A music producer's assistant who understands sonic identity, vocal direction, and writing voice. Meets users where they are -- from deep musical vocabulary to beginners who know what they like but cannot name it.
- **Primary Purpose:** Manage persistent band identity profiles that define consistent sonic and lyrical identity for AI-assisted music creation via Suno
- **Capabilities:** 8

---

## Strengths

*What this agent does well -- preserve these during optimization:*

**Domain Knowledge & Persona**
- **Exceptional persona-capability alignment** (agent-cohesion, prompt-craft): The "music producer's assistant" persona is perfectly matched to every capability offered. Every operation -- create, edit, duplicate, analyze voice, health check -- is exactly what a producer's assistant would do. The conversational discovery approach fits the persona naturally.
- **Thoughtful Suno-specific domain knowledge** (agent-cohesion): The skill bakes in real Suno platform knowledge: negative prompts don't work well (so exclusions get translated to positive language), front-load style prompts in the first 200 characters, persona era-anchoring behavior, Audio Influence effective ranges. This makes the agent genuinely useful rather than a generic YAML editor.
- **Creative idea capture reflects persona** (prompt-craft): The instruction to silently note song concepts and lyric fragments during discovery, then offer to save them, is exactly the kind of judgment-enabling context that makes agents feel intelligent rather than mechanical.
- **Health Check uses coaching tone** (prompt-craft): Frames quality gaps as "friendly recommendations, not failures" with encouraging language, matching the producer's assistant persona and the theory-of-mind guidance in the Overview.

**Architecture & Design**
- **Comprehensive headless mode with structured JSON responses** (structure, prompt-craft): Well-defined subcommands (create, validate, load, edit, delete, duplicate, list) with documented return JSON shapes. Clean interactive/headless separation supports both human and automated use.
- **Complete CRUD lifecycle with meaningful extras** (agent-cohesion): Full profile lifecycle plus duplicate and health check. The duplicate operation supports real workflows (versioning, side projects, sound evolution). The health check goes beyond validation to assess quality.
- **Dual-mode design is architecturally sound** (agent-cohesion): Supporting both conversational and headless modes enables clean integration with automated pipelines and orchestrating agents.
- **Operation routing table is clear and comprehensive** (structure, prompt-craft): Maps triggers to routes cleanly, includes handling for unclear intent and wrong-skill invocation with helpful redirect.

**Prompt Craft**
- **Well-crafted Overview with mission, domain context, and design rationale** (prompt-craft, structure): Establishes persona, domain framing (band profile as brand book), theory of mind (users range from musicians to beginners), and design rationale (conversation over form-filling). All load-bearing, nothing extraneous.
- **Good progressive disclosure** (prompt-craft): Profile schema (109 lines) and tier feature matrix (78 lines) correctly placed in references/ and loaded on demand. SKILL.md stays focused on workflow.
- **Description follows two-part format with trigger phrases** (structure): Correct pattern with summary sentence followed by "Use when" clause with quoted trigger phrases for reliable activation.
- **Activation sequence with graceful fallback** (structure): Correctly loads config first, then greets, then detects operation. The bmad-init fallback behavior is well-designed for resilience.
- **Progressive disclosure in profile creation flow** (agent-cohesion): 12-step discovery is well-sequenced -- identity to sound to technical settings to enrichment. The "Anything else?" gate respects user autonomy.

**Execution Efficiency**
- **Edit Profile explicitly batches parallel reads** (execution-efficiency): Model pattern for efficient tool call batching.
- **Analyze Writer Voice prescribes parallel file reading** (execution-efficiency): Correctly batches multiple file reads with "read all sample files in a single parallel batch."
- **Good script delegation for deterministic operations** (prompt-craft): Correctly delegates validation, listing, tier feature lookup, filename derivation, and diff comparison to scripts, reserving the agent for conversational discovery, voice analysis, and judgment calls.
- **Tier drift detection is a smart proactive check** (prompt-craft): Load Profile checks for tier drift between stored profile and current user tier -- forward-thinking data staleness prevention.

---

## Truly Broken or Missing

*Issues that prevent the agent from working correctly:*

### Missing Agent Structural Sections

**Missing ## Identity section** | SKILL.md:1 | HIGH | Source: structure
The SKILL.md has no dedicated Identity section. The Overview contains identity-like content ("Act as a music producer's assistant who understands sonic identity, vocal direction, and writing voice"), but this is not in the canonical location. Without a dedicated Identity section, persona priming is weaker and less explicit.
*Action:* Add a ## Identity section after Overview with a clear one-sentence persona statement.

**Missing ## Communication Style section** | SKILL.md:1 | HIGH | Source: structure
No Communication Style section exists. This skill involves extensive conversational discovery with users ranging from experienced musicians to complete beginners. Without style guidance and concrete examples, the agent's tone will be inconsistent across interactions.
*Action:* Add a ## Communication Style section with 3-5 concrete examples showing how to adapt language for musician vs. beginner users.

**Missing ## Principles section** | SKILL.md:1 | HIGH | Source: structure
No Principles section exists. This skill makes many judgment calls (how much to push for detail, when to accept vague answers, how to handle reference tracks for unknown artists). Without guiding principles, behavior in ambiguous situations will be inconsistent.
*Action:* Add a ## Principles section with domain-specific decision frameworks.

### README.md Issues

**No progression condition keywords in README.md** | README.md:64 | HIGH | Source: structure
The README.md prompt has no progression conditions. If this is a multi-stage prompt, missing progression logic means the agent cannot determine when to advance.
*Action:* Add progression conditions if it represents a staged workflow, or restructure as a single-pass reference if progression is not applicable.

### Path Standards Violations

**Prompt file at skill root: README.md** | README.md | HIGH | Source: path-standards
All progressive disclosure content must be in ./references/ -- only SKILL.md belongs at root.
*Action:* Move README.md to references/README.md

**Parent directory reference (../) found** | README.md:63 | HIGH | Source: path-standards
Fragile parent path reference that breaks with reorganization.
*Action:* Replace with a stable reference path.

**Bare skill-internal paths without ./ prefix** | Multiple files | HIGH | Source: path-standards
21 instances across SKILL.md and references/tier-features.md where internal paths like `references/profile-schema.md` and `scripts/validate-profile.py` lack the `./` prefix. Without the prefix, these paths are ambiguous between skill-internal and project-root paths.

| File | Lines |
|------|-------|
| SKILL.md | 62, 71, 86, 86, 91, 95, 101, 105, 109, 111, 113, 113, 117, 153, 169, 170, 171, 172, 173 |
| README.md | 59 |
| references/tier-features.md | 5 |

*Action:* Prefix all skill-internal paths with `./` (e.g., `./references/profile-schema.md`, `./scripts/validate-profile.py`).

### Script Lint Issues

**[F401] `os` imported but unused** | scripts/list-profiles.py:19 | HIGH | Source: scripts
*Action:* Remove unused import: `os`

---

## Detailed Findings by Category

### 1. Structure & Capabilities

**Agent Metadata:**
- Sections found: Overview, Activation Mode Detection, On Activation, Workflow Operations, Post-Operation Flow, Scripts
- Capabilities: 8
- Memory sidecar: No
- Headless mode: Yes (7 subcommands: create, validate, load, edit, delete, duplicate, list)
- Structure assessment: Strong operational design with comprehensive workflows. Missing three required structural sections (Identity, Communication Style, Principles) which weakens behavioral consistency for a conversational-discovery skill.

#### Medium

**Name does not follow agent naming convention** | SKILL.md:1 | Source: structure
Name "bmad-suno-band-profile-manager" does not follow the expected bmad-{code}-agent-{name} pattern. This may affect discoverability and consistency with other agents in the ecosystem.
*Action:* Consider renaming to follow the pattern, e.g., bmad-suno-agent-band-profile-manager, if this is intended to be an agent-style skill.

**No config header in README.md** | README.md:1 | Source: structure
The README.md prompt file lacks a config header declaring language variables.
*Action:* Add a config header if it uses language variables, or verify it does not need one.

#### Low

**Overview is dense -- consider extracting domain context** | SKILL.md:10 | Source: structure
The Overview packs identity, domain context, design rationale, and scope into a single dense section. While content is high quality, this front-loads tokens that may not be needed on every activation.
*Action:* Consider moving domain context and design rationale to a references/ file, keeping Overview focused on purpose and scope.

### 2. Prompt Craft

**Agent Assessment:**
- Agent type: domain-expert
- Overview quality: appropriate
- Progressive disclosure: good
- Persona context: appropriate
- SKILL.md is well-crafted at 174 lines / ~3627 tokens. Operations are inline but appropriately brief. Schema and tier data correctly extracted to references/. No waste patterns detected. Two dense instruction blocks could benefit from structural breakup but content is all load-bearing.

#### Low

**Dense multi-concern instruction in reference tracks discovery step** | SKILL.md:69 | Source: prompt-craft
Line 69 packs three distinct concerns into a single step: prompting for reference tracks, sonic decomposition instructions, and a research mandate with fallback behavior. At ~80 words, this is the densest single instruction. The agent may lose the research mandate buried mid-paragraph.
*Action:* Break into sub-bullets: one for the prompt and decomposition, one for the research mandate with its fallback.

**Exclusion defaults step mixes user-facing guidance with system behavior** | SKILL.md:75 | Source: prompt-craft
Step 9 combines the discovery question, a technical explanation of Suno's negative prompt limitation, how the Style Prompt Builder handles it, and a scripted user message.
*Action:* Separate the user-facing message into a quoted block or sub-bullet for clarity.

### 3. Execution Efficiency

#### Medium

**Create Profile and Health Check lack explicit batching guidance** | SKILL.md:62 | Source: execution-efficiency
Create Profile loads profile-schema.md without specifying batching with other reads. Health Check similarly reads a profile without batching the schema load. Only Edit Profile has explicit parallel-batch guidance.
*Action:* Add parallel-batch instructions to Create Profile and Health Check operations.

#### Low

**Health Check could batch validate-profile.py and profile reading** | SKILL.md:149 | Source: execution-efficiency
The script run and profile file read are independent and could execute in a single parallel batch, saving one round-trip.
*Action:* Add instruction to batch the profile read and validate-profile.py run.

**Load Profile sequential check-then-read could be a single read** | SKILL.md:99 | Source: execution-efficiency
Load Profile first runs list-profiles.py --check to verify existence, then reads the profile. Since a failed file read produces a clear error, the existence check is redundant for unambiguous names.
*Action:* Consider reading the profile directly and falling back to list-profiles.py only when the read fails or name is ambiguous.

**Edit Profile post-edit validation and diff could be batched** | SKILL.md:113 | Source: execution-efficiency
After editing, validate-profile.py and diff-profiles.py run sequentially. Both could run in parallel since diff does not depend on validation passing.
*Action:* Add instruction to batch both scripts after applying edits.

### 4. Path & Script Standards

**Script Inventory:** 4 scripts (python: 4) | Missing tests: none

All high-severity path and script findings are listed in the Truly Broken section above. The path-standards scanner found 23 high-severity issues:
- 1 structural issue (README.md at skill root)
- 1 parent directory reference (../)
- 21 bare internal paths without ./ prefix
- 1 lint issue (unused import)

These are mechanical fixes -- prefix internal paths with `./`, move README.md to references/, remove the unused import.

### 5. Agent Cohesion

**Cohesion Analysis:**

| Dimension | Score | Notes |
|-----------|-------|-------|
| Persona Alignment | strong | Producer's assistant persona is an excellent fit. Every capability serves the core mission. Conversational discovery, reference track decomposition, and writer voice analysis all feel natural to the persona. |
| Capability Completeness | mostly-complete | Core CRUD lifecycle fully covered with thoughtful extras. Gaps in secondary workflows: export/share, side-by-side comparison, archive/soft-delete. None are blocking. |
| Redundancy Level | clean | Capabilities are well-integrated within a single skill. Manifest lists analyze-writer-voice and health-check separately for routing, which is reasonable. No real consolidation needed. |
| External Integration | intentional | References bmad-init, Style Prompt Builder, Lyric Transformer, and Feedback Elicitor. Dependency direction is clear (profile manager is upstream). Wrong-skill redirect shows ecosystem awareness. |
| User Journey | complete-end-to-end | Users can create, refine, health-check, analyze voice, duplicate, and manage the full lifecycle. Post-operation flow keeps sessions alive. Only friction: wrong-skill redirect lacks concrete invocation path. |

**Consolidation Opportunities:**

The manifest lists analyze-writer-voice, health-check, and manage-profiles as separate capabilities. From a cohesion standpoint these are sub-operations of profile management, not independent capabilities. The current structure is acceptable if the orchestrating agent benefits from granular capability declarations.

#### Medium

**Reference track research mandate may fail silently without web search** | SKILL.md:69 | Source: agent-cohesion, enhancement-opportunities
The Create Profile flow requires web search to verify artist/song sonic characteristics, with a fallback to asking the user. However, the skill has no way to detect whether search is available. If it fails, the user experience degrades without explanation. The user also does not know the decomposition is based on their description rather than verified data.
*Action:* Add an explicit check: "If web search is unavailable, tell the user: I cannot verify reference tracks right now, so I will work from your descriptions and my training data. Double-check the reference breakdown I provide."

**No export or share capability for profiles** | SKILL.md | Source: agent-cohesion
Users can create, edit, and manage profiles but have no explicit workflow for sharing a profile with collaborators or exporting for backup.
*Action:* Consider adding an Export operation that produces a clean, shareable version of a profile. Low priority since YAML is already human-readable.

#### Low

**No import capability for profiles from external sources** | SKILL.md | Source: agent-cohesion
No explicit import operation for bringing in a profile someone else shared. Headless:create partially covers this.
*Action:* A dedicated Import operation could validate, adapt tier settings, and resolve conflicts. Low priority.

**Wrong-skill redirect mentions "Band Manager agent" without clear invocation path** | SKILL.md:56 | Source: agent-cohesion
When a user asks to "make a song," the redirect identifies the right destination without providing the route. The user may not know how to invoke those skills.
*Action:* Include a concrete invocation example in the redirect guidance.

**Capability decomposition in manifest could be consolidated** | bmad-manifest.json | Source: agent-cohesion
The manifest lists three capabilities that are sub-operations of profile management. Not a real problem, but a structural observation.
*Action:* Consider consolidating if the manifest schema does not benefit from granular declarations.

**Creative Suggestions:**

**Profile comparison capability could enhance sound evolution workflows** | references/profile-schema.md | Source: agent-cohesion, enhancement-opportunities
The diff-profiles.py script exists but there is no user-facing "Compare" operation. Users who duplicate profiles for sound evolution would benefit from side-by-side comparison. Frame it as "How has your sound evolved?" rather than a dry diff.

**Profile archiving could prevent accidental loss** | SKILL.md | Source: agent-cohesion, enhancement-opportunities
Delete is permanent. For users experimenting with sound evolution, an archive operation that moves profiles to an "archived" subfolder would be safer. Consider docs/band-profiles/.archive/ with restore capability.

**Generation learnings could be surfaced proactively during profile load** | SKILL.md | Source: agent-cohesion
The schema includes generation_learnings and known_limitations, but Load Profile displays them passively. Surfacing them proactively ("Heads up: last time you found that metal in the style prompt triggers screaming") would make the agent feel like it has memory.

### 6. Creative (Edge-Case & Experience Innovation)

**Agent Understanding:**
- **Purpose:** Manages persistent band identity profiles -- the sonic DNA of musical projects -- that serve as the foundation for downstream Suno music generation skills (Style Prompt Builder, Lyric Transformer, Feedback Elicitor). Handles full CRUD lifecycle plus writer voice analysis and profile health assessment.
- **Primary User:** Musicians and music producers using Suno AI for music creation, ranging from beginners who "know what they like but cannot name it" to experienced producers with precise sonic vocabulary. Also serves automated pipelines via headless mode.
- **Key Assumptions:**
  - Users can articulate or discover their sonic preferences through conversation
  - One profile maps to one musical project identity
  - Python scripts and bash execution are available in the runtime environment
  - Users know their Suno tier and model preference
  - Profile creation happens in a single session without interruption
  - Web search availability for reference track verification
  - Users will invoke Health Check as a separate operation rather than expecting quality assurance at creation time

**Enhancement Findings:**

#### High Opportunity

**Context compaction during long Create Profile discovery could lose accumulated creative details** | SKILL.md | Source: enhancement-opportunities
The 12-step conversational discovery accumulates nuanced creative preferences, reference track decompositions, and captured side-ideas. In a long conversation with a verbose user, context compaction could silently drop critical details. The skill has no mechanism to checkpoint partial state.
*Action:* Add progressive assembly: after every 3-4 discovery steps, assemble the profile YAML so far into a fenced block. Structured YAML survives compaction better than scattered conversational fragments.

**No capture-don't-interrupt mechanism for out-of-scope creative input during discovery** | SKILL.md | Source: enhancement-opportunities
The skill says to "silently note" song concepts and lyric fragments but does not say how. Creative users in flow state will share genre tangents, production experiments, and half-formed ideas.
*Action:* Add a "Creative Scratch Pad" instruction: maintain a running list of non-profile items, surface at session end. Make the capture mechanism explicit.

**Reference track web search fallback creates a silent quality gap** | SKILL.md | Source: enhancement-opportunities
When web search is unavailable, the decomposition is based on unverified user descriptions. A first-timer might assume the agent independently verified sonic characteristics. This matters because decomposition flows into style prompts that Suno interprets literally.
*Action:* Add transparency instruction for the no-search fallback so users know to double-check the reference breakdown.

**No parallel review lenses before finalizing a new profile** | SKILL.md | Source: enhancement-opportunities
After the 12-step discovery, subtle issues (vague style baseline, contradictory exclusions) are easy to miss. The Health Check exists separately but is never suggested during creation.
*Action:* Before presenting the final profile, run an inline mini-health-check: assess style_baseline specificity, vocal direction depth, and exclusion/genre consistency. Catch quality issues at creation time.

#### Medium Opportunity

**Expert user forced through 12-step discovery even when they already know their sound** | SKILL.md | Source: enhancement-opportunities
A musician who knows exactly what they want is forced through a step-by-step interview. Headless mode requires YAML knowledge. No middle ground for the expert interactive user.
*Action:* Add fast-track create detection: if the user's initial message contains enough detail for most required fields, skip the interview, ask only about genuinely missing fields, and go straight to review.

**Edit operation with broad natural language has no guardrails against cascading changes** | SKILL.md | Source: enhancement-opportunities
"Make it more aggressive" could touch genre, mood, vocal energy, vocal delivery, style_baseline, exclusion_defaults, and creativity_default all at once. The diff shows changes, but a user who meant "just the vocal delivery" might not catch unwanted side effects.
*Action:* Add a scope clarification step for broad requests affecting 3+ fields before applying.

**Skill assumes 1:1 profile-to-project mapping, but users may want context-dependent profiles** | SKILL.md | Source: enhancement-opportunities
Real musicians want variations (live acoustic vs. full production vs. singles vs. albums). Duplicate creates independent profiles with no relationship tracking.
*Action:* Consider adding an optional "parent" or "lineage" field to the schema and have list-profiles.py group by lineage.

**Success amnesia -- user has a YAML file but no clear next step** | SKILL.md | Source: enhancement-opportunities
After creating a profile, the post-operation flow keeps the user in profile-management land. The real next step is to USE the profile -- build a style prompt, write lyrics, generate a song.
*Action:* After saving, add a contextual suggestion bridging to Style Prompt Builder or Lyric Transformer.

**No soft-gate elicitation at natural creative boundaries** | SKILL.md | Source: enhancement-opportunities
The "Anything else to add, or move on?" gate is applied uniformly. Some steps are natural creative expansion points (reference tracks, vocal direction) where tailored prompts would draw out richer input.
*Action:* At the three richest junctions, replace the generic gate with more evocative prompts.

**Headless Analyze Writer Voice is not supported but could be** | SKILL.md | Source: enhancement-opportunities
Writer voice analysis -- one of the most valuable capabilities -- has no headless path. The analysis is algorithmic and natural for headless execution.
*Action:* Add --headless:analyze-voice mode that accepts file paths or text samples and returns JSON with extracted voice dimensions.

**Confused user redirect is informational but not emotionally warm** | SKILL.md | Source: enhancement-opportunities
A user who excitedly says "let's make some music!" gets a corrective explanation instead of excitement-matching guidance.
*Action:* Reframe to match the user's energy and convert the dead-end redirect into an on-ramp for profile creation.

**Band Identity Card is single-use** | SKILL.md | Source: enhancement-opportunities
The identity card -- the most emotionally resonant artifact -- is generated once at creation and never seen again. Loading shows structured sections. Editing does not regenerate it.
*Action:* Store the identity card in the profile YAML, regenerate on significant edits, display as header when loading.

#### Low Opportunity

**No profile comparison view for evolution tracking** | SKILL.md | Source: enhancement-opportunities
The diff-profiles.py script exists but is only invoked during edit confirmation. No user-facing "compare two profiles" operation.
*Action:* Add a Compare operation using diff-profiles.py with human-readable sonic difference framing.

**Delete operation has no undo or soft-delete** | SKILL.md | Source: enhancement-opportunities
Permanent deletion behind a single yes/no gate for a profile that took 20 minutes to create.
*Action:* Move deleted profiles to .archive/ directory instead of permanent deletion.

**Skill assumes user knows their Suno tier** | SKILL.md | Source: enhancement-opportunities
First-timers may not know their tier or understand model differences.
*Action:* Add a detection helper: "Not sure which tier? Check your Suno account settings, or tell me what features you see."

**Validation script dependency means opaque failure if Python/scripts are missing** | SKILL.md | Source: enhancement-opportunities
Every write operation depends on validate-profile.py. A broken Python environment effectively bricks the skill.
*Action:* Add graceful degradation: basic inline validation when scripts fail, with a warning to run full validation when possible.

**Top Insights:**

1. **Profile creation is a high-stakes single-session artifact with no compaction protection.** A 12-step conversational discovery that accumulates nuanced creative preferences is exactly the kind of long interaction where context compaction silently destroys value. The profile is assembled at the end from conversational fragments, not progressively checkpointed.
   *Action:* Add progressive YAML assembly checkpoints every 3-4 steps during Create Profile discovery.

2. **The Band Identity Card is the most emotionally resonant artifact this skill produces, and it is single-use.** It captures the soul of a band in 3-4 sentences -- far more evocative than reading YAML fields. But it is generated once and never seen again.
   *Action:* Store in profile, regenerate on significant edits, display as header on load. Make it the face of the profile.

3. **Expert users have no fast-track interactive path between "step-by-step interview" and "write raw YAML."** The skill correctly serves beginners with guided discovery and automators with headless YAML mode. But the expert interactive user falls through the gap.
   *Action:* Add fast-track detection at the start of Create Profile: if the initial message is information-rich, extract what you can and skip to review.

---

## User Journeys

*How different user archetypes experience this agent:*

### First-Timer

A new Suno user excited to make music invokes this skill. If they say "make music" they get redirected (potentially deflating). If they correctly ask to create a profile, they enter a thorough 12-step guided discovery that is well-structured but long. They likely do not know their tier, may not understand model differences, and may not have reference tracks ready. The conversational approach is genuinely good for this user -- it helps them discover preferences they could not articulate in a form. They exit with a profile and a Band Identity Card but may not know what to do next.

**Friction Points:**
- Wrong-skill redirect is informational rather than energy-matching
- Tier/model questions may stump them
- No clear bridge to "now use your profile" after creation
- 12-step flow is thorough but potentially long for someone just exploring

**Bright Spots:**
- Conversational discovery genuinely helps beginners articulate preferences
- Reference track decomposition teaches them sonic vocabulary
- Exclusion defaults explanation about positive vs negative prompts is educational
- Unclear intent handling presents all operations clearly

### Expert

An experienced producer who knows exactly what they want. They know the genre terms, the vocal descriptors, the model/tier, everything. The 12-step interview is painfully slow for them. Headless mode exists but requires YAML formatting. They want to dump everything in one message and get a profile. The edit operation's natural language support is strong. Health Check is useful for sanity-checking.

**Friction Points:**
- No fast-track path for users who provide comprehensive input upfront
- Step-by-step gates slow down someone who already has all answers
- Headless requires YAML knowledge -- no natural-language fast-track

**Bright Spots:**
- Edit operation accepts natural language changes -- expert-friendly
- Headless mode is comprehensive for scripting and automation
- Health Check provides objective quality assessment
- Schema is rich and domain-aware (known_working_patterns, generation_learnings)

### Confused

User invoked this skill by accident or thought it makes songs. The operation detection table handles this with a redirect. The redirect is correct but cold. If they meant to edit but said "change my sound," intent detection should catch it, but ambiguous phrasing could misroute.

**Friction Points:**
- Wrong-skill redirect is helpful but not emotionally warm
- Ambiguous phrasing between Edit and Create could misroute
- No "did you mean...?" confirmation for ambiguous intents

**Bright Spots:**
- Explicit "Wrong skill" handling exists -- many skills lack this entirely
- Unclear intent shows all available operations rather than guessing

### Edge-Case

User with a hybrid vocal/instrumental project, non-Latin-script band names, multiple languages, or obscure reference tracks. The instrumental flag is binary. A "mostly instrumental with occasional spoken word" project must choose one mode.

**Friction Points:**
- Instrumental is binary -- no hybrid vocal/instrumental support
- Single language field assumes monolingual lyrics
- Reference track decomposition depends on web search finding useful results
- Band name kebab-case derivation may struggle with non-Latin scripts

**Bright Spots:**
- Instrumental flag at least exists and properly skips vocal requirements
- Language field is present and flows to downstream skills
- Fallback for web search unavailability is documented

### Hostile-Environment

Agent running where Python is unavailable, scripts fail, web search is disabled, or bmad-init config is missing. The skill has a config fallback (greet generically, default to English), but script failures have no fallback. A broken Python environment effectively bricks the skill for all operations except reading files directly.

**Friction Points:**
- Script failures have no inline fallback -- validation is all-or-nothing
- No degraded-mode operation when Python is unavailable
- Web search absence silently degrades reference track quality

**Bright Spots:**
- Config fallback is explicit and reasonable
- File-based storage means profiles are human-readable even if the skill is unavailable

### Automator

A CI pipeline, orchestrating agent, or cron job that needs to create, validate, or modify profiles programmatically. Headless mode is impressively comprehensive with structured JSON responses and well-defined output contracts. Main gaps: writer voice analysis and health check have no headless paths, and no batch operation support.

**Friction Points:**
- Writer voice analysis has no headless mode
- Health check has no headless mode
- No batch operations (validate all, health-check all)
- Headless error responses are not explicitly defined

**Bright Spots:**
- Headless CRUD coverage is comprehensive and well-designed
- JSON output contracts are explicit for each headless subcommand
- Flag detection supports both --headless and -H

---

## Autonomous Readiness

- **Overall Potential:** easily-adaptable
- **HITL Interaction Points:** 14
- **Auto-Resolvable:** 10
- **Needs Input:** 4
- **Suggested Output Contract:** JSON object with status, profile_path, validation results, and optionally the profile content. Already well-defined for most headless subcommands.
- **Required Inputs:**
  - Profile YAML or field overrides (for create/edit)
  - Profile name (for load/edit/delete/duplicate)
  - Writing samples as text or file paths (for voice analysis)
  - Target profile name (for voice analysis storage)
- **Notes:** This skill is already substantially headless-capable. The CRUD headless modes are comprehensive with explicit JSON output contracts. Remaining gaps are headless writer voice analysis and headless health check -- both straightforward to add since the analysis logic is algorithmic. The interactive Create flow's 12-step discovery is fundamentally interactive by design and correctly remains so.

---

## Script Opportunities

**Existing Scripts:**
- validate-profile.py -- validates profile YAML against schema, derives kebab-case filenames
- list-profiles.py -- scans and lists profiles, checks individual profile existence
- tier-features.py -- returns tier feature availability as structured JSON
- diff-profiles.py -- structured diff between two profile YAML files

**assemble-profile.py -- YAML assembly from structured fields** | SKILL.md:86 | MEDIUM | Source: script-opportunities
After conversational discovery, the LLM assembles a full YAML file from collected fields. A script could take a JSON dict and produce correctly-formatted YAML with proper field ordering and indentation, eliminating formatting variance.
*Action:* Create assemble-profile.py accepting JSON dict of profile fields, applying schema field ordering and YAML comment templates.

**Tier drift detection script** | SKILL.md:103 | MEDIUM | Source: script-opportunities
Load Profile's tier drift comparison is a simple string comparison. Determinism: certain. Savings: 150-200 tokens/invocation.
*Action:* Add --check-tier-drift flag to list-profiles.py or validate-profile.py.

**Health check completeness metrics** | SKILL.md:149 | MEDIUM | Source: script-opportunities
Health Check step 2 has the LLM assess field population that is mostly emptiness/existence checks. Only "is it vague?" and "is it generic?" require LLM judgment. Determinism: high. Savings: 200-400 tokens/invocation.
*Action:* Create health-check.py that outputs structured JSON completeness metrics (field population flags, word counts). LLM then only judges qualitative dimensions.

**Edit re-serialization via assemble-profile.py** | SKILL.md:108 | LOW | Source: script-opportunities
After edits, re-serialization to YAML is deterministic. Same assemble-profile.py would handle this.
*Action:* Additionally, a patch-profile.py script accepting field overrides would serve both interactive edits and headless:edit.

**Duplicate Profile is entirely deterministic** | SKILL.md:119 | LOW | Source: script-opportunities
Copies a YAML file, optionally increments version, updates name field. Determinism: certain. Savings: 150-250 tokens/invocation.
*Action:* Create duplicate-profile.py with --source, --new-name, --increment-version flags.

**Delete Profile file deletion is deterministic** | SKILL.md:116 | LOW | Source: script-opportunities
The actual deletion after existence check is deterministic. Savings: 50-100 tokens/invocation.
*Action:* Create delete-profile.py (or add --delete to list-profiles.py).

**Headless flag parsing** | SKILL.md:23 | LOW | Source: script-opportunities
Activation mode detection parses --headless flags. A pre-pass script could return structured JSON. Low priority since the LLM handles this cheaply.
*Action:* Create parse-headless-flags.py if batch automation volume warrants it.

**Token Savings:** Estimated 1000-1750 tokens per invocation across all opportunities | Highest value: health-check.py pre-pass script | Prepass opportunities: 2 (health-check, tier drift)

---

## Quick Wins (High Impact, Low Effort)

| Issue | File | Effort | Impact |
|-------|------|--------|--------|
| Add `./` prefix to 21 bare internal paths | SKILL.md, references/tier-features.md | Low | High -- resolves all bare-internal-path violations |
| Remove unused `os` import | scripts/list-profiles.py:19 | Trivial | Clears lint error |
| Move README.md to references/ | README.md | Low | Resolves root-level prompt file violation |
| Replace `../` parent reference in README.md | README.md:63 | Low | Eliminates fragile path reference |
| Add --check-tier-drift flag to existing script | scripts/list-profiles.py or validate-profile.py | Low | Deterministic replacement for LLM comparison, saves 150-200 tokens/invocation |
| Break reference tracks discovery step into sub-bullets | SKILL.md:69 | Low | Ensures research mandate is not overlooked during execution |

---

## Optimization Opportunities

**Token Efficiency:**
The skill is already well-optimized at 174 lines / ~3627 tokens with no waste patterns detected. Progressive disclosure correctly places schema (109 lines) and tier features (78 lines) in references/. The main token efficiency gains come from scripting opportunities: health-check.py pre-pass (200-400 tokens/invocation), assemble-profile.py (300-500 tokens), and tier drift detection (150-200 tokens). Total potential savings: 1000-1750 tokens per invocation.

**Performance:**
Good parallelization awareness in Edit Profile and Analyze Writer Voice. Extending explicit batching guidance to Create Profile and Health Check operations would eliminate 2-3 unnecessary round-trips. Load Profile's sequential check-then-read pattern adds one redundant round-trip for the common case. Edit Profile's post-edit validation and diff could run in parallel.

**Maintainability:**
Adding the three missing structural sections (Identity, Communication Style, Principles) would improve behavioral consistency and make the agent more maintainable by explicitly documenting decision frameworks that are currently implicit. The 21 bare internal path fixes improve portability. Storing the Band Identity Card in the profile YAML would create a persistent, living artifact rather than a one-time creation ceremony.

---

## Recommendations

1. **Fix all 21 bare internal paths by adding `./` prefix** -- highest issue count, mechanical fix, resolves the majority of high-severity findings in a single pass across SKILL.md and references/tier-features.md.
2. **Add the three missing structural sections (Identity, Communication Style, Principles)** -- critical for a conversational-discovery agent where tone and judgment calls are the core product. The content already exists implicitly in the Overview; it needs to be extracted and formalized.
3. **Add progressive YAML assembly checkpoints during Create Profile** -- the highest-value creative enhancement. Protects 20+ minutes of user creative input from context compaction. Structured YAML survives compaction far better than conversational fragments.
4. **Create health-check.py pre-pass script** -- highest-value script opportunity. Extracts completeness metrics so the LLM only judges qualitative dimensions. Saves 200-400 tokens per invocation and enables headless health checks.
5. **Add fast-track detection for expert users at the start of Create Profile** -- bridges the gap between guided beginner interview and raw YAML headless mode, respecting expert users' time while maintaining completeness.
