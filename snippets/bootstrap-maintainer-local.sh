#!/usr/bin/env bash
# Install gitignored bundle maintainer kit (playbooks, rules, commands).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATE="$ROOT/snippets/maintainer-local"
FORCE=0
REFRESH_COMMANDS=0

usage() {
  echo "Usage: $0 [--force] [--refresh-commands]"
  echo "  --force             Overwrite MAINTAINER.md and AGENTS-LOCAL.md"
  echo "  --refresh-commands  Refresh .cursor/commands/ and local-*.mdc only"
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force) FORCE=1; shift ;;
    --refresh-commands) REFRESH_COMMANDS=1; shift ;;
    -h|--help) usage ;;
    *) echo "Unknown option: $1" >&2; usage ;;
  esac
done

copy_if_missing() {
  local src="$1" dst="$2"
  if [[ -f "$dst" && "$FORCE" -eq 0 ]]; then
    echo "Keep existing $dst"
    return 0
  fi
  cp "$src" "$dst"
  echo "Installed $dst"
}

if [[ "$REFRESH_COMMANDS" -eq 1 ]]; then
  exec python3 "$ROOT/snippets/install-maintainer-local-commands.py" --bundle-root "$ROOT"
fi

copy_if_missing "$TEMPLATE/MAINTAINER.md.example" "$ROOT/MAINTAINER.md"
copy_if_missing "$TEMPLATE/AGENTS-LOCAL.md.example" "$ROOT/AGENTS-LOCAL.md"

mkdir -p "$ROOT/openspec/changes"
if [[ ! -f "$ROOT/openspec/config.yaml" ]]; then
  cp "$TEMPLATE/openspec/config.yaml.example" "$ROOT/openspec/config.yaml"
  echo "Installed openspec/config.yaml"
else
  echo "Keep existing openspec/config.yaml (tracked)"
fi

if [[ -d "$TEMPLATE/openspec/changes/_template" ]]; then
  mkdir -p "$ROOT/openspec/changes/_template"
  for f in proposal.md design.md tasks.md; do
    if [[ ! -f "$ROOT/openspec/changes/_template/$f" ]]; then
      cp "$TEMPLATE/openspec/changes/_template/$f" \
        "$ROOT/openspec/changes/_template/$f"
    fi
  done
  echo "Ensured openspec/changes/_template/"
fi

if ! python3 "$ROOT/snippets/install-maintainer-local-commands.py" --bundle-root "$ROOT"; then
  echo "WARN: command install incomplete (overlay or adopter .cursor/commands required)" >&2
fi

echo ""
echo "Done. Run: ./snippets/verify-maintainer-local.sh"
echo "Edit MAINTAINER.md with your WORKFLOWS_BUNDLE_PATH and adopter paths."
