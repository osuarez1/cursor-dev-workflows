## Context

The LSI lifecycle has three lanes (see `overlays/lsi/docs/workflows/openspec-git-integration.md`): human 1–8 (shape + Mode A docs PR), bot 9–19 (apply + Mode B PR), human 20–24 (QA, close, promote). Gate commands exist (`/lsi:senior`, `/lsi:readiness`, `/lsi:review`, `/opsx:verify`) with `address-*` follow-ups, but each is single-purpose and run by hand; `bot-lane.md` is the only sequencer.

Two draft files (an `lsi-pr-bot.md` command and a `bin/pr-comment` Bitbucket helper) were reviewed during exploration. Findings that shape this design:

- `adopt.py` installs `lsi-*` only to `.cursor/commands/`; adopters get **no** Claude Code `/lsi:*` commands and only OpenCode pointer stubs.
- `adopt.py` copies text with `read_text`/`write_text` (mode lost) and never touches `.gitignore`; `gitignore-local-artifacts.txt` is a manual snippet. Three of five adopters do not ignore `.reviews/`.
- Credential naming is inconsistent (`integrations.md`: `BB_API_TOKEN`; `lsi-address-prowler`: `BITBUCKET_EMAIL`/`BITBUCKET_API_TOKEN`; real-world secrets: `BB_APP_PASSWORD`).
- Policy: never post to PR / ticket APIs, never commit, never push unless the user asks (`AGENTS.md`, `integrations.md`, `common-mistakes.md`, every `address-*`, `/lsi:pr`, `/lsi:senior`).
- `slash-command-single-purpose` permits nested commands only when nesting is the documented deliverable.
- Verdict vocabularies: readiness `Ready | Needs fixes | Blocked`; review `Approve | Approve with nits | Request changes`; verify `Aligned | Partial | Discrepancy`; senior `Sound | Acceptable with follow-ups | Rethink`.

## Goals / Non-Goals

**Goals:**

- Three reusable orchestrating commands covering Mode A review, bot-lane apply, and Mode B review, runnable on Cursor, Claude Code, and OpenCode.
- Auditable: every step posted to the PR under a **bot identity** and logged locally.
- Safe by default: read-only unless `--fix` (or apply-bot); bounded loops; never sweep unrelated files into a PR.
- Every adopter gets the commands, helper, gitignore block, and agent permissions through `adopt.py`.

**Non-Goals:**

- GitHub / GitLab support (refuse when `PR_HOST` ≠ Bitbucket).
- Approving, merging, declining, resolving, editing, or deleting PR comments; force-push; history rewrite.
- Running in CI / pipelines (local agent sessions only).
- Replacing human close / promote / release.

## Decisions

### D1. Three commands, one shared session skeleton

```
/lsi:pr-bot-docs <PR>|--local [--fix]   Mode A  →  readiness ⇄ address-readiness (≤3) → senior ⇄ address-senior (≤3) + plan-gap
/lsi:apply-bot   <slug>                 post Mode A merge → apply → verify/readiness/review loops → Mode B PR
/lsi:pr-bot      <PR>|--local [--fix]   Mode B or C  →  verify/readiness/review loops → summary → QA plan
```

`/lsi:readiness` is required on every Mode **A**, **B**, and **C** review (docs session and implementation/tiny session alike).

**`--local`:** run the same gates on the current ticket branch without a Bitbucket PR — write each step under `.reviews/<ts>_local_<kind>_<slug>/` and print full bodies in chat. No `post` / `whoami` / push. Not available on apply-bot.

Shared skeleton (Setup → numbered steps → Close) is documented once in `overlays/lsi/agent-stack/bot-sessions.md`; each command references it and declares its nested commands as its deliverable (satisfies `slash-command-single-purpose`). Separate commands rather than one mode-detecting command because step tables, refusals, and permissions differ materially; mode mismatch is a refusal, not a branch.

### D2. Gate order and loop budget

