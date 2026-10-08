## ADDED Requirements

### Requirement: Parity gate detects surplus and duplicate agent-stack files

`audit-agent-docs.py` (via `verify-adopters.py` and `/lsi:update`) SHALL compare adopter `.cursor/commands/` and `.cursor/rules/` against the expected set derived from bundle sources plus patch `rule_overlays`. It SHALL report missing expected files (warn), surplus files not in expected set (error until resolved), and legacy alias pairs both present (error until resolved).

#### Scenario: Surplus command is reported

- **WHEN** an adopter has an extra `.cursor/commands/legacy-helper.md` (a bundle-managed-namespace command not in the expected set) not covered by `preserve_agent_stack`
- **THEN** `check_agent_stack_parity` SHALL report an error with the actionable path list

#### Scenario: OpenSpec commands are exempt from surplus detection

- **WHEN** an adopter has `.cursor/commands/opsx-*.md` files (owned by OpenSpec)
- **THEN** `check_agent_stack_parity` SHALL NOT report them as surplus

#### Scenario: Legacy alias pair is reported

- **WHEN** both `code_review.mdc` and `code-review.mdc` exist in `.cursor/rules/`
- **THEN** `check_agent_stack_parity` SHALL report an error until one is removed or allowlisted

#### Scenario: Adopt does not silently delete surplus files

- **WHEN** `adopt.py` runs against an adopter with surplus commands or rules
- **THEN** surplus files SHALL remain on disk
- **AND** only bundle-managed paths SHALL be overwritten

#### Scenario: remove_after_adopt deletes only pre-listed paths

- **WHEN** `adopt.py` runs with `remove_after_adopt` listing `code_review.mdc` in patch YAML
- **THEN** that path SHALL be deleted without interactive prompt
- **AND** other surplus files not in `remove_after_adopt` SHALL NOT be deleted

#### Scenario: Interactive removal requires adopter confirmation

- **WHEN** `/lsi:update` finds unresolved surplus after adopt
- **THEN** `update-workflows.py` SHALL list each surplus path and delete only paths the adopter explicitly confirms
- **AND** verify SHALL NOT report PASS while unresolved surplus remains unless `preserve_agent_stack` allowlists them

#### Scenario: Parity regression test passes

- **WHEN** `python3 snippets/test_adopt_command_rule_parity.py` runs before a `VERSION` bump
- **THEN** exit code is `0`

## MODIFIED Requirements

### Requirement: Adopt link and command parity across adopters

The bundle regression suite SHALL verify that adopted `lsi-*.md` commands are identical across registered repos and that domain differences appear only in `openspec-git-integration.md` patch overlays.

#### Scenario: test_adopt_links command parity assertion

- **WHEN** `python3 snippets/test_adopt_links.py` runs after this change
- **THEN** temp adopts for registered patches SHALL assert byte-identical `lsi-*.md` commands
- **AND** domain strings SHALL appear only in per-repo integration doc overlays
