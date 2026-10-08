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
| Card + branch | `/lsi:card` | From `main` or `staging`; OpenSpec → card fields |
| Link card to branch | `/lsi:card-link` | Feature branch without Trello id; **OpenSpec required** |
| List To Do cards | `/lsi:trello-list` | Interactive picker; **OpenSpec required** to confirm/branch |
| Branch from card | `/lsi:trello-branch` | From `main`/`staging`; **OpenSpec required**; sync card + `git tb` |
| Implement | `/opsx:apply` | Ticket branch only |
| PR to staging | `/lsi:pr` | Default target `staging` |
| Promote to main | `/lsi:promote` | After staging QA |
| Close (after promote) | `/lsi:close` | On **`main`** only after promotion merges — sync + archive + `CLOSED.md` |
| Sync specs | `/opsx:sync` | Delta → `openspec/specs/` — as part of `/lsi:close` |
| Archive | `/opsx:archive` | As part of `/lsi:close` on **`main`** after promote |

Manual equivalent: create `openspec/changes/<id>/proposal.md`, spec deltas, `design.md`, `tasks.md`.

Full lifecycle: [openspec-git-integration.md](../../.lsi/workflows/openspec-git-integration.md).

## Profile

Use `core` profile minimum: **explore**, propose, apply, **sync**, archive.

## Version alignment

Run `openspec list` for the current inventory. Key active folders:

| Change folder | Product |
|---------------|---------|
| (see `openspec list`) | Active changes stay open through staging QA |

Closed changes: [`openspec/CLOSED.md`](../../openspec/CLOSED.md) (AGENTS.md links the index; no long archive bullet lists).

Planned (folders not created yet): `v2-workflows-dashboard`, `v3-cloud-scale`.

## Slash commands and overlay

- **OpenSpec:** `/opsx:explore`, `/opsx:propose`, `/opsx:apply`, `/opsx:sync`, `/opsx:archive`
- **Git / delivery:** `/lsi:*` commands — see [openspec-git-integration.md](../../.lsi/workflows/openspec-git-integration.md)
- **Archive timing:** keep change folders active through staging QA and promotion; run `/lsi:close` (sync + archive + `CLOSED.md`) on **`main`** after the promotion PR merges
- **`tasks.md` scope:** never add `/opsx:sync`, `/opsx:archive`, or `/lsi:close` as tasks — close is separate from `/opsx:apply`
- **Human sync policy:** [openspec-sync.md](openspec-sync.md)
- **Project context for artifact generation:** [config.yaml](../../openspec/config.yaml)
