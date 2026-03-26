# Quality Report: bmad-suno-agent-band-manager

**Scanned:** 2026-03-26T09:52:54
**Skill Path:** /home/zarlor/bmm/_bmad-output/bmad-suno-band-manager-module/src/skills/bmad-suno-agent-band-manager
**Report:** /home/zarlor/bmm/_bmad-output/bmad-suno-band-manager-module/src/skills/reports/bmad-suno-agent-band-manager/quality-scan/2026-03-26T095254/quality-report.md
**Performed By** QualityReportBot-9001 and bmad

## Executive Summary

- **Total Issues:** 48
- **Critical:** 3 | **High:** 14 | **Medium:** 18 | **Low:** 13
- **Overall Quality:** Good
- **Overall Cohesion:** cohesive
- **Craft Assessment:** Well-crafted companion-interactive agent with strong persona establishment and outcome-driven capability prompts. Primary gap is missing config headers across all 5 capability prompts creating context-compaction vulnerability.

Mac is a remarkably well-architected Suno music creation orchestrator with a vivid New Orleans-inspired band manager persona, three thoughtfully differentiated interaction modes, and strong engineering fundamentals (parallelization, selective memory loading, graceful degradation). The most significant structural finding is that 8 prompt files sit at the skill root instead of in `references/` and all capability prompts lack config headers, creating both path standard violations and context-compaction vulnerability. The agent's creative design is a standout -- the mode system, feedback loop, and research discipline show sophisticated awareness of both user needs and LLM failure modes.

### Issues by Category

| Category | Critical | High | Medium | Low |
|----------|----------|------|--------|-----|
| Structure & Capabilities | 0 | 3 | 2 | 4 |
| Prompt Craft | 0 | 0 | 5 | 4 |
| Execution Efficiency | 0 | 0 | 3 | 2 |
| Path & Script Standards | 3 | 11 | 0 | 2 |
| Agent Cohesion | 0 | 0 | 2 | 2 |
| Creative | -- | -- | 10 | 4 |

---

## Agent Identity

- **Persona:** Mac -- a warm, New Orleans-inspired band manager and producer who guides users through Suno music creation with three interaction modes (Demo for speed, Studio for depth, Jam for experimentation), orchestrating four specialized skills into a seamless creative workflow with iterative refinement.
- **Primary Purpose:** Orchestrate Suno music creation by bridging the gap between a user's musical vision and Suno's required inputs (style prompt + lyrics), producing complete copy-paste-ready packages through guided creative conversation and iterative post-generation refinement.
- **Capabilities:** 8

---

## Strengths

*What this agent does well -- preserve these during optimization:*

**Persona & Identity**
- **Exceptionally well-defined persona with natural communication style** -- Mac's identity as a warm New Orleans-inspired band manager is vivid, specific, and consistently reflected across all prompt files. The music production metaphors ('lay down the foundation,' 'mix this down') are baked into the communication style. This level of persona specificity makes the agent immediately engaging. *(agent-cohesion, structure)*
- **Identity, communication style, and capabilities are well-aligned** -- The 'warm, music-savvy band manager' identity is consistent with the conversational, encouraging communication style and the music production metaphors. The three interaction modes align with the 'meet them where they are' principle. *(structure)*
- **Principles are domain-specific and guiding** -- All three principles ('Always output everything,' 'Meet them where they are,' 'The magic is iteration') create clear decision frameworks and avoid generic platitudes. *(structure)*

**Architecture & Design**
- **Three interaction modes provide excellent user journey flexibility** -- Demo/Studio/Jam is not cosmetic. Each mode meaningfully changes question depth, default behaviors, and creative energy. The auto-detect for parameter-rich inputs is particularly smart. *(agent-cohesion, enhancement-opportunities)*
- **Graceful degradation when external skills are unavailable** -- The Skill Availability section provides a clear degradation path: inform user, offer inline alternative, note what they are missing, never silently fail. This is unusually mature design for a multi-skill agent. *(agent-cohesion, enhancement-opportunities)*
- **Activation sequence is logically ordered** -- Config loads before config vars are used; access boundaries load before file operations. Correct logical ordering throughout. *(structure)*
- **Overview section is well-balanced for an orchestrator agent** -- Efficiently covers mission, domain context, and design rationale in three focused paragraphs. *(prompt-craft)*

