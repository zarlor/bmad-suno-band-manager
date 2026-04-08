#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Configure pipeline guard hook for Claude Code and standing order for all platforms.

Merges the pipeline guard Stop hook into .claude/settings.local.json
and/or appends the standing order to AGENTS.md. Idempotent — skips
if already configured.

Usage:
    python3 scripts/configure-guard.py --settings-path PATH --guard-script-path PATH
    python3 scripts/configure-guard.py --agents-md-path PATH
    python3 scripts/configure-guard.py --settings-path PATH --agents-md-path PATH

Options:
    --settings-path     Path to .claude/settings.local.json
    --guard-script-path Relative path from project root to pipeline-guard.py
    --agents-md-path    Path to AGENTS.md (or CLAUDE.md / GEMINI.md)
    -o, --output        Write JSON output to file instead of stdout
"""

import argparse
import json
import sys
from pathlib import Path

STANDING_ORDER = """
## Suno Pipeline Rule (MANDATORY)

When the suno-agent-band-manager skill is active, NEVER hand-build a Suno package. ALWAYS invoke suno-style-prompt-builder and suno-lyric-transformer via the Skill tool before presenting any style prompt + lyrics + settings package. This rule exists because the skill reference files contain critical guardrails (artist name detection, production descriptor checks, character budget validation, section tag validation) that cannot be replicated from conversation memory.
""".strip()

STANDING_ORDER_MARKER = "## Suno Pipeline Rule"


def configure_claude_hook(settings_path: Path, guard_script_path: str) -> dict:
    """Merge pipeline guard Stop hook into Claude Code settings."""
    result = {"target": "claude_hook", "path": str(settings_path)}

    # Load existing settings
    if settings_path.is_file():
        try:
            existing = json.loads(settings_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {**result, "status": "error", "message": "Malformed JSON in settings file. Fix manually or delete to recreate."}
    else:
        existing = {}

    # Ensure hooks.Stop structure exists
    hooks = existing.setdefault("hooks", {})
    stop_hooks = hooks.setdefault("Stop", [])

    # Check if already configured
    for entry in stop_hooks:
        for hook in entry.get("hooks", []):
            if "pipeline-guard" in hook.get("command", ""):
                return {**result, "status": "already_configured"}

    # Build the hook command
    command = f'python3 "$CLAUDE_PROJECT_DIR"/{guard_script_path}'

    # Append new entry
    stop_hooks.append({
        "hooks": [{
            "type": "command",
            "command": command,
            "timeout": 10,
        }]
    })

    # Write back
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings_path.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")

    return {**result, "status": "configured"}


def configure_standing_order(md_path: Path) -> dict:
    """Append standing order to a markdown instruction file."""
    result = {"target": "standing_order", "path": str(md_path)}

    # Check if already present
    if md_path.is_file():
        content = md_path.read_text(encoding="utf-8")
        if STANDING_ORDER_MARKER in content:
            return {**result, "status": "already_configured"}
        # Append with separator
        if content and not content.endswith("\n\n"):
            content = content.rstrip("\n") + "\n\n"
        content += STANDING_ORDER + "\n"
    else:
        content = STANDING_ORDER + "\n"

    md_path.write_text(content, encoding="utf-8")
    return {**result, "status": "configured"}


def main():
    parser = argparse.ArgumentParser(description="Configure pipeline guard")
    parser.add_argument("--settings-path", help="Path to .claude/settings.local.json")
    parser.add_argument("--guard-script-path", help="Relative path to pipeline-guard.py from project root")
    parser.add_argument("--agents-md-path", help="Path to AGENTS.md (or CLAUDE.md / GEMINI.md)")
    parser.add_argument("-o", "--output", help="Output file path")
    args = parser.parse_args()

    results = []

    if args.settings_path and args.guard_script_path:
        results.append(configure_claude_hook(
            Path(args.settings_path),
            args.guard_script_path,
        ))

    if args.agents_md_path:
        results.append(configure_standing_order(Path(args.agents_md_path)))

    if not results:
        results.append({"status": "error", "message": "No configuration targets specified. Use --settings-path and/or --agents-md-path."})

    output = json.dumps({"results": results}, indent=2)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Results written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
