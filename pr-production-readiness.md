# PR and production readiness

Checklist for **“ready to open a PR?”** and **“ready to merge to production?”** Customize `BASE_BRANCH`, `TEST_COMMAND`, `PR_HOST` (see [README.md](README.md)).

For deep review, use [code-review.md](code-review.md). For routing, [which-workflow.md](which-workflow.md).

## Triggers

- prepare for PR, draft PR, PR description
- production ready, merge readiness, ship checklist
- ready for `BASE_BRANCH` / staging / production

## Before you branch

If work has not started on a ticket-linked branch, stop and follow [branch-workflow.md](branch-workflow.md) and [ticket-card-info.md](ticket-card-info.md).

## Context gathering

```bash
git branch --show-current
git diff BASE_BRANCH...HEAD
git log BASE_BRANCH..HEAD --oneline
```

Confirm ticket id in branch name when `TICKET_ID_PATTERN` is enforced.

## Two modes

### PR readiness

Branch hygiene, reviewable scope, tests/lint, secrets scan, PR title/body, reviewer test steps.

### Production readiness

Everything in PR readiness, plus:

- Deploy/migration risk and rollback plan
- Feature flags or config toggles
- Target branch policy (`BASE_BRANCH` vs release branch)
- Monitoring/alerts if applicable

## Checklist (agent output)

Use markdown checkboxes; adapt to project.

### Branch and ticket

- [ ] Not on `PROTECTED_BRANCHES`
- [ ] Branch matches `BRANCH_PATTERN` and `TICKET_ID_PATTERN` (if required)
- [ ] `BASE_BRANCH` merged or rebased into branch (diff current)

### Scope

- [ ] PR is reviewable size; large diffs called out in Overview
- [ ] No unrelated drive-by changes

### Quality gates

- [ ] `TEST_COMMAND` passes (or exemption documented per [test-requirements.md](test-requirements.md))
- [ ] `LINT_COMMAND` passes (if project uses it)
- [ ] No secrets or credentials in diff

### Data and deploy

- [ ] Migrations/schema changes documented with rollback notes
- [ ] Config/env changes listed for operators

### PR metadata

- [ ] Title: Conventional Commits style (`type(scope): description`)
- [ ] Body sections: Overview, Changes, Potential risks, Testing, Related
- [ ] Template: [templates/pr-description.template.md](templates/pr-description.template.md)

## Readiness verdict

End with one of:

- **Ready** — safe to open PR or merge given stated assumptions
- **Needs fixes** — addressable issues before PR/merge
- **Blocked** — must not merge until resolved

Same semantics as [code-review.md](code-review.md); readiness is a checklist shorthand, not a substitute for full review.

## PR prep shorthand

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

Map to full PR template: *What changed* → Changes; *Why* → Overview; *Testing* → Testing.

## Customize for your repo

- `PR_HOST` checklist items (required CI checks)
- Link to CONTRIBUTING or deploy runbook
- Staging vs production branch names

## Related

- [code-review.md](code-review.md)  
- [test-requirements.md](test-requirements.md)  
- [commits-logical-order.md](commits-logical-order.md)  
