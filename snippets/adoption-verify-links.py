#!/usr/bin/env python3
"""Verify markdown links after cursor-dev-workflows adoption.

Run from the application repo root. See docs/adoption-layout.md.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"\]\(([^)#]+)")
DOCS_WORKFLOWS_IN_CANONICAL = re.compile(r"\]\(docs/workflows/")
PARENT_DOCS_WORKFLOWS = re.compile(r"\]\(\.\./docs/workflows/")


def collect_links(md: Path) -> list[tuple[Path, str]]:
    links: list[tuple[Path, str]] = []
    for match in LINK_RE.finditer(md.read_text()):
        href = match.group(1)
        if href.startswith(("http://", "https://", "mailto:")):
            continue
        links.append((md, href))
    return links


def check_resolve(root: Path, md: Path, href: str) -> str | None:
    target = (md.parent / href.split("#")[0]).resolve()
    if not target.exists():
        return f"{md.relative_to(root)}: ({href})"
    return None


def check_patterns(
    root: Path,
    md: Path,
    profile: str,
    canonical: Path,
) -> list[str]:
    text = md.read_text()
    rel = md.relative_to(root)
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


def verify(
    repo_root: Path,
    canonical: Path,
    profile: str,
    check_support: bool,
) -> tuple[list[str], list[str]]:
    broken: list[str] = []
    patterns: list[str] = []

    if not canonical.is_dir():
        return [f"Missing CANONICAL_DOCS_PATH: {canonical.relative_to(repo_root)}"], []

    scan_dirs: list[Path] = [canonical]
    if check_support and profile == "A":
        for name in ("templates", "examples"):
            path = repo_root / name
            if path.is_dir():
                scan_dirs.append(path)

    for directory in scan_dirs:
        for md in sorted(directory.rglob("*.md")):
            for _, href in collect_links(md):
                err = check_resolve(repo_root, md, href)
                if err:
                    broken.append(err)
            patterns.extend(check_patterns(repo_root, md, profile, canonical))

    return broken, patterns


def main() -> int:
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
        help="Skip templates/ and examples/ (Profile A checks them by default)",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    canonical = (repo_root / args.canonical).resolve()
    check_support = not args.no_support_dirs

    broken, patterns = verify(repo_root, canonical, args.profile, check_support)

    if patterns:
        print("PATTERN VIOLATIONS:", file=sys.stderr)
        print("\n".join(patterns), file=sys.stderr)

    if broken:
        print("BROKEN LINKS:", file=sys.stderr)
        print("\n".join(broken), file=sys.stderr)

    if patterns or broken:
        return 1

    scope = [str(args.canonical)]
    if check_support and args.profile == "A":
        scope.extend(["templates/", "examples/"])
    print(f"OK: links resolve under {', '.join(scope)} (Profile {args.profile})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
