# Versioning and releases (web)

Application version file: `version.txt` at repo root.

Release train runs on `main` after promotion. See `/lsi:version`, `/lsi:changelog`, `/lsi:release`.

CI: `python3 scripts/check_version.py` in the RSpec PR step (`bitbucket-pipelines.yml`). Snippet: `docs/ci/check_version-web.yml` in the bundle.
