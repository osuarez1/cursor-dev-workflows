# Versioning and releases (search-service)

Version file: `version.txt` at repo root (`VERSION_FILE` in patch YAML).

Release train on `main` after promotion: `/lsi:version`, `/lsi:changelog`, `/lsi:release`.

CI: copy snippet from `docs/ci/check_version-web.yml` in the cursor-dev-workflows bundle into `bitbucket-pipelines.yml` when pipelines are added. Adopt installs `scripts/check_version.py` but does not edit pipelines.
