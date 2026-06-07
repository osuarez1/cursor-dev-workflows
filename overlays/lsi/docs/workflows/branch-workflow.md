# Branch workflow

Rules for **humans and coding agents** before and during feature work. Resolved values: [PROJECT.md](../../PROJECT.md).

## Protected branches

**Never start task implementation** (edits, migrations, feature commits) while checked out on a protected integration branch.

This repo's `PROTECTED_BRANCHES`:

{{PROTECTED_BRANCHES_BULLETS}}

Verify with:

```bash
git branch --show-current
```

If the current branch is protected, **stop** — do not write code, run task migrations, or continue as if that branch were acceptable.

**Exception:** **`/lsi:card`** on **`main` only** — creates Trello card + branch via `git ts`; no source edits. **Refuse on other protected branches.** See [openspec-git-integration.md](openspec-git-integration.md).

### Agent refusal template

When you must refuse:

1. State that protected branches are off-limits for task work in **any** Cursor mode (Plan, Agent, Ask).
2. Show [stop-sign image](https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Stop_sign_MUTCD.svg/240px-Stop_sign_MUTCD.svg.png) and **🛑**.
3. Tell the user to create or check out a ticket-linked branch: `git ts`, `git tl`, `git tb`.
4. Point to [ticket-card-info.md](ticket-card-info.md) if they need card fields first.
5. Point to [sdlc/git-trello.md](sdlc/git-trello.md) for branch/Trello tooling setup.

## Ticket-linked branches

When the team enforces ticket ids in branch names:

| Setting | Example |
|---------|---------|
| `TICKET_ID_PATTERN` | 24-character Trello card id |
| `BRANCH_PATTERN` | `feature\|bugfix\|hotfix\|chore/{id}-short-slug` |

Agents should:

- Confirm the branch name embeds the ticket id before substantive work.
- Not invent ticket ids; ask the user to create/link a card in `TICKET_TOOL`.

**Required for this repo:** [git-trello-tool](https://github.com/osuarez1/git-trello-tool) — see [sdlc/git-trello.md](sdlc/git-trello.md) and [integrations.md](integrations.md).

## Before you branch

1. Draft or locate the ticket — [ticket-card-info.md](ticket-card-info.md) (or Jira/Linear equivalent).
2. Create the branch from **`BASE_BRANCH`** (`main`) using team naming — typically via **`/lsi:card`** → `git ts`.
3. Push with explicit branch name if hooks require it (some tools reject `git push origin HEAD`).

Feature PRs target **`PR_TARGET_BRANCH`** (`staging`), not `BASE_BRANCH`. See [openspec-git-integration.md](openspec-git-integration.md).

## Relationship to other workflows

| Workflow | Role |
|----------|------|
| [ticket-card-info.md](ticket-card-info.md) | Card fields before `git ts` / branch creation |
| [openspec-git-integration.md](openspec-git-integration.md) | `/lsi:card`, `/lsi:branch`, full lifecycle |
| [commits-logical-order.md](commits-logical-order.md) | Commits only on feature branch; only when user asks |
| [pr-production-readiness.md](pr-production-readiness.md) | Merge/rebase `PR_TARGET_BRANCH` before feature PR |
| [branch-reviewability.md](branch-reviewability.md) | PR size limits and split guidance |

## Related

- [which-workflow.md](which-workflow.md)
- [openspec-git-integration.md](openspec-git-integration.md)
- [common-mistakes.md](common-mistakes.md) — implementing on `main`
