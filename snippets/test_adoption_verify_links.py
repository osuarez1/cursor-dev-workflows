"""Tests for snippets/adoption-verify-links.py."""

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


class VerifyFunctionTests(unittest.TestCase):
    def test_profile_a_pass(self) -> None:
        root = fixture("profile-a-pass")
        broken, patterns, warnings = verify(
            root.resolve(),
            (root / "docs/workflows").resolve(),
            "A",
            True,
        )
        self.assertEqual(broken, [])
        self.assertEqual(patterns, [])
        self.assertEqual(warnings, [])

    def test_profile_a_broken_router(self) -> None:
        root = fixture("profile-a-broken-router")
        broken, patterns, _ = verify(
            root.resolve(),
            (root / "docs/workflows").resolve(),
            "A",
            True,
        )
        self.assertTrue(any("which-workflow.md" in item for item in broken))
        self.assertEqual(patterns, [])

    def test_profile_a_broken_agents(self) -> None:
        root = fixture("profile-a-broken-agents")
        broken, patterns, _ = verify(
            root.resolve(),
            (root / "docs/workflows").resolve(),
            "A",
            True,
        )
        self.assertTrue(any("AGENTS.md" in item for item in broken))
        self.assertEqual(patterns, [])

    def test_profile_b_doubled_prefix(self) -> None:
        root = fixture("profile-b-doubled-prefix")
        broken, patterns, _ = verify(
            root.resolve(),
            (root / "docs/workflows").resolve(),
            "B",
            True,
        )
        self.assertEqual(broken, [])
        self.assertTrue(any("doubled prefix" in item for item in patterns))

    def test_out_of_repo_link(self) -> None:
        root = fixture("out-of-repo-link")
        broken, patterns, _ = verify(
            root.resolve(),
            (root / "docs/workflows").resolve(),
            "A",
            True,
        )
        self.assertTrue(any("outside repo root" in item for item in broken))
        self.assertEqual(patterns, [])

    def test_profile_b_extra_dirs_pass(self) -> None:
        root = fixture("profile-b-extra-dirs-pass")
        broken, patterns, _ = verify(
            root.resolve(),
            (root / "docs/workflows").resolve(),
            "B",
            True,
            extra_dirs=[Path("docs/templates")],
        )
        self.assertEqual(broken, [])
        self.assertEqual(patterns, [])

    def test_profile_a_missing_router_warns(self) -> None:
        root = fixture("profile-b-doubled-prefix")
        _, _, warnings = verify(
            root.resolve(),
            (root / "docs/workflows").resolve(),
            "A",
            True,
        )
        self.assertTrue(
            any("which-workflow.md not found" in item for item in warnings)
        )


class MainCliTests(unittest.TestCase):
    def run_script(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        cmd = [
            sys.executable,
            str(SCRIPT),
            "--repo-root",
            str(root),
            "--canonical",
            "docs/workflows",
            *args,
        ]
        return subprocess.run(cmd, capture_output=True, text=True, check=False)

    def test_cli_profile_a_pass(self) -> None:
        result = self.run_script(fixture("profile-a-pass"), "--profile", "A")
        self.assertEqual(result.returncode, 0)
        self.assertIn("OK:", result.stdout)

    def test_cli_profile_a_broken_router(self) -> None:
        result = self.run_script(fixture("profile-a-broken-router"), "--profile", "A")
        self.assertEqual(result.returncode, 1)
        self.assertIn("BROKEN LINKS:", result.stderr)

    def test_main_profile_b_extra_dirs(self) -> None:
        root = fixture("profile-b-extra-dirs-pass")
        code = main(
            [
                "--repo-root",
                str(root),
                "--canonical",
                "docs/workflows",
                "--profile",
                "B",
                "--extra-dirs",
                "docs/templates",
            ]
        )
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
