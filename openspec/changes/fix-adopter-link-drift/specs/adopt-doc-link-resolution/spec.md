## ADDED Requirements

### Requirement: Adopted workflow docs resolve links within adopter repo

After `snippets/adopt.py` runs against an LSI adopter config, every relative markdown link in `.lsi/workflows/**/*.md` SHALL resolve to an existing file under the adopter `--repo-root`. Links SHALL NOT target bundle-maintainer-only paths (`overlays/lsi/`, `agent-stack/`, `patches/`, `snippets/`, or repo-root `docs/` trees that adopt does not install).

#### Scenario: verify-adopters link gate passes on fresh adopt output

- **WHEN** `adopt.py` completes for a registered patch config (e.g. `patches/_template.yaml` against a temp repo)
- **AND** `adoption-verify-links.py --repo-root <target> --canonical .lsi/workflows` runs
- **THEN** exit code is `0` with no `BROKEN LINKS` output

#### Scenario: Known drift paths are fixed

- **WHEN** adopted `.lsi/workflows/adopt-and-update.md` is scanned
- **THEN** links to CI snippets, maintainer docs, and patch registry do not reference `ci/check_version-*.yml`, `../MAINTAINER.md.example`, `adopt-new-repo.md`, or `../patches/README.md` unless adopt copies those targets into the adopter tree

#### Scenario: Overlay cross-references use canonical sibling paths

- **WHEN** adopted `.lsi/workflows/integrations.md`, `ticket-card-info.md`, or `which-workflow.md` link to OpenSpec or slash-command docs
- **THEN** hrefs use `.lsi/workflows/` sibling paths (e.g. `openspec-git-integration.md`, `git-trello.md`) or adopter-installed paths (e.g. `.cursor/commands/lsi-help.md`), not `../../overlays/lsi/docs/…` or `../../agent-stack/commands/…`

#### Scenario: Adopter router source is overlay merge output

- **WHEN** an LSI adopter runs `adopt.py` with overlay
- **THEN** `.lsi/workflows/which-workflow.md` matches `overlays/lsi/docs/workflows/which-workflow.md` (after link rewrite), not bundle-root `which-workflow.md`
- **AND** maintainers edit the overlay router as authoritative source; bundle-root router remains optional dogfood only

### Requirement: Bundle regression catches link drift before adopter re-sync

The bundle repository SHALL include automated tests that exercise adopt link output (full adopt or deterministic rewrite pass) and fail when known maintainer-path prefixes appear under the simulated `.lsi/workflows/` tree.

#### Scenario: Bundle CI fails on maintainer path in adopt output

- **WHEN** a source workflow doc contains a relative link to `overlays/lsi/` or `agent-stack/` that adopt would copy unchanged into `.lsi/workflows/`
- **AND** the bundle link-regression test runs
- **THEN** the test fails with a message identifying the source file and href

#### Scenario: Pattern rule flags bundle layout inside canonical tree

- **WHEN** `adoption-verify-links.py` scans `.lsi/workflows/` containing `](overlays/lsi/` or `](../../agent-stack/`
- **THEN** the script reports a pattern violation (in addition to or instead of broken-link detection, per design)

#### Scenario: Bundle source grep blocks maintainer paths before adopt

- **WHEN** a maintainer edits `docs/workflows/**/*.md` or `overlays/lsi/docs/workflows/**/*.md`
- **AND** the file contains a markdown link with `](overlays/lsi/` (phase 1) or `](agent-stack/` (phase 2, once overlay workflow sources are clean)
- **THEN** the bundle source grep (pre-commit or CI) fails before adopt runs

#### Scenario: Bundle release blocked without adopt-link regression pass

- **WHEN** a maintainer prepares a bundle `VERSION` / `CHANGELOG.md` bump
- **AND** `python3 snippets/test_adopt_links.py` or `python3 snippets/test_adoption_verify_links.py` fails
- **THEN** the release MUST NOT proceed until both tests pass (local gate and CI when present)

#### Scenario: Bundle CI runs both adopt-link test modules

- **WHEN** the bundle repository has a CI pipeline
- **THEN** every PR runs `python3 snippets/test_adoption_verify_links.py` and `python3 snippets/test_adopt_links.py`
- **AND** merge is blocked when either module fails

#### Scenario: Release note tells adopters to re-sync

- **WHEN** a bundle release changes adopt output or link policy
- **THEN** `CHANGELOG.md` for that version includes a prominent **Adopters** callout stating registered LSI adopters must run **`/lsi:update`** after pulling the bundle release

#### Scenario: Adopter parity before announce

- **WHEN** a bundle release that changes adopt output is tagged
- **AND** the maintainer adopt loop has not yet re-synced all registered adopters with passing `verify-adopters.py`
- **THEN** the maintainer MUST NOT announce the release to adopters until adopt loop completes — adopter parity is the real acceptance test

### Requirement: Maintainer and adopter source docs stay distinguishable

Docs consumed only by bundle maintainers (`docs/adopt-new-repo.md`, `patches/README.md`, `MAINTAINER.md.example`) SHALL NOT be linked from adopted `.lsi/workflows/` with relative paths that assume the bundle repo layout. Adopter-facing guidance SHALL live in or be copied to `.lsi/workflows/` (e.g. `adopt-and-update.md`) with self-contained links.

#### Scenario: adopt-and-update is self-contained in adopter tree

- **WHEN** an adopter opens `.lsi/workflows/adopt-and-update.md`
- **THEN** every relative link targets a file that exists in the adopter repo after adopt (including optional copied CI snippet paths under `.lsi/workflows/` if the design copies them)

#### Scenario: Tier 2 URLs receive BUNDLE_VERSION at adopt

- **WHEN** adopter-docs source contains a tier 2 GitHub URL with `v{{BUNDLE_VERSION}}`
- **AND** `adopt.py` completes against a temp adopter repo
- **THEN** adopted markdown contains `v{VERSION}` with no literal `{{BUNDLE_VERSION}}` placeholder
- **AND** adopter `PROJECT.md` includes `BUNDLE_VERSION` matching the bundle `VERSION` file used for substitution

#### Scenario: Future docs use adopter-docs when layouts diverge

- **WHEN** a bundle doc copied into adopters cannot be authored in the maintainer tree without tier 2 hrefs or fragile rewrites
- **THEN** maintainers add an adopter-shaped copy under `overlays/lsi/adopter-docs/` (mirroring install path) and wire `adopt.py` — rather than extending `LINK_REWRITES`
- **AND** when a **second** dual doc enters `adopter-docs/`, maintainers implement heading lint per task 7.2
