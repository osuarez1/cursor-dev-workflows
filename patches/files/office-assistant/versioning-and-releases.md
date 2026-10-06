# Versioning and releases (office-assistant monorepo)

Application version file: **`VERSION`** at workspace root.

| Artifact | Purpose |
|----------|---------|
| [`VERSION`](../../VERSION) | Canonical SemVer |
| [`CHANGELOG.md`](../../CHANGELOG.md) | Keep a Changelog (updated at release) |

CI: `VERSION_FILE=VERSION python3 scripts/check_version.py`

## Release train (on `main` after promotion)

| Command | Role |
|---------|------|
| `/lsi:version` | Infer bump, update `VERSION` |
| `/lsi:changelog` | Format `CHANGELOG.md` |
| `/lsi:release` | Tag `v$(cat VERSION)` |

**Agents:** do not bump version unless the user explicitly asks (see `.cursor/rules/agent-versioning.mdc`).

When tier manifests need sync after a bump, update `frontend/package.json`, `backend/` gem version metadata, and `intelligence/pyproject.toml` in the same release change.
