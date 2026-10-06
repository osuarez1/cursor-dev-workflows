# address-findings-commands Specification

## Purpose
TBD - created by archiving change human-bot-lifecycle-v2. Update Purpose after archive.
## Requirements
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

### Requirement: Review may auto-chain Prowler when a matching comment exists

`/lsi:address-prowler` SHALL remain a standalone command. `/lsi:review` SHALL auto-invoke `/lsi:address-prowler` first when an open Bitbucket PR has a comment body starting with `Prowler · Grok Bot review`, then continue with the review deliverable. When no PR or no matching comment exists, `/lsi:review` SHALL skip Prowler and run the review only. Neither path SHALL emit a Next footer.

#### Scenario: Review auto-chains Prowler

- **WHEN** a user invokes `/lsi:review` and the open PR has a comment beginning with `Prowler · Grok Bot review`
- **THEN** the agent runs `/lsi:address-prowler` (or equivalent triage) before the review findings
- **AND** then emits the structured code-review Output
- **AND** does not emit a Next footer

#### Scenario: Review skips Prowler when absent

- **WHEN** a user invokes `/lsi:review` and there is no PR or no matching Prowler comment
- **THEN** the agent performs the review deliverable only

#### Scenario: Prowler command is invokable alone

- **WHEN** a user invokes `/lsi:address-prowler` with a PR that has a comment beginning with `Prowler · Grok Bot review`
- **THEN** the agent retrieves and triages those findings per the command source
- **AND** stops after its summary without a Next footer

### Requirement: Address commands in expected stack

`snippets/expected_agent_stack.py` (or equivalent) SHALL list the address-* command files among expected LSI commands for adopter parity.

#### Scenario: Parity expects address commands

- **WHEN** `verify-adopters.py` runs against a synced adopter after this change is adopted
- **THEN** `lsi-address-senior`, `lsi-address-review`, `lsi-address-verify`, `lsi-address-readiness`, and `lsi-address-prowler` are required for parity pass

