## ADDED Requirements

### Requirement: Address-findings slash commands

The LSI agent stack SHALL provide slash commands that resolve findings from senior analysis, code review, OpenSpec verify, and PR readiness, then invoke `/lsi:commit` for logical commits.

#### Scenario: Address senior

- **WHEN** a user invokes `/lsi:address-senior` after `/lsi:senior`
- **THEN** the agent addresses recommended design/doc updates for OpenSpec artifacts
- **AND** then runs the `/lsi:commit` workflow
- **AND** emits a summary table of documentation changes

#### Scenario: Address review

- **WHEN** a user invokes `/lsi:address-review` after `/lsi:review`
- **THEN** the agent addresses blocker, major, minor, and nit findings at their stated locations
- **AND** then runs `/lsi:commit` and emits a summary table

#### Scenario: Address verify

- **WHEN** a user invokes `/lsi:address-verify` after `/opsx:verify`
- **THEN** the agent closes implementation gaps against proposal, design, and tasks
- **AND** then runs `/lsi:commit` and emits a summary table

#### Scenario: Address readiness

- **WHEN** a user invokes `/lsi:address-readiness` after a Needs fixes or Blocked readiness verdict
- **THEN** the agent resolves the listed gate failures until local checks pass
- **AND** then runs `/lsi:commit` and emits a summary table

### Requirement: Optional Prowler gate before review

Before `/lsi:review`, the agent SHALL run or offer `/lsi:address-prowler` when an open Bitbucket PR already contains a Prowler · Grok Bot review comment.

#### Scenario: Prowler review present

- **WHEN** `/lsi:review` is about to run and the open PR has a non-deleted comment whose body begins with `Prowler · Grok Bot review`
- **THEN** the agent SHALL invoke `/lsi:address-prowler` (or instruct the user to) before completing `/lsi:review`

#### Scenario: No Prowler review

- **WHEN** there is no open PR or no matching Prowler summary comment
- **THEN** `/lsi:review` proceeds without requiring `/lsi:address-prowler`

### Requirement: Address commands in expected stack

`snippets/expected_agent_stack.py` (or equivalent) SHALL list the address-* command files among expected LSI commands for adopter parity.

#### Scenario: Parity expects address commands

- **WHEN** `verify-adopters.py` runs against a synced adopter after this change is adopted
- **THEN** `lsi-address-senior`, `lsi-address-review`, `lsi-address-verify`, `lsi-address-readiness`, and `lsi-address-prowler` are required for parity pass
