## 1. Slash command

- [ ] 1.1 Add `overlays/lsi/agent-stack/commands/lsi-help.md` — overview template, AskQuestion menu ids, per-section templates, SDLC mermaid, bundle-path map, session loop guardrails, GitHub URL builder; **`status`**: no standing `TITLE_PREFIX` line — conditional token note only when card setup is suggested (`design.md` §9)

## 2. Routing and rules

- [ ] 2.1 Add `/lsi:help` decision-table row to `overlays/lsi/docs/workflows/which-workflow.md` and `overlays/lsi/which-workflow-lsi.md`
- [ ] 2.2 Add overlap rule **#7** (`/lsi:help` vs implementation commands) to **LSI overlay** `overlays/lsi/docs/workflows/which-workflow.md` only — one paragraph per `design.md` §8; link to `lsi-help.md`; do not paste full guardrail list
- [ ] 2.3 Optional: extend bundle-root `which-workflow.md` LSI row with “discovery → `/lsi:help` (overlay)” — **no** full overlap rule at root
- [ ] 2.4 Optional: overlay flowchart early branch for workflow help / which command → `/lsi:help`
- [ ] 2.5 List `/lsi:help` in `overlays/lsi/agent-stack/openspec-git-integration.mdc` and `overlays/lsi/docs/workflows/openspec-git-integration.md` quick reference

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
