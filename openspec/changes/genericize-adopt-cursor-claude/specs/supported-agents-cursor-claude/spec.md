## ADDED Requirements

### Requirement: Bundle emits only Cursor and Claude agent artifacts

The bundle repository and `snippets/adopt.py` SHALL install agent-stack output only for **Cursor** (`.cursor/commands/`, `.cursor/rules/`) and optionally **Claude** (`.claude/commands/`). They SHALL NOT emit OpenCode, JetBrains AI, Junie, or workflow shell wrapper directories.

#### Scenario: Adopt output has no forbidden agent directories

- **WHEN** `adopt.py` completes against a registered patch config
- **THEN** the adopter repo SHALL NOT contain `.opencode/`, `.aiassistant/`, `.junie/`, or workflow `bin/lsi-*` / `bin/opsx-*` installed by adopt

#### Scenario: Bundle tree has no forbidden agent directories

- **WHEN** the bundle repository is scanned at release gate time
- **THEN** `.opencode/`, `.aiassistant/`, `.junie/`, and `bin/lsi-*` / `bin/opsx-*` SHALL NOT exist in the bundle git tree

#### Scenario: Legacy multi-tool YAML keys are rejected

- **WHEN** `adopt.py` loads a patch config containing `agents_opencode`, `agents_junie`, `agents_jetbrains`, or `bin` keys
- **THEN** adopt SHALL exit with an error explaining Cursor + Claude only policy

#### Scenario: Supported-agents regression test passes

- **WHEN** `python3 snippets/test_supported_agents_only.py` runs before a `VERSION` bump
- **THEN** exit code is `0`
