---
description: Resume implementing a paused OpenSpec change
---

Resume implementing a paused or in-progress OpenSpec change. Re-reads context, shows remaining tasks, and picks up where you left off.

**Canonical source:** [`overlays/lsi/docs/workflows/openspec-git-integration.md`](../../overlays/lsi/docs/workflows/openspec-git-integration.md)

**Input:** Optional change slug. If omitted, auto-select the only in-progress change or ask.

**Steps**

1. **Select change**

   ```bash
   openspec list --json
   ```

   - If slug provided, use it.
   - If one in-progress change, auto-select and announce.
   - If multiple, ask user.

2. **Show current progress**

   ```bash
   openspec instructions apply --change "<slug>" --json
   ```

   Display: schema, N/M tasks complete, remaining tasks.

3. **Read context files** — proposal, design, tasks (from apply instructions).

4. **Resume implementation** — pick up from first unchecked task. Mark `- [ ]` → `- [x]` as you go.

5. **Pause if:**
   - Task is unclear → ask for clarification.
   - Error or blocker encountered → report and wait for guidance.

**Output**

```
## Resuming: <slug>

**Progress:** N/M tasks complete
**Next task:** <description>
```

**Guardrails**

- Always announce which task you are working on.
- Mark tasks complete immediately after finishing.
- Refuse to run `/opsx:sync`, `/opsx:archive`, or `/lsi:close` — these belong to production close on `main`.
- Pause on unclear requirements — do not guess.
