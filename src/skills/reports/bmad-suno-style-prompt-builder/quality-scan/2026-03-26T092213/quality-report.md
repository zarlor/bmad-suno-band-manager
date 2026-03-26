# Quality Report: bmad-suno-style-prompt-builder

**Scanned:** 2026-03-26T09:22:13
**Skill Path:** /home/zarlor/bmm/_bmad-output/bmad-suno-band-manager-module/src/skills/bmad-suno-style-prompt-builder
**Report:** /home/zarlor/bmm/_bmad-output/bmad-suno-band-manager-module/src/skills/reports/bmad-suno-style-prompt-builder/quality-scan/2026-03-26T092213/quality-report.md
**Performed By** QualityReportBot-9001

## Executive Summary

- **Total Issues:** 20
- **Critical:** 0 | **High:** 12 | **Medium:** 5 | **Low:** 3
- **Overall Quality:** Good
- **Overall Cohesion:** cohesive
- **Craft Assessment:** Well-crafted domain-expert skill with clean progressive disclosure, efficient persona establishment, and zero waste patterns. SKILL.md is at the upper token boundary (~5074 tokens) but justified by workflow complexity (6 steps, headless modes, tier-aware logic).

This agent embodies a music producer's sound engineer who translates musical intent into Suno-optimized style prompts, backed by exceptionally deep empirical platform knowledge. The architecture is strong -- progressive disclosure is textbook, headless modes are comprehensive, and the domain expertise encoded in the reference file is genuinely rare. The most significant structural finding is three missing behavioral sections (Identity, Communication Style, Principles) and pervasive bare internal paths that need ./ prefixing. The domain content itself is excellent; the gaps are in structural standards compliance rather than capability.

### Issues by Category

| Category | Critical | High | Medium | Low |
|----------|----------|------|--------|-----|
| Structure & Capabilities | 0 | 4 | 3 | 0 |
| Prompt Craft | 0 | 0 | 1 | 3 |
| Execution Efficiency | 0 | 0 | 0 | 2 |
| Path & Script Standards | 0 | 8 | 0 | 0 |
| Agent Cohesion | 0 | 0 | 2 | 3 |
| Creative | -- | -- | 8 | 5 |

---

## Agent Identity

- **Persona:** A music producer's sound engineer who translates musical intent into Suno-optimized style prompts, with deep empirical knowledge of how Suno models interpret prompt language
- **Primary Purpose:** Generate model-aware Suno style prompt packages (style prompt + exclusion prompt + slider recommendations + wild card variant) from band profiles and user creative direction
- **Capabilities:** 6

---

## Strengths

*What this agent does well -- preserve these during optimization:*

**Deep Domain Expertise**
- Exceptionally deep domain knowledge encoded in workflow -- genre trigger words, BPM behavior, critical zone awareness, instrument bleed-through, bass prominence limitations, and dynamic control via style prompt overriding lyric tags. This reads like distilled real-world testing notes, not generic documentation. *(agent-cohesion)*
- Genre Term Behavior Table is a standout reference asset -- empirical testing data (e.g., "progressive metal" produces Dream Theater shred, "progressive groove metal" produces Mastodon-adjacent grooves) that no official Suno documentation provides. *(agent-cohesion, enhancement-opportunities)*
- Production-tested genre behavior table with verifiable claims (e.g., "BPM tags have zero detectable effect -- confirmed by librosa analysis"). *(enhancement-opportunities)*
- Critical zone awareness and front-loading guidance bakes platform expertise directly into the construction process so every prompt benefits from expert knowledge without the user needing to learn it. *(enhancement-opportunities)*

**Architecture & Design**
- Dual-mode activation (interactive + headless) with five distinct invocation patterns and clear contracts. Structured JSON error output makes it composable with orchestrating agents or scripts -- a model for other skills. *(agent-cohesion, enhancement-opportunities)*
- Heavy domain knowledge properly extracted to references/model-prompt-strategies.md -- 333 lines of model strategies, genre tables, vocal triggers, slider guidelines, and tested descriptors, all properly separated from the main SKILL.md. Textbook progressive disclosure. *(prompt-craft)*
- Reference file is comprehensive and well-organized -- exactly the kind of content that belongs in a reference file. *(prompt-craft)*
- Headless mode detection is well-structured with clean separation of sub-modes, defaults, and error contracts. *(prompt-craft)*

