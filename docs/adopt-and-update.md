# Adopt and update (LSI layout)

`cursor-dev-workflows/` is the single source of truth. Application repos consume generated copies via `snippets/adopt.py` — do not hand-edit `.lsi/workflows/`.

## Layout

All adopt-managed specs live under **`.lsi/workflows/`**:

- Router: `which-workflow.md`
- Core specs (pull-requests, branch-workflow, …)
- LSI overlay (openspec-git-integration, versioning-and-releases)
- `templates/`, `examples/`, `sdlc/`

`PROJECT.md` records `CANONICAL_DOCS_PATH=.lsi/workflows/` and `ADOPTION_LAYOUT=lsi`.

## First adopt

```bash
cd cursor-dev-workflows
python3 snippets/adopt.py --target ../my-repo --config patches/my-repo.yaml --audit-only
# Review report; add patches/files/my-repo/audit-resolutions.yaml if needed
python3 snippets/adopt.py --target ../my-repo --config patches/my-repo.yaml --accept-policy-defaults
```

## Bundle update

1. Bump `VERSION` and `CHANGELOG.md` in cursor-dev-workflows
2. Re-run adopt against each adopter repo — agent: **`/lsi:update`** or `python3 snippets/update-workflows.py` (with `WORKFLOWS_BUNDLE_PATH` or `--bundle /path/to/cursor-dev-workflows`)
3. Commit adopted files in each app repo

## Always-on rules (installed by adopt)

| Rule | Role |
|------|------|
| `branch-workflow.mdc` | Protected branches + refusal UX |
| `commit-pr-conventions.mdc` | Pointer to `CONVENTION.md` |
| `openspec-git-integration.mdc` | OpenSpec + `/lsi:*` lifecycle |

## Agent entry points

- `AGENTS.md` — canonical
- `CLAUDE.md` → symlink to `AGENTS.md`
- `.cursorrules` — minimal `<!-- lsi:workflows -->` pointer block

## Audit

`snippets/audit-agent-docs.py` runs before and after adopt. Blocking on error-severity contradictions unless resolutions are accepted.

## Verify after adopt

```bash
python3 snippets/verify-adopters.py --repo-root ../my-repo
```

Checks: `.lsi/workflows/`, 3 always-on rules, `/lsi:*` slash commands, `CLAUDE.md` symlink, `PROJECT.md`, `scripts/check_version.py`, link verify, audit.

## CI: version gate

Adopt installs `scripts/check_version.py` but **does not edit** `bitbucket-pipelines.yml`. Copy from:

- [docs/ci/check_version-web.yml](ci/check_version-web.yml) — `version.txt`
- [docs/ci/check_version-ai-agent.yml](ci/check_version-ai-agent.yml) — `VERSION_FILE=VERSION`

## Ongoing sync (bundle maintainer)

Bundle maintainer adopt loop and local Cursor install are documented in gitignored **`MAINTAINER.md`** (copy from [MAINTAINER.md.example](../MAINTAINER.md.example)).

## New repo

Full checklist: **[adopt-new-repo.md](adopt-new-repo.md)**.

Summary:

1. Copy `patches/_template.yaml` → `patches/<repo>.yaml` and `patches/files/_template/` → `patches/files/<repo>/`
2. Register in [patches/README.md](../patches/README.md)
3. `--audit-only` → `audit-resolutions.yaml` if needed → adopt → `verify-adopters.py`
4. Add to local `MAINTAINER.md` adopt loop
