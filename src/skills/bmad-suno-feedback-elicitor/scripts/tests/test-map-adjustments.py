#!/usr/bin/env python3
"""Tests for map-adjustments.py"""

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = str(Path(__file__).parent.parent / "map-adjustments.py")


def run_script(input_data: dict | str | None = None) -> tuple[int, dict]:
    """Run map-adjustments.py with stdin input and return (exit_code, parsed_json)."""
    cmd = [sys.executable, SCRIPT, "--stdin"]
    input_str = json.dumps(input_data) if isinstance(input_data, dict) else (input_data or "")
    result = subprocess.run(cmd, input=input_str, capture_output=True, text=True)
    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError:
        output = {"raw_stdout": result.stdout, "raw_stderr": result.stderr}
    return result.returncode, output


def test_single_dimension():
    """Single dimension should produce relevant adjustments."""
    data = {"dimensions": [{"dimension": "vocals", "direction": "too_polished"}]}
    code, output = run_script(data)
    assert code == 0
    assert output["status"] == "pass"
    adj = output["adjustments"]
    assert "raw vocal" in adj["style_prompt"]["add_descriptors"]
    assert any("polished" in p for p in adj["style_prompt"]["remove_patterns"])


def test_multiple_dimensions():
    """Multiple dimensions should combine adjustments."""
    data = {
        "dimensions": [
            {"dimension": "vocals", "direction": "too_polished"},
            {"dimension": "energy", "direction": "too_low"},
        ]
    }
    code, output = run_script(data)
    assert code == 0
    adj = output["adjustments"]
    # Should have vocal adjustments
    assert "raw vocal" in adj["style_prompt"]["add_descriptors"]
    # Should have energy adjustments
    assert "high energy" in adj["style_prompt"]["add_descriptors"]


def test_slider_adjustments_paid_tier():
    """Paid tier should get direct slider recommendations."""
    data = {
        "dimensions": [{"dimension": "vibe", "direction": "too_generic"}],
        "tier": "pro",
    }
    code, output = run_script(data)
    assert code == 0
    adj = output["adjustments"]
    assert "sliders" in adj
    assert "weirdness" in adj["sliders"]
    assert "note" not in adj["sliders"]  # No "not available" note for paid tier


def test_slider_adjustments_free_tier():
    """Free tier should get slider note about unavailability."""
    data = {
        "dimensions": [{"dimension": "vibe", "direction": "too_generic"}],
        "tier": "free",
    }
    code, output = run_script(data)
    assert code == 0
    adj = output["adjustments"]
    assert "sliders" in adj
    assert "note" in adj["sliders"]  # Should have unavailability note
    assert "recommended_if_upgraded" in adj["sliders"]


def test_lyric_changes():
    """Structure dimensions should produce lyric change recommendations."""
    data = {"dimensions": [{"dimension": "structure", "direction": "needs_bridge"}]}
    code, output = run_script(data)
    assert code == 0
    adj = output["adjustments"]
    assert "lyrics" in adj
    assert len(adj["lyrics"]["changes"]) > 0
    assert "Bridge" in adj["lyrics"]["changes"][0]


def test_unknown_dimension():
    """Unknown dimension should produce a note, not fail."""
    data = {"dimensions": [{"dimension": "color", "direction": "too_blue"}]}
    code, output = run_script(data)
    assert code == 0
    adj = output["adjustments"]
    assert "notes" in adj
    assert any("Unknown dimension" in n for n in adj["notes"])


def test_unknown_direction():
    """Unknown direction for valid dimension should produce a note."""
    data = {"dimensions": [{"dimension": "vocals", "direction": "too_purple"}]}
    code, output = run_script(data)
    assert code == 0
    adj = output["adjustments"]
    assert "notes" in adj
    assert any("Unknown direction" in n for n in adj["notes"])


def test_deduplication():
    """Duplicate descriptors should be deduped."""
    data = {
        "dimensions": [
            {"dimension": "energy", "direction": "too_low"},
            {"dimension": "energy", "direction": "too_low"},
        ]
    }
    code, output = run_script(data)
    assert code == 0
    add_descs = output["adjustments"]["style_prompt"]["add_descriptors"]
    assert len(add_descs) == len(set(add_descs)), "Descriptors should be deduped"


def test_missing_dimensions_field():
    """Missing dimensions should fail."""
    code, output = run_script({"tier": "pro"})
    assert code == 1
    assert output["status"] == "fail"


def test_invalid_json():
    """Invalid JSON should fail."""
    code, output = run_script("not json")
    assert code == 1
    assert output["status"] == "fail"


def test_empty_dimensions():
    """Empty dimensions array should pass with empty adjustments."""
    data = {"dimensions": []}
    code, output = run_script(data)
    assert code == 0
    adj = output["adjustments"]
    assert adj["style_prompt"]["add_descriptors"] == []
    assert adj["style_prompt"]["remove_patterns"] == []


