## ADDED Requirements

### Requirement: Bundle does not ship OpenSpec commands

The bundle SHALL NOT contain `opsx-*` slash command sources. OpenSpec commands are owned by OpenSpec (`openspec init` / config profile).

#### Scenario: No opsx command sources in bundle

- **WHEN** `overlays/lsi/agent-stack/commands/` is listed
- **THEN** no `opsx-*.md` files SHALL be present

#### Scenario: No opsx commands in generated Claude tree

- **WHEN** `.claude/commands/` is listed
- **THEN** no `opsx/` subtree or `opsx-*` command files SHALL be present

### Requirement: Adopt installs LSI commands only

`adopt.py` SHALL install only `lsi-*` slash commands to `.cursor/commands/` and SHALL NOT install or remove `opsx-*` commands.

#### Scenario: Adopt writes no opsx commands

- **WHEN** `adopt.py` runs for any patch config
- **THEN** `.cursor/commands/` SHALL contain the `lsi-*` commands
- **AND** no `opsx-*.md` file SHALL be written by adopt

#### Scenario: Adopt leaves adopter-owned opsx commands untouched

- **WHEN** an adopter already has `opsx-*` commands (e.g. from `openspec init`)
- **AND** `adopt.py` runs
- **THEN** those `opsx-*` files SHALL remain unchanged

### Requirement: Parity gate ignores the opsx namespace

`expected_commands()` SHALL exclude `opsx-*`, and `check_agent_stack_parity()` SHALL never report `opsx-*` commands as missing or surplus.

#### Scenario: Expected command set excludes opsx

- **WHEN** `expected_agent_stack.expected_commands()` runs
- **THEN** the returned set SHALL contain only `lsi-*` basenames and no `opsx-*` basenames

#### Scenario: Surplus opsx command is not flagged

- **WHEN** an adopter has an `opsx-*` command not produced by the bundle
- **AND** `check_agent_stack_parity()` runs
- **THEN** no `agent_stack_parity` ERROR SHALL be raised for that `opsx-*` command
