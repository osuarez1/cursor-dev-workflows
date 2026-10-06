#!/usr/bin/env bash
# Fresh LSI adopt from an application repo root. Prefer local --bundle path.
set -euo pipefail

BUNDLE="${LSI_BUNDLE:-${WORKFLOWS_BUNDLE_PATH:-}}"
REPO_NAME=""
ACCEPT_POLICY=0
TARGET="$(pwd)"

usage() {
  cat <<'EOF'
Usage: install-adopt.sh --bundle <path-to-cursor-dev-workflows> --repo-name <name> [--accept-policy-defaults]

Env alternatives: LSI_BUNDLE or WORKFLOWS_BUNDLE_PATH for --bundle.

Runs snippets/adopt.py against patches/<repo-name>.yaml, then verify-adopters.py.
Does not invent domain overlay prose. After install, run /lsi:adopt-verify for accuracy review.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --bundle) BUNDLE="$2"; shift 2 ;;
    --repo-name) REPO_NAME="$2"; shift 2 ;;
    --accept-policy-defaults) ACCEPT_POLICY=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; usage; exit 2 ;;
  esac
done

if [[ -z "$BUNDLE" || -z "$REPO_NAME" ]]; then
  echo "ERROR: --bundle (or LSI_BUNDLE) and --repo-name are required." >&2
  usage
  exit 2
fi

BUNDLE="$(cd "$BUNDLE" && pwd)"
CONFIG="$BUNDLE/patches/${REPO_NAME}.yaml"
if [[ ! -f "$CONFIG" ]]; then
  echo "ERROR: missing patch config: $CONFIG" >&2
  exit 2
fi
if [[ ! -f "$BUNDLE/snippets/adopt.py" ]]; then
  echo "ERROR: not a cursor-dev-workflows bundle: $BUNDLE" >&2
  exit 2
fi

ARGS=(--target "$TARGET" --config "$CONFIG")
if [[ "$ACCEPT_POLICY" -eq 1 ]]; then
  ARGS+=(--accept-policy-defaults)
fi

python3 "$BUNDLE/snippets/adopt.py" "${ARGS[@]}"
python3 "$BUNDLE/snippets/verify-adopters.py" --repo-root "$TARGET"
echo "Install-adopt complete. Review with /lsi:adopt-verify (accuracy layer)."
