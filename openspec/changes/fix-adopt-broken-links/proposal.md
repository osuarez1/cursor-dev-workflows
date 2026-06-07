## Why

Adopt failed on bundle **v1.4.0** because adopted workflow docs still pointed at bundle-only paths (`overlays/lsi/…`, `docs/adopt-and-update.md`, `../workflows/ticket-card-info.md`, etc.) that do not exist under `.lsi/workflows/` after copy. Broken links block adopter onboarding and `/lsi:update` re-sync until source docs and `adopt.py` rewrite rules are aligned.

## What Changes

- Extend `snippets/adopt.py` `LINK_REWRITES` for overlay workflow paths, overlay→adopted `adopt-and-update.md`, and sdlc→`ticket-card-info.md`.
- Strip or inline bundle-only links in adopted copies (`MAINTAINER.md.example`, `patches/README.md`, `adopt-new-repo.md`) as plain bundle references instead of dead relative URLs.
- Copy `docs/ci/` into `.lsi/workflows/ci/` during adopt so CI workflow templates ship with adopted bundles.
- Fix source markdown to use adopted-local relative links before rewrite:
  - `docs/workflows/integrations.md` — `openspec-git-integration.md`
  - `docs/workflows/ticket-card-info.md` — `openspec-git-integration.md`
  - `overlays/lsi/docs/sdlc/git-trello.md` — `../ticket-card-info.md`
  - `overlays/lsi/docs/workflows/which-workflow.md` — `adopt-and-update.md`

## Capabilities

### New Capabilities

- `adopt-doc-link-resolution`: Adopt pipeline rewrites bundle and overlay doc links to valid `.lsi/workflows/` paths, strips bundle-only references, and copies `docs/ci/` into adopters.

### Modified Capabilities

- *(none — link fixes do not change requirements in existing `openspec/specs/`)*

## Impact

- `snippets/adopt.py` — link rewrite table, bundle-only link stripping, `docs/ci/` copy in `copy_core_bundle`
- `docs/workflows/integrations.md`, `docs/workflows/ticket-card-info.md` — OpenSpec routing links
- `overlays/lsi/docs/sdlc/git-trello.md`, `overlays/lsi/docs/workflows/which-workflow.md` — adopted-local paths
- Adopters on v1.4.0+ get resolvable workflow cross-links and CI template files under `.lsi/workflows/ci/`
