## MODIFIED Requirements

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
