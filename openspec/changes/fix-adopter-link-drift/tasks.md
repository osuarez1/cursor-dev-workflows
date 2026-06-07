Implementation follows the **three-tier link policy** in `design.md` (tier 1 = relative in-repo; tier 2 = GitHub/prose for maintainer-only; tier 3 = copy-then-link).

## 1. Adopter-shaped source docs

- [ ] 1.1 Create `overlays/lsi/adopter-docs/adopt-and-update.md` per three-tier policy: tier 1 relative links only within adopt output; tier 2 for `patches/`, `MAINTAINER.md`, `adopt-new-repo.md` (GitHub `v{{BUNDLE_VERSION}}` or prose); tier 3 links to `ci/*.yml`
- [ ] 1.2 Add `overlays/lsi/adopter-docs/README.md` — document three-tier link policy and authoring checklist for maintainers
- [ ] 1.3 Update `copy_core_bundle()` in `snippets/adopt.py` to copy adopter doc instead of `docs/adopt-and-update.md`
- [ ] 1.4 Copy **both** `docs/ci/check_version-web.yml` and `docs/ci/check_version-ai-agent.yml` unconditionally into `.lsi/workflows/ci/` during every adopt (tier 3; no per-patch conditionals)
- [ ] 1.5 Add cross-reference in `docs/adopt-and-update.md` pointing maintainers at `overlays/lsi/adopter-docs/adopt-and-update.md` and `adopter-docs/README.md`

## 2. Fix workflow cross-links at source (tier 1)

- [ ] 2.1 `docs/workflows/integrations.md` — replace `../../overlays/lsi/docs/workflows/openspec-git-integration.md` with `openspec-git-integration.md`
- [ ] 2.2 `docs/workflows/ticket-card-info.md` — same OpenSpec link fix
- [ ] 2.3 `docs/workflows/branch-workflow.md` — replace overlay git-trello path with `sdlc/git-trello.md`
- [ ] 2.4 `overlays/lsi/docs/workflows/which-workflow.md` — fix `lsi-help.md` → `../../.cursor/commands/lsi-help.md`; `adopt-and-update.md` → `adopt-and-update.md`
- [ ] 2.5 Review root `which-workflow.md` LSI row; sync `overlays/lsi/which-workflow-lsi.md` with tier 1 link fixes from 2.4 — ensure overlay merge output has no tier 2 bundle paths disguised as relative links

## 3. Adopt pipeline safety net

- [ ] 3.1 Extend `LINK_REWRITES` in `snippets/adopt.py` for accidental tier 2 paths in tier 1 content (`overlays/lsi/docs/workflows/`, `overlays/lsi/docs/sdlc/`, `agent-stack/commands/`, `../../../docs/adopt-and-update.md`)
- [ ] 3.2 Add pattern rules in `snippets/adoption-verify-links.py` for `overlays/lsi/` and `agent-stack/` inside canonical tree (tier 2 smuggled as relative)
- [ ] 3.3 Add fixture + test case for maintainer-path pattern violation under `snippets/fixtures/adoption-verify/`

## 4. Bundle regression tests

- [ ] 4.1 Add `snippets/test_adopt_links.py` — temp adopt + `adoption-verify-links.verify()` asserts zero broken links
- [ ] 4.2 Assert adopted `.lsi/workflows/**/*.md` contains no `overlays/lsi/` or `../../agent-stack/` substrings (tier 2 paths in tier 1 tree)
- [ ] 4.3 Run `python3 snippets/test_adoption_verify_links.py` and new adopt link tests locally

## 5. Docs and release

- [ ] 5.1 Update `docs/adoption-verify-architecture.md` — three-tier link policy, pattern rules, `overlays/lsi/adopter-docs/` source path, tier 3 CI copy
- [ ] 5.2 Fix `overlays/lsi/docs/ai/openspec.md` at source (tier 1 cross-tree): `../workflows/openspec-git-integration.md` → `../../.lsi/workflows/openspec-git-integration.md` (both occurrences); do **not** add `--extra-dirs docs/ai` to `verify-adopters.py`
- [ ] 5.3 Bump `VERSION` and `CHANGELOG.md` — note adopter re-sync required (`/lsi:update`) and three-tier link policy
- [ ] 5.4 Manual smoke: `adopt.py` against temp repo + `verify-adopters.py --repo-root <tmp>` passes

## 6. Post-merge (maintainer — not apply deliverables)

- [ ] 6.1 Re-sync registered adopters via maintainer adopt loop; confirm `verify-adopters.py` passes on each
