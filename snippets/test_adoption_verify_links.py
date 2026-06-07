"""Tests for snippets/adoption-verify-links.py (LSI layout)."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path
from types import ModuleType

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "adoption-verify"
SCRIPT = Path(__file__).resolve().parent / "adoption-verify-links.py"


def load_script_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("adoption_verify_links", SCRIPT)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


verify_mod = load_script_module()
verify = verify_mod.verify
main = verify_mod.main


def fixture(name: str) -> Path:
    return FIXTURES / name


def canonical(root: Path) -> Path:
    return (root / ".lsi" / "workflows").resolve()


class VerifyFunctionTests(unittest.TestCase):
    def test_lsi_pass(self) -> None:
        root = fixture("lsi-pass")
        broken, patterns, warnings = verify(root.resolve(), canonical(root))
        self.assertEqual(broken, [])
        self.assertEqual(patterns, [])
        self.assertEqual(warnings, [])

    def test_lsi_broken_router(self) -> None:
        root = fixture("lsi-broken-router")
        broken, patterns, _ = verify(root.resolve(), canonical(root))
        self.assertTrue(any("which-workflow.md" in item for item in broken))
        self.assertEqual(patterns, [])

    def test_lsi_broken_agents(self) -> None:
        root = fixture("lsi-broken-agents")
        broken, patterns, _ = verify(root.resolve(), canonical(root))
        self.assertTrue(any("AGENTS.md" in item for item in broken))
        self.assertEqual(patterns, [])

    def test_lsi_doubled_prefix(self) -> None:
        root = fixture("lsi-doubled-prefix")
        broken, patterns, _ = verify(root.resolve(), canonical(root))
        self.assertEqual(broken, [])
        self.assertTrue(any("doubled prefix" in item for item in patterns))

    def test_out_of_repo_link(self) -> None:
        root = fixture("out-of-repo-link")
        broken, patterns, _ = verify(root.resolve(), canonical(root))
        self.assertTrue(any("outside repo root" in item for item in broken))
        self.assertEqual(patterns, [])

    def test_lsi_extra_dirs_pass(self) -> None:
        root = fixture("lsi-extra-dirs-pass")
        broken, patterns, _ = verify(
            root.resolve(),
            canonical(root),
            extra_dirs=[Path("docs/templates")],
        )
        self.assertEqual(broken, [])
        self.assertEqual(patterns, [])

    def test_lsi_missing_router_warns(self) -> None:
        root = fixture("lsi-doubled-prefix")
        _, _, warnings = verify(root.resolve(), canonical(root))
        self.assertFalse(any("which-workflow.md not found" in item for item in warnings))


class MainCliTests(unittest.TestCase):
    def run_script(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        cmd = [
            sys.executable,
            str(SCRIPT),
            "--repo-root",
            str(root),
            "--canonical",
            ".lsi/workflows",
            *args,
        ]
        return subprocess.run(cmd, capture_output=True, text=True, check=False)

    def test_cli_lsi_pass(self) -> None:
        result = self.run_script(fixture("lsi-pass"))
        self.assertEqual(result.returncode, 0)
        self.assertIn("OK:", result.stdout)

    def test_cli_lsi_broken_router(self) -> None:
        result = self.run_script(fixture("lsi-broken-router"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("BROKEN LINKS:", result.stderr)

    def test_main_lsi_extra_dirs(self) -> None:
        root = fixture("lsi-extra-dirs-pass")
        code = main(
            [
                "--repo-root",
                str(root),
                "--canonical",
                ".lsi/workflows",
                "--extra-dirs",
                "docs/templates",
            ]
        )
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
