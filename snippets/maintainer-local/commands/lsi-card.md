---
name: /lsi-card
id: lsi-card
category: Workflow
description: Draft Trello card from OpenSpec change and create card + branch via git ts
---

Create a Trello card and ticket-linked branch for the active OpenSpec change using [git-trello-tool](https://github.com/osuarez1/git-trello-tool) **`git ts`**.

**Canonical source:** [ticket-card-info.md](../../.lsi/workflows/ticket-card-info.md) · [git-trello.md](../../.lsi/workflows/sdlc/git-trello.md) · [`.lsi/workflows/openspec-git-integration.md`](../../.lsi/workflows/openspec-git-integration.md) (when present)

**Protected-branch exception:** This is the **only** `/lsi:*` command allowed on a protected branch — and **only on `main`**, never on `staging`. Card + branch creation only; no `src/` edits.

**Input:** Optionally specify change slug after `/lsi:card`. Invoking this command counts as explicit consent to run `git ts`.

**Steps**

1. **Resolve active change**

   ```bash
   openspec list --json
   git branch --show-current
   ```

   - If a slug was provided, use it.
   - If only one active change exists, announce: "Using change: `<slug>`".
   - If multiple active changes exist, use the **AskQuestion tool** — do not guess.

2. **Verify starting point**

   - **`git ts` MUST run from `main` only** — `git pull origin main` first.
   - **Refuse on `staging`** — checkout `main` before continuing.
   - If on a feature branch without a card, checkout `main` first unless user confirms re-card from current context.
   - **Do not** edit `src/` or implement tasks — card + branch creation only.

3. **Read OpenSpec context**

   Read for the resolved slug:

   - `openspec/changes/<slug>/proposal.md`
   - `openspec/changes/<slug>/tasks.md`
   - `openspec/changes/<slug>/design.md` (if present)

   Also read [PROJECT.md](../../PROJECT.md) for `TITLE_PREFIX`.

4. **Draft ticket-card fields (required before `git ts`)**

   Output exactly per [ticket-card-info.md](../../.lsi/workflows/ticket-card-info.md) — three separate fenced blocks:

   | Field | Rules |
   |-------|-------|
   | **Task type** | `feature`, `bugfix`, `hotfix`, `chore`, or `release` — use **`chore`** for docs/process/OpenSpec-only changes; **`feature`** for worker/runtime work |
   | **Task title** | `TITLE_PREFIX` + imperative title (≤ ~60 chars total) |
   | **Task description** | Context/Goal, Acceptance Criteria (`- [ ]`), Technical Notes — source from OpenSpec artifacts; link `openspec/changes/<slug>/`; note Trello + OpenSpec dual ticketing |

   **Branch slug for `git ts`:** when prompted for short description, use **`<change-slug>` exactly** (kebab-case OpenSpec folder name) so the branch becomes:

   ```text
   {type}/{24-char-trello-id}-<change-slug>
   ```

   Example: `feature/5f1b2c3d4e5f6789012345ab-openspec-git-slash-commands`

5. **Confirm with user**

   Show the three blocks and proposed branch suffix. Ask once to confirm before running `git ts` unless the user already invoked `/lsi:card` with "create now" intent.

6. **Run `git ts`**

   ```bash
   git ts
   ```

   - Feed the prepared type, title, and description when `git ts` prompts interactively.
   - If `git ts` fails (missing `~/.trello_secrets`, hook error), stop and point to [git-trello.md](../../.lsi/workflows/sdlc/git-trello.md) install steps — do not fall back to manual `git checkout -b`.

7. **Verify result**

   ```bash
   git branch --show-current
   ```

   Confirm:

   - Branch matches `feature|bugfix|hotfix|chore/{24-char-id}-<change-slug>`
   - Suffix equals the OpenSpec change slug
   - Not on `main` or `staging`

**Output**

```
## Trello card created

**Change:** <slug>
**Branch:** <type>/<id>-<slug>
**Card fields:** (summary — type, title)

Next: `/opsx:apply` to implement tasks, or `/lsi:senior` if `design.md` exists and change is large.
```

**Guardrails**

- **Only** `/lsi:*` command permitted on **`main`**; all others refuse until on ticket branch.
- **Never** run `/lsi:card` on **`staging`**.
- **Never** use `git checkout -b feature/<slug>` without Trello id — breaks git-trello hooks and Bitbucket pipelines.
- **Never** invent a change slug — use OpenSpec folder name or ask the user.
- For "draft card only" requests (no `/lsi:card`), output blocks per ticket-card-info **without** running `git ts`.
- Prefer `git push -u origin "$(git branch --show-current)"` over `HEAD` if hooks require explicit branch names ([integrations.md](../../.lsi/workflows/integrations.md)).
