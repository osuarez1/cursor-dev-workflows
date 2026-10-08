## 1. Bitbucket helper

- [x] 1.1 Add `overlays/lsi/snippets/bin/lsi-bitbucket` (bash, `set -euo pipefail`, `curl`, `jq`) with subcommands `info`, `list` (`--match`, `--exclude-bot`, pagination), `post` (`--step`, `--log`), `create-pr`, `push`, `commit`, `whoami`, and global `--dry-run`
- [x] 1.2 Parse workspace / repo from `git remote get-url origin` (SSH + HTTPS); `BB_WORKSPACE` / `BB_REPO_SLUG` override; refuse non-`bitbucket.org` hosts
- [x] 1.3 Secrets loader: parse `BB_*` `KEY=value` / `export KEY=value` lines only (no `source`); refuse group/world-readable file; precedence `BB_ACCESS_TOKEN_<WS>_<REPO>` → `BB_ACCESS_TOKEN` (Bearer) → `BB_API_TOKEN` → `BB_APP_PASSWORD` (Basic + deprecation warning)
- [x] 1.4 Bot identity: `commit` uses `BB_BOT_NAME` / `BB_BOT_EMAIL` via `GIT_AUTHOR_*` / `GIT_COMMITTER_*`; `push` requires access token, passes `http.extraHeader` via `GIT_CONFIG_COUNT` env, refuses protected branches (from `PROJECT.md`), detached HEAD, and force flags
- [x] 1.5 Posting: `**LSI Bot Review**` header (`LSI_BOT_HEADER` override), step label, split > 30 000 chars at `##` boundaries into `part i/N` comments, `LC_ALL=C.UTF-8` length measurement
- [x] 1.6 Session log append (`--log`) and redaction of loaded `BB_*` values in all output
- [x] 1.7 `LSI_BB_FIXTURE_DIR` support for `info` / `list`; `--dry-run` requires no credentials and makes no network calls
- [x] 1.8 Add `snippets/fixtures/lsi-bitbucket/` (PR info, paged comments incl. Prowler + bot comments, long report body)

## 2. Adopt: helper, gitignore, shared emit

