---
name: /lsi-close
id: lsi-close
category: Workflow
description: Close OpenSpec change on main after promotion merge — sync, archive, CLOSED.md
---

Orchestrate **close after promotion** on **`main`**: sync delta specs (if any), archive the change, append `openspec/CLOSED.md`, emit pasteable commits.

**Canonical source:** [`docs/workflows/openspec-git-integration.md` § Close after promote](../../docs/workflows/openspec-git-integration.md#close-after-promote)

**Input:** Optionally specify change slug. If omitted, infer from `openspec list` or recent promotion context.

**Steps**

1. **Branch gate (`main` only)**

   ```bash
   git branch --show-current
   ```

   - **Require** `main`
   - **Refuse** ticket branches, `staging`, and any other branch
   - Confirm the promotion PR for this change is **merged** into `main` (user confirmation + `git log` / Bitbucket as needed)

2. **Resolve change slug**

   ```bash
   openspec list --json
   ```

   - Prefer user input; else match an active `openspec/changes/<slug>/` that landed via the promotion
   - If multiple active changes, use **AskQuestion** — do not guess

3. **Confirm promotion + staging QA**

   Ask user to confirm:
   - Staging QA / CI passed before promote
   - Promotion to **`main`** has merged

   Do not close without both confirmations.

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

**Branch:** main ✓
**Promotion merge:** confirmed
**Staging QA:** confirmed
**Synced:** yes / skipped (no delta specs)
**Archived to:** openspec/changes/archive/YYYY-MM-DD-<slug>/
**CLOSED.md:** appended

### Commit handoff
git add openspec/changes/archive/YYYY-MM-DD-<slug>/ openspec/CLOSED.md openspec/specs/
git commit -m "docs(openspec): close <slug> after promotion"
```

**Output (refuse)**

```
## Refuse: /lsi:close

**Reason:** Must run on main after the promotion PR is merged (not on ticket branch or staging).
**Fix:** merge the promotion PR to main, checkout main, pull, re-run /lsi:close
```

**Guardrails**

- **`main` only** after promotion merge — refuse ticket branches and `staging`
- Do **not** close before `/lsi:promote` merges
- Prefer `/lsi:close` over manual sync+archive
- When multiple active changes exist, always prompt for slug — never auto-select
- Do **not** auto-commit; do **not** emit a Next footer
- Agents MUST emit the Output skeleton above
