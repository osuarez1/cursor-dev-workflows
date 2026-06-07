# git-trello-tool Integration

[git-trello-tool](https://github.com/osuarez1/git-trello-tool) links Bitbucket branches to Trello cards. Install per repo; credentials live in `~/.trello_secrets` (not committed).

## Install

From the repository root:

```bash
curl -s https://raw.githubusercontent.com/osuarez1/git-trello-tool/main/install.sh | bash
```

This creates `.git-trello/` (gitignored), local Git aliases, and hooks.

### How commands work (agents)

Commands such as **`git ts`**, **`git tb`**, and **`git tl`** are **local Git aliases** to `.git-trello/bin/git-trello` — not standalone binaries on `PATH`.

| Do | Don't |
|----|-------|
| Run `git ts` | Run `git-ts`, `which git-ts`, or probe for a hyphenated executable |
| Verify install: `git config --local --get alias.ts` | Assume a `git-*` binary like `git-lfs` exists for Trello Start |

**Prerequisites:** `git`, `curl`, `jq`. Trello API key and token from [trello.com/app-key](https://trello.com/app-key).

### Local credentials (`~/.trello_secrets`)

```bash
export API_KEY="your_trello_api_key"
export TOKEN="your_trello_token"
export TARGET_BOARD_ID="your_board_id"
export TARGET_LIST_ID="your_todo_list_id"
export TARGET_DOING_LIST_ID="your_doing_list_id"
```

`TARGET_LIST_ID` / `TARGET_DOING_LIST_ID` are for `git td` / `git tt` (To Do / Doing). Pipeline list IDs are separate (below).

### Optional: commit footer for CI merge detection

Merge pipelines read the latest commit message for a 24-character card ID:

```bash
git config git-trello.injectCommitCard true
```

Appends a `Trello-Card:` line to each commit message.

## Card descriptions (assistants)

When drafting a card description for a milestone or OpenSpec phase, follow [docs/workflows/ticket-card-info.md](../workflows/ticket-card-info.md) (**Task type / Task title / Task description (copy below)** blocks). Source scope from `openspec/changes/*/tasks.md`, `docs/roadmap/milestones-v1.md`, and `docs/contracts/` when relevant.

## Workflow

| Command | Use |
|---------|-----|
| `git ts` | New Trello card + branch (from `main`/`staging`) |
| `/lsi:card-link` | New card + rename **current** branch (see agent command) |
| `git tl` | List To Do cards — agent: **`/lsi:trello-list`** (interactive picker → confirm → `git tb`) |
| `git tb <card_id>` | Branch from existing card — agent: **`/lsi:trello-branch`** |
| `git tc "message"` | Comment on card (includes Bitbucket branch link) |
| `git td` / `git tt` | Move card to Doing / To Do |
| `git tl` | List cards in To Do |

## Branch naming

- Remote MUST be Bitbucket (SSH or HTTPS).
- Pattern: `<type>/<24-char-trello-id>-short-description`
- Types: `feature`, `bugfix`, `hotfix`, `chore`, or `release` (from `git ts` / `git tb`).
- Pre-push hook blocks pushes without a valid 24-character Trello ID on feature branches (tag pushes are exempt).

Example: `feature/5f1b2c3d4e5f6789012345ab-add-hls-pipeline`

### Link card to an existing branch

When `/opsx:propose` or early work started on `{type}/<change-slug>` **without** a Trello id:

1. Stay on the feature branch (not `main`/`staging`).
2. Run **`/lsi:card-link`** — creates the Trello card via API, then `git branch -m` to `{type}/{id}-<change-slug>`.
3. Do **not** run `git ts` — it checks out a new branch and leaves the old one behind.

OpenSpec change slug must match the branch suffix after rename.

### Card description from OpenSpec (required)

**`/lsi:card-link`**, **`/lsi:trello-branch`**, and **`/lsi:trello-list`** (confirm path) require an **open in-progress OpenSpec change**. Card title and body are drafted from `proposal.md` / `tasks.md` / `design.md`, **redacted** (no secrets, credentials, or org-only paths), then written to Trello via API before branch creation or `git tb`.

## Bitbucket Pipelines (Trello sync)

Configured in [`bitbucket-pipelines.yml`](../../../bitbucket-pipelines.yml). Default branch is **`main`**; integration branch is **`staging`**.

| Trigger | Behavior |
|---------|----------|
| Pull request | Validate branch name; move card to Ready list; comment with PR URL |
| PR → `staging` | Move to `LIST_READY_STAGING` |
| PR → `main` | Move to `LIST_READY_PROD` |
| Push to `staging` | Move to `LIST_DEPLOYED_STAGING` + merge comment |
| Push to `main` | Move to `LIST_DEPLOYED_PROD` + merge comment |

PRs to other targets skip Trello steps (exit 0).

### Repository variables (secured)

Configure under **Repository settings → Pipelines → Repository variables**. Mark secrets as secured; never log values in pipeline output.

| Variable | When used |
|----------|-----------|
| `TRELLO_API_KEY` | All Trello API calls |
| `TRELLO_TOKEN` | All Trello API calls |
| `LIST_READY_STAGING` | PR targets `staging` |
| `LIST_READY_PROD` | PR targets `main` |
| `LIST_DEPLOYED_STAGING` | Merge/push to `staging` |
| `LIST_DEPLOYED_PROD` | Merge/push to `main` |

Discover list IDs (after `API_KEY` and `TOKEN` are set locally):

```bash
source ~/.trello_secrets
curl -s "https://api.trello.com/1/boards/$TARGET_BOARD_ID/lists?fields=name,id&key=$API_KEY&token=$TOKEN" \
  | jq -r '.[] | "List: \(.name)\nID:   \(.id)\n---"'
```

See also [bitbucket.md](../../../docs/sdlc/bitbucket.md) and [deployment/secrets.md](../../../docs/deployment/secrets.md).
