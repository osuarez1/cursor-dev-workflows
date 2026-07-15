# Versioning and releases (stream-api)

Application version file: `version.txt` at repo root.

Release train runs on `main` after promotion from `staging`. See `/lsi:version`, `/lsi:changelog`, `/lsi:release`.

CI: `python3 scripts/check_version.py` on the **PR Validation & Trello Sync** step (`atlassian/default-image` in `bitbucket-pipelines.yml`). Do not add it to the ruby **RSpec + Coverage** step unless that image installs python3. Snippet reference: `docs/ci/check_version-web.yml` in the bundle (same script; different step placement).
