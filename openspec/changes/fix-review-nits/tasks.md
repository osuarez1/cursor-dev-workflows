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