**Execution Efficiency**
- **Essentials loaded as explicit parallel batch on activation** -- access-boundaries.md, index.md, and bmad-manifest.json are loaded in a single parallel batch during On Activation. *(execution-efficiency)*
- **Steps 3 and 4 explicitly marked as parallel-safe with rationale** -- The note explaining independence between Lyric Transformer and Style Prompt Builder invocations is an exemplary parallelization annotation. *(execution-efficiency)*
- **Conditional parallel routing for independent adjustments in refine flow** -- Correctly distinguishes between independent and dependent adjustments. *(execution-efficiency)*
- **Selective memory loading with load-on-demand discipline** -- index.md and access-boundaries.md load on activation; patterns.md and chronology.md load only when needed. Prevents unnecessary token consumption. *(execution-efficiency)*
- **Context pass-through to external skills avoids re-gathering** -- The instruction to pass relevant context to invoked skills prevents redundant data collection. *(execution-efficiency)*
- **Write delegation to specialized skill preserves access boundary integrity** -- Band profile writes delegated to bmad-suno-band-profile-manager. Both a security and efficiency pattern. *(execution-efficiency)*

**Content Quality**
- **Create-song handles an impressive range of edge cases** -- Instrumental-only, non-English lyrics, long text overflow, URL/audio paste detection, song extension, zero-input Demo, reference track decomposition, and headless/automation mode. Each edge case has a specific handling path. *(agent-cohesion)*
- **Research discipline prevents hallucination in a fast-changing domain** -- 'Search first, assume never' with specific guidance on when to verify. The fallback of stating uncertainty honestly when no search tool is available is exactly right. *(agent-cohesion, enhancement-opportunities)*
- **Battle-tested reference material with empirically validated findings** -- SUNO-REFERENCE.md contains hard-won empirical findings (BPM tags confirmed ineffective via librosa analysis, 'baroque triggers Disney'). *(agent-cohesion)*
- **Reference track decomposition guidance is well-crafted** -- Outcome-focused guidance with 'show your work' instruction that builds user trust. *(prompt-craft)*
- **Package presentation template is comprehensive and Suno-UI-ordered** -- Ordering matches Suno's UI flow with conditional sections for tier, model, and feature availability. *(prompt-craft)*
- **Good cross-reference to create-song format without fragile back-reference** -- refine-song.md includes enough detail to reconstruct the format even if create-song.md is not in context. *(prompt-craft)*
- **Headless mode already designed with a clear input/output contract** -- The create-song headless contract is well-structured with sensible defaults for every optional parameter. *(enhancement-opportunities)*
- **USAGE.md is comprehensive and genuinely useful as standalone documentation** -- Covers every capability with concrete examples, explains feedback elicitation, documents headless modes, and includes real troubleshooting. *(enhancement-opportunities)*

---

## Truly Broken or Missing

*Issues that prevent the agent from working correctly:*

**Critical: {project-root} used for non-_bmad paths (3 instances)**

| File | Line | Detail |
|------|------|--------|
| browse-songbook.md | 14 | `{project-root}/docs/songbook/` -- {project-root} is only valid for {project-root}/_bmad/... paths |
| browse-songbook.md | 15 | `{project-root}/docs/feedback-history/` -- same issue |
| create-song.md | 56 | Band profile loading path uses {project-root} for non-_bmad path |

**Action:** These paths use `{project-root}` to reference directories outside of `_bmad/`. The `{project-root}` prefix is reserved for `{project-root}/_bmad/...` paths only. Update these to use the correct path convention for project-level content outside the _bmad directory.

*(Source: path-standards)*

---

**High: Prompt files at skill root instead of references/ (8 files)**

All progressive disclosure content must be in `./references/` -- only SKILL.md belongs at root.

| File | Source |
|------|--------|
| USAGE.md | path-standards, prompt-craft |
| browse-songbook.md | path-standards |
| save-memory.md | path-standards |
| SUNO-REFERENCE.md | path-standards, prompt-craft |
| create-song.md | path-standards |
| README.md | path-standards |
| refine-song.md | path-standards |
| init.md | path-standards |

**Action:** Move all `.md` files except SKILL.md into the appropriate subdirectory (`references/` for capability prompts and reference files). Update all internal path references after moving.

---

**High: Bare skill-internal paths without ./ prefix (3 instances)**

| File | Line | Detail |
|------|------|--------|
| SKILL.md | 46 | `references/memory-system.md` -- should be `./references/memory-system.md` |
| SKILL.md | 56 | `scripts/pre-activate.py` -- should be `./scripts/pre-activate.py` |
| USAGE.md | 28 | `scripts/pre-activate.py` -- should be `./scripts/pre-activate.py` |

**Action:** Prefix all skill-internal paths with `./` to distinguish from `{project-root}` paths.

*(Source: path-standards)*

---

**High: Bare _bmad reference without {project-root} prefix**

