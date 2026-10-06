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

**Choice:** Human runs `/lsi:close` on the **ticket branch** after QA/CI pass, then `/lsi:promote`. When promote is from accumulated `staging`, close still runs on the ticket branch **with staging merged into it** (not on a bare `staging` checkout). Archive + sync land in commits that promote carries to main.

**Alternatives:** Close on main after promote (current) — rejected (main churn). Close before staging code PR — rejected (archives before staging validation). Close while checked out on `staging` — rejected (prefer ticket branch + staging merge).

**Implication:** Audit id `openspec_archive_timing` default becomes close-before-promote (not `lsi_close_on_main`). Hotfix path: close on ticket/hotfix branch before promote, or document hotfix exception.

### D2 — PR modes A / B / C

| Mode | Scope | Gate |
|------|--------|------|
| A | **`openspec/` only**; no `SOURCE_ROOT`; no overlay/workflow/snippet paths | Default first PR |
| B | Implementation; OpenSpec edits OK | After A merged (unless C) |
| C | Docs + impl one PR | Explicit opt-in; ≤ `PR_WARN_LINES` and ≤ `PR_WARN_FILES`; refuse if over `PR_MAX_LINES` / `PR_MAX_FILES` |

`/lsi:pr` requires mode argument or infers from diff and asks to confirm. Mode A purity: refuse if the PR diff touches anything outside `openspec/`.

**Mode C token defaults** (from `patches/_template.yaml` / adopter PROJECT tokens):

| Token | Default |
|-------|---------|
| `PR_WARN_FILES` | `15` |
| `PR_WARN_LINES` | `250` |
| `PR_MAX_FILES` | `25` |
| `PR_MAX_LINES` | `400` |

Warn at WARN_*; hard refuse above MAX_*. On the docs-only bundle (no adopter `SOURCE_ROOT` / Mode C impl), Mode C is rarely used; if tokens are unset, `/lsi:pr` uses the template defaults above rather than inventing other numbers.

### D3 — CLOSED.md index

**Path:** `openspec/CLOSED.md` at adopter (and bundle) root of OpenSpec tree.

**AGENTS.md:** single pointer under workflows section — no per-change bullet list.

**Close handoff:** emit pasteable `git add` / `git commit` (web pattern); never auto-commit.

### D4 — Bot playbook artifact

Single markdown playbook (e.g. `overlays/lsi/agent-stack/bot-lane.md` or under adopter-docs) listing steps 9–19. Cursor/Claude invoke via slash commands; OpenCode loads playbook + AGENTS.md. No separate orchestration daemon.

### D5 — Address commands + Prowler gate

New commands: `lsi-address-senior`, `lsi-address-review`, `lsi-address-verify`, `lsi-address-readiness`, `lsi-address-prowler`.

Prowler: `/lsi:review` **MAY auto-invoke** `/lsi:address-prowler` first when an open Bitbucket PR has a comment body starting with `Prowler · Grok Bot review`, then continue with the review deliverable. Skip auto-chain when no PR / no matching comment. Standalone `/lsi:address-prowler` remains available. No Next footer after either path (D11).

### D6 — OpenCode support

Emit `.opencode/` command or instruction stubs mirroring LSI+opsx entry points (or a thin pointer to the bot playbook). `adopt.py` accepts optional `agents_opencode: { enabled: true }` — **opt-in** (default off / omitted = do not emit OpenCode). Patches that need QwenCoder set `agents_opencode` explicitly. Still reject `agents_junie`, `agents_jetbrains`, `bin`.

Amends sibling change’s “Cursor + Claude only” tests to allow `.opencode/` when opted in.

### D7 — install-adopt.sh

Modeled on git-trello `install.sh`: run from target repo; flags/env for `--bundle`, `--repo-name`, `--accept-policy-defaults`; calls `adopt.py`; runs structural verify; exits non-zero on failure. Does not invent domain overlay prose — leaves that to humans + `/lsi:adopt-verify`.

**Supply chain:** Prefer required local `--bundle <path-to-cursor-dev-workflows>` (or env `LSI_BUNDLE`). Remote curl|bash install, if documented at all, MUST pin tag/commit and checksum; default docs and examples use local `--bundle` only.

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

**Inventory (2026-10-05):** Diff of `web/.cursor/commands/lsi-*.md` vs overlay `agent-stack/commands/lsi-*.md` shows **exactly three** web-only commands: `lsi-release-train`, `lsi-release-summary`, `lsi-change-summary`. No other web `/lsi-*` files are missing from the overlay. All three are **in scope** for this change (tasks §5 / capability `lsi-release-train-commands`). Infra’s extra surface is the `lsi-host-log` skill (D9), not additional slash commands.

**New command files:** Copy/adapt those three into `overlays/lsi/agent-stack/commands/` with bundle-relative paths (not `.lsi/`-only). Genericize web-only script paths via PROJECT.md / versioning overlay. Note: `/lsi:release-train` intentionally composes version → changelog → release → summary as **one defined deliverable** (D11 allows that composition; still no Next footer).

