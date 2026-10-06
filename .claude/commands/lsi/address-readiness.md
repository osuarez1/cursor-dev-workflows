---
description: Clear PR readiness gate after Needs fixes or Blocked
---

Follow-up to `/lsi:readiness` when verdict is `Needs fixes` or `Blocked`.

**Canonical source:** [pr-production-readiness.md](../../docs/workflows/pr-production-readiness.md) · [bot-lane.md](../bot-lane.md)

**Input:** Optionally specify change slug. Prefer the readiness report just produced in chat.

**Steps**

1. **Resolve change** and verify ticket branch (feature mode) or allowed promotion branch.
2. **Read** readiness Issues table (branch, ticket, Trello id, tests, secrets).
3. **Fix** local CI / `TEST_COMMAND` failures, branch validation, ticket match, and secret-scan alerts. Re-run the test gate from PROJECT.md before claiming ready.
4. **Optional commit** — when user asks, run `/lsi:commit`. Do not auto-commit.
5. **Do not** draft PR title/body — `/lsi:pr` owns that.

**Output**

```
## Address readiness: <slug>

**Prior verdict:** Needs fixes | Blocked
**Fixes applied:** N

### Changes
| Check | Fix | Status |
|-------|-----|--------|
| ... | ... | ✓ |

### Remaining
- (none)
```

**Output (refuse)**

```
## Refuse: /lsi-address-readiness

**Reason:** <wrong branch | already Ready | no issues>
**Fix:** <one line>
```

**Guardrails**

- MUST emit the Output skeleton; MUST NOT invent alternate report shapes
- No `Next:` footer or follow-up steering (D11)
- Never emit a PR title or body draft
