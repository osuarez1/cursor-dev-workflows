## ADDED Requirements

### Requirement: Bundle repo gitignores local Cursor install

The bundle maintainer repository SHALL gitignore `.cursor/` and SHALL NOT track local Cursor rules or slash commands in version control.

#### Scenario: Cursor directory ignored

- **WHEN** a maintainer runs `git status` after bootstrap or adopt local install
- **THEN** `.cursor/` contents are ignored and not staged

#### Scenario: Canonical rules live in snippets

- **WHEN** maintainers or agents need commit/PR convention rules in this repo
- **THEN** they reference `snippets/cursor-rules/commit-pr-conventions.mdc` (installed locally via `bootstrap-maintainer-local.sh`)
