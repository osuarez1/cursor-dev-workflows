# lsi-help-slash-command

## Purpose

Define the `/lsi:help` slash command for LSI workflow discovery — one response per invocation, topic list or section content, SDLC diagram section, GitHub bundle spec links, and adopter parity expectations.

**Verification note:** Topic rendering is **agent-dependent** — agents must read `## Section:` blocks from the command source; there is no programmatic renderer. Apply/review chat dogfood matched overview, `sdlc`, `lifecycle`, `next`, and invalid topic. Residual risk for other agents/models only.
## Requirements
### Requirement: One-shot help overview and topic list

The LSI agent stack SHALL provide `/lsi:help` as a read-only reference command with exactly one response per invocation.

#### Scenario: No topic shows overview and topic list only

- **WHEN** a user invokes `/lsi:help` with no topic argument
- **THEN** the agent emits a short LSI workflow overview (dual ticketing, human vs bot lanes, close-before-promote, PR modes A/B/C, typical path, bundle version reference)
- **AND** the agent presents a numbered list of eight topic ids with labels and `/lsi:help <topic>` invoke hints
- **AND** the agent does not emit section bodies (lifecycle list, command table, SDLC diagram) in the same response

#### Scenario: Topic arg renders section in one response

- **WHEN** a user invokes `/lsi:help` with a recognized topic argument (`lifecycle`, `sdlc`, `status`, `commands`, `policies`, `overlap`, `links`, `next`)
- **THEN** the agent reads the matching `## Section:` block from the command source, substitutes `{ref}` from `PROJECT.md`, and emits the full section in chat
- **AND** the agent does not re-show the topic list or start a multi-turn help session

#### Scenario: Invalid topic

- **WHEN** a user invokes `/lsi:help` with an unrecognized topic argument
- **THEN** the agent emits a one-line error and the numbered topic list
- **AND** the response remains a single turn

### Requirement: Read-only consultation

`/lsi:help` SHALL not perform implementation side effects.

#### Scenario: No implementation from help

- **WHEN** `/lsi:help` runs (with or without topic)
- **THEN** the agent does not run `git ts`, `git tb`, `git commit`, Trello API calls, `adopt.py`, or other slash commands
- **AND** read-only git/openspec inspection is allowed only for `status` and `next` topics

### Requirement: SDLC diagram section

The help command SHALL provide a dedicated SDLC diagram section separate from the numbered lifecycle text.

#### Scenario: SDLC topic shows diagram

- **WHEN** the user invokes `/lsi:help sdlc`
- **THEN** the agent emits a mermaid flowchart of the feature delivery path (human docs PR → bot impl PR → staging QA → promote to main → close on main → optional release)
- **AND** the diagram does not show `/lsi:close` exclusively on `main` after promote as the happy path
- **AND** the agent does not include the numbered lifecycle list in the same response

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

### Requirement: Lifecycle topic matches human-bot lanes

The `/lsi:help lifecycle` section SHALL describe human steps 1–8, bot steps 9–19, and human close/promote steps 20–24 consistent with `openspec-git-integration.md`.

#### Scenario: Lifecycle topic content

- **WHEN** the user invokes `/lsi:help lifecycle`
- **THEN** the emitted section includes mode-A docs PR before mode-B impl PR (unless mode C), bot-lane apply through staging PR, and `/lsi:close` before `/lsi:promote`
- **AND** the section does not instruct production close only on `main` after promote as the default path

