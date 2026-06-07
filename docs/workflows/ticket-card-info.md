# Ticket card info

Use when drafting **task cards** before branching. Output is for copy-paste into `TICKET_TOOL` (Jira, Linear, Trello, or manual entry). Customize `TITLE_PREFIX` and task types (see [README.md](../../README.md)).

**Do not** create remote tickets/cards or run tracker CLI commands (e.g. Trello `git ts`) unless the user explicitly asks.

When running Trello Start, use **`git ts`** (space-separated Git subcommand via local alias) — not `git-ts` or `which git-ts`. See [integrations.md](integrations.md).

## Triggers

- create / draft ticket card, Jira issue, Linear issue, Trello card
- tracker CLI prompts (e.g. `git ts`), task type / title / description
- start work before branch (with [branch-workflow.md](branch-workflow.md))

## Output format (required)

**Mandatory clipboard output (always):** emit **exactly three** fenced blocks in order — **Task type (copy below)**, **Task title (copy below)**, **Task description (copy below)**. Put **all** paste-ready values **only** inside those blocks; do not repeat type, title, or description as prose, bullets, or un-fenced markdown elsewhere in the response.

Use these labels and fence types:

### Task type (copy below)

- Single lowercase keyword for branch prefix when your team uses ticket-linked branch names.
- **Default allowed values:** `feature`, `bugfix`, `hotfix`, `chore`, `release`
- Pick the narrowest accurate type:
  - user-visible capability → `feature`
  - broken behavior → `bugfix`
  - urgent production fix → `hotfix`
  - maintenance, config, docs-only, tests-only → `chore`
  - versioned rollout → `release`

````markdown
**Task type (copy below):**

```text
feature
```
````

### Task title (copy below)

- **Required prefix:** `TITLE_PREFIX` (e.g. `MyApp | ` — repo name, pipe, space)
- Imperative mood, present tense after the prefix
- Full title under **60 characters** (prefix counts). No quotes. No trailing period.
- Align with [commits-logical-order.md](commits-logical-order.md) subject style after the prefix

````markdown
**Task title (copy below):**

```text
MyApp | Add webhook signature verification
```
````

### Task description (copy below)

Markdown body. Required sections:

**Context/Goal** — Why this exists; link plans or prior work.

**Acceptance Criteria** — `- [ ]` list, 3–8 concrete, verifiable outcomes.

**Technical Notes** — When relevant:

- Paths under `SOURCE_ROOT` / `TEST_ROOT`
- `TEST_COMMAND`, `LINT_COMMAND`
- Stack constraints from project docs
- Branch pattern `BRANCH_PATTERN`, commit/PR conventions
- Push command if hooks require explicit branch name

````markdown
**Task description (copy below):**

```markdown
**Context/Goal**
Brief explanation of why this work is needed.

**Acceptance Criteria**
- [ ] First verifiable requirement.
- [ ] Related tests pass (`TEST_COMMAND` or named paths) when SOURCE_ROOT changes.
- [ ] Second verifiable requirement.

**Technical Notes**
- Relevant paths, APIs, or commands for this repo.
```
````

## Agent boundaries

- Ground content in **actual** context (read files/plans when technical).
- One card = one deliverable when possible.
- If context is insufficient, ask **one** focused question; use `(confirm: …)` only in Technical Notes.
- Do not implement on `PROTECTED_BRANCHES` — [branch-workflow.md](branch-workflow.md).

### LSI repos (OpenSpec + Trello)

When using **`/lsi:card`**, **`/lsi:card-link`**, **`/lsi:trello-branch`**, or **`/lsi:trello-list`** (confirm path):

1. **Require** an open in-progress OpenSpec change (`openspec/changes/<slug>/` with `proposal.md`) before creating or updating Trello cards — except trello-list **Exit** (list-only).
2. **Draft** Context/Goal from `proposal.md` **Why**; Acceptance Criteria from `tasks.md`; Technical Notes from `design.md` when present.
3. **Redact** before Trello API: secrets, `.env`, credentials, absolute home paths, org-only slugs; link `openspec/changes/<slug>/`.
4. Branch suffix after card setup = OpenSpec change slug (kebab-case).

See [integrations.md](integrations.md) and adopted [openspec-git-integration.md](openspec-git-integration.md).

## Examples

- [examples/ticket-good-vs-weak.md](../../examples/ticket-good-vs-weak.md)
- Template: [templates/ticket-card-output.example.md](../../templates/ticket-card-output.example.md)

## Related

- [branch-workflow.md](branch-workflow.md)  
- [integrations.md](integrations.md) — optional tracker tooling  
- [which-workflow.md](../../which-workflow.md)  
