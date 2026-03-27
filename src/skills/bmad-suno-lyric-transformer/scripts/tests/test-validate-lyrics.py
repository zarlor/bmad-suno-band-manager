"""Tests for validate-lyrics.py"""

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = str(Path(__file__).parent.parent / "validate-lyrics.py")


def run_script(*args):
    """Run the script and return parsed JSON output."""
    result = subprocess.run(
        [sys.executable, SCRIPT, *args],
        capture_output=True, text=True
    )
    return json.loads(result.stdout) if result.stdout else None, result.returncode


class TestValidateLyrics:
    def test_valid_structured_lyrics(self):
        lyrics = (
            "[Verse 1]\n"
            "Walking through the morning light\n"
            "Counting shadows on the wall\n"
            "\n"
            "[Chorus]\n"
            "Come undone, come undone\n"
            "Let the weight fall where it may\n"
            "\n"
            "[Verse 2]\n"
            "Fingerprints on frosted glass\n"
            "Letters folded into cranes\n"
            "\n"
            "[Chorus]\n"
            "Come undone, come undone\n"
            "Let the weight fall where it may\n"
        )
        report, code = run_script("--text", lyrics)
        assert report is not None
        assert report["script"] == "validate-lyrics"
        assert report["metrics"]["section_count"] == 4
        assert "Verse 1" in report["metrics"]["sections"]
        assert "Chorus" in report["metrics"]["sections"]

    def test_no_section_tags(self):
        lyrics = "Just some raw text\nWith no structure at all\nThree lines of poetry"
        report, code = run_script("--text", lyrics)
        assert report is not None
        issues = [f["issue"] for f in report["findings"]]
        assert any("No section metatags" in i for i in issues)

    def test_style_cue_contamination(self):
        lyrics = "[Verse 1]\nThe punchy drums echo through my mind\n"
        report, code = run_script("--text", lyrics)
        assert report is not None
        issues = [f["issue"] for f in report["findings"]]
        assert any("style cue" in i.lower() for i in issues)

    def test_asterisk_detection(self):
        lyrics = "[Verse 1]\n*This line has asterisks*\n"
        report, code = run_script("--text", lyrics)
        assert report is not None
        issues = [f["issue"] for f in report["findings"]]
        assert any("Asterisk" in i for i in issues)

    def test_empty_lyrics(self):
        report, code = run_script("--text", "")
        assert report is not None
        assert report["status"] == "fail"
        assert any(f["severity"] == "critical" for f in report["findings"])

    def test_unrecognized_metatag(self):
        lyrics = "[Verse 1]\nSome line\n\n[Banana]\nAnother line\n"
        report, code = run_script("--text", lyrics)
        assert report is not None
        issues = [f["issue"] for f in report["findings"]]
        assert any("Unrecognized metatag" in i for i in issues)

    def test_valid_descriptor_metatags(self):
        lyrics = (
            "[Mood: haunting]\n\n"
            "[Verse 1]\n"
            "Walking through the fog\n"
            "Counting all the windows\n"
        )
        report, code = run_script("--text", lyrics)
        assert report is not None
        # Descriptor metatags should not be flagged as unrecognized
        issues = [f["issue"] for f in report["findings"]]
        assert not any("Mood" in i and "Unrecognized" in i for i in issues)

    def test_empty_section(self):
        lyrics = "[Verse 1]\n\n[Chorus]\nSome chorus line\n"
        report, code = run_script("--text", lyrics)
        assert report is not None
        issues = [f["issue"] for f in report["findings"]]
        assert any("Empty section" in i for i in issues)

    def test_report_structure(self):
        lyrics = "[Verse 1]\nA simple test line here\n"
        report, code = run_script("--text", lyrics)
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
        assert "validate" in result.stdout.lower()

    def test_character_count_error(self):
        """Lyrics exceeding 5000 chars (hard limit) should produce high severity finding."""
        # Build lyrics over 5000 characters (hard limit for v4.5+/v5/v5.5)
        line = "This is a long line of lyrics for testing character count limits yeah\n"
        lyrics = "[Verse 1]\n" + line * 80  # well over 5000 chars
        assert len(lyrics) > 5000
        report, code = run_script("--text", lyrics)
        assert report is not None
        issues = [f for f in report["findings"] if "character count" in f["issue"].lower()]
        assert len(issues) >= 1
        assert any(f["severity"] == "high" for f in issues)

    def test_character_count_warning(self):
        """Lyrics between 3000 and 5000 chars should produce medium severity finding (quality degrades)."""
        # Build lyrics between 3000 and 5000 characters (quality budget exceeded)
        line = "This is a medium line of lyrics for testing\n"
        base = "[Verse 1]\n"
        # Each line is 45 chars. Need total between 3000 and 5000.
        count = 72  # 10 + 72*45 = 3250
        lyrics = base + line * count
        total = len(lyrics)
        assert 3000 < total < 5000, f"Got {total} chars"
        report, code = run_script("--text", lyrics)
        assert report is not None
        issues = [f for f in report["findings"] if "character count" in f["issue"].lower()]
        assert len(issues) >= 1
        assert any(f["severity"] == "medium" for f in issues)

    def test_character_count_in_metrics(self):
        """Report metrics should include character_count."""
        lyrics = "[Verse 1]\nHello world\n"
        report, code = run_script("--text", lyrics)
        assert report is not None
        assert "character_count" in report["metrics"]
        assert report["metrics"]["character_count"] == len(lyrics)

    def test_punctuation_density_detection(self):
        """Lines with heavy punctuation should trigger a rhythm finding."""
        lyrics = "[Verse 1]\nwell, - ; : ... yes\n"
        report, code = run_script("--text", lyrics)
        assert report is not None
        issues = [f for f in report["findings"] if "punctuation" in f["issue"].lower()]
        assert len(issues) >= 1
        assert issues[0]["severity"] == "low"
        assert issues[0]["category"] == "rhythm"

    def test_clean_lyrics_normal_punctuation_passes(self):
        """Clean lyrics with normal punctuation should pass without punctuation findings."""
        lyrics = (
            "[Verse 1]\n"
            "Walking through the morning light\n"
            "Counting shadows on the wall\n"
            "\n"
            "[Chorus]\n"
            "Come undone, come undone\n"
            "Let the weight fall where it may\n"
            "\n"
            "[Verse 2]\n"
            "Fingerprints on frosted glass\n"
            "Letters folded into cranes\n"
            "\n"
            "[Chorus]\n"
            "Come undone, come undone\n"
            "Let the weight fall where it may\n"
        )
        report, code = run_script("--text", lyrics)
        assert report is not None
        punct_issues = [f for f in report["findings"] if "punctuation" in f["issue"].lower()]
        assert len(punct_issues) == 0

    def test_new_section_tags_recognized(self):
        """New section tags like Guitar Solo, Instrumental, etc. should not be flagged."""
        new_tags = [
            "Guitar Solo", "Piano Solo", "Sax Solo", "Saxophone Solo",
            "Drum Solo", "Bass Solo", "Solo", "Instrumental", "Interlude",
            "Build", "Build-Up", "Buildup", "Drop", "Hook", "Refrain",
            "Post-Chorus", "End", "Fade Out", "Fade In", "Break",
        ]
        for tag in new_tags:
            lyrics = f"[Verse 1]\nSome line one\nSome line two\n\n[{tag}]\nContent here\n"
            report, code = run_script("--text", lyrics)
            assert report is not None, f"No report for [{tag}]"
            unrecognized = [f for f in report["findings"]
                           if "Unrecognized" in f.get("issue", "") and tag in f.get("issue", "")]
            assert len(unrecognized) == 0, f"[{tag}] was flagged as unrecognized"

    def test_vocal_cues_recognized(self):
        """Vocal delivery cues like [Harmonized] should not be flagged as unrecognized."""
        cues = ["Harmonized", "Hummed", "Humming", "Whistled", "Whistling",
                "Crooning", "Scat", "Call and Response"]
        for cue in cues:
            lyrics = f"[Verse 1]\nSome line here\n[{cue}]\nMore content\n"
            report, code = run_script("--text", lyrics)
            assert report is not None, f"No report for [{cue}]"
            unrecognized = [f for f in report["findings"]
                           if "Unrecognized" in f.get("issue", "") and cue in f.get("issue", "")]
            assert len(unrecognized) == 0, f"[{cue}] was flagged as unrecognized"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
