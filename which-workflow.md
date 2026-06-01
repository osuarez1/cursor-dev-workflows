# Which workflow?

Use this routing guide when the user’s request could match more than one document.

## Decision table

| User says (examples) | Use | Output / verdict |
|----------------------|-----|------------------|
| draft ticket card, `git ts`, task type/title/description | [ticket-card-info.md](docs/workflows/ticket-card-info.md) | Three copy-paste blocks |
| create branch, wrong branch, on main | [branch-workflow.md](docs/workflows/branch-workflow.md) | Refuse or redirect to ticket branch |
| draft PR title, PR description, PR copy | [pull-requests.md](docs/workflows/pull-requests.md) | Title + markdown body (Overview, Changes, Potential risks, Testing, Related) |
| PR merge info, merge commit, extended description | [pull-requests.md](docs/workflows/pull-requests.md) | Default `Merge pull request #…` subject + extended description (Summary, Changes, Commits merged, Post-merge) |
| ready for PR, production ready, ship checklist | [pr-production-readiness.md](docs/workflows/pr-production-readiness.md) | Checklist + `Ready` \| `Needs fixes` \| `Blocked` |
| code review, review branch, review locally | [code-review.md](docs/workflows/code-review.md) | Summary, Critical, Suggestions, Tests; verdict `Ready` \| `Needs fixes` \| `Blocked` |
| senior analysis, design alternatives, before/after, LC-1 | [senior-analysis.md](docs/workflows/senior-analysis.md) | Full report; verdict `Sound` \| `Acceptable with follow-ups` \| `Rethink` |
| commit plan, logical commits, commit message | [commits-logical-order.md](docs/workflows/commits-logical-order.md) | Ordered commit plan; **commit only if asked** |
| when are tests required | [test-requirements.md](docs/workflows/test-requirements.md) | Policy + exemption wording |
| log review to PR host or ticket tool | [integrations.md](docs/workflows/integrations.md) | Optional adapters |
| what did the agent do wrong | [common-mistakes.md](docs/workflows/common-mistakes.md) | Anti-patterns |

## Overlap rules

1. **PR conventions vs readiness vs code review** — [pull-requests.md](docs/workflows/pull-requests.md) defines title/body format and merge-commit extended description. [pr-production-readiness.md](docs/workflows/pr-production-readiness.md) is the readiness checklist and verdict. [code-review.md](docs/workflows/code-review.md) walks logic, security, performance, and tests in depth. Run readiness before opening a PR; run code review before merge.
2. **Senior analysis vs code review** — Senior analysis explains design and alternatives; it does **not** replace security/performance/test gates. Use different verdict words (never `Ready` for senior analysis).
3. **Ticket card vs implementation** — Card drafting does not authorize coding on a protected branch. Branch + ticket first, then Agent mode work.
4. **Commit plan vs commit execution** — Always show a plan before the first commit on a branch when multiple logical changes exist. Run `git commit` only when the user explicitly asks.

## Flowchart

```mermaid
flowchart TD
  start[User request]
  start --> ticket{Draft ticket or card?}
  ticket -->|yes| ticketInfo[ticket-card-info.md]
  ticket -->|no| branch{On protected branch or no ticket?}
  branch -->|yes| bw[branch-workflow.md]
  branch -->|no| intent{Primary intent?}
  intent -->|design or alternatives| sa[senior-analysis.md]
  intent -->|review code| cr[code-review.md]
  intent -->|draft PR title or body| prConv[pull-requests.md]
  intent -->|PR merge info| prMerge[pull-requests.md merge commit]
  intent -->|PR or production ready| pr[pr-production-readiness.md]
  intent -->|commits| co[commits-logical-order.md]
  intent -->|unclear| ask[Ask one focused question then route]
```

## Recommended order (large feature)

1. [ticket-card-info.md](docs/workflows/ticket-card-info.md) — card fields  
2. [branch-workflow.md](docs/workflows/branch-workflow.md) — ticket-linked branch  
3. Implementation (Agent mode)  
4. [senior-analysis.md](docs/workflows/senior-analysis.md) — early, if design is non-trivial  
5. [test-requirements.md](docs/workflows/test-requirements.md) — while coding  
6. [commits-logical-order.md](docs/workflows/commits-logical-order.md) — plan, then commit when asked  
7. [pull-requests.md](docs/workflows/pull-requests.md) — title and description when opening PR  
8. [pr-production-readiness.md](docs/workflows/pr-production-readiness.md) — readiness before opening PR  
9. [code-review.md](docs/workflows/code-review.md) — before merge  
10. [pull-requests.md](docs/workflows/pull-requests.md) — merge extended description when using merge commits on `PR_HOST`  

## Related

- [README.md](README.md) — placeholders and adoption  
- [common-mistakes.md](docs/workflows/common-mistakes.md) — confusing workflows  
