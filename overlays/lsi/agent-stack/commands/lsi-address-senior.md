---
name: /lsi-address-senior
id: lsi-address-senior
category: Workflow
description: Address senior-analysis findings in OpenSpec docs only
---

Follow-up to `/lsi:senior`. Documentation-only changes under `openspec/`.

**Canonical source:** [senior-analysis.md](../../docs/workflows/senior-analysis.md) · [bot-lane.md](../bot-lane.md)

**Input:** Optionally specify change slug. Infer from branch / `openspec list` when omitted.

**Steps**

1. **Resolve change** — announce slug; refuse if ambiguous without AskQuestion.
2. **Verify branch** — ticket-linked branch only; not `main` or `staging`.
3. **Read** latest senior findings (chat or `.senior-analyses/` if user points to a file) plus `proposal.md`, `design.md`, `tasks.md`.
4. **Address** recommended design updates or caveats **only** in OpenSpec docs (`openspec/changes/<slug>/` and related delta specs). Do not implement application code or tick unrelated apply tasks as done.
5. **Optional commit** — when user asks, run `/lsi:commit` to map edits to logical Conventional Commits. Do not auto-commit.

**Output**

```
## Address senior: <slug>

**Scope:** openspec/ docs only
**Findings addressed:** N
**Findings deferred:** N

### Changes
| File | Edit | Senior finding |
|------|------|----------------|
| ... | ... | ... |

### Deferred
- (none)
```

**Output (refuse)**

```
## Refuse: /lsi-address-senior

**Reason:** <wrong branch | no findings | ambiguous slug>
**Fix:** <one line>
```

**Guardrails**

- OpenSpec documentation only — no `SOURCE_ROOT` / app edits
- MUST emit the Output skeleton; MUST NOT invent alternate report shapes
- No `Next:` footer or follow-up steering (D11)
- Do not auto-push or open PRs
