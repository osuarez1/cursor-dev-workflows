# lsi-help-slash-command

## Purpose

Define the interactive `/lsi:help` slash command for LSI workflow discovery — overview-first help session, section menu until Exit, SDLC diagram section, GitHub bundle spec links, and adopter parity expectations.

## ADDED Requirements

### Requirement: Interactive help session overview and menu

The LSI agent stack SHALL provide `/lsi:help` as a read-only consultation command that starts with a short overview and an AskQuestion section menu.

#### Scenario: First turn shows overview only

- **WHEN** a user invokes `/lsi:help` with no topic argument
- **THEN** the agent emits a short LSI workflow overview (dual ticketing, staging-first, typical path, bundle version reference)
- **AND** the agent does not emit the full lifecycle list, command reference table, or SDLC diagram in the same turn
- **AND** the agent presents an AskQuestion menu with section options and Exit

#### Scenario: Numbered menu when AskQuestion unavailable

- **WHEN** AskQuestion is unavailable and the user invokes `/lsi:help`
- **THEN** the agent presents the same section menu as a numbered list with menu ids (`sdlc`, `lifecycle`, `status`, `commands`, `policies`, `overlap`, `links`, `next`, `exit`)
- **AND** the agent prompts the user to reply with a menu id
- **AND** the agent does not refuse help or emit all sections in one response

#### Scenario: Direct topic enters session with menu

- **WHEN** a user invokes `/lsi:help` with a recognized topic argument (`lifecycle`, `sdlc`, `status`, `commands`, `policies`, `overlap`, `links`, `next`)
- **THEN** the agent emits a short overview and the requested section only
- **AND** the agent presents the AskQuestion menu again (session continues)

### Requirement: Help session loop until Exit

The help session SHALL continue across turns until the user selects Exit.

#### Scenario: Section pick re-displays menu

- **WHEN** the user selects any section option other than Exit from the AskQuestion menu
- **THEN** the agent shows that section's content only
- **AND** the agent presents the AskQuestion menu again in the same or next turn
- **AND** the agent does not end the session with only a suggested slash command and no menu

#### Scenario: Exit ends session

- **WHEN** the user selects Exit from the AskQuestion menu
- **THEN** the agent acknowledges exit briefly (e.g. `Exited /lsi:help.`)
- **AND** the agent does not present the AskQuestion menu again
- **AND** the agent does not perform implementation work (commits, Trello API, adopt)

#### Scenario: Read-only consultation

- **WHEN** `/lsi:help` is active (session not exited)
- **THEN** the agent does not run `git ts`, `git tb`, `git commit`, Trello API calls, `adopt.py`, or other slash commands unless the user explicitly invokes them outside help

### Requirement: SDLC diagram section

The help command SHALL provide a dedicated SDLC diagram section separate from the numbered lifecycle text.

#### Scenario: SDLC menu option shows diagram

- **WHEN** the user selects the `sdlc` section from the AskQuestion menu
- **THEN** the agent emits a mermaid flowchart of the staging-first feature delivery path (explore through close on `main`, optional release)
- **AND** the agent does not include the numbered 13-step lifecycle list in the same section response

### Requirement: GitHub bundle spec links in help output

Help section output that references bundle workflow specs SHALL link to the public cursor-dev-workflows GitHub repository.

#### Scenario: Spec links use GitHub blob URLs

- **WHEN** help output includes a link to a bundle workflow spec
- **THEN** the link URL matches `https://github.com/osuarez1/cursor-dev-workflows/blob/{ref}/{bundle-path}`
- **AND** `{ref}` is `v{BUNDLE_VERSION}` from the repo `PROJECT.md` when present, otherwise `main`
- **AND** `{bundle-path}` is the bundle source path (e.g. `docs/workflows/senior-analysis.md` or `overlays/lsi/docs/workflows/openspec-git-integration.md`)
- **AND** the agent does not use relative `.lsi/workflows/` paths or adopter Bitbucket URLs in help output

### Requirement: Adopter parity lists include lsi-help

`snippets/verify-adopters.py` and `snippets/audit-agent-docs.py` SHALL include `lsi-help` in the expected `/lsi:*` command set after implementation.

#### Scenario: Parity check expects lsi-help

- **WHEN** `verify-adopters.py` runs against an adopter with a synced agent stack after `/lsi:help` is implemented
- **THEN** `lsi-help` is listed in `LSI_COMMANDS` and `.cursor/commands/lsi-help.md` is required for parity pass
