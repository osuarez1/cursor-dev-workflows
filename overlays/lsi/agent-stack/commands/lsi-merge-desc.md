---
name: /lsi-merge-desc
id: lsi-merge-desc
category: Workflow
description: Mandatory extended merge description for Bitbucket merge dialog
---

Generate the mandatory extended merge description for Bitbucket's merge-commit dialog after a PR is approved.

**Canonical source:** [commit-pr-conventions.mdc](../../.cursor/rules/commit-pr-conventions.mdc) · [`docs/workflows/openspec-git-integration.md` § Merge extended description](../../docs/workflows/openspec-git-integration.md#merge-extended-description-bitbucket)

**Input:** PR number, branch name, Bitbucket PR URL, or merge target (`staging` or `main`). If omitted, infer from current branch and ask if ambiguous.

**Steps**

1. **Identify PR and merge target**

   Use PR number or URL from user input, or ask user for Bitbucket PR link.

   Determine merge target:
   - Default: **`staging`** (feature PR)
   - **`main`**: promotion PR — use `origin/main..HEAD` for commit log

   ```bash
   git branch --show-current
   ```

2. **Gather commits**

   For PRs targeting **`staging`** (default):

   ```bash
   git log origin/staging..HEAD --oneline --reverse --no-merges
   ```

   For PRs targeting **`main`**:

   ```bash
   git log origin/main..HEAD --oneline --reverse --no-merges
   ```

   Group into numbered logical commits when the PR used a commit plan. Count → `Commits (N logical)`.

3. **Gather PR body sections**

   From PR description or OpenSpec artifacts:
   - Overview, Changes, Potential risks, Testing, Related

4. **Build extended description**

   **Subject (Bitbucket default — do not replace):** merge title from PR

   **Body — mandatory full format (plain text, underline headers):**

   ```text
   <type>(<scope>): <imperative description matching PR title>

   Overview
   --------
   <Why this merged; 2–4 sentences>

   Changes
   -------
   - <path or area> — <outcome>

   Commits (N logical)
   -------------------
   1. <type>(<scope>): <subject>
   2. ...

   Potential risks
   ---------------
   - <concerns or "none" for docs-only>

   Testing
   -------
   - Test suite (see `PROJECT.md` `TEST_COMMAND`) — passed locally
   - <other verification steps>

   Related
   -------
   openspec/changes/<slug>/proposal.md
   Trello: <card id or URL>
   <Bitbucket PR URL>
   ```

5. **Output**

   **Mandatory clipboard output (always):** emit the extended description **only** inside a **`text`** fenced block labeled **Extended description (copy below)**. Do not put merge body content in prose, bullets, or un-fenced markdown outside that block.

   **Next steps footer** (after the copy block, not inside it):
   - PR to **`staging`**: "Next: staging QA, then `/lsi:promote`. Do **not** sync or archive."
   - PR to **`main`**: "Next: checkout **`main`**, pull, then `/lsi:close`."

**Output**

Emit in this order:

1. Summary header (metadata only):

```
## Merge extended description: PR #N

**Subject (keep platform default):** Merge pull request #N from …
**Target:** staging | main
```

2. **Extended description (copy below)** — full merge body, `text` fence only (underline headers, not markdown `##`):

````markdown
**Extended description (copy below):**

```text
<type>(<scope>): <imperative description matching PR title>

Overview
--------
...

Changes
-------
- ...

Commits (N logical)
-------------------
1. ...

Potential risks
---------------
- ...

Testing
-------
- ...

Related
-------
...
```
````

3. Footer (after the copy block).

**Guardrails**

- **Always** emit **Extended description (copy below)** as a single `text` fenced block — never merge body as inline prose only.
- Use underline section headers inside the block — not markdown `##`.
- First line of the copy block is PR title in Conventional Commits form.
- **Do not** use `gh pr view` unless user explicitly asks and `PR_HOST` is GitHub.
- Squash merge: use PR title as squash subject and shortened Overview — not this extended format.
