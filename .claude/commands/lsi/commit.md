---
description: Commit plan from tasks.md with Conventional Commits
---

Create logical commits from the active OpenSpec change's `tasks.md` sections using Conventional Commits.

**Canonical source:** [commits-logical-order.md](../../docs/workflows/commits-logical-order.md) · [`overlays/lsi/docs/workflows/openspec-git-integration.md` § Commit mapping](../../overlays/lsi/docs/workflows/openspec-git-integration.md#commit-mapping)

**Input:** Optionally specify change slug. User must explicitly request commits — this command prepares and executes only when asked.

**Steps**

1. **Resolve change** — announce slug from `openspec list --json` or user input.

2. **Verify branch**

   - Must be `feature|bugfix|hotfix|chore/{24-char-id}-<change-slug>`, not `main` or `staging`.
   - Suffix must match change slug.
   - If wrong branch, stop with refuse Output.

3. **Gather state**

   Run in parallel:

   ```bash
   git status --short
   git diff
   git log --oneline -5
   ```

   Read `openspec/changes/<slug>/tasks.md` for section groupings.

4. **Output commit plan (required before first commit)**

   Ordered list mapping `tasks.md` sections → commit message:

   ```markdown
   ## Commit plan

   1. `type(scope): imperative description`
      - **files:** ...
      - **body:** what changed and why it matters
   2. `type(scope): imperative description`
      - **files:** ...
      - **body:** what changed and why it matters
   ```

   Every entry carries a body — the user reviews the explanation before any commit runs.

   Derive commit scopes from [`overlays/lsi/docs/workflows/openspec-git-integration.md` § Commit mapping](../../overlays/lsi/docs/workflows/openspec-git-integration.md#commit-mapping) (per-repo overlay). Do **not** embed adopter-specific domain scope tables in this command. One logical change per commit.

5. **Execute commits (one at a time)**

   For each planned commit:

   - Stage only files for that commit
   - Commit with HEREDOC message:

   ```bash
   git commit -m "$(cat <<'EOF'
   type(scope): imperative description

   Explain what changed and why it matters — the constraint, the bug's
   consequence, or the decision behind it. Wrap at ~72 characters and use
   bullets when the commit has several distinct points.
   EOF
   )"
   ```

   - Verify with `git status` after each commit

   The body is **required**. Never leave it empty, and never restate the subject in other words — if the body would only rephrase the subject, write the motivation or consequence instead. Do **not** hand-write `Trello-Card:`; git-trello `prepare-commit-msg` appends it from the branch id when present.

6. **Never** use `--no-verify`, `--amend`, or squash unless user explicitly requests.

**Output**

```
## Commits complete

**Change:** <slug>
**Commits created:** N

### Subjects
- `type(scope): subject`
```

**Output (refuse)**

```
## Refuse: /lsi-commit

**Reason:** <wrong branch | no changes | ambiguous slug>
**Fix:** <one line>
```

**Guardrails**

- Run `git commit` **only when the user explicitly asks** (invoking this command counts as asking).
- Never commit secrets (`.env`, credentials, key files, `tmp/`).
- Never create a subject-only commit — every message carries an explanatory body.
- Never hand-write the `Trello-Card:` trailer — the hook adds it when configured.
- If pre-commit hook fails, fix and create a **new** commit — do not amend.
- Refuse on `main` or `staging`.
- MUST emit the Output skeleton; MUST NOT invent alternate report shapes or append follow-up questions.
- No `Next:` footer (D11).
