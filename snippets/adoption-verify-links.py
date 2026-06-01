#!/usr/bin/env python3
"""Verify markdown links after cursor-dev-workflows adoption.

Run from the application repo root. Operator guide: docs/adoption-layout.md.
Design reference: docs/adoption-verify-architecture.md.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"\]\(([^)#]+)")
DOCS_WORKFLOWS_IN_CANONICAL = re.compile(r"\]\(docs/workflows/")
PARENT_DOCS_WORKFLOWS = re.compile(r"\]\(\.\./docs/workflows/")

PROFILE_A_ENTRYPOINTS = ("which-workflow.md", "AGENTS.md", "README.md")


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


def check_patterns(
    repo_root: Path,
    md: Path,
    text: str,
    profile: str,
    canonical: Path,
) -> list[str]:
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

    if profile == "B" and inside_canonical and PARENT_DOCS_WORKFLOWS.search(text):
        violations.append(
            f"{rel}: ](../docs/workflows/ not allowed under CANONICAL_DOCS_PATH (Profile B)"
        )

    return violations


def process_file(
    repo_root: Path,
    md: Path,
    text: str,
    profile: str,
    canonical: Path,
) -> tuple[list[str], list[str]]:
    broken: list[str] = []
    for href in extract_links(text):
        err = check_resolve(repo_root, md, href)
        if err:
            broken.append(err)
    patterns = check_patterns(repo_root, md, text, profile, canonical)
    return broken, patterns


def collect_scan_files(
    repo_root: Path,
    canonical: Path,
    profile: str,
    check_support: bool,
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
    if check_support and profile == "A":
        for name in ("templates", "examples"):
            path = repo_root / name
            if path.is_dir():
                scan_dirs.append(path)

    for extra in extra_dirs:
        extra_path = (repo_root / extra).resolve()
        if extra_path.is_dir():
            scan_dirs.append(extra_path)

    for directory in scan_dirs:
        if directory.is_dir():
            for md in sorted(directory.rglob("*.md")):
                add(md)

    if profile == "A":
        for name in PROFILE_A_ENTRYPOINTS:
            add(repo_root / name)

    return sorted(files, key=lambda p: str(p.relative_to(repo_root)))


def verify(
    repo_root: Path,
    canonical: Path,
    profile: str,
    check_support: bool,
    extra_dirs: list[Path] | None = None,
) -> tuple[list[str], list[str], list[str]]:
    broken: list[str] = []
    patterns: list[str] = []
    warnings: list[str] = []

    if not canonical.is_dir():
        rel = canonical.relative_to(repo_root)
        return [f"Missing CANONICAL_DOCS_PATH: {rel}"], [], warnings

    if profile == "A" and not (repo_root / "which-workflow.md").is_file():
        warnings.append(
            "Profile A: which-workflow.md not found at repo root (router not verified)"
        )

    scan_files = collect_scan_files(
        repo_root, canonical, profile, check_support, extra_dirs or []
    )

    for md in scan_files:
        text = md.read_text()
        file_broken, file_patterns = process_file(
            repo_root, md, text, profile, canonical
        )
        broken.extend(file_broken)
        patterns.extend(file_patterns)

    return broken, patterns, warnings


def build_scope_message(
    canonical: Path,
    profile: str,
    check_support: bool,
    extra_dirs: list[Path],
    repo_root: Path,
) -> str:
    scope = [str(canonical.relative_to(repo_root))]
    if profile == "A":
        for name in PROFILE_A_ENTRYPOINTS:
            if (repo_root / name).is_file():
                scope.append(name)
        if check_support:
            for name in ("templates/", "examples/"):
                if (repo_root / name.rstrip("/")).is_dir():
                    scope.append(name)
    scope.extend(str(p) for p in extra_dirs)
    return ", ".join(scope)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify adoption markdown links (cursor-dev-workflows)."
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
        default=Path("docs/workflows"),
        help="CANONICAL_DOCS_PATH relative to repo root (default: docs/workflows)",
    )
    parser.add_argument(
        "--profile",
        choices=("A", "B"),
        default="A",
        help="Adoption profile (default: A)",
    )
    parser.add_argument(
        "--no-support-dirs",
        action="store_true",
        help="Profile A only: skip root templates/ and examples/",
    )
    parser.add_argument(
        "--extra-dirs",
        type=Path,
        action="append",
        default=[],
        help="Additional directories to scan (repeatable; relative to repo root)",
    )
    args = parser.parse_args(argv)

    repo_root = args.repo_root.resolve()
    canonical = (repo_root / args.canonical).resolve()
    check_support = not args.no_support_dirs
    extra_dirs = args.extra_dirs

    broken, patterns, warnings = verify(
        repo_root, canonical, args.profile, check_support, extra_dirs
    )

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

    scope = build_scope_message(
        canonical, args.profile, check_support, extra_dirs, repo_root
    )
    print(f"OK: links resolve under {scope} (Profile {args.profile})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
