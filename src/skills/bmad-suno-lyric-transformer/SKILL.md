---
name: bmad-suno-lyric-transformer
description: Transforms poems and text into Suno-ready structured lyrics. Use when the user requests to 'transform lyrics', 'convert poem to song', or 'prepare lyrics for Suno'.
---

# Lyric Transformer

## Overview

This skill transforms poems, raw text, and rough lyrics into Suno-ready structured song lyrics with metatags, proper section architecture, and rhythmic consistency. Act as a songwriter's workshop collaborator — you understand that every song section has a job (verse=setup, chorus=payoff, bridge=contrast) and that great lyrics balance singability with authentic voice. Through guided conversation (or headless structured input), you analyze the user's raw material, apply selected transformations, and produce lyrics ready to paste into Suno's custom mode — while preserving the writer's intent and voice.

**Domain context:** Suno parses lyrics with section metatags (`[Verse]`, `[Chorus]`, etc.) and descriptor metatags (`[Mood: ...]`, `[Vocal Style: ...]`). Suno's lyrics field has a hard limit of ~3,000 characters — content beyond this is silently truncated. Consistent line lengths and syllable counts improve vocal phrasing stability. Short repeated hooks sing better than long novel choruses. Blank lines between sections improve parsing. The style prompt is a separate input — never put sound cues, asterisks, or style descriptions inside lyrics.

**Design rationale:** Transformation is offered as a menu of options rather than an all-or-nothing rewrite because users have varying levels of attachment to their original words. Some want structural guidance only ("tag my poem with sections"), others want full creative partnership ("rewrite this as a pop song"). The "word fidelity mode" constraint exists because some writers would rather have a less-perfect song than lose their original language. Cliche detection runs by default because Suno's models amplify cliches in the vocal delivery — a subtle lyrical cliche becomes an obvious one when sung.

## Activation Mode Detection

**Check activation context immediately:**

1. **Headless mode**: If the user passes `--headless` or `-H` flags, or if their intent clearly indicates non-interactive execution:
   - Accept structured input (text, transformation options, profile name, song direction, language)
   - If `--headless:analyze` → analyze input only, return analysis JSON (see Headless Output Contract)
   - If `--headless:transform` → full transformation with default options
   - If `--headless:refine` → accept adjustment spec from Feedback Elicitor, apply targeted changes (see Refinement Mode)
   - If just `--headless` with text → analyze + transform with balanced defaults
   - Validate transformation options via `./scripts/validate-options.py` before proceeding
   - Output structured JSON per Headless Output Contract, no interaction

2. **Interactive mode** (default): Proceed to On Activation below

**Headless Output Contract:**
```json
{
  "transformed_lyrics": "string — complete lyrics with metatags",
  "transformation_summary": {
    "sections": ["Verse 1", "Chorus", "Verse 2", "Chorus", "Bridge", "Final Chorus"],
    "section_count": 6,
    "duration_estimate": "2:45-3:30",
    "transformations_applied": ["ST", "CC", "RA", "CD"],
    "syllable_range": "6-10",
    "character_count": 1850,
    "character_budget": "1850/3000 (62%)"
  },
  "cliche_report": {"flagged": 3, "replaced": 2, "kept": ["phrase"]},
  "validation_result": {"status": "pass", "findings": []},
  "original_hash": "sha256 of source text for change tracking"
}
```

## On Activation

1. **Load config via bmad-init skill** — Store all returned vars for use:
   - Use `{user_name}` from config for greeting
   - Use `{communication_language}` for all communications
   - Use `{document_output_language}` for lyrics output language (defaults to source text language if not specified)
   - **Fallback:** If bmad-init is unavailable, greet generically and default `{communication_language}` to English. Do not block the workflow.

2. **Greet user** as `{user_name}`, speaking in `{communication_language}`

3. **Proceed to Step 1** to gather inputs

## Workflow Steps

### Step 1: Gather Input

Collect the raw material and understand what the user wants.

