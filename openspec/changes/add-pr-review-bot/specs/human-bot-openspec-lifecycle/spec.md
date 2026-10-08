## REMOVED Requirements

### Requirement: Close before promote

### Requirement: Close allowed off main

## ADDED Requirements

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

## MODIFIED Requirements

### Requirement: Human and bot lifecycle lanes

The OpenSpec + Git overlay SHALL define three lanes: human shaping (steps 1–8), coding-agent bot implementation (steps 9–19), and human close/promote/release (steps 20–24).

#### Scenario: Documented lane split

- **WHEN** an agent or human reads `openspec-git-integration.md` lifecycle
- **THEN** the document SHALL list human steps through mode-A docs PR and merge-desc, bot steps from `/opsx:apply` through mode-B staging PR and merge-desc, and human steps for staging QA, `/lsi:promote`, merge-desc, `/lsi:close` on `main`, and optional release-train
- **AND** the document SHALL state that coding agents execute the bot lane using the shared bot playbook

### Requirement: Shared bot playbook

The bundle SHALL ship a bot-lane playbook artifact that enumerates steps 9–19 for Cursor, Claude Code, and OpenCode, and a bot-session skeleton (`overlays/lsi/agent-stack/bot-sessions.md`) shared by `/lsi:pr-bot-docs`, `/lsi:apply-bot`, and `/lsi:pr-bot`.

#### Scenario: Playbook lists bot steps only

- **WHEN** an agent loads the bot playbook
- **THEN** the playbook SHALL include apply, commit, review (which may auto-chain Prowler), address loops, verify, readiness, mode-B PR, and merge-desc as an ordered checklist
- **AND** the playbook SHALL forbid promote, release-train, and close (human lane)
- **AND** individual slash commands SHALL NOT restate that order as a Next footer (sequencing lives in the playbook/lifecycle docs; documented deliverable nesting is allowed)

#### Scenario: Playbook names the automated sessions

- **WHEN** an agent loads the bot playbook
- **THEN** it SHALL state that `/lsi:apply-bot` automates steps 9–18 end to end with human checkpoints
- **AND** that `/lsi:pr-bot-docs` reviews the Mode A PR (human lane step 7, including `/lsi:readiness`) and `/lsi:pr-bot` reviews Mode B and Mode C PRs (including `/lsi:readiness`)

#### Scenario: Lifecycle doc places bot sessions

- **WHEN** a reader opens the Lifecycle section of `openspec-git-integration.md`
- **THEN** `/lsi:pr-bot-docs` appears at Mode A PR review, `/lsi:apply-bot` at the bot lane, and `/lsi:pr-bot` at Mode B/C PR review
