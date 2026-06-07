## 1. Adopt token injection

- [x] 1.1 In `snippets/adopt.py`, merge `BUNDLE_VERSION` from bundle `VERSION` into tokens before copy phases
- [x] 1.2 Replace hardcoded `v1.0.0` with `v{{BUNDLE_VERSION}}` in `overlays/lsi/docs/workflows/openspec-git-integration.md`

## 2. YAML fallback cleanup

- [x] 2.1 Remove dead list-parsing branch in `_load_simple_yaml` and simplify dict/list append logic
- [x] 2.2 Smoke-test `load_config(Path('patches/web.yaml'))` resolves `scope_exclude_globs` as a list

## 3. Dogfood version sync

- [x] 3.1 Update `PROJECT.md` `BUNDLE_VERSION` to match root `VERSION` (1.3.0)

## 4. Verification

- [x] 4.1 Run `python3 snippets/test_adoption_verify_links.py`
- [x] 4.2 Confirm `substitute_tokens` would replace `{{BUNDLE_VERSION}}` in overlay copy path (manual or dry-run inspect)

## 5. Staging-first card policy

- [x] 5.1 Update `overlays/lsi/agent-stack/commands/lsi-card.md` — allow `main` or `staging`; pull current branch before `git ts`
- [x] 5.2 Update related overlay docs and rules (`openspec-git-integration.md`, `branch-workflow.md`, `branch-workflow.mdc`, `lsi-branch.md`, `opsx-propose.md`, `which-workflow.md`, `openspec.md`, `branch-reviewability.md`)

## 6. Trello card slash commands

- [x] 6.1 Add `lsi-card-link.md`, `lsi-trello-list.md`, `lsi-trello-branch.md` under `overlays/lsi/agent-stack/commands/`
- [x] 6.2 Update routing docs (`integrations.md`, `git-trello.md`, `which-workflow.md`, `which-workflow-lsi.md`, `ticket-card-info.md`)
- [x] 6.3 Extend `verify-adopters.py` and `audit-agent-docs.py` parity lists (18× `/lsi:*`)
- [x] 6.4 Fix protected-branch guardrails — card-setup commands include trello-list and trello-branch
- [x] 6.5 Genericize `/lsi:branch` opening line — remove adopter-specific copy from overlay command source

## 7. Maintainer `.cursor/` gitignore

- [x] 7.1 Add `.cursor/` to `.gitignore` and remove tracked rules from git index
- [x] 7.2 Update `AGENTS.md`, `PROJECT.md`, `README.md` to reference `snippets/cursor-rules/commit-pr-conventions.mdc`
- [x] 7.3 Add `bootstrap-maintainer-local.sh` and `install-maintainer-local.py` to sync `.cursor/commands/` from overlay (install docs in gitignored `MAINTAINER.md`)
- [x] 7.4 Add `/lsi:update` and `update-workflows.py` — auto-detect bundle maintainer vs adopter re-sync
- [x] 7.5 Gitignore `maintainer-adopters.local.yaml`; load adopter targets from that file in `update-workflows.py` / `verify-all-adopters.sh`; org paths documented in gitignored `MAINTAINER.md` only
- [x] 7.6 Genericize `/lsi:update` tracked examples — no org-specific adopter paths in slash command copy

## 8. Regression tests

- [x] 8.1 Add `snippets/test_adopt_tokens.py` — `BUNDLE_VERSION` substitution and `patches/web.yaml` list keys
- [x] 8.2 Run `python3 snippets/test_adoption_verify_links.py` and `python3 snippets/test_adopt_tokens.py`
- [x] 8.3 Add `snippets/test_update_workflows.py` — adopter target loader and repo detection
