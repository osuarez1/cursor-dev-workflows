## ADDED Requirements

### Requirement: Trello card slash commands for existing cards and branches

The LSI agent stack SHALL provide slash commands that cover Trello card flows beyond greenfield `git ts`, with OpenSpec-gated card copy and redaction before Trello API calls.

#### Scenario: Link card to existing branch

- **WHEN** a maintainer runs `/lsi:card-link` on a feature branch with an in-progress OpenSpec change and no 24-char Trello id in the branch name
- **THEN** the agent creates or links a Trello card from redacted OpenSpec artifacts and renames the current branch to `{type}/{id}-<change-slug>` via `git branch -m` (not `git ts`)

#### Scenario: Branch from existing To Do card

- **WHEN** a maintainer runs `/lsi:trello-branch` or confirms `/lsi:trello-list` from `main` or `staging` with an in-progress OpenSpec change
- **THEN** the agent updates the Trello card from redacted OpenSpec artifacts and runs `git tb` followed by branch rename to match the OpenSpec slug

#### Scenario: OpenSpec required for card API paths

- **WHEN** `/lsi:card-link`, `/lsi:trello-branch`, or `/lsi:trello-list` (confirm path) is invoked without an in-progress OpenSpec change
- **THEN** the agent refuses and directs the user to `/opsx:propose`

### Requirement: Adopter parity lists include new commands

`snippets/verify-adopters.py` and `snippets/audit-agent-docs.py` SHALL list all `/lsi:*` commands installed under `overlays/lsi/agent-stack/commands/`, including card-link and trello commands.

#### Scenario: Parity check finds new commands

- **WHEN** `verify-adopters.py` runs against an adopter with a synced agent stack
- **THEN** `lsi-card-link`, `lsi-trello-list`, and `lsi-trello-branch` are included in the expected command set