**User Experience**
- Complete prompt package output with copy-ready blocks eliminates last-mile friction between AI output and Suno input. Users get both formatted presentation (with reasoning and character counts) AND raw text for pasting. *(agent-cohesion, enhancement-opportunities)*
- Persona established efficiently through "music producer's sound engineer" analogy -- maintains professional, domain-aware voice without excessive persona reinforcement. *(prompt-craft)*
- Overview is concise and well-structured: 7 lines covering mission, domain context, and design rationale where every sentence earns its place. *(prompt-craft)*
- Activation sequence is logically ordered: headless detection before interactive flow, config loads before config vars are used, proper fallback for missing bmad-init. *(structure)*
- Description follows the two-part format with specific quoted trigger phrases. *(structure)*
- Validation already scripted in validate-prompt.py -- character limit validation, critical zone checks, front-loading checks, and structural validation correctly delegated to a deterministic script. *(script-opportunities)*

---

## Truly Broken or Missing

*Issues that prevent the agent from working correctly:*

### Missing Behavioral Sections (structure)

| Issue | File | Line | Severity |
|-------|------|------|----------|
| Missing ## Identity section | SKILL.md | 1 | HIGH |
| Missing ## Communication Style section | SKILL.md | 1 | HIGH |
| Missing ## Principles section | SKILL.md | 1 | HIGH |

The Overview embeds an implicit identity ("Act as a music producer's sound engineer") and domain-critical principles are scattered throughout workflow steps (e.g., "Never put artist names in the style prompt", "front-load the critical zone", "negative prompts are unreliable"). These are high quality but need extraction into dedicated sections for proper AI behavioral priming.

**Action:**
1. Add a dedicated **## Identity** section after Overview with a clear one-sentence persona.
2. Add a **## Communication Style** section with 3-5 concrete examples showing how to ask about genre, present decompositions, and offer refinements.
3. Add a **## Principles** section consolidating the top 5-7 guiding principles (critical zone front-loading, artist name decomposition, positive instruction framing, etc.).

### README.md Progression and Structure Issues (structure, path-standards)

| Issue | File | Line | Severity | Source |
|-------|------|------|----------|--------|
| No progression condition keywords found in README.md | README.md | 66 | HIGH | structure |
| Prompt file at skill root: README.md | README.md | 0 | HIGH | path-standards |
| Parent directory reference (../) found | README.md | 65 | HIGH | path-standards |

README.md is located at the skill root but should be in ./references/ per path standards. It also lacks progression conditions and contains a fragile parent-directory reference.

**Action:** Move README.md to references/README.md and add progression conditions. Replace the `../` reference with a non-relative path pattern.

### Bare Internal Paths Without ./ Prefix (path-standards)

Six instances of bare skill-internal paths that should use `./references/`, `./scripts/`, `./assets/` to distinguish from `{project-root}` paths:

| File | Line | Path Referenced |
|------|------|----------------|
| SKILL.md | 25 | `references/model-prompt-strategies.md` (in headless:migrate description) |
| SKILL.md | 84 | `references/model-prompt-strategies.md` |
| SKILL.md | 95 | `references/model-prompt-strategies.md` |
| SKILL.md | 210 | `scripts/validate-prompt.py` |
| SKILL.md | 260 | `scripts/` directory reference |
| SKILL.md | 261 | `validate-prompt.py` script reference |

**Action:** Prefix all internal paths with `./` (e.g., `./references/model-prompt-strategies.md`, `./scripts/validate-prompt.py`).

---

## Detailed Findings by Category

### 1. Structure & Capabilities

**Agent Metadata:**
- Sections found: Overview, Activation Mode Detection, On Activation, Workflow Steps, Scripts
- Sections missing: Identity, Communication Style, Principles
- Capabilities: 6
- Memory sidecar: No
- Headless mode: Yes (from-profile, custom, refine, migrate, hybrid)
- Structure assessment: Strong domain content and well-structured workflow, but missing three required behavioral sections.

