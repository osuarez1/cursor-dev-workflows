# Token registry

Tokens are set in `patches/<repo>.yaml` → `PROJECT.md` by `adopt.py`.

| Token | Purpose |
|-------|---------|
| `REPO_NAME` | Repo identifier in docs |
| `TITLE_PREFIX` | Trello card title prefix |
| `BASE_BRANCH` | Integration base (`main`) |
| `PR_TARGET_BRANCH` | Feature PR target (`staging`) |
| `PROTECTED_BRANCHES` | Comma-separated protected branches |
| `SOURCE_ROOT` | Application source globs |
| `TEST_ROOT` | Test directory |
| `TEST_COMMAND` | CI/local test command |
| `VERSION_FILE` | `version.txt` or `VERSION` |
| `PR_WARN_*` / `PR_MAX_*` | Branch reviewability limits |
| `CANONICAL_DOCS_PATH` | `.lsi/workflows/` |
| `ADOPTION_LAYOUT` | `lsi` |
| `BUNDLE_VERSION` | Adopted cursor-dev-workflows version |

Substitution in overlay templates uses `{{TOKEN}}` syntax.
