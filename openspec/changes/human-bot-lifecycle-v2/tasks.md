## 1. Lifecycle docs and bot playbook

- [ ] 1.1 Rewrite `overlays/lsi/docs/workflows/openspec-git-integration.md` lifecycle for human 1–8 / bot 9–19 / human 20–24, close-before-promote, PR modes A/B/C
- [ ] 1.2 Update `overlays/lsi/docs/workflows/which-workflow.md` and `overlays/lsi/which-workflow-lsi.md` for new close timing and lanes
- [ ] 1.3 Add shared bot playbook artifact (e.g. `overlays/lsi/agent-stack/bot-lane.md`) covering steps 9–19 only
- [ ] 1.4 Update adopter-facing adopt docs / `overlays/lsi/docs/ai/openspec.md` archive timing prose
- [ ] 1.5 Update `snippets/audit-agent-docs.py` (and resolutions defaults) so `openspec_archive_timing` expects close-before-promote, not close-on-main-after-promote

## 2. Core command rewrites

- [ ] 2.1 Rewrite `/lsi:close` for ticket-branch gate, CLOSED.md append, commit handoff; remove main-only gate and AGENTS archive append; no Next footer
- [ ] 2.2 Rewrite `/lsi:pr` for modes A/B/C with SOURCE_ROOT / PR_WARN_* / PR_MAX_* gates; PR draft/push only — do not run readiness, review, or verify; no Next footer
- [ ] 2.3 Update `/lsi:promote` and `/lsi:merge-desc` for close-before-promote; strip Next/steering footers
- [ ] 2.4 Update `/lsi:help` sections (lifecycle, sdlc, policies, next) for human/bot lanes and close-before-promote (`next`/`status` topics may still suggest commands)
- [ ] 2.5 Update `/lsi:update` output: review ask + pasteable commit suggestions only (no Next steering to adopt-verify)

## 3. Address-findings and Prowler

- [ ] 3.1 Add `lsi-address-senior.md`, `lsi-address-review.md`, `lsi-address-verify.md`, `lsi-address-readiness.md` from AI prompt library (fix + optional `/lsi:commit` only; no Next footer)
- [ ] 3.2 Add `lsi-address-prowler.md` (Bitbucket comment fetch + triage); document optional Prowler step in lifecycle/playbook — do not auto-chain from `/lsi:review`
- [ ] 3.3 Register address-* (+ prowler) in `expected_agent_stack.py` / verify-adopters / Claude install path

## 3b. Single-purpose slash commands

- [ ] 3b.1 Strip `Next:` / follow-up steering from all `overlays/lsi/agent-stack/commands/lsi-*.md` and mirrored Claude/OpenCode command sources (except `/lsi:help` next/status topics)
- [ ] 3b.2 Remove readiness/review/verify orchestration steps from `/lsi:pr` and `/lsi:promote` command sources
- [ ] 3b.3 Align `/opsx:verify` (and other opsx command copies the bundle maintains) with single-purpose stop-after-verdict pattern
- [ ] 3b.4 Update bot playbook and `openspec-git-integration.md` to document sequencing without embedding Next into individual commands

## 4. Closed-change index

- [ ] 4.1 Add `openspec/CLOSED.md` template/example and AGENTS.md / AGENTS.workflow template pointer (no archive bullet list)
- [ ] 4.2 Document one-time migration: export existing AGENTS archived lists → CLOSED.md for web/infra

## 5. Release-train upstream

- [ ] 5.1 Port `lsi-release-train`, `lsi-release-summary`, `lsi-change-summary` into `overlays/lsi/agent-stack/commands/` with bundle paths
- [ ] 5.2 Register them in expected-agent-stack and genericize web-only script assumptions via PROJECT/versioning overlay

## 5b. Web command hardening (commit / changelog / readiness / review)

- [ ] 5b.1 Port web `/lsi:commit` improvements: required body, plan with files+body, no subject-only, no hand-written `Trello-Card:`; scopes via integration overlay not video-encoder table
- [ ] 5b.2 Port web `/lsi:changelog` rewrite rules: strip `type(scope):`, user-visible bullets, collapse dupes, fold OpenSpec archive noise; keep generator script invocation
- [ ] 5b.3 Port web `/lsi:readiness` improvements: `TEST_COMMAND` from PROJECT.md, docs-only N/A, never emit PR title/body; strip Rails/pytest hardcoding from shared command
- [ ] 5b.4 Port web `/lsi:review` “never draft PR” guardrail; keep focus areas pointed at integration doc / patch (no embedded worker domain table in shared command)
- [ ] 5b.5 Align all four with D11 (no Next footer; no chaining)

## 6. OpenCode support

- [ ] 6.1 Add OpenCode emit path in `adopt.py` / agent-stack (playbook + command stubs); accept `agents_opencode`
- [ ] 6.2 Update `test_supported_agents_only.py` (or successor) to allow `.opencode/`, still forbid Junie/JetBrains/`bin`
- [ ] 6.3 Note amendment in `genericize-adopt-cursor-claude` design/tasks or complete that change’s remaining work consistently

## 7. Adopt verify, install-adopt, and cleanup

- [ ] 7.1 Add `/lsi:adopt-verify` command + deepen structural checks (unresolved tokens, PROJECT vs repo heuristics)
- [ ] 7.2 Add `install-adopt.sh` (git-trello-shaped): `--bundle`, `--repo-name`, `--accept-policy-defaults`, verify, non-zero on failure
- [ ] 7.3 Add `cleanup-adopt.sh` + `/lsi:adopt-clean`: dry-run default, `--yes`/confirm to delete adopt-managed agent-stack and regenerable `.lsi/workflows/` while honoring `preserve` / `preserve_agent_stack`; never touch `PROJECT.md` or app source
- [ ] 7.4 Document fresh-install sequence (cleanup → install → adopt-verify) in `docs/adopt-new-repo.md` and `docs/adopt-and-update.md` (and adopter dual-copy) — as docs only, not chained from one command
- [ ] 7.5 Register `/lsi:adopt-clean` in expected-agent-stack / parity

## 8. Infra host-log

- [ ] 8.1 Add or register `patches/infra.yaml` + copy `lsi-host-log` skill into `patches/files/infra/`
- [ ] 8.2 Wire preserve/parity so infra keeps the skill and other repos do not install it

## 9. Parity, examples, smoke

- [ ] 9.1 Refresh examples/templates that still say close-on-main-after-promote
- [ ] 9.2 Run bundle unit tests touching adopt/commands (`test_commands_generic.py`, adopt/supported-agents tests)
- [ ] 9.3 Bootstrap maintainer local commands and smoke `/lsi:help lifecycle` + `/lsi:help sdlc` section text against new policy
