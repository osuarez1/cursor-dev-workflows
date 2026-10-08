#!/usr/bin/env python3
"""Install local agent stacks for bundle maintainers.

Copies slash commands from overlays/lsi/agent-stack/commands/ with path rewrites
for the bundle repo layout into:

- `.cursor/commands/` (gitignored)
- `.claude/commands/` (tracked dogfood)
- `.opencode/commands/lsi-*.md` (gitignored) — **bundle special case**

Adopters enable OpenCode via patch `agents_opencode: { enabled: true }`. This
repo is not adopted onto itself, so bootstrap always emits OpenCode LSI commands
here for local OpenCode dogfooding.

Re-run after overlay command changes:

    ./snippets/bootstrap-maintainer-local.sh
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

_SNIPPETS = Path(__file__).resolve().parent
if str(_SNIPPETS) not in sys.path:
    sys.path.insert(0, str(_SNIPPETS))

from agent_emit import (  # noqa: E402
    claude_frontmatter,
    claude_subdir,
    opencode_bind_arguments,
    opencode_frontmatter,
)

BUNDLE_ROOT = Path(__file__).resolve().parents[1]
OVERLAY_COMMANDS = BUNDLE_ROOT / "overlays" / "lsi" / "agent-stack" / "commands"
OVERLAY_RULES = BUNDLE_ROOT / "overlays" / "lsi" / "agent-stack"
MAINTAINER_RULES = BUNDLE_ROOT / "snippets" / "maintainer-local" / "rules"
CURSOR_RULES_SNIPPETS = BUNDLE_ROOT / "snippets" / "cursor-rules"
BOT_PERMISSIONS = (
    BUNDLE_ROOT / "overlays" / "lsi" / "agent-stack" / "bot-permissions.json"
)
CURSOR_COMMANDS = BUNDLE_ROOT / ".cursor" / "commands"
CURSOR_RULES = BUNDLE_ROOT / ".cursor" / "rules"
CLAUDE_COMMANDS = BUNDLE_ROOT / ".claude" / "commands"
OPENCODE_COMMANDS = BUNDLE_ROOT / ".opencode" / "commands"
OPENCODE_JSON = BUNDLE_ROOT / "opencode.json"

# Overlay commands use paths relative to overlays/lsi/agent-stack/commands/.
# From .cursor/commands/ at repo root, rewrite LSI-only and template paths.
COMMAND_REWRITES: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(r"\]\(\.\./\.\./docs/sdlc/"),
        "](../../overlays/lsi/docs/sdlc/",
    ),
    (
        re.compile(r"\]\(\.\./\.\./docs/workflows/openspec-git-integration\.md"),
        "](../../overlays/lsi/docs/workflows/openspec-git-integration.md",
    ),
    (
        re.compile(r"\]\(\.\./\.\./docs/workflows/versioning-and-releases\.md"),
        "](../../overlays/lsi/docs/workflows/versioning-and-releases.md",
    ),
    (
        re.compile(r"\]\(\.\./\.\./docs/workflows/templates/"),
        "](../../templates/",
    ),
    (
        re.compile(r"`docs/workflows/openspec-git-integration\.md`"),
        "`overlays/lsi/docs/workflows/openspec-git-integration.md`",
    ),
    (
        re.compile(r"`docs/workflows/versioning-and-releases\.md`"),
        "`overlays/lsi/docs/workflows/versioning-and-releases.md`",
    ),
    (
        re.compile(r"\[docs/workflows/openspec-git-integration\.md\]"),
        "[overlays/lsi/docs/workflows/openspec-git-integration.md]",
    ),
]


def transform_command(text: str) -> str:
    for pattern, repl in COMMAND_REWRITES:
        text = pattern.sub(repl, text)
    return text


def install_commands() -> int:
    """Install LSI slash commands to .cursor/commands/ (OpenSpec commands excluded)."""
    if not OVERLAY_COMMANDS.is_dir():
        print(f"Missing overlay commands: {OVERLAY_COMMANDS}", file=sys.stderr)
        return 1
    CURSOR_COMMANDS.mkdir(parents=True, exist_ok=True)
    count = 0
    for src in sorted(OVERLAY_COMMANDS.glob("lsi-*.md")):
        content = transform_command(src.read_text(encoding="utf-8"))
        (CURSOR_COMMANDS / src.name).write_text(content, encoding="utf-8")
        count += 1
    print(f"Installed {count} slash commands → .cursor/commands/")
    return 0


def install_claude_commands() -> int:
    """Generate .claude/commands/lsi/ from LSI overlay sources (tracked in bundle git).

    OpenSpec (`opsx-*`) commands are owned by OpenSpec and not generated here.
    """
    if not OVERLAY_COMMANDS.is_dir():
        print(f"Missing overlay commands: {OVERLAY_COMMANDS}", file=sys.stderr)
        return 1
    count = 0
    for src in sorted(OVERLAY_COMMANDS.glob("lsi-*.md")):
        raw = src.read_text(encoding="utf-8")
        content = claude_frontmatter(transform_command(raw))
        subdir, name = claude_subdir(src.stem)
        dst_dir = CLAUDE_COMMANDS / subdir if subdir else CLAUDE_COMMANDS
        dst_dir.mkdir(parents=True, exist_ok=True)
        (dst_dir / f"{name}.md").write_text(content, encoding="utf-8")
        count += 1
    print(f"Installed {count} Claude commands → .claude/commands/")
    return 0


def install_opencode_commands() -> int:
    """Emit LSI commands for OpenCode (bundle-maintainer special case; gitignored)."""
    if not OVERLAY_COMMANDS.is_dir():
        print(f"Missing overlay commands: {OVERLAY_COMMANDS}", file=sys.stderr)
        return 1
    OPENCODE_COMMANDS.mkdir(parents=True, exist_ok=True)
    count = 0
    index_lines = [
        "# OpenCode LSI commands (bundle maintainer)",
        "",
        "This repo enables OpenCode as a **special case** via "
        "`./snippets/bootstrap-maintainer-local.sh` (not `agents_opencode` adopt).",
        "OpenSpec `opsx-*` commands may also live under `.opencode/commands/`.",
        "",
        "## LSI commands",
        "",
    ]
    for src in sorted(OVERLAY_COMMANDS.glob("lsi-*.md")):
        content = transform_command(src.read_text(encoding="utf-8"))
        content = opencode_frontmatter(content)
        content = opencode_bind_arguments(content)
        (OPENCODE_COMMANDS / src.name).write_text(content, encoding="utf-8")
        slash = "/" + src.stem.replace("lsi-", "lsi:", 1)
        index_lines.append(f"- `{slash}` → `.opencode/commands/{src.name}`")
        count += 1
    index_lines.append("")
    (BUNDLE_ROOT / ".opencode" / "LSI.md").write_text(
        "\n".join(index_lines), encoding="utf-8"
    )
    print(f"Installed {count} OpenCode LSI commands → .opencode/commands/")
    return 0


def merge_opencode_bot_permissions_local() -> None:
    """Idempotent merge of bot bash allows into gitignored `opencode.json`."""
    if not BOT_PERMISSIONS.is_file():
        return
    perms = json.loads(BOT_PERMISSIONS.read_text(encoding="utf-8"))
    bash_allows: dict[str, str] = dict(perms["opencode"]["permission_bash"])
    data: dict = {}
    if OPENCODE_JSON.is_file():
        raw = json.loads(OPENCODE_JSON.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            data = raw
    permission = data.setdefault("permission", {})
    if not isinstance(permission, dict):
        permission = {}
        data["permission"] = permission
    bash = permission.get("bash")
    if bash is None or isinstance(bash, str):
        bash = {} if bash is None else {"*": bash}
        permission["bash"] = bash
    if not isinstance(bash, dict):
        bash = {}
        permission["bash"] = bash
    for pattern, effect in bash_allows.items():
        bash[pattern] = effect
    OPENCODE_JSON.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("Merged bot permissions → opencode.json")


def install_rules() -> int:
    CURSOR_RULES.mkdir(parents=True, exist_ok=True)

    commit_pr = CURSOR_RULES_SNIPPETS / "commit-pr-conventions.mdc"
    if commit_pr.is_file():
        shutil.copy2(commit_pr, CURSOR_RULES / "commit-pr-conventions.mdc")
        print("Installed commit-pr-conventions.mdc → .cursor/rules/")

    if MAINTAINER_RULES.is_dir():
        for src in sorted(MAINTAINER_RULES.glob("*.mdc")):
            shutil.copy2(src, CURSOR_RULES / src.name)
        print(f"Installed {len(list(MAINTAINER_RULES.glob('*.mdc')))} maintainer rules → .cursor/rules/")

    return 0


def main() -> int:
    code = install_commands()
    if code:
        return code
    code = install_claude_commands()
    if code:
        return code
    code = install_opencode_commands()
    if code:
        return code
    merge_opencode_bot_permissions_local()
    return install_rules()


if __name__ == "__main__":
    raise SystemExit(main())
