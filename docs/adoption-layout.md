# Adoption layout (LSI)

**There is only one adoption layout for LSI repos:** all adopt-managed content lives under **`.lsi/workflows/`**.

Legacy Profile A (root router + `docs/workflows/`) and Profile B (flatten under `docs/workflows/`) are **retired**.

## Target layout

```
app-repo/
├── .lsi/workflows/          # ADOPT-MANAGED — wipe + regenerate on sync
│   ├── which-workflow.md
│   ├── pull-requests.md
│   ├── branch-workflow.md
│   ├── openspec-git-integration.md
│   ├── templates/
│   └── examples/
├── .cursor/
│   ├── rules/               # always-on LSI rules + on-demand rules
│   └── commands/            # lsi-*, opsx-*
├── docs/workflows/          # optional HUMAN app docs (preserve list in patch YAML)
├── PROJECT.md               # CANONICAL_DOCS_PATH=.lsi/workflows/
└── AGENTS.md                # CLAUDE.md -> AGENTS.md
```

## Adopt command

```bash
python3 snippets/adopt.py --target ../my-repo --config patches/my-repo.yaml
```

See [adopt-and-update.md](adopt-and-update.md) for full guide.

## Link verification

```bash
python3 snippets/adoption-verify-links.py --repo-root ../my-repo --canonical .lsi/workflows
```

## Human docs

App-specific runbooks stay in `docs/workflows/` when listed under `preserve` in `patches/<repo>.yaml`. Do not copy bundle specs there by hand.
