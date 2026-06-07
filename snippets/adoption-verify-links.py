#!/usr/bin/env python3
"""Verify markdown links after cursor-dev-workflows adoption (LSI layout)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"\]\(([^)#]+)")
DOCS_WORKFLOWS_IN_CANONICAL = re.compile(r"\]\(docs/workflows/")
OVERLAYS_LSI_IN_CANONICAL = re.compile(r"\]\(overlays/lsi/")
AGENT_STACK_IN_CANONICAL = re.compile(r"\]\(agent-stack/")

LSI_ENTRYPOINTS = ("AGENTS.md", "README.md")


def extract_links(text: str) -> list[str]:
    links: list[str] = []
    for match in LINK_RE.finditer(text):
        href = match.group(1)
        if href.startswith(("http://", "https://", "mailto:")):
            continue
        links.append(href)
    return links


def check_resolve(repo_root: Path, md: Path, href: str) -> str | None:
    path_part = href.split("#")[0]
    if not path_part:
        return None

    target = (md.parent / path_part).resolve()
    try:
        target.relative_to(repo_root)
    except ValueError:
        rel = md.relative_to(repo_root)
        return f"{rel}: ({href}) resolves outside repo root"

    if not target.exists():
        rel = md.relative_to(repo_root)
        return f"{rel}: ({href})"
    return None


def check_patterns(repo_root: Path, md: Path, text: str, canonical: Path) -> list[str]:
    rel = md.relative_to(repo_root)
    violations: list[str] = []

    try:
        md.relative_to(canonical)
        inside_canonical = True
    except ValueError:
        inside_canonical = False

    if inside_canonical and DOCS_WORKFLOWS_IN_CANONICAL.search(text):
        violations.append(
            f"{rel}: doubled prefix ](docs/workflows/ inside CANONICAL_DOCS_PATH"
        )

    if inside_canonical and OVERLAYS_LSI_IN_CANONICAL.search(text):
        violations.append(
            f"{rel}: maintainer path ](overlays/lsi/ inside CANONICAL_DOCS_PATH"
        )

    if inside_canonical and AGENT_STACK_IN_CANONICAL.search(text):
        violations.append(
            f"{rel}: maintainer path ](agent-stack/ inside CANONICAL_DOCS_PATH"
        )

    return violations


def process_file(
    repo_root: Path,
    md: Path,
    text: str,
    canonical: Path,
) -> tuple[list[str], list[str]]:
    broken: list[str] = []
    for href in extract_links(text):
        err = check_resolve(repo_root, md, href)
        if err:
            broken.append(err)
    patterns = check_patterns(repo_root, md, text, canonical)
    return broken, patterns


def collect_scan_files(
    repo_root: Path,
    canonical: Path,
    extra_dirs: list[Path],
) -> list[Path]:
    files: list[Path] = []
    seen: set[Path] = set()

    def add(path: Path) -> None:
        resolved = path.resolve()
        if resolved not in seen and path.is_file() and path.suffix == ".md":
            seen.add(resolved)
            files.append(path)

    scan_dirs: list[Path] = [canonical]
    for name in LSI_ENTRYPOINTS:
        add(repo_root / name)

    for extra in extra_dirs:
        extra_path = (repo_root / extra).resolve()
        if extra_path.is_dir():
            scan_dirs.append(extra_path)

    for directory in scan_dirs:
        if directory.is_dir():
            for md in sorted(directory.rglob("*.md")):
                add(md)

    return sorted(files, key=lambda p: str(p.relative_to(repo_root)))


def verify(
    repo_root: Path,
    canonical: Path,
    extra_dirs: list[Path] | None = None,
) -> tuple[list[str], list[str], list[str]]:
    broken: list[str] = []
    patterns: list[str] = []
    warnings: list[str] = []

    if not canonical.is_dir():
        rel = canonical.relative_to(repo_root)
        return [f"Missing CANONICAL_DOCS_PATH: {rel}"], [], warnings

    router = canonical / "which-workflow.md"
    if not router.is_file():
        warnings.append(
            f"which-workflow.md not found under {canonical.relative_to(repo_root)}"
        )

    scan_files = collect_scan_files(repo_root, canonical, extra_dirs or [])

    for md in scan_files:
        text = md.read_text(encoding="utf-8")
        file_broken, file_patterns = process_file(repo_root, md, text, canonical)
        broken.extend(file_broken)
        patterns.extend(file_patterns)

    return broken, patterns, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify adoption markdown links (LSI layout)."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="Application repo root (default: current directory)",
    )
    parser.add_argument(
        "--canonical",
        type=Path,
        default=Path(".lsi/workflows"),
        help="CANONICAL_DOCS_PATH relative to repo root",
    )
    parser.add_argument(
        "--extra-dirs",
        type=Path,
        action="append",
        default=[],
        help="Additional directories to scan (repeatable)",
    )
    args = parser.parse_args(argv)

    repo_root = args.repo_root.resolve()
    canonical = (repo_root / args.canonical).resolve()

    broken, patterns, warnings = verify(repo_root, canonical, args.extra_dirs)

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)

    if patterns:
        print("PATTERN VIOLATIONS:", file=sys.stderr)
        print("\n".join(patterns), file=sys.stderr)

    if broken:
        print("BROKEN LINKS:", file=sys.stderr)
        print("\n".join(broken), file=sys.stderr)

    if patterns or broken:
        return 1

    scope = str(canonical.relative_to(repo_root))
    print(f"OK: links resolve under {scope} (LSI layout)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
