# opencode-agent-support Specification

## Purpose
TBD - created by archiving change human-bot-lifecycle-v2. Update Purpose after archive.
## Requirements
### Requirement: OpenCode agent artifacts

The bundle and `snippets/adopt.py` SHALL emit OpenCode agent artifacts so local models (for example QwenCoder) can follow the same LSI/OpenSpec bot playbook as Cursor and Claude Code.

#### Scenario: Adopt installs OpenCode only when opted in

- **WHEN** `adopt.py` runs with `agents_opencode: { enabled: true }` (or equivalent opt-in)
- **THEN** the adopter receives OpenCode-readable command or instruction files that cover the bot-lane playbook and core `/lsi:*` / `/opsx:*` entry points
- **AND** Junie, JetBrains AI, and workflow `bin/lsi-*` / `bin/opsx-*` directories are still not installed

#### Scenario: Default adopt does not emit OpenCode

- **WHEN** `adopt.py` runs without `agents_opencode` enabled
- **THEN** no `.opencode/` agent-stack artifacts are installed

#### Scenario: Legacy Junie and JetBrains keys still rejected

- **WHEN** a patch config contains `agents_junie`, `agents_jetbrains`, or `bin` keys
- **THEN** adopt SHALL exit with an error
- **AND** `agents_opencode` SHALL be accepted when present as opt-in

### Requirement: Supported-agents tests allow OpenCode when opted in

Regression tests that previously forbade `.opencode/` SHALL be updated to allow OpenCode when opted in, while still forbidding Junie, JetBrains, and workflow bin wrappers. Default (non-opt-in) emit SHALL NOT require `.opencode/`.

#### Scenario: Supported-agents test passes with OpenCode opt-in

- **WHEN** `python3 snippets/test_supported_agents_only.py` (or successor) runs with OpenCode enabled in the fixture
- **THEN** exit code is `0` with `.opencode/` present in that emit set
- **AND** the test fails if `.junie/`, `.aiassistant/`, or workflow `bin/lsi-*` appear as adopt outputs

