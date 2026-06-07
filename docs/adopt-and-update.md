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
2. Re-run adopt against each adopter repo
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

## New repo

Copy `patches/_template.yaml` → `patches/<repo>.yaml`, add overlay files under `patches/files/<repo>/`, run adopt.
