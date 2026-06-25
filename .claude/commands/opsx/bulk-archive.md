---
description: Archive multiple completed OpenSpec changes on main
---

Archive multiple completed OpenSpec changes in one session. Use after multiple feature PRs have been merged to `main` and production close is overdue for several changes.

**Canonical source:** [`overlays/lsi/docs/workflows/openspec-git-integration.md` § Production close](../../overlays/lsi/docs/workflows/openspec-git-integration.md#production-close-after-main-merge)

**Input:** Optional list of change slugs. If omitted, lists all archivable candidates.

**Prerequisite:** Must be on **`main`** branch with all listed changes merged to `main`.

**Steps**

1. **Verify branch**

   ```bash
   git branch --show-current
   ```

   Refuse if not on `main`.

2. **List archivable changes**

   ```bash
   openspec list --json
   ```

   Filter: changes where all `tasks.md` items are `[x]` and no active PR exists.

3. **Confirm candidates** — show list; ask user which to archive. Do not auto-archive all.

4. **For each confirmed change (in order)**

   a. Check `tasks.md` — all `[x]`.
   b. Run `/opsx:sync` if normative delta specs exist.
   c. Run `/opsx:archive`.
   d. Update `AGENTS.md` archived-changes list.

5. **Report results**

   After each archive: ✓ or ✗ with reason.

**Output**

```
## Bulk archive

**Candidates:** <N changes>
**Confirmed:** <M changes>

### Results
- [x] <slug-1> — archived ✓
- [x] <slug-2> — archived ✓
- [ ] <slug-3> — skipped (reason)

AGENTS.md updated.
```

**Guardrails**

- Only run on **`main`** — refuse on ticket branches or `staging`.
- Never archive a change without explicit user confirmation for each slug.
- If any `tasks.md` items are unchecked, skip that change and warn.
- Run `/opsx:sync` before archive only when normative delta specs exist.
