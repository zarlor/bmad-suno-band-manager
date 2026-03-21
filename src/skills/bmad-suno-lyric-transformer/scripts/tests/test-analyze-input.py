"""Tests for analyze-input.py"""

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = str(Path(__file__).parent.parent / "analyze-input.py")


def run_script(*args):
    """Run the script and return parsed JSON output."""
    result = subprocess.run(
        [sys.executable, SCRIPT, *args],
        capture_output=True, text=True
    )
    return json.loads(result.stdout) if result.stdout else None, result.returncode


class TestAnalyzeInput:
    def test_basic_metrics(self):
        text = "Hello world\nThis is a test\nThree lines here"
        report, code = run_script("--text", text)
        assert report is not None
        m = report["metrics"]
        assert m["line_count"] == 3
        assert m["non_empty_line_count"] == 3
        assert m["word_count"] == 9
        assert m["character_count"] > 0

    def test_detects_existing_structure(self):
        text = "[Verse 1]\nSome lyrics here\nMore lyrics\n\n[Chorus]\nChorus line"
        report, code = run_script("--text", text)
        assert report is not None
        m = report["metrics"]
        assert m["has_existing_structure"] is True
        assert "Verse 1" in m["existing_tags"]
        assert "Chorus" in m["existing_tags"]

    def test_no_structure_detected(self):
        text = "Just raw text\nWith no brackets\nPlain poetry"
        report, code = run_script("--text", text)
        assert report is not None
        m = report["metrics"]
        assert m["has_existing_structure"] is False
        assert m["existing_tags"] == []

    def test_repeated_phrases(self):
        text = "come back to me tonight\nwhen the stars are bright\ncome back to me tonight\nunder the pale moonlight"
        report, code = run_script("--text", text)
        assert report is not None
        m = report["metrics"]
        phrases = [p["phrase"] for p in m["repeated_phrases"]]
        assert any("come back to me" in p for p in phrases)

    def test_rhyme_pairs(self):
        text = "Walking down the street\nFeeling the beat\nLooking for the light\nShining in the night"
        report, code = run_script("--text", text)
        assert report is not None
        m = report["metrics"]
        rhymes = m["potential_rhyme_pairs"]
        rhyme_words = [set(r["words"]) for r in rhymes]
        assert any({"street", "beat"} == w for w in rhyme_words) or any({"light", "night"} == w for w in rhyme_words)

    def test_short_structure_estimate(self):
        text = "\n".join(f"Line {i}" for i in range(1, 10))
        report, code = run_script("--text", text)
        assert report is not None
        m = report["metrics"]
        assert m["estimated_structure"] == "short"

    def test_medium_structure_estimate(self):
        text = "\n".join(f"Line number {i} of the song" for i in range(1, 25))
        report, code = run_script("--text", text)
        assert report is not None
        m = report["metrics"]
        assert m["estimated_structure"] == "medium"

    def test_long_structure_estimate(self):
        text = "\n".join(f"Line number {i} of a very long song" for i in range(1, 35))
        report, code = run_script("--text", text)
        assert report is not None
        m = report["metrics"]
        assert m["estimated_structure"] == "long"

    def test_report_structure(self):
        report, code = run_script("--text", "Some text")
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
        assert "analyze" in result.stdout.lower()


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
