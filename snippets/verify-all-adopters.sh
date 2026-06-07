#!/usr/bin/env bash
# Verify all registered LSI adopters. Run from cursor-dev-workflows root.
# Adopter paths: gitignored maintainer-adopters.local.yaml (see MAINTAINER.md).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
exec python3 snippets/update-workflows.py --verify-adopters-only "$@"
