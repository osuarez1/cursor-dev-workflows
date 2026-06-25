"""Authoritative expected agent-stack for cursor-dev-workflows adopters.

Single source of truth for:
- expected_commands(): cursor command basenames that every adopter must have
- expected_rules(): cursor rule filenames that every adopter must have
- legacy_rule_aliases(): pairs that must not coexist (legacy alias duplication)

Used by audit-agent-docs.py (check_agent_stack_parity) and verify-adopters.py.
"""

from __future__ import annotations

from pathlib import Path

BUNDLE_ROOT = Path(__file__).resolve().parents[1]
COMMANDS_DIR = BUNDLE_ROOT / "overlays" / "lsi" / "agent-stack" / "commands"
CURSOR_RULES_DIR = BUNDLE_ROOT / "snippets" / "cursor-rules"

# Commands always installed regardless of sync_opsx.
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

# OPSX commands installed when sync_opsx: true.
OPSX_COMMANDS = [
    "opsx-explore",
    "opsx-propose",
    "opsx-apply",
    "opsx-sync",
    "opsx-archive",
    "opsx-new",
    "opsx-ff",
    "opsx-continue",
    "opsx-onboard",
    "opsx-verify",
    "opsx-bulk-archive",
]

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


def expected_commands(*, sync_opsx: bool = False) -> set[str]:
    """Return expected cursor command basenames (without .md extension).

    If sync_opsx is True, includes all opsx-* commands.
    Otherwise includes only the base opsx-* commands that are always installed.
    """
    base_opsx = {"opsx-explore", "opsx-propose", "opsx-apply", "opsx-sync", "opsx-archive"}
    cmds = set(LSI_COMMANDS)
    if sync_opsx:
        cmds.update(OPSX_COMMANDS)
    else:
        cmds.update(base_opsx)
    return cmds


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