#### Medium

**Name does not follow standard agent naming pattern** *(SKILL.md:1)*
Name "bmad-suno-style-prompt-builder" does not follow `bmad-{code}-agent-{name}` or `bmad-agent-{name}` pattern. This may be intentional if this is considered a workflow skill rather than a persona agent.
*Action:* Evaluate whether this skill intentionally uses a non-agent naming convention and document the rationale, or rename to follow the standard pattern.

**Headless mode lacks dedicated bare headless activation handling** *(SKILL.md:16)*
The Activation Mode Detection section thoroughly documents headless sub-modes but there is no explicit handling for bare `--headless` (no sub-mode, no profile name) -- this case appears unhandled.
*Action:* Add explicit documentation for what happens with bare `--headless` invocation.

**README.md lacks config header with language variables** *(README.md:1)*
Pre-pass deterministic finding. README.md lacks a config header with language variables.
*Action:* Add a config header with language variables to README.md if this prompt file requires configuration.

### 2. Prompt Craft

**Agent Assessment:**
- Agent type: domain-expert
- Overview quality: appropriate (7 lines, efficient)
- Progressive disclosure: good (model-prompt-strategies.md handles heavy reference material)
- Persona context: appropriate
- SKILL.md is well-crafted for a domain-expert skill. At 262 lines / ~5074 tokens, it is at the upper boundary but justified by the complexity of the workflow (6 steps, headless modes, tier-aware logic). Minor opportunities exist to extract instrument bleed-through details and reduce slider duplication.

**Prompt Health:** 0/1 prompts with config header | 0/1 with progression conditions | 0/1 self-contained (README.md is the only prompt file; SKILL.md itself has config header and progression)

#### Medium

**Web search fallback instruction may be unclear under context compaction** *(SKILL.md:100)*
Line 100 instructs the agent to "Always use web search" with a fallback, while references/model-prompt-strategies.md lines 310-316 contain a more detailed "Confidence Check" covering the same logic. This is acceptable belt-and-suspenders redundancy for a critical judgment call.
*Action:* Consider adding a brief note in SKILL.md: "See Confidence Check in model-prompt-strategies.md for the full protocol."

#### Low

**Instrument bleed-through section is lengthy for SKILL.md** *(SKILL.md:117)*
Lines 117-123 contain 7 lines of detailed guidance on instrument ordering and bleed-through that reads more like reference material than workflow instruction.
*Action:* Consider extracting to references/model-prompt-strategies.md under a new "Instrument Bleed-Through" section.

**Slider ranges duplicated between SKILL.md and reference file** *(SKILL.md:160)*
Step 4 contains slider ranges that overlap substantially with the more detailed version in model-prompt-strategies.md lines 241-296.
*Action:* Borderline acceptable since SKILL.md provides the "quick answer" while the reference provides song-type specifics. If token budget is a concern, keep only creativity-mode ranges in SKILL.md.

**Refinement offer text is prescriptive rather than outcome-focused** *(SKILL.md:246)*
Line 247 specifies exact phrasing for the refinement offer. For a domain-expert agent with a sound engineer persona, the agent should be trusted to phrase this naturally.
*Action:* Replace the quoted script with an outcome directive: "Offer refinement -- if the user wants changes, loop back to the relevant step."

### 3. Execution Efficiency

#### Low

**Band profile read and model-prompt-strategies read could overlap** *(SKILL.md:62)*
These are currently sequential across steps. Savings would be minimal (~1-2 seconds) and only applies when the user provides the model upfront.
*Action:* Consider loading model-prompt-strategies.md eagerly in Step 1 alongside the band profile read when the model is already known.

**Reference track web search and model strategy load could be batched** *(SKILL.md:100)*
Independent operations when both are needed. Batching saves one round-trip (~2-3 seconds). Only applies when reference tracks are provided.
*Action:* Batch the web search for artist/song decomposition with the model-prompt-strategies.md read at the start of Step 2.

### 4. Path & Script Standards

**Script Inventory:** 1 script (python: 1) | Missing tests: none

