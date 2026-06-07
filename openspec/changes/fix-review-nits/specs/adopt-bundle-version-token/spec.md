## ADDED Requirements

### Requirement: Adopt injects bundle version into overlay tokens

The adopt pipeline SHALL read the bundle root `VERSION` file and include its trimmed value as `BUNDLE_VERSION` in the token map passed to `substitute_tokens` for all overlay and workflow copies during LSI adopt.

#### Scenario: Overlay header resolves on adopt

- **WHEN** `adopt.py` copies `overlays/lsi/docs/workflows/openspec-git-integration.md` containing `v{{BUNDLE_VERSION}}`
- **THEN** the adopted file under `.lsi/workflows/` contains `v` followed by the current bundle `VERSION` value (e.g. `v1.3.0`)

#### Scenario: Token available before copy phase

- **WHEN** `adopt()` runs with a valid patch config
- **THEN** `BUNDLE_VERSION` is present in the tokens dict before `copy_core_bundle`, `copy_overlay`, and `install_agent_stack` execute

### Requirement: Overlay docs use portable bundle version placeholder

LSI overlay workflow docs that cite the upstream bundle version SHALL use `{{BUNDLE_VERSION}}` (or `v{{BUNDLE_VERSION}}` where a `v` prefix is shown) instead of a hardcoded semver literal.

#### Scenario: No stale hardcoded bundle version in overlay source

- **WHEN** maintainers inspect `overlays/lsi/docs/workflows/openspec-git-integration.md` in the bundle repo
- **THEN** the upstream bundle version reference uses `{{BUNDLE_VERSION}}`, not a fixed version like `v1.0.0`

#### Scenario: Placeholders remain in bundle source until adopt

- **WHEN** maintainers read overlay markdown in the bundle repo (not an adopted copy)
- **THEN** `v{{BUNDLE_VERSION}}` appears unreplaced — substitution happens at adopt time; adopters must re-sync to pick up resolved version strings

### Requirement: Dogfood PROJECT.md matches VERSION

The bundle maintainer `PROJECT.md` SHALL record `BUNDLE_VERSION` consistent with the root `VERSION` file after each release bump.

#### Scenario: Placeholder table in sync

- **WHEN** `VERSION` contains `1.3.0`
- **THEN** `PROJECT.md` lists `BUNDLE_VERSION` as `1.3.0` (with note matching VERSION)

### Requirement: Stdlib YAML fallback parses patch lists without dead code

When PyYAML is unavailable, `_load_simple_yaml` SHALL parse list items under patch config keys (e.g. `scope_exclude_globs`) without unreachable or invalid logic.

#### Scenario: Patch config with list keys loads

- **WHEN** `load_config` reads `patches/web.yaml` without PyYAML installed
- **THEN** `scope_exclude_globs` resolves to a list of string entries and `repo` resolves to `web`
