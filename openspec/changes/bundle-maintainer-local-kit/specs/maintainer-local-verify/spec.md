## ADDED Requirements

### Requirement: Verify script reports local kit health

The bundle SHALL provide `./snippets/verify-maintainer-local.sh` that checks for required gitignored maintainer artifacts and exits non-zero when any are missing.

#### Scenario: Complete kit

- **WHEN** a maintainer runs verify after successful bootstrap
- **THEN** the script prints `OK` for each required path and exits `0` with `RESULT: OK`

#### Scenario: Incomplete kit

- **WHEN** a maintainer runs verify on a clone that has not been bootstrapped
- **THEN** the script prints `MISSING` for each absent path and exits `1` with guidance to run bootstrap

### Requirement: Verify checks minimum required paths

The verify script SHALL assert presence of: `MAINTAINER.md`, `AGENTS-LOCAL.md`, `local-maintainer.mdc`, `local-branch-workflow.mdc`, `local-openspec-git-integration.mdc`, at least one `lsi-*` and one `opsx-*` command, `openspec/config.yaml`, and `openspec/changes/`.

#### Scenario: Required path list

- **WHEN** verify runs
- **THEN** it checks each path in the minimum required set and reports per-item OK or MISSING
