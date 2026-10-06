# slash-command-single-purpose Specification

## Purpose
TBD - created by archiving change human-bot-lifecycle-v2. Update Purpose after archive.
## Requirements
### Requirement: Slash commands do not steer next steps

LSI and OpenSpec slash commands SHALL complete their defined deliverable and SHALL NOT emit “Next:” footers, suggested follow-up slash commands, or questions whose purpose is to choose the user’s next workflow step.

#### Scenario: Command output has no Next footer

- **WHEN** an agent finishes `/lsi:commit`, `/opsx:verify`, `/lsi:readiness`, `/lsi:review`, `/lsi:senior`, `/lsi:close`, `/lsi:merge-desc`, or `/lsi:update`
- **THEN** the response contains the command’s required output only
- **AND** the response does not include a `Next:` section or equivalent steering to another slash command

#### Scenario: Help next topic remains allowed

- **WHEN** a user invokes `/lsi:help next` or `/lsi:help status`
- **THEN** suggesting a command is allowed because that is the topic’s defined deliverable

### Requirement: Nested commands only when part of defined deliverable

A slash command SHALL execute another slash command only when that nested command is an explicit part of the invoking command’s defined deliverable. Opportunistic chaining outside the documented deliverable is forbidden.

#### Scenario: PR does not run readiness review or verify

- **WHEN** a user invokes `/lsi:pr`
- **THEN** the agent drafts (and optionally pushes/creates) the pull request per mode A/B/C
- **AND** the agent does not run `/lsi:readiness`, `/lsi:review`, or `/opsx:verify` as part of `/lsi:pr`

#### Scenario: Review may chain Prowler as defined deliverable

- **WHEN** a user invokes `/lsi:review` and a matching Prowler · Grok Bot review comment exists on the open PR
- **THEN** the agent MAY run `/lsi:address-prowler` before the review findings as documented for `/lsi:review`
- **AND** the response still has no Next footer

#### Scenario: Verify stops after verdict

- **WHEN** a user invokes `/opsx:verify`
- **THEN** the agent reports tasks progress, diff scope, and verdict
- **AND** the agent does not ask what the user wants to do next or recommend `/lsi:readiness` / `/lsi:pr`

### Requirement: Command sources document single-purpose guardrails

Each updated `/lsi:*` command source under `overlays/lsi/agent-stack/commands/` SHALL state in Guardrails that the command must not emit Next steering and must not chain slash commands outside its documented deliverable. Structured success/refuse report shapes are specified by the sibling capability `slash-command-structured-output`.

#### Scenario: Guardrail present on PR command

- **WHEN** a reviewer reads `lsi-pr.md` after this change is applied
- **THEN** the Guardrails section forbids running readiness, review, or verify inside `/lsi:pr`
- **AND** forbids a Next footer that steers to promote/close/other commands

