"""Tests for snippets/install-maintainer-local.py path rewrites."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from types import ModuleType

SCRIPT = Path(__file__).resolve().parent / "install-maintainer-local.py"


def load_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("install_maintainer_local", SCRIPT)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["install_maintainer_local"] = module
    spec.loader.exec_module(module)
    return module


mod = load_module()


class MaintainerLocalInstallTests(unittest.TestCase):
    def test_rewrites_sdlc_and_overlay_paths(self) -> None:
        sample = (
            "[git-trello.md](../../docs/sdlc/git-trello.md) · "
            "[openspec](../../docs/workflows/openspec-git-integration.md) · "
            "[tpl](../../docs/workflows/templates/pr-description.template.md)"
        )
        out = mod.transform_command(sample)
        self.assertIn("../../overlays/lsi/docs/sdlc/", out)
        self.assertIn("../../overlays/lsi/docs/workflows/openspec-git-integration.md", out)
        self.assertIn("../../templates/pr-description.template.md", out)

    def test_overlay_commands_install_without_drift(self) -> None:
        overlay = mod.OVERLAY_COMMANDS
        self.assertTrue(overlay.is_dir())
        for src in overlay.glob("*.md"):
            expected = mod.transform_command(src.read_text(encoding="utf-8"))
            installed = mod.CURSOR_COMMANDS / src.name
            self.assertTrue(installed.is_file(), f"missing {src.name} — run bootstrap")
            self.assertEqual(
                installed.read_text(encoding="utf-8"),
                expected,
                f"drift in {src.name} — run ./snippets/bootstrap-maintainer-local.sh",
            )


if __name__ == "__main__":
    unittest.main()
