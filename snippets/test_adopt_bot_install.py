#!/usr/bin/env python3
"""Adopt installs helper, gitignore block, Claude/OpenCode emit, bot permissions."""

from __future__ import annotations

import importlib.util
import json
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType

BUNDLE_ROOT = Path(__file__).resolve().parents[1]
ADOPT_SCRIPT = BUNDLE_ROOT / "snippets" / "adopt.py"


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


adopt = load_module(ADOPT_SCRIPT, "adopt_bot_install")

MINIMAL = """\
repo: test-bot-install
overlay: lsi
layout: lsi
canonical: .lsi/workflows
project:
  REPO_NAME: test-bot-install
  BASE_BRANCH: main
  PROTECTED_BRANCHES: main
"""

OPENCODE = """\
repo: test-bot-oc
overlay: lsi
layout: lsi
canonical: .lsi/workflows
agents_opencode:
  enabled: true
project:
  REPO_NAME: test-bot-oc
  BASE_BRANCH: main
  PROTECTED_BRANCHES: main
"""


class AdoptBotInstallTests(unittest.TestCase):
    def _prepare(self, config_text: str) -> tuple[Path, dict, dict[str, str]]:
        tmp = tempfile.mkdtemp()
        target = Path(tmp)
        cfg = target / "patch.yaml"
        cfg.write_text(config_text, encoding="utf-8")
        config = adopt.load_config(cfg)
        bundle_version = (BUNDLE_ROOT / "VERSION").read_text(encoding="utf-8").strip()
        tokens = {**adopt.build_tokens(config), "BUNDLE_VERSION": bundle_version}
        adopt.wipe_lsi_workflows(target)
        adopt.copy_core_bundle(target, tokens)
        adopt.copy_overlay(target, tokens, config)
        adopt.install_agent_stack(target, tokens, config)
        adopt.install_bot_session_docs(target, tokens)
        adopt.install_lsi_bin(target)
        adopt.merge_gitignore_local_artifacts(target)
        adopt.install_claude_commands(target, tokens)
        adopt.install_opencode_stack(target, tokens, config)
        adopt.merge_claude_bot_permissions(target)
        adopt.merge_opencode_bot_permissions(target, config)
        return target, config, tokens

    def test_helper_0755_and_stale_removed(self) -> None:
        target, config, tokens = self._prepare(MINIMAL)
        helper = target / ".lsi" / "bin" / "lsi-bitbucket"
        self.assertTrue(helper.is_file())
        self.assertTrue(helper.stat().st_mode & stat.S_IXUSR)
        stale = target / ".lsi" / "bin" / "stale-tool"
        stale.write_text("#!/bin/sh\n", encoding="utf-8")
        adopt.install_lsi_bin(target)
        self.assertFalse(stale.exists())
        self.assertTrue(helper.is_file())

    def test_gitignore_idempotent(self) -> None:
        target, _, _ = self._prepare(MINIMAL)
        gi = target / ".gitignore"
        self.assertTrue(gi.is_file())
        text1 = gi.read_text(encoding="utf-8")
        self.assertIn("lsi:local-artifacts", text1)
        gi.write_text(text1 + "\n# adopter custom\nfoo.bar\n", encoding="utf-8")
        adopt.merge_gitignore_local_artifacts(target)
        text2 = gi.read_text(encoding="utf-8")
        self.assertIn("foo.bar", text2)
        self.assertEqual(text2.count("# >>> lsi:local-artifacts"), 1)

    def test_claude_settings_merge(self) -> None:
        target = Path(tempfile.mkdtemp())
        settings = target / ".claude" / "settings.json"
        settings.parent.mkdir(parents=True)
        settings.write_text(
            json.dumps(
                {
                    "permissions": {"allow": ["Bash(echo:*)"], "deny": ["Bash(rm:*)"]},
                    "hooks": {"PreToolUse": []},
                }
            ),
            encoding="utf-8",
        )
        adopt.merge_claude_bot_permissions(target)
        data = json.loads(settings.read_text(encoding="utf-8"))
        allow = data["permissions"]["allow"]
        self.assertIn("Bash(echo:*)", allow)
        self.assertIn("Bash(.lsi/bin/lsi-bitbucket:*)", allow)
        self.assertEqual(data["permissions"]["deny"], ["Bash(rm:*)"])
        self.assertIn("hooks", data)
        blob = json.dumps(data)
        self.assertNotIn("git push", blob)
        self.assertNotIn("Bash(git commit", blob)
        adopt.merge_claude_bot_permissions(target)
        data2 = json.loads(settings.read_text(encoding="utf-8"))
        self.assertEqual(
            data2["permissions"]["allow"].count("Bash(.lsi/bin/lsi-bitbucket:*)"), 1
        )
        self.assertIn("api.bitbucket.org", data2["sandbox"]["network"]["allowedDomains"])

    def test_opencode_untouched_unless_opted_in(self) -> None:
        target, _, _ = self._prepare(MINIMAL)
        self.assertFalse((target / "opencode.json").exists())
        self.assertFalse((target / ".opencode").exists())

    def test_opencode_full_bodies_when_opted_in(self) -> None:
        target, _, _ = self._prepare(OPENCODE)
        path = target / ".opencode" / "commands" / "lsi-apply-bot.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        self.assertIn("**Steps**", text)
        self.assertIn("**Output**", text)
        self.assertIn("**Guardrails**", text)
        self.assertIn("$ARGUMENTS", text)
        self.assertNotIn("Canonical instructions: `.cursor/commands/", text)
        self.assertTrue((target / "opencode.json").is_file())

    def test_claude_commands_emitted(self) -> None:
        target, _, _ = self._prepare(MINIMAL)
        for name in ("pr-bot", "pr-bot-docs", "apply-bot", "review"):
            p = target / ".claude" / "commands" / "lsi" / f"{name}.md"
            self.assertTrue(p.is_file(), msg=f"missing {p}")
            self.assertTrue(p.read_text(encoding="utf-8").startswith("---\ndescription:"))


if __name__ == "__main__":
    sys.exit(0 if unittest.main(exit=False).result.wasSuccessful() else 1)
