#!/bin/bash
# Restore Suno module symlinks in .claude/skills/
# Run this after a BMad Method upgrade or fresh clone.

set -e
cd "$(dirname "$0")"
mkdir -p .claude/skills

linked=0
for skill in src/skills/bmad-suno-*/; do
  name=$(basename "$skill")
  target="../../$skill"
  if [ -L ".claude/skills/$name" ]; then
    echo "  exists: $name"
  else
    ln -s "$target" ".claude/skills/$name"
    echo "  linked: $name"
    linked=$((linked + 1))
  fi
done

if [ "$linked" -eq 0 ]; then
  echo "All Suno skills already linked."
else
  echo "$linked skill(s) linked. Run /bmad-suno-setup to complete configuration."
fi
