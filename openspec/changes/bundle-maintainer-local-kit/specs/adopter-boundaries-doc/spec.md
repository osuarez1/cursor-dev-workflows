## ADDED Requirements

### Requirement: Adopter boundaries are documented in tracked docs

The bundle SHALL ship `docs/adopter-boundaries.md` describing three zones: what `adopt.py` manages, what it never touches, and what is bundle-maintainer-only (gitignored local kit).

#### Scenario: Adopter reads boundaries

- **WHEN** an adopter or maintainer opens `docs/adopter-boundaries.md`
- **THEN** they see explicit lists for adopt-managed paths, adopt-never paths, human-maintained per-repo paths, and bundle-maintainer-only gitignored paths
- **AND** the doc links to `snippets/maintainer-local/README.md` for bootstrap instructions

### Requirement: Entry points reference maintainer kit without requiring it for adopters

`AGENTS.md` and `README.md` SHALL document the optional maintainer bootstrap for bundle repo maintainers and SHALL NOT imply adopters must install the local kit.

#### Scenario: Agent reads AGENTS.md in bundle repo

- **WHEN** an agent starts at `AGENTS.md` in cursor-dev-workflows
- **THEN** it finds bootstrap and verify commands under a maintainer-only section
- **AND** it is instructed not to run `adopt.py --target .` on the bundle repo
