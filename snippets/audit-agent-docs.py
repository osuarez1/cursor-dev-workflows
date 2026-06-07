#!/usr/bin/env python3
"""Scan agent/IDE entry points for contradictions before adopt.

v1: regex/token checks — PR target, PROTECTED_BRANCHES, symlink, stale paths, commands.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None  # type: ignore

POLICY_DEFAULT_CHOICES: dict[str, str] = {
    "pr_target": "staging_first",
    "claude_symlink": "symlink_to_agents",
    "openspec_archive_timing": "lsi_close_on_main",
}

SEVERITY_ERROR = "error"
SEVERITY_WARN = "warn"
SEVERITY_INFO = "info"

PR_TO_MAIN = re.compile(
    r"PR\s+(?:to|target(?:ing)?)\s+[`']?main[`']?",
    re.IGNORECASE,
)
STALE_DOCS_WORKFLOWS = re.compile(r"docs/workflows/[a-z0-9_-]+\.md", re.IGNORECASE)
OPSX_ARCHIVE_AFTER_MERGE = re.compile(
    r"/opsx:archive.*(?:after|on)\s+merge",
    re.IGNORECASE,
)
PROTECTED_TOKEN = re.compile(r"PROTECTED_BRANCHES\s*[=:]\s*([^\n]+)", re.IGNORECASE)
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
OPSX_COMMANDS = [
    "opsx-explore",
    "opsx-propose",
    "opsx-apply",
    "opsx-sync",
    "opsx-archive",
]


@dataclass
class Finding:
    severity: str
    category: str
    message: str
    location: str = ""
    suggestion: str = ""


def read_lines(path: Path) -> list[str]:
    if not path.is_file():
        return []
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def project_tokens(repo_root: Path) -> dict[str, str]:
    project = repo_root / "PROJECT.md"
    tokens: dict[str, str] = {}
    for line in read_lines(project):
        m = re.match(r"\|\s*`([A-Z_]+)`\s*\|\s*`?([^`|]+)`?", line)
        if m:
            tokens[m.group(1)] = m.group(2).strip().rstrip("`").strip()
        m2 = re.match(r"^([A-Z_]+)\s*=\s*(.+)$", line.strip())
        if m2:
            tokens[m2.group(1)] = m2.group(2).strip()
    return tokens


def scan_file(
    repo_root: Path,
    path: Path,
    tokens: dict[str, str],
) -> list[Finding]:
    findings: list[Finding] = []
    if not path.is_file():
        return findings
    rel = str(path.relative_to(repo_root))
    lines = read_lines(path)
    pr_target = tokens.get("PR_TARGET_BRANCH", "staging")

    for i, line in enumerate(lines, start=1):
        loc = f"{rel}:{i}"
        if PR_TO_MAIN.search(line) and pr_target == "staging":
            if "promote" not in line.lower() and "promotion" not in line.lower():
                findings.append(
                    Finding(
                        SEVERITY_ERROR,
                        "pr_target",
                        line.strip()[:120],
                        loc,
                        "Align with staging-first: feature PRs target staging",
                    )
                )
        if STALE_DOCS_WORKFLOWS.search(line) and ".lsi/workflows" not in line:
            findings.append(
                Finding(
                    SEVERITY_INFO,
                    "stale_path",
                    line.strip()[:120],
                    loc,
                    "Rewrite to .lsi/workflows/...",
                )
            )
        if OPSX_ARCHIVE_AFTER_MERGE.search(line):
            findings.append(
                Finding(
                    SEVERITY_ERROR,
                    "openspec_archive_timing",
                    line.strip()[:120],
                    loc,
                    "Use /lsi:close on main after promotion",
                )
            )

    return findings


def check_symlink(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    agents = repo_root / "AGENTS.md"
    claude = repo_root / "CLAUDE.md"
    if not agents.is_file():
        findings.append(
            Finding(SEVERITY_WARN, "entry_point", "AGENTS.md missing", "AGENTS.md")
        )
        return findings
    if not claude.exists():
        findings.append(
            Finding(
                SEVERITY_ERROR,
                "claude_symlink",
                "CLAUDE.md missing — should symlink to AGENTS.md",
                "CLAUDE.md",
            )
        )
    elif not claude.is_symlink():
        findings.append(
            Finding(
                SEVERITY_ERROR,
                "claude_symlink",
                "CLAUDE.md is a regular file, not symlink to AGENTS.md",
                "CLAUDE.md",
            )
        )
    elif claude.resolve() != agents.resolve():
        findings.append(
            Finding(
                SEVERITY_ERROR,
                "claude_symlink",
                f"CLAUDE.md -> {claude.readlink()} (expected AGENTS.md)",
                "CLAUDE.md",
            )
        )
    return findings


def check_protected_branches(repo_root: Path, tokens: dict[str, str]) -> list[Finding]:
    findings: list[Finding] = []
    expected = tokens.get("PROTECTED_BRANCHES", "")
    if not expected:
        return findings
    expected_set = {b.strip() for b in expected.split(",") if b.strip()}

    for rel in (
        "PROJECT.md",
        ".cursor/rules/branch-workflow.mdc",
        ".lsi/workflows/branch-workflow.md",
    ):
        path = repo_root / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for branch in expected_set:
            if branch not in text:
                findings.append(
                    Finding(
                        SEVERITY_ERROR,
                        "protected_branches",
                        f"Missing branch `{branch}` in {rel}",
                        rel,
                    )
                )
    return findings


def check_commands(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    cmd_dir = repo_root / ".cursor" / "commands"
    if not cmd_dir.is_dir():
        return [
            Finding(
                SEVERITY_WARN,
                "command_drift",
                ".cursor/commands/ missing",
                str(cmd_dir),
            )
        ]
    present = {p.stem for p in cmd_dir.glob("*.md")}
    for name in LSI_COMMANDS + OPSX_COMMANDS:
        if name not in present:
            findings.append(
                Finding(
                    SEVERITY_WARN,
                    "command_drift",
                    f"Missing command file {name}.md",
                    f".cursor/commands/{name}.md",
                )
            )
    return findings


def default_scan_paths(repo_root: Path) -> list[Path]:
    paths: list[Path] = []
    for rel in (
        "AGENTS.md",
        "CLAUDE.md",
        "PROJECT.md",
        "CONVENTION.md",
        ".cursorrules",
        "README.md",
        "README.development.md",
        "CONTRIBUTING.md",
    ):
        p = repo_root / rel
        if p.is_file():
            paths.append(p)
    for pattern in (
        ".cursor/rules/*.mdc",
        ".cursor/commands/*.md",
        "docs/agents/**/*.md",
        "docs/workflows/*.md",
        ".lsi/workflows/**/*.md",
    ):
        paths.extend(repo_root.glob(pattern))
    return sorted(set(paths))


def load_resolutions(path: Path | None) -> dict[str, str]:
    """Return accepted finding categories (resolution id -> choice)."""
    if path is None or not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    entries: list[object]
    if yaml is not None:
        data = yaml.safe_load(text)
        entries = data if isinstance(data, list) else []
    else:
        entries = []
        current: dict[str, str] | None = None
        for raw in text.splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("- id:"):
                if current:
                    entries.append(current)
                current = {"id": line.split(":", 1)[1].strip()}
            elif current is not None and ":" in line:
                key, value = line.split(":", 1)
                current[key.strip()] = value.strip().strip("'\"")
        if current:
            entries.append(current)

    accepted: dict[str, str] = {}
    for entry in entries:
        if isinstance(entry, dict) and entry.get("id"):
            accepted[str(entry["id"])] = str(entry.get("choice", "accepted"))
    return accepted


def apply_resolutions(
    findings: list[Finding],
    *,
    accepted: dict[str, str],
    policy_defaults: bool = False,
) -> tuple[list[Finding], list[Finding]]:
    """Split findings into unresolved and accepted (suppressed) lists."""
    effective = dict(accepted)
    if policy_defaults:
        effective.update(POLICY_DEFAULT_CHOICES)

    unresolved: list[Finding] = []
    suppressed: list[Finding] = []
    for finding in findings:
        if finding.category in effective:
            suppressed.append(finding)
        else:
            unresolved.append(finding)
    return unresolved, suppressed


def audit(repo_root: Path, extra_paths: list[Path] | None = None) -> list[Finding]:
    repo_root = repo_root.resolve()
    tokens = project_tokens(repo_root)
    findings: list[Finding] = []
    findings.extend(check_symlink(repo_root))
    findings.extend(check_protected_branches(repo_root, tokens))
    findings.extend(check_commands(repo_root))

    scan = default_scan_paths(repo_root)
    if extra_paths:
        scan.extend(extra_paths)
    for path in sorted(set(scan)):
        if path.is_file():
            findings.extend(scan_file(repo_root, path, tokens))
    return findings


def format_report(
    findings: list[Finding],
    *,
    accepted: list[Finding] | None = None,
) -> str:
    if not findings and not accepted:
        return "OK: no findings"
    lines: list[str] = []
    by_cat: dict[str, list[Finding]] = {}
    for f in findings:
        by_cat.setdefault(f.category, []).append(f)
    for cat, items in sorted(by_cat.items()):
        lines.append(f"[{items[0].severity.upper()}] {cat}")
        for f in items:
            if f.location:
                lines.append(f"  {f.location}: {f.message}")
            else:
                lines.append(f"  {f.message}")
            if f.suggestion:
                lines.append(f"    → {f.suggestion}")
    if accepted:
        lines.append("[ACCEPTED]")
        for f in accepted:
            loc = f" {f.location}" if f.location else ""
            lines.append(f"  {f.category}:{loc} {f.message[:80]}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit agent docs for contradictions.")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument(
        "--fail-on",
        choices=("error", "warn", "info"),
        default="error",
        help="Exit 1 when findings at or above this severity (default: error)",
    )
    parser.add_argument(
        "--accept-resolutions",
        type=Path,
        default=None,
        help="YAML file of accepted contradiction resolutions (category id -> choice)",
    )
    parser.add_argument(
        "--accept-policy-defaults",
        action="store_true",
        help="Accept confirmed LSI policy resolutions (staging-first, symlink, /lsi:close)",
    )
    parser.add_argument("--report-file", type=Path, default=None)
    args = parser.parse_args(argv)

    raw_findings = audit(args.repo_root.resolve())
    accepted_map = load_resolutions(
        args.accept_resolutions.resolve() if args.accept_resolutions else None
    )
    findings, suppressed = apply_resolutions(
        raw_findings,
        accepted=accepted_map,
        policy_defaults=args.accept_policy_defaults,
    )
    report = format_report(findings, accepted=suppressed or None)
    print(report)

    if args.report_file:
        args.report_file.parent.mkdir(parents=True, exist_ok=True)
        args.report_file.write_text(report + "\n", encoding="utf-8")

    order = {SEVERITY_INFO: 0, SEVERITY_WARN: 1, SEVERITY_ERROR: 2}
    threshold = order[args.fail_on]
    if any(order.get(f.severity, 0) >= threshold for f in findings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
