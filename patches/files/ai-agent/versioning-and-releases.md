# Versioning and releases (ai-agent monorepo)

Application version file: **`VERSION`** at workspace root (not `version.txt`).

| Artifact | Purpose |
|----------|---------|
| [`VERSION`](../../VERSION) | Canonical SemVer |
| [`docs/VERSIONING.md`](../../docs/VERSIONING.md) | Bump policy |
| [`CHANGELOG.md`](../../CHANGELOG.md) | Keep a Changelog |
| [`docs/RELEASES.md`](../../docs/RELEASES.md) | Release checklist |
| [`bin/sync-version`](../../bin/sync-version) | Sync `frontend/package.json` and `backend/pyproject.toml` |

CI: `VERSION_FILE=VERSION python3 scripts/check_version.py`

## Release train (on `main` after promotion)

| Command | Role |
|---------|------|
| `/lsi:version` | Infer bump, update `VERSION` |
| `/lsi:changelog` | Format `CHANGELOG.md` |
| `/lsi:release` | Tag `v$(cat VERSION)` |

**Agents:** do not bump version unless the user explicitly asks (see `.cursor/rules/agent-versioning.mdc`).

After bumping `VERSION`, run `bin/sync-version` and `bin/sync-version --check`.
