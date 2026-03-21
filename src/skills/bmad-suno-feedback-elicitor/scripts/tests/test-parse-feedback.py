#!/usr/bin/env python3
"""Tests for parse-feedback.py"""

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = str(Path(__file__).parent.parent / "parse-feedback.py")


def run_script(input_data: dict | str | None = None, extra_args: list[str] | None = None) -> tuple[int, dict]:
    """Run parse-feedback.py with stdin input and return (exit_code, parsed_json)."""
    cmd = [sys.executable, SCRIPT, "--stdin"]
    if extra_args:
        cmd.extend(extra_args)

    input_str = json.dumps(input_data) if isinstance(input_data, dict) else (input_data or "")
    result = subprocess.run(cmd, input=input_str, capture_output=True, text=True)
    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError:
        output = {"raw_stdout": result.stdout, "raw_stderr": result.stderr}
    return result.returncode, output


def test_valid_minimal_input():
    """Minimal valid input: just feedback_text."""
    code, output = run_script({"feedback_text": "The guitar is too loud"})
    assert code == 0, f"Expected exit 0, got {code}: {output}"
    assert output["status"] == "pass"
    assert output["parsed"]["feedback_text"] == "The guitar is too loud"
    assert output["summary"]["total"] == 0


def test_valid_full_input():
    """Full valid input with all optional fields."""
    data = {
        "feedback_text": "It feels too polished",
        "original_style_prompt": "indie folk, acoustic, warm",
        "original_lyrics": "[Verse]\nSome lyrics here",
        "band_profile": "midnight-wanderers",
        "model": "v5 Pro",
        "slider_settings": {"weirdness": 45, "style_influence": 60},
        "intent": "I wanted a raw, intimate feel",
        "feedback_type": "clear",
        "dimensions": ["production", "vocals"],
    }
    code, output = run_script(data)
    assert code == 0
    assert output["status"] == "pass"
    assert output["parsed"]["context"]["model"] == "v5 Pro"
    assert output["parsed"]["context"]["band_profile"] == "midnight-wanderers"
    assert output["parsed"]["pre_categorized"]["feedback_type"] == "clear"
    assert output["parsed"]["pre_categorized"]["dimensions"] == ["production", "vocals"]


def test_missing_feedback_text():
    """Missing feedback_text should fail."""
    code, output = run_script({"model": "v5 Pro"})
    assert code == 1
    assert output["status"] == "fail"
    assert output["summary"]["critical"] >= 1


def test_empty_feedback_text():
    """Empty feedback_text should fail."""
    code, output = run_script({"feedback_text": "   "})
    assert code == 1
    assert output["status"] == "fail"
    assert output["summary"]["critical"] >= 1


def test_unrecognized_model_info():
    """Unrecognized model should produce an info finding and still pass."""
    code, output = run_script({"feedback_text": "Sounds off", "model": "v99 Ultra"})
    assert code == 0
    assert output["status"] == "pass", f"Expected pass (info-only findings), got {output['status']}"
    info_findings = [f for f in output["findings"] if f["severity"] == "info"]
    assert len(info_findings) >= 1
    assert "Unrecognized model" in info_findings[0]["issue"]
    assert "informational" in info_findings[0]["fix"]


def test_invalid_dimension():
    """Invalid dimension should produce a low-severity finding but pass."""
    code, output = run_script({"feedback_text": "Too bright", "dimensions": ["brightness"]})
    assert code == 0
    assert output["status"] == "warning"
    assert output["summary"]["low"] >= 1


def test_invalid_feedback_type():
    """Invalid feedback_type should produce a warning."""
    code, output = run_script({"feedback_text": "Hmm", "feedback_type": "confused"})
    assert code == 0
    assert output["status"] == "warning"


def test_invalid_slider_range():
    """Slider value out of range should warn."""
    code, output = run_script({
        "feedback_text": "Off",
        "slider_settings": {"weirdness": 150},
    })
    assert code == 0
    assert output["status"] == "warning"
    assert output["summary"]["medium"] >= 1


def test_invalid_json_input():
    """Non-JSON input should fail."""
    code, output = run_script("this is not json")
    assert code == 1
    assert output["status"] == "fail"


def test_non_object_json():
    """JSON array (not object) should fail."""
    cmd = [sys.executable, SCRIPT, "--stdin"]
    result = subprocess.run(cmd, input="[1, 2, 3]", capture_output=True, text=True)
    assert result.returncode == 1
    output = json.loads(result.stdout)
    assert output["status"] == "fail"


def test_dimensions_not_array():
    """dimensions as non-array should produce high severity finding."""
    code, output = run_script({"feedback_text": "Bad", "dimensions": "vocals"})
    assert code == 1
    assert output["status"] == "fail"
    assert output["summary"]["high"] >= 1


def test_empty_context_stripped():
    """Empty optional context fields should be stripped from output."""
    code, output = run_script({"feedback_text": "Good stuff"})
    assert code == 0
    # Context should only have non-empty fields
    assert "model" not in output["parsed"]["context"]
    assert "band_profile" not in output["parsed"]["context"]


def test_technical_feedback_type():
    """'technical' should be a valid feedback type."""
    code, output = run_script({"feedback_text": "There are artifacts", "feedback_type": "technical"})
    assert code == 0
    assert output["status"] == "pass"
    assert output["summary"]["total"] == 0


def test_length_dimension_valid():
    """'length' should be a valid dimension."""
    code, output = run_script({"feedback_text": "Song is too short", "dimensions": ["length"]})
    assert code == 0
    assert output["status"] == "pass"
    assert output["summary"]["low"] == 0


def test_quality_dimension_valid():
    """'quality' should be a valid dimension."""
    code, output = run_script({"feedback_text": "Audio has clipping", "dimensions": ["quality"]})
    assert code == 0
    assert output["status"] == "pass"
    assert output["summary"]["low"] == 0


def test_unrecognized_model_passes_through():
    """Unrecognized model should still appear in parsed output context."""
    code, output = run_script({"feedback_text": "Test", "model": "v99 Ultra"})
    assert code == 0
    assert output["parsed"]["context"]["model"] == "v99 Ultra"


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
