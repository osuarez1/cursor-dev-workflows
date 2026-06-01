# Changelog

All notable changes to **cursor-dev-workflows** are documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning policy: [docs/versioning.md](docs/versioning.md).

## [Unreleased]

## [1.0.1] - 2026-06-01

### Fixed

- [which-workflow.md](which-workflow.md) PR row lists all required PR body sections, including Potential risks

## [1.0.0] - 2026-06-01

First stable layout after normative specs moved under `docs/workflows/`.

### Added

- [AGENTS.md](AGENTS.md) and [CLAUDE.md](CLAUDE.md) as agent entry points; [PROJECT.md](PROJECT.md) with resolved placeholders including `BUNDLE_VERSION`
- [docs/workflows/](docs/workflows/) as `CANONICAL_DOCS_PATH` for all normative workflow specs
- New workflow spec [pull-requests.md](docs/workflows/pull-requests.md)
- Always-on [.cursor/rules/commit-pr-conventions.mdc](.cursor/rules/commit-pr-conventions.mdc) for Conventional Commits and PR body sections
- Adoption snippets: `commit-pr-conventions.mdc`, `pull-requests.mdc` under [snippets/cursor-rules/](snippets/cursor-rules/)
- Examples: [commit-messages-good-vs-weak.md](examples/commit-messages-good-vs-weak.md), [pr-description-good-vs-weak.md](examples/pr-description-good-vs-weak.md)
- Bundle versioning: [VERSION](VERSION), this changelog, [docs/versioning.md](docs/versioning.md)
- Maintainer and agent playbook templates: [MAINTAINER.md.example](MAINTAINER.md.example), [AGENTS-LOCAL.md.example](AGENTS-LOCAL.md.example) (local copies gitignored)
- [which-workflow.md](which-workflow.md) router; README **Versioning** section; [adoption-checklist.md](adoption-checklist.md) `BUNDLE_VERSION` guidance

### Changed

- Workflow markdown moved from repository root into `docs/workflows/` (breaking for adopters still pointing at old paths)
- Examples and templates aligned with current workflow output shapes
- Task-specific cursor rule snippets updated to point at `docs/workflows/`

### Adopter action (1.0.0)

- Copy or re-sync all files under `docs/workflows/` into your `CANONICAL_DOCS_PATH`
- Update every `.mdc` in `.cursor/rules/` so paths reference your `CANONICAL_DOCS_PATH` (default in snippets: `docs/workflows/`)
- Re-copy [snippets/cursor-rules/](snippets/cursor-rules/) and set `alwaysApply: true` on `commit-pr-conventions.mdc`
- Point `AGENTS.md` / `CLAUDE.md` at [which-workflow.md](which-workflow.md) and `docs/workflows/`
- Record `BUNDLE_VERSION` = `v1.0.0` (or the commit SHA you synced) in your `PROJECT.md`
