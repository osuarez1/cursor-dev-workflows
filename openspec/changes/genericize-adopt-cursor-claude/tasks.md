## 1. REQUIRED — Cursor + Claude only (blocking)

- [x] 1.1 Remove `.opencode/`, `.aiassistant/`, `.junie/`, `bin/lsi-*`, `bin/opsx-*` from bundle git
- [x] 1.2 Claude-only generator; delete multi-tool writers + tests
- [x] 1.3 `adopt.py`: `install_claude_commands` only; error on `agents_opencode|junie|jetbrains|bin`
- [x] 1.4 Add `snippets/test_supported_agents_only.py`; wire `verify-all-adopters.sh`
- [x] 1.5 Update `patches/_template.yaml`, README — no removed tool docs

## 2. Genericize agent-stack + LSI overlays

- [x] 2.1 Rewrite `lsi-review`, `lsi-commit`, `lsi-senior`, `lsi-readiness`, `lsi-pr`, `lsi-promote` (defer pattern)
- [x] 2.2 Generic LSI `openspec-git-integration.md` + `which-workflow.md` baselines
- [x] 2.3 Add `snippets/test_commands_generic.py` + denylist

## 3. OPSX commands

- [x] 3.1 Add `opsx-new`, `opsx-ff`, `opsx-continue`, `opsx-onboard`, `opsx-verify`, `opsx-bulk-archive` (generic)
- [x] 3.2 Centralize expected command list in `snippets/expected_agent_stack.py`; update `verify-adopters` + `audit-agent-docs` to import it
- [x] 3.3 Regenerate `.claude/commands/` only

## 3b. Adopt command/rule parity gate (runs on every `/lsi:update`)

- [x] 3b.1 Add `snippets/expected_agent_stack.py` — `expected_commands()`, `expected_rules()`, `legacy_rule_aliases()`
- [x] 3b.2 Extend `audit-agent-docs.py` → `check_agent_stack_parity`: missing (warn), surplus (error until resolved), legacy alias pairs (error until resolved)
- [x] 3b.3 `adopt.py`: **no auto-prune** of surplus files; overwrite bundle-managed paths only; `remove_after_adopt` runs only paths pre-listed in patch YAML
- [x] 3b.4 `update-workflows.py` + `lsi-update.md`: after parity findings, **ask adopter** which surplus/duplicate paths to remove (list each file); delete **only** confirmed paths; optional `preserve_agent_stack` in patch to allowlist intentional extras
- [x] 3b.5 Add `snippets/test_adopt_command_rule_parity.py` + fixtures; test that adopt does not delete unlisted files
- [x] 3b.6 Wire parity check into `verify-adopters.sh`; `/lsi:update` re-runs verify after adopter-confirmed cleanup

## 4. Per-repo patches + adopt.py

- [x] 4.1 `rule_overlays` in `adopt.py` + `patches/README.md`
- [x] 4.2 `patches/files/web/openspec-git-integration.md` + `cursor-rules/*`
- [x] 4.3 `patches/files/ai-agent/openspec-git-integration.md`; remove `command_overlays` `lsi-review`
- [x] 4.4 `patches/files/video-encoder/openspec-git-integration.md`
- [x] 4.5 Update `web.yaml`, `ai-agent.yaml`, `video-encoder.yaml` (`overlay_files`, `rule_overlays`, `remove_after_adopt`, `sync_opsx`)

## 5. Release

- [x] 5.1 All pre-release gates green:
  ```bash
  python3 snippets/test_supported_agents_only.py
  python3 snippets/test_commands_generic.py
  python3 snippets/test_adopt_command_rule_parity.py
  python3 snippets/test_adopt_links.py
  ```
- [x] 5.2 Bump `VERSION` + `CHANGELOG.md` (Adopters: `/lsi:update` required)
- [x] 5.3 `test_adopt_links`: commands identical across temp adopts; domain only in integration doc

## 6. Post-merge (maintainer — NOT apply deliverables)

- [ ] 6.1 Re-sync `web`, `ai-agent`, `video-encoder` via maintainer adopt loop
- [ ] 6.2 `verify-adopters.py` passes each; announce release only after 6.1
