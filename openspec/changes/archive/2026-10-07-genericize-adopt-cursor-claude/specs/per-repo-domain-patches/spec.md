## ADDED Requirements

### Requirement: Per-repo domain patches apply after generic install

Each registered patch in `patches/<repo>.yaml` MAY supply `overlay_files` (e.g. `openspec-git-integration.md`) and `rule_overlays` (cursor rule `.mdc` sources). `snippets/adopt.py` SHALL apply generic bundle install first, then overlay patch files so repo-specific domain replaces or extends the generic baseline.

#### Scenario: Web patch supplies Rails integration doc and rules

- **WHEN** `adopt.py` runs with `patches/web.yaml`
- **THEN** `.lsi/workflows/openspec-git-integration.md` SHALL contain web-specific commit mapping and code review scopes
- **AND** `rule_overlays` SHALL install web-specific `.cursor/rules/*.mdc` content after generic rules

#### Scenario: Ai-agent patch replaces generic integration doc

- **WHEN** `adopt.py` runs with `patches/ai-agent.yaml`
- **THEN** `.lsi/workflows/openspec-git-integration.md` SHALL contain ai-agent-specific domain
- **AND** `command_overlays.lsi-review` SHALL NOT be used (domain moved to integration patch)

#### Scenario: Video-encoder patch supplies worker domain

- **WHEN** `adopt.py` runs with `patches/video-encoder.yaml`
- **THEN** `.lsi/workflows/openspec-git-integration.md` SHALL contain video-encoder-specific scopes and test gates

#### Scenario: rule_overlays documented in patches README

- **WHEN** a maintainer reads `patches/README.md`
- **THEN** `rule_overlays` usage and apply order (after generic install) SHALL be documented
