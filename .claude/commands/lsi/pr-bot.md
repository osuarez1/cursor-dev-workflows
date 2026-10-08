---
description: Unattended Mode B PR review session (verify/readiness/review loops)
---

Unattended review session for a **Mode B** (implementation) Bitbucket PR. Nested gates are this command's deliverable.

**Canonical source:** [bot-sessions.md](../bot-sessions.md) · [integrations.md](../../docs/workflows/integrations.md) · [openspec-git-integration.md](../../overlays/lsi/docs/workflows/openspec-git-integration.md)

**Input:** `<PR>` (number or `https://bitbucket.org/<workspace>/<repo>/pull-requests/123`). Optional `--fix`.

| | default | `--fix` |
|---|---|---|
| gates | one run each, posted | loops per [bot-sessions.md](../bot-sessions.md) (≤3 address cycles/gate) |
| `address-*` | post `Skipped — --fix not set` | run; commit + push via helper |
| access token | optional (warn if not bot) | **required** (`whoami` bot) |

**Steps**

Re-read this file and [bot-sessions.md](../bot-sessions.md) at the start of every step.

1. **Setup** — follow bot-sessions Setup (`kind=review`). Refuse if PR diff touches **only** `openspec/` (Mode A → use `/lsi:pr-bot-docs`).
2. **Verify loop** — `/opsx:verify` ⇄ `/lsi:address-verify` (budget 3 when `--fix`).
3. **Readiness loop** — `/lsi:readiness` ⇄ `/lsi:address-readiness` (budget 3 when `--fix`).
4. **Review loop** — `/lsi:review` ⇄ `/lsi:address-review` (budget 3 when `--fix`). Prowler is handled inside `/lsi:review` (exclude bot comments via helper `list --exclude-bot`).
5. **Readiness re-check** — if review cycles changed files, one `/lsi:readiness` (no loop).
6. **Change summary** — run `/lsi:change-summary`; post full output.
7. **QA test plan** — from `origin/<destination>...HEAD` + change artifacts, post a plan with: scope / out-of-scope; preconditions; numbered cases (goal, steps, expected); edge/negative; regression; `- [ ]` checklist (≥ one item per case + setup + regression); rollback / known limitations.
8. **Close** — bot-sessions Close format. Verdict `PASS` only if verify/readiness/review all passed (or nits fully addressed); else `NEEDS HUMAN` / `STOPPED`.

**Output**

```
## PR bot: <PR> (<slug>)

**Mode:** B · **Fix:** <yes|no>
**Session verdict:** <PASS | NEEDS HUMAN | STOPPED>
**Gates:** verify=<…> readiness=<…> review=<…>
**Log:** `.reviews/<file>`
```

**Output (refuse)**

```
## Refuse: /lsi-pr-bot

**Reason:** <missing PR | wrong host | mode mismatch | dirty tree | …>
**Fix:** <one line>
```

**Guardrails**

- Nested `/opsx:verify`, `/lsi:readiness`, `/lsi:review`, address-*, `/lsi:change-summary` are the documented deliverable
- Never authorize: other PRs/tickets; approve; merge; decline; request-changes; force-push; history rewrite; protected-branch push; edit/delete/resolve comments
- Commit/push only via `.lsi/bin/lsi-bitbucket` when `--fix`; never `git push` / `git commit` directly
- Loop budget 3 address cycles per gate; no `Next:` footer
- Redact secrets from posts and logs
