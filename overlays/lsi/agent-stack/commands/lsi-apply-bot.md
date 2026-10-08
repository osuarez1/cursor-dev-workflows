---
name: /lsi-apply-bot
id: lsi-apply-bot
category: Workflow
description: Unattended apply after Mode A merge; open Mode B PR
---

Implement an OpenSpec change after its Mode A PR merges to `PR_TARGET_BRANCH`, run gate loops, then open the Mode B PR. Always fixes (requires bot access token). Primary target: OpenCode local models; also Cursor and Claude Code.

**Canonical source:** [bot-sessions.md](../bot-sessions.md) · [bot-lane.md](../bot-lane.md) · [openspec-git-integration.md](../../docs/workflows/openspec-git-integration.md)

**Input:** `<slug>`. Optional `--mode-a <PR>`, `--resume`.

**Steps**

Re-read **this file** at the start of every step (local models: do not rely on memory).

### 0. Preconditions (refuse if any fail)

- `PR_HOST` is Bitbucket
- Mode A PR (arg or discovered) state `MERGED` into `PR_TARGET_BRANCH`
- `origin/<PR_TARGET_BRANCH>` contains `openspec/changes/<slug>/`
- Current branch is the ticket branch for `<slug>` with `PR_TARGET_BRANCH` merged in
- Clean tree; `.reviews/` ignored; `lsi-bitbucket whoami` reports bot

### 1. Setup / resume

- New run: create `SESSION_LOG`, `STATE=.reviews/<ts>_apply_<slug>.state.json`, record `START_SHA`
- `--resume`: load latest state for `<slug>`; continue from step pointer; if pending decision, wait for human choice

### 2. Lock decisions

Record Mode A merge SHA. Write `.reviews/<ts>_apply_<slug>.lock.md` listing each `design.md` decision and each spec requirement name, with a content hash of every change artifact at that SHA. Update state. Post step.

### 3. Apply by `tasks.md` section

For each section in `tasks.md`:

1. Re-read this file.
2. Run `/opsx:apply` for that section only; mark checkboxes.
3. **TEST_COMMAND** from `PROJECT.md`:
   - missing / empty / whitespace / `N/A` → post/log `Skipped — TEST_COMMAND unset`; do **not** fail; proceed to commit
   - set → run it; non-zero → human checkpoint (below)
4. Commit gate (bot-sessions) via `lsi-bitbucket commit` with a Conventional Commit subject from the section.
5. Update state JSON (step pointer, SHAs).

Do **not** run `/opsx:sync`, `/opsx:archive`, or `/lsi:close` as apply deliverables.

### 4. Gate loops

Same order and budgets as `/lsi:pr-bot` (verify → readiness → review, ≤3 address cycles each; readiness re-check after review if files changed). Commit + `lsi-bitbucket push` after mutating address steps.

### 5. Drift check

Diff `openspec/changes/<slug>/` vs lock SHA; evaluate implementation against each locked decision. Any artifact edit or contradiction → drift → human checkpoint. Do not create the Mode B PR while a decision is pending.

### 6. Human checkpoints

Raise when: drift; gate budget exhausted; `Rethink`-class finding; address proposes editing locked artifacts; `TEST_COMMAND` failed.

Present options: **accept** (record drift/rationale for PR body) | **revise** (continue fixing) | **abort**.

Write pending decision into state. If no human in-session → end with `PAUSED — awaiting decision`. Resume with `/lsi:apply-bot <slug> --resume`.

### 7. Mode B PR

When gates pass (or human accepted remaining issues per policy) and no pending decision:

1. Draft via `/lsi:pr` mode B (title/body per `pull-requests.md`)
2. Add `## Locked decisions` — Mode A PR link, decisions implemented, accepted drift + human rationale
3. `lsi-bitbucket push` then `lsi-bitbucket create-pr --source <branch> --dest <PR_TARGET_BRANCH> --title … --body-file …`
4. Close

**Output**

```
## Apply bot: <slug>

**Mode A PR:** <n> @ <merge sha>
**Session verdict:** <PASS | NEEDS HUMAN | STOPPED | PAUSED — awaiting decision>
**Mode B PR:** <url or none>
**Lock:** `.reviews/<lock>`
**State:** `.reviews/<state>`
**Log:** `.reviews/<file>`
```

**Output (refuse)**

```
## Refuse: /lsi-apply-bot

**Reason:** <Mode A PR not merged | no bot token | wrong host | dirty tree | …>
**Fix:** <one line>
```

**Guardrails**

- Nested `/opsx:apply`, verify/readiness/review address loops, `/lsi:pr` are the documented deliverable
- Bot-lane forbidden: `/lsi:close`, `/lsi:promote`, `/lsi:release*`, `/opsx:sync`, `/opsx:archive` (human close owns those). Do not do task work on protected integration branches (`PROTECTED_BRANCHES` / `PR_TARGET_BRANCH`)
- Never authorize: other PRs/tickets; approve; merge; decline; request-changes; force-push; history rewrite; protected-branch push; edit/delete/resolve comments
- Commit/push/`create-pr` only via `.lsi/bin/lsi-bitbucket`; never `git push` / `git commit` directly
- Loop budget 3 address cycles per gate; no `Next:` footer
- Redact secrets from posts and logs
