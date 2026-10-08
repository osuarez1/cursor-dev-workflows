---
description: Unattended Mode A review (Bitbucket PR or --local files+chat)
---

Unattended review session for a **Mode A** (`openspec/`-only) change. Nested readiness, senior, and plan-gap are this command's deliverable. `/lsi:readiness` is required for Mode **A**, **B**, and **C** reviews (Mode B/C → `/lsi:pr-bot`).

**Canonical source:** [bot-sessions.md](../bot-sessions.md) · [pr-production-readiness.md](../../docs/workflows/pr-production-readiness.md) · [senior-analysis.md](../../docs/workflows/senior-analysis.md) · [integrations.md](../../docs/workflows/integrations.md)

**Input:** Either:

- **Remote:** `<PR>` (number or `https://bitbucket.org/<workspace>/<repo>/pull-requests/123`) and optional `--fix`
- **Local:** `--local` (no PR) and optional `--fix` — skip Bitbucket; save steps under `.reviews/` and print full bodies in chat

Refuse if both a PR and `--local` are given, or if neither is given.

| | default | `--fix` |
|---|---|---|
| readiness | one `/lsi:readiness` | readiness ⇄ `/lsi:address-readiness` (≤3) |
| senior | one Deep run, full report | Deep ⇄ `/lsi:address-senior` (≤3) |
| plan-gap | table + verdict | remediates via **same** 3-cycle senior budget (no second budget) |
| access token | remote: optional | remote: **required** (`whoami` bot); `--local`: not required |

**Steps**

Re-read this file and [bot-sessions.md](../bot-sessions.md) at the start of every step.

1. **Setup** — remote: bot-sessions Setup (`kind=review-docs`). `--local`: bot-sessions Setup (`--local`, `kind=review-docs`). Refuse if any path in `git diff staging...HEAD` is outside `openspec/` (Mode B/C → `/lsi:pr-bot`).
2. **Readiness loop** — `/lsi:readiness` ⇄ `/lsi:address-readiness` (budget 3 when `--fix`). Docs-only `TEST_COMMAND` may be **N/A**. If not `Ready` after budget, continue with skip reason `bot session: readiness NEEDS HUMAN`.
3. **Senior loop** — `/lsi:senior` at **Deep** tier. Always save under `.senior-analyses/<ts>_<slug>.md`. Remote: post the **full** report each iteration (helper multi-part). `--local`: write full report to `$SESSION_DIR/` + chat (and `.senior-analyses/`).
   - Verdict `Rethink` → no address cycle; session verdict `NEEDS HUMAN`; continue to plan-gap then Close.
   - With `--fix`: `/lsi:address-senior` until `Sound`, or `Acceptable with follow-ups` with every follow-up in `tasks.md`, max **3** address cycles.
4. **Plan-gap check** — emit checklist table:

   | # | Check | Result |
   |---|-------|--------|
   | 1 | `openspec validate <slug> --strict` | pass/fail |
   | 2 | Every spec requirement/scenario → ≥1 `tasks.md` item | … |
   | 3 | Every `design.md` decision reflected in specs/tasks; no contradiction | … |
   | 4 | Every task names files/areas; no undefined/forward deps | … |
   | 5 | Test work planned per `test-requirements.md` / `TEST_COMMAND` | … |
   | 6 | No administrative apply deliverables (close/sync/archive, promote, release-train family, `/lsi:update`, meta process) | … |
   | 7 | Proposal capabilities ↔ `specs/` folders | … |

   Verdict: **Plan ready** | **Plan gaps**.

   With `--fix`, remediate gaps via `/lsi:address-senior` against the **same** 3-cycle budget already used by the senior loop. Cycles already spent count. If budget exhausted and gaps remain → `NEEDS HUMAN` (do not start a fresh loop).
5. **Close** — bot-sessions Close. `PASS` only if readiness is `Ready`, senior pass condition met, **and** plan-gap is `Plan ready`.

**Output**

```
## PR bot docs: <PR|local> (<slug>)

**Mode:** A · **Local:** <yes|no> · **Fix:** <yes|no>
**Gates:** readiness=<…> senior=<…> plan-gap=<…>
**Session verdict:** <PASS | NEEDS HUMAN | STOPPED>
**Address cycles:** readiness a/3 · senior b/3
**Log:** `.reviews/<file or dir>`
**Senior save:** `.senior-analyses/<file>`
```

**Output (refuse)**

```
## Refuse: /lsi-pr-bot-docs

**Reason:** <missing PR|--local | both PR and --local | wrong host | mode mismatch | dirty tree | …>
**Fix:** <one line>
```

**Guardrails**

- Nested `/lsi:readiness`, `/lsi:senior`, `/lsi:address-*`, and plan-gap are the documented deliverable
- Never authorize: other PRs/tickets; approve; merge; decline; request-changes; force-push; history rewrite; protected-branch push; edit/delete/resolve comments
- `--local`: never call `lsi-bitbucket post` / `push` / `whoami`; always write step files + chat; full senior report in chat + files
- Remote: full senior report always posted (bot invocation = user asks)
- Readiness has its own 3-cycle budget; senior + plan-gap share one 3-cycle senior budget; no `Next:` footer
- Remote `--fix`: commit/push only via `.lsi/bin/lsi-bitbucket`; `--local --fix`: commit only, never push
- Redact secrets from posts, files, and logs
