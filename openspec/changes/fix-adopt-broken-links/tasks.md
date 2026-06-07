## 1. Source doc link fixes

- [x] 1.1 Update `docs/workflows/integrations.md` OpenSpec routing link to `openspec-git-integration.md`
- [x] 1.2 Update `docs/workflows/ticket-card-info.md` OpenSpec link to `openspec-git-integration.md`
- [x] 1.3 Update `overlays/lsi/docs/sdlc/git-trello.md` ticket-card link to `../ticket-card-info.md`
- [x] 1.4 Update `overlays/lsi/docs/workflows/which-workflow.md` adopt row link to `adopt-and-update.md`

## 2. adopt.py link rewrites

- [x] 2.1 Add `LINK_REWRITES` entries for `../../overlays/lsi/docs/workflows/`, `../../../docs/adopt-and-update.md`, and `../workflows/ticket-card-info.md`
- [x] 2.2 Inline bundle-only links for `MAINTAINER.md.example`, `patches/README.md`, and `adopt-new-repo.md` in `rewrite_links`

## 3. adopt.py CI copy

- [x] 3.1 Copy bundle `docs/ci/` to `.lsi/workflows/ci/` in `copy_core_bundle` when source exists

## 4. Verification

- [x] 4.1 Re-run adopt against a test adopter and confirm `.lsi/workflows/` cross-links resolve
- [x] 4.2 Confirm `.lsi/workflows/ci/` contains CI template files after adopt