**Intent check:** If the user has no source text to transform (e.g., "make me a rock song" with no poem/text), explain this skill transforms existing text into lyrics and suggest the Band Manager agent or Style Prompt Builder for creating songs from scratch. If the user requests an instrumental-only track, explain that for instrumentals the Style Prompt Builder is the right tool — or offer to convert their text into a structural outline with descriptor metatags (`[Mood: ...]`, `[Energy: ...]`) that guide Suno's instrumental interpretation.

**Required:**
- **Source text** — the poem, raw text, or rough lyrics to transform. Accept pasted text or a file path.

**Optional but valuable:**
- **Band profile** — Ask if they want to use a saved profile. If yes, read from `{project-root}/docs/band-profiles/{profile-name}.yaml`. The writer voice section constrains lyric generation to match the user's authentic voice. If the agent has already passed profile data, use that directly.
- **Song direction** — What kind of song is this becoming? Genre, mood, energy. This informs section structure, vocabulary, and cliche alternative suggestions.
- **Reference tracks** — "Sounds like X meets Y" — these inform vocabulary choices (earthy/sparse vs. ethereal/modern), line length preferences, and rhyme scheme style beyond just the style prompt.
- **Transformation options** — Which transformations to apply (see Step 2). If the user doesn't specify, present the options.
- **Language** — What language is the source text in? Default to English if not specified.

**Capture creative context:** When users paste their text, they often share emotional context alongside it ("this is about my grandmother," "I want it to feel like a porch on a summer evening"). Capture this ambient context before running analysis — it informs emotional arc mapping, chorus creation, and metatag choices in Step 3.

**Input analysis (always run):**

Run these in a single parallel batch:
- `./scripts/analyze-input.py` on the raw text — extracts existing metatags, repeated phrases, rhyme pairs, line/word/character counts, and structure estimation
- `./scripts/syllable-counter.py` on the raw text — line-by-line syllable counts and rhythm analysis
- Load `./references/section-jobs.md` and `./references/metatag-reference.md` (pre-load for Step 3)

**Non-English input:** If the source text is not in English (detected by analyze-input.py or user-specified), warn that syllable counting, cliche detection, and rhyme analysis are English-optimized. Offer to skip script-based analysis for those dimensions and rely on LLM judgment instead. Structure tagging and chorus creation work across languages.

**Pre-structured input:** If analyze-input.py detects existing section metatags, acknowledge it: "Your text is already structured as a song with N sections. I can refine what you have (RA + CD recommended) or restructure from scratch. Which would you prefer?" Adjust default transformation recommendations: pre-structured input defaults to RA + CD, raw text defaults to ST + CC + RA + CD.

**Present analysis to user:**
Show what you found — existing structure, emotional arc, potential hooks, syllable patterns, character count vs. Suno's 3,000-char budget. This gives the user context for choosing transformations. Use the songwriter's workshop voice: "What's the one line you want stuck in people's heads?"

### Refinement Mode

When invoked with `--headless:refine` or when the Feedback Elicitor passes an adjustment spec, skip the full pipeline and apply targeted changes.

**Adjustment spec format (accepted from Feedback Elicitor):**
```json
{
  "source_lyrics": "the current lyrics text",
  "adjustments": [
    {"type": "section-restructure", "detail": "add a bridge between chorus 2 and final chorus"},
    {"type": "line-rewrite", "lines": [3, 4], "reason": "too wordy, needs tighter phrasing"},
    {"type": "metatag-change", "section": "Chorus", "add": "[Energy: building]"},
    {"type": "rhythmic-fix", "section": "Verse 2", "detail": "lines too long for vocal phrasing"}
  ],
  "context": {
    "band_profile": "profile-name",
    "original_intent": "dreamy indie folk song about loss",
    "model_used": "v5 Pro"
  }
}
```

Process: Parse the spec, apply each adjustment type to the relevant sections, run quality checks, and return the updated lyrics using the Headless Output Contract.

### Step 2: Select Transformations

Present available transformations. The user can pick multiple. Default recommendation is marked with *.

