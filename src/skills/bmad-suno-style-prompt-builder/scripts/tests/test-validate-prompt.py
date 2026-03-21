# /// script
# requires-python = ">=3.9"
# dependencies = ["pytest"]
# ///
"""Tests for validate-prompt.py"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

# Load the script as a module
SCRIPT_PATH = Path(__file__).parent.parent / "validate-prompt.py"
spec = importlib.util.spec_from_file_location("validate_prompt", SCRIPT_PATH)
validate_prompt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_prompt)


class TestValidateStylePrompt:
    """Tests for style prompt validation."""

    def test_valid_prompt_passes(self):
        """A well-formed prompt under the limit should pass."""
        prompt = "indie folk-rock, melancholic warmth, acoustic guitar over ambient pads, breathy male vocal, intimate lo-fi mix"
        findings = validate_prompt.validate_style_prompt(prompt)
        critical = [f for f in findings if f["severity"] == "critical"]
        assert len(critical) == 0

    def test_over_1000_chars_is_critical(self):
        """Prompts over 1,000 chars should produce a critical finding."""
        prompt = "rock, " * 200  # ~1200 chars
        findings = validate_prompt.validate_style_prompt(prompt)
        critical = [f for f in findings if f["severity"] == "critical"]
        assert len(critical) == 1
        assert "1,000" in critical[0]["issue"]

    def test_v4_pro_200_char_limit(self):
        """v4 Pro should have a 200-char limit, not 1,000."""
        prompt = "rock, warm vocals, gentle acoustic guitar, melancholic mood, wide stereo field, intimate mix, layered harmonies, subtle percussion" * 2
        assert len(prompt) > 200
        assert len(prompt) < 1000
        findings = validate_prompt.validate_style_prompt(prompt, model="v4 Pro")
        critical = [f for f in findings if f["severity"] == "critical"]
        assert len(critical) == 1
        assert "200" in critical[0]["issue"]
        assert "v4 Pro" in critical[0]["issue"]

    def test_v5_pro_uses_1000_limit(self):
        """v5 Pro should use 1,000-char limit."""
        prompt = "rock " + "x" * 300
        findings = validate_prompt.validate_style_prompt(prompt, model="v5 Pro")
        critical = [f for f in findings if f["severity"] == "critical"]
        assert len(critical) == 0

    def test_critical_zone_warning(self):
        """Prompts with substantial content beyond 200 chars should warn about critical zone."""
        prompt = "rock, warm vocals, " + "x" * 350
        findings = validate_prompt.validate_style_prompt(prompt)
        zone_warnings = [f for f in findings if "critical zone" in f.get("issue", "").lower()]
        assert len(zone_warnings) == 1

    def test_near_limit_is_low(self):
        """Prompts at 90-100% of limit should produce a low finding."""
        prompt = "x" * 950
        # Add a genre keyword to avoid the front-loading warning
        prompt = "rock " + "x" * 945
        findings = validate_prompt.validate_style_prompt(prompt)
        low = [f for f in findings if f["severity"] == "low" and "near" in f.get("issue", "").lower()]
        assert len(low) == 1

    def test_empty_prompt_is_critical(self):
        """Empty prompts should be critical."""
        findings = validate_prompt.validate_style_prompt("")
        critical = [f for f in findings if f["severity"] == "critical"]
        assert len(critical) == 1

    def test_whitespace_only_is_critical(self):
        """Whitespace-only prompts should be critical."""
        findings = validate_prompt.validate_style_prompt("   \n  ")
        critical = [f for f in findings if f["severity"] == "critical"]
        assert len(critical) == 1

    def test_no_genre_frontloading_warning(self):
        """Prompts without genre in first 200 chars should warn."""
        prompt = "warm and beautiful with layered textures and organic feel throughout the production"
        findings = validate_prompt.validate_style_prompt(prompt)
        medium = [f for f in findings if f["severity"] == "medium" and "genre" in f["issue"].lower()]
        assert len(medium) == 1

    def test_genre_present_no_warning(self):
        """Prompts with genre early should not warn about front-loading."""
        prompt = "indie rock, melancholic, warm production"
        findings = validate_prompt.validate_style_prompt(prompt)
        genre_warnings = [f for f in findings if "genre" in f.get("issue", "").lower()]
        assert len(genre_warnings) == 0

    def test_lyric_metatags_detected(self):
        """Section tags in style prompts should be flagged."""
        prompt = "indie rock [Verse] warm vocals [Chorus] big harmonies"
        findings = validate_prompt.validate_style_prompt(prompt)
        high = [f for f in findings if f["severity"] == "high"]
        assert len(high) >= 1
        assert "metatag" in high[0]["issue"].lower() or "lyric" in high[0]["issue"].lower()

    def test_asterisks_detected(self):
        """Asterisks in style prompts should be flagged."""
        prompt = "indie rock, *bold vocals*, warm production"
        findings = validate_prompt.validate_style_prompt(prompt)
        asterisk = [f for f in findings if "asterisk" in f["issue"].lower()]
        assert len(asterisk) == 1


class TestValidateExclusionPrompt:
    """Tests for exclusion prompt validation."""

    def test_empty_exclusion_is_info(self):
        """Empty exclusion prompts should produce an info finding (optional)."""
        findings = validate_prompt.validate_exclusion_prompt("")
        assert len(findings) == 1
        assert findings[0]["severity"] == "info"

    def test_valid_exclusion_passes(self):
        """A reasonable exclusion prompt should pass cleanly."""
        findings = validate_prompt.validate_exclusion_prompt("no autotune, no screaming")
        high_or_critical = [f for f in findings if f["severity"] in ("critical", "high")]
        assert len(high_or_critical) == 0

    def test_very_long_exclusion_is_high(self):
        """Exclusion prompts over 300 chars should produce a high finding."""
        prompt = "no " + ", no ".join([f"thing{i}" for i in range(60)])
        findings = validate_prompt.validate_exclusion_prompt(prompt)
        high = [f for f in findings if f["severity"] == "high"]
        assert len(high) >= 1

    def test_too_many_items_warns(self):
        """More than 5 exclusion items should produce a medium warning."""
        prompt = "no guitar, no piano, no drums, no bass, no synth, no vocals"
        findings = validate_prompt.validate_exclusion_prompt(prompt)
        medium = [f for f in findings if f["severity"] == "medium" and "many" in f["issue"].lower()]
        assert len(medium) == 1

    def test_vague_terms_caught(self):
        """Vague exclusion terms should be flagged."""
        prompt = "no instruments, nothing bad"
        findings = validate_prompt.validate_exclusion_prompt(prompt)
        vague = [f for f in findings if "vague" in f["issue"].lower()]
        assert len(vague) >= 1


class TestBuildReport:
    """Tests for report generation."""

    def test_report_structure(self):
        """Report should have all required fields."""
        report = validate_prompt.build_report([], [], "test", "", "/test/path")
        assert report["script"] == "validate-prompt"
        assert report["version"] == "1.1.0"
        assert report["status"] == "pass"
        assert "findings" in report
        assert "summary" in report
        assert "metrics" in report

    def test_critical_finding_sets_fail(self):
        """Critical findings should set status to fail."""
        findings = [{"severity": "critical", "category": "structure", "issue": "test", "fix": "test"}]
        report = validate_prompt.build_report(findings, [], "test", "")
        assert report["status"] == "fail"

    def test_high_finding_sets_warning(self):
        """High findings (without critical) should set status to warning."""
        findings = [{"severity": "high", "category": "structure", "issue": "test", "fix": "test"}]
        report = validate_prompt.build_report(findings, [], "test", "")
        assert report["status"] == "warning"

    def test_metrics_include_char_counts(self):
        """Metrics should include character counts."""
        report = validate_prompt.build_report([], [], "hello world", "no guitar")
        assert report["metrics"]["style_prompt_chars"] == 11
        assert report["metrics"]["exclusion_prompt_chars"] == 9


class TestCLI:
    """Tests for command-line interface."""

    def test_help_flag(self):
        """--help should exit 0 with usage info."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "--help"],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "validate" in result.stdout.lower()

    def test_style_flag_produces_json(self):
        """--style should produce valid JSON output."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "--style", "indie rock, warm vocals"],
            capture_output=True, text=True
        )
        output = json.loads(result.stdout)
        assert output["script"] == "validate-prompt"
        assert "findings" in output

    def test_model_flag_v4_pro(self):
        """--model 'v4 Pro' should apply 200-char limit."""
        prompt = "rock, " * 40  # ~240 chars, over 200 but under 1000
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "--style", prompt, "--model", "v4 Pro"],
            capture_output=True, text=True
        )
        output = json.loads(result.stdout)
        critical = [f for f in output["findings"] if f["severity"] == "critical"]
        assert len(critical) >= 1
        assert "200" in critical[0]["issue"]

    def test_no_args_exits_2(self):
        """No arguments should exit with code 2."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH)],
            capture_output=True, text=True
        )
        assert result.returncode == 2
