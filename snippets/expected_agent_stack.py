"""Authoritative expected agent-stack for cursor-dev-workflows adopters.

Single source of truth for:
- expected_commands(): cursor command basenames that every adopter must have
- expected_rules(): cursor rule filenames that every adopter must have
- legacy_rule_aliases(): pairs that must not coexist (legacy alias duplication)
- is_unmanaged_command(): commands the bundle neither installs nor removes

Used by audit-agent-docs.py (check_agent_stack_parity) and verify-adopters.py.

Scope: this bundle manages **LSI** (`lsi-*`) slash commands only. **OpenSpec**
(`opsx-*`) commands are owned by OpenSpec itself (`openspec init` / config
profile); the bundle does not install, regenerate, or remove them, and the
parity gate ignores the `opsx-` namespace entirely.
"""

from __future__ import annotations

from pathlib import Path

BUNDLE_ROOT = Path(__file__).resolve().parents[1]
COMMANDS_DIR = BUNDLE_ROOT / "overlays" / "lsi" / "agent-stack" / "commands"
CURSOR_RULES_DIR = BUNDLE_ROOT / "snippets" / "cursor-rules"

# Commands the bundle installs and verifies on every adopter.
LSI_COMMANDS = [
    "lsi-help",
    "lsi-card",
    "lsi-card-link",
    "lsi-trello-list",
    "lsi-trello-branch",
    "lsi-branch",
    "lsi-senior",
    "lsi-commit",
    "lsi-readiness",
    "lsi-review",
    "lsi-pr",
    "lsi-promote",
    "lsi-merge-desc",
    "lsi-close",
    "lsi-version",
    "lsi-changelog",
    "lsi-release",
    "lsi-bootstrap-release",
    "lsi-update",
]

# Command namespaces the bundle does NOT manage. Files with these prefixes are
# owned by an external tool (OpenSpec) and must never be installed, regenerated,
# or flagged as surplus by the parity gate.
UNMANAGED_COMMAND_PREFIXES = ("opsx-",)

# Rules installed by adopt on every adopter.
ALWAYS_ON_RULES = [
    "branch-workflow.mdc",
    "commit-pr-conventions.mdc",
    "openspec-git-integration.mdc",
    "code-review.mdc",
    "pull-requests.mdc",
    "senior-analysis.mdc",
    "ticket-card-info.mdc",
]

# Legacy alias pairs: both files must NOT coexist.
# Key = canonical name, value = legacy alias that should be removed.
LEGACY_RULE_ALIAS_PAIRS = [
    ("code-review.mdc", "code_review.mdc"),
]


def is_unmanaged_command(name: str) -> bool:
    """Return True for command basenames the bundle delegates to another tool.

    `name` is a command basename without the .md extension (e.g. ``opsx-apply``).
    """
    return name.startswith(UNMANAGED_COMMAND_PREFIXES)


def expected_commands() -> set[str]:
    """Return expected cursor command basenames (without .md extension).

    Only LSI commands are bundle-managed; OpenSpec commands are delegated to
    OpenSpec and intentionally excluded.
    """
    return set(LSI_COMMANDS)


def expected_rules(extra_rules: list[str] | None = None) -> set[str]:
    """Return expected cursor rule filenames.

    extra_rules: additional rules from patch rule_overlays.
    """
    rules = set(ALWAYS_ON_RULES)
    if extra_rules:
        rules.update(extra_rules)
    return rules


def legacy_rule_aliases() -> list[tuple[str, str]]:
    """Return (canonical, legacy_alias) pairs that must not coexist."""
    return list(LEGACY_RULE_ALIAS_PAIRS)


def bundle_command_names() -> set[str]:
    """Return basenames of all command files in overlay source."""
    if not COMMANDS_DIR.is_dir():
        return set()
    return {p.stem for p in COMMANDS_DIR.glob("*.md")}
