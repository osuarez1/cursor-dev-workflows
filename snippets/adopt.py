#!/usr/bin/env python3
"""Adopt cursor-dev-workflows into an application repo (.lsi/workflows/ layout)."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

def _load_yaml_text(text: str):
  """Minimal YAML loader for patch files (stdlib only)."""
  try:
      import yaml  # type: ignore

      return yaml.safe_load(text) or {}
  except ImportError:
      pass
  except Exception:
      pass
  return _load_simple_yaml(text)


def _load_simple_yaml(text: str) -> dict:
    """Parse simple nested dict/list YAML used by patches/*.yaml."""
    root: dict = {}
    stack: list[tuple[int, object]] = [(-1, root)]
    key_re = re.compile(r"^(\s*)(\w+):\s*(.*)$")
    list_re = re.compile(r"^(\s*)-\s+(.*)$")

    for raw in text.splitlines():
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        m = key_re.match(raw)
        if m:
            indent, key, rest = len(m.group(1)), m.group(2), m.group(3).strip()
            while stack and indent <= stack[-1][0]:
                stack.pop()
            parent = stack[-1][1]
            if not isinstance(parent, dict):
                raise ValueError(f"Invalid YAML near key {key}")
            if rest == "":
                value: object = {}
                parent[key] = value
                stack.append((indent, value))
            elif rest.startswith("[") and rest.endswith("]"):
                inner = rest[1:-1].strip()
                parent[key] = (
                    [x.strip() for x in inner.split(",") if x.strip()] if inner else []
                )
            elif rest in ("true", "false"):
                parent[key] = rest == "true"
            else:
                parent[key] = rest.strip("'\"")
            continue
        m = list_re.match(raw)
        if m:
            indent, item = len(m.group(1)), m.group(2).strip()
            while stack and indent <= stack[-1][0]:
                stack.pop()
            parent = stack[-1][1]
            value = item.strip("'\"")
            if isinstance(parent, list):
                parent.append(value)
                stack.append((indent, parent))
                continue
            if isinstance(parent, dict):
                # Patch YAML uses one list key per indented block; append to the most recent list value.
                for v in reversed(list(parent.values())):
                    if isinstance(v, list):
                        v.append(value)
                        break
                else:
                    for k, v in parent.items():
                        if isinstance(v, dict) and not v:
                            lst: list = [value]
                            parent[k] = lst
                            stack.append((indent, lst))
                            break
            continue
    return root

BUNDLE_ROOT = Path(__file__).resolve().parents[1]
OVERLAY_ROOT = BUNDLE_ROOT / "overlays" / "lsi"
AUDIT_SCRIPT = BUNDLE_ROOT / "snippets" / "audit-agent-docs.py"
VERIFY_SCRIPT = BUNDLE_ROOT / "snippets" / "adoption-verify-links.py"

WORKFLOW_ROOT_MD = {
    "branch-workflow.md",
    "branch-reviewability.md",
    "code-review.md",
    "commits-logical-order.md",
    "common-mistakes.md",
    "integrations.md",
    "openspec-git-integration.md",
    "pr-production-readiness.md",
    "pull-requests.md",
    "senior-analysis.md",
    "test-requirements.md",
    "ticket-card-info.md",
    "versioning-and-releases.md",
    "which-workflow.md",
}

LINK_REWRITES = [
    (re.compile(r"\]\(\.\./\.\./docs/workflows/"), "](",),
    (re.compile(r"\]\(\.\./docs/workflows/"), "](",),
    (re.compile(r"\]\(docs/workflows/"), "](",),
    (re.compile(r"\]\(\.\./\.\./which-workflow\.md\)"), "](which-workflow.md)"),
    (re.compile(r"\]\(\.\./\.\./PROJECT\.md\)"), "](../../PROJECT.md)"),
    (re.compile(r"\]\(\.\./\.\./templates/"), "](templates/",),
    (re.compile(r"\]\(\.\./\.\./examples/"), "](examples/",),
    (re.compile(r"\]\(\.\./templates/"), "](templates/",),
    (re.compile(r"\]\(\.\./examples/"), "](examples/",),
    (re.compile(r"\]\(\.\./\.\./snippets/"), "](../../snippets/",),
    (re.compile(r"\]\(\.\./\.\./adoption-checklist\.md\)"), "](../../adoption-checklist.md)"),
    (re.compile(r"\]\(\.\./\.\./CHANGELOG\.md\)"), "](../../CHANGELOG.md)"),
    (re.compile(r"\]\(\.\./workflows/"), "](../",),
    (re.compile(r"\]\(\.\./sdlc/"), "](sdlc/"),
    (re.compile(r"\]\(\.\./\.\./sdlc/"), "](sdlc/"),
    (re.compile(r"\]\(\.\./ai/"), "](../docs/ai/"),
    (re.compile(r"\]\(\.\./deployment/"), "](../../docs/deployment/"),
]


def load_config(path: Path) -> dict:
    data = _load_yaml_text(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"Invalid config (expected mapping): {path}")
    return data


def run_script(script: Path, *args: str) -> int:
    result = subprocess.run(
        [sys.executable, str(script), *args],
        cwd=BUNDLE_ROOT,
    )
    return result.returncode


def substitute_tokens(text: str, tokens: dict[str, str]) -> str:
    for key, value in tokens.items():
        text = text.replace(f"{{{{{key}}}}}", value)
    protected = tokens.get("PROTECTED_BRANCHES", "main, staging")
    bullets = "\n".join(f"- `{b.strip()}`" for b in protected.split(",") if b.strip())
    text = text.replace("{{PROTECTED_BRANCHES}}", protected)
    text = text.replace("{{PROTECTED_BRANCHES_BULLETS}}", bullets)
    return text


def rewrite_links(text: str, *, in_subdir: str | None = None) -> str:
    for pattern, repl in LINK_REWRITES:
        text = pattern.sub(repl, text)
    if in_subdir in ("examples", "templates"):
        prefix = "../"

        def bump_spec_link(match: re.Match[str]) -> str:
            href = match.group(1)
            if href.startswith(("http://", "https://", "mailto:")):
                return match.group(0)
            if href.startswith("examples/"):
                return f"]({prefix}{href})"
            if "/" not in href and not href.startswith(".") and href in WORKFLOW_ROOT_MD:
                return f"]({prefix}{href})"
            return match.group(0)

        text = re.sub(r"\]\(([^)#]+)\)", bump_spec_link, text)
    text = text.replace("](adoption-checklist.md)", "](adopt-and-update.md)")
    text = text.replace("](../../adoption-checklist.md)", "](adopt-and-update.md)")
    text = re.sub(
        r"\]\(\.\./\.\./snippets/[^)]+\)",
        "](adopt-and-update.md)",
        text,
    )
    return text


def copy_tree(src: Path, dst: Path, transform=None) -> None:
    if not src.exists():
        return
    if src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        content = src.read_text(encoding="utf-8")
        if transform:
            content = transform(content)
        dst.write_text(content, encoding="utf-8")
        return
    for item in sorted(src.rglob("*")):
        if item.is_dir():
            continue
        rel = item.relative_to(src)
        out = dst / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        content = item.read_text(encoding="utf-8")
        if transform:
            sub: str | None = None
            dst_parts = out.parts
            if "examples" in dst_parts:
                sub = "examples"
            elif "templates" in dst_parts:
                sub = "templates"
            if sub:
                content = transform(content, in_subdir=sub)
            else:
                content = transform(content)
        out.write_text(content, encoding="utf-8")


def wipe_lsi_workflows(target: Path) -> None:
    lsi = target / ".lsi" / "workflows"
    if lsi.exists():
        shutil.rmtree(lsi)


def copy_core_bundle(target: Path, tokens: dict[str, str]) -> None:
    lsi = target / ".lsi" / "workflows"
    lsi.mkdir(parents=True, exist_ok=True)

    def transform(content: str, in_subdir: str | None = None) -> str:
        text = substitute_tokens(content, tokens)
        return rewrite_links(text, in_subdir=in_subdir)

    for md in sorted((BUNDLE_ROOT / "docs" / "workflows").glob("*.md")):
        path = lsi / md.name
        path.write_text(transform(md.read_text(encoding="utf-8")), encoding="utf-8")

    for name in ("which-workflow.md",):
        src = BUNDLE_ROOT / name
        if src.is_file():
            (lsi / name).write_text(transform(src.read_text(encoding="utf-8")), encoding="utf-8")

    copy_tree(BUNDLE_ROOT / "templates", lsi / "templates", transform)
    copy_tree(BUNDLE_ROOT / "examples", lsi / "examples", transform)

    adopt_guide = BUNDLE_ROOT / "docs" / "adopt-and-update.md"
    if adopt_guide.is_file():
        (lsi / "adopt-and-update.md").write_text(
            transform(adopt_guide.read_text(encoding="utf-8")), encoding="utf-8"
        )


def copy_overlay(target: Path, tokens: dict[str, str], config: dict) -> None:
    lsi = target / ".lsi" / "workflows"

    def transform(content: str) -> str:
        return rewrite_links(substitute_tokens(content, tokens))

    overlay_docs = OVERLAY_ROOT / "docs" / "workflows"
    if overlay_docs.is_dir():
        for md in overlay_docs.glob("*.md"):
            (lsi / md.name).write_text(
                transform(md.read_text(encoding="utf-8")), encoding="utf-8"
            )

    sdlc_src = OVERLAY_ROOT / "docs" / "sdlc"
    if sdlc_src.is_dir():
        copy_tree(sdlc_src, lsi / "sdlc", transform)

    ai_src = OVERLAY_ROOT / "docs" / "ai"
    if ai_src.is_dir():
        copy_tree(ai_src, target / "docs" / "ai", transform)

    for rel, src_rel in (config.get("overlay_files") or {}).items():
        src = BUNDLE_ROOT / src_rel
        if src.is_file():
            out = lsi / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(transform(src.read_text(encoding="utf-8")), encoding="utf-8")

    release_dst = target / "scripts" / "release"
    release_dst.mkdir(parents=True, exist_ok=True)
    for py in (OVERLAY_ROOT / "snippets" / "release").glob("*.py"):
        if py.name == "check_version.py":
            continue
        shutil.copy2(py, release_dst / py.name)

    check_src = OVERLAY_ROOT / "snippets" / "release" / "check_version.py"
    scripts = target / "scripts"
    scripts.mkdir(parents=True, exist_ok=True)
    if check_src.is_file():
        shutil.copy2(check_src, scripts / "check_version.py")


def merge_which_workflow_lsi(target: Path) -> None:
    lsi_router = target / ".lsi" / "workflows" / "which-workflow.md"
    lsi_ext = OVERLAY_ROOT / "which-workflow-lsi.md"
    if not lsi_router.is_file() or not lsi_ext.is_file():
        return
    # Overlay router from video-encoder is richer — prefer VE copy if present in overlay
    ve_router = OVERLAY_ROOT / "docs" / "workflows" / "which-workflow.md"
    if ve_router.is_file():
        lsi_router.write_text(
            rewrite_links(ve_router.read_text(encoding="utf-8")),
            encoding="utf-8",
        )


def install_agent_stack(target: Path, tokens: dict[str, str], config: dict) -> None:
    rules_dir = target / ".cursor" / "rules"
    cmds_dir = target / ".cursor" / "commands"
    rules_dir.mkdir(parents=True, exist_ok=True)
    cmds_dir.mkdir(parents=True, exist_ok=True)

    for mdc in (
        "branch-workflow.mdc",
        "openspec-git-integration.mdc",
        "commit-pr-conventions.mdc",
    ):
        src = OVERLAY_ROOT / "agent-stack" / mdc
        if src.is_file():
            content = substitute_tokens(src.read_text(encoding="utf-8"), tokens)
            (rules_dir / mdc).write_text(content, encoding="utf-8")

    sync_opsx = config.get("sync_opsx", False)
    for cmd in sorted((OVERLAY_ROOT / "agent-stack" / "commands").glob("*.md")):
        if cmd.name.startswith("opsx-") and not sync_opsx:
            dst = cmds_dir / cmd.name
            if dst.exists():
                continue
        content = substitute_tokens(cmd.read_text(encoding="utf-8"), tokens)
        content = content.replace("docs/workflows/", ".lsi/workflows/")
        content = content.replace("../../docs/sdlc/", "../../.lsi/workflows/sdlc/")
        content = rewrite_links(content)
        (cmds_dir / cmd.name).write_text(content, encoding="utf-8")

    cursor_rules = BUNDLE_ROOT / "snippets" / "cursor-rules"
    if cursor_rules.is_dir():
        for mdc in cursor_rules.glob("*.mdc"):
            if mdc.name in {
                "commit-pr-conventions.mdc",
                "openspec-git-integration.mdc",
            }:
                continue
            content = rewrite_links(
                substitute_tokens(mdc.read_text(encoding="utf-8"), tokens)
            )
            content = content.replace("CANONICAL_DOCS_PATH", ".lsi/workflows")
            (rules_dir / mdc.name).write_text(content, encoding="utf-8")


def merge_convention(target: Path) -> None:
    conv = target / "CONVENTION.md"
    template = OVERLAY_ROOT / "agent-stack" / "CONVENTION.commits.template"
    if not template.is_file():
        return
    block = template.read_text(encoding="utf-8")
    if conv.is_file():
        text = conv.read_text(encoding="utf-8")
        if "<!-- lsi:commits:start -->" in text:
            text = re.sub(
                r"<!-- lsi:commits:start -->.*?<!-- lsi:commits:end -->",
                block.strip(),
                text,
                flags=re.DOTALL,
            )
        else:
            text = text.rstrip() + "\n\n" + block + "\n"
        conv.write_text(text, encoding="utf-8")
    else:
        conv.write_text("# Conventions\n\n" + block + "\n", encoding="utf-8")


def merge_agents_markers(target: Path) -> None:
    agents = target / "AGENTS.md"
    template = OVERLAY_ROOT / "agent-stack" / "AGENTS.workflow.md.template"
    if not template.is_file():
        return
    block = template.read_text(encoding="utf-8")
    if agents.is_file():
        text = agents.read_text(encoding="utf-8")
        if "<!-- lsi:workflows:start -->" in text:
            text = re.sub(
                r"<!-- lsi:workflows:start -->.*?<!-- lsi:workflows:end -->",
                block.strip(),
                text,
                flags=re.DOTALL,
            )
        else:
            text = text.rstrip() + "\n\n<!-- lsi:workflows:start -->\n" + block + "\n<!-- lsi:workflows:end -->\n"
        agents.write_text(text, encoding="utf-8")
    else:
        agents.write_text(
            "# Agent Guide\n\n<!-- lsi:workflows:start -->\n"
            + block
            + "\n<!-- lsi:workflows:end -->\n",
            encoding="utf-8",
        )


def merge_cursorrules(target: Path) -> None:
    cr = target / ".cursorrules"
    template = OVERLAY_ROOT / "agent-stack" / "cursorrules.workflow.template"
    if not template.is_file():
        return
    block = template.read_text(encoding="utf-8")
    if cr.is_file():
        text = cr.read_text(encoding="utf-8")
        if "<!-- lsi:workflows:start -->" in text:
            text = re.sub(
                r"<!-- lsi:workflows:start -->.*?<!-- lsi:workflows:end -->",
                block.strip(),
                text,
                flags=re.DOTALL,
            )
        else:
            text = text.rstrip() + "\n\n" + block + "\n"
        cr.write_text(text, encoding="utf-8")
    else:
        cr.write_text(block + "\n", encoding="utf-8")


def reconcile_agents_before_symlink(target: Path, config: dict) -> None:
    """If CLAUDE.md is a regular file, preserve its text before symlink replaces it."""
    agents_cfg = config.get("agents_claude") or {}
    if not agents_cfg.get("claude_symlink", True):
        return
    claude = target / "CLAUDE.md"
    backup = target / ".adopt-claude-backup.md"
    if claude.is_file() and not claude.is_symlink():
        backup.write_text(claude.read_text(encoding="utf-8"), encoding="utf-8")
        # Reconcile hook: maintainer merges backup into AGENTS.md domain block manually
        # or via patches/files/<repo>/AGENTS.domain.md overlay on future adopt runs.


def symlink_claude(target: Path, config: dict) -> None:
    agents_cfg = config.get("agents_claude") or {}
    if not agents_cfg.get("claude_symlink", True):
        return
    agents = target / "AGENTS.md"
    claude = target / "CLAUDE.md"
    if not agents.is_file():
        return
    if claude.exists() or claude.is_symlink():
        claude.unlink(missing_ok=True)
    claude.symlink_to("AGENTS.md")


def update_project_md(target: Path, config: dict, bundle_version: str) -> None:
    project = config.get("project") or {}
    path = target / "PROJECT.md"
    lines: list[str] = []
    if path.is_file():
        lines = path.read_text(encoding="utf-8").splitlines()

    table_tokens = {
        **project,
        "CANONICAL_DOCS_PATH": config.get("canonical", ".lsi/workflows"),
        "ADOPTION_LAYOUT": config.get("layout", "lsi"),
        "BUNDLE_VERSION": bundle_version,
    }

    def upsert_table(existing: list[str]) -> list[str]:
        out: list[str] = []
        seen: set[str] = set()
        in_table = False
        for line in existing:
            m = re.match(r"\|\s*`([A-Z_]+)`\s*\|", line)
            if m:
                in_table = True
                key = m.group(1)
                if key in table_tokens:
                    out.append(f"| `{key}` | `{table_tokens[key]}` |")
                    seen.add(key)
                    continue
            out.append(line)
        if in_table:
            for key, val in sorted(table_tokens.items()):
                if key not in seen:
                    out.append(f"| `{key}` | `{val}` |")
        return out

    if any("| Token |" in l for l in lines):
        lines = upsert_table(lines)
    else:
        lines.append("\n## Adoption tokens\n")
        lines.append("| Token | Value |")
        lines.append("|-------|-------|")
        for key, val in sorted(table_tokens.items()):
            lines.append(f"| `{key}` | `{val}` |")

    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def bootstrap_files(target: Path, config: dict) -> None:
    boot = config.get("bootstrap") or {}
    if "version.txt" in boot and not (target / "version.txt").exists():
        (target / "version.txt").write_text(boot["version.txt"] + "\n", encoding="utf-8")
    version_file = boot.get("VERSION_FILE") or boot.get("version_file")
    if version_file and not (target / version_file).exists():
        ver = boot.get("version", boot.get("VERSION", "0.1.0"))
        (target / version_file).write_text(ver + "\n", encoding="utf-8")


def remove_after_adopt(target: Path, config: dict) -> None:
    for rel in config.get("remove_after_adopt") or []:
        path = target / rel
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)


def build_tokens(config: dict) -> dict[str, str]:
    project = config.get("project") or {}
    return {k: str(v) for k, v in project.items()}


def resolve_audit_resolutions(
    config: dict,
    config_path: Path,
    cli_path: Path | None,
) -> Path | None:
    if cli_path is not None:
        return cli_path.resolve()
    rel = config.get("audit_resolutions")
    if not rel:
        return None
    candidate = Path(rel)
    if candidate.is_file():
        return candidate.resolve()
    bundle_relative = (BUNDLE_ROOT / rel).resolve()
    if bundle_relative.is_file():
        return bundle_relative
    config_relative = (config_path.parent / rel).resolve()
    if config_relative.is_file():
        return config_relative
    return bundle_relative


def audit_cli_args(
    target: Path,
    *,
    accept_resolutions: Path | None = None,
    accept_policy_defaults: bool = False,
) -> list[str]:
    args = ["--repo-root", str(target)]
    if accept_resolutions is not None:
        args.extend(["--accept-resolutions", str(accept_resolutions)])
    if accept_policy_defaults:
        args.append("--accept-policy-defaults")
    return args


def adopt(
    target: Path,
    config_path: Path,
    *,
    dry_run: bool = False,
    skip_audit: bool = False,
    accept_policy_defaults: bool = False,
    accept_resolutions: Path | None = None,
) -> int:
    config = load_config(config_path)
    bundle_version = (BUNDLE_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    tokens = {**build_tokens(config), "BUNDLE_VERSION": bundle_version}
    resolutions = resolve_audit_resolutions(config, config_path, accept_resolutions)

    if not skip_audit and AUDIT_SCRIPT.is_file():
        code = run_script(
            AUDIT_SCRIPT,
            *audit_cli_args(
                target,
                accept_resolutions=resolutions,
                accept_policy_defaults=accept_policy_defaults,
            ),
        )
        if code != 0:
            print(
                "Audit found blocking issues. Fix or re-run with "
                "--accept-policy-defaults / --accept-resolutions after review.",
                file=sys.stderr,
            )
            return code

    if dry_run:
        print(f"DRY RUN: would adopt {config.get('repo', '?')} into {target}")
        return 0

    wipe_lsi_workflows(target)
    copy_core_bundle(target, tokens)
    copy_overlay(target, tokens, config)
    merge_which_workflow_lsi(target)
    install_agent_stack(target, tokens, config)
    merge_convention(target)
    merge_agents_markers(target)
    merge_cursorrules(target)
    reconcile_agents_before_symlink(target, config)
    symlink_claude(target, config)
    update_project_md(target, config, bundle_version)
    bootstrap_files(target, config)
    remove_after_adopt(target, config)

    if VERIFY_SCRIPT.is_file():
        canonical = config.get("canonical", ".lsi/workflows")
        code = run_script(
            VERIFY_SCRIPT,
            "--repo-root",
            str(target),
            "--canonical",
            canonical,
        )
        if code != 0:
            return code

    if AUDIT_SCRIPT.is_file():
        code = run_script(
            AUDIT_SCRIPT,
            *audit_cli_args(
                target,
                accept_resolutions=resolutions,
                accept_policy_defaults=accept_policy_defaults,
            ),
            "--fail-on",
            "error",
        )
        if code != 0:
            print("Post-adopt audit failed.", file=sys.stderr)
            return code

    print(f"Adopted {config.get('repo', target.name)} (bundle {bundle_version})")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Adopt cursor-dev-workflows (LSI layout).")
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--overlay", default="lsi")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--audit-only", action="store_true")
    parser.add_argument("--skip-audit", action="store_true")
    parser.add_argument(
        "--accept-policy-defaults",
        action="store_true",
        help="Continue adopt after audit (known repos only)",
    )
    parser.add_argument("--accept-resolutions", type=Path, default=None)
    args = parser.parse_args(argv)

    if args.overlay != "lsi":
        print("Only --overlay lsi is supported.", file=sys.stderr)
        return 2

    config_path = args.config.resolve()
    config = load_config(config_path)
    resolutions = resolve_audit_resolutions(
        config, config_path, args.accept_resolutions
    )

    if args.audit_only:
        return run_script(
            AUDIT_SCRIPT,
            *audit_cli_args(
                args.target.resolve(),
                accept_resolutions=resolutions,
                accept_policy_defaults=args.accept_policy_defaults,
            ),
        )

    return adopt(
        args.target.resolve(),
        config_path,
        dry_run=args.dry_run,
        skip_audit=args.skip_audit,
        accept_policy_defaults=args.accept_policy_defaults,
        accept_resolutions=args.accept_resolutions,
    )


if __name__ == "__main__":
    sys.exit(main())
