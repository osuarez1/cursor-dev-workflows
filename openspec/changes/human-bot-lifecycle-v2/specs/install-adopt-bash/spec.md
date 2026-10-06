## ADDED Requirements

### Requirement: Prompt-less install-adopt script

The bundle SHALL provide `install-adopt.sh` for first-time LSI adoption from an application repo root, analogous to git-trello-tool’s installer: deterministic, flag/env driven, minimal prompts.

#### Scenario: Flag-driven adopt

- **WHEN** an operator runs `install-adopt.sh` with `--bundle <path>`, `--repo-name <name>`, and `--accept-policy-defaults` from the target repo root
- **THEN** the script invokes `snippets/adopt.py` against that target with the matching `patches/<name>.yaml`
- **AND** runs structural verify afterward
- **AND** exits non-zero if adopt or verify fails

#### Scenario: Missing required inputs

- **WHEN** `--bundle` (or `WORKFLOWS_BUNDLE_PATH`) or `--repo-name` is missing and cannot be inferred
- **THEN** the script exits with a clear error and does not invent patch tokens via an interactive agent session

### Requirement: Installer does not invent domain prose

`install-adopt.sh` SHALL NOT generate hallucinated domain overlay content; domain patches remain human-authored under `patches/files/<repo>/`.

#### Scenario: No domain fabrication

- **WHEN** install-adopt completes for a registered repo
- **THEN** overlay domain files come from existing patch files or templates only
- **AND** post-install messaging points to `/lsi:adopt-verify` for accuracy review
