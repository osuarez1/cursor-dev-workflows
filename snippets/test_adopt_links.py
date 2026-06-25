"""End-to-end adopt → verify link regression tests.

Most cases call adopt helpers directly, then invoke ``verify()`` with optional
``extra_dirs`` (e.g. ``docs/ai`` cross-tree links). That keeps bundle-only scan
scopes explicit and avoids subprocess overhead on every test method.

``test_adopt_entry_point_runs_post_adopt_verify`` calls ``adopt(...,
skip_audit=True)`` once to exercise the full adopt pipeline and the built-in
post-adopt ``adoption-verify-links.py`` hook (pre-adopt audit is skipped on
minimal temp fixtures; post-adopt audit INFO findings are non-blocking).
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
        """Core adopt transforms only — link assertions call ``verify()`` directly."""
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

    def test_adopt_entry_point_runs_post_adopt_verify(self) -> None:
        code = adopt.adopt(self.target, self.config_path, skip_audit=True)
        self.assertEqual(code, 0)

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


    def _adopt_commands(self, repo_name: str, test_cmd: str, source_root: str, protected: str) -> dict[str, str]:
        """Adopt into a temp dir and return {filename: content} for lsi-*.md commands."""
        cfg_text = (
            f"repo: {repo_name}\n"
            "overlay: lsi\n"
            "layout: lsi\n"
            "canonical: .lsi/workflows\n"
            "project:\n"
            f"  REPO_NAME: {repo_name}\n"
            f"  TEST_COMMAND: \"{test_cmd}\"\n"
            "  BASE_BRANCH: main\n"
            f"  PROTECTED_BRANCHES: \"{protected}\"\n"
            f"  SOURCE_ROOT: \"{source_root}\"\n"
            f"  TITLE_PREFIX: \"X | \"\n"
            "  PR_HOST: Bitbucket\n"
            f"  BITBUCKET_REMOTE: lsi/{repo_name}\n"
            "  PR_WARN_FILES: \"15\"\n"
            "  PR_MAX_FILES: \"25\"\n"
            "  PR_WARN_LINES: \"250\"\n"
            "  PR_MAX_LINES: \"400\"\n"
            "  PR_MAX_COMMITS: \"12\"\n"
            "  PR_MAX_PRIMARY_CONCERNS: \"1\"\n"
            "  PR_MAX_SCOPES: \"3\"\n"
            "bootstrap:\n"
            "  version.txt: \"0.1.0\"\n"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir)
            cfg_path = target / "patch.yaml"
            cfg_path.write_text(cfg_text, encoding="utf-8")
            (target / "PROJECT.md").write_text("# stub\n", encoding="utf-8")
            seed_link_targets(target)
            config = adopt.load_config(cfg_path)
            bundle_version = (BUNDLE_ROOT / "VERSION").read_text(encoding="utf-8").strip()
            tokens = {**adopt.build_tokens(config), "BUNDLE_VERSION": bundle_version}
            adopt.copy_core_bundle(target, tokens)
            adopt.copy_overlay(target, tokens, config)
            adopt.install_agent_stack(target, tokens, config)
            cmds_dir = target / ".cursor" / "commands"
            return {
                p.name: p.read_text(encoding="utf-8")
                for p in sorted(cmds_dir.glob("lsi-*.md"))
            }

    def test_lsi_commands_byte_identical_across_repos(self) -> None:
        """lsi-*.md commands are byte-identical regardless of per-repo project tokens."""
        adopted = {
            "repo-rails": self._adopt_commands("repo-rails", "bin/check && bin/rspec", "app/, lib/", "main, staging, master"),
            "repo-python": self._adopt_commands("repo-python", "pytest", "src/", "main, staging"),
            "repo-make": self._adopt_commands("repo-make", "make test", "frontend/, backend/", "main"),
        }
        base_name, base_cmds = "repo-rails", adopted["repo-rails"]
        diffs: list[str] = []
        for other_name, other_cmds in adopted.items():
            if other_name == base_name:
                continue
            for fname in sorted(set(base_cmds) | set(other_cmds)):
                if base_cmds.get(fname) != other_cmds.get(fname):
                    diffs.append(f"{fname}: differs between {base_name!r} and {other_name!r}")
        self.assertEqual(diffs, [], msg="\n".join(diffs))

    def test_adopted_commands_have_no_domain_strings(self) -> None:
        """After adoption, lsi-*.md commands contain no repo-specific domain strings."""
        domain_strings = [
            "FFmpeg", "fastapi", "FastAPI", "rspec", "pytest",
            "make test", "bin/check-schema-sync", "uv run pytest",
        ]
        self.run_adopt()
        cmds_dir = self.target / ".cursor" / "commands"
        hits: list[str] = []
        for md in sorted(cmds_dir.glob("lsi-*.md")):
            text = md.read_text(encoding="utf-8")
            for needle in domain_strings:
                if needle in text:
                    hits.append(f"{md.name}: contains {needle!r}")
        self.assertEqual(hits, [], msg="\n".join(hits))


if __name__ == "__main__":
    unittest.main()
