---
name: /opsx-new
id: opsx-new
category: Workflow
description: Create a new OpenSpec change (quick propose shorthand)
---

Quickly create a new OpenSpec change without full ceremony. Shorthand for `/opsx:propose` when you know the slug and just need the change scaffolded.

**Canonical source:** [`docs/workflows/openspec-git-integration.md`](../../docs/workflows/openspec-git-integration.md)

**Input:** Change slug (required). Optionally a one-line description.

**Steps**

1. **Validate slug** — must be lowercase kebab-case, ≤ 60 chars. Refuse if a change with this slug already exists.

2. **Create change**

   ```bash
   openspec propose <slug>
   ```

3. **Open proposal for editing** — announce path: `openspec/changes/<slug>/proposal.md`.

4. **Remind next steps**

   - Fill in proposal → design → tasks.
   - Then `/lsi:card` for Trello card + branch, `/opsx:apply` to implement.

**Output**

```
## New change: <slug>

Created: openspec/changes/<slug>/

Next: edit proposal.md, then /lsi:card → /opsx:apply
```

**Guardrails**

- Refuse on `main` or `staging` for implementation — proposal creation is allowed.
- Do not auto-run `/lsi:card` or `/opsx:apply` without user confirmation.
