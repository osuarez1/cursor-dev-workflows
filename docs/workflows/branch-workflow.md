# Branch workflow

Rules for **humans and coding agents** before and during feature work. Customize `PROTECTED_BRANCHES`, `TICKET_ID_PATTERN`, and `BRANCH_PATTERN` per project (see [README.md](../../README.md)).

## Protected branches

**Never start task implementation** (edits, migrations, feature commits) while checked out on a protected integration branch.

Default `PROTECTED_BRANCHES`:

- `main`
- `master`
- `staging`

Verify with:

```bash
git branch --show-current
```

If the current branch is protected, **stop** — do not write code, run task migrations, or continue as if that branch were acceptable.

### Agent refusal template

When you must refuse:

1. State that protected branches are off-limits for task work in **any** Cursor mode (Plan, Agent, Ask).
2. Tell the user to create or check out a ticket-linked branch per team process.
3. Point to [ticket-card-info.md](ticket-card-info.md) if they need card fields first.
4. Point to [adoption-checklist.md](../../adoption-checklist.md) for tooling setup.

## Ticket-linked branches

When the team enforces ticket ids in branch names:

| Setting | Example |
|---------|---------|
| `TICKET_ID_PATTERN` | 24-character id, or `PROJ-123` |
| `BRANCH_PATTERN` | `feature/<id>-short-slug` |

Agents should:

- Confirm the branch name embeds the ticket id before substantive work.
- Not invent ticket ids; ask the user to create/link a card in `TICKET_TOOL`.

Optional Trello/git-trello setup and LSI slash commands (`/lsi:card`, `/lsi:card-link`, `/lsi:trello-list`, `/lsi:trello-branch`): [integrations.md](integrations.md). LSI adopters: [git-trello.md](sdlc/git-trello.md).

## Before you branch

1. Draft or locate the ticket — [ticket-card-info.md](ticket-card-info.md) (or Jira/Linear equivalent).
2. Create the branch from `BASE_BRANCH` using team naming.
3. Push with explicit branch name if hooks require it (some tools reject `git push origin HEAD`).

## Relationship to other workflows

| Workflow | Role |
|----------|------|
| [ticket-card-info.md](ticket-card-info.md) | Card fields before `git ts` / branch creation |
| [commits-logical-order.md](commits-logical-order.md) | Commits only on feature branch; only when user asks |
| [pr-production-readiness.md](pr-production-readiness.md) | Merge/rebase `BASE_BRANCH` before PR |

## Customize for your repo

- List exact protected branch names (including `release/*` if applicable).
- Document required hooks (pre-push, commit-msg footers).
- Link internal runbook for hotfix branches if `hotfix/` bypasses normal flow.

## Related

- [which-workflow.md](../../which-workflow.md)  
- [common-mistakes.md](common-mistakes.md) — implementing on `main`  
