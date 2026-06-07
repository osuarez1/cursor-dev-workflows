## ADDED Requirements

### Requirement: Adopt rewrites overlay and bundle layout links to adopted paths

During LSI adopt, `rewrite_links` SHALL normalize markdown links that reference bundle-only directory layouts so adopted files under `.lsi/workflows/` point at sibling workflow docs.

#### Scenario: Overlay workflow path rewritten

- **WHEN** adopted content contains `](../../overlays/lsi/docs/workflows/openspec-git-integration.md)`
- **THEN** the link target becomes `](openspec-git-integration.md)`

#### Scenario: Deep adopt-and-update path rewritten

- **WHEN** adopted overlay content contains `](../../../docs/adopt-and-update.md)`
- **THEN** the link target becomes `](adopt-and-update.md)`

#### Scenario: Sdlc ticket-card path rewritten

- **WHEN** adopted sdlc content contains `](../workflows/ticket-card-info.md)`
- **THEN** the link target becomes `](../ticket-card-info.md)`

### Requirement: Adopt strips bundle-only maintainer links

Links to files that are not copied into adopter repos SHALL be replaced with plain-text bundle references during adopt, not left as broken relative URLs.

#### Scenario: MAINTAINER example link inlined

- **WHEN** adopted content links to `../MAINTAINER.md.example`
- **THEN** the markdown link is replaced with a backtick reference indicating `MAINTAINER.md` lives in the cursor-dev-workflows bundle (gitignored)

#### Scenario: Patches README link inlined

- **WHEN** adopted content links to `../patches/README.md`
- **THEN** the markdown link is replaced with a backtick reference indicating `patches/README.md` lives in the cursor-dev-workflows bundle

#### Scenario: adopt-new-repo link inlined

- **WHEN** adopted content links to `adopt-new-repo.md` as a relative file
- **THEN** the markdown link is replaced with a backtick reference to `docs/adopt-new-repo.md` in the cursor-dev-workflows bundle

### Requirement: Adopt copies CI workflow templates

The adopt pipeline SHALL copy bundle `docs/ci/` into the adopter at `.lsi/workflows/ci/` when the source directory exists.

#### Scenario: CI templates present after adopt

- **WHEN** `adopt.py` runs against a target repo and `docs/ci/` exists in the bundle
- **THEN** `.lsi/workflows/ci/` on the target contains the same files as bundle `docs/ci/` (with token substitution and link rewrite applied per file)

#### Scenario: Missing CI directory is non-fatal

- **WHEN** bundle `docs/ci/` does not exist
- **THEN** adopt completes without creating `.lsi/workflows/ci/`

### Requirement: Source workflow docs use adopted-local cross-links

Bundle and overlay source markdown that is copied into `.lsi/workflows/` SHALL use relative links valid in the adopted flat layout for core workflow cross-references introduced or fixed in this change.

#### Scenario: integrations.md OpenSpec routing link

- **WHEN** maintainers read `docs/workflows/integrations.md` OpenSpec routing reference
- **THEN** the link target is `openspec-git-integration.md` (not `../../overlays/lsi/docs/workflows/…`)

#### Scenario: ticket-card-info.md OpenSpec link

- **WHEN** maintainers read `docs/workflows/ticket-card-info.md` OpenSpec reference
- **THEN** the link target is `openspec-git-integration.md` (not an overlay bundle path)

#### Scenario: git-trello.md ticket-card link

- **WHEN** maintainers read `overlays/lsi/docs/sdlc/git-trello.md` card description reference
- **THEN** the link target is `../ticket-card-info.md`

#### Scenario: overlay which-workflow adopt link

- **WHEN** maintainers read `overlays/lsi/docs/workflows/which-workflow.md` re-sync row
- **THEN** the link target is `adopt-and-update.md` (not `../../../docs/adopt-and-update.md`)
