"""SemVer helpers for release scripts (pre-1.0 and 1.x)."""

from __future__ import annotations

import re
from dataclasses import dataclass

CONVENTIONAL = re.compile(
    r"^(?P<type>[a-z]+)(?P<breaking>!)?(?:\((?P<scope>[^)]+)\))?!?:\s*(?P<subject>.+)$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Semver:
    major: int
    minor: int
    patch: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


def parse_semver(version: str) -> Semver | None:
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)(?:-.+)?$", version.strip())
    if not match:
        return None
    return Semver(int(match[1]), int(match[2]), int(match[3]))


def classify_commit(subject: str) -> str:
    trimmed = subject.strip()
    if not trimmed:
        return "none"
    if re.search(r"BREAKING CHANGE:", trimmed, re.IGNORECASE):
        return "breaking"
    match = CONVENTIONAL.match(trimmed)
    if not match:
        return "none"
    commit_type = match.group("type").lower()
    if match.group("breaking"):
        return "breaking"
    if commit_type == "feat":
        return "feat"
    if commit_type == "fix":
        return "fix"
    return "none"


def infer_bump_from_commits(subjects: list[str], major: int = 0) -> str:
    has_breaking = has_feat = has_fix = False
    for subject in subjects:
        kind = classify_commit(subject)
        if kind == "breaking":
            has_breaking = True
        elif kind == "feat":
            has_feat = True
        elif kind == "fix":
            has_fix = True
    if major >= 1 and has_breaking:
        return "major"
    if has_breaking or has_feat:
        return "minor"
    if has_fix:
        return "patch"
    return "none"


def bump_version(current: str, bump: str) -> tuple[str, str, str]:
    parts = parse_semver(current)
    if parts is None:
        raise ValueError(f"Invalid semver: {current}")
    if bump == "none":
        return str(parts), "none", "No user-facing conventional commits since last tag"
    if parts.major == 0:
        if bump == "minor":
            return (
                str(Semver(parts.major, parts.minor + 1, 0)),
                "minor",
                "Pre-1.0 minor bump (feat or breaking change)",
            )
        if bump == "patch":
            return (
                str(Semver(parts.major, parts.minor, parts.patch + 1)),
                "patch",
                "Pre-1.0 patch bump (fix)",
            )
    if bump == "major":
        return (
            str(Semver(parts.major + 1, 0, 0)),
            "major",
            "Major bump (breaking change at 1.x+)",
        )
    if bump == "minor":
        return (
            str(Semver(parts.major, parts.minor + 1, 0)),
            "minor",
            "Minor bump (feat)",
        )
    return (
        str(Semver(parts.major, parts.minor, parts.patch + 1)),
        "patch",
        "Patch bump (fix)",
    )


def infer_next_version(current: str, subjects: list[str]) -> dict:
    parts = parse_semver(current)
    if parts is None:
        raise ValueError(f"Invalid semver: {current}")
    signals = {"breaking": 0, "feat": 0, "fix": 0}
    for subject in subjects:
        kind = classify_commit(subject)
        if kind in signals:
            signals[kind] += 1
    bump = infer_bump_from_commits(subjects, parts.major)
    next_ver, bump_label, reason = bump_version(current, bump)
    return {
        "current": current,
        "next": next_ver,
        "bump": bump_label,
        "reason": reason,
        "signals": signals,
    }


def compare_semver(a: str, b: str) -> int:
    pa, pb = parse_semver(a), parse_semver(b)
    if pa is None or pb is None:
        raise ValueError("Invalid semver comparison")
    if pa.major != pb.major:
        return pa.major - pb.major
    if pa.minor != pb.minor:
        return pa.minor - pb.minor
    return pa.patch - pb.patch
