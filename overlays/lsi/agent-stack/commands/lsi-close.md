---
name: /lsi-close
id: lsi-close
category: Workflow
description: Production close — sync and archive OpenSpec change on main
---

Orchestrate **production close** after a change is merged to **`main`**: sync delta specs (if any), archive the change, update `AGENTS.md`.

**Canonical source:** [`docs/workflows/openspec-git-integration.md` § Production close](../../docs/workflows/openspec-git-integration.md#production-close-after-main-merge)

**Input:** Optionally specify change slug. If omitted, infer from conversation, recent merge, or `openspec list`.

**Steps**

1. **Branch gate (`main` only)**

   ```bash
   git branch --show-current
   git pull origin main
   ```

   - **Refuse** on ticket branches or **`staging`**
   - Instruct: checkout **`main`**, pull latest, then re-run `/lsi:close`

2. **Resolve change slug**

   ```bash
   openspec list --json
   ```

   - Prefer explicit slug from user input (especially after a cumulative promotion from **`staging`**)
   - On **`main`**, do **not** infer slug from branch name — ticket branches are not checked out here
   - If exactly one active change matches the recent promotion or conversation context, use it
   - If **multiple** active changes remain (`openspec list` shows more than one), use **AskUserQuestion** — list each slug with a one-line summary from `proposal.md`; do **not** guess or auto-select
   - If none match, ask user which change was just promoted to **`main`**

3. **Confirm production merge**

   Ask user to confirm the change code is merged to **`main`** (promotion PR merged or hotfix on main).

   Optionally verify `openspec/changes/<slug>/` still exists (not already archived).

4. **Verify task completion**

   Read `openspec/changes/<slug>/tasks.md`:
   - Count incomplete `- [ ]` tasks
   - Warn if any remain; ask user to confirm before continuing

5. **Sync delta specs (if any)**

   Check `openspec/changes/<slug>/specs/` for delta specs.

   - If deltas exist: invoke `/opsx:sync` for `<slug>` (inherits **`main`** gate)
   - If none or only `specs/README.md`: skip sync
   - If deltas exist but `openspec/specs/` already reflects them (e.g. sync ran on **`staging`** before staging-first policy): compare delta to target spec; skip sync when content is already merged and proceed to archive after user confirms

6. **Archive change**

   Invoke `/opsx:archive` for `<slug>` (inherits **`main`** gate).

7. **Update AGENTS.md**

   Remind user to add archive path to **Archived OpenSpec changes** in [AGENTS.md](../../AGENTS.md):

   ```markdown
   - `openspec/changes/archive/YYYY-MM-DD-<slug>/` — <short description> ([PR #N](url))
   ```

8. **Hotfix back-merge reminder**

   If user confirms hotfix path (change landed on **`main`** without staging QA):

   Remind to merge **`main`** back into **`staging`**:

   ```bash
   git checkout staging
   git pull origin staging
   git merge origin/main
   git push origin staging
   ```

**Output**

```
## Production close: <slug>

**Branch:** main ✓
**Synced:** yes / skipped (no delta specs)
**Archived to:** openspec/changes/archive/YYYY-MM-DD-<slug>/

**Next (optional):**
- Update AGENTS.md archived-changes list
- Hotfix only: merge main → staging
- Release train: /lsi:version → /lsi:changelog → /lsi:release
```

**Guardrails**

- **`main` only** — never close on staging merge
- Do **not** skip archive if user only merged to staging
- Prefer `/lsi:close` over manual sync+archive for consistent policy enforcement
- When multiple active changes exist, always prompt for slug selection — never auto-select
- Do **not** auto-commit AGENTS.md updates unless user asks
