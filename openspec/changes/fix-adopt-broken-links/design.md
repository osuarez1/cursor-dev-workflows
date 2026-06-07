## Context

The LSI adopt pipeline copies bundle `docs/workflows/` and overlay docs into `.lsi/workflows/` on the adopter repo. Markdown cross-links in source files often use bundle-relative paths (`../../overlays/lsi/docs/workflows/…`, `../../../docs/adopt-and-update.md`, `../workflows/ticket-card-info.md`) that resolve in the bundle repo but not after flattening into `.lsi/workflows/`.

`rewrite_links()` in `snippets/adopt.py` already normalizes many `docs/workflows/` prefixes. v1.4.0 exposed gaps: overlay-only paths, sdlc→core workflow links, bundle-only maintainer docs, and missing `docs/ci/` copy. Adopt verification (link checks or manual re-run) failed until both source docs and rewrite rules were fixed.

## Goals / Non-Goals

**Goals:**

- Adopted `.lsi/workflows/` markdown links resolve to sibling files under the adopted tree.
- Bundle-only references (maintainer gitignored files, patch docs) appear as plain text in adopters, not broken links.
- CI workflow templates under `docs/ci/` are copied to `.lsi/workflows/ci/` during adopt.

**Non-Goals:**

- Rewriting links inside adopter application repos outside `.lsi/workflows/`.
- Adding automated link-check CI to the bundle repo (manual adopt re-run is sufficient for this fix).
- Changing adopt token substitution or patch config semantics.

## Decisions

### 1. Fix source docs to adopted-local paths where possible

**Choice:** Update bundle and overlay source markdown to use paths that are correct *after* adopt (e.g. `openspec-git-integration.md`, `../ticket-card-info.md`, `adopt-and-update.md`).

**Rationale:** Source docs remain readable in the bundle repo (overlay paths still work via sibling layout) and reduce reliance on rewrite regex edge cases.

**Alternative:** Rely only on `LINK_REWRITES` — rejected because maintainers reading source in-repo would see odd paths, and regex tables grow harder to audit.

### 2. Extend `LINK_REWRITES` for remaining bundle-only prefixes

**Choice:** Add regex entries for `../../overlays/lsi/docs/workflows/`, `../../../docs/adopt-and-update.md`, and `../workflows/ticket-card-info.md` in `LINK_REWRITES`.

**Rationale:** Catches legacy links in files not yet updated and overlay copies that still reference bundle layout.

### 3. Inline bundle-only links as plain text

**Choice:** Replace links to `MAINTAINER.md.example`, `patches/README.md`, and `adopt-new-repo.md` with backtick references noting they live in the cursor-dev-workflows bundle.

**Rationale:** These files are not copied to adopters; a dead link is worse than an explicit bundle-only note.

### 4. Copy `docs/ci/` in `copy_core_bundle`

**Choice:** After adopt guide copy, `copy_tree(docs/ci, .lsi/workflows/ci, transform)`.

**Rationale:** CI templates are part of the adopted workflow bundle; adopters reference them from adopted docs. Same transform applies token substitution and link rewrite if needed.

## Risks / Trade-offs

- **[Risk] New overlay links use untested bundle paths** → Mitigation: prefer adopted-local paths in new docs; extend `LINK_REWRITES` when overlay layout differs.
- **[Risk] Regex rewrite order conflicts** → Mitigation: more specific patterns before generic `../workflows/` rewrite; existing ordered list preserved.
- **[Trade-off] Bundle-only refs lose click-through in adopters** → Acceptable; adopters should not depend on maintainer-only files.

## Migration Plan

1. Merge fix on a feature branch; bump bundle to v1.4.0 if not already released with these fixes.
2. Re-run `adopt.py --target <adopter>` or `/lsi:update` on each adopter.
3. Spot-check `.lsi/workflows/` links and presence of `.lsi/workflows/ci/`.

Rollback: revert adopt.py and source doc changes; re-adopt from prior bundle tag.

## Open Questions

- None — implementation matches uncommitted working tree.
