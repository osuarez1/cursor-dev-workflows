#!/usr/bin/env python3
"""Infer next version from conventional commits since last tag."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from semver import infer_next_version, parse_semver

ROOT = Path(__file__).resolve().parents[2]
VERSION_FILE = ROOT / "version.txt"


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
    try:
        tags = run_git("tag", "--list", "v*.*.*", "--sort=-v:refname")
    except subprocess.CalledProcessError:
        return None
    for line in tags.splitlines():
        tag = line.strip()
        if tag.startswith("v") and parse_semver(tag[1:]):
            return tag
    return None


def commit_subjects_since(since_ref: str | None) -> list[str]:
    args = ["log", "--pretty=%s"]
    if since_ref:
        args.append(f"{since_ref}..HEAD")
    else:
        args.append("HEAD")
    try:
        out = run_git(*args)
    except subprocess.CalledProcessError:
        return []
    return [line for line in out.splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    current = VERSION_FILE.read_text(encoding="utf-8").strip()
    last_tag = last_version_tag()
    since_ref = last_tag if last_tag else None
    subjects = commit_subjects_since(since_ref)
    result = infer_next_version(current, subjects)
    output = {
        **result,
        "lastTag": last_tag,
        "sinceRef": since_ref or "(first release — all commits)",
        "commitCount": len(subjects),
    }

    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print(f"Current:  {output['current']}")
        print(f"Proposed: {output['next']} ({output['bump']})")
        print(f"Reason:   {output['reason']}")
        print(f"Since:    {output['sinceRef']}")
        print(
            f"Signals:  breaking={output['signals']['breaking']} "
            f"feat={output['signals']['feat']} fix={output['signals']['fix']}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
