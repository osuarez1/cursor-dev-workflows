#!/usr/bin/env bash
# Warn if bundle maintainer local kit is missing (non-CI, local only).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WARN=0

check() {
  local path="$1" label="$2"
  if [[ ! -e "$path" ]]; then
    echo "MISSING: $label ($path)"
    WARN=1
  else
    echo "OK: $label"
  fi
}

echo "Bundle maintainer local kit — $ROOT"
echo ""

check "$ROOT/MAINTAINER.md" "MAINTAINER.md"
check "$ROOT/AGENTS-LOCAL.md" "AGENTS-LOCAL.md"
check "$ROOT/.cursor/rules/local-maintainer.mdc" "local-maintainer.mdc"
check "$ROOT/.cursor/rules/local-branch-workflow.mdc" "local-branch-workflow.mdc"
check "$ROOT/.cursor/rules/local-openspec-git-integration.mdc" "local-openspec-git-integration.mdc"
check "$ROOT/.cursor/commands/lsi-card.md" "lsi-card command"
check "$ROOT/.cursor/commands/opsx-propose.md" "opsx-propose command"
check "$ROOT/openspec/config.yaml" "openspec/config.yaml"
check "$ROOT/openspec/changes" "openspec/changes/"

echo ""
if [[ "$WARN" -eq 1 ]]; then
  echo "RESULT: INCOMPLETE — run ./snippets/bootstrap-maintainer-local.sh"
  exit 1
fi
echo "RESULT: OK"
exit 0
