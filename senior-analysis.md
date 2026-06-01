# Senior analysis

Design-depth analysis **independent** of merge-gate [code-review.md](code-review.md). Any language or framework.

## Independence

| Aspect | Code review | Senior analysis |
|--------|-------------|-----------------|
| Purpose | Ship/no-ship, defects, test gaps | Understand approach, validate design |
| Output | Short, PR-friendly | Long, structured; may include mermaid |
| Remote log | Optional via integrations | Not by default (length) |
| Local archive | `.reviews/` | `.senior-analyses/` |
| Verdict | Ready / Needs fixes / Blocked | Sound / Acceptable with follow-ups / Rethink |

**Order:** senior analysis early on large features; code review before merge.

## Triggers

- senior analysis / analyze approach / design alternatives
- logical change analysis / before and after review
- compare implementation options / design tradeoffs

**Not** senior analysis (use code-review instead):

- code review / review branch / prepare for PR / draft PR summary

## Context gathering

```bash
git diff BASE_BRANCH...HEAD
git log BASE_BRANCH..HEAD --oneline
```

Read changed paths, callers, downstream consumers, schema/config, jobs, public APIs.

## Analysis tiers

State tier and why.

| Mode | When | Depth |
|------|------|--------|
| **Deep** | Large feature/refactor touching application source | Full template; all logical units; diagrams for non-trivial flows |
| **Light** | Small change, ≤ ~3 logical units | Shorter alternatives; diagram optional |
| **Skip** | Docs/config only, no behavioral change | One paragraph + pointer to code review |

## Logical units

Split branch into **LC-1**, **LC-2**, … (not necessarily one per commit).

**Heuristics:**

- One unit per behavioral change (API, state machine, payment path, auth rule)
- Batch inseparable refactors with the behavior they support
- Docs-only: one unit per subsystem if helpful

## Per-unit checklist

Every `LC-n` must include:

### A. Intent and scope

- Problem solved; explicit **out of scope**

### B. Before / after

| Dimension | Before (base) | After (branch) |
|-----------|---------------|----------------|
| Behavior | | |
| Data shape | | |
| Failure modes | | |

**Delta:** user-visible or integration changes

### C. Flow (optional mermaid)

- `flowchart` or `sequenceDiagram`; camelCase node IDs; no spaces in node IDs
- **N/A — trivial** when diagram adds no value

### D. Alternatives

- At least **two** options (include “do nothing” or “extend existing X”)
- Pros/cons table; **recommendation** for this codebase

### E. Logical correctness

- Invariants; nil/empty; authz; idempotency; concurrency; timezones
- Failure and rollback: partial writes, retries, duplicate webhooks/events

### F. Cross-cutting impact

- Schema, cache, search index, jobs, external integrations

### G. Unit verdict

`Sound` | `Acceptable with follow-ups` | `Rethink`

## Global sections

- Cross-unit interactions (ordering, flags, deploy sequence)
- Open questions
- Suggested follow-ups (feeds code review; not duplicate full security pass)
- **Overall design verdict** (1–2 sentences)

## Senior analysis checklist

- [ ] Base range identified  
- [ ] Tier stated  
- [ ] Logical units enumerated  
- [ ] Each unit: intent, before/after, delta, diagram or N/A  
- [ ] Each unit: ≥2 alternatives, recommendation  
- [ ] Cross-unit interactions  
- [ ] Open questions  
- [ ] Overall design verdict  
- [ ] Code review recommended when application source changed  

## Output format

Follow [templates/senior-analysis-report.template.md](templates/senior-analysis-report.template.md).

Use code citations when referencing implementation.

**Cursor Canvas:** optional for large comparison tables; not required every run.

## Local archive

Only when user asks to **save senior analysis locally**:

```text
.senior-analyses/YYYY-MM-DD-HHMM-<branch-slug>.md
```

Gitignore via [snippets/gitignore-local-artifacts.txt](snippets/gitignore-local-artifacts.txt). Never commit `docs/analyses/`.

## Remote posting

Do not post full reports to PR comments by default. Short executive summary only when user asks — [integrations.md](integrations.md).

## Examples

- [examples/senior-analysis-good-vs-weak.md](examples/senior-analysis-good-vs-weak.md)

## Related

- [code-review.md](code-review.md)  
- [which-workflow.md](which-workflow.md)  
- [common-mistakes.md](common-mistakes.md)  
