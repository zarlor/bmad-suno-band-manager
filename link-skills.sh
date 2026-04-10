#!/bin/bash
# Restore Suno module symlinks for LLM CLI skill discovery.
# Creates symlinks in both .claude/skills/ and .agents/skills/ for
# maximum cross-tool compatibility (Agent Skills open standard).
#
# Supported by: Claude Code, Gemini CLI, Codex CLI, GitHub Copilot,
# Windsurf, OpenCode (via .agents/skills/)
#
# Run this after a BMad Method upgrade, fresh clone, or standalone install.

set -e
cd "$(dirname "$0")"

# Skill discovery directories — .claude/ for Claude Code backward compat,
# .agents/ for the portable Agent Skills standard, .gemini/ for Gemini CLI
# (Gemini's glob does not always follow symlinks in .agents/skills/, so it
# needs its own native scan path).
SKILL_DIRS=(".claude/skills" ".agents/skills" ".gemini/skills")

for dir in "${SKILL_DIRS[@]}"; do
  mkdir -p "$dir"
done

linked=0
for skill in src/skills/suno-*/; do
  name=$(basename "$skill")
  for dir in "${SKILL_DIRS[@]}"; do
    # Compute relative path from target dir to skill source
    target="../../$skill"
    if [ -L "$dir/$name" ]; then
      echo "  exists: $dir/$name"
    else
      ln -s "$target" "$dir/$name"
      echo "  linked: $dir/$name"
      linked=$((linked + 1))
    fi
  done
done

if [ "$linked" -eq 0 ]; then
  echo "All Suno skills already linked."
else
  echo "$linked link(s) created across skill directories."
  echo ""
  echo "Skill directories:"
  for dir in "${SKILL_DIRS[@]}"; do
    echo "  $dir/"
  done
  echo ""
  echo "Run /suno-setup to complete configuration (or configure manually — see INSTALLATION.md)."
fi