- [x] 2.1 `adopt.py`: add `install_lsi_bin()` — wipe + rewrite `.lsi/bin/`, `shutil.copy2` + `chmod 0o755`
- [x] 2.2 `adopt.py`: add `merge_gitignore_local_artifacts()` — idempotent `lsi:local-artifacts` marker block from `snippets/gitignore-local-artifacts.txt`; create `.gitignore` if missing; update snippet header comment to say adopt manages it
- [x] 2.3 Extract Claude transform (`_claude_frontmatter`, `_claude_subdir`, command rewrites) from `install-maintainer-local.py` into `snippets/agent_emit.py`; maintainer installer imports it (no output change for the bundle's own `.claude/commands/lsi/`)
- [x] 2.4 `adopt.py`: emit `.claude/commands/lsi/<name>.md` for every `lsi-*` command with adopter link rewriting (one level deeper than `.cursor/commands/`)
- [x] 2.5 `adopt.py`: replace OpenCode pointer stubs with full command bodies at `.opencode/commands/lsi-<name>.md` (frontmatter `description`; `$ARGUMENTS` on Input line); keep `.opencode/README.md` index + bot-lane + bot-sessions
- [x] 2.6 Wire new steps into `adopt()` order (after `install_agent_stack`, before verify)

## 3. Adopt: agent permissions

- [x] 3.1 Confirm current Claude Code `.claude/settings.json` keys for `permissions.allow` and sandbox network allowlist; record in design if they differ
- [x] 3.2 Confirm current OpenCode `opencode.json` `permission` schema for bash patterns
- [x] 3.3 `adopt.py`: idempotent JSON merge of the bot allowlist into `.claude/settings.json` (preserve all existing keys; never add `git push`, `git commit`, `curl`, wildcards)
- [x] 3.4 `adopt.py`: same for `opencode.json` only when `agents_opencode.enabled`; never create it otherwise
- [x] 3.5 Allowlist source of truth as data (e.g. `overlays/lsi/agent-stack/bot-permissions.json`) shared by both merges

## 4. Bot session skeleton and commands

- [x] 4.1 Add `overlays/lsi/agent-stack/bot-sessions.md` — shared Setup (PR resolve, OPEN check, ff-only checkout, change resolution, clean tree, `.reviews/` ignored, `whoami`, session log), commit gate (snapshot / stage-changed-only / never-stage list), push via helper, posting + skipped-step rule, redaction, loop budget (3 address cycles per gate), verdict vocabularies + pass conditions, Close format, STOP handling
- [x] 4.2 Add `overlays/lsi/agent-stack/commands/lsi-pr-bot.md` — Mode B: Setup → verify loop → readiness loop → review loop (Prowler via `/lsi:review`) → readiness re-check → `/lsi:change-summary` → QA test plan → Close; `--fix` table; Output + refuse Output; Guardrails (never-authorized list, nested commands are the deliverable, no Next)
- [x] 4.3 Add `lsi-pr-bot-docs.md` — Mode A: refuse if diff outside `openspec/`; `/lsi:readiness` ⇄ `/lsi:address-readiness` (≤3) before senior; `/lsi:senior` Deep ⇄ `/lsi:address-senior` (≤3); full report posted (multi-part) + saved to `.senior-analyses/`; plan-gap checklist table; verdict `Plan ready` | `Plan gaps`; plan-gap remediation shares the **same** 3-cycle senior address budget (no second budget; exhausted budget + remaining gaps → `NEEDS HUMAN`); `Rethink` → NEEDS HUMAN; `PASS` requires readiness `Ready` + senior pass + Plan ready (Mode A/B/C all run readiness; Mode C via `/lsi:pr-bot`)
- [x] 4.4 Add `lsi-apply-bot.md` — preconditions (Mode A merged, target contains change, ticket branch, clean, bot token); lock file; `/opsx:apply` per section + `TEST_COMMAND` + section commits; when `TEST_COMMAND` is missing/empty/`N/A`, post `Skipped — TEST_COMMAND unset` and still commit the section (do not fail); when set, non-zero → human checkpoint; gate loops; drift check; human checkpoints (accept / revise / abort) with `PAUSED — awaiting decision`; `--resume` from state JSON; `/lsi:pr` mode B draft + `## Locked decisions`; helper `push` + `create-pr`; bot-lane forbidden list; per-step "re-read this file" instruction for local models
- [x] 4.5 Use placeholders only (`BASE_BRANCH`, `PR_TARGET_BRANCH`, `PROTECTED_BRANCHES`, `TEST_COMMAND`, `CANONICAL_DOCS_PATH`); no org names, repo slugs, or machine paths; example URLs as `https://bitbucket.org/<workspace>/<repo>/pull-requests/123`

## 5. Existing command and doc edits

- [x] 5.1 `lsi-senior.md`, `lsi-pr.md`, `lsi-address-{senior,review,verify,readiness,prowler}.md`: add one Guardrail line referencing the bot-session exception; standalone defaults unchanged
- [x] 5.2 `lsi-address-prowler.md`: switch credentials to `BB_*` scheme / helper `list`; exclude bot comments
- [x] 5.3 `lsi-help.md`: add bot sessions to the index and lifecycle topic
- [x] 5.4 `overlays/lsi/agent-stack/bot-lane.md`: reference `/lsi:apply-bot` for 9–18 and the review sessions
- [x] 5.5 `overlays/lsi/docs/workflows/openspec-git-integration.md`: place the three sessions in the Lifecycle lanes; Command syntax section
- [x] 5.6 `docs/workflows/integrations.md`: "Bot sessions" authorization exception; unify credentials on `BB_*`; access-token creation steps (prefer repository token → `BB_ACCESS_TOKEN_<WS>_<REPO>`; if plan lacks repo tokens, workspace token → `BB_ACCESS_TOKEN`; name = bot display name; Pull requests Write; Repositories Write for `--fix` / apply-bot; expiry; `chmod 600`); API token / app password read-only fallback; dependencies `bash`, `curl`, `jq`; network hosts
- [x] 5.7 `docs/workflows/common-mistakes.md`: rows for extending bot authorization beyond its PR/session, calling `git push` directly in bot sessions, committing untracked files outside step output
- [x] 5.8 `docs/workflows/code-review.md`: "Remote / automated review" section linking `/lsi:pr-bot` and the integrations exception
- [x] 5.9 Routing: `which-workflow.md` row + overlap rule; `overlays/lsi/docs/workflows/which-workflow.md` and `overlays/lsi/which-workflow-lsi.md`; `README.md` workflow table row
- [x] 5.10 Dual-copy: `docs/adopt-and-update.md` + `overlays/lsi/adopter-docs/adopt-and-update.md` (new adopt outputs, verify checks, secrets setup)
- [x] 5.11 `patches/README.md`: correct agent-emit paragraph (Claude commands emitted; OpenCode opt-in with full bodies; `.lsi/bin/` allowed)

## 6. Expected stack, verify, tests

- [x] 6.1 `expected_agent_stack.py`: add `lsi-pr-bot`, `lsi-pr-bot-docs`, `lsi-apply-bot`; expected `.lsi/bin/lsi-bitbucket`; Claude command set
- [x] 6.2 `verify-adopters.py`: helper exists + executable; gitignore block present and `git check-ignore` passes; `.claude/commands/lsi/` parity; permissions entries present
- [x] 6.3 `audit-agent-docs.py` parity: treat `.claude/commands/lsi/` like `.cursor/commands/` (flag surplus, never delete)
- [x] 6.4 New `snippets/test_lsi_bitbucket.py`: `shellcheck` (skip with notice if not installed), forbidden-verb/endpoint scan, dry-run without secrets, fixture `info`/`list` (pagination, Prowler match, `--exclude-bot`), multi-part split preserves content, secrets file not executed + permission refusal, redaction, remote parsing, push refusals (protected / detached / force / no token) using a local bare repo
- [x] 6.5 New `snippets/test_adopt_bot_install.py`: helper installed `0755`; stale `.lsi/bin/` files removed; gitignore block idempotent + preserves lines; `.claude/settings.json` merge idempotent + preserves keys + no forbidden entries; `opencode.json` untouched unless opted in; Claude commands emitted; OpenCode full bodies
- [x] 6.6 Update `test_supported_agents_only.py` (allow `.lsi/bin/`, still forbid top-level `bin/`), `test_commands_generic.py` (new commands generic, no org/slug), `test_adopt_command_rule_parity.py`, `test_adopt_links.py` / `test_adoption_verify_links.py` (Claude command links)
- [x] 6.7 Command-text test: each bot command has Output, refuse Output, never-authorized Guardrails, loop budget 3, no `Next:` footer
- [x] 6.8 Run full gate: all `snippets/test_*.py`, `check-workflow-link-sources.py`, `adoption-verify-links.py` on a fixture adopter, `openspec validate add-pr-review-bot --strict`

## 7. Release

- [ ] 7.1 `CHANGELOG.md` `[Unreleased]` → Added / Changed entries and **Adopter action**: run `/lsi:update`; create bot access token (repo-scoped preferred, else workspace as `BB_ACCESS_TOKEN`) + `~/.bitbucket_secrets` (`chmod 600`); install `jq` / `curl`; Cursor auto-run allowlist for `.lsi/bin/lsi-bitbucket`; sandbox network `api.bitbucket.org`, `bitbucket.org`; review new `.gitignore` block and `.claude/settings.json` entries; warn that `.lsi/bin/` is wipe-managed on update (do not store custom tools there); app passwords deprecated — **deferred to `/lsi:release-train`** (not an apply deliverable)
- [ ] 7.2 `VERSION` → `2.1.0` (MINOR) and `PROJECT.md` `BUNDLE_VERSION` at release time — **deferred to `/lsi:release-train`**
- [ ] 7.3 Re-sync registered adopters via maintainer adopt loop; `verify-adopters.py` passes each
- [ ] 7.4 Smoke test on one adopter: `whoami`, `/lsi:pr-bot <PR>` read-only, `/lsi:pr-bot-docs <PR>` on a Mode A PR, `/lsi:apply-bot` with `--dry-run` posting on a throwaway change
