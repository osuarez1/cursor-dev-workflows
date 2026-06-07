#!/usr/bin/env python3
"""Agentic parity checklist for LSI adopters (post-adopt smoke)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

BUNDLE_ROOT = Path(__file__).resolve().parents[1]
AUDIT = BUNDLE_ROOT / "snippets" / "audit-agent-docs.py"
VERIFY = BUNDLE_ROOT / "snippets" / "adoption-verify-links.py"

LSI_COMMANDS = [
    "lsi-help",
    "lsi-card",
    "lsi-card-link",
    "lsi-trello-list",
    "lsi-trello-branch",
    "lsi-branch",
    "lsi-senior",
    "lsi-commit",
    "lsi-readiness",
    "lsi-review",
    "lsi-pr",
    "lsi-promote",
    "lsi-merge-desc",
    "lsi-close",
    "lsi-version",
    "lsi-changelog",
    "lsi-release",
    "lsi-bootstrap-release",
    "lsi-update",
]
ALWAYS_ON_RULES = (
    "branch-workflow.mdc",
    "commit-pr-conventions.mdc",
    "openspec-git-integration.mdc",
)


def check(repo: Path) -> list[str]:
    errors: list[str] = []
    lsi = repo / ".lsi" / "workflows"
    if not lsi.is_dir():
        errors.append("missing .lsi/workflows/")
    router = lsi / "which-workflow.md"
    if not router.is_file():
        errors.append("missing .lsi/workflows/which-workflow.md")

    for name in ALWAYS_ON_RULES:
        if not (repo / ".cursor" / "rules" / name).is_file():
            errors.append(f"missing .cursor/rules/{name}")

    cmds = repo / ".cursor" / "commands"
    for name in LSI_COMMANDS:
        if not (cmds / f"{name}.md").is_file():
            errors.append(f"missing .cursor/commands/{name}.md")

    agents = repo / "AGENTS.md"
    claude = repo / "CLAUDE.md"
    if not agents.is_file():
        errors.append("missing AGENTS.md")
    elif claude.exists() and not claude.is_symlink():
        errors.append("CLAUDE.md is not a symlink")
    elif claude.is_symlink() and claude.resolve() != agents.resolve():
        errors.append("CLAUDE.md does not symlink to AGENTS.md")

    if not (repo / "PROJECT.md").is_file():
        errors.append("missing PROJECT.md")
    elif "CANONICAL_DOCS_PATH" not in (repo / "PROJECT.md").read_text():
        errors.append("PROJECT.md missing CANONICAL_DOCS_PATH")

    if not (repo / "scripts" / "check_version.py").is_file():
        errors.append("missing scripts/check_version.py")

    return errors


def run_script(script: Path, *args: str) -> int:
    return subprocess.run([sys.executable, str(script), *args], cwd=BUNDLE_ROOT).returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify LSI adopter parity.")
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--skip-external", action="store_true")
    args = parser.parse_args(argv)

    repo = args.repo_root.resolve()
    name = repo.name
    print(f"=== {name} ===")

    errors = check(repo)
    if errors:
        print("PARITY FAILURES:")
        for e in errors:
            print(f"  - {e}")
    else:
        print("PARITY: OK")

    if args.skip_external:
        return 1 if errors else 0

    link_code = run_script(
        VERIFY, "--repo-root", str(repo), "--canonical", ".lsi/workflows"
    )
    audit_code = run_script(
        AUDIT, "--repo-root", str(repo), "--fail-on", "error"
    )

    failed = errors or link_code != 0 or audit_code != 0
    print(f"RESULT: {'FAIL' if failed else 'PASS'}\n")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
