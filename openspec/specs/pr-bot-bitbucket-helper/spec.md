# pr-bot-bitbucket-helper Specification

## Purpose
Bitbucket Cloud API helper for LSI bot sessions (post, commit, push under bot identity).

## Requirements
### Requirement: Helper installed at a stable executable path

The bundle SHALL ship a Bitbucket Cloud API helper sourced from `overlays/lsi/snippets/bin/lsi-bitbucket`, and `snippets/adopt.py` SHALL install it at `.lsi/bin/lsi-bitbucket` with mode `0755`. `.lsi/bin/` SHALL be adopt-managed: wiped and rewritten on every adopt. Adopter-facing docs and the CHANGELOG Adopter action SHALL state that `.lsi/bin/` is not a place for custom tools and that `/lsi:update` replaces its contents.

#### Scenario: Adopt installs executable helper

- **WHEN** `adopt.py` runs against an adopter
- **THEN** `.lsi/bin/lsi-bitbucket` exists and is executable by the owner
- **AND** `verify-adopters.py` fails if the file is missing or not executable

#### Scenario: Stale helper files removed

- **WHEN** `.lsi/bin/` contains a file not shipped by the current bundle
- **THEN** adopt removes it while rewriting `.lsi/bin/`

#### Scenario: Adopter action warns wipe-managed bin

- **WHEN** the release CHANGELOG Adopter action is read
- **THEN** it states that `.lsi/bin/` is wiped on `/lsi:update` and must not hold custom tools

### Requirement: Subcommands

The helper SHALL provide `info`, `list`, `post`, `create-pr`, `push`, `commit`, and `whoami`. `<pr>` arguments SHALL accept a PR number or a Bitbucket PR URL.

#### Scenario: Info returns PR metadata

- **WHEN** `lsi-bitbucket info 42` runs with valid credentials
- **THEN** it prints JSON with `id`, `title`, `state`, `source`, `destination`, `author`, and `url`

#### Scenario: List excludes deleted, resolved, and bot comments on request

- **WHEN** `lsi-bitbucket list 42 --match '^Prowler · Grok Bot review' --exclude-bot` runs
- **THEN** it prints one JSON object per open (not deleted, not resolved) comment whose body matches
- **AND** comments whose body begins with the bot header are omitted
- **AND** all pages are fetched until no `next` link remains

#### Scenario: Create PR

- **WHEN** `lsi-bitbucket create-pr --source feature/x --dest staging --title "feat(x): y" --body-file body.md` runs
- **THEN** a pull request is created and its URL is printed

### Requirement: Repository resolved from git remote

The helper SHALL derive workspace and repo slug from `git remote get-url origin` (SSH or HTTPS forms). `BB_WORKSPACE` and `BB_REPO_SLUG` SHALL only override.

#### Scenario: SSH remote parsed

- **WHEN** origin is `git@bitbucket.org:acme/widgets.git` and no overrides are set
- **THEN** API calls target workspace `acme` and repo `widgets`

#### Scenario: Non-Bitbucket remote refused

- **WHEN** origin host is not `bitbucket.org` and no overrides are set
- **THEN** the helper exits non-zero with a message that only Bitbucket Cloud is supported

### Requirement: Authentication precedence

The helper SHALL read credentials from `${BB_SECRETS_FILE:-~/.bitbucket_secrets}` by parsing `KEY=value` or `export KEY=value` lines for `BB_*` keys only, without executing the file. It SHALL refuse a secrets file readable by group or others. Precedence SHALL be: `BB_ACCESS_TOKEN_<WORKSPACE>_<REPO>` → `BB_ACCESS_TOKEN` (Bearer) → `BB_USERNAME` + `BB_API_TOKEN` (Basic) → `BB_USERNAME` + `BB_APP_PASSWORD` (Basic, with a deprecation warning on stderr).

Credential docs SHALL prefer a repository access token as `BB_ACCESS_TOKEN_<WORKSPACE>_<REPO>`, and SHALL document a workspace access token as `BB_ACCESS_TOKEN` when the Bitbucket plan does not provide repository tokens. Both access-token forms SHALL count as bot identity for `--fix` and `/lsi:apply-bot`. API token and app password SHALL remain read-only fallbacks only.

