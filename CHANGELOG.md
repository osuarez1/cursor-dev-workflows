# Changelog

All notable changes to **cursor-dev-workflows** are documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning policy: [docs/versioning.md](docs/versioning.md).

## [Unreleased]

### Added

- Bundle versioning: `VERSION`, this changelog, [docs/versioning.md](docs/versioning.md)
- Maintainer and agent playbooks via tracked templates: `MAINTAINER.md.example`, `AGENTS-LOCAL.md.example` (local copies gitignored)
- `BUNDLE_VERSION` placeholder for adopted repos ([PROJECT.md](PROJECT.md))

## [1.0.0] - 2026-06-01

First stable layout after normative specs moved under `docs/workflows/`.

### Added

- [AGENTS.md](AGENTS.md) and [CLAUDE.md](CLAUDE.md) as agent entry points
- [docs/workflows/](docs/workflows/) as `CANONICAL_DOCS_PATH` for all normative workflow specs
- Always-on [.cursor/rules/commit-pr-conventions.mdc](.cursor/rules/commit-pr-conventions.mdc) for Conventional Commits and PR body sections
- Workflow specs: pull-requests, test-requirements, integrations; expanded examples and templates (commits, PR descriptions)
- Adoption snippets: `commit-pr-conventions.mdc`, `pull-requests.mdc` under [snippets/cursor-rules/](snippets/cursor-rules/)
- [which-workflow.md](which-workflow.md) router and [adoption-checklist.md](adoption-checklist.md)

### Changed

- Workflow markdown moved from repository root into `docs/workflows/` (breaking for adopters still pointing at old paths)
- Examples and templates aligned with current workflow output shapes

### Adopter action (1.0.0)

- Copy or re-sync all files under `docs/workflows/` into your `CANONICAL_DOCS_PATH`
- Update every `.mdc` in `.cursor/rules/` so paths reference your `CANONICAL_DOCS_PATH` (default in snippets: `docs/workflows/`)
- Re-copy [snippets/cursor-rules/](snippets/cursor-rules/) and set `alwaysApply: true` on `commit-pr-conventions.mdc`
- Point `AGENTS.md` / `CLAUDE.md` at [which-workflow.md](which-workflow.md) and `docs/workflows/`
- Record `BUNDLE_VERSION` = `v1.0.0` (or the commit SHA you synced) in your `PROJECT.md`
