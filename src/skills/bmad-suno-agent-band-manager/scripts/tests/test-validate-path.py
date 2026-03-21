#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pytest"]
# ///
"""Tests for validate-path.py"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from importlib.util import spec_from_file_location, module_from_spec

spec = spec_from_file_location(
    "validate_path",
    Path(__file__).parent.parent / "validate-path.py",
)
mod = module_from_spec(spec)
spec.loader.exec_module(mod)


def test_parse_boundaries(tmp_path):
    """Parse access-boundaries.md correctly."""
    boundaries_file = tmp_path / "access-boundaries.md"
    boundaries_file.write_text(
        "# Access Boundaries\n\n"
        "## Read Access\n"
        "- docs/band-profiles/\n"
        "- {project-root}/_bmad/_memory/band-manager-sidecar/\n\n"
        "## Write Access\n"
        "- {project-root}/_bmad/_memory/band-manager-sidecar/\n\n"
        "## Deny Zones\n"
        "- All other directories\n"
    )

    boundaries = mod.parse_boundaries(boundaries_file)
    assert "docs/band-profiles/" in boundaries["read"]
    assert "_bmad/_memory/band-manager-sidecar/" in boundaries["read"]
    assert "_bmad/_memory/band-manager-sidecar/" in boundaries["write"]


def test_validate_read_allowed(tmp_path):
    boundaries = {"read": ["docs/band-profiles/"], "write": []}
    result = mod.validate_path("docs/band-profiles/midnight-orchid.yaml", "read", boundaries)
    assert result["allowed"] is True


def test_validate_read_denied(tmp_path):
    boundaries = {"read": ["docs/band-profiles/"], "write": []}
    result = mod.validate_path("src/secret.py", "read", boundaries)
    assert result["allowed"] is False


def test_validate_write_allowed(tmp_path):
    boundaries = {"read": [], "write": ["_bmad/_memory/band-manager-sidecar/"]}
    result = mod.validate_path("_bmad/_memory/band-manager-sidecar/index.md", "write", boundaries)
    assert result["allowed"] is True


def test_validate_write_denied(tmp_path):
    boundaries = {"read": [], "write": ["_bmad/_memory/band-manager-sidecar/"]}
    result = mod.validate_path("docs/band-profiles/test.yaml", "write", boundaries)
    assert result["allowed"] is False
