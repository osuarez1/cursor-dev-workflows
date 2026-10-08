## ADDED Requirements

### Requirement: Adopt writes scoped Claude Code permissions

`snippets/adopt.py` SHALL merge into the adopter's `.claude/settings.json` `permissions.allow` the bundle's bot allowlist: the helper (`Bash(.lsi/bin/lsi-bitbucket:*)`), `openspec`, and read or branch-local git operations (`status`, `diff`, `log`, `add`, `fetch`, `checkout`, `merge`). The merge SHALL be idempotent, SHALL preserve all existing keys and entries, and SHALL NOT add `git push`, `git commit`, `curl`, or unrestricted wildcards. Where the settings schema supports sandbox network allowlisting, `api.bitbucket.org` and `bitbucket.org` SHALL be added.

#### Scenario: Existing settings preserved

- **WHEN** `.claude/settings.json` already has custom `permissions.allow` and `hooks`
- **THEN** after adopt those entries are unchanged and the bot entries are present once

#### Scenario: No push permission

- **WHEN** the merged settings are inspected
- **THEN** no entry permits `git push`, `git commit`, or `curl`

### Requirement: Adopt writes scoped OpenCode permissions when opted in

When `agents_opencode.enabled` is true, adopt SHALL merge equivalent `allow` entries into the adopter's `opencode.json` `permission` configuration with the same constraints. When OpenCode is not opted in, adopt SHALL NOT create or modify `opencode.json`.

#### Scenario: Not opted in

- **WHEN** adopt runs without `agents_opencode`
- **THEN** `opencode.json` is neither created nor modified

### Requirement: Cursor allowlist documented

Because Cursor's auto-run allowlist is user-level, the adopter docs and CHANGELOG Adopter action SHALL document adding `.lsi/bin/lsi-bitbucket` to it, and sandbox network access to `api.bitbucket.org` and `bitbucket.org`.

#### Scenario: Adopter action lists Cursor step

- **WHEN** the release CHANGELOG entry is read
- **THEN** it includes the Cursor auto-run allowlist and network steps
