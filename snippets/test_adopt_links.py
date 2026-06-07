"""End-to-end adopt → verify link regression tests."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType

BUNDLE_ROOT = Path(__file__).resolve().parents[1]
ADOPT_SCRIPT = BUNDLE_ROOT / "snippets" / "adopt.py"
VERIFY_SCRIPT = BUNDLE_ROOT / "snippets" / "adoption-verify-links.py"


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


adopt = load_module(ADOPT_SCRIPT, "adopt")
verify_mod = load_module(VERIFY_SCRIPT, "adoption_verify_links")
verify = verify_mod.verify


TEST_CONFIG = """\
repo: adopt-link-test
overlay: lsi
layout: lsi
canonical: .lsi/workflows
project:
  REPO_NAME: adopt-link-test
  BASE_BRANCH: main
  PROTECTED_BRANCHES: main
overlay_files:
  ticket-card-info.md: patches/files/_template/ticket-card-info.md
  test-requirements.md: patches/files/_template/test-requirements.md
  versioning-and-releases.md: patches/files/_template/versioning-and-releases.md
bootstrap:
  version.txt: "0.1.0"
"""

# Minimal repo-root targets referenced from adopted .lsi/workflows/ and docs/ai/.
LINK_TARGET_STUBS = (
    "README.md",
    "adoption-checklist.md",
    "bitbucket-pipelines.yml",
    "docs/sdlc/bitbucket.md",
    "docs/deployment/secrets.md",
    "docs/ai/openspec-sync.md",
    "openspec/config.yaml",
    "openspec/specs/.gitkeep",
    "snippets/user-rule-only-commit-when-asked.md",
    "snippets/gitignore-local-artifacts.txt",
)


def seed_link_targets(target: Path) -> None:
    for rel in LINK_TARGET_STUBS:
        path = target / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# stub\n", encoding="utf-8")


class AdoptLinksRegressionTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory()
        self.target = Path(self._tmpdir.name)
        self.config_path = self.target / "test-adopt.yaml"
        self.config_path.write_text(TEST_CONFIG, encoding="utf-8")
        (self.target / "PROJECT.md").write_text(
            "# adopt-link-test\n\n| Token | Value |\n|-------|-------|\n"
            "| `REPO_NAME` | `adopt-link-test` |\n",
            encoding="utf-8",
        )
        seed_link_targets(self.target)

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def run_adopt(self) -> None:
        config = adopt.load_config(self.config_path)
        bundle_version = (BUNDLE_ROOT / "VERSION").read_text(encoding="utf-8").strip()
        tokens = {**adopt.build_tokens(config), "BUNDLE_VERSION": bundle_version}
        adopt.wipe_lsi_workflows(self.target)
        adopt.copy_core_bundle(self.target, tokens)
        adopt.copy_overlay(self.target, tokens, config)
        adopt.merge_which_workflow_lsi(self.target)
        adopt.install_agent_stack(self.target, tokens, config)
        adopt.merge_convention(self.target)
        adopt.merge_agents_markers(self.target)
        adopt.update_project_md(self.target, config, bundle_version)
        adopt.bootstrap_files(self.target, config)

    def test_adopted_workflows_have_no_broken_links(self) -> None:
        self.run_adopt()
        canonical = (self.target / ".lsi" / "workflows").resolve()
        broken, patterns, _ = verify(self.target.resolve(), canonical)
        self.assertEqual(broken, [], msg="\n".join(broken))
        self.assertEqual(patterns, [], msg="\n".join(patterns))

    def test_docs_ai_cross_tree_links(self) -> None:
        self.run_adopt()
        canonical = (self.target / ".lsi" / "workflows").resolve()
        broken, patterns, _ = verify(
            self.target.resolve(),
            canonical,
            extra_dirs=[Path("docs/ai")],
        )
        self.assertEqual(broken, [], msg="\n".join(broken))
        self.assertEqual(patterns, [], msg="\n".join(patterns))

    def test_no_maintainer_path_substrings_in_adopted_workflows(self) -> None:
        self.run_adopt()
        lsi = self.target / ".lsi" / "workflows"
        forbidden = ("overlays/lsi/", "../../agent-stack/")
        hits: list[str] = []
        for md in sorted(lsi.rglob("*.md")):
            text = md.read_text(encoding="utf-8")
            rel = md.relative_to(self.target)
            for needle in forbidden:
                if needle in text:
                    hits.append(f"{rel}: contains {needle!r}")
        self.assertEqual(hits, [], msg="\n".join(hits))

    def test_bundle_version_token_parity(self) -> None:
        self.run_adopt()
        bundle_version = (BUNDLE_ROOT / "VERSION").read_text(encoding="utf-8").strip()
        project = (self.target / "PROJECT.md").read_text(encoding="utf-8")
        self.assertIn(f"| `BUNDLE_VERSION` | `{bundle_version}` |", project)

        adopt_doc = (
            self.target / ".lsi" / "workflows" / "adopt-and-update.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn("{{BUNDLE_VERSION}}", adopt_doc)
        self.assertIn(f"v{bundle_version}", adopt_doc)


if __name__ == "__main__":
    unittest.main()
