#!/usr/bin/env python3
"""Agentic parity checklist for LSI adopters (post-adopt smoke)."""

from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

BUNDLE_ROOT = Path(__file__).resolve().parents[1]
AUDIT = BUNDLE_ROOT / "snippets" / "audit-agent-docs.py"
VERIFY = BUNDLE_ROOT / "snippets" / "adoption-verify-links.py"
ADOPT = BUNDLE_ROOT / "snippets" / "adopt.py"

# Import expected agent stack from single source of truth.
_eas_spec = importlib.util.spec_from_file_location(
    "expected_agent_stack",
    BUNDLE_ROOT / "snippets" / "expected_agent_stack.py",
)
_eas = importlib.util.module_from_spec(_eas_spec)  # type: ignore[arg-type]
_eas_spec.loader.exec_module(_eas)  # type: ignore[union-attr]


def _read_repo_name(repo: Path) -> str | None:
    project = repo / "PROJECT.md"
    if not project.is_file():
        return None
    m = re.search(r"`REPO_NAME`\s*\|\s*`([^`]+)`", project.read_text(encoding="utf-8"))
    return m.group(1).strip() if m else None


def _find_patch_for_repo(repo_name: str) -> Path | None:
    patches = BUNDLE_ROOT / "patches"
    if not patches.is_dir():
        return None
    for yaml_path in sorted(patches.glob("*.yaml")):
        if yaml_path.name.startswith("_"):
            continue
        text = yaml_path.read_text(encoding="utf-8")
        if re.search(rf"^repo:\s*{re.escape(repo_name)}\s*$", text, re.MULTILINE):
            return yaml_path
        if re.search(rf"REPO_NAME:\s*{re.escape(repo_name)}\b", text):
            return yaml_path
    return None


def resolve_preserve_globs(repo: Path) -> list[str]:
    """Resolve adopter `preserve` globs from its registered patch.

    Maps the adopter's PROJECT.md REPO_NAME to patches/<repo>.yaml so the parity
    audit does not flag preserved adopter-owned files as surplus. Defaults to []
    for unregistered adopters.
    """
    repo_name = _read_repo_name(repo)
    if not repo_name:
        return []
    patch = _find_patch_for_repo(repo_name)
    if not patch:
        return []
    spec = importlib.util.spec_from_file_location("adopt_verify", ADOPT)
    if spec is None or spec.loader is None:
        return []
    adopt = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(adopt)  # type: ignore[union-attr]
        data = adopt._load_yaml_text(patch.read_text(encoding="utf-8"))
    except Exception:
        return []
    if not isinstance(data, dict):
        return []
    return list(data.get("preserve") or [])


def check(repo: Path) -> list[str]:
    errors: list[str] = []
    lsi = repo / ".lsi" / "workflows"
    if not lsi.is_dir():
        errors.append("missing .lsi/workflows/")
    router = lsi / "which-workflow.md"
    if not router.is_file():
        errors.append("missing .lsi/workflows/which-workflow.md")

    for name in _eas.ALWAYS_ON_RULES:
        if not (repo / ".cursor" / "rules" / name).is_file():
            errors.append(f"missing .cursor/rules/{name}")

    cmds = repo / ".cursor" / "commands"
    for name in _eas.LSI_COMMANDS:
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

    audit_args = ["--repo-root", str(repo), "--check-parity", "--fail-on", "error"]
    for glob in resolve_preserve_globs(repo):
        audit_args.extend(["--preserve", glob])
    audit_code = run_script(AUDIT, *audit_args)

    failed = errors or link_code != 0 or audit_code != 0
    print(f"RESULT: {'FAIL' if failed else 'PASS'}\n")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
