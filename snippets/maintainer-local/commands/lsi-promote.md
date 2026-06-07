---
name: /lsi-promote
id: lsi-promote
category: Workflow
description: Draft production promotion PR to main after staging validation
---

Prepare and open a **production promotion** pull request after staging QA passes.

**Canonical source:** [pull-requests.md](../../.lsi/workflows/pull-requests.md) · [pr-description.template.md](../../.lsi/workflows/templates/pr-description.template.md) · [`.lsi/workflows/openspec-git-integration.md` § PR promotion](../../.lsi/workflows/openspec-git-integration.md#pr-promotion)

**Input:** Optionally specify change slug. Default base branch is **`main`** (`BASE_BRANCH` per [PROJECT.md](../../PROJECT.md)).

**Steps**

1. **Resolve change** — announce slug from branch suffix or OpenSpec context.

2. **Verify prerequisites**

   Ask user to confirm:
   - Feature PR merged to **`staging`**
   - Staging QA passed
   - Code on current branch includes staging-validated commits

   Refuse if user reports QA failed or feature was cut from release.

3. **Verify branch**

   Accept:
   - Ticket branch with `staging` merged/rebased
   - **`staging`** branch itself (when promoting accumulated staging to main)

   Refuse **`main`** for drafting (PR originates from feature/staging branch).

4. **Run `/lsi:readiness`** in **promotion mode** (`git diff main...HEAD`, PR target **`main`**)

   - Block if verdict is not `Ready` unless user documents explicit exemption.
   - `uv run pytest --cov=src --cov=dev --cov-fail-under=100` must pass locally when `src/` or `dev/` touched.

5. **Run `/lsi:review`** in **promotion mode** (`git diff main...HEAD`)

   - Block on blockers unless user accepts risk.

6. **Gather PR metadata from OpenSpec**

   | Section | Source |
   |---------|--------|
   | **Overview** | `proposal.md` → Why + note "promotion after staging validation" |
   | **Changes** | What Changes + `design.md` |
   | **Potential risks** | BREAKING in proposal + design risks + review |
   | **Testing** | Staging QA results + tasks.md test tasks |
   | **Related** | `openspec/changes/<slug>/proposal.md` + Trello card id/URL |

7. **Draft PR**

   ```bash
   git status
   git diff main...HEAD
   git log main..HEAD --oneline
   ```

   **Title:** Conventional Commits format (≤ ~72 chars).

   Present full PR body per [pr-description.template.md](../../.lsi/workflows/templates/pr-description.template.md).

   If `git log main..HEAD` spans multiple themes, note cumulative promotion scope in **Overview**.

8. **Push (only if user confirms)**

   Ask: "Push branch and create Bitbucket PR to **`main`** with the above title and body?"

   If yes:

   ```bash
   git push -u origin "$(git branch --show-current)"
   ```

   Then instruct user to create the PR in **Bitbucket** targeting **`main`**.

   **Do not** run `gh pr create` — this repo uses Bitbucket only.

9. **Post-push CI**

   Confirm Bitbucket Pipelines test job passes on the PR. Report status in output.

**Output**

```
## Promotion PR: <slug>

**Target:** main (production)
**URL:** <bitbucket pr url or "not created — awaiting confirmation">

**Readiness:** Ready
**Review:** Approve

**CI:** pytest coverage ✓/✗

After merge: `/lsi:merge-desc` (target main).
Next: checkout **main**, pull, then `/lsi:close`.
Do **not** sync or archive until merged to **main**.
```

**Guardrails**

- Do **not** run `gh pr create` or any GitHub CLI PR commands.
- Do **not** auto-push without user confirmation.
- Target is **`main`**, not `staging`.
- Do **not** suggest `/opsx:sync` or `/opsx:archive` before main merge.