All 8 path-standards findings are HIGH severity and documented above in the Truly Broken section:
- 1 prompt file at skill root (README.md should be in ./references/)
- 1 parent directory reference (../)
- 6 bare internal paths without ./ prefix

### 5. Agent Cohesion

**Cohesion Analysis:**

| Dimension | Score | Notes |
|-----------|-------|-------|
| Persona Alignment | strong | The "sound engineer" persona perfectly matches the capabilities. The skill talks like an engineer, thinks like an engineer, and produces engineer-level output. The persona genuinely shapes communication and decision-making. |
| Capability Completeness | mostly-complete | Core prompt-building workflow is thorough. Gaps in session-to-session continuity (no history), edge-case workflows (covers), and scale (batch/album). None prevent primary value delivery. |
| Redundancy Level | clean | No consolidation opportunities identified. |
| External Integration | intentional | References bmad-init (config), Feedback Elicitor (headless:refine input), and Lyric Transformer (handoff target). All references are purposeful with clear patterns. |
| User Journey | complete-end-to-end | User can enter with a vague musical idea and leave with a complete, copy-ready prompt package. Only friction point is cross-session continuity. |

#### Medium

**No prompt history or versioning capability** *(SKILL.md)*
The skill builds prompts and offers refinement loops but has no mechanism to save, recall, or compare previous prompt packages across sessions. Users iterate across sessions but must start from scratch or manually save outputs. *(Also flagged by enhancement-opportunities)*
*Action:* Add an optional save/recall mechanism -- write prompt packages to a per-profile output directory with timestamps. Allow "show last prompt for {profile}" as a conversational command.

**Web search dependency for reference track decomposition lacks graceful degradation** *(SKILL.md)*
The fallback is binary (available/unavailable) with a single generic question for the unavailable case. No structured questionnaire for the fallback, and no handling for the degraded-search scenario (available but slow/unhelpful). *(Also flagged by enhancement-opportunities)*
*Action:* Add a three-tier fallback chain: (1) web search, (2) training knowledge with confidence disclaimer, (3) structured questionnaire asking about genre, era, vocal style, key instruments, energy/dynamics, and emotional tone.

#### Low

**No guidance for multi-song batch workflows** *(SKILL.md)*
For users building an album or EP, no explicit batch mode or guidance for maintaining sonic coherence across a set of songs.
*Action:* Consider adding a batch/album mode or documenting a recommended workflow for album coherence.

**Cover feature mentioned in references but not in skill workflow steps** *(SKILL.md)*
model-prompt-strategies.md documents Cover feature behavior but no workflow path exists for building cover-style prompts.
*Action:* Either add a headless sub-mode (--headless:cover) or explicitly scope covers out in the SKILL.md overview.

**Manifest capability name understates the full output** *(bmad-manifest.json)*
Single capability "build-style-prompt" undersells the skill's breadth (four outputs, five headless modes, migration, refinement).
*Action:* Expand the manifest description to mention migration and refinement modes.

**Creative Suggestions:**

**Prompt A/B testing guidance** *(SKILL.md)*
The skill gives good iteration advice but could formalize a structured A/B testing approach, suggesting which variables to isolate first.
*Action:* Add an optional "iteration coach" conversational mode for structured A/B testing.

**Prompt template library for common starting points** *(SKILL.md)*
Expanding the existing example prompts into a browsable template library organized by genre family, mood, and model would give users fast starting points.
*Action:* Create a references/prompt-templates.md with 15-20 tested starting-point prompts.

**Reverse-engineering existing Suno outputs** *(SKILL.md)*
The skill builds prompts going forward but does not support the reverse direction. A "diagnose my generation" capability would close the feedback loop.
*Action:* Consider adding an interactive "diagnose" mode where the user describes what Suno produced and the skill suggests prompt adjustments.

### 6. Creative (Edge-Case & Experience Innovation)

**Agent Understanding:**
- **Purpose:** Generate model-aware Suno style prompts that translate musical intent into the precise descriptor language each Suno model responds to best, producing a complete package of style prompt, exclusion prompt, slider recommendations, and wild card variant
- **Primary User:** Musicians and music producers using Suno AI to generate songs, ranging from casual free-tier users to Pro/Premier subscribers with complex band profiles and multi-song catalogs
- **Key Assumptions:**
  - Users understand what Suno is and have an account
  - Users have at least a vague musical direction (genre, mood, or reference)
  - Band profiles exist in a known directory structure when referenced
  - The bmad-init skill is available for config loading
  - Web search tools are available for reference track decomposition
  - Users know which Suno model they want to use or can choose when asked

