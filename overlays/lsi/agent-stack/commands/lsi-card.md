---
name: /lsi-card
id: lsi-card
category: Workflow
description: Draft Trello card from OpenSpec change and create card + branch via git ts
---

Create a Trello card and ticket-linked branch for the active OpenSpec change using [git-trello-tool](https://github.com/osuarez1/git-trello-tool) **`git ts`**.

**Canonical source:** [ticket-card-info.md](../../docs/workflows/ticket-card-info.md) · [git-trello.md](../../docs/sdlc/git-trello.md) · [`docs/workflows/openspec-git-integration.md`](../../docs/workflows/openspec-git-integration.md) (when present)

**Contrast with `/lsi:card-link`:** Use **`/lsi:card-link`** when work already exists on a branch without a Trello id (e.g. after `/opsx:propose` on a manual branch). **`/lsi:card`** always creates a **new** branch via `git ts`.

**Protected-branch exception:** Card-setup commands **`/lsi:card`**, **`/lsi:trello-list`**, and **`/lsi:trello-branch`** are allowed on **`main`** or **`staging`** only (no `src/` edits). For existing feature branches without a Trello id, use **`/lsi:card-link`** instead.

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

   - **`git ts` MUST run from a protected integration branch** — `main` or `staging` only:
     - On **`main`**: `git pull origin main` first.
     - On **`staging`**: `git pull origin staging` first.
   - **Refuse on other protected branches** (e.g. `master`, `test`) — checkout `main` or `staging` before continuing.
   - If on a feature branch without a card, checkout `main` or `staging` first unless user confirms re-card from current context.
   - **Do not** edit `src/` or implement tasks — card + branch creation only.

3. **Read OpenSpec context**

   Read for the resolved slug:

   - `openspec/changes/<slug>/proposal.md`
   - `openspec/changes/<slug>/tasks.md`
   - `openspec/changes/<slug>/design.md` (if present)

   Also read [PROJECT.md](../../PROJECT.md) for `TITLE_PREFIX`.

4. **Draft ticket-card fields (required before `git ts`)**

   Output exactly per [ticket-card-info.md](../../docs/workflows/ticket-card-info.md) — three separate fenced blocks:

   | Field | Rules |
   |-------|-------|
   | **Task type** | `feature`, `bugfix`, `hotfix`, `chore`, or `release` — use **`chore`** for docs/process/OpenSpec-only changes; **`feature`** for worker/runtime work |
   | **Task title** | `TITLE_PREFIX` + imperative title (≤ ~60 chars total) |
   | **Task description** | Context/Goal, Acceptance Criteria (`- [ ]`), Technical Notes — **only** from OpenSpec artifacts; **redact** secrets and org-only paths before Trello; link `openspec/changes/<slug>/`; note dual ticketing |

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

   - **`git ts` is a local Git alias** (`.git-trello/bin/git-trello start`) — run it exactly as shown. **Do not** run `git-ts`, `which git-ts`, or search for a hyphenated binary ([git-trello.md](../../docs/sdlc/git-trello.md)).
   - Feed the prepared type, title, and description when `git ts` prompts interactively.
   - If `git ts` fails (missing `~/.trello_secrets`, hook error), stop and point to [git-trello.md](../../docs/sdlc/git-trello.md) install steps — do not fall back to manual `git checkout -b`.

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

- **Card-setup commands only** on **`main`** or **`staging`** — `/lsi:card`, `/lsi:trello-list`, `/lsi:trello-branch`; all other `/lsi:*` commands refuse until on ticket branch.
- **Never** use `git checkout -b feature/<slug>` without Trello id — breaks git-trello hooks and Bitbucket pipelines.
- **Never** invent a change slug — use OpenSpec folder name or ask the user.
- For "draft card only" requests (no `/lsi:card`), output blocks per ticket-card-info **without** running `git ts`.
- **Never** use `git-ts` — only **`git ts`** (space-separated Git subcommand via alias).
- Prefer `git push -u origin "$(git branch --show-current)"` over `HEAD` if hooks require explicit branch names ([integrations.md](../../docs/workflows/integrations.md)).
