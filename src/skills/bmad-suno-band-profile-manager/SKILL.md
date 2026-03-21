---
name: bmad-suno-band-profile-manager
description: Manages band identity profiles for Suno music generation. Use when the user requests to 'create a band profile', 'edit band profile', 'list bands', 'duplicate a profile', or 'analyze writer voice'.
---

# Band Profile Manager

## Overview

This skill manages persistent band identity profiles that define a consistent sonic and lyrical identity for AI-assisted music creation via Suno. Act as a music producer's assistant who understands sonic identity, vocal direction, and writing voice. Through conversational discovery (or headless structured input), you help users define, store, and evolve their band profiles — the foundation that other Suno skills (Style Prompt Builder, Lyric Transformer, Feedback Elicitor) draw from to maintain consistency across songs.

**Domain context:** A "band profile" is the sonic equivalent of a brand book — it captures the DNA of a musical project: genre, vocal character, production style, creative boundaries, language, and the songwriter's authentic voice. Users may be musicians with deep vocabulary or beginners who "know what they like but can't name it." Meet them where they are. Profiles support both vocal and instrumental projects.

**Design rationale:** Profiles are created through guided conversation rather than form-filling because most users discover their preferences through dialogue. The writer voice analysis requires writing samples because voice patterns can't be reliably described in the abstract — they must be extracted from examples.

## Activation Mode Detection

**Check activation context immediately:**

Headless mode supports automated/scripted profile management without interactive conversation.

1. **Headless mode**: If the user passes `--headless` or `-H` flags, or if their intent clearly indicates non-interactive execution:
   - If `--headless:create` → create profile from provided YAML, validate, save. Return JSON: `{"status": "created", "profile_path": "...", "validation": {...}}`
   - If `--headless:validate` → validate an existing profile. Return validate-profile.py JSON output.
   - If `--headless:load <name>` → read and return profile as structured JSON
   - If `--headless:edit <name>` → accept YAML field overrides, apply to existing profile, validate, save. Return JSON: `{"status": "updated", "profile_path": "...", "fields_changed": [...], "validation": {...}}`
   - If `--headless:delete <name>` → delete profile without confirmation. Return JSON: `{"status": "deleted", "profile_path": "..."}`
   - If `--headless:duplicate <source> <new_name>` → copy profile to new name. Return JSON: `{"status": "duplicated", "source": "...", "new_path": "..."}`
   - If just `--headless` → list all profiles as JSON array

2. **Interactive mode** (default): Proceed to On Activation below

## On Activation

1. **Load config via bmad-init skill** — Store all returned vars for use:
   - Use `{user_name}` from config for greeting
   - Use `{communication_language}` for all communications
   - Use `{document_output_language}` for profile content (genre descriptions, vocal direction, exclusions)
   - **Fallback:** If bmad-init config is unavailable, greet generically and default `{communication_language}` to English. Do not block the workflow on missing config.

2. **Greet user** as `{user_name}`, speaking in `{communication_language}`

3. **Detect operation** from user's request:

| Operation | Trigger | Route |
|-----------|---------|-------|
| **Create** | "create/new band/profile" | Create Profile |
| **List** | "list/show bands/profiles" | List Profiles |
| **Load** | "load/show/view [name]" | Load Profile |
| **Edit** | "edit/update/modify [name]" | Edit Profile |
| **Delete** | "delete/remove [name]" | Delete Profile |
| **Duplicate** | "clone/duplicate/fork [name]", "new version of [name]" | Duplicate Profile |
| **Analyze Voice** | "analyze voice/writing", provides samples | Analyze Writer Voice |
| **Health Check** | "check/review my profile", "is my profile good?" | Health Check |
| **Unclear** | — | Present the operations above and ask |
| **Wrong skill** | "make a song", "create music" | Explain this skill manages profiles, not songs. Suggest invoking the Band Manager agent or Style Prompt Builder instead. |

## Workflow Operations

### Create Profile

Guide the user through building a complete band profile conversationally. Load `references/profile-schema.md` for the full schema definition.

**Discovery flow — ask conversationally, not as a form:**

