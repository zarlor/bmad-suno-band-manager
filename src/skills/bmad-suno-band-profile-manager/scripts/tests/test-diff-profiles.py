"""Tests for diff-profiles.py"""

import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent))
from importlib.util import spec_from_file_location, module_from_spec

spec = spec_from_file_location(
    "diff_profiles",
    Path(__file__).parent.parent / "diff-profiles.py"
)
diff_profiles_mod = module_from_spec(spec)
spec.loader.exec_module(diff_profiles_mod)
diff_profiles = diff_profiles_mod.diff_profiles


PROFILE_A = {
    "name": "Test Band",
    "genre": "indie rock",
    "mood": "melancholic",
    "model_preference": "v4.5-all",
    "tier": "free",
    "style_baseline": "Indie rock with warm guitars",
    "vocal": {
        "gender": "male",
        "tone": "warm",
        "delivery": "intimate",
        "energy": "restrained",
    },
}


def write_yaml(tmp_path, filename, data):
    path = tmp_path / filename
    with open(path, "w") as f:
        yaml.dump(data, f)
    return path


def test_identical_profiles(tmp_path):
    a = write_yaml(tmp_path, "a.yaml", PROFILE_A)
    b = write_yaml(tmp_path, "b.yaml", PROFILE_A)
    result = diff_profiles(a, b)
    assert result["status"] == "pass"
    assert result["has_changes"] is False
    assert result["summary"]["total_changes"] == 0


def test_changed_fields(tmp_path):
    modified = {**PROFILE_A, "genre": "electronic", "mood": "energetic"}
    a = write_yaml(tmp_path, "a.yaml", PROFILE_A)
    b = write_yaml(tmp_path, "b.yaml", modified)
    result = diff_profiles(a, b)
    assert result["has_changes"] is True
    assert result["summary"]["fields_changed"] == 2
    changed_fields = [c["field"] for c in result["changed"]]
    assert "genre" in changed_fields
    assert "mood" in changed_fields


def test_added_fields(tmp_path):
    modified = {**PROFILE_A, "language": "Spanish", "instrumental": True}
    a = write_yaml(tmp_path, "a.yaml", PROFILE_A)
    b = write_yaml(tmp_path, "b.yaml", modified)
    result = diff_profiles(a, b)
    assert result["has_changes"] is True
    assert result["summary"]["fields_added"] >= 2
    added_fields = [c["field"] for c in result["added"]]
    assert "language" in added_fields
    assert "instrumental" in added_fields


def test_removed_fields(tmp_path):
    modified = {k: v for k, v in PROFILE_A.items() if k != "mood"}
    a = write_yaml(tmp_path, "a.yaml", PROFILE_A)
    b = write_yaml(tmp_path, "b.yaml", modified)
    result = diff_profiles(a, b)
    assert result["has_changes"] is True
    assert result["summary"]["fields_removed"] >= 1
    removed_fields = [c["field"] for c in result["removed"]]
    assert "mood" in removed_fields


def test_nested_changes(tmp_path):
    modified = {**PROFILE_A, "vocal": {**PROFILE_A["vocal"], "tone": "bright, clear"}}
    a = write_yaml(tmp_path, "a.yaml", PROFILE_A)
    b = write_yaml(tmp_path, "b.yaml", modified)
    result = diff_profiles(a, b)
    assert result["has_changes"] is True
    changed_fields = [c["field"] for c in result["changed"]]
    assert "vocal.tone" in changed_fields


def test_missing_original(tmp_path):
    b = write_yaml(tmp_path, "b.yaml", PROFILE_A)
    result = diff_profiles(tmp_path / "nope.yaml", b)
    assert result["status"] == "fail"
    assert "errors" in result


def test_missing_modified(tmp_path):
    a = write_yaml(tmp_path, "a.yaml", PROFILE_A)
    result = diff_profiles(a, tmp_path / "nope.yaml")
    assert result["status"] == "fail"


def test_invalid_yaml(tmp_path):
    a = write_yaml(tmp_path, "a.yaml", PROFILE_A)
    bad = tmp_path / "bad.yaml"
    bad.write_text(": {{invalid yaml")
    result = diff_profiles(a, bad)
    assert result["status"] == "fail"


def test_mixed_changes(tmp_path):
    modified = {**PROFILE_A, "genre": "electronic", "language": "French"}
    del modified["mood"]
    a = write_yaml(tmp_path, "a.yaml", PROFILE_A)
    b = write_yaml(tmp_path, "b.yaml", modified)
    result = diff_profiles(a, b)
    assert result["has_changes"] is True
    assert result["summary"]["fields_changed"] >= 1
    assert result["summary"]["fields_added"] >= 1
    assert result["summary"]["fields_removed"] >= 1