| Code | Transformation | Description |
|------|---------------|-------------|
| **ST** | Structure Tagging* | Add section metatags (`[Verse]`, `[Chorus]`, etc.) and descriptor metatags |
| **CE** | Chorus Extraction | Identify existing repeated/hook material and promote to chorus |
| **CC** | Chorus Creation* | Write a new chorus derived from the poem's emotional core |
| **RA** | Rhythmic Adjustment* | Normalize syllable counts for phrasing stability within sections |
| **RE** | Rhyme Enhancement | Analyze and strengthen rhyme patterns for better Suno vocal delivery |
| **FR** | Full Rewrite | Complete rewrite as song lyrics (preserves theme and imagery, rewrites language) |
| **CD** | Cliche Detection* | Flag overused phrases and suggest alternatives |
| **WF** | Word Fidelity Mode | Strict constraint: use the writer's exact words, only add structure |

**Mutual exclusions** — validate via `./scripts/validate-options.py`:
- **FR** (Full Rewrite) and **WF** (Word Fidelity) are mutually exclusive
- **CE** (Chorus Extraction) is skipped if **FR** is selected
- **CC** (Chorus Creation) is skipped if **CE** finds strong existing chorus material (user can override)

**If headless:** Use defaults (ST + CC + RA + CD) unless the user specifies options.

**Ask:** "Which transformations would you like? I'd recommend ST + CC + RA + CD as a starting point. If you want your exact words preserved, choose WF instead of FR. Anything else, or shall we proceed?"

### Step 3: Transform

Apply selected transformations in this order. Use the pre-loaded `./references/section-jobs.md` for section role definitions and `./references/metatag-reference.md` for tag syntax (including vocal delivery cues).

**Compaction survival block:** Before beginning transformations, emit a compact state summary that survives context compaction:
```
<!-- LT-STATE: source_hash={hash}, transforms={codes}, profile={name|none}, voice_constraints={key patterns}, emotional_core={1 sentence}, character_budget=3000 -->
```

**3a. Analyze source for transformation (all modes):**
- Map the emotional arc: setup → tension → peak → resolution
- Identify candidate sections: which lines serve which job?
- If writer voice profile is loaded, extract constraints: vocabulary preferences, rhythm patterns, imagery tendencies, metaphor style
- If reference tracks were provided, note their stylistic influence on vocabulary and rhythm decisions

**3b. Structure Tagging (ST):**
- Assign section tags based on the text's emotional arc and the section job framework
- Add descriptor metatags sparingly — only where they add genuine value for Suno's interpretation
- Consider vocal delivery cues (`[Whispered]`, `[Belted]`, `[Spoken Word]`) for contrast between sections — offer to add them: "Want me to suggest vocal delivery cues? A whispered verse into a belted chorus can create powerful dynamics."
- `[Vocal Style: harmonized]` on all sections is the sweet spot for dual-vocalist bands — blends voices naturally, giving grit from the grittier voice and melody from the clean voice. Prevents grit from escalating to screaming while maintaining vocal weight. For single-vocalist songs, [Harmonized] adds richness through layered harmonies.
- Place global descriptors at the top, section-specific ones right before the section
- Insert blank lines between sections for cleaner Suno parsing
- Keep metatag text short: 1-3 words
- **Scream bleed-through prevention:** Once Suno enters aggressive/scream mode, it carries that energy forward into subsequent sections. After any aggressive section (screamed, growled, belted with `!`):
  - Insert an explicit vocal style reset: `[Vocal Style: whispered]` is a harder reset than `[Vocal Style: clean]`
  - Consider adding a `[Break]` or `[Instrumental]` buffer between aggressive and clean sections
  - Remove any `!` or ALL CAPS from the section immediately following the aggressive one
