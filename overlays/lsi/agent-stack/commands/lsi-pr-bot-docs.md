---
name: /lsi-pr-bot-docs
id: lsi-pr-bot-docs
category: Workflow
description: Unattended Mode A openspec PR review (readiness + senior + plan-gap)
---

Unattended review session for a **Mode A** (`openspec/`-only) Bitbucket PR. Nested readiness, senior, and plan-gap are this command's deliverable. `/lsi:readiness` is required for Mode **A**, **B**, and **C** reviews (Mode B/C → `/lsi:pr-bot`).

**Canonical source:** [bot-sessions.md](../bot-sessions.md) · [pr-production-readiness.md](../../docs/workflows/pr-production-readiness.md) · [senior-analysis.md](../../docs/workflows/senior-analysis.md) · [integrations.md](../../docs/workflows/integrations.md)

**Input:** `<PR>` (number or `https://bitbucket.org/<workspace>/<repo>/pull-requests/123`). Optional `--fix`.

| | default | `--fix` |
|---|---|---|
| readiness | one `/lsi:readiness` | readiness ⇄ `/lsi:address-readiness` (≤3) |
| senior | one Deep run, full report posted | Deep ⇄ `/lsi:address-senior` (≤3) |
| plan-gap | table + verdict | remediates via **same** 3-cycle senior budget (no second budget) |
| access token | optional | **required** (`whoami` bot) |

**Steps**

Re-read this file and [bot-sessions.md](../bot-sessions.md) at the start of every step.

1. **Setup** — bot-sessions Setup (`kind=review-docs`). Refuse if any diff path is outside `openspec/` (Mode B/C → `/lsi:pr-bot`).
2. **Readiness loop** — `/lsi:readiness` ⇄ `/lsi:address-readiness` (budget 3 when `--fix`). Docs-only `TEST_COMMAND` may be **N/A**. If not `Ready` after budget, continue with skip reason `bot session: readiness NEEDS HUMAN`.
3. **Senior loop** — `/lsi:senior` at **Deep** tier. Post the **full** report each iteration (helper multi-part). Save under `.senior-analyses/<ts>_<slug>.md`.
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
   | 6 | No `/opsx:sync`, `/opsx:archive`, `/lsi:close` as apply deliverables | … |
   | 7 | Proposal capabilities ↔ `specs/` folders | … |

   Verdict: **Plan ready** | **Plan gaps**.

   With `--fix`, remediate gaps via `/lsi:address-senior` against the **same** 3-cycle budget already used by the senior loop. Cycles already spent count. If budget exhausted and gaps remain → `NEEDS HUMAN` (do not start a fresh loop).
5. **Close** — bot-sessions Close. `PASS` only if readiness is `Ready`, senior pass condition met, **and** plan-gap is `Plan ready`.

**Output**

```
## PR bot docs: <PR> (<slug>)

**Mode:** A · **Fix:** <yes|no>
**Gates:** readiness=<…> senior=<…> plan-gap=<…>
**Session verdict:** <PASS | NEEDS HUMAN | STOPPED>
**Address cycles:** readiness a/3 · senior b/3
**Log:** `.reviews/<file>`
**Senior save:** `.senior-analyses/<file>`
```

**Output (refuse)**

```
## Refuse: /lsi-pr-bot-docs

**Reason:** <missing PR | wrong host | mode mismatch | dirty tree | …>
**Fix:** <one line>
```

**Guardrails**

- Nested `/lsi:readiness`, `/lsi:senior`, `/lsi:address-*`, and plan-gap are the documented deliverable
- Never authorize: other PRs/tickets; approve; merge; decline; request-changes; force-push; history rewrite; protected-branch push; edit/delete/resolve comments
- Full senior report always posted in this session (bot invocation = user asks)
- Readiness has its own 3-cycle budget; senior + plan-gap share one 3-cycle senior budget; no `Next:` footer
- Commit/push only via `.lsi/bin/lsi-bitbucket` when `--fix`
- Redact secrets from posts and logs