#### Scenario: Repo-scoped access token preferred

- **WHEN** both `BB_ACCESS_TOKEN_ACME_WIDGETS` and `BB_USERNAME`/`BB_API_TOKEN` are set for `acme/widgets`
- **THEN** requests use `Authorization: Bearer` with the repo-scoped token

#### Scenario: Workspace access token is bot identity

- **WHEN** only `BB_ACCESS_TOKEN` is set (workspace token) and no repo-scoped token is present
- **THEN** requests use `Authorization: Bearer` with that token
- **AND** `whoami` reports bot identity

#### Scenario: App password still works

- **WHEN** only `BB_USERNAME` and `BB_APP_PASSWORD` are set
- **THEN** requests use HTTP Basic and a deprecation warning is printed to stderr

#### Scenario: Secrets file not executed

- **WHEN** the secrets file contains a line that is not a `BB_*` assignment
- **THEN** the line is ignored and never executed

#### Scenario: Whoami reports identity class

- **WHEN** `lsi-bitbucket whoami` runs
- **THEN** it prints the auth method and whether the identity is a bot (access token) or a person

### Requirement: Bot identity for commits and pushes

`commit` SHALL author and commit as `BB_BOT_NAME` / `BB_BOT_EMAIL` (documented defaults). `push` SHALL require an access token, push the current branch over HTTPS with the token supplied via git config environment variables, and SHALL NOT place the token on argv, in `.git/config`, or in a remote URL.

#### Scenario: Push refuses without access token

- **WHEN** `lsi-bitbucket push` runs with only API-token or app-password credentials
- **THEN** it exits non-zero with a fix line pointing to the access-token instructions

#### Scenario: Push refuses protected branch and force

- **WHEN** the current branch is listed in `PROTECTED_BRANCHES` in `PROJECT.md`, HEAD is detached, or any force option is passed
- **THEN** the helper exits non-zero without pushing

#### Scenario: Non-fast-forward rejection surfaces

- **WHEN** the remote rejects the push as non-fast-forward
- **THEN** the helper exits non-zero and does not retry with force

### Requirement: Forbidden operations absent

The helper SHALL issue only `GET` requests for PRs and comments and `POST` requests to the PR comments and PR creation endpoints. It SHALL contain no code paths for approve, unapprove, merge, decline, request-changes, comment edit, comment delete, or comment resolve.

#### Scenario: Static check forbids other verbs

- **WHEN** the bundle test suite scans the helper source
- **THEN** it fails if `PUT`, `DELETE`, `PATCH`, `/approve`, `/merge`, `/decline`, `/request-changes`, or `/resolve` appear

### Requirement: Posting format and long bodies

`post` SHALL prefix the body with the bot header (`**LSI Bot Review**`, overridable via `LSI_BOT_HEADER`) and the step label. Bodies longer than 30 000 characters SHALL be split at `##` heading boundaries into numbered parts, each posted as a separate comment, without dropping content.

#### Scenario: Long report split into parts

- **WHEN** a 70 000-character senior report is posted with `--step "3. Senior"`
- **THEN** three or more comments are posted, labelled `part 1/N` … `part N/N`
- **AND** the concatenated parts contain the full report

### Requirement: Dry-run and fixtures

Every subcommand SHALL accept `--dry-run`, which performs no network calls, requires no credentials, and prints what would be sent. `LSI_BB_FIXTURE_DIR` SHALL make `info` and `list` read JSON fixtures instead of the API.

#### Scenario: Dry-run in CI without secrets

- **WHEN** `lsi-bitbucket post 42 body.md --dry-run` runs with no secrets file
- **THEN** it exits `0` and prints the formatted comment

### Requirement: Session log with redaction

When `--log <file>` is given, the helper SHALL append the step label, timestamp, posted URL(s) (or dry-run marker), and body, and SHALL redact the values of any loaded `BB_*` secret from everything it writes or prints.

#### Scenario: Token never logged

- **WHEN** a body accidentally contains the access token value
- **THEN** the log and the posted comment contain `[REDACTED]` in its place
