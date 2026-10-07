## ADDED Requirements

### Requirement: PR review bot commands

The LSI agent stack SHALL provide `/lsi:pr-bot <PR> [--fix]` for Mode B (implementation) PRs and `/lsi:pr-bot-docs <PR> [--fix]` for Mode A (`openspec/`-only) PRs. Both SHALL follow the shared session skeleton in `overlays/lsi/agent-stack/bot-sessions.md` (Setup → numbered steps → Close) and SHALL declare the nested commands they run as their documented deliverable.

#### Scenario: Missing PR reference

- **WHEN** either command is invoked without a PR number or URL
- **THEN** it emits the refuse Output and posts nothing

#### Scenario: Wrong PR host

- **WHEN** `PR_HOST` in `PROJECT.md` is not `Bitbucket`
- **THEN** the command emits the refuse Output and posts nothing

#### Scenario: Mode mismatch

- **WHEN** `/lsi:pr-bot-docs` targets a PR whose diff touches paths outside `openspec/`, or `/lsi:pr-bot` targets a PR whose diff touches only `openspec/`
- **THEN** the command refuses and names the correct command

### Requirement: Session setup preconditions

Setup SHALL: resolve the PR via `lsi-bitbucket info`; stop unless state is `OPEN`; fetch and check out the PR source branch with fast-forward only; resolve exactly one active OpenSpec change from the branch name; require a clean working tree; require `.reviews/` to be git-ignored; create `SESSION_LOG=.reviews/<YYYYMMDD-HHMMSS>_<review|review-docs>_<change>.md`. The bot SHALL NOT edit `.gitignore`.

#### Scenario: Dirty tree stops session

- **WHEN** `git status --porcelain` is non-empty at Setup
- **THEN** the session stops with `STOPPED — working tree not clean` and posts only the Close step

#### Scenario: Reviews directory not ignored

- **WHEN** `.reviews/` is not ignored by git
- **THEN** the session stops with a fix line pointing to `/lsi:update`

#### Scenario: Ambiguous change

- **WHEN** zero or more than one active change matches the branch name
- **THEN** the session stops and posts the Close step with the reason

### Requirement: Read-only default and fix mode

Without `--fix`, sessions SHALL run each gate once, post `address-*` steps as `Skipped — --fix not set`, and SHALL NOT commit or push. With `--fix`, sessions SHALL require a bot access token (`lsi-bitbucket whoami` reports bot) and SHALL commit and push only through the helper.

#### Scenario: Default run makes no commits

- **WHEN** `/lsi:pr-bot 42` completes
- **THEN** `git rev-parse HEAD` equals the Setup `START_SHA`
- **AND** every address step comment reads `Skipped — --fix not set`

#### Scenario: Fix without bot token refused

- **WHEN** `/lsi:pr-bot 42 --fix` runs and `whoami` reports a person identity
- **THEN** the session stops at Setup with a fix line pointing to the access-token instructions

### Requirement: Gate loops with bounded budget

`/lsi:pr-bot` SHALL run gates in the order verify (`/opsx:verify` ⇄ `/lsi:address-verify`), readiness (`/lsi:readiness` ⇄ `/lsi:address-readiness`), review (`/lsi:review` ⇄ `/lsi:address-review`), each with at most **3** address cycles under `--fix`, followed by one readiness re-check without looping if review cycles changed files. Pass conditions SHALL use each command's own verdict vocabulary: verify `Aligned`; readiness `Ready`; review `Approve` or `Approve with nits`. A gate that does not pass within budget SHALL set the session verdict to `NEEDS HUMAN`, and the session SHALL continue to summary and close.

#### Scenario: Readiness passes on second cycle

- **WHEN** readiness returns `Needs fixes`, address-readiness runs, and the re-run returns `Ready`
- **THEN** the readiness gate passes and the session proceeds to review

#### Scenario: Budget exhausted

