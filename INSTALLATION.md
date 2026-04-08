# Installation Guide

Mac follows the [Agent Skills](https://agentskills.io) open standard. The same SKILL.md files work across multiple LLM CLI tools. Choose the installation path that matches your setup.

## Standalone Installation (Recommended)

Works with any LLM CLI that supports Agent Skills: Claude Code, Gemini CLI, Codex CLI, GitHub Copilot, Windsurf, OpenCode.

### 1. Clone the repository

```bash
git clone https://github.com/zarlor/bmad-suno-band-manager.git
cd bmad-suno-band-manager
```

### 2. Link skills

```bash
./link-skills.sh
```

This creates symlinks in both `.claude/skills/` and `.agents/skills/`. The `.agents/skills/` path is the portable standard scanned by most LLM CLI tools.

### 3. First-run setup

Activate Mac using your tool's skill invocation. On first run, Mac walks you through setup interactively — Suno tier, interaction mode, preferences. No manual config files needed.

**Claude Code:**
```
/bmad-suno-agent-band-manager
```

**Gemini CLI:**
Activate the `bmad-suno-agent-band-manager` skill via Gemini's skill activation flow.

**Other tools:**
Skills in `.agents/skills/` are auto-discovered at session start. Invoke by name or description match.

### 4. Start creating

Tell Mac what kind of song you want. See the [Usage Guide](USAGE.md) for all features.

---

## Installation with BMad Method

If you use [BMad Method](https://github.com/bmad-code-org/BMAD-METHOD/) (v6.2.0+), the module integrates with BMad's config management and help system.

### 1. Clone and install BMad

```bash
git clone https://github.com/zarlor/bmad-suno-band-manager.git
cd bmad-suno-band-manager
npx bmad-method@next install
```

### 2. Link skills and run setup

```bash
./link-skills.sh
/bmad-suno-setup
```

The setup skill configures Suno tier, interaction mode, folder paths, and registers capabilities with BMad's help system.

---

## Pipeline Guard (Recommended)

The module ships a Stop hook script (`scripts/pipeline-guard.py`) that enforces Mac's mandatory production pipeline. It blocks any response containing a Suno package if `suno-style-prompt-builder` and `suno-lyric-transformer` weren't invoked during the session.

**Why:** Without this guard, the agent may hand-build packages from conversation memory instead of running them through the skills. The skills contain critical guardrails (artist name detection, production descriptor checks, character budget validation, section tag validation) that cannot be replicated from memory.

**Auto-configuration:** Running `suno-setup` offers to configure the pipeline guard automatically — both the Claude Code Stop hook and the cross-platform AGENTS.md standing order. The manual steps below are for reference or if you prefer to set it up yourself.

### Claude Code Setup

Add to your `.claude/settings.local.json` (create if it doesn't exist):

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR\"/_bmad-output/suno-band-manager/scripts/pipeline-guard.py",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

Adjust the path to match where you cloned the module. If using a standalone install, the path would be relative to your project root.

### Standing Order (All Platforms)

For additional reinforcement, add this to your project instruction file (`CLAUDE.md`, `AGENTS.md`, or `GEMINI.md`):

```markdown
## Suno Pipeline Rule (MANDATORY)

When the suno-agent-band-manager skill is active, NEVER hand-build a Suno package. ALWAYS invoke suno-style-prompt-builder and suno-lyric-transformer via the Skill tool before presenting any style prompt + lyrics + settings package.
```

---

## Tool-Specific Notes

### Claude Code

Primary development and testing platform. Full feature support including:
- Skill invocation via `/bmad-suno-agent-band-manager`
- Sub-agent spawning for parallel skill execution
- Bash tool for Python script execution (validation, analysis)
- Full read/write file access for memory, profiles, songbook
- Pipeline guard Stop hook (see above)

Skills discovered from: `.claude/skills/`, `.agents/skills/`

### Gemini CLI

Skills discovered from: `.agents/skills/`, `.gemini/skills/`

Gemini CLI uses the same SKILL.md format. The skill activates when Gemini identifies a matching task from the skill description. User approval is requested before activation.

If you prefer Gemini's native path, you can additionally symlink into `.gemini/skills/`:
```bash
mkdir -p .gemini/skills
for skill in src/skills/bmad-suno-*/; do
  ln -s "../../$skill" ".gemini/skills/$(basename "$skill")" 2>/dev/null
done
```

### Codex CLI (OpenAI)

Skills discovered from: `.agents/skills/`

Codex uses the same SKILL.md format. Skills can be invoked explicitly via `$skill-name` or through the `/skills` menu.

Custom instructions live in `AGENTS.md` (Codex's equivalent of `CLAUDE.md`). The module does not require an `AGENTS.md` file but you can create one for project-level instructions.

### GitHub Copilot

Skills discovered from: `.agents/skills/`, `.github/skills/`, `.claude/skills/`

Works across Copilot coding agent, Copilot CLI, and VS Code agent mode.

### Windsurf

Skills discovered from: `.agents/skills/`, `.windsurf/skills/`

Activate skills via `@skill-name` in Cascade input.

### OpenCode

Skills discovered from: `.agents/skills/`, `.opencode/skills/`, `.claude/skills/`

OpenCode also supports custom agent definitions in `.opencode/agents/` with granular per-agent tool permissions.

### Cursor

Skills discovered from: `.cursor/skills/` only (does not scan `.agents/skills/`).

Cursor requires skills in its own directory. Copy (don't symlink) if symlinks cause issues:
```bash
mkdir -p .cursor/skills
cp -r src/skills/bmad-suno-* .cursor/skills/
```

Note: Copying means `git pull` won't auto-update Cursor's copies. Re-copy after updates.

### Aider

Aider does not support the Agent Skills format. You can load reference documents manually:
```bash
aider --read SUNO-REFERENCE.md --read USAGE.md
```

This provides Suno context but not the interactive Mac workflow.

---

## Standalone Configuration (without BMad)

When installed standalone (no `_bmad/` directory), Mac uses sensible defaults on first run:
- **Suno tier:** Free (configurable through conversation — "I'm on Pro")
- **Interaction mode:** Demo (configurable — "switch to Studio mode")
- **Band profiles:** `docs/band-profiles/`
- **Songbook:** `docs/songbook/`

All preferences are saved to Mac's memory system and persist across sessions. No manual config file is required.

If you prefer to pre-configure, create `_bmad/config.yaml` and `_bmad/config.user.yaml` manually:

```yaml
# _bmad/config.yaml
document_output_language: English
output_folder: '{project-root}/_bmad-output'
suno:
  name: BMad Suno Band Manager
  version: 1.3.0
  suno_tier: pro          # free, pro, or premier
  default_mode: studio    # demo, studio, or jam
  band_profiles_folder: '{project-root}/docs/band-profiles'
  songbook_folder: '{project-root}/docs/songbook'
```

```yaml
# _bmad/config.user.yaml (gitignored — personal settings)
user_name: Your Name
communication_language: English
```

---

## Updating

```bash
git pull
```

Symlinks point into `src/skills/`, so changes are picked up immediately. If the update includes new config options, Mac will detect them on next activation.

### After a BMad Method upgrade

BMad upgrades may replace `.claude/skills/` contents. Re-run:
```bash
./link-skills.sh
/bmad-suno-setup
```

Your `.agents/skills/` symlinks, config, profiles, songbook, and memory are unaffected.

---

## Optional: Audio Analysis

For objective audio measurements (BPM, key, energy, chord progressions, playlist sequencing):

```bash
pip install librosa numpy
```

Mac will offer to help install these if you try to use audio analysis features without them. The full song creation and refinement workflow works without them.

---

## Troubleshooting

**Skills not discovered:** Verify symlinks exist in the expected directory for your tool. Run `ls -la .agents/skills/` to check.

**Permission denied on link-skills.sh:** Run `chmod +x link-skills.sh` first.

**Python scripts fail:** Ensure Python 3.9+ is available. Mac's scripts use only standard library modules (no pip dependencies except optional librosa/numpy).

**Config not found warnings:** Safe to ignore on standalone installs. Mac uses defaults and discovers preferences through conversation.

**Symlinks not working (Windows):** On Windows without WSL, symlinks may require developer mode or admin privileges. Consider copying skills directly instead of symlinking.
