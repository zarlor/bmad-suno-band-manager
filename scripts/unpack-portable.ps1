#!/usr/bin/env pwsh
# Unpack portable session files from a sync archive (Windows / PowerShell).
# Extracts portable-sync.tar.gz into the project root, overwriting existing files.
#
# Requirements: Windows 10 1803+ ships with tar.exe. On older Windows, install
# Git for Windows (which includes tar) or use WSL.

param(
    [string]$ProjectRoot = '.'
)

$ErrorActionPreference = 'Stop'

$Archive = Join-Path $ProjectRoot 'docs/portable-sync.tar.gz'

# Backward compatibility: also check project root
if (-not (Test-Path $Archive)) {
    $altArchive = Join-Path $ProjectRoot 'portable-sync.tar.gz'
    if (Test-Path $altArchive) {
        $Archive = $altArchive
    }
}

if (-not (Test-Path $Archive)) {
    Write-Output '{"status": "error", "message": "No portable-sync.tar.gz found in docs/ or project root."}'
    exit 1
}

# Count contents before extracting
$fileCount = (& tar -tzf $Archive | Measure-Object -Line).Lines

# Extract into project root
Push-Location $ProjectRoot
try {
    & tar -xzf $Archive
    if ($LASTEXITCODE -ne 0) {
        throw "tar extract exited with code $LASTEXITCODE"
    }
} finally {
    Pop-Location
}

Write-Output ('{"status": "success", "files_unpacked": ' + $fileCount + '}')
[Console]::Error.WriteLine("Unpacked $fileCount files from $Archive")

# Post-unpack reconciliation — warn if the sidecar narrative may be stale
# relative to the unpacked files. Never blocks: reconciliation is the agent's
# job, not the script's. Bypass with $env:BMAD_SKIP_RECONCILE=1.
$reconcile = Join-Path $ProjectRoot '.claude/skills/suno-agent-band-manager/scripts/reconcile-sidecar.py'
if ($env:BMAD_SKIP_RECONCILE -ne '1' -and (Test-Path $reconcile)) {
    $py = $null
    foreach ($candidate in @('python3', 'python')) {
        if (Get-Command $candidate -ErrorAction SilentlyContinue) { $py = $candidate; break }
    }
    if ($py) {
        [Console]::Error.WriteLine("")
        [Console]::Error.WriteLine("--- Post-unpack reconciliation check ---")
        try {
            & $py $reconcile $ProjectRoot 2>&1 | ForEach-Object { [Console]::Error.WriteLine($_) }
        } catch {
            [Console]::Error.WriteLine("reconcile-sidecar.py skipped: $_")
        }
    }
}

# Optionally remove the archive after unpacking
# Remove-Item $Archive
