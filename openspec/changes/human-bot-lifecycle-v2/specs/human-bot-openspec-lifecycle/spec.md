## ADDED Requirements

### Requirement: Human and bot lifecycle lanes

The OpenSpec + Git overlay SHALL define three lanes: human shaping (steps 1–8), coding-agent bot implementation (steps 9–19), and human close/promote/release (steps 20–24).

#### Scenario: Documented lane split

- **WHEN** an agent or human reads `openspec-git-integration.md` lifecycle
- **THEN** the document SHALL list human steps through mode-A docs PR and merge-desc, bot steps from `/opsx:apply` through mode-B staging PR and merge-desc, and human steps for staging QA, `/lsi:close`, `/lsi:promote`, merge-desc, and optional release-train
- **AND** the document SHALL state that coding agents execute the bot lane using the shared bot playbook

### Requirement: Close before promote

After staging QA and CI pass, a human SHALL run `/lsi:close` before `/lsi:promote`. Promote SHALL merge already-closed work so main requires no sync/archive for that change.

#### Scenario: Close precedes promote

- **WHEN** staging QA and CI have passed for a change
- **THEN** `/lsi:close` is the next lifecycle step before `/lsi:promote`
- **AND** `/lsi:promote` output SHALL NOT instruct `/lsi:close` on `main` after merge

#### Scenario: Staging issues after close are follow-ups

- **WHEN** a defect is found on staging after the change was closed
- **THEN** the defect SHALL be tracked as a new OpenSpec change (follow-up), not by reopening the archived folder as the primary workflow

### Requirement: Close allowed off main

`/lsi:close` SHALL run on the ticket-linked development branch (with staging validation confirmed), not exclusively on `main`. When promoting work that accumulated on `staging`, the human SHALL merge staging into the ticket branch before `/lsi:close` (not close while checked out on bare `staging`).

#### Scenario: Close on ticket branch

- **WHEN** a user invokes `/lsi:close` on a ticket branch after confirming staging QA passed
- **THEN** the command proceeds with sync (if needed), archive, CLOSED.md update, and commit handoff
- **AND** the command does not refuse solely because the branch is not `main`

#### Scenario: Accumulated staging uses ticket branch with merge

- **WHEN** promote will carry multiple staging-validated commits for the change
- **THEN** `/lsi:close` runs on the ticket branch after staging is merged into that branch
- **AND** the lifecycle docs do not require closing while checked out on `staging`

### Requirement: PR modes A B and C

`/lsi:pr` SHALL support modes A (`openspec/` tree only), B (implementation with optional OpenSpec edits), and C (full docs + implementation for tiny tasks).

#### Scenario: Mode A is openspec-only

- **WHEN** `/lsi:pr` runs in mode A and the diff touches any path outside `openspec/`
- **THEN** the command SHALL refuse mode A and instruct the user to use mode B or C

#### Scenario: Mode A rejects source changes

- **WHEN** `/lsi:pr` runs in mode A and the diff touches `SOURCE_ROOT` paths from PROJECT.md
- **THEN** the command SHALL refuse mode A and instruct the user to use mode B or C

#### Scenario: Mode C gate uses PROJECT tokens

- **WHEN** `/lsi:pr` runs in mode C
- **THEN** the command SHALL warn when changed lines or files exceed `PR_WARN_LINES` / `PR_WARN_FILES`
- **AND** the command SHALL refuse when changed lines > `PR_MAX_LINES` or files > `PR_MAX_FILES`

#### Scenario: Mode C token defaults when unset

- **WHEN** Mode C runs and PROJECT/patch tokens omit `PR_WARN_*` / `PR_MAX_*`
- **THEN** the command SHALL use template defaults `PR_WARN_FILES=15`, `PR_WARN_LINES=250`, `PR_MAX_FILES=25`, `PR_MAX_LINES=400`

#### Scenario: Normal path requires mode A then mode B

- **WHEN** a change is not explicitly opted into mode C
- **THEN** the lifecycle SHALL require a mode-A docs PR before a mode-B implementation PR

### Requirement: Initial docs commit baseline

After `/opsx:propose` artifacts exist and a ticket branch is available, the human lane SHALL commit the initial OpenSpec docs before senior analysis edits so later diffs show senior-driven changes.

#### Scenario: Commit before senior

- **WHEN** the human lane reaches the commit step after card creation
- **THEN** `/lsi:commit` (or equivalent) records the initial proposal/design/tasks/specs commit before `/lsi:senior`

### Requirement: Shared bot playbook

The bundle SHALL ship a bot-lane playbook artifact that enumerates steps 9–19 for Cursor, Claude Code, and OpenCode.

#### Scenario: Playbook lists bot steps only

- **WHEN** an agent loads the bot playbook
- **THEN** the playbook SHALL include apply, commit, review (which may auto-chain Prowler), address loops, verify, readiness, mode-B PR, and merge-desc as an ordered checklist
- **AND** the playbook SHALL forbid promote, release-train, and close (human lane)
- **AND** individual slash commands SHALL NOT restate that order as a Next footer (sequencing lives in the playbook/lifecycle docs; documented deliverable nesting is allowed)
