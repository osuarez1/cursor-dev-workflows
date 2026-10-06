## ADDED Requirements

### Requirement: Closed change index file

Closed OpenSpec changes SHALL be recorded in `openspec/CLOSED.md` (date, slug, one-line summary, PR URLs, optional release tag), not as a growing bullet list inside `AGENTS.md`.

#### Scenario: Close appends CLOSED.md

- **WHEN** `/lsi:close` completes archive for a slug
- **THEN** the agent appends an entry to `openspec/CLOSED.md`
- **AND** does not append a per-change archive bullet to `AGENTS.md`

### Requirement: AGENTS.md pointer only

`AGENTS.md` SHALL reference the closed-change index with a stable link or path, without enumerating archived changes.

#### Scenario: AGENTS points to index

- **WHEN** an adopter’s AGENTS.md workflows section is rendered after adopt/close policy update
- **THEN** it contains a pointer to `openspec/CLOSED.md` (or equivalent)
- **AND** it does not require maintainers to keep a full archived-changes list in AGENTS.md

### Requirement: Close commit handoff

`/lsi:close` SHALL emit pasteable commit commands for sync/archive/CLOSED.md changes and SHALL NOT run `git commit` unless the user explicitly asks.

#### Scenario: Handoff without auto-commit

- **WHEN** `/lsi:close` finishes file updates
- **THEN** the output includes a **Commit (copy below)** bash block with real slug substituted
- **AND** the agent does not commit unless the user explicitly requests a commit
