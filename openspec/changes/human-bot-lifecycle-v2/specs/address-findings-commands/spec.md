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

### Requirement: Optional Prowler step is separate from review

`/lsi:address-prowler` SHALL be a standalone command. Lifecycle docs and the bot playbook MAY list it before `/lsi:review` when a Prowler · Grok Bot review exists on the PR. `/lsi:review` SHALL NOT auto-invoke `/lsi:address-prowler`.

#### Scenario: Review does not chain Prowler

- **WHEN** a user invokes `/lsi:review`
- **THEN** the agent performs the review deliverable only
- **AND** the agent does not run `/lsi:address-prowler` unless the user invoked that command

#### Scenario: Prowler command is invokable alone

- **WHEN** a user invokes `/lsi:address-prowler` with a PR that has a comment beginning with `Prowler · Grok Bot review`
- **THEN** the agent retrieves and triages those findings per the command source
- **AND** stops after its summary without a Next footer

### Requirement: Address commands in expected stack

`snippets/expected_agent_stack.py` (or equivalent) SHALL list the address-* command files among expected LSI commands for adopter parity.

#### Scenario: Parity expects address commands

- **WHEN** `verify-adopters.py` runs against a synced adopter after this change is adopted
- **THEN** `lsi-address-senior`, `lsi-address-review`, `lsi-address-verify`, `lsi-address-readiness`, and `lsi-address-prowler` are required for parity pass
