# Application versioning (SDL)

Product repos use SemVer in `version.txt` or `VERSION` (see [PROJECT.md](../../../PROJECT.md) `VERSION_FILE`).

Release train: `/lsi:version`, `/lsi:changelog`, `/lsi:release` on `main` after promotion.

CI gate: `scripts/check_version.py`.
