"""Tests for snippets/adopt.py token injection and patch YAML loading."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from types import ModuleType

ADOPT_SCRIPT = Path(__file__).resolve().parent / "adopt.py"


def load_adopt_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("adopt", ADOPT_SCRIPT)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {ADOPT_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["adopt"] = module
    spec.loader.exec_module(module)
    return module


adopt = load_adopt_module()


class AdoptTokenTests(unittest.TestCase):
    def test_substitute_bundle_version_token(self) -> None:
        bundle_version = (adopt.BUNDLE_ROOT / "VERSION").read_text(encoding="utf-8").strip()
        result = adopt.substitute_tokens("v{{BUNDLE_VERSION}}", {"BUNDLE_VERSION": bundle_version})
        self.assertEqual(result, f"v{bundle_version}")

    def test_adopt_token_map_includes_bundle_version(self) -> None:
        config = adopt.load_config(adopt.BUNDLE_ROOT / "patches" / "web.yaml")
        bundle_version = (adopt.BUNDLE_ROOT / "VERSION").read_text(encoding="utf-8").strip()
        tokens = {**adopt.build_tokens(config), "BUNDLE_VERSION": bundle_version}
        self.assertEqual(tokens["BUNDLE_VERSION"], bundle_version)
        self.assertIn("REPO_NAME", tokens)

    def test_load_config_web_yaml_list_keys(self) -> None:
        config = adopt.load_config(adopt.BUNDLE_ROOT / "patches" / "web.yaml")
        self.assertEqual(config["repo"], "web")
        globs = config.get("scope_exclude_globs")
        self.assertIsInstance(globs, list)
        self.assertGreater(len(globs), 0)
        self.assertTrue(all(isinstance(item, str) for item in globs))

    def test_load_simple_yaml_web_patch_list_keys(self) -> None:
        """Stdlib fallback path (no PyYAML) must parse patch list keys."""
        text = (adopt.BUNDLE_ROOT / "patches" / "web.yaml").read_text(encoding="utf-8")
        config = adopt._load_simple_yaml(text)
        self.assertEqual(config["repo"], "web")
        globs = config.get("scope_exclude_globs")
        self.assertIsInstance(globs, list)
        self.assertGreater(len(globs), 0)

    def test_load_config_ai_agent_yaml_preserve_list(self) -> None:
        config = adopt.load_config(adopt.BUNDLE_ROOT / "patches" / "ai-agent.yaml")
        self.assertEqual(config["repo"], "ai-agent")
        preserve = config.get("preserve")
        self.assertIsInstance(preserve, list)
        self.assertIn("bitbucket-pipelines.yml", preserve)

    def test_load_simple_yaml_ai_agent_preserve_list(self) -> None:
        """Stdlib fallback must parse top-level preserve list keys."""
        text = (adopt.BUNDLE_ROOT / "patches" / "ai-agent.yaml").read_text(encoding="utf-8")
        config = adopt._load_simple_yaml(text)
        self.assertEqual(config["repo"], "ai-agent")
        preserve = config.get("preserve")
        self.assertIsInstance(preserve, list)
        self.assertIn("bitbucket-pipelines.yml", preserve)


if __name__ == "__main__":
    unittest.main()
