## ADDED Requirements

### Requirement: Agent-stack commands are stack-neutral

Sources under `overlays/lsi/agent-stack/commands/` SHALL contain workflow mechanics only. They SHALL NOT embed repo-specific domain strings (FastAPI, FFmpeg, Rails version pins, per-repo pytest paths, data-lake scopes, etc.). Domain tables and personas SHALL live in generic `.lsi/workflows/openspec-git-integration.md` baseline or per-repo `patches/files/<repo>/openspec-git-integration.md`.

#### Scenario: Denylist regression test passes

- **WHEN** `python3 snippets/test_commands_generic.py` runs before a `VERSION` bump
- **THEN** exit code is `0` and no agent-stack command source matches the denylist

#### Scenario: Adopted lsi commands are identical across registered repos

- **WHEN** `adopt.py` runs against each registered patch (`web`, `ai-agent`, `video-encoder`) into temp repos
- **THEN** every `.cursor/commands/lsi-*.md` file SHALL be byte-identical across all three temp adopts

#### Scenario: Domain deferral in command sources

- **WHEN** an agent-stack command references commit mapping, code review focus, or test gates
- **THEN** the command SHALL defer to `openspec-git-integration.md` § sections rather than inlining repo-specific tables

#### Scenario: Repo-specific scope lives in integration patch only

- **WHEN** an adopter repo has domain-specific commit scopes or review focus areas
- **THEN** those details SHALL appear only in `.lsi/workflows/openspec-git-integration.md` from `patches/files/<repo>/` overlay, not in shared `lsi-*.md` commands
