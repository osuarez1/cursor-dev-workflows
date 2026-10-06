---
name: /lsi-close
id: lsi-close
category: Workflow
description: Close OpenSpec change after staging QA — sync, archive, CLOSED.md (before promote)
---

Orchestrate **close before promote** after staging QA: sync delta specs (if any), archive the change, append `openspec/CLOSED.md`, emit pasteable commits.

**Canonical source:** [`docs/workflows/openspec-git-integration.md` § Close before promote](../../docs/workflows/openspec-git-integration.md#close-before-promote)

**Input:** Optionally specify change slug. If omitted, infer from branch suffix or `openspec list`.

**Steps**

1. **Branch gate (ticket branch)**

   ```bash
   git branch --show-current
   ```

   - **Require** ticket pattern `feature|bugfix|hotfix|chore/{24-char-id}-<change-slug>`
   - **Refuse** `main` (close is not a post-main-merge step)
   - **Refuse** bare `staging` checkout — merge `staging` into the ticket branch first when promoting accumulated staging work, then re-run on the ticket branch

2. **Resolve change slug**

   ```bash
   openspec list --json
   ```

   - Prefer user input; else branch suffix must match `openspec/changes/<slug>/`
   - If multiple active changes, use **AskQuestion** — do not guess

3. **Confirm staging QA**

   Ask user to confirm staging QA / CI passed for this change. Do not close without that confirmation.

4. **Verify task completion**

   Read `openspec/changes/<slug>/tasks.md`:
   - Count incomplete `- [ ]` tasks
   - Warn if any remain; ask user to confirm before continuing

5. **Sync delta specs (if any)**

   Check `openspec/changes/<slug>/specs/` for delta specs.

   - If deltas exist: invoke `/opsx:sync` for `<slug>`
   - If none or only `specs/README.md`: skip sync
   - If content already reflected in `openspec/specs/`: skip sync after user confirms

6. **Archive change**

   Invoke `/opsx:archive` for `<slug>`.

7. **Append `openspec/CLOSED.md`**

   Ensure `openspec/CLOSED.md` exists (create from template if missing). Append one row/bullet:

   ```markdown
   - `YYYY-MM-DD` — `<slug>` — <one-line from proposal Why> — archived `openspec/changes/archive/YYYY-MM-DD-<slug>/`
   ```

   Do **not** append a long archive list to `AGENTS.md`. AGENTS.md may only **link** `openspec/CLOSED.md`.

8. **Commit handoff (pasteable; do not auto-commit)**

   Emit copy-paste commands for archive + CLOSED.md (and sync diffs if any). Run `git commit` only if the user explicitly asks.

**Output**

```
## Close: <slug>

**Branch:** <ticket-branch> ✓
**Staging QA:** confirmed
**Synced:** yes / skipped (no delta specs)
**Archived to:** openspec/changes/archive/YYYY-MM-DD-<slug>/
**CLOSED.md:** appended

### Commit handoff
git add openspec/changes/archive/YYYY-MM-DD-<slug>/ openspec/CLOSED.md openspec/specs/
git commit -m "docs(openspec): close <slug> after staging QA"
```

**Output (refuse)**

```
## Refuse: /lsi:close

**Reason:** Must run on ticket branch after staging QA (not on main or bare staging).
**Fix:** checkout ticket branch; merge staging into it if needed; re-run /lsi:close
```

**Guardrails**

- Ticket branch only after staging QA — never require `main`; never close on bare `staging`
- Do **not** skip archive if user only merged Mode A/B to staging without QA
- Prefer `/lsi:close` over manual sync+archive
- When multiple active changes exist, always prompt for slug — never auto-select
- Do **not** auto-commit; do **not** emit a Next footer
- Agents MUST emit the Output skeleton above
