# Bot session skeleton

Shared Setup → steps → Close rules for `/lsi:pr-bot`, `/lsi:pr-bot-docs`, and `/lsi:apply-bot`. Each command declares its nested gates as its deliverable. Do **not** emit `Next:` footers.

**Helper:** `.lsi/bin/lsi-bitbucket` (adopt-managed). Agents MUST NOT call `git push` or `git commit` directly in bot sessions — use the helper. Credentials: `BB_*` via `${BB_SECRETS_FILE:-~/.bitbucket_secrets}` — see [integrations.md](../../docs/workflows/integrations.md).

**Placeholders** (from adopter `PROJECT.md`): `BASE_BRANCH`, `PR_TARGET_BRANCH`, `PROTECTED_BRANCHES`, `TEST_COMMAND`, `CANONICAL_DOCS_PATH`, `PR_HOST`.

Example PR URL shape: `https://bitbucket.org/<workspace>/<repo>/pull-requests/123`

---

## Authorization

Invoking one of the three bot commands is the explicit request to post to that one PR (apply-bot: create one PR) for that session. With `--fix` / apply-bot, also commit and push (no force) via the helper to that PR's source branch.

**Never authorized:** other PRs or tickets; approve / unapprove / merge / decline / request-changes; force-push; history rewrite; protected-branch push; edit / delete / resolve any comment (including the bot's own).

Redact secrets, tokens, `.env` values, credentials, and internal hostnames/IPs from every post and log.

---

## Setup (all sessions)

1. **PR host** — refuse unless `PR_HOST` is Bitbucket.
2. **Resolve PR** — `.lsi/bin/lsi-bitbucket info <PR>` (number or URL). Stop unless state is `OPEN` (apply-bot Mode A must be `MERGED` — see that command).
3. **Checkout** — `git fetch origin` then fast-forward-only checkout of the PR source branch. Non-ff → STOP.
4. **Change** — resolve exactly one active `openspec/changes/<slug>/` from the branch name. Zero or many → STOP.
5. **Clean tree** — `git status --porcelain` must be empty. Else `STOPPED — working tree not clean`.
6. **Ignore** — `git check-ignore -q .reviews/x` must succeed. Else STOP with fix: run `/lsi:update`. Do **not** edit `.gitignore`.
7. **Identity** — `.lsi/bin/lsi-bitbucket whoami`. Record method + bot flag. `--fix` / apply-bot require `bot: true`; else STOP with access-token fix line (integrations.md).
8. **Session log** — create `SESSION_LOG=.reviews/<YYYYMMDD-HHMMSS>_<kind>_<slug>.md` (`kind` = `review` | `review-docs` | `apply`). Record `START_SHA=$(git rev-parse HEAD)`, human starter (`git config user.name` only — no email), PR URL, change slug.
9. **Announce** — change slug, PR, mode, `--fix` on/off, bot identity.

Post Setup (and every later step) with:

```bash
.lsi/bin/lsi-bitbucket post <PR> <body-file> --step "<label>" --log "$SESSION_LOG"
```

---

## Commit gate (`--fix` / apply-bot only)

Before each mutating step, snapshot:

```bash
git status --porcelain=v1 -z > /tmp/lsi-bot-snap
```

After the step, stage **only** paths that changed vs the snapshot and are not ignored. Commit via:

```bash
.lsi/bin/lsi-bitbucket commit -m "<conventional subject>"
```

Push via:

```bash
.lsi/bin/lsi-bitbucket push
```

**Never stage:** `.reviews/`, `.senior-analyses/`, `.lsi/`, `.cursor/`, `.claude/`, `.opencode/`, `opencode.json`, `.env*`.

Pre-existing untracked files must not exist (tree clean at Setup). Do not sweep unrelated paths into the PR.

---

## Posting and skipped steps

- Every numbered step posts a comment (header `**LSI Bot Review**` via helper).
- Without `--fix`, each `address-*` step posts `Skipped — --fix not set` and does not edit.
- Bodies > 30 000 characters are split by the helper at `##` boundaries (`part i/N`) — never truncate silently.

---

## Loop budget

Per gate, at most **3** address cycles (≤ 4 runs of the gate itself) when fixing is enabled:

```
gate → (if not pass && fixing) address → gate …  (≤ 3 address cycles)
```

Order for pr-bot / apply-bot (Mode **B** / **C**):

1. verify ⇄ `/lsi:address-verify`
2. readiness ⇄ `/lsi:address-readiness`
3. review ⇄ `/lsi:address-review` (Prowler via `/lsi:review` auto-chain; exclude bot comments)
4. If review cycles changed files: one readiness re-check (no loop)

Order for pr-bot-docs (Mode **A**):

1. readiness ⇄ `/lsi:address-readiness`
2. senior ⇄ `/lsi:address-senior` (Deep; full report)
3. plan-gap check (remediation shares the senior address budget)

**Pass conditions**

| Gate | Pass |
|------|------|
| verify (`/opsx:verify`) | `Aligned` |
| readiness | `Ready` |
| review | `Approve` or `Approve with nits` (nits still addressed under `--fix`) |
| senior | `Sound`, or `Acceptable with follow-ups` with every follow-up in `tasks.md` |
| plan-gap | `Plan ready` |

Exhausted budget → session verdict **NEEDS HUMAN**; continue to summary / close (do not abort the rest of the session unless STOP).

`/lsi:readiness` runs on **every** Mode A, B, and C review session. If readiness is not `Ready` after its budget, later gates may still run with skip reason `bot session: readiness NEEDS HUMAN` (review for B/C; senior for A).

---

## STOP handling

On hard STOP (dirty tree, wrong host, mode mismatch, push rejected, missing token for `--fix`): post **Close** only with the reason; do not continue steps.

---

## Close format

Every session ends with a Close comment + Output:

```
## Close: <command> <PR or slug>

**Session verdict:** <PASS | NEEDS HUMAN | STOPPED | PAUSED — awaiting decision>
**START_SHA → HEAD:** <sha> → <sha>
**Steps posted:** <n>
**Address cycles:** verify a/3 · readiness b/3 · review c/3 (or readiness a/3 · senior b/3 for docs)
**Human starter:** <git user.name>
**Log:** `.reviews/<file>`
**Reason (if not PASS):** <one line>
```
