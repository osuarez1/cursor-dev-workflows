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
   - uv run pytest --cov=src --cov=dev --cov-fail-under=100 — passed locally
   - <other verification steps>

   Related
   -------
   openspec/changes/<slug>/proposal.md
   Trello: <card id or URL>
   <Bitbucket PR URL>
   ```

5. **Output**

   Provide a `text` fenced code block for copy-paste into Bitbucket's extended description field.

   **Next steps footer:**
   - PR to **`staging`**: "Next: staging QA, then `/lsi:promote`. Do **not** sync or archive."
   - PR to **`main`**: "Next: checkout **`main`**, pull, then `/lsi:close`."

**Output**

```
## Merge extended description: PR #N

**Subject (keep Bitbucket default):** <merge title>

**Extended description (copy below):**

```text
...
```
```

**Guardrails**

- Use underline section headers — not markdown `##`.
- First line of body is PR title in Conventional Commits form.
- **Do not** use `gh pr view` — Bitbucket only.
- Squash merge: use PR title as squash subject and shortened Overview — not this extended format.
