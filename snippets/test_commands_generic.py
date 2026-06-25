#!/usr/bin/env python3
"""Denylist regression gate: agent-stack commands must not embed repo-specific domain strings.

Domain tables, personas, and test paths belong in per-repo openspec-git-integration.md
patches, not in the shared agent-stack command sources.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

BUNDLE_ROOT = Path(__file__).resolve().parents[1]
COMMANDS_DIR = BUNDLE_ROOT / "overlays" / "lsi" / "agent-stack" / "commands"

# Strings that must NOT appear in generic command sources.
# Domain belongs in patches/files/<repo>/openspec-git-integration.md.
DENYLIST = [
    # video-encoder domain
    "FFmpeg",
    "ffmpeg",
    "HLS",
    "BLPOP",
    "BRPOP",
    "S3 / AWS",
    "boto3",
    "s3_manager",
    "ffmpeg_pipeline",
    "data-lake",
    "uv run pytest --cov=src --cov=dev",
    # ai-agent domain
    "FastAPI",
    "fastapi",
    "frontend proxy",
    # web/rails domain
    "bin/rspec",
    "bin/check-schema",
    # Avoid hard-coded per-repo pytest invocations
    "--cov-fail-under=100",
]

# Worker scope references that should come from integration doc, not command sources
DOMAIN_SCOPE_PHRASES = [
    "Worker listener",
    "Worker / `main.py`",
    "FFmpeg / HLS",
    "S3 / AWS CLI",
    "Webhook / HTTP client",
    "video-encoder worker",
    "data-lake scopes",
]


class CommandsGenericTest(unittest.TestCase):
    def setUp(self) -> None:
        self.commands: list[Path] = sorted(COMMANDS_DIR.glob("*.md"))
        self.assertTrue(
            self.commands,
            f"No command files found in {COMMANDS_DIR}",
        )

    def test_no_denylist_strings_in_commands(self) -> None:
        hits: list[str] = []
        for cmd in self.commands:
            text = cmd.read_text(encoding="utf-8")
            for needle in DENYLIST:
                if needle in text:
                    hits.append(f"{cmd.name}: contains denylist string {needle!r}")
        self.assertEqual(hits, [], msg="\n".join(hits))

    def test_no_domain_scope_phrases_in_commands(self) -> None:
        hits: list[str] = []
        for cmd in self.commands:
            text = cmd.read_text(encoding="utf-8")
            for phrase in DOMAIN_SCOPE_PHRASES:
                if phrase in text:
                    hits.append(f"{cmd.name}: contains domain phrase {phrase!r}")
        self.assertEqual(hits, [], msg="\n".join(hits))

    def test_all_lsi_commands_defer_to_integration_doc(self) -> None:
        """Commands that reference commit mapping, code review, or test gates
        must cite openspec-git-integration.md rather than inline tables."""
        domain_refs = ("openspec-git-integration.md",)
        must_defer = {
            "lsi-commit.md": "Commit mapping",
            "lsi-review.md": "Code review",
            "lsi-readiness.md": "PR production readiness",
        }
        hits: list[str] = []
        for name, section in must_defer.items():
            cmd = COMMANDS_DIR / name
            if not cmd.is_file():
                hits.append(f"{name}: file missing")
                continue
            text = cmd.read_text(encoding="utf-8")
            has_ref = any(ref in text for ref in domain_refs)
            if not has_ref:
                hits.append(
                    f"{name}: expected reference to openspec-git-integration.md for section '{section}'"
                )
        self.assertEqual(hits, [], msg="\n".join(hits))


if __name__ == "__main__":
    sys.exit(0 if unittest.main(exit=False).result.wasSuccessful() else 1)
