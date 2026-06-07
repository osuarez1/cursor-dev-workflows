# Versioning and releases (my-repo)

Version file: `version.txt` at repo root (or `VERSION` — set `VERSION_FILE` in patch YAML).

Release train on `main` after promotion: `/lsi:version`, `/lsi:changelog`, `/lsi:release`.

CI: copy snippet from `docs/ci/check_version-web.yml` or `check_version-ai-agent.yml` in the bundle.
