#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pytest"]
# ///
"""Tests for check-memory-health.py"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from importlib.util import spec_from_file_location, module_from_spec

spec = spec_from_file_location(
    "check_memory_health",
    Path(__file__).parent.parent / "check-memory-health.py",
)
mod = module_from_spec(spec)
spec.loader.exec_module(mod)


def test_healthy_files(tmp_path):
    """All files under threshold."""
    (tmp_path / "index.md").write_text("x" * 100)
    (tmp_path / "patterns.md").write_text("x" * 100)
    (tmp_path / "chronology.md").write_text("x" * 100)

    result = mod.check_health(tmp_path)
    assert result["maintenance_recommended"] is False
    assert result["needs_pruning"] == []


def test_over_threshold(tmp_path):
    """File over threshold flagged."""
    (tmp_path / "index.md").write_text("x" * 5000)
    (tmp_path / "patterns.md").write_text("x" * 100)
    (tmp_path / "chronology.md").write_text("x" * 100)

    result = mod.check_health(tmp_path)
    assert result["maintenance_recommended"] is True
    assert "index.md" in result["needs_pruning"]


def test_missing_files(tmp_path):
    """Missing files reported correctly."""
    result = mod.check_health(tmp_path)
    assert result["files"]["index.md"]["exists"] is False
