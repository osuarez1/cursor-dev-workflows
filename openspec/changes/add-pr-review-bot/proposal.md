## Why

Review and implementation gates (`/lsi:senior`, `/lsi:readiness`, `/lsi:review`, `/opsx:verify` and their `address-*` follow-ups) are run by hand, one command at a time, and their results live only in chat. Adopters want unattended, repeatable sessions that run those gates against a PR, loop on fixes with a bounded budget, and leave an auditable trail on the PR itself — posted under a bot identity, never as the human who started the session. Today the bundle cannot do this: it has no PR API helper, no orchestrating commands, installs no `/lsi:*` commands for Claude Code in adopters, gives OpenCode only pointer stubs, and does not enforce the `.reviews/` gitignore that an unattended commit gate depends on.

## What Changes

- **Add** `/lsi:pr-bot <PR> [--fix]` — unattended review session for a Mode B (implementation) PR: readiness, review (with Prowler), and verify gates, each looping with its `address-*` command (max 3 fix cycles per gate) when `--fix` is set; change summary; QA test plan; close report. Every step is posted to the PR and logged to `.reviews/`.
- **Add** `/lsi:pr-bot-docs <PR> [--fix]` — unattended review session for a Mode A (`openspec/`-only) PR: `/lsi:senior` (Deep) ⇄ `/lsi:address-senior` loop (max 3) plus a deterministic **plan-gap check** that the execution plan (proposal ↔ specs ↔ design ↔ tasks) has no gaps or discrepancies before apply. Posts the **full** senior report.
- **Add** `/lsi:apply-bot <slug>` — after the Mode A PR is merged to `PR_TARGET_BRANCH`: snapshot locked decisions, `/opsx:apply`, verify / readiness / review loops (max 3 each), drift check against locked decisions, then push and create the Mode B PR. Human-in-the-loop checkpoint whenever a revision or drift decision is needed; resumable. Primary target: OpenCode with a local model (also runs on Cursor and Claude Code).
- **Add** `.lsi/bin/lsi-bitbucket` helper (Bitbucket Cloud API client): `info`, `list`, `post` (with multi-part split for long bodies), `create-pr`, `push`, `commit`, all with `--dry-run`. Auth precedence: repository/workspace **access token** (bot identity) → Atlassian API token → app password (deprecated, warns). No approve / merge / decline / edit / delete code paths exist.
- **Add** bot identity: `--fix` commits are authored as the bot and pushed with the access token; `--fix` and `/lsi:apply-bot` refuse without an access token.
- **Add** scoped authorization exception: invoking one of the three bot commands is the explicit request to post (and, with `--fix` / apply-bot, commit and push) for that one PR / change for that session only. `integrations.md`, `common-mistakes.md`, `/lsi:senior`, `/lsi:pr`, and `address-*` guardrails reference it without weakening their defaults.
- **Add** to `adopt.py`: managed `.gitignore` block (`.reviews/`, `.senior-analyses/`); `.lsi/bin/` install with executable mode; agent permission settings (Claude Code `.claude/settings.json`, OpenCode `opencode.json`) merged idempotently and scoped to the helper.
- **Add** Claude Code adopter emit: `.claude/commands/lsi/<name>.md` (`/lsi:<name>`) for every `lsi-*` command.
- **Change** OpenCode opt-in emit from pointer stubs to full command bodies under `.opencode/commands/`.
- **Change** credential docs to one variable scheme (`BB_*`), including how to create a bot access token; align `/lsi:address-prowler`.
- **Update** routing (`which-workflow.md`, overlay router, README, `code-review.md`, `bot-lane.md`, `openspec-git-integration.md`), `/lsi:help`, expected agent stack, verify-adopters, tests, CHANGELOG, VERSION (MINOR → 2.1.0).

## Capabilities

### New Capabilities

- `pr-bot-bitbucket-helper`: `.lsi/bin/lsi-bitbucket` API client — subcommands, auth precedence, bot identity, dry-run/fixture mode, truncation/splitting, forbidden operations.
- `pr-review-bot-sessions`: `/lsi:pr-bot` and `/lsi:pr-bot-docs` — session setup, step tables, `--fix` semantics, loop budgets, commit gate, posting, session log, close report, plan-gap check.
- `apply-bot-session`: `/lsi:apply-bot` — preconditions, locked-decision snapshot, apply + gate loops, drift check, human-in-the-loop checkpoints, resume, Mode B PR creation.
- `bot-posting-authorization`: scoped exception to the "never post / commit / push unless asked" rules for an explicit bot invocation; what is never authorized.
- `adopt-local-artifacts-gitignore`: adopt-managed `.gitignore` marker block and the bot's ignore preconditions.
- `adopt-agent-permissions`: adopt writes scoped Claude Code and OpenCode permission settings for the helper.
- `claude-code-adopter-commands`: adopt emits `/lsi:*` Claude Code commands in adopters.

### Modified Capabilities

- `opencode-agent-support`: opted-in emit installs full command bodies (not pointer stubs) under `.opencode/commands/`; `.lsi/bin/` API helpers are not "workflow bin wrappers".
- `address-findings-commands`: address commands commit when run inside a bot session with `--fix` / apply-bot; standalone default unchanged.
- `human-bot-openspec-lifecycle`: lifecycle documents the three bot sessions at Mode A review, bot lane apply, and Mode B review.

## Impact

- **Bundle:** `overlays/lsi/agent-stack/commands/` (3 new, edits to `lsi-senior`, `lsi-pr`, `lsi-address-*`, `lsi-help`), `overlays/lsi/agent-stack/bot-lane.md`, new `overlays/lsi/snippets/bin/lsi-bitbucket`, `snippets/adopt.py`, `snippets/install-maintainer-local.py` (shared Claude transform), `snippets/expected_agent_stack.py`, `snippets/verify-adopters.py`, `snippets/gitignore-local-artifacts.txt`, tests, `docs/workflows/{integrations,common-mistakes,code-review}.md`, `which-workflow.md`, overlay router + `openspec-git-integration.md`, `README.md`, `patches/README.md`, `CHANGELOG.md`, `VERSION`.
- **Adopters:** `/lsi:update` required. New files: `.lsi/bin/lsi-bitbucket`, `.claude/commands/lsi/*`, managed `.gitignore` block, permission entries in `.claude/settings.json` (and `opencode.json` when opted in). New local prerequisites: `bash`, `curl`, `jq`; `~/.bitbucket_secrets` with a bot access token; network access to `api.bitbucket.org` and `bitbucket.org`; Cursor auto-run allowlist for the helper (user-level, documented only).
- **Out of scope:** GitHub / GitLab hosts (commands refuse unless `PR_HOST` is Bitbucket); approving, merging, declining, or resolving PR comments; application code in adopter repos.
