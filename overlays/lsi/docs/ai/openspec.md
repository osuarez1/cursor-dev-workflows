# OpenSpec

Framework: [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec)

## Layout

```
openspec/
  config.yaml
  specs/           # current behavior
  changes/         # proposed work
  changes/archive/ # completed changes
```

## Init (once per repo)

```bash
# When Node/openspec CLI available:
openspec init
```

Documentation sprint seeds `openspec/` manually; `openspec init` is optional if aligning CLI tooling.

## Workflow (slash commands)

| Step | Command | Notes |
|------|---------|-------|
| Explore | `/opsx:explore` | Docs-only on `main`/`staging` |
| Propose | `/opsx:propose <slug>` | Creates proposal, design, tasks |
| Card + branch | `/lsi:card` | From `main` only |
| Implement | `/opsx:apply` | Ticket branch only |
| PR to staging | `/lsi:pr` | Default target `staging` |
| Promote to main | `/lsi:promote` | After staging QA |
| Production close | `/lsi:close` | On **`main`** — sync + archive |
| Sync specs | `/opsx:sync` | Delta → `openspec/specs/` — **`main` only** |
| Archive | `/opsx:archive` | After **`main`** merge — prefer `/lsi:close` |

Manual equivalent: create `openspec/changes/<id>/proposal.md`, spec deltas, `design.md`, `tasks.md`.

Full lifecycle: [openspec-git-integration.md](../workflows/openspec-git-integration.md).

## Profile

Use `core` profile minimum: **explore**, propose, apply, **sync**, archive.

## Version alignment

Run `openspec list` for the current inventory. Key active folders:

| Change folder | Product |
|---------------|---------|
| `v1-mvp-hls` | V1 worker (close on **`main`** via `/lsi:close`) |
| `staging-first-archive-policy` | Workflow — staging-first sync/archive policy |
| `doc-audit-remediation` | Documentation hygiene |

Archived changes: [`AGENTS.md`](../../AGENTS.md) § Archived OpenSpec changes (e.g. `openspec-git-slash-commands`).

Planned (folders not created yet): `v2-workflows-dashboard`, `v3-cloud-scale`.

## Slash commands and overlay

- **OpenSpec:** `/opsx:explore`, `/opsx:propose`, `/opsx:apply`, `/opsx:sync`, `/opsx:archive`
- **Git / delivery:** `/lsi:*` commands — see [openspec-git-integration.md](../workflows/openspec-git-integration.md)
- **Archive timing:** keep change folders active through staging QA; sync/archive only on **`main`** via `/lsi:close`
- **`tasks.md` scope:** never add `/opsx:sync`, `/opsx:archive`, or `/lsi:close` as tasks — production close is separate from `/opsx:apply`
- **Human sync policy:** [openspec-sync.md](openspec-sync.md)
- **Project context for artifact generation:** [config.yaml](../../openspec/config.yaml)
