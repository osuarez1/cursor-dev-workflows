## Why

Recent LSI overlay updates (card-link, Trello list/branch flows, `/lsi:update`, branch-workflow and OpenSpec integration rules, `AGENTS.md`, and `docs/ai/openspec.md`) introduced markdown links that still target the **bundle maintainer** tree (`overlays/lsi/…`, `agent-stack/commands/…`, `docs/ci/…`, `patches/…`). After `adopt.py` copies specs into `.lsi/workflows/`, `verify-adopters.py` / `adoption-verify-links.py` fail because those paths do not exist in adopter repos.

## What Changes

- Fix **source** workflow docs and adopt transforms so every link inside adopted `.lsi/workflows/**/*.md` resolves within the adopter repo root.
- Replace or rewrite maintainer-only targets (`../MAINTAINER.md.example`, `../patches/README.md`, `../../overlays/lsi/docs/…`, `../../agent-stack/commands/…`, `ci/check_version-*.yml` without a copied target).
- Introduce an **adopter-shaped source subtree** (`overlays/lsi/adopter-docs/`) for docs where maintainer layout diverges from adopter layout — starting with `adopt-and-update.md`; **long-term:** expand for any similar doc rather than growing rewrites
- Add **bundle-side regression tests** (`test_adopt_links.py`) — **highest-value deliverable** for long-term maintenance; catches adopt link drift before adopter re-sync and before every `VERSION` bump
- Optionally extend link-verify **pattern rules** to flag bundle-maintainer path prefixes inside `CANONICAL_DOCS_PATH` (fail fast on future drift).
- Add **bundle-side source grep** in `docs/workflows/` and `overlays/lsi/docs/workflows/` — phase 1: `](overlays/lsi/`; phase 2: `](agent-stack/` once overlay workflow sources are clean (pre-commit or CI, before adopt)
- Codify a **three-tier link policy** for adopt output: tier 1 relative in-repo, tier 2 GitHub/prose for maintainer-only, tier 3 copy-then-link for small extras.
- Update `docs/adoption-verify-architecture.md` and maintainer notes if scan rules or source layout change.

## Capabilities

### New Capabilities

- `adopt-doc-link-resolution`: Adopt output under `.lsi/workflows/` SHALL have no broken relative links; bundle sources and transforms SHALL be verifiable before adopter re-sync.

### Modified Capabilities

- _(none — no existing spec defines adopt link resolution requirements)_

## Impact

- **Source docs:** `docs/adopt-and-update.md`, `docs/workflows/integrations.md`, `docs/workflows/ticket-card-info.md`, `docs/workflows/branch-workflow.md`, **`overlays/lsi/docs/workflows/which-workflow.md`** (adopter router source; root `which-workflow.md` dogfood optional)
- **Adopt authoring:** `overlays/lsi/adopter-docs/` (three-tier link policy README + adopter-facing docs; seeds with `adopt-and-update.md`; long-term home for any doc where maintainer layout diverges)
- **Verification:** `snippets/adoption-verify-links.py`, `snippets/verify-adopters.py`, new `snippets/test_adopt_links.py` — **required local/CI gate before `VERSION` bump**; optional source grep script for workflow doc trees (pre-commit or CI)
- **Fixtures:** `snippets/fixtures/adoption-verify/` — add post-adopt drift cases
- **Adopters:** **`/lsi:update` required** after bundle release — release note (`CHANGELOG.md`) must state this clearly; maintainer adopt loop (6.1) must pass on registered repos **before announcing**; no application code changes in adopter repos
