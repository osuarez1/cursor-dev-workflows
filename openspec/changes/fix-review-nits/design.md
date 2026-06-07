## Context

Bundle **v1.3.0** promotion review (`/lsi:review`) flagged three fixable nits: stale `PROJECT.md` dogfood version, hardcoded `v1.0.0` in the LSI overlay header, and dead code in `_load_simple_yaml`. Partial fixes may already exist in the working tree from an ad-hoc edit session; this change formalizes the scope for `/opsx:apply` and `/lsi:commit` on a ticket branch.

`adopt.py` already reads bundle `VERSION` for `update_project_md` on the **target** adopter repo. The gap is that overlay copy paths use `build_tokens(config)` only — project tokens from `patches/<repo>.yaml` — so `{{BUNDLE_VERSION}}` in overlay markdown would not substitute unless injected into the adopt-time token map.

## Goals / Non-Goals

**Goals:**

- Inject `BUNDLE_VERSION` from bundle `VERSION` into all adopt copy transforms.
- Tokenize overlay bundle version reference in `openspec-git-integration.md`.
- Sync maintainer `PROJECT.md` with `VERSION`.
- Simplify `_load_simple_yaml` list-item handling; verify patch YAML still loads.
- Align `/lsi:card` protected-branch policy with staging-first workflow (`main` or `staging`).
- Add Trello slash commands for existing branches and To Do cards (`/lsi:card-link`, `/lsi:trello-list`, `/lsi:trello-branch`) with OpenSpec-gated redacted card copy.
- Gitignore local `.cursor/` maintainer install; canonical rules in `snippets/cursor-rules/`.
- Provide maintainer re-sync tooling (`/lsi:update`, `update-workflows.py`, `install-maintainer-local.py`) with org-specific adopter paths in gitignored `maintainer-adopters.local.yaml`.

**Non-Goals:**

- Re-adopting all LSI repos (maintainer follow-up after merge).
- Fixing web adopter `stale_path` INFO audit findings (intentional preserved paths).
- Adding `/lsi:ask` command (deferred v1.3.1).
- Bumping bundle semver or changelog (no release — patch on staging before promotion).

## Decisions

### 1. Merge `BUNDLE_VERSION` into adopt tokens at `adopt()` entry

**Choice:** `tokens = {**build_tokens(config), "BUNDLE_VERSION": bundle_version}` immediately after reading `VERSION`.

**Rationale:** Single injection point covers `copy_core_bundle`, `copy_overlay`, and `install_agent_stack` without duplicating logic. Matches existing `{{TOKEN}}` substitution in `substitute_tokens`.

**Alternative rejected:** Add `BUNDLE_VERSION` only in `update_project_md` — does not fix overlay copy.

### 2. Use `v{{BUNDLE_VERSION}}` in overlay source

**Choice:** Replace literal `v1.0.0` with `v{{BUNDLE_VERSION}}` in overlay markdown.

**Rationale:** Per [docs/token-registry.md](../../../docs/token-registry.md); survives future release bumps without manual overlay edits.

**Alternative rejected:** Hardcode `v1.3.0` — repeats on every release.

### 3. Minimal `_load_simple_yaml` refactor

**Choice:** Remove dead `v is ...` branch; handle list parent vs dict parent explicitly.

**Rationale:** Fallback path must remain correct when PyYAML missing; dead code is confusing and was flagged in review.

### 4. Allow `/lsi:card` from `staging`

**Choice:** Permit card + branch setup on **`main`** or **`staging`**; pull the current branch before `git ts`.

**Rationale:** Staging-first repos integrate on `staging`; requiring checkout to `main` for every new card adds friction and conflicts with "implement from staging" in the migration plan.

**Alternative rejected:** `main` only — blocks card creation when maintainer is already on `staging` for promotion catch-up work.

### 5. Trello card slash commands

**Choice:** Add `/lsi:card-link` (rename in place), `/lsi:trello-list` (picker + confirm), `/lsi:trello-branch` (`git tb` + OpenSpec sync). Require in-progress OpenSpec change and redact before Trello API.

**Rationale:** Staging-first and propose-before-card flows left branches without Trello ids; existing To Do cards need `git tb` with consistent OpenSpec card bodies.

### 6. Gitignore `.cursor/` in bundle repo

**Choice:** Track rules in `snippets/cursor-rules/`; install to `.cursor/` locally via bootstrap; gitignore `.cursor/`.

**Rationale:** Slash commands and maintainer-local rules are install artifacts, not bundle source.

### 7. Maintainer re-sync helpers

**Choice:** Add `/lsi:update`, `update-workflows.py` (auto-detect bundle maintainer vs adopter), and `install-maintainer-local.py` (invoked by `bootstrap-maintainer-local.sh`).

**Rationale:** After gitignoring `.cursor/`, maintainers need a repeatable path to re-sync slash commands from overlay source and re-run adopt across registered adopters after bundle releases.

**Alternative rejected:** Document manual `adopt.py` loops only in MAINTAINER.md — error-prone and duplicates bootstrap + adopt steps.

### 8. Gitignored adopter path config

**Choice:** Org-specific clone paths live in gitignored `maintainer-adopters.local.yaml` at bundle root; `update-workflows.py` and `verify-all-adopters.sh` load targets from that file. Tracked slash commands and public docs reference gitignored `MAINTAINER.md` only — no hardcoded `../<repo>` paths in tracked command examples.

**Rationale:** Maintainer tooling may ship in the bundle repo, but clone layout is machine- and org-specific; should not appear in PRs or adopted copies.

**Alternative rejected:** Hardcode `MAINTAINER_ADOPTER_TARGETS` in tracked `update-workflows.py` — leaks org layout into version control.

## Risks / Trade-offs

- **[Risk] Bundle repo reads overlay with unreplaced `{{BUNDLE_VERSION}}`** → Expected in source overlay; only adopted copies substitute. Adopters must re-sync after merge to pick up resolved version strings.
- **[Risk] Working tree already contains fixes** → `/opsx:apply` should verify idempotently and commit only if diffs remain.
- **[Risk] Missing `maintainer-adopters.local.yaml`** → `/lsi:update` still bootstraps `.cursor/` but skips adopter sync loop until maintainer creates the file per `MAINTAINER.md`.

## Migration Plan

1. Implement on ticket branch from `staging`.
2. Run `python3 snippets/test_adoption_verify_links.py`, `python3 snippets/test_adopt_tokens.py`, and `python3 snippets/test_update_workflows.py`.
3. Commit via `/lsi:commit`; merge to `staging`; include in promotion PR to `main`.
4. **Post-merge:** re-sync all LSI adopters via `/lsi:update` so adopted overlay docs resolve `v{{BUNDLE_VERSION}}` and new slash commands install.

## Open Questions

- None blocking merge.
