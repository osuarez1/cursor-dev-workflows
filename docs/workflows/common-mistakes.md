# Common agent mistakes

Anti-patterns to avoid when using [cursor-dev-workflows](../../README.md) in a target repository.

## Git and commits

| Mistake | Correct behavior |
|---------|------------------|
| Running `git commit` without the user asking | Only commit when explicitly requested; see [commits-logical-order.md](commits-logical-order.md) |
| One commit mixing feature + refactor + unrelated fix | One logical change per commit; output a commit plan first |
| Subject `fix stuff` or `feat: updates` | Conventional Commits: `type(scope): imperative subject`, optional body — see [examples/commit-messages-good-vs-weak.md](../../examples/commit-messages-good-vs-weak.md) |
| Past tense or period on subject (`Added reports.`) | Imperative, no trailing period — [commits-logical-order.md](commits-logical-order.md) |
| `git commit --amend` after failed hook or pushed commit | New commit or user-directed amend only; see commit doc |
| `--no-verify` unless user asks | Never skip hooks by default |

## Branches

| Mistake | Correct behavior |
|---------|------------------|
| Editing on `main` / `master` / `staging` | Refuse; [branch-workflow.md](branch-workflow.md) |
| Starting implementation without a ticket branch | Card/branch first when team requires it |
| `git push -u origin HEAD` when hooks need literal branch name | `git push -u origin "$(git branch --show-current)"` if documented |

## Workflows

| Mistake | Correct behavior |
|---------|------------------|
| Using code review verdict `Ready` in senior analysis | Senior analysis: `Sound` / `Acceptable with follow-ups` / `Rethink` |
| Posting full senior analysis to PR comments | Short summary only unless asked; see [integrations.md](integrations.md) |
| Skipping tests for `SOURCE_ROOT` changes | [test-requirements.md](test-requirements.md) |
| Vague acceptance criteria (“works correctly”) | Testable checkboxes in [ticket-card-info.md](ticket-card-info.md) |

## Artifacts

| Mistake | Correct behavior |
|---------|------------------|
| Committing `.reviews/` or `.senior-analyses/` | Gitignore via [snippets/gitignore-local-artifacts.txt](../../snippets/gitignore-local-artifacts.txt) |
| Creating `docs/reviews/` in the repo | Local archives only when user asks to save locally |
| Auto-posting review to Bitbucket/Trello | Only when user asks to log remotely |

## Ticket cards

| Mistake | Correct behavior |
|---------|------------------|
| Wrong task type (not in team’s allowed set) | Use team list; default: feature, bugfix, hotfix, chore, release |
| Title without `TITLE_PREFIX` or over 60 chars | `TITLE_PREFIX` + imperative title |
| Running `git ts` without user ask | Output copy-paste blocks only |

## Pull requests

| Mistake | Correct behavior |
|---------|------------------|
| PR title `Fixed stuff` or vague body (“looks good”) | [pull-requests.md](pull-requests.md) — Conventional Commits title; runnable Testing steps — [examples/pr-description-good-vs-weak.md](../../examples/pr-description-good-vs-weak.md) |
| Merge extended description is only PR title or full PR markdown | [pull-requests.md](pull-requests.md) — Summary, `Changes:`, `Commits merged:`, `Post-merge:` — [examples/pr-merge-commit-good-vs-weak.md](../../examples/pr-merge-commit-good-vs-weak.md) |
| Confusing PR conventions with readiness checklist | Conventions → `pull-requests.md`; verdict checklist → `pr-production-readiness.md` |

## Routing

| Mistake | Correct behavior |
|---------|------------------|
| Deep security review labeled “senior analysis” only | Run [code-review.md](code-review.md) before merge |
| PR checklist instead of real review | Readiness + code review are complementary; [which-workflow.md](../../which-workflow.md) |

## Related

- [which-workflow.md](../../which-workflow.md)  
- [adoption-checklist.md](../../adoption-checklist.md)  
