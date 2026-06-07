## Why

Bundle maintainers need the same OpenSpec, slash-command, and adopt-loop workflows that application repos get from `adopt.py`, but the bundle repo must **not** self-adopt (no `.lsi/workflows/`). A **maintainer local kit** provides gitignored playbooks and slash commands while using **tracked `openspec/`** — same CLI layout as adopters, without polluting adopter trees.

## What Changes

- Add `snippets/bootstrap-maintainer-local.sh` and `snippets/verify-maintainer-local.sh` for one-time install and health check
- Add `snippets/install-maintainer-local-commands.py` to copy and path-rewrite overlay slash commands into gitignored `.cursor/commands/`
- Add `snippets/maintainer-local/` templates: `MAINTAINER.md`, `AGENTS-LOCAL.md`, `local-*.mdc`, `openspec/` scaffold
- Add tracked `openspec/config.yaml` and [docs/ai/openspec.md](docs/ai/openspec.md)
- Extend `.gitignore` for gitignored maintainer artifacts (`local-*.mdc`, `.cursor/commands/`)
- Slim tracked `MAINTAINER.md.example` and `AGENTS-LOCAL.md.example` to pointers; full content lives in maintainer-local templates
- Document boundaries in `docs/adopter-boundaries.md` (adopt vs maintainer-only vs human-maintained)
- Update `AGENTS.md` and `README.md` with bootstrap/verify quick start and layout
- Add CHANGELOG `[Unreleased]` entry (MINOR — new optional maintainer tooling, no adopter action)

## Capabilities

### New Capabilities

- `maintainer-local-bootstrap`: One-time install of gitignored playbooks, rules, commands, and `openspec/` scaffold from tracked templates
- `maintainer-local-verify`: Non-CI script that asserts the local kit is present and reports missing pieces
- `adopter-boundaries-doc`: Canonical list of what `adopt.py` manages, never touches, and what is bundle-maintainer-only

### Modified Capabilities

- _(none — no existing OpenSpec capability specs in this repo)_

## Impact

- **Tracked:** `snippets/`, `.gitignore`, `AGENTS.md`, `README.md`, `docs/adopter-boundaries.md`, slimmed `*.example` files, `CHANGELOG.md`
- **Tracked:** `openspec/config.yaml`, `openspec/changes/`, `docs/ai/openspec.md`
- **Gitignored (installed locally):** `MAINTAINER.md`, `AGENTS-LOCAL.md`, `.cursor/rules/local-*.mdc`, `.cursor/commands/`
- **Adopters:** No change to `adopt.py` behavior or adopted paths; optional read of `docs/adopter-boundaries.md` for clarity
- **Semver:** MINOR (new maintainer-only tooling)
