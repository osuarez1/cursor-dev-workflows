# Changelog

All notable changes to **cursor-dev-workflows** are documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning policy: [docs/versioning.md](docs/versioning.md).

## [Unreleased]

## [1.3.0] - 2026-06-06

### Added

- **LSI overlay** — `overlays/lsi/` with OpenSpec + Git integration, release scripts, agent stack (3 always-on rules, 13× `/lsi:*`, 5× `/opsx:*` commands)
- **`snippets/adopt.py`** — single adopt entry point for `.lsi/workflows/` layout; `--accept-resolutions` wired to audit
- **`snippets/audit-agent-docs.py`** — pre/post adopt contradiction scan (v1 token/path checks); `--accept-resolutions` and `--accept-policy-defaults`
- **`snippets/verify-adopters.py`** — parity checklist + link/audit gate for LSI adopters
- **`snippets/verify-all-adopters.sh`** — verify video-encoder, web, ai-agent in one command
- **`patches/`** — per-repo YAML registry (`video-encoder`, `web`, `ai-agent`, `_template`) with `audit_resolutions` paths
- **`patches/files/_template/`** — overlay examples + `audit-resolutions.yaml.example`
- **Docs** — [docs/adopt-and-update.md](docs/adopt-and-update.md), [docs/adopt-new-repo.md](docs/adopt-new-repo.md), [docs/token-registry.md](docs/token-registry.md), [docs/adopter-boundaries.md](docs/adopter-boundaries.md), [overlays/lsi/docs/workflows/branch-reviewability.md](overlays/lsi/docs/workflows/branch-reviewability.md)
- **CI snippets** — `docs/ci/check_version-web.yml`, `docs/ci/check_version-ai-agent.yml`

### Changed

- **Adoption layout** — LSI only (`.lsi/workflows/`); Profile A/B retired; verify test fixtures updated
- **`snippets/adoption-verify-links.py`** — LSI layout only; removed `--profile` flag
- **`check_version.py`** — supports `VERSION_FILE` env var (e.g. `VERSION` for ai-agent)
- **`patches/_template.yaml`** — full patch schema with comments
- **`patches/README.md`** — registered repos table and patch key reference
- **`adoption-checklist.md`** — LSI adopt.py path at top; legacy manual steps deprecated
- **`MAINTAINER.md.example`** — LSI adopt loop and verify commands (replaces Profile A/B)

### Adopter note (1.3.0)

- Add `patches/<repo>.yaml` if missing; run `python3 snippets/adopt.py --target ../<repo> --config patches/<repo>.yaml`
- Review audit report before first adopt; use `--accept-policy-defaults` on video-encoder re-sync after sign-off
- `/lsi:ask` deferred to v1.3.1

## [1.2.0] - 2026-06-01

### Added

- [docs/workflows/pull-requests.md](docs/workflows/pull-requests.md) — **PR merge commit** section (GitHub default subject, extended description blocks, squash vs merge)
- [templates/pr-merge-extended-description.template.md](templates/pr-merge-extended-description.template.md) — copy-paste merge extended description
- [examples/pr-merge-commit-good-vs-weak.md](examples/pr-merge-commit-good-vs-weak.md) — good vs weak merge-commit illustrations

### Changed

- [which-workflow.md](which-workflow.md) — route PR merge info to `pull-requests.md`; merge step in large-feature order
- [AGENTS.md](AGENTS.md) — merge commit guidance in entry point and examples list
- [docs/workflows/common-mistakes.md](docs/workflows/common-mistakes.md) — anti-pattern for weak merge extended descriptions
- [.cursor/rules/commit-pr-conventions.mdc](.cursor/rules/commit-pr-conventions.mdc) and [snippets/cursor-rules/commit-pr-conventions.mdc](snippets/cursor-rules/commit-pr-conventions.mdc) — PR merge commit rules and PR template references
- [snippets/cursor-rules/pull-requests.mdc](snippets/cursor-rules/pull-requests.mdc) — merge info routing
- [docs/workflows/pull-requests.md](docs/workflows/pull-requests.md) — Commits merged oldest-first; omit sync merges; consolidated Assistant output
- [templates/pr-merge-extended-description.template.md](templates/pr-merge-extended-description.template.md) — `git log … --reverse --no-merges` gather command
- [README.md](README.md) — workflow table and intro mention merge commit text
- [adoption-checklist.md](adoption-checklist.md) — PR merge info agent smoke test in §9

### Adopter note (1.2.0)

- Re-sync [docs/workflows/pull-requests.md](docs/workflows/pull-requests.md), [README.md](README.md), and [adoption-checklist.md](adoption-checklist.md)
- Re-copy [snippets/cursor-rules/commit-pr-conventions.mdc](snippets/cursor-rules/commit-pr-conventions.mdc) and [snippets/cursor-rules/pull-requests.mdc](snippets/cursor-rules/pull-requests.mdc) into `.cursor/rules/`
- Copy [templates/pr-merge-extended-description.template.md](templates/pr-merge-extended-description.template.md) and [examples/pr-merge-commit-good-vs-weak.md](examples/pr-merge-commit-good-vs-weak.md) to repo root (Profile A)

## [1.1.0] - 2026-06-01

### Added

- [docs/adoption-layout.md](docs/adoption-layout.md) — layout profiles (A mirror / B flatten), copy map, link conventions, merging existing docs, verification gate
- [docs/adoption-verify-architecture.md](docs/adoption-verify-architecture.md) — verification gate design reference
- [adoption-checklist.md](adoption-checklist.md) — profile choice, expanded copy steps, merging existing docs, required link verification in §9
- [snippets/adoption-verify-links.py](snippets/adoption-verify-links.py) — runnable Profile A/B link and pattern verification
- [snippets/test_adoption_verify_links.py](snippets/test_adoption_verify_links.py) and [snippets/fixtures/adoption-verify/](snippets/fixtures/adoption-verify/) — regression tests for link verification
- [README.md](README.md) — Profile A adoption recipe, `ADOPTION_PROFILE` placeholder, submodule/subtree note
- [AGENTS.md](AGENTS.md) — adoption layout as first step for application repos

### Changed

- [snippets/adoption-verify-links.py](snippets/adoption-verify-links.py) — Profile A root entry points (`which-workflow.md`, `AGENTS.md`, `README.md`); `--extra-dirs`; out-of-repo link rejection
- [MAINTAINER.md.example](MAINTAINER.md.example) — Profile A as default sync mapping; re-sync link verification step; pre-release script and unittest check
- [docs/versioning.md](docs/versioning.md) — adopter sync references adoption layout and link verification
- [docs/adoption-layout.md](docs/adoption-layout.md) — stable Profile B anchor; verification script as primary path; `--extra-dirs` and scan scope

### Adopter note (1.1.0)

- No adopter action required for repos already on Profile A mirror layout
- New adopters: read [docs/adoption-layout.md](docs/adoption-layout.md) and run [snippets/adoption-verify-links.py](snippets/adoption-verify-links.py) before merge

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