Per gate: run → if not passing and fixing is enabled, address → re-run; **max 3 address cycles** (≤ 4 runs). Order for pr-bot and apply-bot (Mode B/C):

```
verify ⇄ address-verify (≤3) → readiness ⇄ address-readiness (≤3) → review ⇄ address-review (≤3)
  → if review cycles changed files: one readiness re-check (no loop)
```

Order for pr-bot-docs (Mode A):

```
readiness ⇄ address-readiness (≤3) → senior ⇄ address-senior (≤3) → plan-gap (shares senior budget)
```

Verify first on B/C because spec gaps drive the most code movement; review last because it is the most expensive and `/lsi:review` requires readiness `Ready` (if readiness is not Ready after its budget, later gates run with the documented skip reason "bot session: readiness NEEDS HUMAN"). `/lsi:review` already auto-chains `/lsi:address-prowler`; no separate Prowler step. Pass conditions: verify `Aligned`; readiness `Ready`; review `Approve` or `Approve with nits` (nits still addressed under `--fix`); senior `Sound`, or `Acceptable with follow-ups` when every follow-up is captured in `tasks.md`; plan-gap `Plan ready`. Exhausted budget → session verdict **NEEDS HUMAN**, continue to summary / close.

### D3. `--fix` and `--local` semantics

| | default | `--fix` |
|---|---|---|
| gates | one run each | loops per D2 |
| `address-*` | `Skipped — --fix not set` | run; their edits committed |
| commit / push (remote) | never | bot identity via helper + push |
| commit / push (`--local`) | never | local commit only; **never push** |
| requires access token | remote: no (warn if not bot); `--local`: no | remote: **yes**; `--local`: no |

| | remote | `--local` |
|---|--------|-----------|
| PR arg | required | omitted |
| Bitbucket | post + optional whoami | none |
| outputs | PR comments + session log | step files + chat + session log |

`/lsi:apply-bot` always fixes (it is an implementation session) and therefore always requires the access token.

### D4. Helper: `.lsi/bin/lsi-bitbucket`

Bash + `curl` + `jq`. Source `overlays/lsi/snippets/bin/lsi-bitbucket`; installed by adopt with mode `0755`; directory `.lsi/bin/` wiped and rewritten each adopt (adopt-managed like `.lsi/workflows/`). **Not a user toolbox** — adopters MUST NOT store custom scripts under `.lsi/bin/`; CHANGELOG Adopter action and adopt docs SHALL warn that every `/lsi:update` replaces the directory contents.

Subcommands: `info <pr>`, `list <pr> [--match <regex>] [--exclude-bot]`, `post <pr> <file> [--step <label>] [--log <file>]`, `create-pr --source <b> --dest <b> --title <t> --body-file <f>`, `push [<branch>]`, `commit -m <subject> [-m <body>]`, `whoami`. Global `--dry-run` (no network, no credential requirement) and `LSI_BB_FIXTURE_DIR` (serve `info`/`list` from JSON files) for tests.

