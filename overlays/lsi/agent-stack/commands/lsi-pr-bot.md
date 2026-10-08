---
name: /lsi-pr-bot
id: lsi-pr-bot
category: Workflow
description: Unattended Mode B/C review (Bitbucket PR or --local files+chat)
---

Unattended review session for a **Mode B** (implementation) or **Mode C** (tiny docs+impl) change. Nested gates are this command's deliverable. `/lsi:readiness` is required for Mode **A**, **B**, and **C** reviews (Mode A → `/lsi:pr-bot-docs`).

**Canonical source:** [bot-sessions.md](../bot-sessions.md) · [integrations.md](../../docs/workflows/integrations.md) · [openspec-git-integration.md](../../docs/workflows/openspec-git-integration.md)

**Input:** Either:

- **Remote:** `<PR>` (number or `https://bitbucket.org/<workspace>/<repo>/pull-requests/123`) and optional `--fix`
- **Local:** `--local` (no PR) and optional `--fix` — skip Bitbucket; save steps under `.reviews/` and print full bodies in chat

Refuse if both a PR and `--local` are given, or if neither is given.

| | default | `--fix` |
|---|---|---|
| gates | one run each | loops per [bot-sessions.md](../bot-sessions.md) (≤3 address cycles/gate) |
| `address-*` | `Skipped — --fix not set` | run; commit (remote: + push via helper; `--local`: commit only, no push) |
| access token | remote: optional (warn if not bot) | remote: **required** (`whoami` bot); `--local`: not required |

**Steps**

Re-read this file and [bot-sessions.md](../bot-sessions.md) at the start of every step.

1. **Setup** — remote: bot-sessions Setup (`kind=review`). `--local`: bot-sessions Setup (`--local`, `kind=review`). Refuse if diff vs `staging` touches **only** `openspec/` (Mode A → `/lsi:pr-bot-docs`). Mode **C** uses this command.
2. **Verify loop** — `/opsx:verify` ⇄ `/lsi:address-verify` (budget 3 when `--fix`).
3. **Readiness loop** — `/lsi:readiness` ⇄ `/lsi:address-readiness` (budget 3 when `--fix`).
4. **Review loop** — `/lsi:review` ⇄ `/lsi:address-review` (budget 3 when `--fix`). Prowler: remote only when a matching PR comment exists; `--local` skips Prowler auto-chain (no PR comments).
5. **Readiness re-check** — if review cycles changed files, one `/lsi:readiness` (no loop).
6. **Change summary** — run `/lsi:change-summary`; emit full output (remote: post; `--local`: file + chat).
7. **QA test plan** — from `staging...HEAD` (or PR destination) + change artifacts; same sections as before (scope, cases, checklist, rollback).
8. **Close** — bot-sessions Close. Verdict `PASS` only if verify/readiness/review all passed (or nits fully addressed); else `NEEDS HUMAN` / `STOPPED`.

**Output**

```
## PR bot: <PR|local> (<slug>)

**Mode:** B|C · **Local:** <yes|no> · **Fix:** <yes|no>
**Session verdict:** <PASS | NEEDS HUMAN | STOPPED>
**Gates:** verify=<…> readiness=<…> review=<…>
**Log:** `.reviews/<file or dir>`
```

**Output (refuse)**

```
## Refuse: /lsi-pr-bot

**Reason:** <missing PR|--local | both PR and --local | wrong host | mode mismatch | dirty tree | …>
**Fix:** <one line>
```

**Guardrails**

- Nested `/opsx:verify`, `/lsi:readiness`, `/lsi:review`, address-*, `/lsi:change-summary` are the documented deliverable
- Never authorize: other PRs/tickets; approve; merge; decline; request-changes; force-push; history rewrite; protected-branch push; edit/delete/resolve comments
- `--local`: never call `lsi-bitbucket post` / `push` / `whoami`; always write step files + chat
- Remote `--fix`: commit/push only via `.lsi/bin/lsi-bitbucket`; never `git push` / `git commit` directly
- `--local --fix`: commit allowed; never push
- Loop budget 3 address cycles per gate; no `Next:` footer
- Redact secrets from posts, files, and logs
