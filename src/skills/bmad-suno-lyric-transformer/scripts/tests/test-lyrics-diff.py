"""Tests for lyrics-diff.py"""

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = str(Path(__file__).parent.parent / "lyrics-diff.py")


def run_script(*args):
    """Run the script and return parsed JSON output."""
    result = subprocess.run(
        [sys.executable, SCRIPT, *args],
        capture_output=True, text=True
    )
    return json.loads(result.stdout) if result.stdout else None, result.returncode


class TestLyricsDiff:
    def test_identical_lyrics(self):
        text = "[Verse 1]\nHello world\nGoodbye moon"
        report, code = run_script("--original-text", text, "--transformed-text", text)
        assert report is not None
        assert report["status"] == "pass"
        assert len(report["changes"]) == 0
        assert report["summary"]["lines_added"] == 0
        assert report["summary"]["lines_removed"] == 0
        assert report["summary"]["lines_modified"] == 0

    def test_modified_line(self):
        original = "[Verse 1]\nWalking through the rain"
        transformed = "[Verse 1]\nRunning through the storm"
        report, code = run_script("--original-text", original, "--transformed-text", transformed)
        assert report is not None
        assert report["status"] == "info"
        modified = [c for c in report["changes"] if c["type"] == "modified"]
        assert len(modified) >= 1
        assert report["summary"]["lines_modified"] >= 1

    def test_added_lines(self):
        original = "[Verse 1]\nLine one"
        transformed = "[Verse 1]\nLine one\nLine two\nLine three"
        report, code = run_script("--original-text", original, "--transformed-text", transformed)
        assert report is not None
        added = [c for c in report["changes"] if c["type"] == "added"]
        assert len(added) >= 1
        assert report["summary"]["lines_added"] >= 1

    def test_removed_lines(self):
        original = "[Verse 1]\nLine one\nLine two\nLine three"
        transformed = "[Verse 1]\nLine one"
        report, code = run_script("--original-text", original, "--transformed-text", transformed)
        assert report is not None
        removed = [c for c in report["changes"] if c["type"] == "removed"]
        assert len(removed) >= 1
        assert report["summary"]["lines_removed"] >= 1

    def test_section_tracking(self):
        original = "[Verse 1]\nOld verse line\n\n[Chorus]\nOld chorus line"
        transformed = "[Verse 1]\nNew verse line\n\n[Chorus]\nNew chorus line"
        report, code = run_script("--original-text", original, "--transformed-text", transformed)
        assert report is not None
        assert len(report["summary"]["sections_affected"]) >= 1

    def test_unified_diff_output(self):
        original = "[Verse 1]\nHello"
        transformed = "[Verse 1]\nGoodbye"
        report, code = run_script("--original-text", original, "--transformed-text", transformed)
        assert report is not None
        assert "unified_diff" in report
        assert len(report["unified_diff"]) > 0

    def test_file_input(self, tmp_path):
        orig_file = tmp_path / "orig.txt"
        trans_file = tmp_path / "trans.txt"
        orig_file.write_text("[Verse 1]\nOriginal line")
        trans_file.write_text("[Verse 1]\nTransformed line")
        report, code = run_script("--original", str(orig_file), "--transformed", str(trans_file))
        assert report is not None
        assert len(report["changes"]) >= 1

    def test_report_structure(self):
        report, code = run_script("--original-text", "a", "--transformed-text", "b")
        assert report is not None
        assert "script" in report
        assert "version" in report
        assert "timestamp" in report
        assert "status" in report
        assert "changes" in report
        assert "summary" in report
        assert "unified_diff" in report

    def test_help_flag(self):
        result = subprocess.run(
            [sys.executable, SCRIPT, "--help"],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "diff" in result.stdout.lower()


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