- **Workspace / repo** parsed from `git remote get-url origin` (ssh or https); `BB_WORKSPACE` / `BB_REPO_SLUG` only override. No per-repo values in the secrets file are required.
- **Auth precedence:** `BB_ACCESS_TOKEN_<WORKSPACE>_<REPO>` (uppercased, non-alnum → `_`) → `BB_ACCESS_TOKEN` → `BB_USERNAME`+`BB_API_TOKEN` → `BB_USERNAME`+`BB_APP_PASSWORD` (stderr deprecation warning). Access tokens use `Authorization: Bearer`; others HTTP Basic. `whoami` reports which method and whether it is a bot identity.
- **Access-token availability (decided):** Prefer a **repository** access token stored as `BB_ACCESS_TOKEN_<WS>_<REPO>`. When the Bitbucket plan does not offer repository tokens, use a **workspace** access token as `BB_ACCESS_TOKEN` (still Bearer / bot identity for `--fix` and apply-bot). API token / app password remain read-only fallbacks only. `integrations.md` SHALL document both token forms.
- **Secrets file** `${BB_SECRETS_FILE:-~/.bitbucket_secrets}` is parsed as `export KEY=value` / `KEY=value` lines for an allowlist of `BB_*` keys — not `source`d. Refuse if the file is group/world readable.
- **Allowed HTTP:** `GET` on PR / comments; `POST` to `…/pullrequests/{id}/comments` and `…/pullrequests`. No other verbs or endpoints in the code (asserted by test).
- **Header** `**LSI Bot Review**` (override `LSI_BOT_HEADER`). Bot's own comments are recognised by that header; `list --exclude-bot` drops them (prevents Prowler self-match).
- **Long bodies:** split at `##` heading boundaries into parts ≤ 30 000 chars, each prefixed `_<step> — part i/N_`; never truncate silently (full senior report requirement). Length measured with `LC_ALL=C.UTF-8`.
- **Log:** `--log` appends step label, timestamp, posted URL(s), and body; helper redacts values of loaded `BB_*` secrets from anything it writes.

### D5. Bot identity for commits and pushes

- `commit` runs `git commit` with `GIT_AUTHOR_*`/`GIT_COMMITTER_*` from `BB_BOT_NAME` / `BB_BOT_EMAIL` (defaults `LSI Review Bot` / `lsi-review-bot@users.noreply.invalid`); refuses if nothing staged.
- `push` pushes the current branch to `https://bitbucket.org/<ws>/<repo>.git` using the access token through `GIT_CONFIG_COUNT`/`GIT_CONFIG_KEY_n`/`GIT_CONFIG_VALUE_n` env (`http.extraHeader: Authorization: Bearer …`) — token never on argv, never in `.git/config`, never in remote URL. Refuses: no access token, `PROTECTED_BRANCHES` from `PROJECT.md`, detached HEAD, any force option; non-fast-forward rejection exits non-zero (session STOPs).
- Agents never call `git push` directly in bot sessions; permissions allowlist only the helper.

### D6. Commit gate (the untracked-file trap)

- Setup refuses if `git status --porcelain` is non-empty or `git check-ignore -q .reviews/x` fails (no `.gitignore` edits by the bot).
- Before each step record `git status --porcelain=v1 -z` snapshot; after the step stage only paths that changed relative to that snapshot **and** are not ignored; commit via helper with Conventional Commit subjects derived from the address command's Output table. Pre-existing untracked files are never staged (the tree is clean at start, so any untracked file present is a step output, but the snapshot also guards against files appearing from outside the agent).
- Never stage `.reviews/`, `.senior-analyses/`, `.lsi/`, `.cursor/`, `.claude/`, `.opencode/`, `opencode.json`, `.env*`.

### D7. Authorization model

New section in `integrations.md` "Bot sessions" and one row in `common-mistakes.md`. Invoking `/lsi:pr-bot <PR>`, `/lsi:pr-bot-docs <PR>`, or `/lsi:apply-bot <slug>` is the explicit request to: post comments to that PR (apply-bot: create one PR); with `--fix` / apply-bot, commit and push to that PR's source branch. Scope = that PR / change, that session. Never authorized: other PRs or tickets, approve, merge, decline, force-push, history rewrite, editing / deleting / resolving any comment, protected-branch pushes. Standalone commands keep their defaults; their guardrails gain one line pointing at the bot-session exception.

### D8. Mode A plan-gap check (`pr-bot-docs`)

Deterministic checklist emitted as a table, after the senior loop:

1. `openspec validate <slug> --strict` passes.
2. Every spec requirement / scenario maps to ≥ 1 `tasks.md` item.
3. Every `design.md` decision is reflected in specs or tasks; no task contradicts a decision.
4. Every task names files / areas; no task depends on something undefined or later.
5. Test work planned per `test-requirements.md` / `TEST_COMMAND`.
6. No administrative apply deliverables (close/sync/archive, promote, release-train family, `/lsi:update`, meta process) — `/lsi:readiness` also enforces purpose-only `tasks.md`.
7. Proposal capabilities ↔ `specs/` folders match.

