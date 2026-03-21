#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pytest"]
# ///
"""Tests for pre-activate.py"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from importlib.util import spec_from_file_location, module_from_spec

# Load module
spec = spec_from_file_location(
    "pre_activate",
    Path(__file__).parent.parent / "pre-activate.py",
)
mod = module_from_spec(spec)
spec.loader.exec_module(mod)


def test_check_first_run_true(tmp_path):
    """First run when sidecar doesn't exist."""
    assert mod.check_first_run(tmp_path) is True


def test_check_first_run_false(tmp_path):
    """Not first run when sidecar exists."""
    sidecar = tmp_path / "_bmad" / "_memory" / "band-manager-sidecar"
    sidecar.mkdir(parents=True)
    assert mod.check_first_run(tmp_path) is False


def test_scaffold_sidecar(tmp_path):
    """Scaffold creates all expected files."""
    result = mod.scaffold_sidecar(tmp_path)
    assert result["scaffolded"] is True
    assert "access-boundaries.md" in result["files_created"]
    assert "patterns.md" in result["files_created"]
    assert "chronology.md" in result["files_created"]

    sidecar = tmp_path / "_bmad" / "_memory" / "band-manager-sidecar"
    assert (sidecar / "access-boundaries.md").exists()
    assert (sidecar / "patterns.md").exists()
    assert (sidecar / "chronology.md").exists()


def test_scaffold_idempotent(tmp_path):
    """Scaffold doesn't overwrite existing files."""
    mod.scaffold_sidecar(tmp_path)
    sidecar = tmp_path / "_bmad" / "_memory" / "band-manager-sidecar"

    # Write custom content
    (sidecar / "patterns.md").write_text("custom content")

    result = mod.scaffold_sidecar(tmp_path)
    assert "patterns.md" not in result["files_created"]
    assert (sidecar / "patterns.md").read_text() == "custom content"


def test_render_menu(tmp_path):
    """Menu renders correctly from manifest."""
    manifest = {
        "capabilities": [
            {"menu-code": "CS", "description": "Create a song"},
            {"menu-code": "RS", "description": "Refine a song"},
        ]
    }
    manifest_path = tmp_path / "bmad-manifest.json"
    manifest_path.write_text(json.dumps(manifest))

    menu = mod.render_menu(manifest_path)
    assert "1. [CS] Create a song" in menu
    assert "2. [RS] Refine a song" in menu
    assert "prompt" not in menu.lower() or "prompt" in "Create a song".lower()


def test_build_routing_table(tmp_path):
    """Routing table maps codes and numbers correctly."""
    manifest = {
        "capabilities": [
            {"name": "create-song", "menu-code": "CS", "prompt": "create-song.md"},
            {"name": "manage-bands", "menu-code": "MB", "skill-name": "bmad-suno-band-profile-manager"},
        ]
    }
    manifest_path = tmp_path / "bmad-manifest.json"
    manifest_path.write_text(json.dumps(manifest))

    table = mod.build_routing_table(manifest_path)
    assert table["CS"]["type"] == "prompt"
    assert table["CS"]["target"] == "create-song.md"
    assert table["1"]["type"] == "prompt"
    assert table["MB"]["type"] == "skill"
    assert table["MB"]["target"] == "bmad-suno-band-profile-manager"
