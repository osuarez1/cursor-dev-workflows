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

3. **Gather context**

   Read:
   - `openspec/changes/<slug>/proposal.md`, `design.md`, `tasks.md`
   - Delta specs if present
   - `docs/contracts/` when payload or wire format touched
   - Feature: `git diff staging...HEAD` · Promotion: `git diff main...HEAD`

4. **Review focus areas (video-encoder worker)**

   | Area | When to check |
   |------|---------------|
   | FFmpeg / HLS | `ffmpeg_pipeline.py`, segment naming, encryption key consumption (no key generation) |
   | Redis queue | BLPOP/BRPOP, job payload parsing, error handling |
   | S3 / AWS CLI | `s3_manager.py` — `aws s3 sync` subprocess only; no boto3 bulk upload |
   | Contracts | Payload shape vs `docs/contracts/`; webhook callbacks |
   | Security | No secrets in repo; `tmp/` cleanup after job success/failure |
   | Version scope | No V2/V3 modules (`workflow_executor`, multi-queue) during V1 tasks |

5. **Structured findings**

   For each issue: **severity** (blocker / major / minor / nit), **location**, **recommendation**.

6. **Align with PR sections**

   Potential risks and Testing bullets must match what will appear in the PR body.

7. **Save locally (only if user asks)**

   Path: `.reviews/YYYY-MM-DD-HHMM-<branch-slug>.md` (gitignored).

**Output**

```
## Code Review: <slug>

**Recommendation:** <Approve | Approve with nits | Request changes>

### Blockers
- (none)

### Major
- ...

### Minor / Nits
- ...

### PR draft alignment
- **Potential risks:** ...
- **Testing:** ...

### Next
- Approve (feature) → `/lsi:pr` (when user asks to open PR)
- Approve (promotion) → push and open Bitbucket PR to **`main`** via `/lsi:promote` flow
- Request changes → fix and re-run `/lsi:readiness`
```

**Guardrails**

- Never post full review to Bitbucket unless user explicitly asks.
- Never commit `.reviews/` files.
