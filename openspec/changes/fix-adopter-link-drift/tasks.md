Implementation follows the **three-tier link policy** in `design.md` (tier 1 = relative in-repo; tier 2 = GitHub/prose for maintainer-only; tier 3 = copy-then-link). **Source fixes (§2) are primary; `LINK_REWRITES` (§3) are a transition aid only** — pattern rules + tests enforce that boundary.

## 1. Adopter-shaped source docs

- [ ] 1.1 Create `overlays/lsi/adopter-docs/adopt-and-update.md` per three-tier policy: tier 1 relative links only within adopt output; tier 2 for `patches/`, `MAINTAINER.md`, `adopt-new-repo.md` (GitHub `v{{BUNDLE_VERSION}}` or prose); tier 3 links to `ci/*.yml`
- [ ] 1.2 Add `overlays/lsi/adopter-docs/README.md` — document three-tier link policy, authoring checklist, `LINK_REWRITES` as transition aid only, **long-term expansion rule**, and **`which-workflow.md` canonicality** (adopter: `.lsi/workflows/` merge output; edit: `overlays/lsi/docs/workflows/which-workflow.md`; dogfood: bundle root optional)
- [ ] 1.3 Update `copy_core_bundle()` in `snippets/adopt.py` to copy adopter doc instead of `docs/adopt-and-update.md`
- [ ] 1.4 Copy **both** `docs/ci/check_version-web.yml` and `docs/ci/check_version-ai-agent.yml` unconditionally into `.lsi/workflows/ci/` during every adopt (tier 3; no per-patch conditionals)
- [ ] 1.5 Add maintainer **dual-copy checklist** in `docs/adopt-and-update.md` (banner at top): when editing adopter-facing sections, update `overlays/lsi/adopter-docs/adopt-and-update.md`; link to `adopter-docs/README.md`

## 2. Fix workflow cross-links at source (tier 1)

- [ ] 2.1 `docs/workflows/integrations.md` — replace `../../overlays/lsi/docs/workflows/openspec-git-integration.md` with `openspec-git-integration.md`
- [ ] 2.2 `docs/workflows/ticket-card-info.md` — same OpenSpec link fix
- [ ] 2.3 `docs/workflows/branch-workflow.md` — replace overlay git-trello path with `sdlc/git-trello.md`
- [ ] 2.4 `overlays/lsi/docs/workflows/which-workflow.md` — fix `lsi-help.md` → `../../.cursor/commands/lsi-help.md`; `adopt-and-update.md` → `adopt-and-update.md`
- [ ] 2.5 **Router canonicality** — document which file is authoritative for adopters; sync `overlays/lsi/which-workflow-lsi.md` with tier 1 link fixes from 2.4; optional review of bundle-root `which-workflow.md` LSI row (dogfood only — may keep maintainer paths):
  - **Adopter canonical (installed):** `.lsi/workflows/which-workflow.md` after adopt
  - **Edit source (authoritative):** `overlays/lsi/docs/workflows/which-workflow.md` — `merge_which_workflow_lsi()` overwrites core copy with this file
  - **Sync helper (not installed):** `overlays/lsi/which-workflow-lsi.md` — keep row/link parity with overlay router; not adopt output
  - **Bundle dogfood (optional):** root `which-workflow.md` — maintainer navigation only; do not treat as adopter canon

## 3. Adopt pipeline safety net (transition aid — §2 source fixes are primary)

- [ ] 3.1 Extend `LINK_REWRITES` in `snippets/adopt.py` for accidental tier 2 paths in tier 1 content (`overlays/lsi/docs/workflows/`, `overlays/lsi/docs/sdlc/`, `agent-stack/commands/`, `../../../docs/adopt-and-update.md`) — catch-alls only; do not add rewrites instead of source fixes
- [ ] 3.2 Add pattern rules in `snippets/adoption-verify-links.py` for `overlays/lsi/` and `agent-stack/` inside canonical tree (tier 2 smuggled as relative)
- [ ] 3.3 Add fixture + test case for maintainer-path pattern violation under `snippets/fixtures/adoption-verify/`
- [ ] 3.4 Add bundle-side source grep in `docs/workflows/` and `overlays/lsi/docs/workflows/` — script under `snippets/`; **phase 1:** `](overlays/lsi/`; **phase 2:** extend to `](agent-stack/` once §2 overlay workflow sources are clean (after 2.4); wire as pre-commit and/or CI (fail before adopt; complements §4 regression tests)

