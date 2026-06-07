# Pull requests

Normative rules for **PR titles**, **descriptions**, and **hygiene** on `PR_HOST`. Customize placeholders via [README.md](../../README.md).

For **“ready to open a PR?”** checklists and verdicts, use [pr-production-readiness.md](pr-production-readiness.md). For merge-gate review, [code-review.md](code-review.md). Commit message rules: [commits-logical-order.md](commits-logical-order.md).

## Triggers

- draft PR title, PR description, PR copy
- open a pull request on `PR_HOST`
- what should the PR say
- PR merge info, merge commit message, extended description, confirm merge on `PR_HOST`

## Platform

- Open PRs on `PR_HOST` against `BASE_BRANCH` (and release/staging branches when your team uses them).
- Link tickets in **Related** using `TICKET_TOOL` (issue URL, key such as `PROJ-456`, etc.).
- Do not assume GitHub `#123` unless the user referenced it.

## PR title

Same rules as [Conventional Commits](commits-logical-order.md):

```text
<type>(<optional-scope>): <description>
```

- Imperative mood, present tense; lowercase first letter after the colon; **no** trailing period.
- ≤ ~72 characters when practical.
- Should **stand alone** — a reviewer understands the theme without opening every file.

**Good**

```text
feat(api): add webhook signature verification for inbound events
```

```text
docs(workflows): add pull request title and description guide
```

**Avoid**

```text
Fixed stuff
```

```text
feat: updates.
```

More examples: [examples/pr-description-good-vs-weak.md](../../examples/pr-description-good-vs-weak.md).

## PR description

Use markdown. Required sections:

### Overview

Why this change exists; link to product or ticket context when available.

### Changes

Bullet list of major behavior or areas — not a file-by-file dump.

### Potential risks

Regression areas, migration risk, auth/payment edge cases, deploy notes, or other merge concerns.

### Testing

Numbered steps a reviewer can run. When application code under `SOURCE_ROOT` changed, include `TEST_COMMAND` (or scoped variant) or list explicit test paths. See [test-requirements.md](test-requirements.md).

### Related

Links to tickets, design docs, or runbooks.

### Template

Copy-paste shape: [templates/pr-description.template.md](../../templates/pr-description.template.md).

```markdown
## Overview
<Why this change exists; link to ticket or product context if available.>

## Changes
- <major behavior or area>
- <major behavior or area>

## Potential risks
- <regression or deploy concern>

## Testing
1. <TEST_COMMAND or scoped variant>
2. <manual step a reviewer can run>

## Related
- <ticket URL, design doc, runbook>
```

### Checklist (application changes)

```markdown
- [ ] Tests added or updated for `SOURCE_ROOT` changes (see test-requirements.md)
- [ ] `TEST_COMMAND` passes (or Testing explains exemption)
- [ ] `LINT_COMMAND` passes (if the project uses it)
- [ ] No unintended secrets or credentials
- [ ] Docs, migrations, or config updated if applicable
```

### Checklist (docs-only or config-only PRs)

```markdown
- [ ] No unintended secrets or credentials
- [ ] Docs or config changes are intentional and scoped
```

## PR merge commit (GitHub merge commit)

When the user merges with a **merge commit** on `PR_HOST` (not squash), use GitHub’s two fields as follows.

### Commit message (subject)

Keep GitHub’s default unless the team has documented another merge strategy:

```text
Merge pull request #<N> from <owner>/<branch>
```

Do not put the Conventional Commits PR title here; that belongs in the PR title field when opening the PR, and in **Commits merged** below.

### Extended description (body)

Plain text (not markdown `##` headings). Required blocks in order:

1. **Summary** — one or two sentences on why this merged (from PR Overview).
2. **`Changes:`** — bullets: `path or area — what changed` (major files or release artifacts, not every diff hunk).
3. **`Commits merged:`** — bullets: each feature commit on the branch, **oldest first** (how the branch was built). Omit merge commits that only sync `BASE_BRANCH` into the branch (e.g. `Merge branch 'main' into …`). Gather with `git log BASE_BRANCH..HEAD --oneline --reverse --no-merges`.
4. **`Post-merge:`** — one line: tag, deploy, notify operators, or `none` if nothing is required.

Template: [templates/pr-merge-extended-description.template.md](../../templates/pr-merge-extended-description.template.md).  
Examples: [examples/pr-merge-commit-good-vs-weak.md](../../examples/pr-merge-commit-good-vs-weak.md).

```text
<Summary paragraph>

Changes:
- <path or area> — <outcome>
- <path or area> — <outcome>

Commits merged:
- <type>(<scope>): <subject>
- <type>(<scope>): <subject>

Post-merge: <action or none>
```

### Squash merge

If the repo uses **squash and merge**, the squash dialog uses a single subject + body: use the **PR title** (Conventional Commits) as the subject and a shortened summary from Overview — not the merge-commit extended description format above.

## Hygiene

- Merge or rebase `BASE_BRANCH` into the branch before final review so the diff stays current.
- Prefer **small, reviewable PRs**; if the diff is large, call that out in Overview and justify.
- Branch name should match `BRANCH_PATTERN` and `TICKET_ID_PATTERN` when enforced — see [branch-workflow.md](branch-workflow.md).
- Push with an explicit branch name when hooks require it: `git push -u origin "$(git branch --show-current)"`.

## Assistant output

### PR title and description

When drafting a PR for the user:

1. **Title** — **always** one line in a `text` fenced code block labeled **Title (copy below)**.
2. **Description** — **always** full markdown body in a `markdown` fenced code block labeled **Body (copy below)** using the section template above. Do not put title or body content outside those blocks.
3. Match commit **type** and **scope** from [commits-logical-order.md](commits-logical-order.md).
4. Include concrete **Testing** steps using `TEST_COMMAND` and manual reviewer steps.
5. Run [code-review.md](code-review.md) checklists before opening a PR when an agent or self-review was performed.

### Merge commit (merge-commit strategy only)

When the user asks for **PR merge info**, **merge commit text**, or help filling the merge dialog:

1. **Commit message** — keep GitHub’s default `Merge pull request #…` line; state that explicitly; do not replace with the PR title.
2. **Extended description** — **always** output a `text` fenced code block labeled **Extended description (copy below)** with Summary, `Changes:`, `Commits merged:`, and `Post-merge:` blocks per the template above. Do not put merge body content outside that block.
3. **Commits merged** — populate from `git log BASE_BRANCH..HEAD --oneline --reverse --no-merges` when branch history is available (oldest first; omit sync merges from `BASE_BRANCH`).

## Overlap with other workflows

| Doc | Role |
|-----|------|
| This file | Title/body **conventions** and assistant output format |
| [pr-production-readiness.md](pr-production-readiness.md) | **Readiness** checklist + `Ready` \| `Needs fixes` \| `Blocked` |
| [code-review.md](code-review.md) | Merge-gate **review** (logic, security, performance, tests) |

## Related

- [commits-logical-order.md](commits-logical-order.md)  
- [pr-production-readiness.md](pr-production-readiness.md)  
- [code-review.md](code-review.md)  
- [test-requirements.md](test-requirements.md)  
- [branch-workflow.md](branch-workflow.md)  
- [which-workflow.md](../../which-workflow.md)  
- [examples/pr-description-good-vs-weak.md](../../examples/pr-description-good-vs-weak.md)  
- [examples/pr-merge-commit-good-vs-weak.md](../../examples/pr-merge-commit-good-vs-weak.md)  
- [templates/pr-merge-extended-description.template.md](../../templates/pr-merge-extended-description.template.md)  
