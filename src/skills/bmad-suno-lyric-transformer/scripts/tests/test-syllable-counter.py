"""Tests for syllable-counter.py"""

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = str(Path(__file__).parent.parent / "syllable-counter.py")


def run_script(*args):
    """Run the script and return parsed JSON output."""
    result = subprocess.run(
        [sys.executable, SCRIPT, *args],
        capture_output=True, text=True
    )
    return json.loads(result.stdout) if result.stdout else None, result.returncode


# Also test the count_syllables function directly
import importlib.util
_spec = importlib.util.spec_from_file_location("syllable_counter", Path(__file__).parent.parent / "syllable-counter.py")
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
count_syllables = _mod.count_syllables
estimate_duration = _mod.estimate_duration
format_duration_range = _mod.format_duration_range


class TestSyllableCounting:
    """Test individual word syllable counting."""

    def test_one_syllable_words(self):
        for word in ["cat", "dog", "the", "run", "light", "dream"]:
            assert count_syllables(word) == 1, f"Expected 1 syllable for '{word}', got {count_syllables(word)}"

    def test_two_syllable_words(self):
        for word in ["hello", "window", "walking", "morning", "shadow"]:
            assert count_syllables(word) == 2, f"Expected 2 syllables for '{word}', got {count_syllables(word)}"

    def test_three_syllable_words(self):
        for word in ["beautiful", "another", "everyone", "different"]:
            result = count_syllables(word)
            assert result == 3, f"Expected 3 syllables for '{word}', got {result}"

    def test_contractions(self):
        assert count_syllables("I'm") == 1
        assert count_syllables("don't") == 1
        assert count_syllables("couldn't") == 2

    def test_empty_string(self):
        assert count_syllables("") == 0


class TestLyricsAnalysis:
    """Test full lyrics analysis via the script."""

    def test_basic_analysis(self):
        lyrics = (
            "[Verse 1]\n"
            "Walking through the morning light\n"
            "Counting shadows on the wall\n"
        )
        report, code = run_script("--text", lyrics)
        assert report is not None
        assert report["script"] == "syllable-counter"
        assert report["metrics"]["total_lyric_lines"] == 2
        assert report["metrics"]["total_syllables"] > 0

    def test_section_grouping(self):
        lyrics = (
            "[Verse 1]\n"
            "Short line here\n"
            "Another short one\n"
            "\n"
            "[Chorus]\n"
            "The chorus comes in strong and bold\n"
            "With longer lines that carry more weight\n"
        )
        report, code = run_script("--text", lyrics)
        assert report is not None
        assert len(report["section_analysis"]) == 2
        section_names = [s["section"] for s in report["section_analysis"]]
        assert "[Verse 1]" in section_names
        assert "[Chorus]" in section_names

    def test_line_data_includes_syllables(self):
        lyrics = "[Verse 1]\nHello world\n"
        report, code = run_script("--text", lyrics)
        assert report is not None
        assert len(report["line_data"]) == 1
        assert "syllables" in report["line_data"][0]
        assert report["line_data"][0]["syllables"] > 0

    def test_skips_metatags(self):
        lyrics = "[Mood: haunting]\n[Verse 1]\nWalking through fog\n"
        report, code = run_script("--text", lyrics)
        assert report is not None
        # Only the lyric line should be counted, not metatags
        assert report["metrics"]["total_lyric_lines"] == 1

    def test_high_variance_warning(self):
        lyrics = (
            "[Verse 1]\n"
            "Hi\n"
            "This is a much longer line with many more syllables than the first\n"
            "Short\n"
            "Another really long line that goes on and on and on\n"
        )
        report, code = run_script("--text", lyrics)
        assert report is not None
        # Should flag high syllable variance
        issues = [f["issue"] for f in report["findings"]]
        assert any("variance" in i.lower() or "syllable" in i.lower() for i in issues)

    def test_report_structure(self):
        lyrics = "[Verse 1]\nA simple test line\n"
        report, code = run_script("--text", lyrics)
        assert report is not None
        assert "script" in report
        assert "version" in report
        assert "timestamp" in report
        assert "status" in report
        assert "metrics" in report
        assert "line_data" in report
        assert "section_analysis" in report
        assert "findings" in report
        assert "summary" in report

    def test_help_flag(self):
        result = subprocess.run(
            [sys.executable, SCRIPT, "--help"],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "syllable" in result.stdout.lower()


class TestDurationEstimation:
    """Test duration estimation function."""

    def test_zero_lines(self):
        min_s, max_s = estimate_duration(0, 0)
        assert min_s == 0
        assert max_s == 0

    def test_one_line(self):
        # 7.0 avg syllables = mid range (3.0-4.5 secs/line)
        min_s, max_s = estimate_duration(1, 7.0)
        assert min_s == round(1 * 3.5)  # low-density range
        assert max_s == round(1 * 5.5)

    def test_typical_song(self):
        # 20 lines at 7.0 avg syllables (mid range)
        min_s, max_s = estimate_duration(20, 7.0)
        assert min_s == round(20 * 3.5)  # 70
        assert max_s == round(20 * 5.5)  # 110

    def test_high_density_faster(self):
        # High syllable density = faster delivery = less time per line
        min_s, max_s = estimate_duration(20, 12.0)
        assert min_s == round(20 * 2.5)  # 50
        assert max_s == round(20 * 4.0)  # 80

    def test_instrumental_sections_add_time(self):
        # Sections with instrumental tags add time
        sections = [
            {"name": "[Intro]", "lines": []},
            {"name": "[Verse]", "lines": [{"syllables": 7}] * 4},
            {"name": "[Guitar Solo]", "lines": []},
            {"name": "[Outro]", "lines": []},
        ]
        min_s, max_s = estimate_duration(4, 7.0, sections)
        # 4 lines at mid range + intro (5-15) + guitar solo (10-25) + outro (8-20)
        assert min_s > round(4 * 3.5)  # More than just lyrics
        assert max_s > round(4 * 5.5)

    def test_formatted_range(self):
        formatted = format_duration_range(50, 90)
        assert formatted == "0:50-1:30"

    def test_formatted_range_zero(self):
        formatted = format_duration_range(0, 0)
        assert formatted == "0:00-0:00"

    def test_formatted_range_large(self):
        formatted = format_duration_range(120, 240)
        assert formatted == "2:00-4:00"

    def test_duration_in_report(self):
        lyrics = (
            "[Verse 1]\n"
            "Walking through the morning light\n"
            "Counting shadows on the wall\n"
            "\n"
            "[Chorus]\n"
            "Come undone come undone\n"
            "Let the weight fall where it may\n"
        )
        report, code = run_script("--text", lyrics)
        assert report is not None
        duration = report["metrics"]["estimated_duration"]
        assert "min_seconds" in duration
        assert "max_seconds" in duration
        assert "formatted" in duration
        assert duration["min_seconds"] > 0
        assert duration["max_seconds"] > duration["min_seconds"]
        # Check formatted string pattern M:SS-M:SS
        assert "-" in duration["formatted"]

    def test_estimate_duration_flag(self):
        lyrics = "[Verse 1]\nHello world\n"
        report, code = run_script("--text", lyrics, "--estimate-duration")
        assert report is not None
        assert "estimated_duration" in report["metrics"]


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
