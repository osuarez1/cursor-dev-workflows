#!/usr/bin/env python3
"""Fail when workflow spec sources contain forbidden maintainer-path markdown links.

Phase 1: ](overlays/lsi/
Phase 2: ](agent-stack/ (enable after overlay workflow sources are clean)

Manual pre-PR / pre-VERSION gate until bundle CI lands (task 4.6).
"""

from __future__ import annotations

import sys
from pathlib import Path

BUNDLE_ROOT = Path(__file__).resolve().parents[1]

SCAN_DIRS = (
    BUNDLE_ROOT / "docs" / "workflows",
    BUNDLE_ROOT / "overlays" / "lsi" / "docs" / "workflows",
)

PHASE_1 = "](overlays/lsi/"
PHASE_2 = "](agent-stack/"

# Set True once task 2.4 overlay router links are clean (lsi-help → .cursor/commands).
ENABLE_PHASE_2 = True


def scan_file(path: Path, patterns: tuple[str, ...]) -> list[str]:
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(BUNDLE_ROOT)
    hits: list[str] = []
    for pattern in patterns:
        if pattern in text:
            hits.append(f"{rel}: forbidden markdown link substring {pattern!r}")
    return hits


def main() -> int:
    patterns: list[str] = [PHASE_1]
    if ENABLE_PHASE_2:
        patterns.append(PHASE_2)

    violations: list[str] = []
    for directory in SCAN_DIRS:
        if not directory.is_dir():
            continue
        for md in sorted(directory.rglob("*.md")):
            violations.extend(scan_file(md, tuple(patterns)))

    if violations:
        print("FORBIDDEN WORKFLOW LINK SOURCES:", file=sys.stderr)
        for item in violations:
            print(f"  {item}", file=sys.stderr)
        return 1

    print(f"OK: no forbidden link sources in {len(SCAN_DIRS)} workflow trees")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
