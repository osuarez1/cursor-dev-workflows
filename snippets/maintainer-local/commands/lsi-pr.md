---
name: /lsi-pr
id: lsi-pr
category: Workflow
description: Readiness, review, draft PR for Bitbucket (default target staging)
---

Prepare and open a pull request for the active OpenSpec change after readiness and code review pass.

**Canonical source:** [pull-requests.md](../../.lsi/workflows/pull-requests.md) · [pr-description.template.md](../../.lsi/workflows/templates/pr-description.template.md) · [`.lsi/workflows/openspec-git-integration.md` § Pull request](../../.lsi/workflows/openspec-git-integration.md#pull-request-from-openspec)

**Input:** Optionally specify change slug or base branch (default **`staging`**).

**Steps**

1. **Resolve change** — announce slug.

2. **Verify branch** — ticket-linked branch only; refuse `main` or `staging`.

3. **Run `/lsi:readiness`**

   - Block if verdict is not `Ready` unless user documents explicit exemption.
   - `uv run pytest --cov=src --cov=dev --cov-fail-under=100` must pass locally.

4. **Run `/lsi:review`**

   - Block on blockers unless user accepts risk.
   - Request-changes items must be fixed or waived explicitly.

5. **Gather PR metadata from OpenSpec**

   | Section | Source |
   |---------|--------|
   | **Overview** | `proposal.md` → Why |
   | **Changes** | What Changes + `design.md` |
   | **Potential risks** | BREAKING in proposal + design risks + review |
   | **Testing** | tasks.md test tasks + pytest results from readiness |
   | **Related** | `openspec/changes/<slug>/proposal.md` + Trello card id/URL |

6. **Draft PR**

   ```bash
   git status
   git diff staging...HEAD
   git log staging..HEAD --oneline
   ```

   **Title:** Conventional Commits format (≤ ~72 chars).

   Present full PR body per [pr-description.template.md](../../.lsi/workflows/templates/pr-description.template.md).

   If `git log staging..HEAD` spans multiple themes or a large catch-up vs `staging`, state that explicitly in **Overview** (cumulative staging catch-up, not a single-ticket diff).

7. **Push (only if user confirms)**

   Ask: "Push branch and create Bitbucket PR to `staging` with the above title and body?"

   If yes:

   ```bash
   git push -u origin "$(git branch --show-current)"
   ```

   Then instruct user to create the PR in **Bitbucket** with the drafted title and body.

   **Do not** run `gh pr create` — this repo uses Bitbucket only.

8. **Post-push CI**

   Confirm Bitbucket Pipelines test job passes on the PR. Report status in output.

**Output**

```
## PR: <slug>

**Target:** staging (default)
**URL:** <bitbucket pr url or "not created — awaiting confirmation">

**Readiness:** Ready
**Review:** Approve

**CI:** pytest coverage ✓/✗

After merge: `/lsi:merge-desc` for extended merge description — **do not** sync or archive.
Next: staging QA → `/lsi:promote` → after main merge → `/lsi:close` on **main**.
```

**Guardrails**

- Do **not** run `gh pr create` or any GitHub CLI PR commands.
- Do **not** auto-push without user confirmation.
- Default PR target is **`staging`**, not `main`.
- Full lifecycle (card → propose → apply → commits → PR → promote → close) requires separate confirmation per integration doc — mention in footer if scope unclear.
