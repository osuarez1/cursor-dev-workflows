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

**OpenSpec required** for `/lsi:card-link`, `/lsi:trello-branch`, and `/lsi:trello-list` (confirm path): an in-progress change with `proposal.md` must exist. Card description is built from OpenSpec artifacts and **redacted** (no secrets, credentials, org-only paths) before Trello create/update. Full routing: [openspec-git-integration.md](openspec-git-integration.md).

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

**Agent rules (standalone):**

- Never call PR or ticket APIs unless the user explicitly asks.
- Support `--dry-run` for routing checks without network.
- Long bodies: prefer the adopt-managed helper (multi-part split) over silent truncation.

### Bot sessions (authorization exception)

Invoking **`/lsi:pr-bot <PR>`**, **`/lsi:pr-bot-docs <PR>`**, or **`/lsi:apply-bot <slug>`** is the user's explicit request to:

- Post comments to **that one PR** for **that session** (apply-bot: create and comment on one Mode B PR).
- With `--fix` / apply-bot: commit under the bot identity and push (no force) to that PR's source branch via `.lsi/bin/lsi-bitbucket`.

Scope does **not** carry to other PRs or later standalone commands. Never authorized: approve, merge, decline, request-changes, force-push, history rewrite, protected-branch push, edit/delete/resolve comments.

Shared skeleton: overlay `agent-stack/bot-sessions.md`. See also [common-mistakes.md](common-mistakes.md).

### Credentials (Bitbucket Cloud — `BB_*`)

File: `${BB_SECRETS_FILE:-~/.bitbucket_secrets}` (`chmod 600`). The helper parses `KEY=value` / `export KEY=value` for `BB_*` keys only (never `source`s the file).

**Prefer a bot access token** (required for `--fix` and `/lsi:apply-bot`):

1. Create a Bitbucket **access token** whose **name** is the bot display name (e.g. `LSI Review Bot`).
2. **Repository** access token when the plan offers it → store as `BB_ACCESS_TOKEN_<WORKSPACE>_<REPO>` (uppercased; non-alnum → `_`).
3. If the plan lacks repository tokens → **workspace** access token → `BB_ACCESS_TOKEN`.
4. Scopes: **Pull requests: Write**; for `--fix` / apply-bot also **Repositories: Write**.
5. Set an expiry; rotate before it lapses.
6. `chmod 600` the secrets file.

**Read-only fallbacks** (posts as the token owner; not bot identity):

- `BB_USERNAME` + `BB_API_TOKEN` (Atlassian API token + account email) — HTTP Basic.
- `BB_USERNAME` + `BB_APP_PASSWORD` — deprecated; helper warns on stderr.

Optional: `BB_BOT_NAME` / `BB_BOT_EMAIL` (commit identity; defaults `LSI Review Bot` / `lsi-review-bot@users.noreply.invalid`). `BB_WORKSPACE` / `BB_REPO_SLUG` override git-remote parsing only.

```bash
# ~/.bitbucket_secrets (chmod 600) — example only
export BB_ACCESS_TOKEN_ACME_WIDGETS="..."   # repo-scoped preferred
# export BB_ACCESS_TOKEN="..."              # workspace token if no repo tokens
export BB_BOT_NAME="LSI Review Bot"
export BB_BOT_EMAIL="lsi-review-bot@users.noreply.invalid"
# Read-only fallback:
# export BB_USERNAME="you@example.com"
# export BB_API_TOKEN="..."
```

**Dependencies:** `bash`, `curl`, `jq`. **Network hosts:** `api.bitbucket.org`, `bitbucket.org` (Cursor auto-run: allowlist `.lsi/bin/lsi-bitbucket`; Claude sandbox: `sandbox.network.allowedDomains` merged by adopt).

GitHub/GitLab: not supported by the helper (`PR_HOST` must be Bitbucket for bot sessions).

## Senior analysis and remote posts

Full senior analysis reports ([senior-analysis.md](senior-analysis.md)) are poor fit for PR comments (length, mermaid). Default: **chat or local file only**. Post a **short executive summary** remotely only when the user asks. **Exception:** `/lsi:pr-bot-docs` posts the full report (multi-part) as part of its deliverable.

## Related

- [code-review.md](code-review.md) — local vs remote review  
- [ticket-card-info.md](ticket-card-info.md)  
- [common-mistakes.md](common-mistakes.md) — auto-posting reviews  

