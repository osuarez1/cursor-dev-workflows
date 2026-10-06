# Versioning and releases (recurly_wp_plugin)

Version file: `version.txt` at repo root (`VERSION_FILE` in patch YAML). Keep the WordPress plugin header `Version:` in `wp-lsi-recurly.php` (and any `PLUGIN_*_VERSION` defines) aligned when releasing.

Release train on `main` after promotion: `/lsi:version`, `/lsi:changelog`, `/lsi:release`.

Note: Bitbucket default branch is currently `master`; protect `master` until `main`/`staging` are the delivery train.

CI: adopt installs `scripts/check_version.py` but does not edit pipelines. Copy from `docs/ci/check_version-web.yml` in the cursor-dev-workflows bundle when adding Bitbucket pipelines.
