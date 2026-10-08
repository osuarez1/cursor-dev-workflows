# claude-code-adopter-commands Specification

## Purpose
Adopt emits /lsi:* Claude Code commands under .claude/commands/lsi/.

## Requirements
### Requirement: Adopt emits Claude Code LSI commands

`snippets/adopt.py` SHALL install every `overlays/lsi/agent-stack/commands/lsi-*.md` as `.claude/commands/lsi/<name>.md` (invoked as `/lsi:<name>`) in adopters, using the same token substitution and link rewriting as the Cursor emit, with Claude frontmatter reduced to `description`. The transform SHALL live in one shared module used by both `adopt.py` and `snippets/install-maintainer-local.py`.

#### Scenario: Bot commands available in Claude Code

- **WHEN** adopt completes
- **THEN** `.claude/commands/lsi/pr-bot.md`, `pr-bot-docs.md`, and `apply-bot.md` exist alongside every other LSI command

#### Scenario: OpenSpec Claude commands untouched

- **WHEN** the adopter has `.claude/commands/opsx/`
- **THEN** adopt neither modifies nor removes it

### Requirement: Claude command parity

`verify-adopters.py` and the parity gate SHALL check that `.claude/commands/lsi/` contains every expected LSI command and SHALL flag, without deleting, surplus files in that directory.

#### Scenario: Missing Claude command

- **WHEN** `.claude/commands/lsi/review.md` is absent
- **THEN** verify reports `missing .claude/commands/lsi/review.md`

### Requirement: Cross-references resolve in Claude commands

Links in emitted Claude commands SHALL resolve from `.claude/commands/lsi/` (one directory deeper than `.cursor/commands/`), and link verification SHALL cover the directory.

#### Scenario: Link check

- **WHEN** `adoption-verify-links.py` runs on an adopted repo
- **THEN** no broken links are reported under `.claude/commands/lsi/`
