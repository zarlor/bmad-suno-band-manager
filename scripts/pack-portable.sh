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
VALIDATOR="$PROJECT_ROOT/.claude/skills/suno-agent-band-manager/scripts/validate-sidecar.py"

# Pre-sync validation gate. Stops stale sidecar state from propagating to
# other machines. The validator reads songbook + band profiles + sidecar
# index and reports drift. Exit code 1 from the validator blocks the pack.
# Warnings (pre-existing content gaps) do not block.
#
# Bypass: set BMAD_SKIP_VALIDATE=1 to skip (e.g., emergency syncs). Missing
# validator script or missing Python falls through gracefully with a warning
# so older installs keep working.
if [ "${BMAD_SKIP_VALIDATE:-0}" = "1" ]; then
    echo "NOTE: BMAD_SKIP_VALIDATE=1 — skipping sidecar validation." >&2
elif [ ! -f "$VALIDATOR" ]; then
    echo "NOTE: $VALIDATOR not found — skipping sidecar validation." >&2
elif ! command -v python3 >/dev/null 2>&1; then
    echo "NOTE: python3 not available — skipping sidecar validation." >&2
else
    if ! python3 "$VALIDATOR" "$PROJECT_ROOT" >&2; then
        echo "" >&2
        echo "ERROR: Sidecar validation failed — refusing to pack stale state." >&2
        echo "Fix the errors above, or override with BMAD_SKIP_VALIDATE=1 if intentional." >&2
        exit 1
    fi
fi

# Build file list from manifest if it exists, otherwise use defaults
FILES=()

add_glob() {
    local pattern="$1"
    local matches=""

    if [[ "$pattern" == *'**'* ]]; then
        # Recursive pattern: split at the first **, use the prefix as the base
        # directory and the suffix as the filename filter. This matches the
        # PowerShell version's Add-Glob recursive logic so cross-platform
        # manifests behave identically. Using find's default recursion means
        # the base directory's own files are matched along with nested ones,
        # which is the expected glob semantics for patterns like
        # docs/band-profiles/**/*.yaml (should match top-level AND nested).
        local prefix="${pattern%%\*\**}"   # Everything before the first **
        local suffix="${pattern#*\*\*}"    # Everything after the first **
        prefix="${prefix%/}"               # Strip trailing /
        suffix="${suffix#/}"               # Strip leading /
        [ -z "$suffix" ] && suffix="*"     # Default to * if no tail pattern
        local base="$PROJECT_ROOT"
        [ -n "$prefix" ] && base="$PROJECT_ROOT/$prefix"
        if [ ! -d "$base" ]; then
            return
        fi
        matches=$(find "$base" -type f -name "$suffix" 2>/dev/null || true)
    else
        # Non-recursive pattern: use find -path. In find -path, * matches any
        # character including /, so patterns with * will match across directory
        # boundaries. This is fine for flat patterns like docs/voice-context-*.md.
        matches=$(find "$PROJECT_ROOT" -path "$PROJECT_ROOT/$pattern" -type f 2>/dev/null || true)
    fi

    if [ -n "$matches" ]; then
        while IFS= read -r f; do
            FILES+=("${f#$PROJECT_ROOT/}")
        done <<< "$matches"
    fi
}

if [ -f "$MANIFEST" ]; then
    # Read includes from manifest (lines under "include:" that start with "- ").
    # Use sed to extract and strip the full prefix (leading whitespace + "- ")
    # plus trailing inline comments and surrounding quotes robustly. The
    # previous implementation used shell parameter expansion (${line#- }) which
    # did not strip YAML's standard leading indentation, so valid manifests
    # following portable-manifest.example.yaml silently packed nothing.
    while IFS= read -r pattern; do
        [ -n "$pattern" ] && add_glob "$pattern"
    done < <(sed -n '/^include:/,/^[^ #-]/{ /^[[:space:]]*-[[:space:]]/ { s/^[[:space:]]*-[[:space:]]*//; s/[[:space:]]*#.*$//; s/^"//; s/"$//; s/^'\''//; s/'\''$//; p; }; }' "$MANIFEST")
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