| File | Line | Detail |
|------|------|--------|
| USAGE.md | 643 | `_bmad/_memory/band-manager-sidecar/chronology.md` -- missing `{project-root}` prefix |

**Action:** Add `{project-root}/` prefix to all `_bmad` path references.

*(Source: path-standards)*

---

**High: Missing progression condition keywords (3 prompts)**

| File | Line | Detail |
|------|------|--------|
| browse-songbook.md | 46 | No progression condition keywords -- unclear when prompt completes or hands control back |
| init.md | 56 | After first-run setup completes, unclear how control returns to main activation flow |
| save-memory.md | 31 | After memory is saved, unclear how control returns to Mac |

**Action:** Add explicit progression/completion conditions to each prompt (e.g., 'when complete, return to main menu' or 'proceed when user confirms').

*(Source: structure, structure-capabilities-prepass)*

---

**High: LLM generates capability menu from manifest instead of using existing script (script-opportunities)**

The pre-activate.py script already has `render_menu()` and builds a routing table, but SKILL.md instructs the LLM to 'Generate from actual manifest data -- DO NOT hardcode menu items' rather than calling the script. Estimated token savings: 300-500 per activation.

**Action:** Update SKILL.md On Activation to call `./scripts/pre-activate.py --scaffold` and use its JSON output for menu rendering instead of instructing the LLM to read bmad-manifest.json and generate the menu itself.

*(Source: script-opportunities)*

---

**High: LLM scans multiple directories for songbook inventory on every browse (script-opportunities)**

The LLM reads potentially many files (docs/songbook/, docs/feedback-history/, chronology.md) just to build an inventory listing. Estimated token savings: 500-1500 per invocation.

**Action:** Create `./scripts/scan-songbook.py` that scans directories, extracts metadata from each file, groups by band profile, and outputs a compact JSON inventory for conversational browsing.

*(Source: script-opportunities)*

---

## Detailed Findings by Category

### 1. Structure & Capabilities

**Agent Metadata:**
- Sections found: Overview, Identity, Communication Style, Principles, Research Discipline, Sidecar, On Activation, External Skills, Skill Availability
- Capabilities: 7
- Memory sidecar: Yes
- Headless mode: No (not declared at structure level, though create-song.md has a headless contract)
- Structure assessment: Structurally solid agent with complete required sections, well-defined identity, strong principles, and a logically ordered activation sequence.

**Medium**

- **Memory path inconsistency between Sidecar section and On Activation** (SKILL.md:44) -- Line 46 references `references/memory-system.md` using a relative path while other references use `{project-root}` prefixed paths. **Action:** Ensure all file path references use the same convention. *(structure)*

- **Missing config headers across all prompt files** (8 files) -- README.md, SUNO-REFERENCE.md, USAGE.md, browse-songbook.md, create-song.md, init.md, refine-song.md, and save-memory.md all lack config headers with language variables. **Action:** Add a config header block with required language variables to each prompt file. *(structure, prompt-craft, structure-capabilities-prepass)*

**Low**

- **Description trigger clause lacks quoted specific phrases** (SKILL.md:3) -- Triggers reference 'Mac' and 'Band Manager' by name but do not use quoted specific phrases. **Action:** Consider quoting key trigger phrases. *(structure)*
- **Communication style could benefit from discrete examples** (SKILL.md:20) -- Inline examples within prose are effective but could be clearer as a bulleted do/don't list. **Action:** Consider restructuring as 3-5 discrete example pairs. *(structure)*
- **On Activation section is well-structured but dense** (SKILL.md:48) -- 38 lines covering all activation concerns. Density is justified for a multi-capability orchestrator agent. *(prompt-craft, note)*
- **Overview quality is appropriate** (SKILL.md:8) -- Well-balanced for an orchestrator agent. No action needed. *(prompt-craft, note)*

### 2. Prompt Craft

**Agent Assessment:**
- Agent type: companion-interactive
- Overview quality: appropriate
- Progressive disclosure: needs-extraction
- Persona context: appropriate
- SKILL.md at 107 lines and ~2425 tokens is well within guidelines. Persona is established effectively without redundancy. Main structural issue is SUNO-REFERENCE.md and USAGE.md sitting at root instead of in references/ or docs/ -- together they represent ~14K tokens that could be inadvertently loaded.

**Prompt Health:** 0/5 with config header | 3/5 with progression conditions | 3/5 self-contained

**Medium**

- **No config header -- capability prompts rely on SKILL.md context for variables** -- All 5 capability prompts (browse-songbook.md, init.md, save-memory.md, create-song.md, refine-song.md) lack config headers. If invoked after context compaction drops SKILL.md, the agent has no source for `{project-root}` or `{communication_language}`. create-song.md is most complex and most vulnerable. **Action:** Add config header to each capability prompt declaring required variables. *(prompt-craft)*

