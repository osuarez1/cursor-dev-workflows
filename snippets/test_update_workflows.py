"""Tests for snippets/update-workflows.py repo detection."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from types import ModuleType

SCRIPT = Path(__file__).resolve().parent / "update-workflows.py"


def load_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("update_workflows", SCRIPT)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["update_workflows"] = module
    spec.loader.exec_module(module)
    return module


mod = load_module()
BUNDLE = mod.BUNDLE_ROOT


class UpdateWorkflowsTests(unittest.TestCase):
    def test_detects_bundle_maintainer(self) -> None:
        self.assertTrue(mod.is_bundle_maintainer(BUNDLE))

    def test_finds_patch_for_web(self) -> None:
        patch = mod.find_patch_for_repo(BUNDLE, "web")
        self.assertIsNotNone(patch)
        assert patch is not None
        self.assertEqual(patch.name, "web.yaml")

    def test_read_project_repo_name(self) -> None:
        name = mod.read_project_repo_name(BUNDLE)
        self.assertEqual(name, "cursor-dev-workflows")

    def test_load_maintainer_adopter_targets_missing_file(self) -> None:
        targets = mod.load_maintainer_adopter_targets(BUNDLE / "nonexistent-bundle")
        self.assertEqual(targets, [])

    def test_load_maintainer_adopter_targets_from_local_yaml(self) -> None:
        local = BUNDLE / mod.MAINTAINER_ADOPTERS_LOCAL
        if not local.is_file():
            self.skipTest(f"{mod.MAINTAINER_ADOPTERS_LOCAL} not present")
        targets = mod.load_maintainer_adopter_targets(BUNDLE)
        self.assertGreater(len(targets), 0)
        for target, config in targets:
            self.assertTrue(target.startswith("../"))
            self.assertTrue(config.startswith("patches/"))


if __name__ == "__main__":
    unittest.main()