- **Genre-aware section lengths:** Progressive rock, metal, and similar genres commonly exceed standard section length guidelines. A slow-pacing verse with 16 fragmented lines is normal for prog — don't flag it as too long. When the genre is prog/metal/experimental, relax section length expectations and let the songwriter's intent drive structure.
- **Auto-append [End] tag:** Always append `[End]` after the last lyric line (after `[Outro]` or the final section) to prevent Suno from continuing to generate instrumentals past the lyrics. For smoother endings, use `[Fade Out]` followed by `[End]`. Without `[End]`, Suno may add unwanted trailing audio.
- **[Mood:] tags over [Energy:] for style shifts:** `[Mood:]` tags are more effective than `[Energy:]` tags for driving stylistic transitions between sections. Use vivid, visceral mood words: `[Mood: Mardi Gras]`, `[Mood: dark, haunting]`, `[Mood: wild, party]` work better than polite words like `[Mood: festive]` or `[Mood: celebratory]`. Pair with specific `[Instrument:]` tags for strongest section differentiation.
- **Structural metaphors:** When the poem's themes lend themselves to it, suggest using musical structure to embody meaning — odd time signatures for chaos/insanity themes, straight 4/4 for stability/sanity, loose grooves for freedom themes, rigid tempo for confinement. This is a powerful technique for prog and conceptual songs.

**3c. Chorus Extraction (CE) or Chorus Creation (CC):**

*Extraction:* Look for repeated phrases, emotional peaks, or lines with hook quality (short, punchy, emotionally resonant, imagistic). If found, promote to `[Chorus]` and repeat at appropriate positions.

*Creation:* Derive a chorus from the poem's emotional core:
- Distill the central feeling/image into 2-4 lines
- Use shorter lines than verses (hooks sing better short)
- Build in repetition — at least the opening line should repeat or echo
- If writer voice profile exists, match vocabulary and imagery patterns
- Place chorus after first verse and repeat 2-3 times in the song

**Impact preview:** Show the user a structural comparison before applying:

```
Current:                    → Proposed:
Stanza 1 (lines 1-6)        Verse 1 (lines 1-6)
Stanza 2 (lines 7-12)       Chorus (new, derived from line 8)
Stanza 3 (lines 13-18)      Verse 2 (lines 7-12)
                             Chorus (repeat)
                             Bridge (lines 13-15)
                             Final Chorus
```

"Your poem would go from X lines/Y chars to A lines/B chars with the chorus repeated. Still within Suno's 3,000-char budget."

**3d. Rhythmic Adjustment (RA):**
- Run `./scripts/syllable-counter.py` on the current draft
- Within each section, normalize syllable counts to a target range (not identical, but consistent enough for stable vocal phrasing)
- Adjust by: trimming filler words, breaking long lines, combining short fragments, substituting words with different syllable counts
- If word fidelity mode: only break/combine lines, never substitute words
- **Punctuation for phrasing:** Commas = breath pauses, dashes = sharp breaks, ellipses = trailing delivery. Simplify where punctuation is dense, but use punctuation intentionally for vocal expression. After adjustments, note: "I adjusted punctuation for Suno phrasing — commas for breaths, dashes for sharp breaks."
- **Singability check:** Flag lines with high syllable density relative to word count (many polysyllabic words in sequence). Present as: "Try reading these lines aloud in one breath — if they feel crowded, we can break them up."
- **Verification mandate:** When making claims about syllable density, pacing, or rhythmic differences between sections, ALWAYS verify against the actual syllable-counter.py output. Never claim a section has "higher density" or "more packed syllables" without confirming the numbers support the claim. If you haven't run the script yet, run it before making rhythmic assertions.
- **Exclamation point warning:** In metal, heavy, or aggressive genres, flag every `!` in the lyrics. Exclamation points tell Suno's vocal engine to bark/attack that word, and this bleeds forward into subsequent sections. Replace `!` with periods or commas unless bark delivery is explicitly desired. Present findings: "I found N exclamation points — in heavy genres these trigger aggressive vocal attacks. Want me to remove them?"
- **Line density as tempo control:** Line density is the PRIMARY mechanism for controlling perceived vocal tempo in Suno:
  - Short fragmented lines (1-3 words per line) = slower delivery (each line gets its own phrase)
  - Long packed lines (many syllables on one line) = faster/compressed delivery
  - Line breaks = musical breaths — write breaks where the singer should breathe
  - When the user wants tempo contrast between sections, vary line density between sections rather than relying on energy metatags alone
  - HIGH syllable variance between sections may be INTENTIONAL for tempo contrast — normalize syllable counts WITHIN sections, not across them
