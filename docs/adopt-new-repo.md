# Adopt a new LSI repository

Step-by-step for registering and adopting a **new** application repo into the LSI workflow bundle.

**Prerequisites:** `cursor-dev-workflows` cloned locally; PyYAML (`pip install pyyaml`); target repo on disk.

## Registered adopters (reference)

| Patch | Repo path (typical) | Notes |
|-------|---------------------|-------|
| [patches/video-encoder.yaml](../patches/video-encoder.yaml) | `../video-encoder` | Python worker; `version.txt` |
| [patches/web.yaml](../patches/web.yaml) | `../web` | Rails; `master` protected; app docs in `docs/workflows/` |
| [patches/ai-agent.yaml](../patches/ai-agent.yaml) | `../agents/ai-agent` | Monorepo; `VERSION`; `test` protected |

## 1. Create patch YAML

```bash
cd cursor-dev-workflows
cp patches/_template.yaml patches/<repo>.yaml
cp -r patches/files/_template patches/files/<repo>
```

Edit `patches/<repo>.yaml`:

- `project.*` tokens — see [token-registry.md](token-registry.md)
- `preserve` — human/app docs and domain `.mdc` rules adopt must not delete
- `overlay_files` — paths under `patches/files/<repo>/`
- `remove_after_adopt` — legacy workflow files/rules to delete after first adopt
- `bootstrap` — initial `version.txt` or `VERSION` if missing

Add a row to [patches/README.md](../patches/README.md) registered table.

## 2. Audit before adopt

```bash
python3 snippets/adopt.py \
  --target /path/to/<repo> \
  --config patches/<repo>.yaml \
  --audit-only
```

Fix blocking contradictions or record decisions in `patches/files/<repo>/audit-resolutions.yaml` (see [audit-resolutions.yaml.example](../patches/files/_template/audit-resolutions.yaml.example)).

Common fixes:

- Staging-first PR target vs prose in `CLAUDE.md` / `CONTRIBUTING.md`
- `/opsx:archive` after merge → `/lsi:close` on `main`
- `CLAUDE.md` regular file → merge into `AGENTS.md`, then symlink

## 3. Run adopt

```bash
python3 snippets/adopt.py \
  --target /path/to/<repo> \
  --config patches/<repo>.yaml \
  --accept-policy-defaults   # known repos only; else use resolutions file
```

Dry run first if desired: add `--dry-run` (skips writes).

## 4. Post-adopt manual steps

1. **Reconcile `AGENTS.md`** — ensure `<!-- lsi:workflows -->` and `<!-- lsi:domain -->` blocks; merge unique content from old `CLAUDE.md` if adopt backed up to `.adopt-claude-backup.md`
2. **CI** — add `scripts/check_version.py` to `bitbucket-pipelines.yml` (snippets in [docs/ci/](ci/)); adopt does not edit pipelines
3. **OpenSpec** — `openspec init` at repo root if needed; single `openspec/config.yaml` for monorepos
4. **Stubs** — create `docs/sdlc/bitbucket.md` and `docs/deployment/secrets.md` if link verify needs them (see web/ai-agent)
5. **Retire** hand-vendored `docs/workflows/*` bundle copies (not listed under `preserve`)

## 5. Verify

```bash
python3 snippets/verify-adopters.py --repo-root /path/to/<repo>
```

Expect: parity OK, links OK, audit no errors.

## 6. App-repo PR

Suggested title: `chore: adopt cursor-dev-workflows v1.3.0 (LSI layout)`

PR body should include:

- Agent docs audit summary (contradictions resolved)
- `BUNDLE_VERSION` in `PROJECT.md`
- CI snippet added (if applicable)
- List of `preserve` docs untouched

## 7. Maintainer registry

Add the repo to your local `MAINTAINER.md` adopt loop (see [MAINTAINER.md.example](../MAINTAINER.md.example)):

```bash
python3 snippets/adopt.py --target ../<repo> --config patches/<repo>.yaml --accept-policy-defaults
```

Re-run on every bundle tag bump.

## Monorepo notes

- Set `SOURCE_ROOT` to comma-separated paths (`frontend/, backend/`)
- Use root `openspec/` only; remove per-package `openspec/` dirs in `remove_after_adopt`
- `VERSION` + `VERSION_FILE: VERSION` in patch YAML
- Cursor: prefer opening **repo root** or add root folder to `.code-workspace` so root `.cursor/commands/` load

## What adopt never touches

See [adopter-boundaries.md](adopter-boundaries.md) — `bitbucket-pipelines.yml` (except you add CI manually), preserved domain docs, application source.
