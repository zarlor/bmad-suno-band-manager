#!/usr/bin/env pwsh
# Pack portable session files for multi-machine sync (Windows / PowerShell).
# Creates portable-sync.tar.gz in docs/ under the project root.
#
# This bundles the user-generated content that lives in docs/ -- voice files,
# band profiles, songbook, WIP files -- so it can move between machines
# without going through git.
#
# Customization:
#   Create portable-manifest.yaml at the project root to control which files
#   get packed. See portable-manifest.example.yaml for the format. Without a
#   manifest, the defaults below pack the documented Suno module data dirs.
#
# Requirements: Windows 10 1803+ ships with tar.exe. On older Windows, install
# Git for Windows (which includes tar) or use WSL.

param(
    [string]$ProjectRoot = '.'
)

$ErrorActionPreference = 'Stop'

$Archive = Join-Path $ProjectRoot 'docs/portable-sync.tar.gz'
$Manifest = Join-Path $ProjectRoot 'portable-manifest.yaml'
$Validator = Join-Path $ProjectRoot '.claude/skills/suno-agent-band-manager/scripts/validate-sidecar.py'

# Pre-sync validation gate. Stops stale sidecar state from propagating to
# other machines. The validator reads songbook + band profiles + sidecar
# index and reports drift. A non-zero exit from the validator blocks the
# pack. Warnings (pre-existing content gaps) do not block.
#
# Bypass: set $env:BMAD_SKIP_VALIDATE=1 to skip (e.g., emergency syncs).
# Missing validator script or missing Python falls through gracefully with
# a warning so older installs keep working.
if ($env:BMAD_SKIP_VALIDATE -eq '1') {
    [Console]::Error.WriteLine('NOTE: BMAD_SKIP_VALIDATE=1 -- skipping sidecar validation.')
} elseif (-not (Test-Path $Validator)) {
    [Console]::Error.WriteLine("NOTE: $Validator not found -- skipping sidecar validation.")
} else {
    $python = (Get-Command python3 -ErrorAction SilentlyContinue)
    if (-not $python) {
        $python = (Get-Command python -ErrorAction SilentlyContinue)
    }
    if (-not $python) {
        [Console]::Error.WriteLine('NOTE: python not available -- skipping sidecar validation.')
    } else {
        & $python.Source $Validator $ProjectRoot 1>&2
        if ($LASTEXITCODE -ne 0) {
            [Console]::Error.WriteLine('')
            [Console]::Error.WriteLine('ERROR: Sidecar validation failed -- refusing to pack stale state.')
            [Console]::Error.WriteLine('Fix the errors above, or override with $env:BMAD_SKIP_VALIDATE=1 if intentional.')
            exit 1
        }
    }
}

$files = New-Object System.Collections.Generic.List[string]

function Add-Glob {
    param([string]$Pattern)

    $rootAbs = (Resolve-Path $ProjectRoot).Path

    # Handle recursive patterns containing **
    if ($Pattern -match '\*\*') {
        $idx = $Pattern.IndexOf('**')
        $baseRel = $Pattern.Substring(0, $idx).TrimEnd('/', '\')
        $tailPattern = $Pattern.Substring($idx + 2).TrimStart('/', '\')
        if (-not $tailPattern) { $tailPattern = '*' }
        $base = if ($baseRel) { Join-Path $ProjectRoot $baseRel } else { $ProjectRoot }
        if (-not (Test-Path $base)) { return }
        $matches = Get-ChildItem -Path $base -Filter $tailPattern -File -Recurse -ErrorAction SilentlyContinue
    } else {
        $rooted = Join-Path $ProjectRoot $Pattern
        $matches = Get-ChildItem -Path $rooted -File -ErrorAction SilentlyContinue
    }

    foreach ($m in $matches) {
        $rel = $m.FullName.Substring($rootAbs.Length).TrimStart('\', '/').Replace('\', '/')
        $files.Add($rel) | Out-Null
    }
}

if (Test-Path $Manifest) {
    # Read includes from manifest (lines under "include:" that start with "- ").
    # Two-step extraction: match the payload between "- " and optional inline
    # comment, then trim whitespace and strip surrounding quotes (both " and ').
    # The previous regex excluded only " and #, so single-quoted YAML patterns
    # had the quotes captured as part of the pattern and failed to match.
    $inIncludes = $false
    foreach ($line in Get-Content $Manifest) {
        if ($line -match '^include:') {
            $inIncludes = $true
            continue
        }
        if ($inIncludes) {
            if ($line -match '^\s*-\s*(.+?)\s*(#.*)?$') {
                $pattern = $Matches[1].Trim().Trim('"').Trim("'")
                if ($pattern) {
                    Add-Glob $pattern
                }
            } elseif ($line -match '^\S' -and $line -notmatch '^\s*#') {
                $inIncludes = $false
            }
        }
    }
} else {
    # Default patterns: documented Suno module data conventions only.
    # Anything outside these (custom companion files, session findings, etc.)
    # belongs in portable-manifest.yaml -- see portable-manifest.example.yaml.
    Add-Glob 'docs/voice-context-*.md'
    Add-Glob 'docs/songbook/**/*.md'
    Add-Glob 'docs/band-profiles/**/*.yaml'
    Add-Glob 'docs/wip-*.md'
}

if ($files.Count -eq 0) {
    Write-Output '{"status": "empty", "message": "No portable files found to pack."}'
    exit 0
}

# Ensure docs/ exists for the archive output
$archiveDir = Split-Path -Parent $Archive
if (-not (Test-Path $archiveDir)) {
    New-Item -ItemType Directory -Path $archiveDir -Force | Out-Null
}

# Create archive using built-in tar (Win10 1803+) or Git Bash tar
Push-Location $ProjectRoot
try {
    & tar -czf $Archive @files
    if ($LASTEXITCODE -ne 0) {
        throw "tar exited with code $LASTEXITCODE"
    }
} finally {
    Pop-Location
}

Write-Output ('{"status": "success", "archive": "' + $Archive + '", "files_packed": ' + $files.Count + '}')
[Console]::Error.WriteLine("Files packed:")
foreach ($f in $files) { [Console]::Error.WriteLine("  $f") }
