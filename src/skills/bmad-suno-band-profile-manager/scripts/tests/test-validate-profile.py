"""Tests for validate-profile.py"""

import json
import sys
import tempfile
from pathlib import Path

import pytest
import yaml

# Add parent directory to path for import
sys.path.insert(0, str(Path(__file__).parent.parent))
from importlib.util import spec_from_file_location, module_from_spec

# Import the module
spec = spec_from_file_location(
    "validate_profile",
    Path(__file__).parent.parent / "validate-profile.py"
)
validate_profile_mod = module_from_spec(spec)
spec.loader.exec_module(validate_profile_mod)
validate_profile = validate_profile_mod.validate_profile
derive_filename = validate_profile_mod.derive_filename


def write_profile(tmp_path, data):
    """Helper to write a YAML profile and return its path."""
    profile_path = tmp_path / "test-band.yaml"
    with open(profile_path, "w") as f:
        yaml.dump(data, f)
    return profile_path


VALID_PROFILE = {
    "name": "Test Band",
    "genre": "indie rock",
    "mood": "melancholic",
    "model_preference": "v4.5-all",
    "tier": "free",
    "style_baseline": "Indie rock with warm guitars and atmospheric pads",
    "vocal": {
        "gender": "male",
        "tone": "warm, breathy",
        "delivery": "intimate",
        "energy": "restrained",
    },
}

VALID_INSTRUMENTAL_PROFILE = {
    "name": "Ambient Waves",
    "genre": "ambient electronic",
    "mood": "contemplative, spacious",
    "model_preference": "v4.5-all",
    "tier": "free",
    "style_baseline": "Ambient electronic with lush pads and field recordings",
    "instrumental": True,
}


def test_valid_profile(tmp_path):
    path = write_profile(tmp_path, VALID_PROFILE)
    result = validate_profile(path)
    assert result["status"] == "pass"
    assert result["summary"]["total"] == 0


def test_missing_file(tmp_path):
    path = tmp_path / "nonexistent.yaml"
    result = validate_profile(path)
    assert result["status"] == "fail"
    assert result["summary"]["critical"] == 1


def test_invalid_yaml(tmp_path):
    path = tmp_path / "bad.yaml"
    path.write_text(": invalid: yaml: {{{{")
    result = validate_profile(path)
    assert result["status"] == "fail"
    assert result["summary"]["critical"] >= 1


def test_missing_required_fields(tmp_path):
    path = write_profile(tmp_path, {"name": "Test"})
    result = validate_profile(path)
    assert result["status"] == "fail"
    assert result["summary"]["critical"] >= 1


def test_invalid_model(tmp_path):
    data = {**VALID_PROFILE, "model_preference": "v99 Ultra"}
    path = write_profile(tmp_path, data)
    result = validate_profile(path)
    assert any(f.get("location", {}).get("field") == "model_preference"
               for f in result["findings"])


def test_invalid_tier(tmp_path):
    data = {**VALID_PROFILE, "tier": "ultimate"}
    path = write_profile(tmp_path, data)
    result = validate_profile(path)
    assert any("tier" in str(f) for f in result["findings"])


def test_style_baseline_too_long(tmp_path):
    data = {**VALID_PROFILE, "style_baseline": "x" * 1001}
    path = write_profile(tmp_path, data)
    result = validate_profile(path)
    assert any("style_baseline" in str(f) for f in result["findings"])


def test_style_baseline_v4_pro_200_limit(tmp_path):
    data = {**VALID_PROFILE, "model_preference": "v4 Pro", "tier": "pro",
            "style_baseline": "x" * 201}
    path = write_profile(tmp_path, data)
    result = validate_profile(path)
    assert any("style_baseline" in str(f) and "200" in str(f)
               for f in result["findings"])


def test_free_tier_wrong_model(tmp_path):
    data = {**VALID_PROFILE, "tier": "free", "model_preference": "v5 Pro"}
    path = write_profile(tmp_path, data)
    result = validate_profile(path)
    assert any("free" in f.get("issue", "").lower() or "free" in f.get("fix", "").lower()
               for f in result["findings"])


def test_free_tier_slider_warning(tmp_path):
    data = {**VALID_PROFILE, "sliders": {"weirdness": 80, "style_influence": 30}}
    path = write_profile(tmp_path, data)
    result = validate_profile(path)
    assert any("slider" in f.get("issue", "").lower() for f in result["findings"])


def test_slider_out_of_range(tmp_path):
    data = {**VALID_PROFILE, "tier": "pro", "model_preference": "v5 Pro",
            "sliders": {"weirdness": 150}}
    path = write_profile(tmp_path, data)
    result = validate_profile(path)
    assert any("out of range" in f.get("issue", "").lower() for f in result["findings"])


def test_audio_influence_slider_validation(tmp_path):
    data = {**VALID_PROFILE, "tier": "pro", "model_preference": "v5 Pro",
            "sliders": {"audio_influence": 200}}
    path = write_profile(tmp_path, data)
    result = validate_profile(path)
    assert any("audio_influence" in str(f) and "out of range" in f.get("issue", "").lower()
               for f in result["findings"])


def test_invalid_vocal_gender(tmp_path):
    data = {**VALID_PROFILE}
    data["vocal"] = {**VALID_PROFILE["vocal"], "gender": "robot"}
    path = write_profile(tmp_path, data)
    result = validate_profile(path)
    assert any("gender" in str(f) for f in result["findings"])


