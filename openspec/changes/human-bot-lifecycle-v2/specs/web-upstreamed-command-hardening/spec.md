## ADDED Requirements

### Requirement: Commit command requires explanatory body

The shared `/lsi:commit` command (upstreamed from web hardening) SHALL require an explanatory commit body, include files and body in the commit plan, and SHALL NOT allow subject-only commits or hand-written `Trello-Card:` trailers.

#### Scenario: Commit plan includes body

- **WHEN** `/lsi:commit` presents a commit plan
- **THEN** each entry includes files and a body explaining what changed and why
- **AND** the command refuses to create a subject-only commit

#### Scenario: Scopes stay generic

- **WHEN** `/lsi:commit` documents typical scopes
- **THEN** it refers to the per-repo openspec-git-integration overlay or PROJECT tokens
- **AND** it does not embed a video-encoder-only worker/FFmpeg/S3 scope table in the shared command source

### Requirement: Changelog rewrite rules

The shared `/lsi:changelog` command SHALL treat generator output as draft input and rewrite entries before the user reviews the diff: strip Conventional Commit prefixes, one user-visible bullet per change, collapse duplicates, and fold pure OpenSpec sync/archive noise.

#### Scenario: No type-scope subjects in changelog

- **WHEN** `/lsi:changelog` finishes rewriting `CHANGELOG.md`
- **THEN** finalized bullets do not retain `feat|fix|chore|docs(…):` commit-subject form

### Requirement: Readiness uses PROJECT TEST_COMMAND

The shared `/lsi:readiness` command SHALL run the test gate from `PROJECT.md` `TEST_COMMAND`, allow an explicit docs-only N/A exemption when source roots are untouched, and SHALL NOT draft PR title or body.

#### Scenario: Docs-only exemption

- **WHEN** `/lsi:readiness` runs and the diff does not touch `SOURCE_ROOT` / related test roots
- **THEN** the agent may mark the test gate N/A with an explicit exemption note
- **AND** does not invent another repo’s test command

#### Scenario: Readiness does not draft PR

- **WHEN** `/lsi:readiness` completes
- **THEN** the output is the readiness verdict and checks only
- **AND** the agent does not emit a PR title or body draft

### Requirement: Review does not draft PR

The shared `/lsi:review` command SHALL NOT emit a PR title or body draft. Domain focus areas SHALL come from the repo integration overlay or patch, not a hardcoded worker domain table in the shared command.

#### Scenario: Review stops at findings

- **WHEN** `/lsi:review` completes
- **THEN** the output is the structured recommendation and findings
- **AND** the agent does not emit PR title/body clipboard blocks
