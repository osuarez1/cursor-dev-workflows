# maintainer-cursor-gitignore

## Purpose

Define how bundle maintainers install local Cursor artifacts without tracking them in version control, and how re-sync tooling loads org-specific adopter paths from gitignored config.

## Requirements

### Requirement: Bundle repo gitignores local Cursor install

The bundle maintainer repository SHALL gitignore `.cursor/` and SHALL NOT track local Cursor rules or slash commands in version control.

#### Scenario: Cursor directory ignored

- **WHEN** a maintainer runs `git status` after bootstrap or adopt local install
- **THEN** `.cursor/` contents are ignored and not staged

#### Scenario: Canonical rules live in snippets

- **WHEN** maintainers or agents need commit/PR convention rules in this repo
- **THEN** they reference `snippets/cursor-rules/commit-pr-conventions.mdc` (local install steps in gitignored `MAINTAINER.md`)

### Requirement: Bootstrap syncs slash commands from overlay

The bundle maintainer SHALL provide `./snippets/bootstrap-maintainer-local.sh` invoking `snippets/install-maintainer-local.py` to copy `overlays/lsi/agent-stack/commands/` into gitignored `.cursor/commands/` with bundle-layout path rewrites. Install and re-sync instructions SHALL live in gitignored **`MAINTAINER.md`**, not in tracked `AGENTS.md` or `README.md`.

#### Scenario: Re-run after overlay command edits

- **WHEN** a maintainer edits slash commands under `overlays/lsi/agent-stack/commands/`
- **THEN** running bootstrap (per `MAINTAINER.md`) updates `.cursor/commands/` to match overlay without manual copy

### Requirement: Maintainer re-sync via update-workflows helper

The bundle SHALL provide `snippets/update-workflows.py` and overlay slash command `/lsi:update` to re-sync workflows: bootstrap local `.cursor/` when run from the bundle maintainer repo, or `adopt.py` when run from an LSI adopter repo.

#### Scenario: Bundle maintainer full sync

- **WHEN** a maintainer runs `python3 snippets/update-workflows.py` from the bundle repo with `maintainer-adopters.local.yaml` present
- **THEN** bootstrap updates `.cursor/commands/` from overlay and adopt runs for each configured adopter target

#### Scenario: Adopter self-update

- **WHEN** a maintainer runs `/lsi:update` or `update-workflows.py --bundle <path>` from an LSI adopter repo
- **THEN** `adopt.py` re-syncs `.lsi/workflows/` and agent stack from the bundle without modifying the bundle repo

### Requirement: Org-specific adopter paths are gitignored

The bundle maintainer repository SHALL gitignore `maintainer-adopters.local.yaml` at the repo root. Org-specific adopter clone paths SHALL NOT appear in tracked slash command examples or public maintainer docs — only in gitignored `MAINTAINER.md` and the local YAML file.

#### Scenario: Adopter targets loaded from local config

- **WHEN** `update-workflows.py` runs the maintainer adopter sync loop
- **THEN** it reads `adopters:` entries (`target`, `config`) from gitignored `maintainer-adopters.local.yaml` and skips the loop with a clear message when the file is absent

#### Scenario: Tracked slash commands stay generic

- **WHEN** a reviewer reads `overlays/lsi/agent-stack/commands/lsi-update.md` in version control
- **THEN** maintainer adopter sync examples reference gitignored `MAINTAINER.md` / `maintainer-adopters.local.yaml` and do not embed org-specific clone paths like `../web`

### Requirement: Adopter parity includes maintainer re-sync command

`snippets/verify-adopters.py` and `snippets/audit-agent-docs.py` SHALL list `/lsi:update` among expected `/lsi:*` commands when the agent stack is synced to adopters.

#### Scenario: Parity check finds update command

- **WHEN** `verify-adopters.py` runs against an adopter with a synced agent stack
- **THEN** `lsi-update` is included in the expected command set
