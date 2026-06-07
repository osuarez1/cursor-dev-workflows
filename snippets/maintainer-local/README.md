# Bundle maintainer local kit

Gitignored workflow parity for **cursor-dev-workflows** maintainers — without running `adopt.py` on the bundle.

**OpenSpec** uses tracked **`openspec/`** (same as app repos). Only playbooks, local rules, and slash commands are gitignored.

## One-time setup

```bash
./snippets/bootstrap-maintainer-local.sh
```

Edit gitignored `MAINTAINER.md` with your machine paths and adopter locations.

## What gets installed (gitignored)

| Path | Purpose |
|------|---------|
| `MAINTAINER.md` | Adopt loop, release checklist, local paths |
| `AGENTS-LOCAL.md` | Bundle release playbook for agents |
| `.cursor/rules/local-*.mdc` | Maintainer routing |
| `.cursor/commands/*.md` | `/opsx:*` and `/lsi:*` (paths rewritten for bundle) |

## What stays tracked

| Path | Purpose |
|------|---------|
| `openspec/config.yaml` | Bundle OpenSpec context |
| `openspec/changes/<slug>/` | Active and archived changes |
| `openspec/specs/` | Normative specs after sync |
| `.cursor/rules/commit-pr-conventions.mdc` | Always-on commit/PR rules |

## Re-run after bundle bump

```bash
./snippets/bootstrap-maintainer-local.sh --refresh-commands
```

## Verify

```bash
./snippets/verify-maintainer-local.sh
```

## Boundaries

- **Do not** run `adopt.py --target .` on this repo.
- **Do not** commit `MAINTAINER.md`, `AGENTS-LOCAL.md`, or `.cursor/commands/`.
- Use `/opsx:propose` — changes land in **`openspec/changes/`** (tracked).

| `commands/*.md` | Bundled slash-command sources (rewritten on install) |

Templates: this directory.

**Legacy:** If you previously used gitignored `openspec-local/`, delete that directory — planning now lives in tracked `openspec/`.
