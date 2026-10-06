# slash-command-structured-output Specification

## Purpose
TBD - created by archiving change human-bot-lifecycle-v2. Update Purpose after archive.
## Requirements
### Requirement: Every slash command defines a structured Output template

Every `/lsi:*` and `/opsx:*` command source the bundle maintains (under `overlays/lsi/agent-stack/commands/`, mirrored Claude/OpenCode command paths, and bundle-owned `opsx-*` copies) SHALL include an `**Output**` section with a fenced markdown skeleton that agents MUST follow when reporting success. The reference shape is `/opsx:verify`: a stable `##` title with identity placeholders, labeled status lines (e.g. `**Verdict:**`), and named `###` subsections for lists or tables.

#### Scenario: Verify-shaped success response

- **WHEN** an agent completes `/opsx:verify` (or any command with an Output skeleton)
- **THEN** the user-visible response matches the command’s Output fence (filled placeholders)
- **AND** required sections appear in the documented order
- **AND** empty list sections use an explicit `(none)` (or equivalent) rather than omitting a required heading

#### Scenario: Command file documents Output

- **WHEN** a reviewer opens any maintained `lsi-*.md` or `opsx-*.md` command after this change is applied
- **THEN** the file contains `**Output**` (or path-specific `**Output (...)**` variants) followed by at least one fenced skeleton
- **AND** the skeleton does not rely on freeform prose alone for the final report

### Requirement: Output templates omit Next and follow-up steering

Structured Output skeletons SHALL NOT include `Next:` footers, suggested follow-up slash commands, or questions that choose the user’s next workflow step (same policy as single-purpose commands). Sequencing belongs in lifecycle/playbook docs, not in per-command Output.

#### Scenario: Verify Output has no Next

- **WHEN** `/opsx:verify` Output is updated under this change
- **THEN** the fenced skeleton ends after Remaining tasks / Discrepancies (or equivalent)
- **AND** it does not contain `Next: /lsi:readiness` or similar steering

### Requirement: Refuse and early-exit paths stay structured

When a command refuses (wrong branch, missing change, gate failure) or exits early, the agent SHALL emit a short structured block rather than unstructured prose. Prefer either (a) the same Output shell with an explicit fail/refuse verdict field, or (b) a dedicated refuse skeleton documented in that command (`## Refuse: …`, `**Reason:**`, optional `**Fix:**`).

#### Scenario: Wrong-branch refuse

- **WHEN** `/lsi:commit` (or similar) refuses because the branch is `main` or `staging`
- **THEN** the response uses the command’s refuse or fail Output shape
- **AND** it does not ask which command to run next

### Requirement: Multi-path commands document each path’s Output

Commands with distinct success paths (e.g. maintainer vs adopter `/lsi:update`, list-only vs branched `/lsi:trello-list`) SHALL document a separate `**Output (...)**` skeleton per path. `/lsi:help` MAY use per-topic section templates instead of a single global Output; each topic still MUST be a fixed skeleton.

#### Scenario: Update has maintainer and adopter skeletons

- **WHEN** `/lsi:update` completes on an adopter repo
- **THEN** the response matches the adopter Output skeleton
- **AND** when run as bundle maintainer, the response matches the maintainer skeleton

### Requirement: New commands ship with Output at authoring time

Address-*, adopt-verify, adopt-clean, release-train, release-summary, change-summary, and any other commands added by this change SHALL include structured Output skeletons in the first commit that adds the command file.

#### Scenario: Address-senior has Output

- **WHEN** `lsi-address-senior.md` is added
- **THEN** it includes `**Output**` with a fenced success skeleton and a refuse/fail shape if applicable
- **AND** the skeleton has no Next footer