**Enhancement Findings:**

#### High-Opportunity

**No band profile discovery flow when user has no profiles yet** *(SKILL.md:60)*
A first-time user who has never created a band profile gets dumped into a cold "no profiles found" state with no guidance on how to create one.
*Action:* When no profiles exist, proactively offer two paths: (1) "We can build from scratch" and (2) "I can hand you off to the Profile Manager first." Frame the no-profile path as the default.

**Missing soft gate elicitation during input gathering** *(SKILL.md:84)*
Step 1 uses checklist-style enumeration without soft gates like "anything else, or shall we start building?" that would draw out richer creative input from users in creative flow.
*Action:* Insert soft gates after initial genre/mood gathering and after model/creativity selection.

**Iteration history across refinement loops** *(SKILL.md:209)*
Each refinement iteration overwrites the previous version in conversation. After 3-4 rounds, users cannot compare variants, revert, or see what changed. The wild card variant gets lost on refinement.
*Action:* Number each prompt version (v1, v2, v3...), note what changed, and offer a collected summary at session end.

**Model-prompt-strategies reference is a goldmine barely mined during interactive use** *(references/model-prompt-strategies.md)*
Production-tested findings about genre triggers, dangerous words, vocal behavior sit in a reference file that is only passively consulted. A user requesting "progressive metal" will get Dream Theater shred without warning.
*Action:* Add a "gotchas check" substep that scans the constructed prompt against known genre triggers and dangerous words, proactively warning the user before presenting output.

#### Medium-Opportunity

**No capture-don't-interrupt mechanism for out-of-scope creative input** *(SKILL.md:93)*
Users in creative flow often volunteer information belonging to other workflow parts (lyric ideas, structure preferences). No mechanism to silently capture and defer.
*Action:* Add a capture-and-defer note in Step 1 for lyric, structure, or mix-stage information to be stored for handoff.

**Wild card variant could be more targeted with a "twist dial"** *(SKILL.md:195)*
User has no control over what gets twisted. An expert wanting to explore adjacent genres cannot direct the exploration.
*Action:* Offer a brief "twist dial" before generating: (a) genre fusion, (b) era/production shift, (c) mood inversion, (d) instrumentation flip, (e) surprise me.

**Headless refine mode assumes well-structured delta input but provides no schema** *(SKILL.md:20)*
No explicit contract for what "structured adjustments" looks like from the Feedback Elicitor. Most likely headless failure point.
*Action:* Define an explicit input schema for --headless:refine referenced by both skills.

**Headless migrate mode could enable batch model migration** *(SKILL.md:24)*
Built for single-prompt invocation when the highest-value use case is batch migration across a catalog.
*Action:* Document a batch invocation pattern and consider a --headless:migrate-batch mode.

**Web search fallback lacks timeout and degraded-search handling** *(SKILL.md:100)*
Binary available/unavailable check misses the far more common degraded-search scenario.
*Action:* Add a three-tier fallback chain: web search, training knowledge with disclaimer, structured questionnaire.

**Model-specific formatting differences invisible to user** *(SKILL.md:126)*
The skill silently chooses between conversational (v4.5) and film-brief (v5) formatting. Users never see WHY their prompt looks the way it does.
*Action:* Add a one-line rationale above the style prompt output explaining the formatting choice.

**No dual-output for downstream LLM consumption** *(SKILL.md:246)*
When another skill needs to consume the style prompt programmatically, it must parse human-formatted output. No JSON distillate exists.
*Action:* After copy-ready blocks, offer a structured JSON distillate gated behind headless mode or explicit request.

**No parallel review lenses before finalizing** *(SKILL.md)*
The skill never self-reviews output through genre accuracy, Suno gotchas, and user intent lenses before presenting.
*Action:* Add a brief self-review substep between building and presenting that checks against the Genre Term Behavior Table, user intent, and model-specific strategy.

