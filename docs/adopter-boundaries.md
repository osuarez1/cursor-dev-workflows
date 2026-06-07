# Adopter boundaries

## Adopt manages

- `.lsi/workflows/**`
- `.cursor/commands/lsi-*.md` (and `opsx-*` when `sync_opsx: true`)
- `.cursor/rules/branch-workflow.mdc`, `openspec-git-integration.mdc`, `commit-pr-conventions.mdc`
- `CONVENTION.md` `<!-- lsi:commits -->` block
- `AGENTS.md` / `.cursorrules` workflow marker blocks
- `CLAUDE.md` symlink
- `scripts/release/`, `scripts/check_version.py`

## Adopt never touches

- `bitbucket-pipelines.yml` (document CI hook only)
- App domain docs in `docs/workflows/` listed under `preserve`
- Domain `.mdc` rules (ffmpeg, rails, etc.)
- Application source code

## Human-maintained per repo

- `patches/<repo>.yaml`
- `patches/files/<repo>/` overlays
- `MAINTAINER.md` (gitignored) in cursor-dev-workflows bundle repo

## Bundle maintainer only

**cursor-dev-workflows** uses tracked **`openspec/`** (same CLI layout as adopters). Gitignored via bootstrap:

- `MAINTAINER.md`, `AGENTS-LOCAL.md` — local adopt loop and release playbooks
- `.cursor/rules/local-*.mdc` — maintainer routing (tracked `commit-pr-conventions.mdc` stays in git)
- `.cursor/commands/` — `/opsx:*` and `/lsi:*` with bundle path rewrites

See [snippets/maintainer-local/README.md](../snippets/maintainer-local/README.md) and [docs/ai/openspec.md](ai/openspec.md).
