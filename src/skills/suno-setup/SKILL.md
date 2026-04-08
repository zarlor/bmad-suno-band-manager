---
name: suno-setup
description: Sets up Suno Band Manager module in a project. Use when the user requests to 'install suno module', 'configure Suno Band Manager', or 'setup Suno Band Manager'.
---

# Module Setup

## Overview

Installs and configures a BMad module into a project. Module identity (name, code, version) comes from `./assets/module.yaml`. Collects user preferences and writes them to three files:

- **`{project-root}/_bmad/config.yaml`** — shared project config: core settings at root (e.g. `output_folder`, `document_output_language`) plus a section per module with metadata and module-specific values. User-only keys (`user_name`, `communication_language`) are **never** written here.
- **`{project-root}/_bmad/config.user.yaml`** — personal settings intended to be gitignored: `user_name`, `communication_language`, and any module variable marked `user_setting: true` in `./assets/module.yaml`. These values live exclusively here.
- **`{project-root}/_bmad/module-help.csv`** — registers module capabilities for the help system.
- **`{project-root}/_bmad/core/config.yaml`** and **`{project-root}/_bmad/suno/config.yaml`** — per-module config files written automatically by `merge-config.py` so that `bmad-init` can load config at runtime. These bridge the shared config format with `bmad-init`'s expected per-module layout.

Both config scripts use an anti-zombie pattern — existing entries for this module are removed before writing fresh ones, so stale values never persist.

`{project-root}` is a **literal token** in config values — never substitute it with an actual path. It signals to the consuming LLM that the value is relative to the project root, not the skill root.

## On Activation

1. Read `./assets/module.yaml` for module metadata and variable definitions (the `code` field is the module identifier)
2. **Detect installation mode:**
   - If `{project-root}/_bmad/config.yaml` exists with a section for this module → this is an **update**
   - If `{project-root}/_bmad/` exists but no module section → this is a **fresh BMad install**
   - If `{project-root}/_bmad/` does not exist → this is a **standalone install**. Create `_bmad/` and proceed with defaults. Inform the user: "Setting up standalone — no BMad Method detected, using direct configuration."
3. Check for per-module configuration at `{project-root}/_bmad/suno/config.yaml` and `{project-root}/_bmad/core/config.yaml`. If either file exists:
   - If `{project-root}/_bmad/config.yaml` does **not** yet have a section for this module: this is a **fresh install**. Inform the user that installer config was detected and values will be consolidated into the new format.
   - If `{project-root}/_bmad/config.yaml` **already** has a section for this module: this is a **legacy migration**. Inform the user that legacy per-module config was found alongside existing config, and legacy values will be used as fallback defaults.
   - In both cases, per-module config files and directories will be cleaned up after setup.

If the user provides arguments (e.g. `accept all defaults`, `--headless`, or inline values like `user name is BMad, I speak Swahili`), map any provided values to config keys, use defaults for the rest, and skip interactive prompting. Still display the full confirmation summary at the end.

## Collect Configuration

Ask the user for values. Show defaults in brackets. Present all values together so the user can respond once with only the values they want to change (e.g. "change language to Swahili, rest are fine"). Never tell the user to "press enter" or "leave blank" — in a chat interface they must type something to respond.

**Default priority** (highest wins): existing new config values > legacy config values > `./assets/module.yaml` defaults. When legacy configs exist, read them and use matching values as defaults instead of `module.yaml` defaults. Only keys that match the current schema are carried forward — changed or removed keys are ignored.

**Core config** (only if no core keys exist yet): `user_name` (default: BMad), `communication_language` and `document_output_language` (default: English — ask as a single language question, both keys get the same answer), `output_folder` (default: `{project-root}/_bmad-output`). Of these, `user_name` and `communication_language` are written exclusively to `config.user.yaml`. The rest go to `config.yaml` at root and are shared across all modules.

**Module config**: Read each variable in `./assets/module.yaml` that has a `prompt` field. Ask using that prompt with its default value (or legacy value if available).

## Write Files

Write a temp JSON file with the collected answers structured as `{"core": {...}, "module": {...}}` (omit `core` if it already exists). Then run both scripts — they can run in parallel since they write to different files:

```bash
python3 ./scripts/merge-config.py --config-path "{project-root}/_bmad/config.yaml" --user-config-path "{project-root}/_bmad/config.user.yaml" --module-yaml ./assets/module.yaml --answers {temp-file} --legacy-dir "{project-root}/_bmad"
python3 ./scripts/merge-help-csv.py --target "{project-root}/_bmad/module-help.csv" --source ./assets/module-help.csv --legacy-dir "{project-root}/_bmad" --module-code suno
```

