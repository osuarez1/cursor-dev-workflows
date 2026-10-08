---
name: /lsi-pr
id: lsi-pr
category: Workflow
description: Draft PR for Bitbucket (modes A/B/C; default target staging)
---

Draft (and optionally push) a pull request for the active OpenSpec change. **PR-only** — do not run readiness, review, or verify.

**Canonical source:** [pull-requests.md](../../docs/workflows/pull-requests.md) · [pr-description.template.md](../../docs/workflows/templates/pr-description.template.md) · [`docs/workflows/openspec-git-integration.md` § Pull request](../../docs/workflows/openspec-git-integration.md#pull-request-from-openspec)

**Input:** Change slug (optional). Mode **A** | **B** | **C** (required or inferred + confirm). Base branch default **`staging`**.

**Modes**

| Mode | Scope | Gate |
|------|--------|------|
| **A** | `openspec/` only | Refuse any path outside `openspec/` |
| **B** | Implementation; OpenSpec edits OK | Normal code PR after Mode A (unless C) |
| **C** | Docs + impl one PR | Explicit opt-in; warn at `PR_WARN_FILES=15` / `PR_WARN_LINES=250`; refuse above `PR_MAX_FILES=25` / `PR_MAX_LINES=400` (PROJECT/patch tokens override; else those defaults) |

**Steps**

1. **Resolve change** — announce slug.

2. **Verify branch** — ticket-linked branch only; refuse `main` or `staging`.

3. **Resolve mode**

   - Use user-provided mode, or infer from `git diff staging...HEAD` and **confirm** with the user.
   - Mode A: if any path outside `openspec/` → refuse Mode A.
   - Mode C: compute changed files/lines vs `staging`; warn at WARN_*; refuse above MAX_*.

4. **Gather PR metadata from OpenSpec**

   | Section | Source |
   |---------|--------|
   | **Overview** | `proposal.md` → Why (+ mode A/B/C note) |
   | **Changes** | What Changes + `design.md` |
   | **Potential risks** | BREAKING in proposal + design risks |
   | **Testing** | tasks.md + `TEST_COMMAND` when applicable; docs-only N/A for Mode A |
   | **Related** | `openspec/changes/<slug>/proposal.md` + Trello card id/URL |

5. **Draft PR**

   ```bash
   git status
   git diff staging...HEAD --stat
   git log staging..HEAD --oneline
   ```

   **Title:** Conventional Commits format (≤ ~72 chars).

   Present full PR body per [pr-description.template.md](../../docs/workflows/templates/pr-description.template.md).

   If `git log staging..HEAD` spans multiple themes or a large catch-up vs `staging`, state that explicitly in **Overview**.

   **Mandatory clipboard output (always):** after the summary header, emit **exactly two** fenced blocks — **Title (copy below)** then **Body (copy below)**. Put **all** title and body content **only** inside those blocks.

6. **Push (only if user confirms)**

   Ask: "Push branch and create Bitbucket PR to `staging` with the above title and body?"

   If yes:

   ```bash
   git push -u origin "$(git branch --show-current)"
   ```

   Then instruct user to create the PR in **Bitbucket** with the drafted title and body.

   **Do not** run `gh pr create` — this repo uses Bitbucket only (unless `PROJECT.md` `PR_HOST` is GitHub for that adopter).

**Output**

```
## PR: <slug>

**Mode:** A | B | C
**Target:** staging
**URL:** <PR create URL or "not created — awaiting confirmation">
```

Then **Title (copy below)** (`text` fence) and **Body (copy below)** (`markdown` fence) as today.

**Output (refuse)**

```
## Refuse: /lsi:pr

**Reason:** <wrong branch | Mode A purity | Mode C over max>
**Fix:** <checkout ticket branch | use Mode B/C | split PR>
```

**Guardrails**

- **PR-only:** do **not** run `/lsi:readiness`, `/lsi:review`, or `/opsx:verify` inside this command
- **Always** emit separate Title/Body fenced blocks
- Do **not** auto-push without user confirmation
- Default PR target is **`staging`**, not `main`
- Do **not** emit a Next footer; agents MUST emit the Output skeleton
- Bot session exception: when nested under `/lsi:apply-bot`, that invocation satisfies "user asks" for push/`create-pr` within that session's scope — see [integrations.md](../../docs/workflows/integrations.md) Bot sessions; standalone defaults unchanged.
