---
description: Draft production promotion PR to main after staging validation
---

Prepare and open a **production promotion** pull request after staging QA passes.

**Canonical source:** [pull-requests.md](../../docs/workflows/pull-requests.md) · [pr-description.template.md](../../templates/pr-description.template.md) · [`overlays/lsi/docs/workflows/openspec-git-integration.md` § PR promotion](../../overlays/lsi/docs/workflows/openspec-git-integration.md#pr-promotion)

**Input:** Optionally specify change slug. Default base branch is **`main`** (`BASE_BRANCH` per [PROJECT.md](../../PROJECT.md)).

**Steps**

1. **Resolve change** — announce slug from branch suffix or OpenSpec context.

2. **Verify prerequisites**

   Ask user to confirm:
   - Feature PR(s) merged to **`staging`**
   - Staging QA passed
   - Change is still **active** (do **not** require `/lsi:close` yet — close runs on **`main`** after this promotion merges)
   - Code on current branch includes staging-validated commits

   Refuse if user reports QA failed or feature was cut from release.

3. **Verify branch**

   Accept:
   - Ticket branch with `staging` merged/rebased
   - **`staging`** branch itself (when promoting accumulated staging to main)

   Refuse **`main`** for drafting (PR originates from feature/staging branch).

4. **Gather PR metadata from OpenSpec** (do not run readiness/review inside this command)

   | Section | Source |
   |---------|--------|
   | **Overview** | `proposal.md` → Why + note "promotion after staging QA; close on main after merge" |
   | **Changes** | What Changes + `design.md` |
   | **Potential risks** | BREAKING in proposal + design risks |
   | **Testing** | Staging QA results + tasks.md test tasks |
   | **Related** | active `openspec/changes/<slug>/` + Trello card id/URL |

5. **Draft PR**

   ```bash
   git status
   git diff main...HEAD
   git log main..HEAD --oneline
   ```

   **Title:** Conventional Commits format (≤ ~72 chars).

   Present full PR body per [pr-description.template.md](../../templates/pr-description.template.md).

   If `git log main..HEAD` spans multiple themes, note cumulative promotion scope in **Overview**.

6. **Push (only if user confirms)**

   Ask: "Push branch and create Bitbucket PR to **`main`** with the above title and body?"

   If yes:

   ```bash
   git push -u origin "$(git branch --show-current)"
   ```

   Then instruct user to create the PR in **Bitbucket** targeting **`main`**.

   **Do not** run `gh pr create` — this repo uses Bitbucket only.

7. **Post-push CI**

   Confirm Bitbucket Pipelines test job passes on the PR. Report status in output.

**Output**

```
## Promotion PR: <slug>

**Target:** main (production)
**URL:** <bitbucket pr url or "not created — awaiting confirmation">
**Close:** after this PR merges — `/lsi:close` on **main**
**CI:** Test suite ✓/✗ / N/A
```

**Guardrails**

- Do **not** run `gh pr create` or any GitHub CLI PR commands.
- Do **not** auto-push without user confirmation.
- Target is **`main`**, not `staging`.
- Do **not** run readiness/review/verify inside promote; do **not** emit a Next footer
- Do **not** run `/lsi:close` or release-train inside promote — close is on **`main`** after merge
- Agents MUST emit the Output skeleton