- **WHEN** review still returns `Request changes` after 3 address cycles
- **THEN** the session verdict is `NEEDS HUMAN`
- **AND** the session still posts the change summary, QA plan, and Close

#### Scenario: Prowler handled inside review

- **WHEN** the PR has an open comment starting with `Prowler · Grok Bot review`
- **THEN** it is handled through `/lsi:review`'s documented Prowler chain, not as a separate session step
- **AND** bot comments are excluded from Prowler matching

### Requirement: Mode B summary and QA plan

After the gates, `/lsi:pr-bot` SHALL post `/lsi:change-summary` output and a QA test plan covering scope and out-of-scope, preconditions and setup, numbered test cases (goal, exact steps, expected outcome), edge and negative cases, regression areas, a `- [ ]` QA checklist, and rollback / known limitations, based on `origin/<destination>...HEAD` and the change artifacts.

#### Scenario: QA plan has checklist per case

- **WHEN** the QA plan lists N numbered test cases
- **THEN** the QA checklist contains at least N `- [ ]` items plus setup and regression items

### Requirement: Mode A senior loop and plan-gap check

`/lsi:pr-bot-docs` SHALL run `/lsi:senior` at the Deep tier, post the **full** senior report each iteration (multi-part when long), save it under `.senior-analyses/`, and with `--fix` loop `/lsi:address-senior` up to **3** cycles until the verdict is `Sound`, or `Acceptable with follow-ups` with every follow-up captured in `tasks.md`. It SHALL then run the plan-gap check: `openspec validate <slug> --strict`; requirement/scenario → task coverage; design decision → spec/task reflection without contradiction; every task names files or areas and has no undefined or forward dependency; test work planned; no sync/archive/close apply deliverables; proposal capabilities match `specs/` folders. The verdict SHALL be `Plan ready` or `Plan gaps`.

#### Scenario: Rethink verdict needs a human

- **WHEN** `/lsi:senior` returns `Rethink`
- **THEN** no address cycle runs and the session verdict is `NEEDS HUMAN`

#### Scenario: Uncovered requirement is a gap

- **WHEN** a spec scenario has no corresponding `tasks.md` item
- **THEN** the plan-gap table lists it and the verdict is `Plan gaps`

#### Scenario: Docs session never edits outside openspec

- **WHEN** `/lsi:pr-bot-docs --fix` commits
- **THEN** every committed path is under `openspec/`

### Requirement: Commit gate stages only step output

Under `--fix`, before each step the session SHALL snapshot `git status`. After the step it SHALL stage only paths that changed relative to the snapshot and are not ignored, SHALL never stage `.reviews/`, `.senior-analyses/`, `.lsi/`, `.cursor/`, `.claude/`, `.opencode/`, `opencode.json`, or `.env*`, and SHALL commit through `lsi-bitbucket commit` with Conventional Commit subjects. After a step creates commits, the session SHALL push through `lsi-bitbucket push`; a rejected push SHALL stop the session.

#### Scenario: Env file never committed

- **WHEN** a step creates `.env.local`
- **THEN** it is not staged and the step comment notes the skipped path

#### Scenario: Push rejected

- **WHEN** `lsi-bitbucket push` exits non-zero
- **THEN** the session stops with `STOPPED — push rejected` and posts Close

### Requirement: Posting, logging, and close

Every step, including skipped steps, SHALL be posted through `lsi-bitbucket post --step <label> --log $SESSION_LOG`. The session log SHALL also record commands run, decisions taken, and their one-line outcomes, with secrets redacted. Close SHALL post the final verdict (`READY`, `NEEDS HUMAN`, or `STOPPED — <reason>`), a step table (ran or skipped, outcome), commits since `START_SHA`, remaining open items, duration, and the log filename, and SHALL run after any STOP.

#### Scenario: Stop still closes

- **WHEN** a STOP condition occurs at any step
- **THEN** the Close comment is posted with `STOPPED — <reason>`
- **AND** `.reviews/.tmp/` is removed and the log path is printed in chat
