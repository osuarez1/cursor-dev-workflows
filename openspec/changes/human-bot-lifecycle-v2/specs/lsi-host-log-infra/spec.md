## ADDED Requirements

### Requirement: Infra-only host-log skill

The bundle SHALL ship the `lsi-host-log` Cursor skill only through the infra adopter patch, not as a global agent-stack install for all repos.

#### Scenario: Infra adopt installs skill

- **WHEN** `adopt.py` runs with `patches/infra.yaml` (or successor infra patch)
- **THEN** the infra adopter receives the `lsi-host-log` skill under `.cursor/skills/lsi-host-log/`
- **AND** a non-infra adopter adopt does not install that skill

#### Scenario: Update preserves infra skill

- **WHEN** `/lsi:update` re-syncs infra
- **THEN** the host-log skill remains present (via patch install or `preserve_agent_stack`)
- **AND** parity does not fail solely because the skill exists on infra