Both scripts output JSON to stdout with results. If either exits non-zero, surface the error and stop. The scripts automatically read legacy config values as fallback defaults, then delete the legacy files after a successful merge. `merge-config.py` also writes per-module config files (`_bmad/core/config.yaml` and `_bmad/suno/config.yaml`) that `bmad-init` reads at runtime. Check `legacy_configs_deleted`, `legacy_csvs_deleted`, and `init_configs_written` in the output to confirm.

Run `./scripts/merge-config.py --help` or `./scripts/merge-help-csv.py --help` for full usage.

## Create Output Directories

After writing config, create any output directories that were configured. For filesystem operations only (such as creating directories), resolve the `{project-root}` token to the actual project root and create each path-type value from `config.yaml` that does not yet exist — this includes `output_folder` and any module variable whose value starts with `{project-root}/`. The paths stored in the config files must continue to use the literal `{project-root}` token; only the directories on disk should use the resolved paths. Use `mkdir -p` or equivalent to create the full path.

## Cleanup Legacy Directories

After both merge scripts complete successfully, remove the installer's package directories. Skills and agents in these directories are already installed at `.claude/skills/` — the `_bmad/` directory should only contain config files.

```bash
python3 ./scripts/cleanup-legacy.py --bmad-dir "{project-root}/_bmad" --module-code suno --also-remove _config --skills-dir "{project-root}/.claude/skills"
```

The script verifies that every skill in the legacy directories exists at `.claude/skills/` before removing anything. Directories without skills (like `_config/`) are removed directly. The script preserves `config.yaml` files in directories being cleaned — `bmad-init` needs these per-module config files at runtime. If the script exits non-zero, surface the error and stop. Missing directories (already cleaned by a prior run) are not errors — the script is idempotent.

Check `directories_removed` and `files_removed_count` in the JSON output for the confirmation step. Run `./scripts/cleanup-legacy.py --help` for full usage.

## Configure Pipeline Guard (Optional)

After config and cleanup are complete, offer to configure the pipeline guard. The guard enforces Mac's mandatory production pipeline — it prevents hand-building Suno packages without running the formal skill pipeline (Style Prompt Builder + Lyric Transformer).

Ask: "Want me to set up the pipeline guard? It ensures Mac always runs the production skills before presenting a Suno package. I can configure it for your coding tool."

If the user declines, skip to Confirm.

If the user accepts, configure both layers:

### Claude Code Stop Hook

If the project has a `.claude/` directory (indicating Claude Code usage), configure the deterministic Stop hook:

```bash
python3 ./scripts/configure-guard.py --settings-path "{project-root}/.claude/settings.local.json" --guard-script-path "scripts/pipeline-guard.py"
```

The script merges the hook into existing settings without overwriting other configuration. It's idempotent — skips if already configured. Check the JSON output for `status` ("configured", "already_configured", or "error").

**Path note:** The hook command uses `$CLAUDE_PROJECT_DIR` (a Claude Code environment variable) so it works regardless of where the project lives on disk.

### Standing Order (All Platforms)

Configure the cross-platform standing order in `AGENTS.md` — readable by Codex CLI, Cursor, GitHub Copilot, Windsurf, Amp, and Gemini CLI (when configured to read AGENTS.md):

```bash
python3 ./scripts/configure-guard.py --agents-md-path "{project-root}/AGENTS.md"
```

The script appends the standing order section to AGENTS.md (creates the file if it doesn't exist). Idempotent — skips if the section already exists.

**Both commands can run in parallel** since they write to different files. Report what was configured in the Confirm step.

## Confirm

Use the script JSON output to display what was written — config values set (written to `config.yaml` at root for core, module section for module values), user settings written to `config.user.yaml` (`user_keys` in result), init-compatible per-module configs written (`init_configs_written`), help entries added, fresh install vs update. If legacy files were deleted, mention the migration. If legacy directories were removed, report the count and list (e.g. "Cleaned up 106 installer package files from bmb/, core/, \_config/ — skills are installed at .claude/skills/"). Then display the `module_greeting` from `./assets/module.yaml` to the user.

## Outcome

Once the user's `user_name` and `communication_language` are known (from collected input, arguments, or existing config), use them consistently for the remainder of the session: address the user by their configured name and communicate in their configured `communication_language`.
