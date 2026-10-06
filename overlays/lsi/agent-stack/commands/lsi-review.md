---
name: /lsi-review
id: lsi-review
category: Workflow
description: Pre-merge code review checklist for active change
---

Run code review for the active OpenSpec change after readiness passes and before opening a PR.

**Canonical source:** [code-review.md](../../docs/workflows/code-review.md) · [`docs/workflows/openspec-git-integration.md` § Code review](../../docs/workflows/openspec-git-integration.md#code-review)

**Input:** Optionally specify change slug. Use **promotion mode** when invoked from `/lsi:promote` or when the PR target is **`main`**.

**Prerequisite:** `/lsi:readiness` verdict must be `Ready` (or user explicitly skips with documented reason).

**Modes**

| Mode | When | Diff base | Branch |
|------|------|-----------|--------|
| **Feature** (default) | `/lsi:pr`, first PR | `staging` | Ticket branch only; refuse `main` or `staging` |
| **Promotion** | `/lsi:promote`, production PR | `main` (`BASE_BRANCH`) | Ticket branch or **`staging`**; refuse `main` |

**Steps**

1. **Resolve change** — announce slug and mode (feature or promotion).

2. **Verify branch** — feature: ticket-linked branch only; promotion: ticket branch or **`staging`**; never `main`.

3. **Prowler auto-chain (when applicable)**

   If an open Bitbucket PR exists for this branch and a comment body starts with `Prowler · Grok Bot review`, invoke `/lsi:address-prowler` first (same PR), then continue this review. Skip when no PR or no matching comment. Standalone `/lsi:address-prowler` remains available. No `Next:` footer after either path.

4. **Gather context**

   Read:
   - `openspec/changes/<slug>/proposal.md`, `design.md`, `tasks.md`
   - Delta specs if present
   - `docs/contracts/` when payload or wire format touched
   - Feature: `git diff staging...HEAD` · Promotion: `git diff main...HEAD`

5. **Review focus areas**

   Refer to [`docs/workflows/openspec-git-integration.md` § Code review](../../docs/workflows/openspec-git-integration.md#code-review) for this repo's specific focus areas (domain components, security, version scope, etc.). Do **not** embed adopter-specific domain tables in this shared command.

6. **Structured findings**

   For each issue: **severity** (blocker / major / minor / nit), **location**, **recommendation**.

7. **Align with PR sections**

   Potential risks and Testing bullets must match what will appear in the PR body. Do **not** draft the PR title or body here — `/lsi:pr` owns that.

8. **Save locally (only if user asks)**

   Path: `.reviews/YYYY-MM-DD-HHMM-<branch-slug>.md` (gitignored).

**Output**

```
## Code Review: <slug>

**Recommendation:** <Approve | Approve with nits | Request changes>
**Prowler:** skipped | addressed (see Address Prowler output above)

### Blockers
- (none)

### Major
- (none)

### Minor / Nits
- (none)

### PR draft alignment
- **Potential risks:** ...
- **Testing:** ...
```

**Output (refuse)**

```
## Refuse: /lsi-review

**Reason:** <wrong branch | readiness not Ready>
**Fix:** <one line>
```

**Guardrails**

- Never post full review to Bitbucket unless user explicitly asks.
- Never commit `.reviews/` files.
- Never draft PR title/body — name `/lsi:pr` instead.
- MUST emit the Output skeleton; MUST NOT invent alternate report shapes or append follow-up questions.
- No `Next:` footer (D11).