Verdict **Plan ready** | **Plan gaps**. With `--fix`, plan-gap remediation SHALL call `/lsi:address-senior` against the **same single budget of 3 address cycles** already used by the senior loop — there is **no second budget** for plan-gap. Cycles spent fixing senior findings count toward the cap; if the budget is already exhausted when gaps remain, session verdict is **NEEDS HUMAN** (do not start a fresh loop). The full senior report from every iteration is posted (multi-part per D4) and saved to `.senior-analyses/` — the bot invocation is the "user asks" for both.

### D9. Apply-bot: locked decisions, drift, human in the loop

- **Preconditions:** `PR_HOST` = Bitbucket; Mode A PR id given or discovered (`--mode-a <PR>`), state `MERGED` into `PR_TARGET_BRANCH`; `origin/<PR_TARGET_BRANCH>` contains `openspec/changes/<slug>/`; on ticket branch with target merged in; clean tree; access token present.
- **Lock:** record merge SHA; write `.reviews/<ts>_apply_<slug>.lock.md` listing design decisions (D-ids / headings) and requirement names with a hash of each artifact at the merge SHA.
- **`TEST_COMMAND` after each `tasks.md` section:** If `TEST_COMMAND` from `PROJECT.md` is missing, empty, whitespace-only, or the literal `N/A`, the section SHALL **not** fail — post/log `Skipped — TEST_COMMAND unset` and proceed to the section commit. If set, run it; non-zero exit fails the section and raises a human checkpoint (same options as other apply failures).
- **Drift check** after the gate loops: diff `openspec/changes/<slug>/` vs merge SHA, and evaluate implementation against each locked decision. Any artifact edit or contradiction is drift.
- **Checkpoints (human in the loop):** on drift, on any gate exhausting its budget, on `Rethink`-class findings, or when an `address-*` proposes editing locked artifacts. The agent stops, writes the decision prompt into the state file, presents options (accept drift and record it in the PR body / revise implementation / abort), and waits. When no human is attached, the session ends with `PAUSED — awaiting decision`, and `/lsi:apply-bot <slug> --resume` continues from the state file.
- **State file** `.reviews/<ts>_apply_<slug>.state.json`: step pointer, cycle counters, SHAs, pending decision. Local models crash; every step re-reads its command file instead of relying on memory.
- **PR:** `/lsi:pr` mode B draft (title / body per `pull-requests.md`), body adds `## Locked decisions` (link to Mode A PR, decisions implemented, accepted drift with human rationale); helper `push` then `create-pr` to `PR_TARGET_BRANCH`.

### D10. Agent emit

- **Cursor:** unchanged (`.cursor/commands/lsi-*.md`).
- **Claude Code:** `install_claude_commands` logic moves from `install-maintainer-local.py` to a shared module (`snippets/agent_emit.py`) used by both the maintainer installer and `adopt.py`; adopters get `.claude/commands/lsi/<name>.md`. Parity / verify treat `.claude/commands/lsi/` like `.cursor/commands/` (adopt-managed; surplus flagged, not deleted).
- **OpenCode (opt-in):** full bodies to `.opencode/commands/lsi-<name>.md` with frontmatter `description` (and `agent`/`model` left to the adopter); `$ARGUMENTS` placeholder appended to the Input line. `bot-lane.md` / `bot-sessions.md` still emitted into `.opencode/README.md`.
- **Permissions:** merge into `.claude/settings.json` `permissions.allow` the entries `Bash(.lsi/bin/lsi-bitbucket:*)`, `Bash(openspec:*)`, `Bash(git status:*)`, `Bash(git diff:*)`, `Bash(git log:*)`, `Bash(git add:*)`, `Bash(git fetch:*)`, `Bash(git checkout:*)`, `Bash(git merge:*)`; OpenCode `opencode.json` `permission.bash` equivalents set to `allow`. Merge is key-level and idempotent, preserves adopter entries, never adds `git push`, `git commit`, `curl`, or wildcards. Network allowlists for sandboxes (`api.bitbucket.org`, `bitbucket.org`) are written where the agent's settings support them and otherwise documented. Cursor's auto-run allowlist is user-level — documented only.

