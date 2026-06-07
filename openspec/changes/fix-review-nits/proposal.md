## Why

Promotion readiness and code review for bundle **v1.3.0** surfaced minor inconsistencies: dogfood `PROJECT.md` lagged `VERSION`, the LSI overlay cited a stale bundle version, and `adopt.py` had dead code in its stdlib YAML fallback. These nits block a clean `/lsi:commit` on a ticket branch and would drift again on the next release unless the overlay version is tokenized.

## What Changes

- Sync bundle dogfood `PROJECT.md` `BUNDLE_VERSION` to match `VERSION` (1.3.0).
- Replace hardcoded `v1.0.0` in `openspec-git-integration.md` overlay with `v{{BUNDLE_VERSION}}`.
- Inject `BUNDLE_VERSION` from bundle `VERSION` file into adopt token substitution so overlay docs resolve correctly on every adopt.
- Remove dead/broken list parsing branch in `_load_simple_yaml` fallback (PyYAML-unavailable path).
- Allow **`/lsi:card`** from **`staging`** as well as **`main`** (staging-first repos start card + branch from integration branch).

## Capabilities

### New Capabilities

- `adopt-bundle-version-token`: Overlay and adopt pipeline substitute `{{BUNDLE_VERSION}}` from bundle `VERSION` during LSI adopt.

### Modified Capabilities

- *(none — no normative specs in `openspec/specs/` yet)*

## Impact

- `PROJECT.md` — dogfood placeholder table
- `overlays/lsi/docs/workflows/openspec-git-integration.md` — overlay header
- `overlays/lsi/agent-stack/commands/lsi-card.md` and related workflow docs — staging-first card policy
- `snippets/adopt.py` — token build and YAML fallback parser
- Adopters re-syncing after merge will get correct bundle version in adopted overlay docs