**Harden existing commands from web** (source of truth: web `.cursor/commands/`, strip domain contamination):

| Command | Upstream from web | Keep generic |
|---------|-------------------|--------------|
| `/lsi:commit` | Required explanatory body; plan entries with files + body; never subject-only; do not hand-write `Trello-Card:` | Scope table from per-repo integration overlay / PROJECT — not video-encoder worker table |
| `/lsi:changelog` | Required rewrite of generator draft: strip `type(scope):`, one user-visible bullet, collapse dupes, fold OpenSpec archive noise | Script path via versioning overlay / PROJECT |
| `/lsi:readiness` | Use `TEST_COMMAND` from PROJECT.md; docs-only N/A exemption; never draft PR title/body | No hardcoded `bin/rspec-changed` / pytest in shared command |
| `/lsi:review` | Never draft PR title/body; single-purpose stop | Focus areas from integration doc / patch — not embedded FFmpeg/S3 tables in shared command |
| `/lsi:senior` | Full report shape from `senior-analysis-report.template.md` / web dogfood: executive summary, design verdict vocabulary (Sound / Acceptable with follow-ups / Rethink), per-LC Intent/Before-After/Alternatives/Unit verdict, relationship to code review; Deep for multi-capability or BREAKING workflow changes (do not Skip OpenSpec lifecycle work as “docs-only”) | Tier signals + `TEST_COMMAND` from integration overlay / PROJECT — not hardcoded FFmpeg/pytest; no Next footer (D11) |

### D11 — Slash commands are single-purpose (no Next; chaining only when defined)

**Choice:** The hard rule is **no `Next:` footers** and no follow-up questions that pick the user’s next workflow step. Nested slash-command execution **is allowed** when it is an **explicit part of the invoking command’s defined deliverable** (examples: `/lsi:release-train` composing version/changelog/release/summary; `/lsi:review` auto-running `/lsi:address-prowler` when a Prowler comment exists; address-* running `/lsi:commit`). Undocumented / opportunistic chaining is forbidden.

**`/lsi:pr` specifically:** Draft title/body (modes A/B/C), optional push/PR create confirmation only. Do **not** invoke `/lsi:readiness`, `/lsi:review`, or `/opsx:verify` inside `/lsi:pr` (those are not part of the PR deliverable). Prerequisites remain in the lifecycle playbook for humans/bots to run separately.

**Model for stop-after-report:** `/opsx:verify` — report verdict and stop (no Next).

**Exceptions:** `/lsi:help` topics `status` / `next` may suggest a command because that **is** the topic’s job.

**Alternatives rejected:** Next footers that steer sequencing; silent orchestration of readiness→review→PR inside `/lsi:pr`.

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
| Users forget readiness before PR | Lifecycle + bot playbook document order; `/lsi:pr` stays PR-only (does not auto-run readiness/review/verify) |

## Migration Plan

1. Land OpenSpec docs (this change) via Mode A PR on bundle (`openspec/` only).
2. Apply: overlay commands/docs/scripts; bump expected command lists.
3. Amend or finish `genericize-adopt-cursor-claude` OpenCode opt-in tests.
4. Re-sync adopters (`/lsi:update` + `/lsi:adopt-verify`); migrate AGENTS archives → CLOSED.md; enable `agents_opencode` only on patches that need it.
5. Bundle VERSION minor/major per docs versioning (BREAKING lifecycle) at release.

**Rollback:** Revert overlay lifecycle to close-on-main; keep new commands inert or behind help text. CLOSED.md can coexist with AGENTS lists temporarily.

## Open Questions

- (none — resolved 2026-10-05: OpenCode **opt-in**; close on **ticket branch with staging merged**; Mode A = **`openspec/` only**; Prowler **auto-chain from `/lsi:review` allowed**, no Next is the hard rule.)

## Senior analysis follow-ups (addressed)

Deep senior (2026-10-05) verdict was Acceptable with follow-ups. Closed in OpenSpec docs as follows:

| Follow-up | Resolution |
|-----------|------------|
| OpenCode default on vs opt-in | **Opt-in** (D6); sibling `genericize-adopt-cursor-claude` amended to allow opt-in |
| Close branch gate for accumulated staging | Ticket branch **with staging merged** (D1) |
| Mode A purity | **`openspec/` only** (D2) |
| D5 vs D11 Prowler | Auto-chain from `/lsi:review` allowed; hard rule is **no Next** (D5/D11) |
| `PR_WARN_*` / `PR_MAX_*` defaults | Template defaults 15/250 warn, 25/400 max (D2) |
| install-adopt supply chain | Local `--bundle` preferred/required in docs (D7) |
| AGENTS → CLOSED.md migration | Already in D3 + migration plan step 4; task 4.2 |
