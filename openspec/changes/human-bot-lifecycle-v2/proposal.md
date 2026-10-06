## Why

Adopter repos (`web` at bundle 1.4.2, `infra` at 1.5.0) have drifted: web minted release-train / change-summary / richer close handoff outside the overlay; infra added `lsi-host-log`; both still close on `main` after promote and bury archive lists in `AGENTS.md`. The desired operating model splits **human** shaping (explore → docs PR) from a **coding-agent bot lane** (apply → staging code PR), closes OpenSpec **after staging QA and before promote** so main merge needs no sync/archive, and needs prompt-less first adopt plus deep adopt verification so agents cannot ship hallucinated PROJECT/AGENTS content.

## What Changes

- **BREAKING** — Replace staging-first “close only on `main` after promote” with **close after staging QA, before `/lsi:promote`** (human). Promote merges already-closed work; staging regressions become follow-up OpenSpec changes.
- Document and enforce **human lane (1–8)** vs **bot lane (9–19)** vs **human promote/release (20–24)** in overlay lifecycle, `/lsi:help`, and a shared bot playbook for Cursor, Claude Code, and OpenCode.
- Add **`/lsi:pr` modes A / B / C**: A = OpenSpec docs only; B = implementation (OpenSpec edits allowed); C = single PR for tiny tasks gated by `PR_WARN_LINES` / `PR_WARN_FILES` (refuse above `PR_MAX_*`).
- Require **initial docs commit** after propose (baseline before senior edits) and **always** a mode-A docs PR for normal work (mode C is the only single-PR escape).
- Add **address-findings** slash commands from the AI prompt library (senior, review, verify, readiness) plus optional **`/lsi:address-prowler`** before `/lsi:review` when a Prowler · Grok review exists on the Bitbucket PR.
- Replace AGENTS.md archive appends with **`openspec/CLOSED.md`** (or equivalent index); AGENTS.md only links it. `/lsi:close` emits pasteable commit commands (web handoff pattern) and does **not** require `main`.
- Upstream web-local commands into the overlay: `/lsi:release-train`, `/lsi:release-summary`, `/lsi:change-summary`, and close commit handoff.
- Add **OpenCode** agent-stack emit for local models (e.g. QwenCoder). Keep Junie / JetBrains / workflow `bin/` out. **Amends** in-flight `genericize-adopt-cursor-claude` Cursor+Claude-only policy → Cursor + Claude + OpenCode.
- Ship **`lsi-host-log`** as an **infra-only** Cursor skill via patch (not global).
- Add **`/lsi:adopt-verify`** (deep semantic + structural adopt verification against hallucination/drift) and **`install-adopt.sh`** (git-trello-style, prompt-less first adopt).
- Update `/lsi:update` to fix/sync, ask for human review, and provide commit-command suggestions (no auto-commit).
- Update audit resolutions / `openspec_archive_timing` defaults and adopter patches for the new close timing.

## Capabilities

### New Capabilities

- `human-bot-openspec-lifecycle`: Human/bot/promote lanes, close-before-promote, PR modes A/B/C, bot playbook, docs-baseline commit, lifecycle doc/command updates.
- `address-findings-commands`: Slash commands to address senior/review/verify/readiness findings; optional Prowler gate before `/lsi:review`.
- `closed-change-index`: Closed-change index file; AGENTS.md pointer only; close commit handoff.
- `adopt-verify-deep`: `/lsi:adopt-verify` deep accuracy checks beyond structural parity.
- `install-adopt-bash`: Non-interactive `install-adopt.sh` for first adopt (git-trello-shaped).
- `opencode-agent-support`: Adopt/bootstrap emit for OpenCode alongside Cursor and Claude.
- `lsi-host-log-infra`: Infra patch skill for per-change SSH host logging.
- `lsi-release-train-commands`: Upstream `/lsi:release-train`, `/lsi:release-summary`, `/lsi:change-summary` into the shared agent stack.

### Modified Capabilities

- `lsi-help-slash-command`: Lifecycle / SDLC / next-command heuristics must describe close-before-promote, PR modes A/B/C, and human vs bot lanes (not close-on-main-after-promote).

## Impact

- Overlay docs: `openspec-git-integration.md`, `which-workflow.md`, adopt docs, `/lsi:help`, `/lsi:close`, `/lsi:pr`, `/lsi:promote`, `/lsi:update`, `/lsi:merge-desc`.
- New commands under `overlays/lsi/agent-stack/commands/` (+ Claude/OpenCode mirrors); expected-agent-stack lists; verify/audit scripts.
- `snippets/adopt.py` / `install-adopt.sh` / deeper verify scripts; audit rule for archive timing.
- Adopter patches (`web`, `infra`, others): archive-timing resolutions, preserve globs for intentional extras during transition, infra `lsi-host-log` skill.
- Sibling change `genericize-adopt-cursor-claude`: design must record OpenCode policy amendment before or with that change’s close.
- Bundle VERSION bump expected at release (BREAKING lifecycle) — not an apply task here.
