# apply-bot-session Specification

## Purpose
Unattended /lsi:apply-bot after Mode A merge: apply, gates, drift checkpoints, Mode B PR.

## Requirements
### Requirement: Apply bot command

The LSI agent stack SHALL provide `/lsi:apply-bot <slug> [--mode-a <PR>] [--resume]` that implements an OpenSpec change after its Mode A PR is merged and opens the Mode B PR. It SHALL be runnable on Cursor, Claude Code, and OpenCode, and its command text SHALL be written so that a local model following it step by step can complete it (explicit steps, re-read the command file each step, deterministic gates).

#### Scenario: Runs on OpenCode opt-in adopter

- **WHEN** an adopter with `agents_opencode.enabled: true` is adopted
- **THEN** `.opencode/commands/lsi-apply-bot.md` contains the full command body

### Requirement: Preconditions

The command SHALL refuse unless: `PR_HOST` is Bitbucket; the Mode A PR (given or discovered from the change's branch) is `MERGED` into `PR_TARGET_BRANCH`; `origin/<PR_TARGET_BRANCH>` contains `openspec/changes/<slug>/`; the current branch is the ticket branch for `<slug>` with `PR_TARGET_BRANCH` merged in; the working tree is clean; `.reviews/` is ignored; and `lsi-bitbucket whoami` reports a bot identity.

#### Scenario: Mode A PR not merged

- **WHEN** the Mode A PR state is `OPEN`
- **THEN** the command refuses with reason `Mode A PR not merged`

#### Scenario: No bot token

- **WHEN** only person credentials are configured
- **THEN** the command refuses before any apply work

### Requirement: Locked decisions snapshot

Before applying, the command SHALL record the Mode A merge SHA and write `.reviews/<ts>_apply_<slug>.lock.md` listing each `design.md` decision and each spec requirement name, with a content hash of every change artifact at that SHA.

#### Scenario: Lock file written

- **WHEN** preconditions pass
- **THEN** the lock file exists before `/opsx:apply` starts and names the merge SHA

### Requirement: Apply and gate loops

The command SHALL run `/opsx:apply` task by task, run `TEST_COMMAND` after each `tasks.md` section when it is set, commit each section through `lsi-bitbucket commit`, then run verify, readiness, and review gates with at most **3** address cycles each, in the order and with the pass conditions defined for `/lsi:pr-bot`.

When `TEST_COMMAND` from `PROJECT.md` is missing, empty, whitespace-only, or the literal `N/A`, the section SHALL NOT fail: the session SHALL post and log `Skipped — TEST_COMMAND unset` and proceed to the section commit. When `TEST_COMMAND` is set, a non-zero exit SHALL fail the section and raise a human checkpoint before continuing.

#### Scenario: Section commit per tasks section

- **WHEN** `tasks.md` has sections 1–4 and all apply cleanly
- **THEN** at least four bot-authored commits exist since the session start SHA

#### Scenario: Unset TEST_COMMAND skips without failing the section

- **WHEN** `PROJECT.md` has no `TEST_COMMAND`, or its value is empty, whitespace-only, or `N/A`
- **THEN** after a section's apply work the session posts `Skipped — TEST_COMMAND unset`
- **AND** the section commit still proceeds
- **AND** the session does not treat the skip as a gate failure

### Requirement: Drift check

After the gates, the command SHALL compare `openspec/changes/<slug>/` with the lock SHA and evaluate the implementation against each locked decision. Any artifact edit or contradiction SHALL be treated as drift.

#### Scenario: Artifact edited during apply

- **WHEN** an address cycle modified `design.md`
- **THEN** drift is reported and a human checkpoint is raised before any PR is created

### Requirement: Human-in-the-loop checkpoints

The command SHALL stop for a human decision when drift is detected, when any gate exhausts its budget, when a finding requires a design revision, or when an address step proposes editing locked artifacts. It SHALL present the options *accept and record the drift*, *revise the implementation*, or *abort*, write the pending decision into the state file, and wait. When no human responds in the session, it SHALL end with `PAUSED — awaiting decision`. It SHALL NOT create the Mode B PR while a decision is pending.

#### Scenario: Paused then resumed

- **WHEN** the session paused on drift and the user later runs `/lsi:apply-bot <slug> --resume` choosing *accept*
- **THEN** the session continues from the recorded step and the accepted drift and rationale appear in the PR body

#### Scenario: Abort leaves no PR

- **WHEN** the human chooses *abort*
- **THEN** no PR is created and the Close Output records `STOPPED — aborted by human`

### Requirement: Resumable state

The command SHALL maintain `.reviews/<ts>_apply_<slug>.state.json` with the current step, cycle counters, SHAs, and any pending decision, updated after every step. `--resume` SHALL continue from the latest state file for `<slug>`.

#### Scenario: Crash recovery

- **WHEN** the agent process exits mid-session and `--resume` is invoked
- **THEN** completed steps are not re-run and cycle counters are preserved

### Requirement: Mode B PR creation

When gates pass (or the human accepts the outcome) and no decision is pending, the command SHALL draft the PR per `/lsi:pr` mode B and `pull-requests.md`, add a `## Locked decisions` section (Mode A PR link, decisions implemented, accepted drift with human rationale), push through `lsi-bitbucket push`, and create the PR to `PR_TARGET_BRANCH` through `lsi-bitbucket create-pr`. It SHALL post the session summary to the new PR.

#### Scenario: PR targets staging

- **WHEN** `PR_TARGET_BRANCH` is `staging`
- **THEN** the created PR's destination is `staging` and its body contains `## Locked decisions`

### Requirement: Bot-lane boundaries kept

The command SHALL NOT run `/lsi:close`, `/lsi:promote`, `/lsi:release-train`, `/opsx:sync`, or `/opsx:archive`, and SHALL NOT edit or push `main` or any `PROTECTED_BRANCHES` branch.

#### Scenario: Close never invoked

- **WHEN** the session completes
- **THEN** the change remains active under `openspec/changes/<slug>/`
