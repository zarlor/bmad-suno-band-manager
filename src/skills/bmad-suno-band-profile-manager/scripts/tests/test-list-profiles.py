"""Tests for list-profiles.py"""

import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent))
from importlib.util import spec_from_file_location, module_from_spec

spec = spec_from_file_location(
    "list_profiles",
    Path(__file__).parent.parent / "list-profiles.py"
)
list_profiles_mod = module_from_spec(spec)
spec.loader.exec_module(list_profiles_mod)
list_profiles = list_profiles_mod.list_profiles
check_profile = list_profiles_mod.check_profile


SAMPLE_PROFILE = {
    "name": "Test Band",
    "genre": "indie rock",
    "mood": "melancholic",
    "model_preference": "v4.5-all",
    "tier": "free",
}


def test_nonexistent_directory(tmp_path):
    result = list_profiles(tmp_path / "nope")
    assert result["status"] == "pass"
    assert result["count"] == 0
    assert "No profiles directory" in result.get("message", "")


def test_empty_directory(tmp_path):
    profiles_dir = tmp_path / "profiles"
    profiles_dir.mkdir()
    result = list_profiles(profiles_dir)
    assert result["status"] == "pass"
    assert result["count"] == 0


def test_single_profile(tmp_path):
    profiles_dir = tmp_path / "profiles"
    profiles_dir.mkdir()
    with open(profiles_dir / "test-band.yaml", "w") as f:
        yaml.dump(SAMPLE_PROFILE, f)
    result = list_profiles(profiles_dir)
    assert result["count"] == 1
    assert result["profiles"][0]["name"] == "Test Band"
    assert result["profiles"][0]["genre"] == "indie rock"


def test_multiple_profiles(tmp_path):
    profiles_dir = tmp_path / "profiles"
    profiles_dir.mkdir()
    for i in range(3):
        data = {**SAMPLE_PROFILE, "name": f"Band {i}"}
        with open(profiles_dir / f"band-{i}.yaml", "w") as f:
            yaml.dump(data, f)
    result = list_profiles(profiles_dir)
    assert result["count"] == 3


def test_writer_voice_detection(tmp_path):
    profiles_dir = tmp_path / "profiles"
    profiles_dir.mkdir()
    data_with_voice = {
        **SAMPLE_PROFILE,
        "writer_voice": {"vocabulary": "formal, archaic", "rhythm": "long flowing"}
    }
    with open(profiles_dir / "voiced.yaml", "w") as f:
        yaml.dump(data_with_voice, f)
    data_without = {**SAMPLE_PROFILE}
    with open(profiles_dir / "plain.yaml", "w") as f:
        yaml.dump(data_without, f)

    result = list_profiles(profiles_dir)
    voiced = next(p for p in result["profiles"] if p["file"] == "voiced.yaml")
    plain = next(p for p in result["profiles"] if p["file"] == "plain.yaml")
    assert voiced["has_writer_voice"] is True
    assert plain["has_writer_voice"] is False


def test_invalid_yaml_skipped(tmp_path):
    profiles_dir = tmp_path / "profiles"
    profiles_dir.mkdir()
    (profiles_dir / "bad.yaml").write_text(": {{invalid")
    with open(profiles_dir / "good.yaml", "w") as f:
        yaml.dump(SAMPLE_PROFILE, f)
    result = list_profiles(profiles_dir)
    assert result["count"] == 1


def test_new_fields_in_listing(tmp_path):
    profiles_dir = tmp_path / "profiles"
    profiles_dir.mkdir()
    data = {
        **SAMPLE_PROFILE,
        "instrumental": True,
        "language": "Spanish",
        "creativity_default": "experimental",
        "generation_history": [{"date": "2026-03-19"}],
    }
    with open(profiles_dir / "test.yaml", "w") as f:
        yaml.dump(data, f)
    result = list_profiles(profiles_dir)
    p = result["profiles"][0]
    assert p["instrumental"] is True
    assert p["language"] == "Spanish"
    assert p["creativity_default"] == "experimental"
    assert p["has_generation_history"] is True


# --- check_profile tests ---

def test_check_profile_exists(tmp_path):
    profiles_dir = tmp_path / "profiles"
    profiles_dir.mkdir()
    with open(profiles_dir / "test-band.yaml", "w") as f:
        yaml.dump(SAMPLE_PROFILE, f)
    result = check_profile(profiles_dir, "test-band")
    assert result["exists"] is True
    assert result["name"] == "Test Band"
    assert "size_bytes" in result
    assert "last_modified" in result


def test_check_profile_exists_with_extension(tmp_path):
    profiles_dir = tmp_path / "profiles"
    profiles_dir.mkdir()
    with open(profiles_dir / "test-band.yaml", "w") as f:
        yaml.dump(SAMPLE_PROFILE, f)
    result = check_profile(profiles_dir, "test-band.yaml")
    assert result["exists"] is True


def test_check_profile_not_exists(tmp_path):
    profiles_dir = tmp_path / "profiles"
    profiles_dir.mkdir()
    result = check_profile(profiles_dir, "nonexistent")
    assert result["exists"] is False
    assert result["query"] == "nonexistent"