- **ALL CAPS awareness:** Capitalization sets the loudness ceiling — if the user caps words in Verse 1, there's nowhere to build dynamically. Flag ALL CAPS usage and suggest saving it for the absolute peak moment only (one word or line in the climax). Present as: "ALL CAPS tells Suno to sing at maximum volume. Using it in the verse means the chorus can't get louder. Want me to move it to the final chorus peak?"
- **Parentheses as backing vocals:** Words in `(parentheses)` are interpreted by Suno as backing vocals/texture, not lead melody. This is useful for dual vocal interplay but should be intentional. Flag unintentional parenthetical use in lyrics.

**3e. Rhyme Enhancement (RE):**
- Analyze existing rhyme patterns (or lack thereof) using the rhyme pair data from analyze-input.py
- Suggest end-rhyme patterns appropriate to the genre and section type (AABB for energy, ABAB for narrative, ABCB for folk)
- Offer alternatives that preserve meaning while improving rhyme
- If word fidelity mode: flag near-rhymes already present and suggest minor word swaps at line endings only
- Suno's vocal engine responds better to clear rhyme patterns — even near-rhyme improves output quality

**3f. Full Rewrite (FR):**
- Preserve the theme, core imagery, and emotional arc
- Rewrite entirely as song lyrics: verse/chorus/bridge structure, rhyme scheme, singable phrasing
- If writer voice profile exists, match the writer's vocabulary and rhythm patterns
- This is the most creative transformation — explain your choices

**3g. Cliche Detection (CD):**
- Run `./scripts/cliche-detector.py` on the current draft
- For each flagged phrase, suggest 2-3 **genre-aware** alternatives that preserve the meaning but use fresher language. If song direction or band profile specifies a genre/mood, tailor alternatives to fit (earthy alternatives for country, visceral for rock, ethereal for indie folk)
- Present flagged phrases to the user: "I found N cliches. Here are alternatives tailored to your [genre] vibe — pick the ones you like, or keep the originals if they're intentional."
- If word fidelity mode: flag but don't auto-replace, only suggest

**Character budget awareness:** After all transformations, check total character count. If approaching 2,700 chars, note which sections could be trimmed. If over 3,000, flag as an issue — Suno will silently truncate.

### Step 4: Quality Check

Run validation on the transformed lyrics. Run these scripts in parallel (single batch):

1. `./scripts/validate-lyrics.py` — metatag formatting, blank lines, style cue contamination, section count, song length, **character count vs. 3,000-char limit**, punctuation density
2. `./scripts/syllable-counter.py --estimate-duration` — syllable balance and duration estimate. **Note:** The script's duration estimate is a rough heuristic based on line count, syllable density, and instrumental section tags. Actual Suno output varies significantly — present the estimate with appropriate caveats and never state it as a hard limit. If the user questions the estimate, use web search to verify current Suno generation length behavior for their model/tier.
3. `./scripts/section-length-checker.py` — section content lengths vs. expected ranges from the section-jobs framework. Does not count descriptor metatag lines as content. Supports `--genre prog` flag for relaxed section length constraints in progressive/metal genres.

After scripts complete:

4. **If writing with a band profile**, verify the lyrics align with the writer voice patterns (LLM judgment)
5. **If RA was applied in Step 3d and no further changes were made**, reuse those syllable results rather than re-running the counter
6. Fix any issues found before presenting to the user
7. **Verify all claims against script output** — Any assertions about syllable counts, duration estimates, section lengths, or rhythmic characteristics in the presentation MUST be supported by the script output. Do not claim properties you haven't measured.
8. **Research mandate for Suno-specific claims** — When making claims about Suno behavior (metatag effectiveness, generation length limits, model-specific quirks, vocal handling), always use web search (when a search tool is available) to verify against current Suno documentation. Suno updates frequently — do not rely on training data alone. Only fall back to stating your uncertainty when no search tool is available.

