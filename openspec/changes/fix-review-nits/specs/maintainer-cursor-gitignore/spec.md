## ADDED Requirements

### Requirement: Bundle repo gitignores local Cursor install

The bundle maintainer repository SHALL gitignore `.cursor/` and SHALL NOT track local Cursor rules or slash commands in version control.

#### Scenario: Cursor directory ignored

- **WHEN** a maintainer runs `git status` after bootstrap or adopt local install
- **THEN** `.cursor/` contents are ignored and not staged

#### Scenario: Canonical rules live in snippets

- **WHEN** maintainers or agents need commit/PR convention rules in this repo
- **THEN** they reference `snippets/cursor-rules/commit-pr-conventions.mdc` (local install steps in gitignored `MAINTAINER.md`)

### Requirement: Bootstrap syncs slash commands from overlay

The bundle maintainer SHALL provide `./snippets/bootstrap-maintainer-local.sh` to copy `overlays/lsi/agent-stack/commands/` into gitignored `.cursor/commands/` with bundle-layout path rewrites. Install and re-sync instructions SHALL live in gitignored **`MAINTAINER.md`**, not in tracked `AGENTS.md` or `README.md`.

#### Scenario: Re-run after overlay command edits

- **WHEN** a maintainer edits slash commands under `overlays/lsi/agent-stack/commands/`
- **THEN** running bootstrap (per `MAINTAINER.md`) updates `.cursor/commands/` to match overlay without manual copy
