# Branch reviewability

Hard and soft limits for PR size. Values come from [PROJECT.md](../../PROJECT.md).

## Limits

| Token | Role |
|-------|------|
| `PR_WARN_FILES` | Soft warning — consider splitting |
| `PR_MAX_FILES` | Hard block — must split |
| `PR_WARN_LINES` | Soft warning (changed lines) |
| `PR_MAX_LINES` | Hard block |
| `PR_MAX_COMMITS` | Hard block |
| `PR_MAX_PRIMARY_CONCERNS` | One primary concern per PR |
| `PR_MAX_SCOPES` | Conventional-commit scope count guidance |

## When over limits

1. **Stop** — do not open the PR as-is.
2. Propose a **split plan** — each slice gets its own Trello card and ticket branch.
3. Per slice: from **`main`** or **`staging`**, run **`/lsi:card`** or **`/lsi:trello-list`** (OpenSpec required for trello flows); if work already exists on a branch without a Trello id, run **`/lsi:card-link`** on that branch (OpenSpec required).
4. One OpenSpec change folder = one PR when possible.

## OpenSpec at propose

- Epic + slice changes at `/opsx:propose` time when work is large.
- `/opsx:apply` respects the same file/line limits — split before implementation if needed.

## Related

- [pull-requests.md](pull-requests.md)
- [pr-production-readiness.md](pr-production-readiness.md)
- [openspec-git-integration.md](openspec-git-integration.md)
