#!/usr/bin/env bash
# Install gitignored .cursor/commands and .cursor/rules for bundle maintainers.
# Re-run after editing overlays/lsi/agent-stack/commands/ or maintainer-local rules.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$ROOT/snippets/install-maintainer-local.py"
