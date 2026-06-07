# Versioning and releases (web)

Application version file: `version.txt` at repo root.

Release train runs on `main` after promotion. See `/lsi:version`, `/lsi:changelog`, `/lsi:release`.

CI: add `scripts/check_version.py` to Bitbucket Pipelines (see `patches/web.yaml` `ci_hook`).
