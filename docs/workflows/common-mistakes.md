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
| Bumping `VERSION` / `version.txt` or editing `CHANGELOG.md` on a feature PR | Leave version and changelog to `/lsi:release-train` on `main`; `/lsi:readiness` fails when those files change |
| Vague acceptance criteria (“works correctly”) | Testable checkboxes in [ticket-card-info.md](ticket-card-info.md) |

## Artifacts

| Mistake | Correct behavior |
|---------|------------------|
| Committing `.reviews/` or `.senior-analyses/` | Gitignore via adopt-managed `lsi:local-artifacts` block ([snippets/gitignore-local-artifacts.txt](../../snippets/gitignore-local-artifacts.txt)) |
| Creating `docs/reviews/` in the repo | Local archives only when user asks to save locally |
| Auto-posting review to Bitbucket/Trello | Only when user asks to log remotely, or via an explicit bot session ([integrations.md](integrations.md) Bot sessions) |
| Extending bot authorization beyond that PR/session | Bot scope is one PR (or one apply-bot change) for that invocation only |
| Calling `git push` / `git commit` directly inside a bot session | Use `.lsi/bin/lsi-bitbucket` only |
| Committing untracked files outside the step's snapshot | Commit gate stages only paths changed since the pre-step snapshot; never stage `.reviews/`, `.env*`, agent dirs |

## Ticket cards

| Mistake | Correct behavior |
|---------|------------------|
| Wrong task type (not in team’s allowed set) | Use team list; default: feature, bugfix, hotfix, chore, release |
| Title without `TITLE_PREFIX` or over 60 chars | `TITLE_PREFIX` + imperative title |
| Running `git ts` without user ask | Output copy-paste blocks only |
| Running `git-ts`, `which git-ts`, or probing for a hyphenated binary | Run **`git ts`** — local Git alias to `.git-trello/bin/git-trello`; verify with `git config --local --get alias.ts` |

## Pull requests

| Mistake | Correct behavior |
|---------|------------------|
| PR title `Fixed stuff` or vague body (“looks good”) | [pull-requests.md](pull-requests.md) — Conventional Commits title; runnable Testing steps — [examples/pr-description-good-vs-weak.md](../../examples/pr-description-good-vs-weak.md) |
| Merge extended description is only PR title or full PR markdown | [pull-requests.md](pull-requests.md) — Summary, `Changes:`, `Commits merged:`, `Post-merge:` — [examples/pr-merge-commit-good-vs-weak.md](../../examples/pr-merge-commit-good-vs-weak.md) |
| Confusing PR conventions with readiness checklist | Conventions → `pull-requests.md`; verdict checklist → `pr-production-readiness.md` |
| Skipping `/lsi:readiness` on Mode A or Mode C review | Run readiness for Mode A/B/C — nested in `/lsi:pr-bot-docs` (A) and `/lsi:pr-bot` (B/C) |
| Running `/lsi:close` on a ticket branch or before promote | Close only on **`main`** after the promotion PR merges |
| Running release-train (or version/changelog/release) off `main` | Those commands are **`main`-only**; never nest them in readiness/review/PR/promote/close |
| Putting close/promote/release/`/lsi:update` items in `tasks.md` | Keep checkboxes purpose-only; `/lsi:readiness` fails administrative apply tasks |
| Passing both a PR and `--local` to pr-bot / pr-bot-docs | Use `<PR>` for Bitbucket posting or `--local` for files+chat — not both |
| Expecting `--local` to push or post | Local mode never posts or pushes; use remote `<PR>` when you need Bitbucket |

## Routing

| Mistake | Correct behavior |
|---------|------------------|
| Deep security review labeled “senior analysis” only | Run [code-review.md](code-review.md) before merge |
| PR checklist instead of real review | Readiness + code review are complementary; [which-workflow.md](../../which-workflow.md) |

## Related

- [which-workflow.md](../../which-workflow.md)  
- [adoption-checklist.md](../../adoption-checklist.md)  
