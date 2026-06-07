#!/usr/bin/env bash
# Verify all registered LSI adopters. Run from cursor-dev-workflows root.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

declare -a TARGETS=(
  "../video-encoder"
  "../web"
  "../agents/ai-agent"
)

failed=0
for target in "${TARGETS[@]}"; do
  if [[ ! -d "$target" ]]; then
    echo "SKIP: $target (not found)"
    continue
  fi
  if ! python3 snippets/verify-adopters.py --repo-root "$target"; then
    failed=1
  fi
done

exit "$failed"
