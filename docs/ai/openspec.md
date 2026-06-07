# OpenSpec (cursor-dev-workflows)

Framework: [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec)

## Layout (tracked)

```text
openspec/
  config.yaml
  changes/<slug>/     # active work
  changes/archive/    # completed
  specs/              # normative after sync
```

Active example: `openspec/changes/bundle-maintainer-local-kit/`.

## Workflow

| Step | Command |
|------|---------|
| Explore | `/opsx:propose` / `/opsx:explore` |
| Propose | `/opsx:propose <slug>` |
| Implement | `/opsx:apply` |
| Sync specs | `/opsx:sync` on `main` |
| Archive | `/lsi:close` or `/opsx:archive` on `main` |

Full lifecycle: [overlays/lsi/docs/workflows/openspec-git-integration.md](../../overlays/lsi/docs/workflows/openspec-git-integration.md).

## Maintainer setup

Slash commands are gitignored — install once:

```bash
./snippets/bootstrap-maintainer-local.sh
```

Bundle uses **source** paths (`docs/workflows/`, `overlays/lsi/`), not `.lsi/workflows/`. Do not run `adopt.py --target .` on this repo.
