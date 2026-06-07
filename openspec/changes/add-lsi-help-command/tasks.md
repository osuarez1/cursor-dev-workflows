## 1. Slash command

- [ ] 1.1 Add `overlays/lsi/agent-stack/commands/lsi-help.md` — overview template, AskQuestion menu ids, per-section templates, SDLC mermaid, bundle-path map, session loop guardrails, GitHub URL builder

## 2. Routing and rules

- [ ] 2.1 Add `/lsi:help` row to `overlays/lsi/docs/workflows/which-workflow.md` and `overlays/lsi/which-workflow-lsi.md`
- [ ] 2.2 List `/lsi:help` in `overlays/lsi/agent-stack/openspec-git-integration.mdc` and `overlays/lsi/docs/workflows/openspec-git-integration.md` quick reference

## 3. Parity tooling

- [ ] 3.1 Append `lsi-help` to `LSI_COMMANDS` in `snippets/verify-adopters.py`
- [ ] 3.2 Append `lsi-help` to `LSI_COMMANDS` in `snippets/audit-agent-docs.py`

## 4. Maintainer dogfood and release

- [ ] 4.1 Run `snippets/bootstrap-maintainer-local.sh` (or `install-maintainer-local.py`) so `.cursor/commands/lsi-help.md` exists in bundle repo
- [ ] 4.2 Add `[Unreleased]` CHANGELOG entry for `/lsi:help`
- [ ] 4.3 Bump `VERSION` to **1.4.1** and sync `PROJECT.md` `BUNDLE_VERSION`

## 5. Verification

- [ ] 5.1 Manual: `/lsi:help` first turn = overview + AskQuestion only
- [ ] 5.2 Manual: each section pick ends with AskQuestion; Exit ends session
- [ ] 5.3 Manual: `sdlc` section shows mermaid only
- [ ] 5.4 Manual: all spec links are `github.com/osuarez1/cursor-dev-workflows/blob/v.../...`
- [ ] 5.5 Run `python3 snippets/verify-adopters.py` after bootstrap (bundle repo smoke)
