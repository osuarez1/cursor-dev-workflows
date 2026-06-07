## Why

Promotion readiness and code review for bundle **v1.3.0** surfaced minor inconsistencies: dogfood `PROJECT.md` lagged `VERSION`, the LSI overlay cited a stale bundle version, and `adopt.py` had dead code in its stdlib YAML fallback. Implementation also needed Trello card flows for branches created before card setup and for existing To Do cards, plus gitignore of the local `.cursor/` maintainer install.

## What Changes

- Sync bundle dogfood `PROJECT.md` `BUNDLE_VERSION` to match `VERSION` (1.3.0).
- Replace hardcoded `v1.0.0` in `openspec-git-integration.md` overlay with `v{{BUNDLE_VERSION}}`.
- Inject `BUNDLE_VERSION` from bundle `VERSION` file into adopt token substitution so overlay docs resolve correctly on every adopt.
- Remove dead/broken list parsing branch in `_load_simple_yaml` fallback (PyYAML-unavailable path).
- Allow **`/lsi:card`** from **`staging`** as well as **`main`** (staging-first repos start card + branch from integration branch).
- Add **`/lsi:card-link`**, **`/lsi:trello-list`**, and **`/lsi:trello-branch`** — OpenSpec-gated, redacted Trello card copy for existing branches and To Do cards.
- Gitignore **`.cursor/`** in the bundle repo; remove tracked rules from version control; point maintainer docs at `snippets/cursor-rules/`.
- Add **`/lsi:update`** and maintainer re-sync helpers — `update-workflows.py`, `install-maintainer-local.py`, `bootstrap-maintainer-local.sh` — with org-specific adopter clone paths in gitignored **`maintainer-adopters.local.yaml`** (documented in gitignored **`MAINTAINER.md`** only, not tracked slash commands).
- Add regression tests for `BUNDLE_VERSION` token injection and patch YAML list loading.
- Genericize overlay command copy where review surfaced adopter-specific wording (e.g. `/lsi:branch` opening line).

## Capabilities

### New Capabilities

- `adopt-bundle-version-token`: Overlay and adopt pipeline substitute `{{BUNDLE_VERSION}}` from bundle `VERSION` during LSI adopt.
- `trello-card-slash-commands`: Card-link and trello list/branch slash commands with OpenSpec-gated redacted card copy.
- `maintainer-cursor-gitignore`: Local `.cursor/` install gitignored; canonical rules in `snippets/cursor-rules/`; maintainer re-sync via `/lsi:update` and gitignored adopter path config.

### Modified Capabilities

- *(none — no normative specs in `openspec/specs/` yet)*

## Impact

- `PROJECT.md`, `AGENTS.md`, `README.md` — dogfood paths and `.cursor/` gitignore note
- `.gitignore` — `.cursor/`, `.git-trello/`, `maintainer-adopters.local.yaml`
- `overlays/lsi/docs/workflows/openspec-git-integration.md` — overlay header and card routing
- `overlays/lsi/agent-stack/commands/` — `lsi-card`, `lsi-card-link`, `lsi-trello-list`, `lsi-trello-branch`, `lsi-update`, `lsi-branch` (generic copy)
- `docs/workflows/integrations.md`, `overlays/lsi/docs/sdlc/git-trello.md`, routing tables
- `snippets/adopt.py`, `update-workflows.py`, `install-maintainer-local.py`, `verify-adopters.py`, `audit-agent-docs.py`, `test_adopt_tokens.py`, `test_update_workflows.py`
- Adopters re-syncing after merge will get new slash commands, resolved bundle version strings in adopted overlay docs, and updated `BUNDLE_VERSION` in `PROJECT.md`
