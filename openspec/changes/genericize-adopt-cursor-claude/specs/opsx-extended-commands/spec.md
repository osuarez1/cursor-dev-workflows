## ADDED Requirements

### Requirement: Six OPSX commands ship in agent-stack

The bundle SHALL include six generic OPSX slash commands in `overlays/lsi/agent-stack/commands/`: `opsx-new`, `opsx-ff`, `opsx-continue`, `opsx-onboard`, `opsx-verify`, `opsx-bulk-archive`.

#### Scenario: OPSX commands exist in bundle source

- **WHEN** `overlays/lsi/agent-stack/commands/` is listed
- **THEN** all six `opsx-*.md` files SHALL be present

#### Scenario: sync_opsx installs all opsx commands to Cursor

- **WHEN** `adopt.py` runs with a patch where `sync_opsx: true`
- **THEN** every `opsx-*.md` from agent-stack SHALL be copied to `.cursor/commands/`

#### Scenario: Expected command list includes OPSX commands

- **WHEN** `expected_agent_stack.expected_commands()` runs
- **THEN** the returned set SHALL include all six `opsx-*` command basenames

#### Scenario: Claude commands regenerated from agent-stack

- **WHEN** the Claude-only generator runs after OPSX commands are added
- **THEN** `.claude/commands/` SHALL contain matching OPSX command files