### D11. `.gitignore` managed block

`adopt.py` upserts:

```
# >>> lsi:local-artifacts (managed by cursor-dev-workflows adopt) >>>
.reviews/
.senior-analyses/
# <<< lsi:local-artifacts <<<
```

Content sourced from `snippets/gitignore-local-artifacts.txt`; idempotent; adopter lines outside the markers untouched; `verify-adopters.py` checks presence.

## Risks / Trade-offs

- [Unattended pushes to a shared branch] → read-only default; `--fix` requires bot token; no force; protected-branch refusal; bounded loops; NEEDS HUMAN exit.
- [Local models drift from command specs] → per-step re-read, deterministic gates (`TEST_COMMAND`, `openspec validate`), state file + resume, human checkpoints.
- [Full senior reports flood PR comments] → multi-part posting, one step label per part; accepted per product decision.
- [Writing agent settings is persistent config in adopter repos] → narrow allowlist, no push / commit / curl entries, idempotent merge, listed in CHANGELOG Adopter action.
- [Access-token plan availability varies] → prefer repo token; workspace token via `BB_ACCESS_TOKEN` when repo tokens unavailable; API token / app password fall back for read-only sessions with a warning; `--fix` / apply-bot refuse without an access token (fix line → token instructions).
- [Custom files under `.lsi/bin/`] → wipe on every adopt; Adopter action warns not to store custom tools there.
- [Bot commits not signed / not attributable to a human] → PR body and session log name the human who started the session (`git config user.name`), without email.
- [`.claude/commands/lsi/` emit collides with adopter custom commands] → parity gate flags, never deletes; `lsi/` subdirectory namespace.

## Migration Plan

1. Land bundle changes; MINOR bump to 2.1.0 with Adopter action notes.
2. Maintainer adopt loop / `/lsi:update` per adopter; `verify-adopters.py` passes.
3. Each adopter creates a bot access token ("LSI Review Bot") — repository-scoped when available, otherwise workspace-scoped as `BB_ACCESS_TOKEN` — and adds it to `~/.bitbucket_secrets` (`chmod 600`).
4. Smoke test per adopter: `.lsi/bin/lsi-bitbucket whoami`, `/lsi:pr-bot <PR>` read-only on a throwaway PR.
5. Adopter action MUST state that `.lsi/bin/` is wipe-managed on `/lsi:update` (do not store custom tools there).

Rollback: revert adopter sync commit; helper and commands are additive.

## Open Questions

- Exact Claude Code settings key for sandbox network allowlisting and OpenCode `permission` schema — confirm against current docs during implementation (tasks 3.1 / 3.2) and amend this design if keys differ from D10.

### Confirmed settings keys (tasks 3.1 / 3.2)

- **Claude Code** (project `.claude/settings.json`): `permissions.allow` (string patterns such as `Bash(.lsi/bin/lsi-bitbucket:*)`); sandbox network allowlist is `sandbox.network.allowedDomains` (not under `permissions`). Adopt merges both. `sandbox.network.strictAllowlist` is user/managed-scope only — not written by adopt.
- **OpenCode** (current docs, v1 shape): `permission.bash` as a map of command patterns → `allow` | `ask` | `deny` (e.g. `".lsi/bin/lsi-bitbucket *": "allow"`). OpenCode v2 uses a `permissions` array with `action: "shell"`; this change targets the v1 `permission.bash` object still documented at opencode.ai/docs/permissions. Adopt only creates/modifies `opencode.json` when `agents_opencode.enabled`.
