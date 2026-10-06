## MODIFIED Requirements

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

### Requirement: SDLC diagram section

The help command SHALL provide a dedicated SDLC diagram section separate from the numbered lifecycle text.

#### Scenario: SDLC topic shows diagram

- **WHEN** the user invokes `/lsi:help sdlc`
- **THEN** the agent emits a mermaid flowchart of the feature delivery path (human docs PR → bot impl PR → staging QA → close before promote → promote to main → optional release)
- **AND** the diagram does not show `/lsi:close` exclusively on `main` after promote as the happy path
- **AND** the agent does not include the numbered lifecycle list in the same response

## ADDED Requirements

### Requirement: Lifecycle topic matches human-bot lanes

The `/lsi:help lifecycle` section SHALL describe human steps 1–8, bot steps 9–19, and human close/promote steps 20–24 consistent with `openspec-git-integration.md`.

#### Scenario: Lifecycle topic content

- **WHEN** the user invokes `/lsi:help lifecycle`
- **THEN** the emitted section includes mode-A docs PR before mode-B impl PR (unless mode C), bot-lane apply through staging PR, and `/lsi:close` before `/lsi:promote`
- **AND** the section does not instruct production close only on `main` after promote as the default path
