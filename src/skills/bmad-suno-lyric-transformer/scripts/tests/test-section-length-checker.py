"""Tests for section-length-checker.py"""

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = str(Path(__file__).parent.parent / "section-length-checker.py")


def run_script(*args):
    """Run the script and return parsed JSON output."""
    result = subprocess.run(
        [sys.executable, SCRIPT, *args],
        capture_output=True, text=True
    )
    return json.loads(result.stdout) if result.stdout else None, result.returncode


class TestSectionLengthChecker:
    def test_sections_within_range(self):
        lyrics = (
            "[Verse 1]\n"
            "Line one of the verse\n"
            "Line two of the verse\n"
            "Line three of the verse\n"
            "Line four of the verse\n"
            "\n"
            "[Chorus]\n"
            "Chorus line one\n"
            "Chorus line two\n"
            "Chorus line three\n"
        )
        report, code = run_script("--text", lyrics)
        assert report is not None
        assert report["status"] == "pass"
        assert report["metrics"]["sections_pass"] == 2
        assert report["metrics"]["sections_fail"] == 0

    def test_verse_too_short(self):
        lyrics = (
            "[Verse 1]\n"
            "Only one line\n"
            "\n"
            "[Chorus]\n"
            "Chorus one\n"
            "Chorus two\n"
        )
        report, code = run_script("--text", lyrics)
        assert report is not None
        assert report["status"] == "warning"
        short_sections = [s for s in report["sections"] if s["status"] == "short"]
        assert len(short_sections) >= 1
        assert short_sections[0]["base_name"] == "verse"

    def test_verse_too_long(self):
        lyrics = "[Verse 1]\n" + "\n".join(f"Line {i}" for i in range(1, 12)) + "\n"
        report, code = run_script("--text", lyrics)
        assert report is not None
        long_sections = [s for s in report["sections"] if s["status"] == "long"]
        assert len(long_sections) >= 1

    def test_intro_can_be_empty(self):
        lyrics = (
            "[Intro]\n"
            "\n"
            "[Verse 1]\n"
            "Line one\nLine two\nLine three\nLine four\n"
        )
        report, code = run_script("--text", lyrics)
        assert report is not None
        intro = [s for s in report["sections"] if s["base_name"] == "intro"]
        assert len(intro) == 1
        assert intro[0]["status"] == "pass"

    def test_numbered_sections_normalized(self):
        lyrics = (
            "[Verse 2]\n"
            "Line one\nLine two\nLine three\nLine four\n"
            "\n"
            "[Chorus]\n"
            "Chorus one\nChorus two\n"
        )
        report, code = run_script("--text", lyrics)
        assert report is not None
        verse = [s for s in report["sections"] if s["tag"] == "Verse 2"]
        assert len(verse) == 1
        assert verse[0]["base_name"] == "verse"

    def test_unknown_section_type(self):
        lyrics = "[Spoken Word]\nSome content\nMore content\n"
        report, code = run_script("--text", lyrics)
        assert report is not None
        unknown = [s for s in report["sections"] if s["status"] == "unknown"]
        assert len(unknown) >= 1

    def test_report_structure(self):
        lyrics = "[Verse 1]\nLine one\nLine two\nLine three\nLine four\n"
        report, code = run_script("--text", lyrics)
        assert report is not None
        assert "script" in report
        assert "version" in report
        assert "timestamp" in report
        assert "status" in report
        assert "sections" in report
        assert "findings" in report
        assert "summary" in report

    def test_help_flag(self):
        result = subprocess.run(
            [sys.executable, SCRIPT, "--help"],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "section" in result.stdout.lower()

    def test_descriptor_metatags_not_counted_as_content(self):
        """Descriptor metatags like [Energy: slow] should not inflate line counts."""
        lyrics = (
            "[Verse 1]\n"
            "[Energy: slow]\n"
            "[Vocal Style: clean]\n"
            "[Mood: dark]\n"
            "Line one of the verse\n"
            "Line two of the verse\n"
            "Line three of the verse\n"
            "Line four of the verse\n"
        )
        report, code = run_script("--text", lyrics)
        assert report is not None
        verse = [s for s in report["sections"] if s["base_name"] == "verse"]
        assert len(verse) == 1
        # Should count only 4 lyric lines, not 7
        assert verse[0]["line_count"] == 4
        assert verse[0]["status"] == "pass"

    def test_prog_genre_relaxes_verse_limit(self):
        """With --genre prog, verses can have up to 16 lines without warning."""
        lines = "\n".join(f"Line {i}" for i in range(1, 13))
        lyrics = f"[Verse 1]\n{lines}\n"
        # Without genre flag, 12 lines should be too long (max 8)
        report_normal, _ = run_script("--text", lyrics)
        assert report_normal is not None
        verse_normal = [s for s in report_normal["sections"] if s["base_name"] == "verse"]
        assert verse_normal[0]["status"] == "long"

        # With prog genre, 12 lines should pass (max becomes 16)
        report_prog, _ = run_script("--text", lyrics, "--genre", "prog")
        assert report_prog is not None
        verse_prog = [s for s in report_prog["sections"] if s["base_name"] == "verse"]
        assert verse_prog[0]["status"] == "pass"

    def test_interlude_is_known_section(self):
        """Interlude should now be a known section type with defined range."""
        lyrics = "[Interlude]\nSome content\nMore content\n"
        report, code = run_script("--text", lyrics)
        assert report is not None
        interlude = [s for s in report["sections"] if s["base_name"] == "interlude"]
        assert len(interlude) == 1
        assert interlude[0]["status"] == "pass"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
