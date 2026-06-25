## Why

Agent-stack commands in `overlays/lsi/agent-stack/commands/` embed **ai-agent** and **video-encoder** domain (FastAPI, FFmpeg, `uv run pytest`, data-lake scopes). After adopt, every org repo receives the wrong persona and test gates — `web` already has **video-encoder** contamination in `.lsi/workflows/openspec-git-integration.md` and `.cursor/commands/lsi-*.md` from a prior bad adopt.

The bundle still ships **OpenCode**, **Junie**, **JetBrains AI**, and workflow `bin/lsi-*` / `bin/opsx-*` artifacts. Policy is **Cursor + Claude only**.

Six **OPSX** slash commands exist in `web` but not in the bundle agent-stack (`opsx-new`, `opsx-ff`, `opsx-continue`, `opsx-onboard`, `opsx-verify`, `opsx-bulk-archive`).

`/lsi:update` today only flags **missing** commands; surplus files (duplicate `code_review.mdc` + `code-review.mdc`, extra `opsx-*`) pass verify silently. Adopt must not silently delete adopter files.

## What Changes

- **Genericize** all `overlays/lsi/agent-stack/commands/*.md` — workflow mechanics only; defer domain to `.lsi/workflows/openspec-git-integration.md` (per-repo patch).
- **Remove** unsupported agent tooling from bundle tree, generator, `adopt.py`, and tests (OpenCode, Junie, JetBrains, `bin/lsi-*`, `bin/opsx-*`).
- **Add** six generic OPSX commands to agent-stack; `sync_opsx: true` on registered patches installs all `opsx-*` to `.cursor/commands/`.
- **Add** `rule_overlays` to `adopt.py`; per-repo `openspec-git-integration.md` patches for `web`, `ai-agent`, `video-encoder`.
- **Add** adopt command/rule **parity gate** — detect surplus commands/rules and legacy alias pairs; adopter confirms before any deletion; `remove_after_adopt` in patch YAML for pre-agreed legacy paths only.
- **Add** pre-release gates: `test_supported_agents_only.py`, `test_commands_generic.py`, `test_adopt_command_rule_parity.py`.
- **Drop** ai-agent `command_overlays.lsi-review` after domain moves to integration patch.

## Capabilities

### New Capabilities

- `supported-agents-cursor-claude`: Bundle and adopt emit only Cursor + Claude artifacts.
- `generic-agent-commands`: Agent-stack commands stack-neutral; domain in workflow docs / repo patches.
- `per-repo-domain-patches`: `overlay_files` + `rule_overlays` hold repo-specific scopes and personas.
- `opsx-extended-commands`: Six OPSX commands in agent-stack; adopt with `sync_opsx: true` installs all `opsx-*`.
- `adopt-command-rule-parity`: `/lsi:update` detects surplus/duplicate commands/rules; adopter confirms before any deletion.

### Modified Capabilities

- `adopt-doc-link-resolution`: Extend gates; command parity across adopters.

## Impact

- **Bundle:** `snippets/adopt.py`, `generate-multi-tool-commands.py`, agent-stack commands, LSI workflow overlays, `patches/*.yaml`, `patches/files/*`, tests, `CHANGELOG.md`, `VERSION`.
- **Adopters:** `/lsi:update` required after release (not in apply PR).
- **Out of scope for apply:** application code in `web/`, `ai-agent/`, `video-encoder/`.