#### Low-Opportunity

**bmad-init config failure silently degrades workflow context** *(SKILL.md:43)*
Fallback handles greeting/language but not other config values (default model preferences, output directories, tier info).
*Action:* Audit what bmad-init provides beyond user_name and communication_language and add explicit fallbacks.

**User who changes model mid-refinement gets full rebuild without expectation-setting** *(SKILL.md)*
Switching from v4.5 to v5 Pro is a fundamental prompt philosophy change, but the flow treats it like any other refinement.
*Action:* Preview the impact before rebuilding: explain the prompt will be rewritten in a different style.

**Skill assumes user understands Suno's UI fields** *(SKILL.md)*
Output includes separate sections but a first-timer may not know where each goes in Suno's interface.
*Action:* Add brief parenthetical after each copy-ready section: "paste into Suno's 'Style of Music' field."

**validate-prompt.py could check for known genre trigger words** *(scripts/validate-prompt.py)*
Script checks structural validity but not known dangerous words from model-prompt-strategies.md.
*Action:* Add optional --check-triggers flag that warns when dangerous words appear without mitigating context.

**Exclude Styles formatting as comma-separated list could be scripted** *(SKILL.md:190)*
Marginal value. validate-prompt.py already validates exclusions; adding format normalization saves ~30-50 tokens.
*Action:* Marginal -- could be added as --format-exclusions flag but savings are too small to prioritize.

**Top Insights:**

1. **The model-prompt-strategies reference is a goldmine that the interactive workflow barely mines.** Production-tested knowledge about genre triggers, dangerous words, vocal behavior, and instrument limitations sits passively in a reference file. A "gotchas check" substep would transform this from passive background knowledge into active quality assurance.

2. **Version tracking across refinement iterations would transform the experience for power users.** The refinement loop is the most-used feature for serious users, but each iteration is ephemeral. Numbering versions and offering a summary makes the loop an exploration tool rather than a replacement cycle.

3. **Soft gate elicitation would draw out richer creative direction from users.** Adding "anything else or shall we move on?" pauses at natural transitions is the single highest-leverage conversational pattern missing from the skill.

---

## User Journeys

*How different user archetypes experience this agent:*

### First-Timer

A user who has heard about Suno and wants to make a song but has never written a style prompt. They are asked about band profiles, models, and creativity modes -- concepts they may not understand. The output is excellent once produced, but the input gathering phase assumes more Suno familiarity than a true first-timer has.

**Friction Points:**
- Model selection question requires Suno platform knowledge
- Band profile question is confusing if they have no profiles
- No guidance on where to paste each output in Suno's UI
- Tier detection question assumes they know their subscription tier

**Bright Spots:**
- Creativity mode explanations are concrete and helpful
- Copy-ready blocks eliminate manual formatting
- Character count display builds trust in the output

### Expert

A power user with multiple band profiles, a preferred model, and specific sonic requirements. Knows exactly what they want and finds input gathering efficient thanks to profile loading. Refinement loop serves them well. Main frustration is lack of version tracking and inability to direct the wild card twist.

**Friction Points:**
- No version history across refinement iterations
- Wild card variant is untargeted -- cannot specify what to twist
- No batch mode for migrating multiple prompts across models
- Cannot fast-track by providing all inputs in a single structured message in interactive mode

**Bright Spots:**
- Profile baseline + per-song modification is exactly the right workflow
- Headless modes are comprehensive and well-designed
- Model-specific formatting is automatic and correct
- Reference track decomposition with show-your-work is trust-building

### Confused

A user who wanted the Lyric Transformer but invoked the Style Prompt Builder by accident, or who thinks "style prompt" means song lyrics. The skill has no intent verification step and proceeds directly to input gathering.

**Friction Points:**
- No intent verification -- skill assumes correct invocation
- No "did you mean to use a different skill?" escape hatch
- Terminology ("style prompt", "exclusion prompt") is Suno jargon without definition

**Bright Spots:**
- The README explains when to use this skill vs. Mac
- Conversational input gathering would eventually reveal the mismatch

### Edge-Case

