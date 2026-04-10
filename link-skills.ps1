#!/usr/bin/env pwsh
# Restore Suno module symlinks for LLM CLI skill discovery (Windows / PowerShell).
# Creates symlinks in both .claude/skills/ and .agents/skills/ for
# maximum cross-tool compatibility (Agent Skills open standard).
#
# Supported by: Claude Code, Gemini CLI, Codex CLI, GitHub Copilot,
# Windsurf, OpenCode (via .agents/skills/)
#
# Requires Developer Mode (Windows 10 1703+) OR running as Administrator.
# To enable Developer Mode: Settings -> Update & Security -> For developers -> Developer Mode.
#
# Run this after a BMad Method upgrade, fresh clone, or standalone install.

$ErrorActionPreference = 'Stop'

# Run from the repo root (script's own directory)
Set-Location -Path $PSScriptRoot

$SkillDirs = @('.claude/skills', '.agents/skills')

foreach ($dir in $SkillDirs) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
}

$linked = 0
$skillFolders = Get-ChildItem -Path 'src/skills' -Directory -Filter 'suno-*' -ErrorAction Stop

foreach ($skill in $skillFolders) {
    $name = $skill.Name
    foreach ($dir in $SkillDirs) {
        $linkPath = Join-Path $dir $name
        if (Test-Path $linkPath) {
            Write-Host "  exists: $linkPath"
        } else {
            try {
                # Absolute path target — Windows symlinks resolve relative paths
                # against the link's location, which makes relative targets fragile
                New-Item -ItemType SymbolicLink -Path $linkPath -Target $skill.FullName | Out-Null
                Write-Host "  linked: $linkPath"
                $linked++
            } catch {
                Write-Error @"
Failed to create symlink: $linkPath

This typically means Developer Mode is not enabled and you are not running as
Administrator. Either:
  1. Enable Developer Mode in Windows Settings (recommended), or
  2. Re-run this script in an elevated PowerShell, or
  3. Use the copy fallback documented in INSTALLATION.md

Original error: $($_.Exception.Message)
"@
                exit 1
            }
        }
    }
}

if ($linked -eq 0) {
    Write-Host "All Suno skills already linked."
} else {
    Write-Host "$linked link(s) created across skill directories."
    Write-Host ""
    Write-Host "Skill directories:"
    foreach ($dir in $SkillDirs) {
        Write-Host "  $dir/"
    }
    Write-Host ""
    Write-Host "Run /suno-setup to complete configuration (or configure manually -- see INSTALLATION.md)."
}
