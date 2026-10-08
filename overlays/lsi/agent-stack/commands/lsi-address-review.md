---
name: /lsi-address-review
id: lsi-address-review
category: Workflow
description: Address code-review findings at every severity
---

Follow-up to `/lsi:review`. Resolves structured findings (blocker / major / minor / nit).

**Canonical source:** [code-review.md](../../docs/workflows/code-review.md) · [bot-lane.md](../bot-lane.md)

**Input:** Optionally specify change slug. Prefer the review just produced in chat.

**Steps**

1. **Resolve change** and verify ticket branch (not `main`/`staging`).
2. **Read** structured findings from the latest `/lsi:review` output (or user-supplied `.reviews/` path).
3. **Address** each finding per severity and recommendation at the stated location. Prefer smallest fix that closes the gap.
4. **Optional commit** — when user asks, run `/lsi:commit`. Do not auto-commit.

**Output**

```
## Address review: <slug>

**Findings addressed:** N
**Findings deferred/rejected:** N

### Changes
| Severity | Location | Fix | Recommendation addressed |
|----------|----------|-----|--------------------------|
| ... | ... | ... | ... |

### Deferred / rejected
- (none)
```

**Output (refuse)**

```
## Refuse: /lsi-address-review

**Reason:** <wrong branch | no review findings>
**Fix:** <one line>
```

**Guardrails**

- MUST emit the Output skeleton; MUST NOT invent alternate report shapes
- No `Next:` footer or follow-up steering (D11)
- Do not draft PR title/body — `/lsi:pr` owns that
- Bot session exception: when nested under `/lsi:pr-bot` / `/lsi:apply-bot` with `--fix`/apply, that invocation satisfies "user asks" for commit/push within that session's scope — see [integrations.md](../../docs/workflows/integrations.md) Bot sessions; standalone defaults unchanged.
