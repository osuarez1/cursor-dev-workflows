## Context

Today’s overlay lifecycle keeps `openspec/changes/<slug>/` active through staging QA and runs `/lsi:close` only on **`main`** after promote. Web and infra dogfood a richer local stack (release-train, change-summary, close commit handoff, infra `lsi-host-log`) that never landed in the bundle. Exploration against those repos plus the attached AI prompt library produced a human/bot split and close-before-promote policy.

Constraints: docs-only bundle; Bitbucket + Trello via [git-trello-tool](https://github.com/osuarez1/git-trello-tool); adopters consume via `snippets/adopt.py`; in-flight `genericize-adopt-cursor-claude` deleted OpenCode — this change re-adds OpenCode only (not Junie/JetBrains/`bin`).

Stakeholders: bundle maintainers, web/infra adopters, coding agents (Cursor, Claude Code, OpenCode/QwenCoder).

## Goals / Non-Goals

**Goals:**

- Normative human (1–8) / bot (9–19) / human close+promote (20–24) lifecycle.
- Close after staging QA, before promote; main needs no OpenSpec close work.
- PR modes A/B/C with Mode C line/file gates from PROJECT.md tokens.
- Address-* + optional Prowler commands; CLOSED.md index; adopt-verify + install-adopt.sh.
- OpenCode emit; infra-only host-log skill; upstream web release-train family.
- Single-purpose slash commands with verify-shaped structured Output (no Next / no follow-up steering).

**Non-Goals:**

- Implementing application features in adopter repos.
- Auto-merge, auto-push, or auto-commit without explicit user request.
- Reintroducing Junie, JetBrains AI, or workflow `bin/lsi-*` / `bin/opsx-*`.
- Making Mode C the default path.
- Closing or archiving on every staging merge (change stays active until post-QA close).

## Decisions

### D1 — Close timing: after staging QA, before promote (option A)

**Choice:** Human runs `/lsi:close` on the ticket branch (or staging-synced ticket branch) after QA/CI pass, then `/lsi:promote`. Archive + sync land in commits that promote carries to main.

**Alternatives:** Close on main after promote (current) — rejected (main churn). Close before staging code PR — rejected (archives before staging validation).

**Implication:** Audit id `openspec_archive_timing` default becomes close-before-promote (not `lsi_close_on_main`). Hotfix path: close on ticket/hotfix branch before promote, or document hotfix exception.

### D2 — PR modes A / B / C

| Mode | Scope | Gate |
|------|--------|------|
| A | `openspec/` (+ allowed workflow docs); no `SOURCE_ROOT` | Default first PR |
| B | Implementation; OpenSpec edits OK | After A merged (unless C) |
| C | Docs + impl one PR | Explicit opt-in; ≤ `PR_WARN_LINES` and ≤ `PR_WARN_FILES`; refuse if over `PR_MAX_LINES` / `PR_MAX_FILES` |

`/lsi:pr` requires mode argument or infers from diff and asks to confirm.

### D3 — CLOSED.md index

**Path:** `openspec/CLOSED.md` at adopter (and bundle) root of OpenSpec tree.

**AGENTS.md:** single pointer under workflows section — no per-change bullet list.

**Close handoff:** emit pasteable `git add` / `git commit` (web pattern); never auto-commit.

### D4 — Bot playbook artifact

Single markdown playbook (e.g. `overlays/lsi/agent-stack/bot-lane.md` or under adopter-docs) listing steps 9–19. Cursor/Claude invoke via slash commands; OpenCode loads playbook + AGENTS.md. No separate orchestration daemon.

### D5 — Address commands + Prowler gate

New commands: `lsi-address-senior`, `lsi-address-review`, `lsi-address-verify`, `lsi-address-readiness`, `lsi-address-prowler`.

Prowler: before `/lsi:review`, if open Bitbucket PR comments include a body starting with `Prowler · Grok Bot review`, run address-prowler first (or instruct user). Skip if no PR / no matching comment.

### D6 — OpenCode support

Emit `.opencode/` command or instruction stubs mirroring LSI+opsx entry points (or a thin pointer to the bot playbook). `adopt.py` accepts optional `agents_opencode: { enabled: true }` (default on for new template, or default off with opt-in — **prefer default on** when regenerating agent stack so QwenCoder works without patch surgery). Still reject `agents_junie`, `agents_jetbrains`, `bin`.

Amends sibling change’s “Cursor + Claude only” tests to allow `.opencode/`.

### D7 — install-adopt.sh

Modeled on git-trello `install.sh`: run from target repo; flags/env for `--bundle`, `--repo-name`, `--accept-policy-defaults`; calls `adopt.py`; runs structural verify; exits non-zero on failure. Does not invent domain overlay prose — leaves that to humans + `/lsi:adopt-verify`.

### D7b — Cleanup for fresh install

**Choice:** Ship `cleanup-adopt.sh` (deterministic) plus `/lsi:adopt-clean` (slash wrapper that runs/documents the script). Removes **adopt-managed** artifacts so `install-adopt.sh` can reinstall cleanly.

**Remove (default):** adopt-installed LSI commands under `.cursor/commands/lsi-*.md` (and Claude/OpenCode mirrors if present), adopt-managed `.cursor/rules/` workflow rules, regenerable `.lsi/workflows/` tree (except paths listed in patch `preserve` / `preserve_agent_stack`).

**Never remove without explicit override:** `PROJECT.md`, `patches` are N/A on adopter, application source, `preserve` globs, `openspec/` change history, `AGENTS.md` domain content outside LSI marker blocks (marker blocks may be stripped or left for merge — prefer strip only `<!-- lsi:workflows -->` managed sections when safe).

**Safety:** dry-run lists paths; require `--yes` (script) or explicit user confirm (slash) before delete. Single-purpose: cleanup only — does not run install or adopt-verify (D11).

**Fresh install sequence (documented, not chained):** `cleanup-adopt.sh` → `install-adopt.sh` → `/lsi:adopt-verify`.

### D8 — `/lsi:adopt-verify`

Two layers: (1) deterministic scripts (parity, links, token presence, unresolved `{{`, hash/version drift); (2) agent checklist comparing PROJECT.md / AGENTS domain claims to repo reality. Output findings table + fix suggestions; no auto-commit.

### D9 — infra host-log

Ship under `patches/files/infra/` (skill tree) + `preserve_agent_stack` / overlay install hook so `/lsi:update` does not delete it. Not installed for web or other repos.

### D10 — Upstream web commands

**New command files:** Copy/adapt `lsi-release-train`, `lsi-release-summary`, `lsi-change-summary` into `overlays/lsi/agent-stack/commands/` with bundle-relative paths (not `.lsi/`-only). Genericize web-only script paths via PROJECT.md / versioning overlay.

**Harden existing commands from web** (source of truth: web `.cursor/commands/`, strip domain contamination):

| Command | Upstream from web | Keep generic |
|---------|-------------------|--------------|
| `/lsi:commit` | Required explanatory body; plan entries with files + body; never subject-only; do not hand-write `Trello-Card:` | Scope table from per-repo integration overlay / PROJECT — not video-encoder worker table |
| `/lsi:changelog` | Required rewrite of generator draft: strip `type(scope):`, one user-visible bullet, collapse dupes, fold OpenSpec archive noise | Script path via versioning overlay / PROJECT |
| `/lsi:readiness` | Use `TEST_COMMAND` from PROJECT.md; docs-only N/A exemption; never draft PR title/body | No hardcoded `bin/rspec-changed` / pytest in shared command |
| `/lsi:review` | Never draft PR title/body; single-purpose stop | Focus areas from integration doc / patch — not embedded FFmpeg/S3 tables in shared command |
| `/lsi:senior` | Full report shape from `senior-analysis-report.template.md` / web dogfood: executive summary, design verdict vocabulary (Sound / Acceptable with follow-ups / Rethink), per-LC Intent/Before-After/Alternatives/Unit verdict, relationship to code review; Deep for multi-capability or BREAKING workflow changes (do not Skip OpenSpec lifecycle work as “docs-only”) | Tier signals + `TEST_COMMAND` from integration overlay / PROJECT — not hardcoded FFmpeg/pytest; no Next footer (D11) |

### D11 — Slash commands are single-purpose (no Next, no chaining)

**Choice:** Every slash command ends after its deliverable. No `Next:` footers, no “run X then Y”, no follow-up questions that pick the user’s next workflow step. The user (or bot playbook / human lane doc) decides sequencing.

**`/lsi:pr` specifically:** Draft title/body (modes A/B/C), optional push/PR create confirmation only. Do **not** invoke `/lsi:readiness`, `/lsi:review`, or `/opsx:verify` inside `/lsi:pr`. Prerequisites remain documented in the lifecycle playbook; agents do not auto-run them.

**Model:** `/opsx:verify` — report verdict and stop.

**Exceptions:** `/lsi:help` topics `status` / `next` may suggest a command because that **is** the topic’s job. Address-* commands may run `/lsi:commit` when that is part of their defined deliverable (fix + commit), but MUST NOT emit a further Next after that.

**Alternatives rejected:** Orchestrator commands that chain readiness→review→PR (hides failures, steers the human).

### D12 — Structured Output on every slash command (verify-shaped)

**Choice:** Every maintained `/lsi:*` and `/opsx:*` command file MUST include an `**Output**` (or path-specific `**Output (...)**`) fenced skeleton. Agents MUST fill that skeleton on success so responses are structurally stable run-to-run.

**Skeleton rules (model: `/opsx:verify`):**

1. Top-level `##` title with identity placeholders (slug, branch, repo, etc.).
2. Labeled status lines with closed vocabularies where applicable (`**Verdict:**`, `**Recommendation:**`, `**Tasks:** N/M`).
3. Named `###` subsections for lists/tables; required empty sections use `(none)` rather than omitting the heading.
4. No `Next:` / follow-up steering inside the Output fence (D11).
5. Refuse / early-exit: same shell with fail verdict, or a documented short `## Refuse:` / `**Reason:**` block — never unstructured-only refusals.
6. Multi-path commands (e.g. `/lsi:update` maintainer vs adopter) document one skeleton per path; `/lsi:help` may use per-topic templates.

**Apply work:** Audit overlay + opsx command sources; add missing Output to `lsi-help` (topic templates already count if labeled), normalize `lsi-trello-list` / `lsi-update` / thin opsx commands (`apply`, `archive`, `explore`, `sync`, …); strip Next from existing fences (including `/opsx:verify`); require Output on all new commands in this change.

**Alternatives rejected:** Freeform “report and stop” prose (agents drift); JSON-only machine output (humans read chat); optional Output only on “important” commands.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Normative specs sync before production (close before main) | Explicit policy: staging-validated code + closed change promote together; follow-ups for staging bugs |
| Mode C abuse (large “tiny” PRs) | Hard refuse above PR_MAX_*; warn at PR_WARN_* |
| OpenCode vs nearly-done genericize change | Document amendment; update sibling tasks/tests in same release train or sequential apply |
| install-adopt.sh curl\|bash supply chain | Prefer local `--bundle` path; document checksum/tag pin for remote install |
| Deep adopt-verify false positives | Severity tiers; resolutions file pattern like audit-resolutions |
| Adopter AGENTS.md archive lists huge | Migration: generate CLOSED.md from existing AGENTS section once, then delete bullets |
| Users forget readiness before PR | Lifecycle + bot playbook document order; `/lsi:pr` stays PR-only (D11) |

## Migration Plan

1. Land OpenSpec docs (this change) via Mode A PR on bundle.
2. Apply: overlay commands/docs/scripts; bump expected command lists.
3. Amend or finish `genericize-adopt-cursor-claude` OpenCode tests.
4. Re-sync adopters (`/lsi:update` + `/lsi:adopt-verify`); migrate AGENTS archives → CLOSED.md.
5. Bundle VERSION minor/major per docs versioning (BREAKING lifecycle) at release.

**Rollback:** Revert overlay lifecycle to close-on-main; keep new commands inert or behind help text. CLOSED.md can coexist with AGENTS lists temporarily.

## Open Questions

- Default `agents_opencode` on vs opt-in per patch (design leans **on**).
- Exact branch gate for `/lsi:close` when promoting from accumulated `staging` (ticket branch vs staging checkout) — prefer ticket branch with staging merged.
- Whether Mode A may include non-openspec workflow docs under `.lsi/workflows` patches only (lean **openspec/ only** for Mode A purity).
