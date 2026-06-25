## Why

Agent-stack commands in `overlays/lsi/agent-stack/commands/` embed **ai-agent** and **video-encoder** domain (FastAPI, FFmpeg, `uv run pytest`, data-lake scopes). After adopt, every org repo receives the wrong persona and test gates — `web` already has **video-encoder** contamination in `.lsi/workflows/openspec-git-integration.md` and `.cursor/commands/lsi-*.md` from a prior bad adopt.

The bundle still ships **OpenCode**, **Junie**, **JetBrains AI**, and workflow `bin/lsi-*` / `bin/opsx-*` artifacts. Policy is **Cursor + Claude only**.

The bundle also ships and installs **OpenSpec** (`opsx-*`) slash commands, which duplicates ownership: OpenSpec itself provides those commands via `openspec init` / config profile. The bundle should manage **LSI** (`lsi-*`) commands only and leave `opsx-*` to OpenSpec.

`/lsi:update` today only flags **missing** commands; surplus files (e.g. duplicate `code_review.mdc` + `code-review.mdc`) pass verify silently. Adopt must not silently delete adopter files.

## What Changes

- **Genericize** all `overlays/lsi/agent-stack/commands/*.md` — workflow mechanics only; defer domain to `.lsi/workflows/openspec-git-integration.md` (per-repo patch).
- **Remove** unsupported agent tooling from bundle tree, generator, `adopt.py`, and tests (OpenCode, Junie, JetBrains, `bin/lsi-*`, `bin/opsx-*`).
- **Delegate** OpenSpec (`opsx-*`) slash commands to OpenSpec (`openspec init` / config profile): drop all `opsx-*` sources from the bundle; `adopt.py` installs `lsi-*` only and never installs or removes `opsx-*`; the parity gate ignores the `opsx-*` namespace.
- **Add** `rule_overlays` to `adopt.py`; per-repo `openspec-git-integration.md` patches for `web`, `ai-agent`, `video-encoder`.
- **Add** adopt command/rule **parity gate** — detect surplus commands/rules and legacy alias pairs; adopter confirms before any deletion; `remove_after_adopt` in patch YAML for pre-agreed legacy paths only.
- **Add** pre-release gates: `test_supported_agents_only.py`, `test_commands_generic.py`, `test_adopt_command_rule_parity.py`.
- **Drop** ai-agent `command_overlays.lsi-review` after domain moves to integration patch.

## Capabilities

### New Capabilities

- `supported-agents-cursor-claude`: Bundle and adopt emit only Cursor + Claude artifacts.
- `generic-agent-commands`: Agent-stack commands stack-neutral; domain in workflow docs / repo patches.
- `per-repo-domain-patches`: `overlay_files` + `rule_overlays` hold repo-specific scopes and personas.
- `opsx-commands-delegated-to-openspec`: Bundle manages `lsi-*` only; `opsx-*` owned by OpenSpec — not installed, regenerated, or removed; parity ignores the `opsx-*` namespace.
- `adopt-command-rule-parity`: `/lsi:update` detects surplus/duplicate commands/rules; adopter confirms before any deletion.

### Modified Capabilities

- `adopt-doc-link-resolution`: Extend gates; command parity across adopters.

## Impact

- **Bundle:** `snippets/adopt.py`, `generate-multi-tool-commands.py`, agent-stack commands, LSI workflow overlays, `patches/*.yaml`, `patches/files/*`, tests, `CHANGELOG.md`, `VERSION`.
- **Adopters:** `/lsi:update` required after release (not in apply PR).
- **Out of scope for apply:** application code in `web/`, `ai-agent/`, `video-encoder/`.
