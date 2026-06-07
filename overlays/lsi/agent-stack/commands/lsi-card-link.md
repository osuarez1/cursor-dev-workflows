---
name: /lsi-card-link
id: lsi-card-link
category: Workflow
description: Create Trello card for current branch and rename to match OpenSpec slug
---

Create a Trello card for work already on a **feature branch** (without a 24-char id), then **rename the current branch** to `{type}/{id}-<change-slug>` and verify OpenSpec alignment.

Use when `/opsx:propose` or early implementation happened on a branch **before** card setup — e.g. `chore/fix-review-nits` — instead of losing work by running `git ts` (which always creates a **new** branch).

**Canonical source:** [ticket-card-info.md](../../docs/workflows/ticket-card-info.md) · [git-trello.md](../../docs/sdlc/git-trello.md) · [`docs/workflows/openspec-git-integration.md`](../../docs/workflows/openspec-git-integration.md)

**Prerequisite:** An **open (in-progress) OpenSpec change** is **required**. Card title and description are drafted **only** from that change’s artifacts, then **redacted** before any Trello API call.

**Contrast with `/lsi:card`:** `/lsi:card` runs from **`main`** or **`staging`** and uses **`git ts`** (new card + **new** branch). **`/lsi:card-link`** runs **on the existing ticket branch** and keeps commits in place via **`git branch -m`**.

**Input:** Optionally specify change slug, or an existing Trello card id (24-char hex) to link without creating a card. Invoking this command counts as explicit consent to create/link the card and rename the branch.

**Steps**

1. **Resolve open OpenSpec change (required — refuse if missing)**

   ```bash
   openspec list --json
   git branch --show-current
   ```

   - If a slug was provided, verify `openspec/changes/<slug>/` exists and change is **not** complete/archived-only.
   - If only one **in-progress** active change exists, announce: "Using change: `<slug>`".
   - If multiple active changes exist, use the **AskQuestion tool** — do not guess.
   - **Stop** if `openspec list --json` has no in-progress change, or `proposal.md` is missing — run **`/opsx:propose`** first. Do not create or update Trello cards without OpenSpec context.

2. **Verify starting point**

   | Check | Pass | Fail action |
   |-------|------|-------------|
   | OpenSpec | In-progress change + `proposal.md` | Stop — `/opsx:propose` |
   | Branch | Ticket branch; **not** `main`, `staging`, or other protected branches | Stop — use `/lsi:card` from `main`/`staging` for greenfield work |
   | Trello id | **No** 24-char hex id in branch name yet | If id present **and** suffix matches slug → stop: already linked; run `/lsi:branch` |
   | Slug alignment | Branch suffix equals `<slug>` **or** branch is `{type}/<slug>` without id | If suffix ≠ slug, propose rename target `{type}/{id}-<slug>` after card step |

   Parse branch patterns:

   ```text
   chore/fix-review-nits              → type=chore, slug=fix-review-nits, id=missing
   feature/my-slug                    → type=feature, slug=my-slug, id=missing
   chore/6a252db09bf782984e08e2be-fix-review-nits → id present (already linked)
   ```

3. **Read OpenSpec context (sole source for card body)**

   Read for the resolved slug:

   - `openspec/changes/<slug>/proposal.md`
   - `openspec/changes/<slug>/tasks.md`
   - `openspec/changes/<slug>/design.md` (if present)

   Also read [PROJECT.md](../../PROJECT.md) for `TITLE_PREFIX` (or `REPO_NAME |` convention).

4. **Draft and redact ticket-card fields (required before card API)**

   Output exactly per [ticket-card-info.md](../../docs/workflows/ticket-card-info.md) — three separate fenced blocks:

   | Field | Rules |
   |-------|------|
   | **Task type** | `feature`, `bugfix`, `hotfix`, `chore`, or `release` — infer from branch prefix when valid; else from proposal scope |
   | **Task title** | `TITLE_PREFIX` + imperative phrase from proposal **Why** / **What** (≤ ~60 chars total) |
   | **Task description** | **Only** from OpenSpec: Context/Goal ← proposal Why; Acceptance Criteria ← `tasks.md` checkboxes; Technical Notes ← design + impact. Link `openspec/changes/<slug>/`; note dual ticketing |

   **Redact before Trello** (apply to title + description):

   - Remove secrets, tokens, `.env`, credentials paths, `MAINTAINER.md` org-specific slugs
   - Replace absolute home paths with placeholders; keep repo-relative paths
   - Omit ad-hoc agent prose not grounded in OpenSpec files
   - Show redacted draft to user in the three blocks before API call

   **Rename target after link:**

   ```text
   {task-type}/{24-char-trello-id}-<change-slug>
   ```

5. **Create or link Trello card**

   **Path A — create card (default):**

   Source credentials: `source ~/.trello_secrets` ([git-trello.md](../../docs/sdlc/git-trello.md)).

   Create card via Trello API (same payload as `git ts`; do **not** run `git ts`):

   ```bash
   source ~/.trello_secrets
   MEMBER_ID=$(curl -s "https://api.trello.com/1/members/me?key=$API_KEY&token=$TOKEN" | jq -r '.id')
   CREATE_BODY=$(curl -s -X POST \
     --data-urlencode "name=<REDACTED_TASK_TITLE>" \
     --data-urlencode "desc=<REDACTED_TASK_DESCRIPTION>" \
     --data-urlencode "idList=$TARGET_LIST_ID" \
     --data-urlencode "idMembers=$MEMBER_ID" \
     "https://api.trello.com/1/cards?key=$API_KEY&token=$TOKEN")
   CARD_ID=$(echo "$CREATE_BODY" | jq -r '.id')
   ```

   **Path B — link existing card (user supplied id):**

   - Validate id matches `[a-f0-9]{24}`.
   - **Update** card with redacted OpenSpec description (replace stale body):

   ```bash
   curl -s -X PUT \
     --data-urlencode "name=<REDACTED_TASK_TITLE>" \
     --data-urlencode "desc=<REDACTED_TASK_DESCRIPTION>" \
     "https://api.trello.com/1/cards/$CARD_ID?key=$API_KEY&token=$TOKEN"
   ```

   If API or credentials fail, stop and point to [git-trello.md](../../docs/sdlc/git-trello.md).

6. **Rename current branch (keep commits)**

   ```bash
   git branch -m "${TASK_TYPE}/${CARD_ID}-${CHANGE_SLUG}"
   ```

   - **`CHANGE_SLUG`** = OpenSpec folder name exactly (kebab-case).

7. **Sync with OpenSpec**

   ```bash
   git branch --show-current
   openspec list --json
   ```

   Confirm branch suffix equals change slug. Optional: `git tc "Linked branch to openspec/changes/<slug>/"`

8. **Remote branch (if previously pushed)**

   ```bash
   git push -u origin "$(git branch --show-current)"
   ```

**Output**

```
## Trello card linked

**Change:** <slug>
**Card id:** <24-char-id>
**Branch:** <type>/<id>-<slug>  (renamed in place)
**Description:** redacted from OpenSpec artifacts

Next: `/opsx:apply` or continue implementation; `/lsi:branch` to re-verify.
```

**Guardrails**

- **Require** open OpenSpec change — never invent card copy without `proposal.md` + `tasks.md`.
- **Redact** before every Trello create/update.
- **Only** on a non-protected feature branch — never on `main` or `staging`.
- **Never** run `git ts` for this flow.
- If branch already has valid id + matching slug, refuse — use `/lsi:branch`.
