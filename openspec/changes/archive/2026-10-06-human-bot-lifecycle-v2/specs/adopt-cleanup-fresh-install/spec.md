## ADDED Requirements

### Requirement: Cleanup script for fresh adopt install

The bundle SHALL provide `cleanup-adopt.sh` that removes adopt-managed LSI agent-stack and regenerable `.lsi/workflows/` artifacts so a subsequent `install-adopt.sh` can perform a fresh install.

#### Scenario: Dry-run lists paths

- **WHEN** an operator runs `cleanup-adopt.sh` without `--yes`
- **THEN** the script lists paths it would remove
- **AND** does not delete any files

#### Scenario: Confirm deletes adopt-managed files

- **WHEN** an operator runs `cleanup-adopt.sh --yes` in an adopter repo
- **THEN** adopt-installed `lsi-*.md` commands and adopt-managed workflow rules under `.cursor/` are removed when present
- **AND** regenerable `.lsi/workflows/` content not listed in patch `preserve` / `preserve_agent_stack` is removed
- **AND** `PROJECT.md` and application source under `SOURCE_ROOT` are not deleted

#### Scenario: Preserve globs survive

- **WHEN** cleanup runs against a patch that lists `preserve` or `preserve_agent_stack` paths
- **THEN** those paths are not removed

### Requirement: Adopt-clean slash command

The LSI agent stack SHALL provide `/lsi:adopt-clean` that runs or documents the cleanup script with confirm, and stops after cleanup (no install, no adopt-verify, no Next footer).

#### Scenario: Clean does not chain install

- **WHEN** a user invokes `/lsi:adopt-clean`
- **THEN** the agent performs only the cleanup deliverable (dry-run or confirmed delete)
- **AND** does not invoke `install-adopt.sh` or `/lsi:adopt-verify` unless the user runs those separately
