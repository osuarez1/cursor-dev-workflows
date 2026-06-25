---
name: /opsx-verify
id: opsx-verify
category: Workflow
description: Verify current change implementation matches spec and tasks
---

Verify that the current change's implementation matches its OpenSpec artifacts: proposal scope, design decisions, and tasks checklist.

**Canonical source:** [`docs/workflows/openspec-git-integration.md`](../../docs/workflows/openspec-git-integration.md)

**Input:** Optional change slug. If omitted, resolve from branch or `openspec list --json`.

**Steps**

1. **Resolve change** — announce slug.

2. **Read artifacts**

   Read: `openspec/changes/<slug>/proposal.md`, `design.md`, `tasks.md`.

3. **Check task completion**

   ```bash
   openspec instructions apply --change "<slug>" --json
   ```

   Report: N/M tasks complete, list unchecked tasks.

4. **Diff review**

   ```bash
   git diff staging...HEAD --stat
   ```

   Confirm staged changes align with proposal scope and design decisions.

5. **Flag discrepancies**

   - Tasks marked complete but no matching diff → flag.
   - Diff touches areas not covered by tasks → flag.
   - Design decisions overridden without task → flag.

6. **Verdict**

   - **Aligned** — implementation matches spec.
   - **Partial** — N tasks remaining; list them.
   - **Discrepancy** — list mismatches; suggest corrective action.

**Output**

```
## Verify: <slug>

**Tasks:** N/M complete
**Diff scope:** <aligned|out of scope>
**Verdict:** <Aligned|Partial|Discrepancy>

### Remaining tasks
- [ ] ...

### Discrepancies (if any)
- ...

Next: /lsi:readiness when all tasks are complete.
```

**Guardrails**

- Do not mark tasks complete during verify — use `/opsx:apply` or `/opsx:continue`.
- Report discrepancies as warnings, not errors, unless they are blockers for PR.
