---
name: /lsi-trello-branch
id: lsi-trello-branch
category: Workflow
description: Checkout branch from existing Trello card via git tb
---

Create and checkout a ticket branch from an **existing** Trello card using **`git tb`**, after syncing the card description from an **open OpenSpec change** (redacted).

**Canonical source:** [git-trello.md](../../docs/sdlc/git-trello.md) · [ticket-card-info.md](../../docs/workflows/ticket-card-info.md) · [`docs/workflows/openspec-git-integration.md`](../../docs/workflows/openspec-git-integration.md)

**Prerequisite:** An **open (in-progress) OpenSpec change** is **required**. The Trello card description is **updated** from that change’s artifacts (redacted) before `git tb`.

**Contrast:**

| Command | When |
|---------|------|
| **`/lsi:card`** | New card + branch from `main`/`staging` (`git ts`) |
| **`/lsi:card-link`** | Card + rename **current** branch (keeps commits) |
| **`/lsi:trello-branch`** | Existing card → **new** branch (`git tb`) + OpenSpec card sync |
| **`/lsi:trello-list`** | Interactive picker → confirm → same as trello-branch |

**Input:** Trello card id (24-char hex). OpenSpec slug from active change (required unless exactly one in-progress change).

**Protected-branch exception:** Allowed on **`main`** or **`staging`** only. Invoking counts as consent to run **`git tb`** and update the card description.

**Steps**

1. **Resolve open OpenSpec change (required — refuse if missing)**

   ```bash
   openspec list --json
   git branch --show-current
   ```

   - **Stop** if no in-progress change or missing `proposal.md` — run **`/opsx:propose`** first.
   - If slug provided, verify folder exists and is active.
   - If one in-progress change, use it; if multiple, **AskQuestion** — do not guess.
   - Must be on **`main`** or **`staging`** (pull first). **Refuse** on ticket branches.

2. **Validate card id**

   - Must match `[a-f0-9]{24}` (argument or from `/lsi:trello-list`).
   - Fetch current card:

   ```bash
   source ~/.trello_secrets
   curl -s "https://api.trello.com/1/cards/<CARD_ID>?fields=name,desc&key=$API_KEY&token=$TOKEN" | jq .
   ```

3. **Read OpenSpec and draft redacted description**

   Read `openspec/changes/<slug>/proposal.md`, `tasks.md`, `design.md` (if present).

   Draft per [ticket-card-info.md](../../docs/workflows/ticket-card-info.md) — **mandatory clipboard blocks** in order: **Task type (copy below)**, **Task title (copy below)**, **Task description (copy below)**. Do **not** put field values outside those blocks.

   - **Context/Goal** ← proposal **Why**
   - **Acceptance Criteria** ← `tasks.md` `- [ ]` items
   - **Technical Notes** ← design + impact; link `openspec/changes/<slug>/`

   **Redact** before Trello: no secrets, `.env`, credentials, absolute paths, org-only slugs; no copy not grounded in OpenSpec files.

4. **Update Trello card (required before `git tb`)**

   Replace card name/description with redacted OpenSpec draft (title may stay board-visible short form if ≤60 chars):

   ```bash
   curl -s -X PUT \
     --data-urlencode "name=<REDACTED_TASK_TITLE>" \
     --data-urlencode "desc=<REDACTED_TASK_DESCRIPTION>" \
     "https://api.trello.com/1/cards/<CARD_ID>?key=$API_KEY&token=$TOKEN"
   ```

   - Do **not** run `git tb` until card update succeeds (or user explicitly skips update in writing — default is required).

5. **Run `git tb`**

   ```bash
   git tb <CARD_ID>
   ```

   - Task type: infer from proposal scope or branch intent; default **`chore`** for docs/process.
   - Default branch: `{type}/{id}-{title-derived-slug}`.

6. **Sync branch suffix with OpenSpec**

   ```bash
   git branch -m "${TASK_TYPE}/${CARD_ID}-${CHANGE_SLUG}"
   ```

   - **`CHANGE_SLUG`** = OpenSpec folder name exactly.

7. **Verify**

   ```bash
   git branch --show-current
   openspec list --json
   ```

   Optional: `git tc "Branch + card synced to openspec/changes/<slug>/"`

**Output**

```
## Branch from Trello card

**Change:** <slug>
**Card id:** <24-char-id>
**Branch:** <type>/<id>-<slug>
**Card description:** updated (redacted from OpenSpec)

Next: `/opsx:apply`; `/lsi:branch` to verify.
```

**Guardrails**

- **Require** open OpenSpec change — refuse without `proposal.md`.
- **Always** redact and sync card description before `git tb` (unless user explicitly skips).
- **Never** use `git checkout -b` without Trello id.
- Run from **`main`** or **`staging`** only.
- Branch suffix **must** match OpenSpec change slug after rename.
