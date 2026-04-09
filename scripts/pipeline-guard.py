#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Stop hook guard: blocks Suno package output if required skills weren't invoked.

This script runs as a Claude Code Stop hook. It checks whether the assistant's
response contains a Suno-ready package (style prompt + lyrics + settings) and
verifies that suno-style-prompt-builder and suno-lyric-transformer were invoked
via the Skill tool during the conversation.

If a package is detected without prior skill invocation, the response is blocked
and Claude is instructed to invoke the missing skills.

Usage: Configure as a Stop hook in .claude/settings.local.json:
    {
      "hooks": {
        "Stop": [{
          "hooks": [{
            "type": "command",
            "command": "python3 path/to/pipeline-guard.py",
            "timeout": 10
          }]
        }]
      }
    }

The script reads JSON from stdin (Claude Code hook input) and outputs
a JSON decision to stdout.
"""

import json
import re
import sys


def detect_suno_package(message: str) -> bool:
    """Check if the message contains a Suno-ready package."""
    patterns = [
        r"##\s*Style Prompt.*v\d",
        r"###\s*Copy-Ready:\s*Style Prompt",
        r"##\s*Copy-Ready Lyrics",
        r"##\s*Your Suno Package",
        r"###\s*Copy-Ready:\s*Exclude Styles",
        r"\|\s*Setting\s*\|\s*Value\s*\|.*\n.*Weirdness:",
        r"paste into Suno",
    ]
    return any(re.search(p, message, re.IGNORECASE | re.MULTILINE) for p in patterns)


def _extract_tool_uses(entry: dict) -> list[dict]:
    """Walk the transcript entry structure to find all tool_use items.

    Claude Code transcripts nest tool_use items inside
    entry.message.content[] for assistant messages. Older structures
    may place them at the top level. This helper handles both.
    """
    tool_uses = []
    # Top-level shapes (defensive)
    if entry.get("type") == "tool_use":
        tool_uses.append(entry)
    if "tool_name" in entry and entry.get("tool_name"):
        # Legacy/flattened shape: tool_name + tool_input
        tool_uses.append({
            "name": entry.get("tool_name"),
            "input": entry.get("tool_input", {}),
        })
    # Nested shape: entry.message.content[] with items of type "tool_use"
    message = entry.get("message", {})
    if isinstance(message, dict):
        content = message.get("content", [])
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "tool_use":
                    tool_uses.append(item)
    return tool_uses


def check_skill_invocations(transcript_path: str) -> set[str]:
    """Read the transcript and find which skills were invoked.

    Checks both direct Skill tool invocations AND Agent subagent
    invocations that reference skill names (for parallel execution
    via the Refine Song workflow).
    """
    skills = set()
    skill_names_to_detect = {
        "suno-style-prompt-builder",
        "suno-lyric-transformer",
        "suno-feedback-elicitor",
        "suno-band-profile-manager",
    }
    if not transcript_path:
        return skills
    try:
        with open(transcript_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                for tool_use in _extract_tool_uses(entry):
                    name = tool_use.get("name", "")
                    tool_input = tool_use.get("input", {}) or {}
                    if name == "Skill":
                        skill_name = tool_input.get("skill", "")
                        if skill_name:
                            skills.add(skill_name)
                    elif name == "Agent":
                        # Agent subagent invocations that reference skill
                        # names (parallel skill execution pattern)
                        prompt = tool_input.get("prompt", "")
                        for sn in skill_names_to_detect:
                            if sn in prompt:
                                skills.add(sn)
        return skills
    except (OSError, PermissionError):
        return skills


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    # Prevent infinite loops
    if input_data.get("stop_hook_active", False):
        sys.exit(0)

    message = input_data.get("last_assistant_message", "")
    if not message:
        sys.exit(0)

    # Only check if there's a Suno package in the output
    if not detect_suno_package(message):
        sys.exit(0)

    # Check which skills were invoked
    transcript_path = input_data.get("transcript_path", "")
    skills_invoked = check_skill_invocations(transcript_path)

    missing = []
    if "suno-style-prompt-builder" not in skills_invoked:
        missing.append("suno-style-prompt-builder")

    # Only require lyric transformer if lyrics are present (not instrumental)
    is_instrumental = bool(re.search(r"Instrumental \(no vocals\)", message))
    if "suno-lyric-transformer" not in skills_invoked and not is_instrumental:
        missing.append("suno-lyric-transformer")

    if missing:
        output = {
            "decision": "block",
            "reason": (
                f"PIPELINE VIOLATION: You are presenting a Suno package without "
                f"invoking the required skills: {', '.join(missing)}. "
                f"The formal pipeline is mandatory per Mac's creed. "
                f"Invoke the missing skill(s) via the Skill tool now, "
                f"then re-present the package with their validated output."
            ),
        }
        print(json.dumps(output))

    sys.exit(0)


if __name__ == "__main__":
    main()
