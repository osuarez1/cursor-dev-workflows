## Context

The cursor-dev-workflows bundle is docs-only and portable. Application repos adopt workflows via `adopt.py`, which installs `.lsi/workflows/`, tracked `openspec/`, and slash commands. Bundle maintainers author in `docs/workflows/` and `overlays/lsi/` and must **not** self-adopt.

Maintainers need OpenSpec planning, `/opsx:*` and `/lsi:*` parity, and local playbooks (`MAINTAINER.md`, adopt-loop paths). This change formalizes tracked templates plus bootstrap/verify scripts.

**Authoring split:** core specs in `docs/workflows/`; LSI extensions in `overlays/lsi/`; **tracked** OpenSpec in `openspec/` (same CLI as adopters).

## Goals / Non-Goals

**Goals:**

- One-command bootstrap of gitignored maintainer kit from tracked templates under `snippets/maintainer-local/`
- Verify script for local health checks (non-CI)
- Path-rewritten slash commands sourced from `overlays/lsi/agent-stack/`
- Clear adopter vs maintainer boundaries in tracked docs
- Slim tracked `*.example` files; full playbooks only in gitignored copies

**Non-Goals:**

- Running `adopt.py --target .` on the bundle repo
- Changing adopter `adopt.py` behavior or `.lsi/workflows/` layout
- CI enforcement of maintainer kit (local-only)
- Tracking `.cursor/commands/` in git

## Decisions

### 1. Templates live under `snippets/maintainer-local/`, install is gitignored

**Choice:** Track templates and install scripts; install copies to gitignored paths.

**Rationale:** Keeps the portable bundle free of org names, machine paths, and private planning. Matches existing pattern for `MAINTAINER.md.example` → `MAINTAINER.md`.

**Alternative:** Commit `.cursor/commands/` in bundle — rejected because commands contain bundle-specific rewrites and encourage self-adopt confusion.

### 2. Command install via Python rewriter, not raw copy

**Choice:** `snippets/install-maintainer-local-commands.py` copies from overlay `agent-stack`, applies token substitution and link rewrites for bundle layout.

**Rationale:** Overlay commands target adopted app paths (`../../docs/workflows/`). Bundle root uses `docs/workflows/` directly.

**Alternative:** Duplicate command files in snippets — rejected; duplicates drift from overlay source.

### 3. Tracked OpenSpec tree at `openspec/`

**Choice:** Commit `openspec/config.yaml` and changes under `openspec/changes/`. Bootstrap ensures `_template/` scaffold; `/opsx:propose` uses default CLI paths (no `openspec-local/` rewrite).

**Rationale:** Simplifies maintainer workflow — same layout as adopters; no path mismatch between slash-command prose and `openspec new change`.

**Supersedes:** Earlier gitignored `openspec-local/` kit approach (removed from `.gitignore` and install rewrites).

### 4. Slim tracked examples; README/AGENTS point to maintainer-local README

**Choice:** `MAINTAINER.md.example` and `AGENTS-LOCAL.md.example` become short pointers; full content in `snippets/maintainer-local/`.

**Rationale:** Reduces duplication; adopters who copy examples get a pointer, maintainers get full playbooks via bootstrap.

### 5. `docs/adopter-boundaries.md` as single boundaries reference

**Choice:** New tracked doc with four zones: adopt manages, adopt never touches, human-maintained per repo, bundle-maintainer-only.

**Rationale:** Reduces confusion between adopter sync and maintainer local kit.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Bootstrap not run → slash commands missing | `verify-maintainer-local.sh`; `AGENTS.md` documents one-time setup |
| Overlay command drift breaks rewriter | `--refresh-commands` flag; verify checks sample commands |
| Maintainer commits gitignored files | `.gitignore` entries; boundaries doc warns |
| Accidental commit of machine paths in MAINTAINER.md | `.gitignore`; boundaries doc |
| Install script fails without overlay | Bootstrap warns; verify fails with clear MISSING lines |

## Migration Plan

1. Merge tracked templates, scripts, docs on `chore/bundle-maintainer-local-kit` (or `feat/...` with ticket).
2. Existing maintainers run `./snippets/bootstrap-maintainer-local.sh` once (or `--refresh-commands` if kit partially present).
3. No adopter action — optional read of `docs/adopter-boundaries.md`.
4. Rollback: revert tracked files; delete local gitignored installs manually if desired.

## Open Questions

- Unit tests for `install-maintainer-local-commands.py` link rewrites — defer unless verify script insufficient.