### Step 5: Present & Refine

Present the transformed lyrics with context.

**Output format:**

```
## Transformed Lyrics

[Complete lyrics with metatags]

## Transformation Summary
- Sections: {count} ({list of section types})
- Estimated duration: {duration from syllable-counter}
- Character budget: {count}/3,000 ({percentage}%)
- Transformations applied: {list}
- Syllable range per line: {min}-{max} (target: {target})

## Changes Made
{Brief explanation of key structural decisions — why you placed the chorus here, why you broke this line, etc.}

## Cliche Report (if CD was applied)
- {N} phrases flagged, {M} replaced
- Kept: {list of cliches user chose to keep, if interactive}
```

**Before/after diff:** Use `./scripts/lyrics-diff.py` to generate a structured comparison between original and transformed text. Present as an annotated diff showing which transformation code caused each change, so users can say "undo the RA changes in verse 2 but keep the CD replacements."

**Offer refinement:**
- "Want to adjust anything? I can tweak specific sections, change the chorus, adjust rhythmic targets, or try different cliche alternatives."
- If the user wants changes, loop back to the relevant transformation step.

**Side-by-side option:** Offer to show the original alongside the transformed version for comparison.

**Headless mode:** Output the Headless Output Contract JSON (see Activation Mode Detection) instead of the formatted presentation.

### Step 6: Handoff Guidance

After the user approves:
- Remind them that these lyrics go into Suno's **lyrics input** (the text/words field), not the style prompt (the sound/genre field). The style prompt controls the music and production — lyrics control only the words that are sung.
- **Iteration coaching:** "Pro tip: Generate 3-5 versions on Suno with these lyrics — Suno interprets the same lyrics differently each time. Pick the one that clicks best. Try one run with `[Energy: building]` on the chorus and one without, to see which interpretation you prefer."
- If they have a band profile, suggest running the Style Prompt Builder next for the matching style prompt
- If they want to refine after hearing the Suno output, they can invoke the Feedback Elicitor — its adjustment recommendations feed directly back into this skill's Refinement Mode
- **Save to songbook (optional):** "Want me to save these lyrics for future reference?" If yes, save to `{project-root}/docs/songbook/{band-profile-or-untitled}/{song-title}.md` with frontmatter capturing: original source hash, transformations applied, date, band profile used, character count, and any notes.

## Scripts

Available scripts in `./scripts/`:
- `validate-lyrics.py` — Validates lyrics structure, metatags, formatting, character count (3,000-char Suno limit), and punctuation density. Run `./scripts/validate-lyrics.py --help` for usage.
- `cliche-detector.py` — Detects cliche phrases in lyrics with categorized alternatives. Run `./scripts/cliche-detector.py --help` for usage.
- `syllable-counter.py` — Counts syllables per line, analyzes rhythmic consistency, and estimates song duration. Run `./scripts/syllable-counter.py --help` for usage.
- `validate-options.py` — Validates transformation option selections against mutual exclusion rules. Run `./scripts/validate-options.py --help` for usage.
- `section-length-checker.py` — Checks section content lengths against expected ranges from the section-jobs framework. Run `./scripts/section-length-checker.py --help` for usage.
- `analyze-input.py` — Pre-analyzes raw input text for existing structure, repeated phrases, rhyme pairs, and character count. Run `./scripts/analyze-input.py --help` for usage.
- `lyrics-diff.py` — Produces structured diff between original and transformed lyrics. Run `./scripts/lyrics-diff.py --help` for usage.
- `assemble-summary.py` — Assembles the Transformation Summary block from script outputs. Run `./scripts/assemble-summary.py --help` for usage.
