## 1. Lifecycle docs and bot playbook

- [ ] 1.1 Rewrite `overlays/lsi/docs/workflows/openspec-git-integration.md` lifecycle for human 1–8 / bot 9–19 / human 20–24, close-before-promote, PR modes A/B/C
- [ ] 1.2 Update `overlays/lsi/docs/workflows/which-workflow.md` and `overlays/lsi/which-workflow-lsi.md` for new close timing and lanes
- [ ] 1.3 Add shared bot playbook artifact (e.g. `overlays/lsi/agent-stack/bot-lane.md`) covering steps 9–19 only
- [ ] 1.4 Update adopter-facing adopt docs / `overlays/lsi/docs/ai/openspec.md` archive timing prose
- [ ] 1.5 Update `snippets/audit-agent-docs.py` (and resolutions defaults) so `openspec_archive_timing` expects close-before-promote, not close-on-main-after-promote

## 2. Core command rewrites

- [ ] 2.1 Rewrite `/lsi:close` for ticket-branch gate, CLOSED.md append, commit handoff; remove main-only gate and AGENTS archive append
- [ ] 2.2 Rewrite `/lsi:pr` for modes A/B/C with SOURCE_ROOT / PR_WARN_* / PR_MAX_* gates
- [ ] 2.3 Update `/lsi:promote` and `/lsi:merge-desc` footers: no close-on-main; require prior close
- [ ] 2.4 Update `/lsi:help` sections (lifecycle, sdlc, policies, next) for human/bot lanes and close-before-promote
- [ ] 2.5 Update `/lsi:update` output: review ask, `/lsi:adopt-verify` next, pasteable commit suggestions

## 3. Address-findings and Prowler

- [ ] 3.1 Add `lsi-address-senior.md`, `lsi-address-review.md`, `lsi-address-verify.md`, `lsi-address-readiness.md` from AI prompt library
- [ ] 3.2 Add `lsi-address-prowler.md` (Bitbucket comment fetch + triage) and wire optional pre-`/lsi:review` gate in `lsi-review.md`
- [ ] 3.3 Register address-* (+ prowler) in `expected_agent_stack.py` / verify-adopters / Claude install path

## 4. Closed-change index

- [ ] 4.1 Add `openspec/CLOSED.md` template/example and AGENTS.md / AGENTS.workflow template pointer (no archive bullet list)
- [ ] 4.2 Document one-time migration: export existing AGENTS archived lists → CLOSED.md for web/infra

## 5. Release-train upstream

- [ ] 5.1 Port `lsi-release-train`, `lsi-release-summary`, `lsi-change-summary` into `overlays/lsi/agent-stack/commands/` with bundle paths
- [ ] 5.2 Register them in expected-agent-stack and genericize web-only script assumptions via PROJECT/versioning overlay

## 6. OpenCode support

- [ ] 6.1 Add OpenCode emit path in `adopt.py` / agent-stack (playbook + command stubs); accept `agents_opencode`
- [ ] 6.2 Update `test_supported_agents_only.py` (or successor) to allow `.opencode/`, still forbid Junie/JetBrains/`bin`
- [ ] 6.3 Note amendment in `genericize-adopt-cursor-claude` design/tasks or complete that change’s remaining work consistently

## 7. Adopt verify and install-adopt.sh

- [ ] 7.1 Add `/lsi:adopt-verify` command + deepen structural checks (unresolved tokens, PROJECT vs repo heuristics)
- [ ] 7.2 Add `install-adopt.sh` (git-trello-shaped): `--bundle`, `--repo-name`, `--accept-policy-defaults`, verify, non-zero on failure
- [ ] 7.3 Document installer + adopt-verify in `docs/adopt-new-repo.md` and `docs/adopt-and-update.md` (and adopter dual-copy)

## 8. Infra host-log

- [ ] 8.1 Add or register `patches/infra.yaml` + copy `lsi-host-log` skill into `patches/files/infra/`
- [ ] 8.2 Wire preserve/parity so infra keeps the skill and other repos do not install it

## 9. Parity, examples, smoke

- [ ] 9.1 Refresh examples/templates that still say close-on-main-after-promote
- [ ] 9.2 Run bundle unit tests touching adopt/commands (`test_commands_generic.py`, adopt/supported-agents tests)
- [ ] 9.3 Bootstrap maintainer local commands and smoke `/lsi:help lifecycle` + `/lsi:help sdlc` section text against new policy