**Low**

- **Research Discipline section is verbose for SKILL.md** (SKILL.md:30) -- ~200 tokens stating one principle five different ways. **Action:** Condense to 2-3 lines in SKILL.md and extract detailed bullets to a reference file. *(prompt-craft)*
- **Reference file at skill root instead of references/** (SUNO-REFERENCE.md) -- 234 lines, ~4675 tokens at skill root. **Action:** Move to references/ directory. *(prompt-craft)*
- **Large user-facing documentation at skill root** (USAGE.md) -- 808 lines, ~9294 tokens, ~39% of total skill tokens. **Action:** Move to docs/ subdirectory or ensure loader excludes non-frontmatter files. *(prompt-craft)*
- **Minimal context for judgment-heavy browsing capability** (browse-songbook.md:11) -- Only 46 lines covering scan, present, and interact. No guidance on comparison presentation or export format. **Action:** Add 2-3 lines of guidance on comparison presentation and export format. *(prompt-craft)*

### 3. Execution Efficiency

**Medium**

- **Lyric Transformer invocation lacks output format specification** (create-song.md:111) -- Passes context but does not specify expected return format. Skill may return verbose explanatory text alongside structured lyrics. **Action:** Add expected return format spec, e.g., 'Return structured lyrics with metatags only -- no commentary.' *(execution-efficiency)*
- **Style Prompt Builder invocation lacks output format specification** (create-song.md:131) -- Same issue. **Action:** Add expected return format spec. *(execution-efficiency)*
- **Feedback Elicitor invocation lacks output format specification** (refine-song.md:35) -- Same pattern. All 4 external skill invocations pass context but none specify return format. **Action:** Add expected return format spec to all external skill invocations. *(execution-efficiency)*

**Low**

- **Three independent location scans not explicitly batched** (browse-songbook.md:13) -- Step 1 checks three independent locations as sequential bullet points. Time savings are modest. **Action:** Add explicit parallel batch instruction. *(execution-efficiency)*
- **Checkpoint writes could be parallelized** (save-memory.md:24) -- patterns.md and chronology.md writes are independent and could run in parallel after index.md. **Action:** Note parallel batch opportunity. *(execution-efficiency)*

### 4. Path & Script Standards

**Script Inventory:** 3 scripts (python: 3) | Missing tests: none

All path-standards critical and high findings are reported in the Truly Broken section above.

**Low**

- **No sys.exit() calls in check-memory-health.py** (scripts/check-memory-health.py:1) -- May not return meaningful exit codes. **Action:** Return 0=success, 1=fail, 2=error via sys.exit(). *(scripts)*
- **No sys.exit() calls in pre-activate.py** (scripts/pre-activate.py:1) -- Same issue. **Action:** Return 0=success, 1=fail, 2=error via sys.exit(). *(scripts)*

### 5. Agent Cohesion

**Cohesion Analysis:**

| Dimension | Score | Notes |
|-----------|-------|-------|
| Persona Alignment | strong | Mac's persona is deeply aligned with every capability. Communication style is consistently reflected. No capability feels like it belongs to a different persona. |
| Capability Completeness | mostly-complete | Core creative workflow fully supported. Gaps: songbook cleanup/deletion, songbook search/filtering, album/project-level planning. |
| Redundancy Level | clean | One intentional overlap between create-song Step 6 quick refinement and refine-song capability. Boundary heuristic could be more precise. |
| External Integration | intentional | 4 external skills with clear, distinct roles. Orchestration well-defined. Context passing explicitly designed. Degradation path thoughtful. |
| User Journey | complete-end-to-end | Full creative journey supported. Only friction at scale (large songbook browsing, no album planning). |

**Consolidation Opportunities:**

- **create-song Step 6 (Quick Refinement) / refine-song (RS)** -- The overlap is intentional for UX flow. The boundary heuristic ('clear, simple tweaks' vs. 'deeper feedback') could be documented more precisely to avoid agent confusion about when to handle inline vs. route to the Feedback Elicitor.

**Medium**

- **No dedicated delete/archive capability for songbook** (bmad-manifest.json) -- The songbook accumulates entries with no cleanup mechanism. Over time, browsing degrades. **Action:** Add a delete/archive action to browse-songbook.md or a songbook management capability. *(agent-cohesion)*
- **Songbook has no search or filter capability** (browse-songbook.md) -- Flat list becomes unwieldy at scale with no way to search by genre, mood, date, model, or keyword. **Action:** Add search/filter options to browse-songbook Step 3. *(agent-cohesion)*

**Low**

- **No explicit help/explain-Suno capability for confused newcomers** (SKILL.md) -- Intent check redirects confused users but does not offer interactive Suno orientation. **Action:** Consider adding a lightweight 'Suno 101' capability or integrating orientation into init.md first-run flow. *(agent-cohesion)*
- **Quick refinement boundary with refine-song is vague** (create-song.md) -- 'Clear, simple tweaks' vs. 'deeper feedback' is judgment-based rather than rule-based. **Action:** Document the heuristic more explicitly with concrete examples. *(agent-cohesion)*

**Creative Suggestions:**

- **Album/EP project mode for multi-song coherence** -- No concept of a 'project' tying multiple songs into a coherent album. Users doing album work would benefit from project-level tracking: song ordering, thematic arcs, production consistency. **Action:** Consider adding a project/album concept with track order, mood arc notes, and production consistency checks. *(agent-cohesion)*
- **Template or preset system for common song patterns** -- Experienced users cannot save and reuse abstract patterns (structure skeletons, metatag placements, slider presets). **Action:** Consider adding templates to the memory system or band profiles. *(agent-cohesion)*
- **Memory save could offer a session summary** -- No human-readable session recap after productive sessions. **Action:** Enhance save-memory output to include an optional 3-5 bullet session recap in Mac's voice. *(agent-cohesion)*
- **Songbook could surface creative insights and evolution patterns** -- The songbook shows what exists but does not analyze patterns or growth over time. **Action:** Add an optional 'creative insights' view drawing from patterns.md and chronology.md. *(agent-cohesion)*

### 6. Creative (Edge-Case & Experience Innovation)

**Agent Understanding:**
- **Purpose:** Orchestrates Suno music creation by coordinating four specialized skills through a warm, music-savvy persona that meets users at their skill level via three interaction modes
- **Primary User:** Musicians, poets, and creative people who want to create music with Suno but struggle to translate their vision into Suno's required inputs
- **Key Assumptions:**
  - Users have a Suno account and understand the basic concept of AI music generation
  - Users know their Suno tier and preferred interaction mode before starting
  - Users will complete setup before their first creative work
  - Users will remember to save their session manually or accept the save prompt
  - The four external skills are generally available and reliable
  - Users interact in a single continuous session per song creation/refinement cycle
  - Users can articulate enough about their musical vision to give Mac a starting point

**Enhancement Findings:**

**High-Opportunity**

- **Activation sequence scans context before understanding intent** (SKILL.md:50) -- Loads memory index, band profiles, and chronology before knowing why the user showed up. **Action:** Reorder activation: greet first with minimal context, ask intent, then load only relevant context. *(enhancement-opportunities)*
- **Mode selection is a hard menu when it should be a soft gate** (create-song.md:36) -- Explicit mode question interrupts creative flow. First-timers do not know the difference; experts already communicated intent through detail level. **Action:** Replace with inference-first behavior and a soft confirmation gate. *(enhancement-opportunities)*
- **First-run setup asks four questions up front before any creative work** (SKILL.md:56) -- Highest-friction moment in the entire agent. Every question between 'hello' and 'tell me about your song' is a dropout risk. **Action:** Implement progressive preference discovery with sensible defaults. *(enhancement-opportunities)*
- **Missing Capture-Don't-Interrupt pattern during creative direction gathering** (create-song.md) -- No instruction to silently capture out-of-scope information during direction gathering and route appropriately. **Action:** Add a Capture-Don't-Interrupt directive to Step 2. *(enhancement-opportunities)*

**Medium-Opportunity**

- **Songbook is read-only with no creative re-entry beyond 'reuse'** (browse-songbook.md) -- Misses the most powerful creative action: evolving past songs. **Action:** Add creative re-entry actions: Evolve, Mashup, Sequel, Acoustic/Electric flip. *(enhancement-opportunities)*
- **Refinement fresh start requires re-providing original prompts** (refine-song.md:20) -- Users who come back days later must recall technical details they forgot. **Action:** Add automatic package lookup from songbook/chronology. *(enhancement-opportunities)*
- **Skill availability check has no retry or delayed-availability handling** (SKILL.md:100) -- Once Mac announces degraded mode, no mechanism to re-check later. **Action:** Add soft re-check when degraded capability is requested again. *(enhancement-opportunities)*
- **Memory save is manual-only with no auto-save on milestones** (save-memory.md) -- Session work can be lost if user closes without saving. **Action:** Implement milestone-based auto-save prompts after refine loops, pattern discovery, and long sessions. *(enhancement-opportunities)*
- **Song extension workflow is under-specified** (create-song.md:98) -- Gets three bullet points while other paths get detailed handling. Extension is a common use case. **Action:** Expand to match detail level of other special paths with style continuity and drift warnings. *(enhancement-opportunities)*
- **No Parallel Review Lenses before presenting final package** (SKILL.md) -- Package goes directly from skill outputs to user. No internal consistency check. **Action:** Add three-lens review: coherence, Suno pitfall detection, wild card differentiation. *(enhancement-opportunities)*
- **Headless mode missing batch and pipeline integration patterns** (create-song.md:13) -- Only handles single song creation. Most valuable headless use case is batch processing. **Action:** Extend headless contract with batch mode and variations parameter. *(enhancement-opportunities)*
- **Mac's persona could be more generative during creative direction** (SKILL.md:19) -- Currently mostly receptive during direction-gathering. A real producer makes creative leaps. **Action:** Add 'creative riff' behavior to Studio and Jam modes. *(enhancement-opportunities)*
- **Setup assumes user knows Suno tier and mode names** (init.md) -- Decision paralysis for first-timers afraid of choosing wrong. **Action:** Help users figure out tier, skip mode question on first run, teach through experience. *(enhancement-opportunities)*
- **Context compaction could drop critical state in long sessions** (SKILL.md:54) -- No mechanism to detect or recover when compaction drops essential state. **Action:** Add lightweight state checkpoint mechanism after each create/refine cycle. *(enhancement-opportunities)*

**Low-Opportunity**

- **URL detection does not leverage web search for context** (create-song.md:89) -- Mac says it cannot listen but does not search for song metadata. **Action:** Attempt to extract song/artist name and look up sonic characteristics via web search. *(enhancement-opportunities)*
- **Songbook could surface creative evolution insights** (browse-songbook.md) -- Lists songs but does not show creative growth over time. **Action:** Add a 'Creative Evolution' view synthesizing patterns from chronology.md and patterns.md. *(enhancement-opportunities)*
- **Current mode never surfaced proactively** (SKILL.md:66) -- No visible indicator of active mode during session. **Action:** Include subtle mode indicator in package presentation header. *(enhancement-opportunities)*
- **Refinement loop has no concept of diminishing returns** (refine-song.md) -- Tells users they can refine indefinitely but Suno's stochastic nature means prompt changes have limits. **Action:** After 2-3 rounds, Mac should suggest generating multiple versions instead of further refinement. *(enhancement-opportunities)*

**Top Insights:**

1. **First-run setup is the highest-friction moment and should be replaced with progressive preference discovery** -- Every question between 'hello' and 'tell me about your song' is a dropout risk. Deferring all preferences to organic discovery during the first creative workflow would eliminate the setup wall entirely. **Action:** Remove explicit first-run interview. Set sensible defaults. Capture preferences as they naturally surface during the first song creation.

2. **A pre-presentation consistency check would reduce Suno generation round-trips** -- The assembled package goes directly from skill outputs to user. A quick coherence check (style prompt vs. lyric energy, exclusions vs. genre, character limits, known Suno pitfalls) would catch mismatches before the user wastes a generation. **Action:** Add a three-lens review step before package presentation.

3. **Mac's producer persona could be more generative during creative direction** -- A real producer hears what you describe and makes creative leaps. Mac currently gathers direction through questions but rarely offers unexpected connections. **Action:** Add a 'creative riff' behavior to Studio and Jam modes -- one proactive suggestion per song.

---

## User Journeys

*How different user archetypes experience this agent:*

### first-timer

A user who just signed up for Suno and invoked Mac for the first time. They are hit with four setup questions about preferences they do not yet understand (tier, mode, band profiles, exclusions). If they survive setup, they enter create-song and may be asked to choose a mode they have no context for. The actual song creation flow is smooth once reached -- Demo mode asks minimal questions and produces a complete package with helpful Suno guidance.

**Friction Points:**
- Four setup questions before any creative work
- Asked to choose Demo/Studio/Jam without understanding the difference
- May not know their Suno tier
- Menu presentation with codes (CS, RS, MB, SP, TL, FE, SB, SM) is overwhelming for someone who just wants to make a song

**Bright Spots:**
- Demo mode asks minimal questions and gets to output fast
- First-use Suno guidance explains exactly how to paste the output
- Mac's warm persona and music metaphors make the experience approachable
- The output package is comprehensive and copy-paste ready

### expert

A producer who knows Suno well, has specific model preferences, and wants to move fast. Auto-detect kicks in when they provide 3+ parameters in their opening message, skipping mode selection entirely. Studio mode gives them section-by-section control. The headless mode contract lets them script batch operations.

**Friction Points:**
- Cannot bypass the greeting and menu to go straight to a command
- No shortcut syntax for experienced users
- Headless mode lacks batch processing for album workflows
- Wild card variant may feel like noise when the user has a precise vision

**Bright Spots:**
- Auto-detect skips mode selection for parameter-rich inputs
- Studio mode provides deep creative control
- Direct skill access via slash commands bypasses Mac entirely
- Headless contracts are well-defined for automation

### confused

A user who invoked Mac by accident or thought it did something else. The activation sequence includes an intent check that catches misalignment and offers graceful redirect. If the user is confused about what Suno is (not just what Mac does), there is no educational path.

**Friction Points:**
- No 'what is Suno?' explanation for users who do not know the platform
- Menu codes assume familiarity with the system
- If confused mid-flow, the only escape is to say 'help' -- no persistent navigation

**Bright Spots:**
- Intent check on activation catches misalignment early
- Graceful redirect to other capabilities
- Mac adapts vocabulary to the user's technical level

### edge-case

A user who provides technically valid but unexpected input: a 2,000-word poem, lyrics in Mandarin, a request for a podcast intro or ambient soundscape, or contradictory direction. Long text detection handles the poem case well. Non-English detection is thoughtful. Edge cases like non-music audio are not addressed.

**Friction Points:**
- Non-music audio use cases (podcast intros, soundscapes, jingles) have no workflow
- Song extension is under-specified
- Contradictory direction could be caught earlier during direction gathering
- Multiple songs in one session have no batch support

**Bright Spots:**
- Long text detection with three handling options
- Non-English detection with metatag reliability warnings
- URL detection with graceful explanation of limitations
- Instrumental detection with automatic exclusion defaults

### hostile-environment

A scenario where external skills fail, memory files are corrupted, or the sidecar directory is missing. First-run detection and scaffolding handle the missing directory case. Skill unavailability has explicit graceful degradation. Memory file corruption has no handling.

**Friction Points:**
- No recovery path for corrupted memory files
- Access boundaries could block reading user-provided source text files outside allowed zones
- No validation of memory file integrity on load
- If pre-activate.py fails, no fallback to manual directory creation

**Bright Spots:**
- First-run scaffolding via pre-activate.py
- Explicit skill unavailability handling with degraded paths
- Access boundaries loaded and enforced on every activation
- Memory health check script exists (check-memory-health.py)

### automator

A script, CI pipeline, or another agent invoking Mac headlessly. The create-song headless contract is clean and well-documented. The main gap is batch processing and partial failure handling.

**Friction Points:**
- No batch processing contract for multiple songs
- No partial failure handling in headless mode
- No way to pass a band profile inline -- must reference by name
- Headless output format described as 'structured JSON' but exact schema not documented

**Bright Spots:**
- Headless mode exists with clear input contract and sensible defaults
- Individual skills all have headless variants
- Error contract returns structured JSON with missing field identification
- USAGE.md documents headless modes comprehensively

---

## Autonomous Readiness

- **Overall Potential:** easily-adaptable
- **HITL Interaction Points:** 8
- **Auto-Resolvable:** 6
- **Needs Input:** 2
- **Suggested Output Contract:** Complete Suno package as structured JSON containing: style_prompt (string), lyrics (string with metatags), exclude_styles (string), settings (object with vocal_gender, lyrics_mode, weirdness, style_influence, audio_influence), song_title (string), wild_card_variant (object with style_prompt and pitch), metadata (object with model, character_count, character_limit, band_profile_used)
- **Required Inputs:** genre_mood (required), source_text (optional), band_profile (optional), model (optional, defaults to v4.5-all), creativity_mode (optional, defaults to balanced)
- **Notes:** The agent is already easily adaptable -- headless mode exists with a documented contract. Main gaps: (1) no batch mode for album-scale operations, (2) no inline band profile specification, (3) headless output schema described but not formally defined with field types and enums. The HITL points that genuinely need input are: initial creative direction and source text if lyrics desired.

---

## Script Opportunities

**Existing Scripts:**
- scripts/pre-activate.py -- first-run check, sidecar scaffolding, menu rendering, routing table
- scripts/check-memory-health.py -- memory file size monitoring and pruning recommendations
- scripts/validate-path.py -- access boundary enforcement for file operations

| Priority | Finding | Estimated Savings | Action |
|----------|---------|-------------------|--------|
| High | Menu rendering done by LLM instead of existing script | 300-500 tokens/activation | Update SKILL.md to use pre-activate.py output |
| High | Songbook directory scanning done by LLM | 500-1500 tokens/invocation | Create scripts/scan-songbook.py |
| Medium | Menu-code routing lookup redone by LLM | 100-200 tokens/selection | Use routing_table from pre-activate.py |
| Medium | Source text word counting done by LLM | 100-150 tokens/create | Create scripts/text-metrics.py |
| Medium | Style prompt character counting done by LLM | 100-200 tokens/package | Create scripts/check-prompt-limits.py |
| Medium | Memory file reading for save context | 200-400 tokens/save | Extend check-memory-health.py --summary mode |
| Medium | Access boundary enforcement done by LLM | 150-300 tokens/session | Update prompts to call validate-path.py |
| Low | Sidecar directory existence check | 50-80 tokens/activation | Simplify to always run pre-activate.py --scaffold |
| Low | External skill availability check | 50-100 tokens/activation | Create scripts/check-skill-availability.py |
| Low | Access-boundaries.md creation in init.md | 50-80 tokens/first-run | Remove redundant sections from init.md |
| Low | Band profile YAML reading | 50-150 tokens/profile load | Consider scripts/load-profile-summary.py |

**Token Savings:** 1700-3600 estimated per session | Highest value: songbook scanner (500-1500/invocation) | Prepass opportunities: 4

---

## Quick Wins (High Impact, Low Effort)

| Issue | File | Effort | Impact |
|-------|------|--------|--------|
| Add ./ prefix to 3 bare internal paths | SKILL.md, USAGE.md | Trivial | Fixes path resolution ambiguity |
| Update menu rendering to use pre-activate.py output | SKILL.md | Trivial | Saves 300-500 tokens per activation; script already exists |
| Update routing to use pre-activate.py routing table | SKILL.md | Trivial | Saves 100-200 tokens per selection; script already exists |
| Add sys.exit() to check-memory-health.py and pre-activate.py | scripts/ | Trivial | Enables meaningful exit code checking |
| Add config headers to 5 capability prompts | 5 prompt files | Low | Survives context compaction; all need same 2-3 vars |
| Add progression conditions to browse-songbook, init, save-memory | 3 prompt files | Low | Clarifies capability completion for the agent |
| Update prompts to call validate-path.py | SKILL.md, memory-system.md | Low | Saves 150-300 tokens; script already exists |
| Condense Research Discipline to 2-3 lines | SKILL.md | Low | Saves ~200 tokens; extract detail to reference |

---

## Optimization Opportunities

**Token Efficiency:**
The most impactful token savings come from utilizing existing scripts that are already implemented but not referenced by prompts. Pre-activate.py's menu rendering and routing table capabilities could save 400-700 tokens per activation with zero new code -- just prompt updates. The proposed songbook scanner script represents the highest single-operation savings (500-1500 tokens). Adding output format specifications to all 4 external skill invocations would prevent verbose returns from bloating the orchestrator context. Total estimated savings across all script opportunities: 1700-3600 tokens per session.

**Performance:**
Parallelization discipline is already strong with 3 explicit parallel batch patterns. Two minor opportunities remain in browse-songbook (3 independent scans) and save-memory (2 independent writes). The highest-impact performance improvement would be reordering the activation sequence to greet the user before loading full context (Intent-Before-Ingestion), which improves perceived responsiveness and avoids loading irrelevant context.

**Maintainability:**
Moving 8 prompt files from skill root to references/ would establish a cleaner progressive disclosure structure matching the existing references/ directory pattern. Adding config headers to capability prompts would make them self-contained and resilient to context compaction. Documenting the quick-refinement vs. refine-song boundary heuristic more precisely would prevent agent confusion about routing decisions.

---

## Recommendations

1. **Fix critical path violations** -- Update the 3 `{project-root}` references to non-_bmad paths in browse-songbook.md and create-song.md. These may cause path resolution failures at runtime.
2. **Move prompt files to references/ and add config headers** -- Address the 8 root-level prompt files and 5 missing config headers in a single restructuring pass. This fixes both path-standard violations and context-compaction vulnerability simultaneously.
3. **Update SKILL.md to use existing script outputs** -- Pre-activate.py already handles menu rendering, routing, and directory scaffolding. Updating 2-3 lines in SKILL.md to reference script output instead of instructing LLM behavior saves 400-700 tokens per activation with zero new code.
4. **Add progression conditions to 3 capability prompts** -- browse-songbook.md, init.md, and save-memory.md need explicit completion signals so the agent knows when to return control to the main flow.
5. **Add output format specifications to external skill invocations** -- All 4 external skill calls (Lyric Transformer, Style Prompt Builder, Feedback Elicitor, Band Profile Manager) should specify expected return format to prevent verbose responses from bloating orchestrator context.
