#!/usr/bin/env bash
# Pack portable session files for multi-machine sync.
# Creates portable-sync.tar.gz in the project root.
#
# Usage: bash scripts/pack-portable.sh [project-root]
#   project-root defaults to current directory

set -euo pipefail

PROJECT_ROOT="${1:-.}"
ARCHIVE="$PROJECT_ROOT/portable-sync.tar.gz"
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
    # Default portable file patterns
    add_glob "docs/voice-context-*.md"
    add_glob "docs/songbook/**/*.md"
    add_glob "docs/band-profiles/**/*.yaml"
    add_glob "docs/*-playlist-ordering.md"
    add_glob "docs/*-playlist.yaml"
    add_glob "docs/audio-analysis-reference.md"
    add_glob "docs/catalog-analysis-report.md"
    add_glob "docs/session-findings-*.md"
    add_glob "docs/*-family-history-and-voice.md"
    add_glob "docs/wip-*.md"
fi

if [ ${#FILES[@]} -eq 0 ]; then
    echo '{"status": "empty", "message": "No portable files found to pack."}'
    exit 0
fi

# Create archive
cd "$PROJECT_ROOT"
tar czf portable-sync.tar.gz "${FILES[@]}"

echo "{\"status\": \"success\", \"archive\": \"portable-sync.tar.gz\", \"files_packed\": ${#FILES[@]}}"
echo "Files packed:" >&2
printf '  %s\n' "${FILES[@]}" >&2
