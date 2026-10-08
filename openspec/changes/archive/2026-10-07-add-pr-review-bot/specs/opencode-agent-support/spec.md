## MODIFIED Requirements

### Requirement: OpenCode agent artifacts

The bundle and `snippets/adopt.py` SHALL emit OpenCode agent artifacts so local models (for example QwenCoder) can follow the same LSI/OpenSpec bot playbook as Cursor and Claude Code. When opted in, every `lsi-*` command SHALL be emitted with its **full** body (not a pointer stub) to `.opencode/commands/lsi-<name>.md` with OpenCode frontmatter (`description`) and the command's input bound to `$ARGUMENTS`.

#### Scenario: Adopt installs OpenCode only when opted in

- **WHEN** `adopt.py` runs with `agents_opencode: { enabled: true }` (or equivalent opt-in)
- **THEN** the adopter receives OpenCode-readable command or instruction files that cover the bot-lane playbook, the bot-session skeleton, and core `/lsi:*` / `/opsx:*` entry points
- **AND** Junie, JetBrains AI, and workflow `bin/lsi-*` / `bin/opsx-*` directories are still not installed

#### Scenario: OpenCode commands carry full bodies

- **WHEN** OpenCode is opted in
- **THEN** `.opencode/commands/lsi-apply-bot.md` contains the same Steps, Output, and Guardrails as `.cursor/commands/lsi-apply-bot.md`
- **AND** does not consist solely of a pointer to `.cursor/commands/`

#### Scenario: Default adopt does not emit OpenCode

- **WHEN** `adopt.py` runs without `agents_opencode` enabled
- **THEN** no `.opencode/` agent-stack artifacts are installed

#### Scenario: Legacy Junie and JetBrains keys still rejected

- **WHEN** a patch config contains `agents_junie`, `agents_jetbrains`, or `bin` keys
- **THEN** adopt SHALL exit with an error
- **AND** `agents_opencode` SHALL be accepted when present as opt-in

### Requirement: Supported-agents tests allow OpenCode when opted in

Regression tests that previously forbade `.opencode/` SHALL be updated to allow OpenCode when opted in, while still forbidding Junie, JetBrains, and workflow bin wrappers. Default (non-opt-in) emit SHALL NOT require `.opencode/`. The adopt-managed API helper directory `.lsi/bin/` SHALL NOT count as a workflow bin wrapper; top-level `bin/lsi-*` and `bin/opsx-*` remain forbidden.

#### Scenario: Supported-agents test passes with OpenCode opt-in

- **WHEN** `python3 snippets/test_supported_agents_only.py` (or successor) runs with OpenCode enabled in the fixture
- **THEN** exit code is `0` with `.opencode/` present in that emit set
- **AND** the test fails if `.junie/`, `.aiassistant/`, or workflow `bin/lsi-*` appear as adopt outputs

#### Scenario: LSI helper directory allowed

- **WHEN** adopt emits `.lsi/bin/lsi-bitbucket`
- **THEN** the supported-agents test passes
- **AND** it still fails if a top-level `bin/` directory is emitted
