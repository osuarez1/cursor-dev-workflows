---
name: /lsi-commit
id: lsi-commit
category: Workflow
description: Commit plan from tasks.md with Conventional Commits
---

Create logical commits from the active OpenSpec change's `tasks.md` sections using Conventional Commits.

**Canonical source:** [commits-logical-order.md](../../.lsi/workflows/commits-logical-order.md) · [`.lsi/workflows/openspec-git-integration.md` § Commit mapping](../../.lsi/workflows/openspec-git-integration.md#commit-mapping)

**Input:** Optionally specify change slug. User must explicitly request commits — this command prepares and executes only when asked.

**Steps**

1. **Resolve change** — announce slug from `openspec list --json` or user input.

2. **Verify branch**

   - Must be `feature|bugfix|hotfix|chore/{24-char-id}-<change-slug>`, not `main` or `staging`.
   - Suffix must match change slug.
   - If wrong branch, stop and suggest `/lsi:card` or `/lsi:branch`.

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

   1. `type(scope): imperative description` — files: ...
   2. `type(scope): imperative description` — files: ...
   ```

   Map sections per integration doc worker scope table:

   | Area | Typical scope / type |
   |------|----------------------|
   | Worker listener / `main.py` | `feat(worker):` / `fix(worker):` |
   | FFmpeg / HLS pipeline | `feat(ffmpeg):` / `fix(ffmpeg):` |
   | S3 / AWS CLI upload | `feat(s3):` / `fix(s3):` |
   | Webhook / HTTP client | `feat(webhook):` / `fix(webhook):` |
   | Job payload / contracts | `feat(contracts):` / `fix(contracts):` |
   | Tests under `tests/` | `test(<scope>):` |
   | OpenSpec / workflow docs | `docs(openspec):` / `chore(docs):` |
   | CI / Bitbucket pipelines | `ci:` / `chore(ci):` |
   | Release / version | `chore(release):` |

   One logical change per commit.

5. **Execute commits (one at a time)**

   For each planned commit:

   - Stage only files for that commit
   - Commit with HEREDOC message:

   ```bash
   git commit -m "$(cat <<'EOF'
   type(scope): imperative description

   EOF
   )"
   ```

   - Verify with `git status` after each commit

6. **Never** use `--no-verify`, `--amend`, or squash unless user explicitly requests.

**Output**

```
## Commits complete

**Change:** <slug>
**Commits created:** N

<list of commit subjects>

Next: `/lsi:readiness` before opening a PR.
```

**Guardrails**

- Run `git commit` **only when the user explicitly asks** (invoking this command counts as asking).
- Never commit secrets (`.env`, credentials, `key.bin`, `tmp/`).
- If pre-commit hook fails, fix and create a **new** commit — do not amend.
- Refuse on `main` or `staging`.
