#!/usr/bin/env python3
"""CI gate: version.txt must not regress vs merge-base; CHANGELOG on bump."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE_DIR = Path(__file__).resolve().parent / "release"
sys.path.insert(0, str(RELEASE_DIR))

import os

from semver import compare_semver, parse_semver

VERSION_REL = os.environ.get("VERSION_FILE", "version.txt")
VERSION_FILE = ROOT / VERSION_REL
CHANGELOG = ROOT / "CHANGELOG.md"


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def merge_base_ref() -> str:
    for ref in ("origin/main", "main"):
        if run_git("rev-parse", "--verify", ref):
            base = run_git("merge-base", "HEAD", ref)
            if base:
                return base
    return "HEAD~1"


def version_at_ref(ref: str) -> str | None:
    try:
        content = run_git("show", f"{ref}:{VERSION_REL}")
    except Exception:
        return None
    if not content:
        return None
    ver = content.strip()
    return ver if parse_semver(ver) else None


def changelog_has_version(version: str) -> bool:
    if not CHANGELOG.exists():
        return False
    text = CHANGELOG.read_text(encoding="utf-8")
    return bool(re.search(rf"^## \[{re.escape(version)}\]", text, re.MULTILINE))


def main() -> int:
    current = VERSION_FILE.read_text(encoding="utf-8").strip()
    if parse_semver(current) is None:
        print(f"Invalid {VERSION_REL}: {current}", file=sys.stderr)
        return 1

    base_ref = merge_base_ref()
    base_version = version_at_ref(base_ref)
    if base_version and compare_semver(current, base_version) < 0:
        print(
            f"Version regression: {VERSION_REL}={current} < merge-base {base_version}",
            file=sys.stderr,
        )
        return 1

    if base_version and compare_semver(current, base_version) > 0:
        if not changelog_has_version(current):
            print(
                f"CHANGELOG.md missing ## [{current}] section for version bump",
                file=sys.stderr,
            )
            return 1

    print(f"OK: {VERSION_REL}={current}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
