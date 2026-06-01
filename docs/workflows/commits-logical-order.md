# Commits and logical order

How agents **plan** and **execute** git commits. Language- and framework-agnostic.

## Golden rules

1. **Only run `git commit` when the user explicitly asks** (or a project user rule requires the same). See [snippets/user-rule-only-commit-when-asked.md](../../snippets/user-rule-only-commit-when-asked.md).
2. **Before the first commit** on a branch with multiple concerns, output a **commit plan** (ordered list).
3. **One logical change per commit** — do not mix unrelated feature, refactor, and fix. Do not “compact” several logical changes into one commit or a one-line subject when a body is needed.
4. **Conventional Commits** for every commit (see below).
5. **No** `git commit --amend`, squash, or `rebase -i` unless the user explicitly requests.
6. **Never** `--no-verify` unless the user explicitly requests.

## When the user asks for a commit message

When drafting text only (not running `git commit`):

1. Match **Conventional Commits** for the subject line (see below).
2. Use **imperative mood** (`add`, `fix`, `remove` — not `added`, `fixes`, `adding`).
3. Keep the subject **≤ ~72 characters** when practical; no trailing period.
4. Choose the **narrowest accurate `type`**. If unsure between `feat` and `fix`, ask one clarifying question or default to what the code does (user-visible behavior → `feat`/`fix`; tooling-only → `chore`/`ci`).
5. For **PR** title or body, follow [pull-requests.md](pull-requests.md).
6. Issue footers: `Closes PROJ-123`, `Resolves #456`, or your team’s ticket URL — do not assume GitHub `#issue` unless the user referenced it.

Good and weak examples: [examples/commit-messages-good-vs-weak.md](../../examples/commit-messages-good-vs-weak.md).

## When the user asks to commit

1. `git status` — untracked and modified files  
2. `git diff` — staged and unstaged  
3. `git log` — recent message style on branch  
4. Stage only files for **one** logical commit (or execute the approved plan one commit at a time)  
5. Commit with HEREDOC message  
6. `git status` after — verify success  

If the hook fails, **do not amend** — fix and create a **new** commit.

## Conventional Commits

### Format

```text
<type>(<optional-scope>): <description>

<optional body>

<optional footer>
```

### Types

| type | Use when |
|------|----------|
| `feat` | New user-facing capability or API behavior |
| `fix` | Bug fix |
| `chore` | Maintenance, deps, tooling (not product fix/feature) |
| `docs` | Documentation only |
| `refactor` | Neither fix nor feature |
| `style` | Formatting only |
| `test` | Tests only |
| `ci` | CI/CD |
| `build` | Build system / artifacts |

### Subject

- Imperative, present tense; completes *“If applied, this commit will …”*
- Lowercase first letter after colon; **no** trailing period
- ≤ ~72 characters when practical

### Body

- What and **why**, not line-by-line how
- Blank line between subject and body
- Bullets for multiple points

### Footer

- `BREAKING CHANGE:` when applicable
- Ticket keys: `Closes PROJ-123`, Trello URL, etc.
- Hook-generated footers (e.g. Trello card id from branch) — **do not hand-write** if hooks add them; see [integrations.md](integrations.md)

## Commit plan format

Output before committing when N > 1 logical commit:

```markdown
## Proposed commit plan (N commits)

### 1. feat(api): add webhook signature verification
**Includes:** path/to/handler.ts, path/to/handler.test.ts
**Body:**
- Verify HMAC before parsing body

### 2. test(api): add regression for invalid signature
**Includes:** path/to/handler.test.ts
```

Template: [templates/commit-plan.example.md](../../templates/commit-plan.example.md)  
Examples: [examples/commit-plan-good-vs-weak.md](../../examples/commit-plan-good-vs-weak.md)

## Scope

Use short domain scopes: `api`, `auth`, `ui`, `deps`, package name in monorepos.

## Forbidden files

Do not commit secrets (`.env`, credentials, private keys). Warn the user if they request it.

## Why this matters

Structured commits improve **history search**, **changelogs**, and **review focus**. Pair with structured PRs ([pull-requests.md](pull-requests.md)) so QA steps stay explicit.

## Related

- [pull-requests.md](pull-requests.md)  
- [branch-workflow.md](branch-workflow.md)  
- [pr-production-readiness.md](pr-production-readiness.md)  
- [common-mistakes.md](common-mistakes.md)  
- [which-workflow.md](../../which-workflow.md)  
- [examples/commit-messages-good-vs-weak.md](../../examples/commit-messages-good-vs-weak.md)  
