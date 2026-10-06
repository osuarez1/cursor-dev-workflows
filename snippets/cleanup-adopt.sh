#!/usr/bin/env bash
# Remove adopt-managed LSI agent-stack + regenerable .lsi/workflows (dry-run default).
set -euo pipefail

YES=0
BUNDLE="${LSI_BUNDLE:-${WORKFLOWS_BUNDLE_PATH:-}}"
REPO_NAME=""
TARGET="$(pwd)"

usage() {
  cat <<'EOF'
Usage: cleanup-adopt.sh [--yes] [--bundle <path>] [--repo-name <name>]

Dry-run lists paths. --yes deletes adopt-managed artifacts.
Never deletes PROJECT.md or application source.
Honors preserve / preserve_agent_stack globs from patches/<repo>.yaml when --repo-name is set.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --yes) YES=1; shift ;;
    --bundle) BUNDLE="$2"; shift 2 ;;
    --repo-name) REPO_NAME="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; usage; exit 2 ;;
  esac
done

candidates=()
shopt -s nullglob
for f in .cursor/commands/lsi-*.md; do candidates+=("$f"); done
for f in .cursor/rules/branch-workflow.mdc \
         .cursor/rules/commit-pr-conventions.mdc \
         .cursor/rules/openspec-git-integration.mdc \
         .cursor/rules/code-review.mdc \
         .cursor/rules/pull-requests.mdc \
         .cursor/rules/senior-analysis.mdc \
         .cursor/rules/ticket-card-info.mdc; do
  [[ -e "$f" ]] && candidates+=("$f")
done
for f in .claude/commands/lsi/*.md; do candidates+=("$f"); done
[[ -d .opencode ]] && candidates+=(".opencode")
[[ -d .lsi/workflows ]] && candidates+=(".lsi/workflows")

preserve_patterns=()
if [[ -n "$BUNDLE" && -n "$REPO_NAME" && -f "$BUNDLE/patches/${REPO_NAME}.yaml" ]]; then
  while IFS= read -r line; do
    [[ -n "$line" ]] && preserve_patterns+=("$line")
  done < <(python3 - "$BUNDLE/patches/${REPO_NAME}.yaml" <<'PY'
import re
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text()
in_block = False
for raw in text.splitlines():
    if re.match(r"^(preserve|preserve_agent_stack):\s*$", raw):
        in_block = True
        continue
    if in_block:
        m = re.match(r"^\s*-\s+(.+)$", raw)
        if m:
            print(m.group(1).strip().strip('"').strip("'"))
        elif re.match(r"^\S", raw):
            in_block = False
PY
)
fi

should_keep() {
  local path="$1"
  local pat prefix
  for pat in "${preserve_patterns[@]:-}"; do
    case "$path" in
      $pat) return 0 ;;
    esac
    if [[ "$pat" == *'/**' ]]; then
      prefix="${pat%/**}"
      [[ "$path" == "$prefix"* ]] && return 0
    fi
  done
  return 1
}

filtered=()
for c in "${candidates[@]}"; do
  if should_keep "$c"; then
    echo "KEEP (preserve): $c"
  else
    filtered+=("$c")
  fi
done

echo "Cleanup candidates (${#filtered[@]}):"
for c in "${filtered[@]}"; do echo "  $c"; done

if [[ "$YES" -ne 1 ]]; then
  echo "Dry-run only. Re-run with --yes to delete."
  exit 0
fi

for c in "${filtered[@]}"; do
  if [[ -d "$c" ]]; then
    rm -rf "$c"
  elif [[ -e "$c" ]]; then
    rm -f "$c"
  fi
  echo "Removed $c"
done
echo "Cleanup complete. PROJECT.md and app source were not touched."
