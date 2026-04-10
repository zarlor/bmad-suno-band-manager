#!/usr/bin/env bash
# Pack portable session files for multi-machine sync.
# Creates portable-sync.tar.gz in docs/ under the project root.
#
# This bundles the user-generated content that lives in docs/ — voice files,
# band profiles, songbook, WIP files — so it can move between machines
# without going through git.
#
# Usage: bash scripts/pack-portable.sh [project-root]
#   project-root defaults to current directory
#
# Customization:
#   Create portable-manifest.yaml at the project root to control which files
#   get packed. See portable-manifest.example.yaml for the format. Without a
#   manifest, the defaults below pack the documented Suno module data dirs.
#
# Windows: see scripts/pack-portable.ps1 for the PowerShell equivalent.

set -euo pipefail

PROJECT_ROOT="${1:-.}"
ARCHIVE="$PROJECT_ROOT/docs/portable-sync.tar.gz"
MANIFEST="$PROJECT_ROOT/portable-manifest.yaml"

# Build file list from manifest if it exists, otherwise use defaults
FILES=()

add_glob() {
    local pattern="$1"
    local matches
    matches=$(find "$PROJECT_ROOT" -path "$PROJECT_ROOT/$pattern" -type f 2>/dev/null || true)
    if [ -n "$matches" ]; then
        while IFS= read -r f; do
            FILES+=("${f#$PROJECT_ROOT/}")
        done <<< "$matches"
    fi
}

if [ -f "$MANIFEST" ]; then
    # Read includes from manifest (lines under "include:" that start with "- ")
    while IFS= read -r line; do
        pattern="${line#- }"
        pattern="${pattern#\"}"
        pattern="${pattern%\"}"
        add_glob "$pattern"
    done < <(sed -n '/^include:/,/^[^ -]/{ /^  *- /p }' "$MANIFEST")
else
    # Default patterns: documented Suno module data conventions only.
    # Anything outside these (custom companion files, session findings, etc.)
    # belongs in portable-manifest.yaml — see portable-manifest.example.yaml.
    add_glob "docs/voice-context-*.md"
    add_glob "docs/songbook/**/*.md"
    add_glob "docs/band-profiles/**/*.yaml"
    add_glob "docs/wip-*.md"
fi

if [ ${#FILES[@]} -eq 0 ]; then
    echo '{"status": "empty", "message": "No portable files found to pack."}'
    exit 0
fi

# Create archive
mkdir -p "$PROJECT_ROOT/docs"
cd "$PROJECT_ROOT"
tar czf "$ARCHIVE" "${FILES[@]}"

echo "{\"status\": \"success\", \"archive\": \"$ARCHIVE\", \"files_packed\": ${#FILES[@]}}"
echo "Files packed:" >&2
printf '  %s\n' "${FILES[@]}" >&2
