#!/usr/bin/env python3
"""Bot command sources must include Output, refuse Output, never-auth, budget 3, no Next."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

BUNDLE_ROOT = Path(__file__).resolve().parents[1]
COMMANDS = BUNDLE_ROOT / "overlays" / "lsi" / "agent-stack" / "commands"

BOT_COMMANDS = [
    "lsi-pr-bot.md",
    "lsi-pr-bot-docs.md",
    "lsi-apply-bot.md",
]

NEVER_AUTH = [
    "approve",
    "merge",
    "decline",
    "request-changes",
    "force-push",
    "history rewrite",
    "protected-branch",
    "edit/delete/resolve",
]


class BotCommandTextTests(unittest.TestCase):
    def test_bot_commands_shape(self) -> None:
        for name in BOT_COMMANDS:
            path = COMMANDS / name
            self.assertTrue(path.is_file(), msg=f"missing {path}")
            text = path.read_text(encoding="utf-8")
            self.assertIn("**Output**", text)
            self.assertIn("**Output (refuse)**", text)
            self.assertIn("**Guardrails**", text)
            self.assertIn("3", text)  # loop budget
            self.assertRegex(text, r"(?i)loop budget|≤3|max \*\*3\*\*|budget 3|≤ 3")
            self.assertNotRegex(text, r"(?m)^Next:")
            self.assertNotIn("\nNext:", text)
            lower = text.lower()
            for phrase in NEVER_AUTH:
                self.assertIn(phrase, lower, msg=f"{name} missing never-auth: {phrase}")


if __name__ == "__main__":
    sys.exit(0 if unittest.main(exit=False).result.wasSuccessful() else 1)
