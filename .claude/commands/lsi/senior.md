---
description: Deep, light, or skip senior analysis after design.md
---

Run senior analysis tier selection for the active OpenSpec change after `design.md` exists and before bulk `/opsx:apply`.

**Canonical source:** [senior-analysis.md](../../docs/workflows/senior-analysis.md) · [`overlays/lsi/docs/workflows/openspec-git-integration.md` § Senior analysis](../../overlays/lsi/docs/workflows/openspec-git-integration.md#senior-analysis) · [senior-analysis-report.template.md](../../templates/senior-analysis-report.template.md)

**Input:** Optionally specify change slug or tier (`deep`, `light`, `skip`). If omitted, infer tier from change scope.

**Steps**

1. **Resolve change** — same as `/lsi:branch` (announce slug; ask if ambiguous).

2. **Verify branch** — must be ticket-linked branch, not `main` or `staging`. If wrong, stop with refuse Output.

3. **Confirm `design.md` exists**

   Read `openspec/changes/<slug>/proposal.md`, `design.md`, and `tasks.md`.

4. **Select tier**

   | Tier | When |
   |------|------|
   | **Deep** | Runtime-critical, integration-heavy, multi-capability, or **BREAKING** OpenSpec/workflow change — see integration doc tier signals. Prefer Deep (not Skip) for multi-capability lifecycle/workflow OpenSpec work. |
   | **Light** | ≤ ~3 `tasks.md` sections and low integration risk |
   | **Skip** | Truly trivial docs-only with no design risk — still prefer Light/Deep when the change alters lifecycle policy |

   If ambiguous, use **AskQuestion** with Deep / Light / Skip options.

5. **Run analysis (Deep or Light)**

   Emit the **full** report shape from [senior-analysis-report.template.md](../../templates/senior-analysis-report.template.md):

   - Executive summary; overall design verdict vocabulary: **Sound** / **Acceptable with follow-ups** / **Rethink**
   - Per-LC: Intent, Before/After, Alternatives, Unit verdict
   - Cross-cutting; open questions; relationship to code review
   - Logical units **LC-1, LC-2, …** align with numbered `tasks.md` sections
   - Test strategy: run / cite `TEST_COMMAND` from [PROJECT.md](../../PROJECT.md); rollback if BREAKING
   - **Do not** post full analysis to Bitbucket unless user explicitly asks

6. **Save locally (only if user asks)**

   Path: `.senior-analyses/YYYY-MM-DD-HHMM-<branch-slug>.md` (gitignored).

**Output**

Fill [senior-analysis-report.template.md](../../templates/senior-analysis-report.template.md) in chat (title through Relationship to code review). Required empty sections use `(none)` / `N/A` rather than omitting headings.

```
# Senior analysis — <branch> — <YYYY-MM-DD>

**Base:** <base>...HEAD
**Tier:** Deep | Light | Skip — <why>
**Overall verdict:** Sound | Acceptable with follow-ups | Rethink

## Executive summary
...

## Logical changes overview
| ID | Title | Files / area | Unit verdict |
|----|-------|--------------|--------------|
| LC-1 | ... | ... | ... |

## LC-1: <title>
...

## Relationship to code review
- Merge readiness is not this document’s verdict.
```

**Output (refuse)**

```
## Refuse: /lsi-senior

**Reason:** <wrong branch | missing design.md>
**Fix:** <one line>
```

**Guardrails**

- Skip tier: short Output with tier Skip and one paragraph pointing to code review at PR time — still use the title/verdict shell.
- Never commit `.senior-analyses/` files.
- Refuse on `main` or `staging`.
- MUST emit the template-shaped Output; MUST NOT invent alternate report shapes or append follow-up questions.
- No `Next:` footer (D11).
- Bot session exception: when nested under `/lsi:pr-bot-docs` (or another bot session), that invocation satisfies "user asks" for posting/saving the full report within that session's scope — see [integrations.md](../../docs/workflows/integrations.md) Bot sessions; standalone defaults unchanged.
