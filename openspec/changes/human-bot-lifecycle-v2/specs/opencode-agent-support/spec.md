## ADDED Requirements

### Requirement: OpenCode agent artifacts

The bundle and `snippets/adopt.py` SHALL emit OpenCode agent artifacts so local models (for example QwenCoder) can follow the same LSI/OpenSpec bot playbook as Cursor and Claude Code.

#### Scenario: Adopt installs OpenCode entry points

- **WHEN** `adopt.py` runs with OpenCode support enabled
- **THEN** the adopter receives OpenCode-readable command or instruction files that cover the bot-lane playbook and core `/lsi:*` / `/opsx:*` entry points
- **AND** Junie, JetBrains AI, and workflow `bin/lsi-*` / `bin/opsx-*` directories are still not installed

#### Scenario: Legacy Junie and JetBrains keys still rejected

- **WHEN** a patch config contains `agents_junie`, `agents_jetbrains`, or `bin` keys
- **THEN** adopt SHALL exit with an error
- **AND** `agents_opencode` SHALL be accepted when present

### Requirement: Supported-agents tests allow OpenCode

Regression tests that previously forbade `.opencode/` SHALL be updated to allow OpenCode while still forbidding Junie, JetBrains, and workflow bin wrappers.

#### Scenario: Supported-agents test passes with OpenCode

- **WHEN** `python3 snippets/test_supported_agents_only.py` (or successor) runs before a VERSION bump after this change
- **THEN** exit code is `0` with `.opencode/` present in the expected emit set
- **AND** the test fails if `.junie/`, `.aiassistant/`, or workflow `bin/lsi-*` appear as adopt outputs
