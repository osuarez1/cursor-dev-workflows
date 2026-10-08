## MODIFIED Requirements

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