## 4. Bundle regression tests (highest-value deliverable)

- [ ] 4.1 Add `snippets/test_adopt_links.py` — temp adopt + `adoption-verify-links.verify()` asserts zero broken links under `.lsi/workflows/`; same test calls `verify(..., extra_dirs=[Path("docs/ai")])` to cover `docs/ai/openspec.md` cross-tree links to `../../.lsi/workflows/openspec-git-integration.md` (bundle regression only — does not change `verify-adopters.py` default per 5.2)
- [ ] 4.2 Assert **`BUNDLE_VERSION` token parity** after temp adopt — adopter `PROJECT.md` has `BUNDLE_VERSION` matching bundle `VERSION`; adopted tier 2 URLs show `v{VERSION}` with no literal `{{BUNDLE_VERSION}}` (existing `substitute_tokens` + `update_project_md`; one assertion in `test_adopt_links.py`)
- [ ] 4.3 Assert adopted `.lsi/workflows/**/*.md` contains no `overlays/lsi/` or `../../agent-stack/` substrings (tier 2 paths in tier 1 tree)
- [ ] 4.4 Run `python3 snippets/test_adoption_verify_links.py` and `python3 snippets/test_adopt_links.py` locally — both must pass before §5 release tasks
- [ ] 4.5 Document **required release gate**: adopt-link regression tests must pass before `VERSION` bump — update `docs/adoption-verify-architecture.md`, bundle `README.md`, and maintainer pre-release checklist; document source grep (task 3.4) as fast PR/pre-commit check
- [ ] 4.6 **When bundle pipeline lands:** add CI step running **both** test modules on every PR / pre-release:
  ```bash
  python3 snippets/test_adoption_verify_links.py
  python3 snippets/test_adopt_links.py
  ```
  Block merge on failure; same gate as local maintainer pre-`VERSION` checklist (task 4.4). Optionally add source grep (task 3.4) and `test_adopt_tokens.py` in the same job.

## 5. Docs and release

- [ ] 5.1 Update `docs/adoption-verify-architecture.md` — three-tier link policy, pattern rules, bundle source grep (task 3.4), `overlays/lsi/adopter-docs/` source path, tier 3 CI copy, **pre-`VERSION` regression gate**, **CI step for both test modules when pipeline lands** (task 4.6)
- [ ] 5.2 Fix `overlays/lsi/docs/ai/openspec.md` at source (tier 1 cross-tree): `../workflows/openspec-git-integration.md` → `../../.lsi/workflows/openspec-git-integration.md` (both occurrences); do **not** add `--extra-dirs docs/ai` to `verify-adopters.py`
- [ ] 5.3 Bump `VERSION` and `CHANGELOG.md` — **only after §4 tests pass**; release note **must** include a prominent **Adopters** callout that registered LSI adopters need **`/lsi:update`** after pulling this bundle release (not optional); also summarize three-tier link policy
- [ ] 5.4 Manual smoke: `adopt.py` against temp repo + `verify-adopters.py --repo-root <tmp>` passes

## 6. Post-merge (maintainer — not apply deliverables; **real acceptance test**)

Adopter parity on registered repos is the **real acceptance test** — temp-dir regression (§4) is necessary but not sufficient. **Do not announce** the release (team chat, adopter ping, `/lsi:update` broadcast) until 6.1 completes.

- [ ] 6.1 Re-sync registered adopters via maintainer adopt loop; confirm `verify-adopters.py` passes on each — **required before announcing this release**

## 7. Long-term (follow-on — not apply deliverables)

- [ ] 7.1 When a copied doc cannot be authored cleanly in the maintainer tree, add an adopter-shaped source under `overlays/lsi/adopter-docs/` (mirroring install path) and wire `adopt.py` — expand beyond `adopt-and-update.md` per design **Long-term direction**; **when a second dual doc enters `adopter-docs/`, reconsider task 7.2**
- [ ] 7.2 **When a second dual doc enters `adopter-docs/`** (follow-on to 7.1 — not before): add bundle lint that diffs **adopter-relevant** `##` headings between each maintainer superset and its `adopter-docs/` copy (not naive full heading parity); wire to CI alongside adopt-link regression (task 4.6). This change seeds one dual doc (`adopt-and-update.md`) — checklist (1.5) + link tests suffice until then
