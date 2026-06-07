# Integrations (optional)

Optional tooling around [cursor-dev-workflows](../../README.md). **None of this is required** for the core workflows to work.

## Trello and git-trello-tool

[git-trello-tool](https://github.com/osuarez1/git-trello-tool) links branches, commit footers, and Trello comments.

**Agent note:** `git ts`, `git tb`, etc. are **local Git aliases** to `.git-trello/bin/git-trello` — run **`git ts`** (two words). There is no `git-ts` binary; do not run `which git-ts` or similar probes.

| Command | Purpose |
|---------|---------|
| `git ts` | Trello Start — create card and checkout **new** branch (from `main`/`staging`) |
| `/lsi:card-link` | Agent command — create card and rename **current** branch to match OpenSpec slug |
| `git tl` | List To Do cards — agent: **`/lsi:trello-list`** (interactive picker → confirm → `git tb`) |
| `git tb <id>` | Branch from existing card — agent: **`/lsi:trello-branch`** |
| `git tc` | Comment on card (e.g. review summary) |

### LSI agent commands (OpenSpec + Trello)

When the LSI overlay is adopted, agents use slash commands instead of raw CLI for card/branch setup:

| Slash command | Git / API | When |
|---------------|-----------|------|
| `/lsi:card` | `git ts` | New card + branch from `main`/`staging` |
| `/lsi:card-link` | Trello API + `git branch -m` | OpenSpec exists; work already on branch without Trello id |
| `/lsi:trello-list` | `git tl` + picker | List To Do cards; confirm → sync card + `git tb` |
| `/lsi:trello-branch` | Trello PUT + `git tb` | Existing card id from `main`/`staging` |

**OpenSpec required** for `/lsi:card-link`, `/lsi:trello-branch`, and `/lsi:trello-list` (confirm path): an in-progress change with `proposal.md` must exist. Card description is built from OpenSpec artifacts and **redacted** (no secrets, credentials, org-only paths) before Trello create/update. Full routing: [overlays/lsi/docs/workflows/openspec-git-integration.md](../../overlays/lsi/docs/workflows/openspec-git-integration.md).

Card field format for `git ts`: [ticket-card-info.md](ticket-card-info.md).

**Push note:** Some hooks validate the **literal** ref name. Prefer:

```bash
git push -u origin "$(git branch --show-current)"
```

over `git push -u origin HEAD` when the hook does not resolve symbolic refs.

### Credentials

- `~/.trello_secrets` — API key and token ([trello.com/app-key](https://trello.com/app-key))
- Cursor sandbox: allowlist `api.trello.com` if agents run post-commit hooks

## Jira / Linear

Map the three [ticket-card-info.md](ticket-card-info.md) outputs to your tracker:

| Field | Jira / Linear equivalent |
|-------|---------------------------|
| Task type | Issue type + labels |
| Title | Summary (`TITLE_PREFIX` optional) |
| Description | Description (Context, Acceptance Criteria, Technical Notes) |

Branch pattern may use `PROJ-123` instead of a 24-char Trello id. Set `TICKET_ID_PATTERN` accordingly.

## PR comment logging

Pattern used by some teams (e.g. custom `bin/log-review`):

1. User completes [code-review.md](code-review.md) in chat.
2. User explicitly asks to **log** or **record** remotely.
3. Script posts a formatted comment to `PR_HOST` and optionally `TICKET_TOOL`.

**Agent rules:**

- Never call PR or ticket APIs unless the user explicitly asks.
- Support `--dry-run` for routing checks without network.
- Truncate very long comments (~32k) with a clear footer.

### Credentials (example: Bitbucket Cloud)

HTTP Basic: Atlassian account **email** + API **token** (not login password).

```bash
# ~/.bitbucket_secrets (chmod 600) — example only
export BB_USERNAME="you@example.com"
export BB_API_TOKEN="..."
export BB_WORKSPACE="my-workspace"
export BB_REPO_SLUG="my-repo"
```

GitHub/GitLab: use PAT or app tokens per host documentation.

## Senior analysis and remote posts

Full senior analysis reports ([senior-analysis.md](senior-analysis.md)) are poor fit for PR comments (length, mermaid). Default: **chat or local file only**. Post a **short executive summary** remotely only when the user asks.

## Related

- [code-review.md](code-review.md) — local vs remote review  
- [ticket-card-info.md](ticket-card-info.md)  
- [common-mistakes.md](common-mistakes.md) — auto-posting reviews  
