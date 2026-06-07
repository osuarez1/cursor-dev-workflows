---
name: /lsi-branch
id: lsi-branch
category: Workflow
description: Branch checklist and verify ticket-linked branch for active change
---

Run the video-encoder branch checklist and verify the ticket-linked branch for the active OpenSpec change.

**Canonical source:** [`docs/workflows/openspec-git-integration.md` § Branch checklist](../../docs/workflows/openspec-git-integration.md#branch-checklist) · [branch-workflow.md](../../docs/workflows/branch-workflow.md) · [git-trello.md](../../docs/sdlc/git-trello.md)

**Input:** Optionally specify a change slug after `/lsi:branch`. If omitted, resolve from conversation context or `openspec list --json`.

**Steps**

1. **Resolve active change**

   ```bash
   openspec list --json
   git branch --show-current
   ```

   - If a slug was provided, use it.
   - If only one active change exists, use it and announce: "Using change: `<slug>`".
   - If multiple active changes exist, use the **AskQuestion tool** to let the user select — do not guess.

2. **Verify branch checklist**

   Display checklist with current status:

   ```markdown
   - [ ] Current branch is not `main` or `staging`
   - [ ] Branch matches `feature|bugfix|hotfix|chore/{24-char-trello-id}-<change-slug>`
   - [ ] Branch suffix equals OpenSpec change slug exactly
   - [ ] `openspec list --json` shows the matching active change
   - [ ] `staging` merged or rebased into branch before final PR review
   ```

3. **Missing or wrong branch**

   If on `main` or `staging`, or branch lacks a 24-char Trello id, or suffix ≠ change slug:

   - **Stop** — do not run `git checkout -b feature/<slug>` or any branch without Trello id.
   - Suggest **`/lsi:card`** from **`main`** (never from `staging`) to create card + branch via `git ts`.
   - If card already exists, suggest `git tb <card_id>` per [git-trello.md](../../docs/sdlc/git-trello.md).

4. **Switch or sync existing ticket branch (when user confirms)**

   If branch exists and user is on wrong branch:

   ```bash
   git checkout <type>/<24-char-id>-<change-slug>
   git merge origin/staging   # or rebase if user prefers — ask if conflicts likely
   ```

5. **Read change context**

   Read `openspec/changes/<slug>/proposal.md` and `design.md` (if present) before implementation.

**Output**

```
## Branch: <type>/<id>-<change-slug>

**Change:** <slug>
**Branch status:** <verified | wrong branch | missing — use /lsi:card>
**Checklist:** <N/5 complete>

Next: `/opsx:apply` to implement tasks, or `/lsi:senior` if `design.md` exists and change is large.
```

**Guardrails**

- **Never** implement features on `main` or `staging`.
- **Never** create branches without Trello id — use **`/lsi:card`** + `git ts` only.
- Branch suffix must match active change slug exactly.
- Do not auto-run full lifecycle — branch verification only unless user confirms broader scope.
