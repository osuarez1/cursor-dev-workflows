## ADDED Requirements

### Requirement: Bootstrap installs gitignored maintainer kit from tracked templates

The bundle SHALL provide `./snippets/bootstrap-maintainer-local.sh` that installs gitignored maintainer artifacts from `snippets/maintainer-local/` without running `adopt.py --target .` on the bundle repo.

#### Scenario: First-time bootstrap

- **WHEN** a maintainer runs `./snippets/bootstrap-maintainer-local.sh` from the bundle root on a clean clone
- **THEN** the script installs `MAINTAINER.md`, `AGENTS-LOCAL.md`, `.cursor/rules/local-*.mdc`, `.cursor/commands/` (from overlay via install script), and ensures `openspec/changes/_template/` scaffold when missing
- **AND** existing `MAINTAINER.md` and `AGENTS-LOCAL.md` are preserved unless `--force` is passed

#### Scenario: Refresh commands only

- **WHEN** a maintainer runs `./snippets/bootstrap-maintainer-local.sh --refresh-commands`
- **THEN** only `.cursor/commands/` and local rule copies are refreshed from overlay sources
- **AND** `MAINTAINER.md`, `AGENTS-LOCAL.md`, and tracked `openspec/config.yaml` are not overwritten

### Requirement: Bootstrap must not commit private artifacts

Installed paths SHALL be listed in `.gitignore` so maintainers cannot accidentally commit org-specific or machine-specific content.

#### Scenario: Gitignore coverage

- **WHEN** bootstrap completes successfully
- **THEN** `.gitignore` excludes `MAINTAINER.md`, `AGENTS-LOCAL.md`, `.cursor/rules/local-*.mdc`, and `.cursor/commands/`
- **AND** `openspec/` remains trackable in git

### Requirement: Command install rewrites paths for bundle layout

The install script SHALL copy slash commands from `overlays/lsi/agent-stack/` (or equivalent) and rewrite links so they resolve against bundle paths (`docs/workflows/`, `which-workflow.md`, `templates/`, `examples/`) instead of adopted-app paths.

#### Scenario: Slash commands usable in bundle repo

- **WHEN** bootstrap installs `.cursor/commands/opsx-propose.md` and `.cursor/commands/lsi-card.md`
- **THEN** relative links in those files point to valid paths in the bundle repo root layout
