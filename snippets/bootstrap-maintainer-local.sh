#!/usr/bin/env bash
# Install local agent stacks for bundle maintainers:
#   .cursor/commands + rules, .claude/commands/lsi/, .opencode/commands/lsi-*
# OpenCode emit here is a bundle special case (adopters use agents_opencode).
# Re-run after editing overlays/lsi/agent-stack/commands/ or maintainer-local rules.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$ROOT/snippets/install-maintainer-local.py"
