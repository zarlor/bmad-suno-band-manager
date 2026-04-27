#!/usr/bin/env python3
"""Post-unpack reconciliation helper for the Mac sidecar.

After `unpack-portable.sh/.ps1` extracts a sync archive on a receiving
machine, the sidecar index.md still reflects the receiving machine's prior
local state — even though the freshly-arrived files (WIPs, songbook entries,
band profiles, playlist docs, session-context) may contain updates the
sidecar narrative should integrate.

This script produces a punch list for the agent to walk through:

  1. **Files modified more recently than index.md** — candidates for
     narrative integration (session history, current work, pending threads).
  2. **Validator findings** — calls `validate-sidecar.py` so drift between
     the sidecar narrative and the unpacked file state surfaces immediately.

The script does not edit files. The agent is responsible for reading each
candidate and deciding whether the sidecar narrative should integrate its
content, surfacing the decision to the user via the usual handoff
checkpoint.

Usage:
    python3 scripts/reconcile-sidecar.py [project_root]
    python3 scripts/reconcile-sidecar.py --format json

Exit codes:
    0 — sidecar and files are in sync (or sidecar absent — nothing to check)
    1 — candidates found or validator reported errors (agent should reconcile)
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _format_mtime(mtime: float) -> str:
    return datetime.fromtimestamp(mtime, tz=timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )


def find_newer_docs(project_root: Path, index_mtime: float) -> list[dict[str, Any]]:
    """Return docs/*.md files whose mtime is newer than the sidecar index.md.

    These are the most likely candidates for sidecar narrative integration —
    a freshly unpacked WIP update, session-context edit, or songbook
    addition that hasn't yet shown up in the sidecar's story.
    """
    docs_root = project_root / "docs"
    if not docs_root.is_dir():
        return []

    candidates: list[dict[str, Any]] = []
    for path in sorted(docs_root.rglob("*.md")):
        try:
            mtime = path.stat().st_mtime
        except OSError:
            continue
        if mtime <= index_mtime:
            continue
        rel = str(path.relative_to(project_root))
        candidates.append(
            {
                "path": rel,
                "mtime": _format_mtime(mtime),
                "delta_seconds": int(mtime - index_mtime),
            }
        )
    return candidates


def run_validator(project_root: Path) -> dict[str, Any]:
    """Invoke validate-sidecar.py and return its JSON payload.

    Soft-fail if the validator isn't present — older installs or partial
    checkouts shouldn't break the reconcile flow.
    """
    validator = Path(__file__).parent / "validate-sidecar.py"
    if not validator.is_file():
        return {"status": "skipped", "reason": "validate-sidecar.py not found"}

    try:
        result = subprocess.run(
            [
                sys.executable,
                str(validator),
                str(project_root),
                "--format",
                "json",
                "--warn-only",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        return {"status": "error", "reason": f"could not invoke validator: {exc}"}

    if result.returncode not in (0, 1):
        return {
            "status": "error",
            "reason": f"validator exited {result.returncode}",
            "stderr": result.stderr.strip(),
        }

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return {"status": "error", "reason": f"validator output unparseable: {exc}"}


def format_text(payload: dict[str, Any]) -> str:
    lines = [
        "Sidecar Reconciliation Report",
        "=" * 29,
        "",
    ]

    status = payload.get("status", "unknown")
    lines.append(f"Status: {status}")
    lines.append(f"Sidecar index.md: {payload.get('index_path', 'unknown')}")
    if payload.get("index_mtime"):
        lines.append(f"Index last updated: {payload['index_mtime']}")
    lines.append("")

    candidates = payload.get("newer_files", [])
    lines.append(
        f"Files modified more recently than the sidecar: {len(candidates)}"
    )
    if candidates:
        lines.append("")
        lines.append(
            "These are candidates for narrative integration. Review each and "
            "decide whether the sidecar's session history, current work, or "
            "catalog status should be updated before continuing:"
        )
        lines.append("")
        for item in candidates:
            lines.append(f"  - {item['path']}  (modified {item['mtime']})")
        lines.append("")

    validator = payload.get("validator", {})
    v_status = validator.get("status", "unknown")
    lines.append(f"Validator: {v_status}")
    findings = validator.get("findings", []) or []
    if findings:
        by_category: dict[str, list[dict[str, Any]]] = {}
        for f in findings:
            by_category.setdefault(f.get("category", "other"), []).append(f)
        for category, items in sorted(by_category.items()):
            lines.append(f"  [{category.upper()}] ({len(items)})")
            for f in items:
                lines.append(
                    f"    ({f.get('severity', 'warning')}) "
                    f"{f.get('path', '')} — {f.get('message', '')}"
                )
        lines.append("")

    if payload.get("needs_reconciliation"):
        lines.append(
            "ACTION NEEDED: walk the punch list above with the user and "
            "integrate changes into the sidecar narrative before packing "
            "a return sync."
        )
    else:
        lines.append("CLEAN: sidecar is in sync with unpacked file state.")

    return "\n".join(lines)


def build_report(project_root: Path) -> dict[str, Any]:
    index_path = (
        project_root / "_bmad" / "_memory" / "band-manager-sidecar" / "index.md"
    )
    payload: dict[str, Any] = {
        "index_path": str(
            index_path.relative_to(project_root)
            if index_path.is_relative_to(project_root)
            else index_path
        ),
    }

    if not index_path.is_file():
        payload["status"] = "no_sidecar"
        payload["newer_files"] = []
        payload["validator"] = {"status": "skipped", "reason": "no sidecar index.md"}
        payload["needs_reconciliation"] = False
        return payload

    index_mtime = index_path.stat().st_mtime
    payload["index_mtime"] = _format_mtime(index_mtime)
    payload["newer_files"] = find_newer_docs(project_root, index_mtime)
    payload["validator"] = run_validator(project_root)

    validator_findings = payload["validator"].get("findings", []) or []
    has_errors = any(f.get("severity") == "error" for f in validator_findings)
    payload["needs_reconciliation"] = bool(payload["newer_files"]) or has_errors
    payload["status"] = (
        "needs_reconciliation" if payload["needs_reconciliation"] else "clean"
    )
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Post-unpack reconciliation helper for the Mac sidecar."
    )
    parser.add_argument(
        "project_root",
        nargs="?",
        default=".",
        help="Project root directory (default: current directory)",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    if not project_root.is_dir():
        print(f"ERROR: project root not found: {project_root}", file=sys.stderr)
        return 2

    payload = build_report(project_root)

    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(format_text(payload))

    return 1 if payload.get("needs_reconciliation") else 0


if __name__ == "__main__":
    sys.exit(main())