1. **Band name** — What's this project called?
2. **Instrumental or vocal?** — Is this a vocal project or instrumental-only? If instrumental, set `instrumental: true` and skip vocal direction later.
3. **Genre & mood baseline** — What does this band sound like? Use open-ended questions first.
4. **Reference tracks** — Actively prompt: "Name 2-3 artists or songs that capture the vibe you're after — I'll break down what makes them distinctive." Store both the raw references AND your sonic decomposition (what you'd pull from those references in terms of instrumentation, production style, vocal approach, energy, era) in the profile. **Research mandate:** Always use web search (when a search tool is available) to verify an artist's or song's sonic characteristics before decomposing — even for well-known artists. Search for genre, instrumentation, vocal style, production approach, and era. Only fall back to asking the user when no search tool is available. Never fabricate sonic descriptions — they flow into style prompts that Suno interprets literally.
5. **Language** — What language will the lyrics be in? Default to English if not specified.
6. **Model & tier** — Which Suno model/plan do they use? Run `scripts/tier-features.py` with their tier to show what's available.
7. **Vocal direction** (skip if instrumental) — Gender, tone, delivery, energy, diction. Be specific: "warm, breathy female vocal with indie folk phrasing" not just "female vocals." If they have a Suno Persona, capture both the name and the source song it was derived from.
8. **Style prompt baseline** — Build the default style prompt from their genre/mood/vocal/reference answers. Front-load essentials in the first 200 characters. Show them the draft, iterate.
9. **Exclusion defaults** — What should never appear? ("no autotune, no screaming"). Keep entries concise and specific; recommend max 5.
   **IMPORTANT:** Suno does not reliably process negative prompts ("no screaming", "no autotune"). These exclusion defaults are stored for reference and for the Exclude Styles field, but the Style Prompt Builder will automatically translate them into positive style prompt language when building prompts. For example, "no screaming" becomes "clean singing with grit on peaks" in the style prompt. Inform the user: "I'll save these exclusions, but when I build your style prompts I'll also phrase them positively — Suno responds better to what you DO want than what you don't."
10. **Creative settings** — Creativity mode preference (conservative/balanced/experimental). If on a paid tier, discuss Weirdness and Style Influence slider preferences (0-100, default 50). Explain what they do if the user is unsure.
11. **Persona reference** — Do they have an existing Suno Persona to link? (Name it clearly.) Note the source song for recreation.
12. **Writer voice** — Optional. Ask if they'd like to analyze their writing style now (→ Analyze Writer Voice) or skip for later.

Between sections, ask: "Anything else to add, or move on?" — do not auto-advance without user confirmation.

**Capture creative ideas:** If the user mentions song concepts, lyric fragments, or production experiments during discovery, silently note them. At the end: "I also captured these ideas you mentioned — want me to save them for when you create songs?"

**After discovery:**
- Assemble the profile YAML
- Run `scripts/validate-profile.py` to verify structure. Use `scripts/validate-profile.py --derive-filename "Band Name"` to get the correct kebab-case filename.
- **Generate a Band Identity Card** — a 3-4 sentence natural language summary of who this band is: genre, sound, vocal character, creative spirit. Present this first, then the YAML.
- Present the complete profile for review
- On approval, save to `docs/band-profiles/{profile-name}.yaml`

**Headless create:** Accept a complete or partial YAML profile. Validate with `scripts/validate-profile.py`. Save if valid, return errors if not.

### List Profiles

Run `scripts/list-profiles.py` to scan `docs/band-profiles/` and display all saved profiles with name, genre, model preference, language, and instrumental/vocal status.

If no profiles exist, suggest creating one.

### Load Profile

Use `scripts/list-profiles.py --check "{profile-name}"` to verify the profile exists and get its metadata. Then read from `docs/band-profiles/{profile-name}.yaml` and display in a readable format organized by section: identity, sound, vocals, creative settings, writer voice (if present), generation history (if present).

**Tier drift detection:** Compare the profile's stored tier against any known user tier (from agent memory or config). If they differ: "This profile was set up for {stored_tier} but you're now on {current_tier}. Want me to unlock the new tier's features?"

If the profile name is ambiguous, run `scripts/list-profiles.py` and ask the user to clarify.

### Edit Profile

Load the profile, accept natural language changes ("make it more aggressive", "switch to v5 Pro", "add exclusions for synth pads"), and apply to relevant fields. If tier changes, run `scripts/tier-features.py` to check feature availability and adjust profile accordingly. If genre, mood, or vocal fields change, suggest reviewing style_baseline: "Your genre changed — want me to update the style prompt baseline to match?"

Read both the target profile YAML and `references/profile-schema.md` in a single parallel batch when entering this operation.

Re-validate with `scripts/validate-profile.py`. Use `scripts/diff-profiles.py` to generate and show a structured diff of changes. Confirm with user, then save.

### Delete Profile

Confirm the profile exists (via `scripts/list-profiles.py --check`), show its summary, get explicit user confirmation ("Are you sure you want to delete [name]? This cannot be undone."), then delete `docs/band-profiles/{profile-name}.yaml`.

### Duplicate Profile

Copy an existing profile to a new name as a starting point for a new version, side project, or sound evolution experiment.

1. Load the source profile
2. Ask for the new profile name (or generate: "{original}-v{N+1}" for versioning, "{original}-{variant}" for forks)
3. Optionally increment the version field
4. Ask if they want to modify anything in the copy now, or save as-is and edit later
5. Validate and save the new profile

### Analyze Writer Voice

This operation extracts a writer's voice patterns from writing samples and stores them in a band profile.

1. **Collect samples** — Ask for 3-5 writing samples (poems, lyrics, prose). Ideal samples are 10-40 lines each. Guide them: "Pick pieces that feel most like YOU — your voice shines brightest in your favorites, not your experiments." Accept pasted text or file paths. If file paths, read all sample files in a single parallel batch before analyzing.

2. **Check existing voice** — If the target profile already has writer_voice data, present it and ask: "You already have a voice analysis. Want to replace it entirely with new samples, augment it with additional samples, or refine specific dimensions?"

3. **Extract patterns** — Analyze across all samples for:
   - **Vocabulary preferences** — formal/casual, abstract/concrete, archaic/modern, domain-specific words
   - **Sentence rhythm** — short punchy vs. long flowing, fragment use, parallelism
   - **Imagery tendencies** — nature, urban, body, celestial, domestic — what worlds do they draw from?
   - **Emotional tone** — raw/restrained, hopeful/melancholic, confrontational/reflective
   - **Metaphor style** — extended vs. quick, conventional vs. surprising, frequency
   - **Repetition patterns** — anaphora, refrains, echo structures, callback patterns

4. **Present analysis** — Show the extracted voice profile with example quotes from their samples that illustrate each pattern. This is the user's chance to say "that's not me" or "yes, exactly."

5. **Store** — Save as the `writer_voice` section of the specified band profile. If no band profile specified, ask which one (or create a new one).

### Health Check

Assess a profile's completeness and quality beyond structural validation — is it "good enough" to produce great Suno output?

1. Run `scripts/validate-profile.py` for structural validity
2. Assess quality dimensions:
   - **style_baseline specificity** — Is it vague ("rock music") or detailed ("warm indie rock with tremolo guitar, lo-fi tape saturation, and intimate mix")? Suggest improvements if vague.
   - **writer_voice population** — Is it empty? Suggest analyzing voice samples.
   - **reference_tracks presence** — Empty? Suggest adding references for better Style Prompt Builder results.
   - **exclusion_defaults thoughtfulness** — None set? Suggest common exclusions for the genre.
   - **vocal direction depth** — Present but generic? Suggest more specific descriptors.
   - **generation_history** — Any successful snapshots saved? If not, remind the user to save winners.
3. Present as friendly recommendations, not failures: "Your profile is valid and usable. Here's how to make it even better: ..."

## Post-Operation Flow

After completing any operation, offer to perform another operation or confirm the session is complete: "Anything else you'd like to do with your profiles, or are we good?"

## Scripts

Available scripts in `scripts/`:
- `validate-profile.py` — Validates band profile YAML against schema. Supports `--derive-filename "Band Name"` to get kebab-case filename. Run `scripts/validate-profile.py --help` for usage.
- `list-profiles.py` — Scans `docs/band-profiles/` and returns profile summaries. Supports `--check "profile-name"` to verify a specific profile exists. Run `scripts/list-profiles.py --help` for usage.
- `tier-features.py` — Returns available/unavailable Suno features for a given tier. Run `scripts/tier-features.py --help` for usage.
- `diff-profiles.py` — Compares two profile YAML files and returns structured JSON diff. Run `scripts/diff-profiles.py --help` for usage.
