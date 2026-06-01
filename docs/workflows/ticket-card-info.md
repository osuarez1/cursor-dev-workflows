# Ticket card info

Use when drafting **task cards** before branching. Output is for copy-paste into `TICKET_TOOL` (Jira, Linear, Trello, or manual entry). Customize `TITLE_PREFIX` and task types (see [README.md](../../README.md)).

**Do not** create remote tickets/cards or run tracker CLI commands (e.g. Trello `git ts`) unless the user explicitly asks.

## Triggers

- create / draft ticket card, Jira issue, Linear issue, Trello card
- tracker CLI prompts (e.g. `git ts`), task type / title / description
- start work before branch (with [branch-workflow.md](branch-workflow.md))

## Output format (required)

Use exactly these three headings. Wrap **only the paste-ready value** for each item in its **own** fenced code block (Copy to Clipboard).

### 1. Task type

- Single lowercase keyword for branch prefix when your team uses ticket-linked branch names.
- **Default allowed values:** `feature`, `bugfix`, `hotfix`, `chore`, `release`
- Pick the narrowest accurate type:
  - user-visible capability → `feature`
  - broken behavior → `bugfix`
  - urgent production fix → `hotfix`
  - maintenance, config, docs-only, tests-only → `chore`
  - versioned rollout → `release`

```text
feature
```

### 2. Task title

- **Required prefix:** `TITLE_PREFIX` (e.g. `MyApp | ` — repo name, pipe, space)
- Imperative mood, present tense after the prefix
- Full title under **60 characters** (prefix counts). No quotes. No trailing period.
- Align with [commits-logical-order.md](commits-logical-order.md) subject style after the prefix

```text
MyApp | Add webhook signature verification
```

### 3. Task description

Markdown body. Required sections:

**Context/Goal** — Why this exists; link plans or prior work.

**Acceptance Criteria** — `- [ ]` list, 3–8 concrete, verifiable outcomes.

**Technical Notes** — When relevant:

- Paths under `SOURCE_ROOT` / `TEST_ROOT`
- `TEST_COMMAND`, `LINT_COMMAND`
- Stack constraints from project docs
- Branch pattern `BRANCH_PATTERN`, commit/PR conventions
- Push command if hooks require explicit branch name

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

## Agent boundaries

- Ground content in **actual** context (read files/plans when technical).
- One card = one deliverable when possible.
- If context is insufficient, ask **one** focused question; use `(confirm: …)` only in Technical Notes.
- Do not implement on `PROTECTED_BRANCHES` — [branch-workflow.md](branch-workflow.md).

## Examples

- [examples/ticket-good-vs-weak.md](../../examples/ticket-good-vs-weak.md)
- Template: [templates/ticket-card-output.example.md](../../templates/ticket-card-output.example.md)

## Related

- [branch-workflow.md](branch-workflow.md)  
- [integrations.md](integrations.md) — optional tracker tooling  
- [which-workflow.md](../../which-workflow.md)  
