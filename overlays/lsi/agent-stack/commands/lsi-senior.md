---
name: /lsi-senior
id: lsi-senior
category: Workflow
description: Deep, light, or skip senior analysis after design.md
---

Run senior analysis tier selection for the active OpenSpec change after `design.md` exists and before bulk `/opsx:apply`.

**Canonical source:** [senior-analysis.md](../../docs/workflows/senior-analysis.md) · [`docs/workflows/openspec-git-integration.md` § Senior analysis](../../docs/workflows/openspec-git-integration.md#senior-analysis)

**Input:** Optionally specify change slug or tier (`deep`, `light`, `skip`). If omitted, infer tier from change scope.

**Steps**

1. **Resolve change** — same as `/lsi:branch` (announce slug; ask if ambiguous).

2. **Verify branch** — must be ticket-linked branch, not `main` or `staging`. If wrong, stop and suggest `/lsi:card` or `/lsi:branch`.

3. **Confirm `design.md` exists**

   Read `openspec/changes/<slug>/proposal.md`, `design.md`, and `tasks.md`.

4. **Select tier**

   | Tier | When |
   |------|------|
   | **Deep** | Runtime-critical, integration-heavy, or multi-capability change — see integration doc for this repo's tier signals |
   | **Light** | ≤ ~3 `tasks.md` sections |
   | **Skip** | Docs/openspec-only; point to `/lsi:review` instead |

   If ambiguous, use **AskQuestion tool** with Deep / Light / Skip options.

5. **Run analysis (Deep or Light)**

   - Logical units **LC-1, LC-2, …** align with numbered `tasks.md` sections.
   - Inputs: Why / What Changes, `design.md` decisions, capabilities from `proposal.md`.
   - Cover: architecture fit, risks, test strategy (run the test command from [PROJECT.md](../../PROJECT.md)), rollback if BREAKING.
   - **Do not** post full analysis to Bitbucket unless user explicitly asks.

6. **Save locally (only if user asks)**

   Path: `.senior-analyses/YYYY-MM-DD-HHMM-<branch-slug>.md` (gitignored).

**Output**

```
## Senior Analysis: <slug> (tier: <Deep|Light|Skip>)

### LC-1: <tasks.md section title>
<findings>

### Summary
- **Proceed?** <yes with caveats | recommend design update>
- **Next:** `/opsx:apply` or update `design.md` if blockers found
```

**Guardrails**

- Skip tier: output one paragraph pointing to code review at PR time.
- Never commit `.senior-analyses/` files.
- Refuse on `main` or `staging`.