def test_missing_vocal_fields(tmp_path):
    data = {**VALID_PROFILE, "vocal": {"gender": "male"}}
    path = write_profile(tmp_path, data)
    result = validate_profile(path)
    assert result["summary"]["high"] >= 1


def test_too_many_exclusions(tmp_path):
    data = {**VALID_PROFILE, "exclusion_defaults": [f"no thing {i}" for i in range(7)]}
    path = write_profile(tmp_path, data)
    result = validate_profile(path)
    assert any("exclusion" in f.get("issue", "").lower() for f in result["findings"])


def test_pro_tier_valid_with_sliders(tmp_path):
    data = {
        **VALID_PROFILE,
        "tier": "pro",
        "model_preference": "v5 Pro",
        "sliders": {"weirdness": 70, "style_influence": 40},
    }
    path = write_profile(tmp_path, data)
    result = validate_profile(path)
    assert result["status"] == "pass"


# --- Instrumental profile tests ---

def test_instrumental_profile_valid_without_vocal(tmp_path):
    path = write_profile(tmp_path, VALID_INSTRUMENTAL_PROFILE)
    result = validate_profile(path)
    assert result["status"] == "pass"
    assert result["summary"]["total"] == 0


def test_instrumental_profile_with_optional_vocal(tmp_path):
    data = {**VALID_INSTRUMENTAL_PROFILE, "vocal": {"gender": "any"}}
    path = write_profile(tmp_path, data)
    result = validate_profile(path)
    assert result["status"] == "pass"


def test_non_instrumental_requires_vocal(tmp_path):
    data = {**VALID_PROFILE}
    del data["vocal"]
    path = write_profile(tmp_path, data)
    result = validate_profile(path)
    assert result["status"] == "fail"
    assert result["summary"]["high"] >= 1


# --- New field tests ---

def test_valid_creativity_default(tmp_path):
    for mode in ["conservative", "balanced", "experimental"]:
        data = {**VALID_PROFILE, "creativity_default": mode}
        path = write_profile(tmp_path, data)
        result = validate_profile(path)
        assert not any(f.get("location", {}).get("field") == "creativity_default"
                       for f in result["findings"]), f"Failed for {mode}"


def test_invalid_creativity_default(tmp_path):
    data = {**VALID_PROFILE, "creativity_default": "wild"}
    path = write_profile(tmp_path, data)
    result = validate_profile(path)
    assert any("creativity_default" in str(f) for f in result["findings"])


def test_valid_language(tmp_path):
    data = {**VALID_PROFILE, "language": "Spanish"}
    path = write_profile(tmp_path, data)
    result = validate_profile(path)
    assert not any(f.get("location", {}).get("field") == "language"
                   for f in result["findings"])


def test_empty_language(tmp_path):
    data = {**VALID_PROFILE, "language": ""}
    path = write_profile(tmp_path, data)
    result = validate_profile(path)
    assert any("language" in str(f) for f in result["findings"])


def test_generation_history_valid(tmp_path):
    data = {**VALID_PROFILE, "generation_history": [
        {"date": "2026-03-19", "style_prompt": "test", "model": "v4.5-all"}
    ]}
    path = write_profile(tmp_path, data)
    result = validate_profile(path)
    assert not any(f.get("location", {}).get("field") == "generation_history"
                   for f in result["findings"])


def test_generation_history_too_many(tmp_path):
    data = {**VALID_PROFILE, "generation_history": [
        {"date": f"2026-03-{i:02d}"} for i in range(1, 15)
    ]}
    path = write_profile(tmp_path, data)
    result = validate_profile(path)
    assert any("generation_history" in str(f) for f in result["findings"])


def test_generation_history_not_list(tmp_path):
    data = {**VALID_PROFILE, "generation_history": "not a list"}
    path = write_profile(tmp_path, data)
    result = validate_profile(path)
    assert any("generation_history" in str(f) for f in result["findings"])


def test_studio_preferences_non_premier_warning(tmp_path):
    data = {**VALID_PROFILE, "tier": "pro", "model_preference": "v5 Pro",
            "studio_preferences": {"bpm": 120, "key": "C minor"}}
    path = write_profile(tmp_path, data)
    result = validate_profile(path)
    assert any("studio" in f.get("issue", "").lower() for f in result["findings"])


def test_studio_preferences_premier_valid(tmp_path):
    data = {**VALID_PROFILE, "tier": "premier", "model_preference": "v5 Pro",
            "studio_preferences": {"bpm": 120, "key": "C minor", "time_signature": "4/4"}}
    path = write_profile(tmp_path, data)
    result = validate_profile(path)
    assert not any("studio" in f.get("issue", "").lower() for f in result["findings"])


def test_studio_preferences_invalid_bpm(tmp_path):
    data = {**VALID_PROFILE, "tier": "premier", "model_preference": "v5 Pro",
            "studio_preferences": {"bpm": "fast"}}
    path = write_profile(tmp_path, data)
    result = validate_profile(path)
    assert any("bpm" in str(f).lower() for f in result["findings"])


# --- derive_filename tests ---

def test_derive_filename_basic():
    assert derive_filename("Test Band") == "test-band.yaml"


def test_derive_filename_special_chars():
    assert derive_filename("The Band's Name!") == "the-bands-name.yaml"


def test_derive_filename_multiple_spaces():
    assert derive_filename("  My   Cool  Band  ") == "my-cool-band.yaml"


def test_derive_filename_already_kebab():
    assert derive_filename("already-kebab") == "already-kebab.yaml"
