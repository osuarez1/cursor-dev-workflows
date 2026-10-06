---
description: Close gaps found during OpenSpec verification
---

Address implementation gaps, bugs, or missing acceptance criteria from `/opsx:verify`.

**Canonical source:** [openspec-git-integration.md](../../overlays/lsi/docs/workflows/openspec-git-integration.md) · [bot-lane.md](../bot-lane.md)

**Input:** Optionally specify change slug. Prefer the verify report just produced in chat.

**Steps**

1. **Resolve change** and verify ticket branch.
2. **Read** verify findings plus `proposal.md`, `design.md`, `tasks.md`.
3. **Fix** gaps so implementation aligns with those artifacts. Update `tasks.md` checkboxes only for work actually completed.
4. **Optional commit** — when user asks, run `/lsi:commit`. Do not auto-commit.

**Output**

```
## Address verify: <slug>

**Gaps closed:** N
**Gaps deferred:** N

### Changes
| File | Change | Verify requirement |
|------|--------|--------------------|
| ... | ... | ... |

### Deferred
- (none)
```

**Output (refuse)**

```
## Refuse: /lsi-address-verify

**Reason:** <wrong branch | no verify findings>
**Fix:** <one line>
```

**Guardrails**

- MUST emit the Output skeleton; MUST NOT invent alternate report shapes
- No `Next:` footer or follow-up steering (D11)
