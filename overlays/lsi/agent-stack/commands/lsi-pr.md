---
name: /lsi-pr
id: lsi-pr
category: Workflow
description: Readiness, review, draft PR for Bitbucket (default target staging)
---

Prepare and open a pull request for the active OpenSpec change after readiness and code review pass.

**Canonical source:** [pull-requests.md](../../docs/workflows/pull-requests.md) · [pr-description.template.md](../../docs/workflows/templates/pr-description.template.md) · [`docs/workflows/openspec-git-integration.md` § Pull request](../../docs/workflows/openspec-git-integration.md#pull-request-from-openspec)

**Input:** Optionally specify change slug or base branch (default **`staging`**).

**Steps**

1. **Resolve change** — announce slug.

2. **Verify branch** — ticket-linked branch only; refuse `main` or `staging`.

3. **Run `/lsi:readiness`**

   - Block if verdict is not `Ready` unless user documents explicit exemption.
   - Test suite must pass locally (see integration doc § PR production readiness).

4. **Run `/lsi:review`**

   - Block on blockers unless user accepts risk.
   - Request-changes items must be fixed or waived explicitly.

5. **Gather PR metadata from OpenSpec**

   | Section | Source |
   |---------|--------|
   | **Overview** | `proposal.md` → Why |
   | **Changes** | What Changes + `design.md` |
   | **Potential risks** | BREAKING in proposal + design risks + review |
   | **Testing** | tasks.md test tasks + test results from readiness |
   | **Related** | `openspec/changes/<slug>/proposal.md` + Trello card id/URL |

6. **Draft PR**

   ```bash
   git status
   git diff staging...HEAD
   git log staging..HEAD --oneline
   ```

   **Title:** Conventional Commits format (≤ ~72 chars).

   Present full PR body per [pr-description.template.md](../../docs/workflows/templates/pr-description.template.md).

   If `git log staging..HEAD` spans multiple themes or a large catch-up vs `staging`, state that explicitly in **Overview** (cumulative staging catch-up, not a single-ticket diff).

   **Mandatory clipboard output (always):** after the summary header, emit **exactly two** fenced blocks — **Title (copy below)** then **Body (copy below)**. Put **all** title and body content **only** inside those blocks; do not repeat title or body as prose, bullets, or un-fenced markdown elsewhere in the response.

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

Emit in this order:

1. Summary header (metadata only — no title/body prose here):

```
## PR: <slug>

**Target:** staging (default)
**URL:** <PR create URL or "not created — awaiting confirmation">

**Readiness:** Ready
**Review:** Approve

**CI:** Test suite ✓/✗
```

2. **Title (copy below)** — single line, `text` fence only:

````markdown
**Title (copy below):**

```text
<type>(<scope>): <imperative description>
```
````

3. **Body (copy below)** — full PR description, `markdown` fence only:

````markdown
**Body (copy below):**

```markdown
## Overview
...

## Changes
- ...

## Potential risks
- ...

## Testing
1. ...

## Related
- ...
```
````

4. Footer (after both blocks):

```
After merge: `/lsi:merge-desc` for extended merge description — **do not** sync or archive.
Next: staging QA → `/lsi:promote` → after main merge → `/lsi:close` on **main**.
```

**Guardrails**

- **Always** emit separate **Title (copy below)** and **Body (copy below)** fenced blocks — never title/body as inline prose only.
- Do **not** run `gh pr create` or any GitHub CLI PR commands.
- Do **not** auto-push without user confirmation.
- Default PR target is **`staging`**, not `main`.
- Full lifecycle (card → propose → apply → commits → PR → promote → close) requires separate confirmation per integration doc — mention in footer if scope unclear.
