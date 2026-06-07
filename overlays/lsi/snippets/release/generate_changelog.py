#!/usr/bin/env python3
"""Update CHANGELOG.md since last tag or maintain [Unreleased]."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHANGELOG = ROOT / "CHANGELOG.md"


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def last_version_tag() -> str | None:
    tags = run_git("tag", "--list", "v*.*.*", "--sort=-v:refname")
    for line in tags.splitlines():
        tag = line.strip()
        if re.match(r"^v\d+\.\d+\.\d+$", tag):
            return tag
    return None


def commits_since(since_ref: str | None) -> list[str]:
    args = ["log", "--pretty=- %s"]
    if since_ref:
        args.append(f"{since_ref}..HEAD")
    else:
        args.append("-5")
    out = run_git(*args)
    return [line.strip() for line in out.splitlines() if line.strip()]


def append_unreleased(lines: list[str]) -> None:
    text = CHANGELOG.read_text(encoding="utf-8")
    block = "\n".join(["", "### Added", *lines, ""])
    if "## [Unreleased]" in text:
        text = text.replace("## [Unreleased]", f"## [Unreleased]{block}", 1)
    else:
        text = f"# Changelog\n\n## [Unreleased]{block}\n{text}"
    CHANGELOG.write_text(text, encoding="utf-8")


def finalize_release(version: str) -> None:
    text = CHANGELOG.read_text(encoding="utf-8")
    today = date.today().isoformat()
    entry = f"## [{version}] - {today}\n"
    if "## [Unreleased]" not in text:
        raise SystemExit("No [Unreleased] section in CHANGELOG.md")
    unreleased_match = re.search(
        r"## \[Unreleased\]\n(?P<body>.*?)(?=\n## \[|\Z)",
        text,
        re.DOTALL,
    )
    body = unreleased_match.group("body").strip() if unreleased_match else ""
    if not body:
        body = "### Changed\n\n- Release v{0}\n".format(version)
    text = re.sub(r"## \[Unreleased\]\n.*?(?=\n## \[|\Z)", "", text, count=1, flags=re.DOTALL)
    insert_at = text.find("\n## [")
    new_section = f"{entry}\n{body}\n\n"
    if insert_at == -1:
        text = text.rstrip() + "\n\n" + new_section
    else:
        text = text[:insert_at] + "\n" + new_section + text[insert_at:].lstrip("\n")
    CHANGELOG.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("unreleased", "since-tag", "finalize"), required=True)
    parser.add_argument("--finalize", metavar="VERSION")
    args = parser.parse_args()

    if args.mode == "finalize":
        if not args.finalize:
            print("--finalize VERSION required", file=sys.stderr)
            return 1
        finalize_release(args.finalize)
        print(f"Finalized CHANGELOG for {args.finalize}")
        return 0

    last_tag = last_version_tag()
    lines = commits_since(last_tag)
    if not lines:
        lines = ["- (no conventional commits since last tag)"]
    append_unreleased(lines)
    print(f"Updated [Unreleased] with {len(lines)} commit line(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
