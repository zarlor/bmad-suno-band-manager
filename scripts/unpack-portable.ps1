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

# Optionally remove the archive after unpacking
# Remove-Item $Archive
