---
name: /opsx-ff
id: opsx-ff
category: Workflow
description: Fast-forward — commit and push current branch without PR ceremony
---

Fast-forward the current change: stage all modified files, commit with a message derived from the active OpenSpec change, and push. For minor doc or config iterations that do not warrant readiness + review first.

**Canonical source:** [`docs/workflows/openspec-git-integration.md`](../../docs/workflows/openspec-git-integration.md) · [commits-logical-order.md](../../docs/workflows/commits-logical-order.md)

**Input:** Optional commit message override or change slug.

**Prerequisite:** Must be on a ticket branch (not `main` or `staging`).

**Steps**

1. **Resolve change** — from branch suffix or `openspec list --json`.

2. **Verify branch** — refuse `main` or `staging`.

3. **Show diff summary**

   ```bash
   git diff --stat
   git status --short
   ```

4. **Propose commit message** — derive from active change title and diff. Show to user before committing.

5. **Commit and push (only if user confirms)**

   ```bash
   git add -p   # or stage specific files
   git commit -m "..."
   git push
   ```

**Output**

```
## Fast-forward: <slug>

**Commit:** <subject>
**Pushed:** <branch>

Next: /lsi:readiness when ready for PR.
```

**Guardrails**

- Never commit secrets or key material.
- Refuse on `main` or `staging`.
- Always show proposed commit message before executing.
- Do not skip pre-commit hooks.
