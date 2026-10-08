# pr-review-bot-sessions Specification

## Purpose
Unattended Mode A/B/C PR review sessions (/lsi:pr-bot, /lsi:pr-bot-docs) with shared bot-sessions skeleton.

## Requirements
### Requirement: PR review bot commands

The LSI agent stack SHALL provide `/lsi:pr-bot <PR> [--fix]` and `/lsi:pr-bot --local [--fix]` for Mode B (implementation) / Mode C reviews, and `/lsi:pr-bot-docs <PR> [--fix]` and `/lsi:pr-bot-docs --local [--fix]` for Mode A (`openspec/`-only) reviews. Both SHALL follow the shared session skeleton in `overlays/lsi/agent-stack/bot-sessions.md` (Setup → numbered steps → Close) and SHALL declare the nested commands they run as their documented deliverable.

#### Scenario: Missing PR reference without --local

- **WHEN** either command is invoked without a PR number or URL and without `--local`
- **THEN** it emits the refuse Output and posts nothing

#### Scenario: Local mode without PR

- **WHEN** `/lsi:pr-bot --local` or `/lsi:pr-bot-docs --local` runs on a clean ticket branch
- **THEN** the session does not call `lsi-bitbucket post`, `whoami`, or `push`
- **AND** each step body is written under `.reviews/<ts>_local_<kind>_<slug>/` and emitted in full in chat

#### Scenario: PR and --local together refused

- **WHEN** either command is invoked with both a PR reference and `--local`
- **THEN** it emits the refuse Output

#### Scenario: Wrong PR host

- **WHEN** `PR_HOST` in `PROJECT.md` is not `Bitbucket`
- **THEN** the command emits the refuse Output and posts nothing

#### Scenario: Mode mismatch

- **WHEN** `/lsi:pr-bot-docs` targets a PR whose diff touches paths outside `openspec/`, or `/lsi:pr-bot` targets a PR whose diff touches only `openspec/`
- **THEN** the command refuses and names the correct command

### Requirement: Session setup preconditions

Remote Setup SHALL: resolve the PR via `lsi-bitbucket info`; stop unless state is `OPEN`; fetch and check out the PR source branch with fast-forward only; resolve exactly one active OpenSpec change from the branch name; require a clean working tree; require `.reviews/` to be git-ignored; create `SESSION_LOG=.reviews/<YYYYMMDD-HHMMSS>_<review|review-docs>_<change>.md`. Local Setup SHALL: stay on the current ticket branch; resolve the change from the branch suffix; require a clean tree and ignored `.reviews/`; create `SESSION_DIR=.reviews/<YYYYMMDD-HHMMSS>_local_<review|review-docs>_<change>/` and `SESSION_LOG` inside it; skip Bitbucket entirely. The bot SHALL NOT edit `.gitignore`.

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

### Requirement: Readiness on Mode A, B, and C reviews

Every PR review session for Mode **A**, **B**, or **C** SHALL run `/lsi:readiness` (with `/lsi:address-readiness` under `--fix`, at most **3** address cycles). Mode A sessions use `/lsi:pr-bot-docs`; Mode B and Mode C sessions use `/lsi:pr-bot`. Session `PASS` SHALL require readiness verdict `Ready`. If readiness is not `Ready` after its budget, later gates MAY still run with skip reason `bot session: readiness NEEDS HUMAN`.

#### Scenario: Mode A docs session runs readiness

- **WHEN** `/lsi:pr-bot-docs` runs on an `openspec/`-only PR
- **THEN** the session runs `/lsi:readiness` before senior and plan-gap
- **AND** `PASS` requires readiness `Ready`

#### Scenario: Mode C uses implementation review session

- **WHEN** a Mode C (docs+impl under size gates) PR is reviewed unattended
- **THEN** `/lsi:pr-bot` runs (not `/lsi:pr-bot-docs`)
- **AND** the session includes the readiness gate

### Requirement: Mode A senior loop and plan-gap check

`/lsi:pr-bot-docs` SHALL run readiness first (see above), then `/lsi:senior` at the Deep tier, post the **full** senior report each iteration (multi-part when long), save it under `.senior-analyses/`, and with `--fix` loop `/lsi:address-senior` up to **3** cycles until the verdict is `Sound`, or `Acceptable with follow-ups` with every follow-up captured in `tasks.md`. It SHALL then run the plan-gap check: `openspec validate <slug> --strict`; requirement/scenario → task coverage; design decision → spec/task reflection without contradiction; every task names files or areas and has no undefined or forward dependency; test work planned; no administrative apply deliverables (close/sync/archive, promote, release-train family, `/lsi:update`, meta process); proposal capabilities match `specs/` folders. The verdict SHALL be `Plan ready` or `Plan gaps`.

With `--fix`, remediating **Plan gaps** SHALL use `/lsi:address-senior` against the **same single budget of 3 address cycles** as the senior loop. There SHALL be no second or separate budget for plan-gap. Address cycles already spent on senior findings count toward the cap. If gaps remain after the budget is exhausted, the session verdict SHALL be `NEEDS HUMAN` and no further address cycle SHALL run.

#### Scenario: Rethink verdict needs a human

- **WHEN** `/lsi:senior` returns `Rethink`
- **THEN** no address cycle runs and the session verdict is `NEEDS HUMAN`

#### Scenario: Uncovered requirement is a gap

- **WHEN** a spec scenario has no corresponding `tasks.md` item
- **THEN** the plan-gap table lists it and the verdict is `Plan gaps`

#### Scenario: Plan-gap shares senior address budget

- **WHEN** `--fix` is set and two address cycles were already used during the senior loop
- **THEN** at most one further `/lsi:address-senior` cycle may run for plan-gap remediation
- **AND** if plan gaps remain after that cycle, the session verdict is `NEEDS HUMAN`

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

Remote sessions: every step, including skipped steps, SHALL be posted through `lsi-bitbucket post --step <label> --log $SESSION_LOG`. Local sessions: every step SHALL be written to `$SESSION_DIR/NN_<label>.md` and emitted in full in chat, with outcomes appended to `$SESSION_LOG`, and SHALL NOT call `lsi-bitbucket post`. The session log SHALL also record commands run, decisions taken, and their one-line outcomes, with secrets redacted. Close SHALL emit the final verdict (`PASS`, `NEEDS HUMAN`, or `STOPPED — <reason>`), a step table (ran or skipped, outcome), commits since `START_SHA`, remaining open items, duration, and the log path (remote: post Close; local: Close file + chat), and SHALL run after any STOP.

#### Scenario: Stop still closes

- **WHEN** a STOP condition occurs at any step
- **THEN** the Close comment is posted with `STOPPED — <reason>`
- **AND** the log path is printed in chat
