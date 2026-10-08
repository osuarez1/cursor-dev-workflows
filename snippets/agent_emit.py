"""Shared Claude / OpenCode command transforms for adopt and maintainer install."""

from __future__ import annotations

import re

_FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n", re.DOTALL)
_DESCRIPTION_RE = re.compile(r"^description:\s*(.+)$", re.MULTILINE)
_INPUT_LINE_RE = re.compile(r"^(\*\*Input:\*\*.+)$", re.MULTILINE)


def claude_frontmatter(text: str) -> str:
    """Replace multi-field cursor frontmatter with minimal Claude description-only header."""
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return text
    frontmatter = m.group(0)
    desc_m = _DESCRIPTION_RE.search(frontmatter)
    description = desc_m.group(1).strip() if desc_m else ""
    body = text[m.end() :]
    return f"---\ndescription: {description}\n---\n{body}"


def claude_subdir(stem: str) -> tuple[str, str]:
    """Return (subdir, filename) for a command stem like 'lsi-branch' → ('lsi', 'branch')."""
    if stem.startswith("lsi-"):
        return "lsi", stem[len("lsi-") :]
    return "", stem


def deepen_relative_links(text: str, extra_levels: int = 1) -> str:
    """Prefix relative markdown link targets with extra ``../`` segments.

    Used when emitting the same body one directory deeper (e.g. `.claude/commands/lsi/`
    vs `.cursor/commands/`). Absolute, hash, and scheme URLs are left unchanged.
    """
    if extra_levels <= 0:
        return text
    prefix = "../" * extra_levels

    def repl(match: re.Match[str]) -> str:
        url = match.group(1)
        if not url or url.startswith(
            ("http://", "https://", "/", "#", "mailto:", "`")
        ):
            return match.group(0)
        # Already repo-root style paths (no ../) stay as-is — they resolve from cwd
        # conventions in verify; only deepen explicit relative parent walks.
        if not url.startswith("../") and not url.startswith("./"):
            return match.group(0)
        return f"]({prefix}{url})"

    return re.sub(r"\]\(([^)]+)\)", repl, text)


def opencode_frontmatter(text: str) -> str:
    """OpenCode command frontmatter: description only (same shape as Claude)."""
    return claude_frontmatter(text)


def opencode_bind_arguments(text: str) -> str:
    """Append ``$ARGUMENTS`` to the Input line when not already present."""
    if "$ARGUMENTS" in text:
        return text

    def repl(match: re.Match[str]) -> str:
        line = match.group(1)
        if "$ARGUMENTS" in line:
            return line
        return f"{line} `$ARGUMENTS`"

    updated, n = _INPUT_LINE_RE.subn(repl, text, count=1)
    return updated if n else text
