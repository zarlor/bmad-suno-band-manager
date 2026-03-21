"""Tests for cliche-detector.py"""

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = str(Path(__file__).parent.parent / "cliche-detector.py")


def run_script(*args):
    """Run the script and return parsed JSON output."""
    result = subprocess.run(
        [sys.executable, SCRIPT, *args],
        capture_output=True, text=True
    )
    return json.loads(result.stdout) if result.stdout else None, result.returncode


class TestClicheDetector:
    def test_detects_fire_in_soul(self):
        report, code = run_script("--text", "There's a fire in my soul tonight")
        assert report is not None
        assert report["metrics"]["total_cliches_found"] >= 1
        assert any("fire in my soul" in f["data"]["matched_text"] for f in report["findings"])

    def test_detects_dance_in_rain(self):
        report, code = run_script("--text", "We'll dance in the rain together")
        assert report is not None
        assert report["metrics"]["total_cliches_found"] >= 1

    def test_detects_broken_heart(self):
        report, code = run_script("--text", "My broken heart won't heal")
        assert report is not None
        assert report["metrics"]["total_cliches_found"] >= 1

    def test_detects_stand_tall(self):
        report, code = run_script("--text", "I'm standing tall against the wind")
        assert report is not None
        assert report["metrics"]["total_cliches_found"] >= 1

    def test_no_cliches_in_clean_text(self):
        report, code = run_script("--text", "The kitchen table holds three plates\nSteam rising from the coffee cup")
        assert report is not None
        assert report["metrics"]["total_cliches_found"] == 0
        assert code == 0

    def test_skips_metatags(self):
        text = "[Verse 1]\nFire in my soul\n[Chorus]\nClean lyrics here"
        report, code = run_script("--text", text)
        assert report is not None
        # Should find the cliche in the lyric line, not in metatags
        assert report["metrics"]["total_cliches_found"] >= 1

    def test_provides_alternatives(self):
        report, code = run_script("--text", "Rise from the ashes of what we were")
        assert report is not None
        assert len(report["findings"]) > 0
        finding = report["findings"][0]
        assert "alternatives" in finding["data"]
        assert len(finding["data"]["alternatives"]) > 0

    def test_multiple_cliches_in_one_text(self):
        text = (
            "Fire in my soul keeps burning bright\n"
            "Standing tall through broken dreams\n"
            "Dance in the rain with a heart of gold\n"
        )
        report, code = run_script("--text", text)
        assert report is not None
        assert report["metrics"]["total_cliches_found"] >= 3

    def test_case_insensitive(self):
        report, code = run_script("--text", "FIRE IN MY SOUL")
        assert report is not None
        assert report["metrics"]["total_cliches_found"] >= 1

    def test_report_structure(self):
        report, code = run_script("--text", "Just a normal line")
        assert report is not None
        assert "script" in report
        assert "version" in report
        assert "timestamp" in report
        assert "status" in report
        assert "metrics" in report
        assert "findings" in report
        assert "summary" in report

    def test_help_flag(self):
        result = subprocess.run(
            [sys.executable, SCRIPT, "--help"],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "cliche" in result.stdout.lower()


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
