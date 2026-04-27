#!/usr/bin/env bash
# Unpack portable session files from a sync archive.
# Extracts portable-sync.tar.gz into the project root, overwriting existing files.
#
# Usage: bash scripts/unpack-portable.sh [project-root]
#   project-root defaults to current directory

set -euo pipefail

PROJECT_ROOT="${1:-.}"
ARCHIVE="$PROJECT_ROOT/docs/portable-sync.tar.gz"

# Also check project root for backward compatibility
if [ ! -f "$ARCHIVE" ] && [ -f "$PROJECT_ROOT/portable-sync.tar.gz" ]; then
    ARCHIVE="$PROJECT_ROOT/portable-sync.tar.gz"
fi

if [ ! -f "$ARCHIVE" ]; then
    echo '{"status": "error", "message": "No portable-sync.tar.gz found in docs/ or project root."}'
    exit 1
fi

# List contents before extracting
FILE_COUNT=$(tar tzf "$ARCHIVE" | wc -l)

# Extract into project root
cd "$PROJECT_ROOT"
tar xzf "$ARCHIVE"

echo "{\"status\": \"success\", \"files_unpacked\": $FILE_COUNT}"
echo "Unpacked $FILE_COUNT files from $ARCHIVE" >&2

# Post-unpack reconciliation — warn if the sidecar's narrative may be stale
# relative to the unpacked files. Never blocks: reconciliation is the agent's
# job, not the script's. Bypass with BMAD_SKIP_RECONCILE=1.
RECONCILE="$PROJECT_ROOT/.claude/skills/suno-agent-band-manager/scripts/reconcile-sidecar.py"
if [ "${BMAD_SKIP_RECONCILE:-}" != "1" ] && [ -f "$RECONCILE" ] && command -v python3 >/dev/null 2>&1; then
    echo "" >&2
    echo "--- Post-unpack reconciliation check ---" >&2
    python3 "$RECONCILE" "$PROJECT_ROOT" >&2 || true
fi

# Optionally remove the archive after unpacking
# rm "$ARCHIVE"
