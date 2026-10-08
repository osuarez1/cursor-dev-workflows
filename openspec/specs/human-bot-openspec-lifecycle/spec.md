# human-bot-openspec-lifecycle Specification

## Purpose
TBD - created by archiving change human-bot-lifecycle-v2. Update Purpose after archive.
## Requirements
### Requirement: Human and bot lifecycle lanes

The OpenSpec + Git overlay SHALL define three lanes: human shaping (steps 1–8), coding-agent bot implementation (steps 9–19), and human close/promote/release (steps 20–24).

#### Scenario: Documented lane split

- **WHEN** an agent or human reads `openspec-git-integration.md` lifecycle
- **THEN** the document SHALL list human steps through mode-A docs PR and merge-desc, bot steps from `/opsx:apply` through mode-B staging PR and merge-desc, and human steps for staging QA, `/lsi:promote`, merge-desc, `/lsi:close` on `main`, and optional release-train
- **AND** the document SHALL state that coding agents execute the bot lane using the shared bot playbook

### Requirement: Close after promote on main

After staging QA and CI pass, a human SHALL run `/lsi:promote` while the change is still active. After the promotion PR merges to `main`, a human SHALL run `/lsi:close` on **`main` only** (sync + archive + CLOSED.md). `/lsi:promote` SHALL NOT require close beforehand.

#### Scenario: Promote precedes close

- **WHEN** staging QA and CI have passed for a change
- **THEN** `/lsi:promote` is the next lifecycle step
- **AND** `/lsi:close` runs on `main` after the promotion merge

#### Scenario: Staging issues after promote are follow-ups

- **WHEN** a defect is found on staging after promotion (before or after close)
- **THEN** the defect SHALL be tracked as a new OpenSpec change (follow-up), not by reopening the archived folder as the primary workflow

### Requirement: Close requires main

`/lsi:close` SHALL refuse unless the current branch is `main` and the user confirms the promotion PR for the change has merged. It SHALL refuse ticket branches and bare `staging`.

#### Scenario: Close on main after promotion

- **WHEN** a user invokes `/lsi:close` on `main` after confirming the promotion merge and prior staging QA
- **THEN** the command proceeds with sync (if needed), archive, CLOSED.md update, and commit handoff

#### Scenario: Close refused off main

- **WHEN** a user invokes `/lsi:close` on a ticket branch or `staging`
- **THEN** the command refuses with a fix to merge the promotion PR and re-run on `main`

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