A user who wants to build a prompt for a genre Suno handles poorly (microtonal music, field recordings, musique concrete) or who provides contradictory input ("make it sound heavy and acoustic, aggressive but gentle").

**Friction Points:**
- No guidance for genres Suno cannot produce well
- No mechanism to surface and resolve contradictions in user input
- Reference track decomposition may fail on very obscure artists

**Bright Spots:**
- Confidence check for reference tracks prevents hallucinated decompositions
- Web search fallback helps with obscure references
- Creativity modes give a framework for handling unusual requests

### Hostile-Environment

The skill is invoked but band profile files are missing, bmad-init is down, web search is unavailable, and the docs/band-profiles/ directory does not exist. The hostile environment journey is surprisingly resilient.

**Friction Points:**
- If docs/band-profiles/ directory itself does not exist, the "list available profiles" fallback may produce a confusing filesystem error
- validate-prompt.py execution failure has no documented fallback -- if Python is unavailable, Step 6 validation silently fails

**Bright Spots:**
- bmad-init fallback is explicit and does not block
- Profile missing-fields handling warns and fills from conversation
- Web search fallback chain is honest about uncertainty

### Automator

A CI pipeline or another skill that wants to invoke this skill headlessly. The headless mode is comprehensive with five invocation patterns, structured error contracts, and clear defaults. The automator journey is excellent.

**Friction Points:**
- No batch invocation pattern for --headless:migrate
- Headless refine input schema is undefined
- No structured output schema documented for headless mode return value

**Bright Spots:**
- Five distinct headless modes cover real use cases
- Structured JSON error contract with missing field details
- Sensible defaults for omitted optional parameters
- Wild card disabled by default in headless mode (correct for automation)

---

## Autonomous Readiness

- **Overall Potential:** headless-ready
- **HITL Interaction Points:** 6
- **Auto-Resolvable:** 5
- **Needs Input:** 1
- **Suggested Output Contract:** Structured text prompt package containing style_prompt, exclusion_prompt, slider_recommendations, and optional wild_card_prompt, plus a JSON distillate for programmatic consumption
- **Required Inputs:** genre_mood (required), model (optional, defaults to v4.5-all), creativity_mode (optional, defaults to balanced), profile_name (optional), specific_requests (optional), reference_tracks (optional), include_wild_card (optional, defaults to false in headless)
- **Notes:** Already headless-ready with five distinct invocation modes. Only gaps are a formal output schema for headless returns and undefined input schema for refine mode. All interactive HITL points have sensible defaults or accept pre-supplied parameters.

---

## Script Opportunities

**Existing Scripts:** scripts/validate-prompt.py

**Medium-Priority:**

**Band profile YAML pre-parsing** *(SKILL.md:62)* -- Determinism: high | Savings: 300-500 tokens/invocation | Could be prepass: yes | Reusable: yes
Step 1 instructs the LLM to read and parse band profile YAML. A script could return a compact JSON summary instead.
*Action:* Create scripts/extract-profile.py that extracts style_baseline, vocal, exclusion_defaults, model_preference, tier, and reference_tracks into JSON.

**Model strategy extraction** *(SKILL.md:84)* -- Determinism: high | Savings: 800-1500 tokens/invocation | Could be prepass: yes | Reusable: yes
The LLM reads the entire 330-line, ~6700-token reference to find one model's section. A script could extract only the relevant section plus Universal Rules.
*Action:* Create scripts/extract-model-strategy.py that accepts --model and returns only the relevant section, reducing context consumption by 50-75%.

**Headless dispatch pre-parsing** *(SKILL.md:20)* -- Determinism: high | Savings: 200-400 tokens/headless invocation | Could be prepass: yes | Reusable: yes
Deterministic flag parsing, default application, and required-field validation.
*Action:* Create scripts/headless-dispatch.py for pre-validated, normalized headless input.

**Exclusion prompt character/item counting** *(SKILL.md:130)* -- Determinism: certain | Savings: 100-200 tokens
validate-prompt.py already handles this verification, but SKILL.md restates the rules inline.
*Action:* Reference the script's validation as the authority rather than restating rules.

**Low-Priority:**

