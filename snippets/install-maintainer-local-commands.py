#!/usr/bin/env python3
"""Install gitignored maintainer slash commands and local rules into the bundle repo."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SNIPPETS = Path(__file__).resolve().parent
BUNDLE_ROOT = SNIPPETS.parent
OVERLAY = BUNDLE_ROOT / "overlays" / "lsi"
AGENT_STACK = OVERLAY / "agent-stack"

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
    (re.compile(r"\]\(\.\./workflows/"), "](../",),
    (re.compile(r"\]\(\.\./sdlc/"), "](sdlc/"),
    (re.compile(r"\]\(\.\./\.\./sdlc/"), "](sdlc/"),
    (re.compile(r"\]\(\.\./ai/"), "](../docs/ai/"),
    (re.compile(r"\]\(\.\./deployment/"), "](../../docs/deployment/"),
]


def substitute_tokens(text: str, tokens: dict[str, str]) -> str:
    for key, value in tokens.items():
        text = text.replace(f"{{{{{key}}}}}", value)
    protected = tokens.get("PROTECTED_BRANCHES", "main")
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
    text = text.replace("](adoption-checklist.md)", "](docs/adopt-and-update.md)")
    text = text.replace("](../../adoption-checklist.md)", "](docs/adopt-and-update.md)")
    return text


OVERLAY_ONLY_WORKFLOWS = {
    "branch-reviewability.md",
    "openspec-git-integration.md",
    "versioning-and-releases.md",
}


def bundle_workflow_href(name: str) -> str:
    """Repo-root-relative path for a workflow spec in the bundle source tree."""
    if name in OVERLAY_ONLY_WORKFLOWS:
        return f"overlays/lsi/docs/workflows/{name}"
    core = BUNDLE_ROOT / "docs" / "workflows" / name
    if core.is_file():
        return f"docs/workflows/{name}"
    overlay = OVERLAY / "docs" / "workflows" / name
    if overlay.is_file():
        return f"overlays/lsi/docs/workflows/{name}"
    return f"docs/workflows/{name}"


def bundle_workflow_link_from_rules(name: str) -> str:
    """Relative path from .cursor/rules/ to a workflow spec."""
    href = bundle_workflow_href(name)
    return f"../../{href}"


def maintainer_tokens() -> dict[str, str]:
    return {
        "REPO_NAME": "cursor-dev-workflows",
        "TITLE_PREFIX": "Bundle | ",
        "BASE_BRANCH": "main",
        "PR_TARGET_BRANCH": "main",
        "PROTECTED_BRANCHES": "main",
        "SOURCE_ROOT": "docs/, overlays/, snippets/, templates/, examples/",
        "TEST_ROOT": "snippets/",
        "TEST_COMMAND": "python3 snippets/test_adoption_verify_links.py",
        "PR_HOST": "GitHub",
        "BITBUCKET_REMOTE": "",
        "VERSION_FILE": "VERSION",
    }


def rewrite_lsi_workflow_paths(text: str) -> str:
    for name in WORKFLOW_ROOT_MD:
        bundle_href = bundle_workflow_href(name)
        rules_href = bundle_workflow_link_from_rules(name)
        text = text.replace(f".lsi/workflows/{name}", bundle_href)
        text = text.replace(f"../../.lsi/workflows/{name}", rules_href)
    text = text.replace(".lsi/workflows/", "docs/workflows/")
    text = text.replace("../../.lsi/workflows/", "../../docs/workflows/")
    return text


def rewrite_command_file_links(text: str) -> str:
    """Adjust markdown links for paths relative to .cursor/commands/."""
    prefix = "../../"
    for name in WORKFLOW_ROOT_MD:
        href = bundle_workflow_href(name)
        text = re.sub(
            rf"\]\({re.escape(name)}\)",
            f"]({prefix}{href})",
            text,
        )
    text = re.sub(
        r"\]\(sdlc/([^)]+)\)",
        rf"]({prefix}overlays/lsi/docs/sdlc/\1)",
        text,
    )
    text = text.replace("](PROJECT.md)", "](../../PROJECT.md)")
    text = text.replace("](adoption-checklist.md)", "](../../adoption-checklist.md)")
    return text


def rewrite_maintainer_content(text: str, *, from_rules: bool = False) -> str:
    text = substitute_tokens(text, maintainer_tokens())
    text = rewrite_lsi_workflow_paths(text)
    text = text.replace("../../docs/sdlc/", "../../overlays/lsi/docs/sdlc/")
    text = text.replace("](sdlc/", "](overlays/lsi/docs/sdlc/")
    text = rewrite_links(text)
    if from_rules:
        text = text.replace(
            "](branch-workflow.mdc)",
            "](local-branch-workflow.mdc)",
        )
    else:
        text = rewrite_command_file_links(text)
    return text


def resolve_commands_source() -> Path | None:
    candidates = [
        AGENT_STACK / "commands",
        SNIPPETS / "maintainer-local" / "commands",
        BUNDLE_ROOT.parent / "video-encoder" / ".cursor" / "commands",
        BUNDLE_ROOT.parent / "web" / ".cursor" / "commands",
    ]
    for path in candidates:
        if path.is_dir() and any(path.glob("lsi-*.md")):
            return path
    return None


def install_commands(target_commands: Path) -> int:
    src_dir = resolve_commands_source()
    if src_dir is None:
        print(
            "WARN: no command source (need overlays/lsi/agent-stack/commands "
            "or sibling adopter .cursor/commands/)",
            file=sys.stderr,
        )
        return 1
    target_commands.mkdir(parents=True, exist_ok=True)
    for cmd in sorted(src_dir.glob("*.md")):
        if not (cmd.name.startswith("lsi-") or cmd.name.startswith("opsx-")):
            continue
        content = rewrite_maintainer_content(cmd.read_text(encoding="utf-8"))
        (target_commands / cmd.name).write_text(content, encoding="utf-8")
    count = len(list(target_commands.glob("*.md")))
    print(f"Installed {count} commands from {src_dir} → {target_commands}")
    return 0 if count else 1


def install_local_rules(target_rules: Path) -> int:
    target_rules.mkdir(parents=True, exist_ok=True)
    template_dir = SNIPPETS / "maintainer-local"
    mapping: dict[str, Path] = {
        "local-maintainer.mdc": template_dir / "local-maintainer.mdc.example",
        "local-branch-workflow.mdc": template_dir / "local-branch-workflow.mdc.example",
        "local-openspec-git-integration.mdc": (
            template_dir / "local-openspec-git-integration.mdc.example"
        ),
    }
    overlay_rules = {
        "local-branch-workflow.mdc": AGENT_STACK / "branch-workflow.mdc",
        "local-openspec-git-integration.mdc": AGENT_STACK / "openspec-git-integration.mdc",
    }
    for dest_name, default_src in mapping.items():
        src = overlay_rules.get(dest_name)
        if src is not None and src.is_file():
            content = rewrite_maintainer_content(
                src.read_text(encoding="utf-8"), from_rules=True
            )
        elif default_src.is_file():
            content = default_src.read_text(encoding="utf-8")
        else:
            print(f"Skip missing rule template {dest_name}", file=sys.stderr)
            continue
        (target_rules / dest_name).write_text(content, encoding="utf-8")
    print(f"Installed local rules → {target_rules}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Install maintainer-local Cursor assets.")
    parser.add_argument(
        "--bundle-root",
        type=Path,
        default=BUNDLE_ROOT,
        help="cursor-dev-workflows root",
    )
    parser.add_argument("--commands-only", action="store_true")
    parser.add_argument("--rules-only", action="store_true")
    args = parser.parse_args(argv)

    root = args.bundle_root.resolve()
    commands = root / ".cursor" / "commands"
    rules = root / ".cursor" / "rules"

    code = 0
    if not args.rules_only:
        code = install_commands(commands) or code
    if not args.commands_only:
        code = install_local_rules(rules) or code
    return code


if __name__ == "__main__":
    sys.exit(main())
