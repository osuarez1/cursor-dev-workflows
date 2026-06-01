# Code review and PR preparation

Merge-gate review for any stack. Customize `BASE_BRANCH`, `SOURCE_ROOT`, `TEST_COMMAND` (see [README.md](../../README.md)).

**Not** [senior-analysis.md](senior-analysis.md) — use that for design depth and alternatives.

## Triggers

**Standard review** (may log remotely when asked):

- review branch / review code / code review
- prepare for PR / draft PR summary

**Local review** (never post remotely unless user later asks):

- local code review / review locally / private review (don't log)

For local review: same checklists; optional save to `.reviews/` only when user asks.

## Context gathering

```bash
git diff BASE_BRANCH...HEAD
git log BASE_BRANCH..HEAD --oneline
```

Read changed files under `SOURCE_ROOT`, tests, migrations/schema, config.

## Review checklists

Report findings with file/line references when possible.

### Logic and edge cases

Nil/empty handling, authorization, state transitions, error paths, races, off-by-one, timezone/date edges.

### Performance

- N+1 queries or equivalent (batch loading, eager fetch)
- Memory: streaming vs loading entire datasets; pagination
- Indexes on filtered/sorted/joined columns (when applicable)

### Security

- Injection (SQL, command, template, HTML)
- Authentication and authorization on changed paths
- XSS or unsafe HTML rendering
- Secrets in code or logs; dependency vulnerabilities if visible in diff

### Tests

Follow [test-requirements.md](test-requirements.md). Note missing regression tests for bugfixes. Cite `TEST_COMMAND` to run.

### Conventions

DRY, clear naming, appropriate layer boundaries (controller/handler vs service vs domain). Match surrounding file style.

### Stack / project constraints

Link to project stack doc (version limits, banned patterns, framework rules).

### Repo-specific focus (customize)

| Area | What to check |
|------|----------------|
| Auth | Roles, permissions, session/token handling |
| API | Input validation, versioning, error contracts |
| Payments | Idempotency, webhooks, reconciliation |
| Background jobs | Retries, duplicates, dead letters |
| Search / cache | Invalidation, stale reads |
| i18n | Locale fallbacks when strings or formats change |
| Frontend | Scope to changed components; bundle impact |

## Review output format

```markdown
## Summary
<1–2 sentences: overall readiness>

## Critical issues
<must-fix before merge>

## Suggestions
<performance, style, optional improvements>

## Test coverage
<what exists, what is missing, commands to run>
```

Use code citations (`startLine:endLine:path`) when referencing specific lines.

**Verdict:** `Ready` | `Needs fixes` | `Blocked`

## PR summary (review prep)

```markdown
## What changed
- <bullet>

## Why it changed
<motivation; ticket link>

## Potential risks
- <regression, deploy>

## Testing instructions
1. TEST_COMMAND
2. <manual steps>
```

PR title and body conventions: [pull-requests.md](pull-requests.md). Template: [templates/pr-description.template.md](../../templates/pr-description.template.md). Readiness: [pr-production-readiness.md](pr-production-readiness.md).

## Pre-PR hygiene

```bash
git branch --show-current
# merge/rebase BASE_BRANCH
TEST_COMMAND
LINT_COMMAND   # if used
git push -u origin "$(git branch --show-current)"   # when hooks require explicit branch name
```

## Record the review (remote) — optional

Only when user asks to **log** or **record**:

Emit a log-ready block in a separate `text` fenced code block:

```text
**Code review — YYYY-MM-DD HH:MM (local)**
**Base:** BASE_BRANCH...HEAD (<N> commits)
**Verdict:** Ready | Needs fixes | Blocked

**Summary**
...

**Critical issues**
- ...

**Suggestions**
- ...

**Test coverage**
- ...
```

See [integrations.md](integrations.md) for PR/ticket posting tools.

## Local review archive

Only when user asks to **save locally**:

```text
.reviews/YYYY-MM-DD-HHMM-<branch-slug>.md
```

- Create `.reviews/` if missing; gitignore via [snippets/gitignore-local-artifacts.txt](../../snippets/gitignore-local-artifacts.txt)
- Sanitize slug: lowercase, `/` → `-`, truncate if long
- **Never** commit `.reviews/` or create `docs/reviews/` in the repo

## Examples

- [examples/code-review-good-vs-weak.md](../../examples/code-review-good-vs-weak.md)
- Template: [templates/code-review-output.template.md](../../templates/code-review-output.template.md)

## Related

- [pull-requests.md](pull-requests.md)  
- [senior-analysis.md](senior-analysis.md)  
- [which-workflow.md](../../which-workflow.md)  
- [common-mistakes.md](common-mistakes.md)  