**Profile directory listing** *(SKILL.md:63)* -- Determinism: certain | Savings: 50-100 tokens (error path only)
Simple filesystem enumeration when profile not found.
*Action:* Add --list-profiles flag to extract-profile.py.

**Genre danger-word checking** *(SKILL.md:107)* -- Determinism: high | Savings: 150-200 tokens
Pattern-matching against known word lists currently done inline by the LLM.
*Action:* Extend validate-prompt.py with --check-dangers flag.

**Genre Term Behavior Table lookup** *(references/model-prompt-strategies.md)* -- Determinism: high | Savings: 200-400 tokens
A pre-pass could return only relevant genre rows instead of all tables.
*Action:* Create scripts/genre-lookup.py for filtered genre data.

**Token Savings:** ~1800-3200 tokens per invocation across all actionable findings | Highest value: extract-model-strategy.py (800-1500 tokens) | Prepass opportunities: 3

---

## Quick Wins (High Impact, Low Effort)

| Issue | File | Effort | Impact |
|-------|------|--------|--------|
| Add ./ prefix to 6 bare internal paths | SKILL.md (lines 25, 84, 95, 210, 260, 261) | Low | Resolves 6 high-severity path-standards violations |
| Move README.md to references/ | README.md | Low | Resolves 1 high-severity structure violation |
| Replace ../ parent reference in README | README.md:65 | Low | Resolves 1 high-severity path violation |
| Add one-line rationale above style prompt output explaining model formatting | SKILL.md:126 | Low | Improves comprehension for all users |
| Add parenthetical paste-target hints to copy-ready blocks | SKILL.md:239 | Low | Prevents most common first-timer mistake |
| Replace prescriptive refinement offer text with outcome directive | SKILL.md:246 | Low | Trusts the agent's persona for natural phrasing |

---

## Optimization Opportunities

**Token Efficiency:**
The highest-value token optimization is an extract-model-strategy.py script that feeds the LLM only the relevant model section from the 330-line reference file, saving 800-1500 tokens per invocation (50-75% reduction in reference file context). Combined with a band profile YAML pre-parser (300-500 tokens) and headless dispatch pre-parser (200-400 tokens), total estimated savings are 1800-3200 tokens per invocation. Additionally, the instrument bleed-through section (7 lines) and slider range duplication could be extracted from SKILL.md to the reference file, saving another ~100-200 tokens from the base prompt.

**Performance:**
Two minor parallelization opportunities exist: batching the model-prompt-strategies read with the band profile read (when model is known upfront), and batching web search with reference file read (when reference tracks are provided). Combined savings of ~3-5 seconds in applicable scenarios. The skill's sequential step structure is otherwise correct given the data dependencies between steps.

**Maintainability:**
The three missing behavioral sections (Identity, Communication Style, Principles) are the biggest maintainability gap. The embedded identity and scattered principles work today but are fragile -- a future editor may accidentally remove or dilute them without realizing their importance. Extracting them into dedicated sections makes the behavioral contract explicit and auditable. The bare internal paths without ./ prefix create fragility if the skill is reorganized. The undefined headless:refine input schema is a maintenance liability -- when the Feedback Elicitor changes output format, there is no contract to validate against.

---

## Recommendations

1. **Add ./ prefix to all 6 bare internal paths and move README.md to references/.** This resolves 8 of 12 high-severity findings with trivial effort and improves resilience to reorganization.
2. **Add dedicated Identity, Communication Style, and Principles sections to SKILL.md.** The content already exists scattered throughout -- extract and consolidate into proper behavioral priming sections. This resolves the remaining 3 high-severity structure findings.
3. **Build extract-model-strategy.py to feed the LLM only the relevant model section.** Highest-value single optimization: saves 800-1500 tokens per invocation and reduces the chance of model strategy cross-contamination.
4. **Add a "gotchas check" substep that scans constructed prompts against the Genre Term Behavior Table and Dangerous Words.** Transforms the passive reference goldmine into an active quality gate, catching Suno pitfalls before the user wastes generations.
5. **Number refinement versions and offer a collected summary at session end.** The refinement loop is the most-used feature for power users; making it archival rather than ephemeral is the highest-leverage UX improvement.
