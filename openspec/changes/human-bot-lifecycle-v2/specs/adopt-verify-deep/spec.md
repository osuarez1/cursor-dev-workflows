## ADDED Requirements

### Requirement: Adopt-verify slash command

The LSI agent stack SHALL provide `/lsi:adopt-verify` that runs structural adopter verification and a deep accuracy review for hallucinated or drifted adopt content.

#### Scenario: Structural layer runs

- **WHEN** a user invokes `/lsi:adopt-verify` in an adopter repo
- **THEN** the agent runs `verify-adopters.py` (parity, links, audit) against the repo
- **AND** reports PASS/FAIL for the structural layer

#### Scenario: Deep accuracy layer

- **WHEN** `/lsi:adopt-verify` runs the deep layer
- **THEN** the agent compares `PROJECT.md` tokens to repo reality (protected branches, test command presence, source roots, remote)
- **AND** flags unresolved `{{…}}` placeholders, wrong-repo domain copy, and AGENTS domain claims that contradict the codebase
- **AND** emits a findings table with severity and recommended fixes
- **AND** does not auto-commit fixes

### Requirement: Update recommends adopt-verify

`/lsi:update` SHALL instruct the user to run `/lsi:adopt-verify` after a successful adopt/bootstrap sync and SHALL provide commit-command suggestions for review.

#### Scenario: Post-update next step

- **WHEN** `/lsi:update` completes a sync with file changes
- **THEN** the output asks the user to review the diff, run `/lsi:adopt-verify`, and shows pasteable commit commands
- **AND** the agent does not auto-commit