def test_exclusion_generation():
    """Dimensions with exclusion recommendations should populate exclusions."""
    data = {"dimensions": [{"dimension": "instrumentation", "direction": "too_much"}]}
    code, output = run_script(data)
    assert code == 0
    adj = output["adjustments"]
    assert len(adj["exclusions"]["add"]) > 0


def test_dimension_with_note():
    """Dimensions that need further clarification should include notes."""
    data = {"dimensions": [{"dimension": "music", "direction": "general_issue"}]}
    code, output = run_script(data)
    assert code == 0
    adj = output["adjustments"]
    assert "notes" in adj
    assert any("further narrowing" in n.lower() for n in adj["notes"])


def test_quality_robotic_vocals():
    """Quality dimension robotic_vocals should produce style and exclusion adjustments."""
    data = {"dimensions": [{"dimension": "quality", "direction": "robotic_vocals"}]}
    code, output = run_script(data)
    assert code == 0
    adj = output["adjustments"]
    assert "natural vocal" in adj["style_prompt"]["add_descriptors"]
    assert "no auto-tune" in adj["exclusions"]["add"]


def test_quality_clipping():
    """Quality dimension clipping should add clean mix descriptors and remove heavy patterns."""
    data = {"dimensions": [{"dimension": "quality", "direction": "clipping"}]}
    code, output = run_script(data)
    assert code == 0
    adj = output["adjustments"]
    assert "clean mix" in adj["style_prompt"]["add_descriptors"]
    assert "heavy" in adj["style_prompt"]["remove_patterns"]


def test_quality_muffled():
    """Quality dimension muffled should add crisp descriptors."""
    data = {"dimensions": [{"dimension": "quality", "direction": "muffled"}]}
    code, output = run_script(data)
    assert code == 0
    adj = output["adjustments"]
    assert "crisp" in adj["style_prompt"]["add_descriptors"]
    assert "lo-fi" in adj["style_prompt"]["remove_patterns"]


def test_quality_artifacts_note():
    """Quality dimension artifacts should produce a note about regeneration."""
    data = {"dimensions": [{"dimension": "quality", "direction": "artifacts"}]}
    code, output = run_script(data)
    assert code == 0
    adj = output["adjustments"]
    assert "notes" in adj
    assert any("regenerate" in n.lower() for n in adj["notes"])


def test_length_too_short():
    """Length dimension too_short should produce lyric change recommendations."""
    data = {"dimensions": [{"dimension": "length", "direction": "too_short"}]}
    code, output = run_script(data)
    assert code == 0
    adj = output["adjustments"]
    assert "lyrics" in adj
    assert any("extend" in c.lower() or "add sections" in c.lower() for c in adj["lyrics"]["changes"])


def test_length_outro_cuts_off():
    """Length dimension outro_cuts_off should recommend Outro and Fade Out."""
    data = {"dimensions": [{"dimension": "length", "direction": "outro_cuts_off"}]}
    code, output = run_script(data)
    assert code == 0
    adj = output["adjustments"]
    assert "lyrics" in adj
    assert any("Outro" in c for c in adj["lyrics"]["changes"])


def test_length_pacing_drags():
    """Length dimension pacing_drags should recommend energy metatags."""
    data = {"dimensions": [{"dimension": "length", "direction": "pacing_drags"}]}
    code, output = run_script(data)
    assert code == 0
    adj = output["adjustments"]
    assert "lyrics" in adj
    assert any("Energy" in c or "Build-Up" in c for c in adj["lyrics"]["changes"])


def test_consistency_check_no_conflicts():
    """Clean adjustments should produce no consistency warnings."""
    data = {"dimensions": [{"dimension": "vocals", "direction": "too_polished"}]}
    code, output = run_script(data)
    assert code == 0
    adj = output["adjustments"]
    assert "consistency_warnings" not in adj


def test_consistency_check_add_remove_conflict():
    """Conflicting add/remove should produce a consistency warning."""
    # instrumentation too_little adds "lush arrangement" etc. but also combine with
    # production too_polished which adds "lo-fi" and removes "crisp", "polished"
    # We need a case where add and remove overlap. Let's use energy too_high (adds "gentle", "soft")
    # combined with energy too_low (adds "high energy" and removes "gentle", "soft")
    data = {
        "dimensions": [
            {"dimension": "energy", "direction": "too_high"},
            {"dimension": "energy", "direction": "too_low"},
        ]
    }
    code, output = run_script(data)
    assert code == 0
    adj = output["adjustments"]
    assert "consistency_warnings" in adj
    conflict_types = [w["type"] for w in adj["consistency_warnings"]]
    assert "add_remove_conflict" in conflict_types


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
            print(f"  PASS: {test.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL: {test.__name__}: {e}")
        except Exception as e:
            failed += 1
            print(f"  ERROR: {test.__name__}: {e}")

    print(f"\n{passed} passed, {failed} failed out of {len(tests)} tests")
    sys.exit(1 if failed else 0)
