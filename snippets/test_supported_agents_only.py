#!/usr/bin/env python3
"""Regression gate: bundle emits only Cursor + Claude artifacts.

Checks:
- git-tracked bundle tree has no forbidden agent directories
- adopt.py errors on legacy multi-tool YAML keys
- adopt output contains no forbidden directories
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType

BUNDLE_ROOT = Path(__file__).resolve().parents[1]
ADOPT_SCRIPT = BUNDLE_ROOT / "snippets" / "adopt.py"

FORBIDDEN_DIRS = (".opencode", ".aiassistant", ".junie", "bin")
FORBIDDEN_GLOBS = ("bin/lsi-*", "bin/opsx-*")


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


adopt = load_module(ADOPT_SCRIPT, "adopt_supported_agents")


MINIMAL_CONFIG = """\
repo: test-agents-only
overlay: lsi
layout: lsi
canonical: .lsi/workflows
project:
  REPO_NAME: test-agents-only
  BASE_BRANCH: main
  PROTECTED_BRANCHES: main
"""

LEGACY_KEY_CONFIG_TEMPLATE = """\
repo: test-legacy
overlay: lsi
layout: lsi
canonical: .lsi/workflows
{legacy_key}: legacy_value
project:
  REPO_NAME: test-legacy
  BASE_BRANCH: main
  PROTECTED_BRANCHES: main
"""


class SupportedAgentsOnlyTests(unittest.TestCase):
    def test_bundle_git_tree_has_no_forbidden_dirs(self) -> None:
        result = subprocess.run(
            ["git", "ls-files", "--", *[f"{d}/" for d in FORBIDDEN_DIRS],
             "bin/lsi-*", "bin/opsx-*"],
            cwd=BUNDLE_ROOT,
            capture_output=True,
            text=True,
        )
        tracked = [line for line in result.stdout.splitlines() if line.strip()]
        self.assertEqual(
            tracked,
            [],
            msg=f"Bundle git tree contains forbidden paths: {tracked}",
        )

    def test_legacy_opencode_key_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = Path(tmp) / "patch.yaml"
            cfg.write_text(
                LEGACY_KEY_CONFIG_TEMPLATE.format(legacy_key="agents_opencode"),
                encoding="utf-8",
            )
            with self.assertRaises(SystemExit) as ctx:
                adopt.load_config(cfg)
            self.assertIn("agents_opencode", str(ctx.exception))

    def test_legacy_junie_key_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = Path(tmp) / "patch.yaml"
            cfg.write_text(
                LEGACY_KEY_CONFIG_TEMPLATE.format(legacy_key="agents_junie"),
                encoding="utf-8",
            )
            with self.assertRaises(SystemExit) as ctx:
                adopt.load_config(cfg)
            self.assertIn("agents_junie", str(ctx.exception))

    def test_legacy_jetbrains_key_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = Path(tmp) / "patch.yaml"
            cfg.write_text(
                LEGACY_KEY_CONFIG_TEMPLATE.format(legacy_key="agents_jetbrains"),
                encoding="utf-8",
            )
            with self.assertRaises(SystemExit) as ctx:
                adopt.load_config(cfg)
            self.assertIn("agents_jetbrains", str(ctx.exception))

    def test_legacy_bin_key_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = Path(tmp) / "patch.yaml"
            cfg.write_text(
                LEGACY_KEY_CONFIG_TEMPLATE.format(legacy_key="bin"),
                encoding="utf-8",
            )
            with self.assertRaises(SystemExit) as ctx:
                adopt.load_config(cfg)
            self.assertIn("bin", str(ctx.exception))

    def test_adopt_output_has_no_forbidden_dirs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            cfg = target / "patch.yaml"
            cfg.write_text(MINIMAL_CONFIG, encoding="utf-8")
            config = adopt.load_config(cfg)
            bundle_version = (BUNDLE_ROOT / "VERSION").read_text(encoding="utf-8").strip()
            tokens = {**adopt.build_tokens(config), "BUNDLE_VERSION": bundle_version}
            adopt.wipe_lsi_workflows(target)
            adopt.copy_core_bundle(target, tokens)
            adopt.copy_overlay(target, tokens, config)
            adopt.install_agent_stack(target, tokens, config)
            for forbidden in FORBIDDEN_DIRS:
                self.assertFalse(
                    (target / forbidden).exists(),
                    msg=f"adopt wrote forbidden dir: {forbidden}",
                )
            for glob in FORBIDDEN_GLOBS:
                hits = list(target.glob(glob))
                self.assertEqual(hits, [], msg=f"adopt wrote forbidden files: {hits}")


if __name__ == "__main__":
    sys.exit(0 if unittest.main(exit=False).result.wasSuccessful() else 1)
