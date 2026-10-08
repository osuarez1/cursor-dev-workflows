# address-findings-commands Specification

## Purpose
TBD - created by archiving change human-bot-lifecycle-v2. Update Purpose after archive.
## Requirements
### Requirement: Address-findings slash commands

The LSI agent stack SHALL provide slash commands that resolve findings from senior analysis, code review, OpenSpec verify, and PR readiness. Standalone, each command SHALL commit through the `/lsi:commit` workflow only when the user asks. When invoked as a step of a bot session with fixing enabled (`/lsi:pr-bot --fix`, `/lsi:pr-bot-docs --fix`, `/lsi:apply-bot`), the session's commit gate SHALL commit the command's edits under the bot identity, and the command SHALL NOT push by itself.

#### Scenario: Address senior

- **WHEN** a user invokes `/lsi:address-senior` after `/lsi:senior`
- **THEN** the agent addresses recommended design/doc updates for OpenSpec artifacts
- **AND** commits through the `/lsi:commit` workflow only when the user asks
- **AND** emits a summary table of documentation changes

#### Scenario: Address review

- **WHEN** a user invokes `/lsi:address-review` after `/lsi:review`
- **THEN** the agent addresses blocker, major, minor, and nit findings at their stated locations
- **AND** commits only when the user asks, and emits a summary table

#### Scenario: Address verify

- **WHEN** a user invokes `/lsi:address-verify` after `/opsx:verify`
- **THEN** the agent closes implementation gaps against proposal, design, and tasks
- **AND** commits only when the user asks, and emits a summary table

#### Scenario: Address readiness

- **WHEN** a user invokes `/lsi:address-readiness` after a Needs fixes or Blocked readiness verdict
- **THEN** the agent resolves the listed gate failures until local checks pass
- **AND** commits only when the user asks, and emits a summary table

#### Scenario: Address step inside a fixing bot session

- **WHEN** `/lsi:address-review` runs as a step of `/lsi:pr-bot --fix`
- **THEN** its edits are committed by the session commit gate under the bot identity
- **AND** the address command itself does not push


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

