# Adopter patches

Each LSI application repo has a `patches/<repo>.yaml` consumed by `snippets/adopt.py`.

**New repo?** Follow [docs/adopt-new-repo.md](../docs/adopt-new-repo.md).

## Registered repos

| Patch | Application repo | Version file | Protected branches |
|-------|------------------|--------------|-------------------|
| [video-encoder.yaml](video-encoder.yaml) | video-encoder | `version.txt` | `main`, `staging` |
| [web.yaml](web.yaml) | web | `version.txt` | `main`, `staging`, `master` |
| [ai-agent.yaml](ai-agent.yaml) | ai-agent (monorepo) | `VERSION` | `main`, `staging`, `test` |
| [_template.yaml](_template.yaml) | — copy for new repos | configurable | configurable |

Per-repo markdown overlays: `patches/files/<repo>/` (template: `patches/files/_template/`).

## Run adopt

```bash
cd cursor-dev-workflows

# 1. Audit (first time or after drift)
python3 snippets/adopt.py --target ../video-encoder --config patches/video-encoder.yaml --audit-only

# 2. Adopt / re-sync
python3 snippets/adopt.py --target ../video-encoder --config patches/video-encoder.yaml --accept-policy-defaults

# 3. Verify
python3 snippets/verify-adopters.py --repo-root ../video-encoder
```

Paths for this workspace:

| Repo | `--target` |
|------|------------|
| video-encoder | `../video-encoder` |
| web | `../web` |
| ai-agent | `../agents/ai-agent` |

## Supported agents

This bundle emits artifacts for **Cursor** (`.cursor/commands/`, `.cursor/rules/`) and **Claude** (`.claude/commands/`) only. OpenCode, Junie, JetBrains AI, and workflow shell wrappers (`bin/lsi-*`, `bin/opsx-*`) are not supported. Legacy keys `agents_opencode`, `agents_junie`, `agents_jetbrains`, and `bin` cause adopt to exit with an error.

The bundle installs **LSI** (`lsi-*`) slash commands only. **OpenSpec** (`opsx-*`) commands are owned by OpenSpec (`openspec init` / config profile): adopt never installs or removes them, and the parity gate ignores the `opsx-*` namespace.

## Patch YAML keys

| Key | Purpose |
|-----|---------|
| `project` | Tokens written to `PROJECT.md` |
| `preserve` | Globs/paths adopt never deletes |
| `overlay_files` | Replace specific `.lsi/workflows/*.md` from `patches/files/<repo>/` |
| `rule_overlays` | Install repo-specific `.cursor/rules/*.mdc` from `patches/files/<repo>/cursor-rules/` |
| `remove_after_adopt` | Delete pre-listed legacy paths after adopt (no interactive prompt) |
| `agents_claude` | `AGENTS.md` canonical + `CLAUDE.md` symlink |
| `bootstrap` | Create `version.txt` / `VERSION` if missing |
| `ci_hook.add_check_version` | Document only — see `docs/ci/` |

Full token list: [docs/token-registry.md](../docs/token-registry.md).

## Audit resolutions

When `--audit-only` reports errors, record decisions in `patches/files/<repo>/audit-resolutions.yaml`. Example: [files/_template/audit-resolutions.yaml.example](files/_template/audit-resolutions.yaml.example).
