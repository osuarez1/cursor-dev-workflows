#!/usr/bin/env python3
"""Install gitignored .cursor/ stack and tracked .claude/commands/ for bundle maintainers.

Copies slash commands from overlays/lsi/agent-stack/commands/ with path rewrites
for the bundle repo layout. Re-run after overlay command changes:

    ./snippets/bootstrap-maintainer-local.sh
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

BUNDLE_ROOT = Path(__file__).resolve().parents[1]
OVERLAY_COMMANDS = BUNDLE_ROOT / "overlays" / "lsi" / "agent-stack" / "commands"
OVERLAY_RULES = BUNDLE_ROOT / "overlays" / "lsi" / "agent-stack"
MAINTAINER_RULES = BUNDLE_ROOT / "snippets" / "maintainer-local" / "rules"
CURSOR_RULES_SNIPPETS = BUNDLE_ROOT / "snippets" / "cursor-rules"
CURSOR_COMMANDS = BUNDLE_ROOT / ".cursor" / "commands"
CURSOR_RULES = BUNDLE_ROOT / ".cursor" / "rules"
CLAUDE_COMMANDS = BUNDLE_ROOT / ".claude" / "commands"

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

_FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n", re.DOTALL)
_DESCRIPTION_RE = re.compile(r"^description:\s*(.+)$", re.MULTILINE)


def transform_command(text: str) -> str:
    for pattern, repl in COMMAND_REWRITES:
        text = pattern.sub(repl, text)
    return text


def _claude_frontmatter(text: str) -> str:
    """Replace multi-field cursor frontmatter with minimal Claude description-only header."""
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return text
    frontmatter = m.group(0)
    desc_m = _DESCRIPTION_RE.search(frontmatter)
    description = desc_m.group(1).strip() if desc_m else ""
    body = text[m.end():]
    return f"---\ndescription: {description}\n---\n{body}"


def _claude_subdir(stem: str) -> tuple[str, str]:
    """Return (subdir, filename) for a command stem like 'lsi-branch' → ('lsi', 'branch')."""
    if stem.startswith("lsi-"):
        return "lsi", stem[len("lsi-"):]
    return "", stem


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
        content = _claude_frontmatter(transform_command(raw))
        subdir, name = _claude_subdir(src.stem)
        dst_dir = CLAUDE_COMMANDS / subdir if subdir else CLAUDE_COMMANDS
        dst_dir.mkdir(parents=True, exist_ok=True)
        (dst_dir / f"{name}.md").write_text(content, encoding="utf-8")
        count += 1
    print(f"Installed {count} Claude commands → .claude/commands/")
    return 0


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
    return install_rules()


if __name__ == "__main__":
    raise SystemExit(main())
