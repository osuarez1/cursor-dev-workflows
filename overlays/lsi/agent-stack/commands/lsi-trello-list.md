---
name: /lsi-trello-list
id: lsi-trello-list
category: Workflow
description: Interactive To Do card picker — select card, confirm, sync OpenSpec, git tb
---

Fetch the Trello **To Do** list via **`git tl`**, show an **interactive card picker**, then — after **confirm or exit** — sync the selected card from an **open OpenSpec change** (redacted) and optionally run **`git tb`**.

**Canonical source:** [git-trello.md](../../docs/sdlc/git-trello.md) · [ticket-card-info.md](../../docs/workflows/ticket-card-info.md) · [`lsi-trello-branch.md`](lsi-trello-branch.md)

**Prerequisite:** An **open (in-progress) OpenSpec change** is **required** before confirm/branch steps. List-only exit (step 3 **Exit**) does not need OpenSpec.

**Input:** None. OpenSpec slug resolved from `openspec list --json` when branching.

**Steps**

1. **Verify git-trello install**

   ```bash
   git config --local --get alias.tl
   git branch --show-current
   ```

   - If missing alias, stop — [git-trello.md](../../docs/sdlc/git-trello.md).
   - Note branch — **`git tb`** requires **`main`** or **`staging`**.

2. **Fetch and parse cards**

   ```bash
   git tl
   ```

   - Parse `{24-char-id} | {title}` lines into `[{ id, title }, ...]`.
   - If empty, suggest **`/lsi:card`**. Stop.

3. **Interactive card picker (required)**

   Use **AskQuestion** — single select:

   - **Prompt:** `Select a Trello card to branch from (To Do list):`
   - **Options:** one per card (`id` = card id, `label` = title); last option `exit` / `Exit — list only, no branch`
   - If **>20 cards**, paginate AskQuestion rounds.

4. **Handle picker result**

   - **`exit`:** read-only table; stop — no OpenSpec required.
   - Card selected: store `SELECTED_ID`, `SELECTED_TITLE`; continue.

5. **Resolve open OpenSpec change (required before confirm)**

   ```bash
   openspec list --json
   ```

   - **Stop** if no in-progress change or missing `proposal.md` — run **`/opsx:propose`**, then re-run picker.
   - One change → use slug; multiple → **AskQuestion**.
   - Read `proposal.md`, `tasks.md`, `design.md` for redacted card draft (same rules as [lsi-trello-branch.md](lsi-trello-branch.md) step 3).

6. **Confirm before sync + `git tb` (required)**

   Use **AskQuestion**:

   - **Prompt:** `Sync card "{SELECTED_TITLE}" from OpenSpec "<slug>" and create branch?`
   - **Options:** `confirm` / `Confirm — update card and run git tb` · `exit` / `Exit — no branch`

   - **`exit`:** show id + slug; no API/git changes.

7. **Pre-flight branch check**

   - Must be on **`main`** or **`staging`** before `git tb`.
   - On ticket branch: stop with checkout instructions.

8. **Update card + run `git tb`**

   Follow [lsi-trello-branch.md](lsi-trello-branch.md) steps 4–7:

   - PUT redacted title/description to Trello for `SELECTED_ID`
   - `git tb <SELECTED_ID>`
   - `git branch -m "${TASK_TYPE}/${SELECTED_ID}-${CHANGE_SLUG}"`

9. **Verify**

   ```bash
   git branch --show-current
   ```

**Output (confirmed + branched)**

```
## Trello card selected

**Change:** <slug>
**Card:** {SELECTED_TITLE}
**Id:** {SELECTED_ID}
**Branch:** {type}/{id}-{slug}
**Card description:** updated (redacted from OpenSpec)

Next: `/opsx:apply` or `/lsi:branch`.
```

**Output (exit)**

```
## Trello To Do list

<table>

No branch created.
```

**Guardrails**

- **Require** open OpenSpec change for confirm/branch path — not for list-only exit.
- **Always** redact OpenSpec draft before Trello PUT.
- **Always** use **AskQuestion** for picker and confirm.
- **Never** run `git tb` on Exit or without OpenSpec sync (unless user explicitly skips card update in writing).
- **Never** invent card ids or description copy.
