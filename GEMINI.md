# Suno Band Manager — Project Standing Orders

This file contains standing orders that apply to any LLM agent working in this repository. It is loaded automatically by Gemini CLI, Claude Code (`CLAUDE.md`), and Codex CLI / OpenCode (`AGENTS.md`) — three separate files with identical content for cross-tool compatibility.

## Skill Activation Discipline (MANDATORY)

When activating any skill in this module — `suno-agent-band-manager`, `suno-band-profile-manager`, `suno-style-prompt-builder`, `suno-lyric-transformer`, `suno-feedback-elicitor`, or `suno-setup` — you MUST follow the "On Activation" instructions in the skill's `SKILL.md` exactly:

1. **Execute any scripts** referenced in the activation block (e.g., `pre-activate.py`, `check-memory-health.py`, `validate-path.py`) using your shell tool. Do not skip these — they emit dynamic menu data and pre-load required state. The menu you present to the user MUST come from the script output, not from a hardcoded approximation derived from `SKILL.md` text.

2. **Read ALL referenced reference files** (e.g., `persona.md`, `creed.md`, `capabilities.md`, `activation.md`, `memory-system.md`) before responding to the user. The persona and creed files define how you should communicate; skipping them produces a generic response that breaks the user experience and forces the user to manually re-instruct you on their preferred interaction style.

3. **Present the dynamic menu** from the script output (e.g., from `pre-activate.py`), not a hardcoded approximation derived from your interpretation of `SKILL.md`. Missing menu items confuse users who expect a complete capability list.

4. **Load voice context** (`docs/voice-context-{username}.md` if it exists) before greeting. This is the user's durable creative identity file — without it, you have no context about who you're working with, their creative history, their preferences, or their active projects.

5. **Internalize persona vocabulary, do not enumerate it.** When `persona.md` lists vocabulary or phrasing examples (e.g., NOLA voice terms), treat them as voice grounding to be sampled naturally, NOT as a checklist to use exhaustively in a single response.

## Suno Pipeline Rule (MANDATORY)

When the `suno-agent-band-manager` skill is active, NEVER hand-build a Suno package from conversation memory. ALWAYS invoke `suno-style-prompt-builder` and `suno-lyric-transformer` via your skill/tool invocation mechanism before presenting any style prompt + lyrics + settings package to the user.

The skills contain critical guardrails (artist name detection, production descriptor checks, character budget validation, section tag validation, current-prompt-only exclusion reasoning) that cannot be reliably replicated from memory. Skipping them produces packages that look correct but fail in Suno or violate documented constraints.

**The full rule, including Pre-Output Self-Check and Violation Tells, lives in the agent's creed** (`src/skills/suno-agent-band-manager/references/creed.md` → "Package Assembly Rule") which is loaded on every agent activation. This root file is a brief cross-tool reinforcement — the authoritative rule is in the creed.

## Why This File Exists

The activation rules used to live only inside individual `SKILL.md` files in a declarative style ("Load config...", "Route by state..."). That style works in Claude Code because the harness adds scaffolding around skill activation, but in Gemini CLI, Codex CLI, OpenCode, and other LLM CLIs, the model sees the `SKILL.md` text more literally and may treat the activation steps as optional reading rather than mandatory tool calls.

This file makes the activation discipline explicit and tool-agnostic. It is loaded into every session automatically by the LLM CLI, so the standing orders are always present regardless of which skill activates or how the model interprets `SKILL.md`.

## Cross-References

- `INSTALLATION.md` — Setup instructions for all supported LLM CLIs (Claude Code, Gemini CLI, Codex CLI, GitHub Copilot, Windsurf, OpenCode, Cursor, Aider)
- `src/skills/suno-agent-band-manager/references/USAGE.md` — End-user guide
- `README.md` — Module overview and architecture
- `src/skills/*/SKILL.md` — Per-skill activation and capability definitions
