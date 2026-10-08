## ADDED Requirements

### Requirement: Bot invocation is scoped explicit authorization

Invoking `/lsi:pr-bot <PR>`, `/lsi:pr-bot-docs <PR>`, or `/lsi:apply-bot <slug>` SHALL count as the user's explicit request to post comments to that one PR (apply-bot: to create and comment on one PR) for that session. With `--fix` or `/lsi:apply-bot`, it SHALL also count as the explicit request to commit, under the bot identity, and push, without force, to that PR's source branch. Invoking `/lsi:pr-bot --local` or `/lsi:pr-bot-docs --local` SHALL authorize writing step outputs under `.reviews/` and emitting them in chat only — it SHALL NOT authorize Bitbucket posts or pushes. `docs/workflows/integrations.md` SHALL document this as a "Bot sessions" exception, and `docs/workflows/common-mistakes.md` SHALL list extending it beyond that scope as a mistake.

#### Scenario: Default rule unchanged elsewhere

- **WHEN** a user runs `/lsi:review` standalone
- **THEN** nothing is posted to the PR host unless the user separately asks

#### Scenario: Authorization does not carry over

- **WHEN** a bot session for PR 42 has finished and the user asks for a review of PR 43 without invoking a bot command
- **THEN** the agent does not post to PR 43

### Requirement: Never-authorized actions

No bot session SHALL approve, unapprove, merge, decline, request changes, force-push, rewrite history, push to a protected branch, post to any other PR or ticket, or edit, delete, or resolve any comment, including its own.

#### Scenario: Command text forbids actions

- **WHEN** the bundle tests scan the three bot command sources
- **THEN** each contains a Guardrails list naming every never-authorized action

### Requirement: Standalone command guardrails reference the exception

`/lsi:senior`, `/lsi:pr`, and every `/lsi:address-*` command SHALL keep their standalone defaults (no remote posting of full analysis, ask before push, commit only when asked), and SHALL each add one guardrail line stating that a bot session's invocation satisfies "user asks" for the scope in this capability.

#### Scenario: Senior posts full report only in bot session

- **WHEN** `/lsi:senior` runs inside `/lsi:pr-bot-docs`
- **THEN** the full report is posted and saved under `.senior-analyses/`
- **AND** when `/lsi:senior` runs standalone it is neither posted nor saved unless the user asks

### Requirement: Redaction

Bot sessions SHALL NOT post or log secrets, tokens, `.env` values, credentials, or internal hostnames or IPs.

#### Scenario: Env value in diff

- **WHEN** a reviewed diff contains a credential-like value
- **THEN** posted findings refer to its location without reproducing the value
