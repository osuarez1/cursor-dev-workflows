# Integrations (optional)

Optional tooling around [cursor-dev-workflows](../../README.md). **None of this is required** for the core workflows to work.

## Trello and git-trello-tool

[git-trello-tool](https://github.com/osuarez1/git-trello-tool) links branches, commit footers, and Trello comments.

| Command | Purpose |
|---------|---------|
| `git ts` | Trello Start — create/link card and checkout branch |
| `git tl` | List cards with ids |
| `git tb <id>` | Branch from existing card |
| `git tc` | Comment on card (e.g. review summary) |

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
