"""Tests for snippets/check-workflow-link-sources.py."""

from __future__ import annotations

import importlib.util
import io
import runpy
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parent / "check-workflow-link-sources.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "check-workflow-link-sources"


def load_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("check_workflow_link_sources", SCRIPT)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_workflow_link_sources"] = module
    spec.loader.exec_module(module)
    return module


mod = load_module()


class ScanFileTests(unittest.TestCase):
    def test_clean_file_has_no_hits(self) -> None:
        path = FIXTURES / "clean" / "ok.md"
        hits = mod.scan_file(path, (mod.PHASE_1, mod.PHASE_2))
        self.assertEqual(hits, [])

    def test_overlay_pattern_reported(self) -> None:
        path = FIXTURES / "violations" / "overlay.md"
        hits = mod.scan_file(path, (mod.PHASE_1,))
        self.assertEqual(len(hits), 1)
        self.assertIn("overlay.md", hits[0])
        self.assertIn(mod.PHASE_1, hits[0])

    def test_agent_stack_pattern_reported(self) -> None:
        path = FIXTURES / "violations" / "agent-stack.md"
        hits = mod.scan_file(path, (mod.PHASE_2,))
        self.assertEqual(len(hits), 1)
        self.assertIn("agent-stack.md", hits[0])
        self.assertIn(mod.PHASE_2, hits[0])

    def test_multiple_patterns_report_all_hits(self) -> None:
        text = f"Bad {mod.PHASE_1}foo.md) and {mod.PHASE_2}bar.md)\n"
        path = FIXTURES / "violations" / "both.md"
        path.write_text(text, encoding="utf-8")
        try:
            hits = mod.scan_file(path, (mod.PHASE_1, mod.PHASE_2))
            self.assertEqual(len(hits), 2)
        finally:
            path.unlink(missing_ok=True)


class MainTests(unittest.TestCase):
    def test_main_passes_on_clean_fixture_tree(self) -> None:
        with patch.object(mod, "SCAN_DIRS", (FIXTURES / "clean",)):
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = mod.main()
        self.assertEqual(code, 0)
        self.assertIn("OK:", stdout.getvalue())

    def test_main_fails_on_overlay_violation(self) -> None:
        with patch.object(mod, "SCAN_DIRS", (FIXTURES / "violations",)):
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                code = mod.main()
        self.assertEqual(code, 1)
        err = stderr.getvalue()
        self.assertIn("FORBIDDEN WORKFLOW LINK SOURCES:", err)
        self.assertIn("overlay.md", err)
        self.assertIn(mod.PHASE_1, err)

    def test_main_fails_on_agent_stack_when_phase_2_enabled(self) -> None:
        only_agent = FIXTURES / "violations" / "agent-only"
        only_agent.mkdir(exist_ok=True)
        bad = only_agent / "bad.md"
        bad.write_text(f"Link {mod.PHASE_2}lsi-help.md)\n", encoding="utf-8")
        try:
            with patch.object(mod, "SCAN_DIRS", (only_agent,)), patch.object(
                mod, "ENABLE_PHASE_2", True
            ):
                stderr = io.StringIO()
                with redirect_stderr(stderr):
                    code = mod.main()
            self.assertEqual(code, 1)
            self.assertIn(mod.PHASE_2, stderr.getvalue())
        finally:
            bad.unlink(missing_ok=True)
            only_agent.rmdir()

    def test_main_ignores_agent_stack_when_phase_2_disabled(self) -> None:
        only_agent = FIXTURES / "violations" / "agent-only"
        only_agent.mkdir(exist_ok=True)
        bad = only_agent / "bad.md"
        bad.write_text(f"Link {mod.PHASE_2}lsi-help.md)\n", encoding="utf-8")
        try:
            with patch.object(mod, "SCAN_DIRS", (only_agent,)), patch.object(
                mod, "ENABLE_PHASE_2", False
            ):
                stdout = io.StringIO()
                with redirect_stdout(stdout):
                    code = mod.main()
            self.assertEqual(code, 0)
            self.assertIn("OK:", stdout.getvalue())
        finally:
            bad.unlink(missing_ok=True)
            only_agent.rmdir()

    def test_main_skips_missing_scan_dirs(self) -> None:
        missing = FIXTURES / "does-not-exist"
        with patch.object(mod, "SCAN_DIRS", (missing, FIXTURES / "clean")):
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = mod.main()
        self.assertEqual(code, 0)
        self.assertIn("OK:", stdout.getvalue())

    def test_main_passes_on_real_bundle_trees(self) -> None:
        code = mod.main()
        self.assertEqual(code, 0)


class CliTests(unittest.TestCase):
    def test_script_entry_point(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("OK:", result.stdout)

    def test_name_main_guard_exits_zero(self) -> None:
        with self.assertRaises(SystemExit) as ctx:
            runpy.run_path(str(SCRIPT), run_name="__main__")
        self.assertEqual(ctx.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
