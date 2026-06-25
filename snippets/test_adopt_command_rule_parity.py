"""Regression gate: adopt.py does not delete unlisted surplus files; remove_after_adopt
deletes only pre-listed paths; parity check detects surplus correctly.
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType

BUNDLE_ROOT = Path(__file__).resolve().parents[1]
ADOPT_SCRIPT = BUNDLE_ROOT / "snippets" / "adopt.py"
AUDIT_SCRIPT = BUNDLE_ROOT / "snippets" / "audit-agent-docs.py"


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


adopt = load_module(ADOPT_SCRIPT, "adopt_parity")
audit = load_module(AUDIT_SCRIPT, "audit_parity")


MINIMAL_CONFIG = """\
repo: parity-test
overlay: lsi
layout: lsi
canonical: .lsi/workflows
project:
  REPO_NAME: parity-test
  BASE_BRANCH: main
  PROTECTED_BRANCHES: main
"""

CONFIG_WITH_REMOVE = """\
repo: parity-test
overlay: lsi
layout: lsi
canonical: .lsi/workflows
project:
  REPO_NAME: parity-test
  BASE_BRANCH: main
  PROTECTED_BRANCHES: main
remove_after_adopt:
  - .cursor/rules/code_review.mdc
"""


def _run_adopt(target: Path, config_text: str) -> None:
    cfg = target / "patch.yaml"
    cfg.write_text(config_text, encoding="utf-8")
    config = adopt.load_config(cfg)
    bundle_version = (BUNDLE_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    tokens = {**adopt.build_tokens(config), "BUNDLE_VERSION": bundle_version}
    adopt.wipe_lsi_workflows(target)
    adopt.copy_core_bundle(target, tokens)
    adopt.copy_overlay(target, tokens, config)
    adopt.install_agent_stack(target, tokens, config)
    adopt.remove_after_adopt(target, config)


class AdoptCommandRuleParityTests(unittest.TestCase):
    def test_adopt_does_not_delete_surplus_files(self) -> None:
        """Surplus files not in expected set must survive adopt unchanged."""
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            _run_adopt(target, MINIMAL_CONFIG)
            surplus = target / ".cursor" / "commands" / "my-custom-command.md"
            surplus.write_text("# custom\n", encoding="utf-8")

            # Re-adopt — surplus must survive
            _run_adopt(target, MINIMAL_CONFIG)
            self.assertTrue(surplus.is_file(), "adopt deleted a surplus file it should not touch")

    def test_remove_after_adopt_removes_only_listed_path(self) -> None:
        """remove_after_adopt removes the pre-listed path but leaves others alone."""
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            _run_adopt(target, MINIMAL_CONFIG)
            # Place a legacy alias
            legacy = target / ".cursor" / "rules" / "code_review.mdc"
            legacy.write_text("# legacy\n", encoding="utf-8")
            other = target / ".cursor" / "rules" / "my-rule.mdc"
            other.write_text("# my rule\n", encoding="utf-8")

            # Adopt with remove_after_adopt listing the legacy alias
            _run_adopt(target, CONFIG_WITH_REMOVE)

            self.assertFalse(legacy.is_file(), "pre-listed legacy alias should be removed")
            self.assertTrue(other.is_file(), "unlisted rule should NOT be removed")

    def test_parity_check_detects_surplus_command(self) -> None:
        """check_agent_stack_parity reports ERROR for surplus commands."""
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            _run_adopt(target, MINIMAL_CONFIG)
            surplus = target / ".cursor" / "commands" / "my-extra.md"
            surplus.write_text("# extra\n", encoding="utf-8")

            findings = audit.check_agent_stack_parity(target)
            errors = [f for f in findings if f.category == "agent_stack_parity" and "my-extra" in f.message]
            self.assertTrue(errors, "expected parity ERROR for surplus command my-extra.md")

    def test_parity_check_detects_legacy_alias_pair(self) -> None:
        """check_agent_stack_parity reports ERROR when both alias pair files exist."""
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            _run_adopt(target, MINIMAL_CONFIG)
            rules_dir = target / ".cursor" / "rules"
            (rules_dir / "code-review.mdc").write_text("# canonical\n", encoding="utf-8")
            (rules_dir / "code_review.mdc").write_text("# legacy\n", encoding="utf-8")

            findings = audit.check_agent_stack_parity(target)
            alias_errors = [
                f for f in findings
                if f.category == "agent_stack_parity" and "Legacy alias" in f.message
            ]
            self.assertTrue(alias_errors, "expected parity ERROR for legacy alias pair")

    def test_parity_check_clean_after_remove_after_adopt(self) -> None:
        """After remove_after_adopt removes the listed legacy alias, no parity error for it."""
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            _run_adopt(target, MINIMAL_CONFIG)
            rules_dir = target / ".cursor" / "rules"
            (rules_dir / "code_review.mdc").write_text("# legacy\n", encoding="utf-8")

            _run_adopt(target, CONFIG_WITH_REMOVE)

            findings = audit.check_agent_stack_parity(target)
            alias_errors = [
                f for f in findings
                if f.category == "agent_stack_parity" and "code_review" in f.message
            ]
            self.assertFalse(alias_errors, "legacy alias should have been removed")


if __name__ == "__main__":
    sys.exit(0 if unittest.main(exit=False).result.wasSuccessful() else 1)
