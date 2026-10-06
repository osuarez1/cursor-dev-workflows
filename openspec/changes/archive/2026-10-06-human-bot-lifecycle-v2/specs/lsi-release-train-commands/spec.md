## ADDED Requirements

### Requirement: Release-train command family in overlay

The shared LSI agent stack SHALL include `/lsi:release-train`, `/lsi:release-summary`, and `/lsi:change-summary` (upstreamed from web/infra local commands), with bundle-relative paths.

#### Scenario: Commands present after adopt

- **WHEN** an adopter syncs the agent stack after this change
- **THEN** `.cursor/commands/` contains `lsi-release-train.md`, `lsi-release-summary.md`, and `lsi-change-summary.md`
- **AND** expected-agent-stack parity requires those files

#### Scenario: Release-train stays on main

- **WHEN** `/lsi:release-train` is invoked off `main`
- **THEN** the command refuses and does not bump version, rewrite changelog, or tag
