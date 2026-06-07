# Versioning and releases (video-encoder worker)

Worker semver, `CHANGELOG.md`, git tags, and Bitbucket releases for the **deployable Python worker**.

**Related:** [OpenSpec + Git integration](openspec-git-integration.md) · [versioning.md](../sdlc/versioning.md) (post-1.0 product mapping) · [changelog-policy.md](../sdlc/changelog-policy.md) (short reference)

---

## Source of truth

| Artifact | Role |
|----------|------|
| [version.txt](../../version.txt) | Canonical SemVer |
| [CHANGELOG.md](../../CHANGELOG.md) | Human release notes (Keep a Changelog) |
| Git tag `vX.Y.Z` | Release marker on Bitbucket |

Run `scripts/sync-version.sh --check` after bumping `version.txt` (validates `src/__version__.py` when present).

---

## Pre-1.0 SemVer rules (`0.4.x` phase)

While `major === 0`:

| Signal since last tag | Bump |
|-----------------------|------|
| `BREAKING CHANGE:` or `type!:` | **MINOR** (`0.(y+1).0`) |
| `feat(scope):` | **MINOR** |
| `fix(scope):` | **PATCH** |
| `docs`, `chore`, `test`, `refactor`, `ci` only | No automatic bump |

Tag MUST match `version.txt`: `v$(cat version.txt)`.

Existing [CHANGELOG.md](../../CHANGELOG.md) at **0.4.0** is the canonical baseline — **do not replay** full git history.

---

## Post-1.0 product mapping

At V1 ship (`1.0.0`), follow [versioning.md](../sdlc/versioning.md):

| SemVer major | Product phase |
|--------------|---------------|
| `1.x` | V1 Basic |
| `2.x` | V2 Intermediate |
| `3.x` | V3 Advanced |

Breaking contract or behavior → MAJOR; new feature → MINOR; fix/docs → PATCH.

---

## Release scripts

| Script | Purpose |
|--------|---------|
| `scripts/release/infer_version.py` | Propose next semver from commits since last `v*` tag |
| `scripts/release/generate_changelog.py` | Modes: `since-tag`, `unreleased`, `finalize` |
| `scripts/check_version.py` | CI gate — no version regression; CHANGELOG required on bump |

**Examples:**

```bash
uv run python scripts/release/infer_version.py --json
uv run python scripts/release/generate_changelog.py --mode since-tag
uv run python scripts/release/generate_changelog.py --mode unreleased
uv run python scripts/release/generate_changelog.py --mode finalize --finalize 0.5.0
uv run python scripts/check_version.py
scripts/sync-version.sh --check
```

Release script tests live in `tests/test_release_*.py` and `tests/test_check_version.py` — **outside** the 100% `COVERAGE_ROOTS` (`src/`, `dev/`) gate.

---

## `/lsi:*` release commands

Thin wrappers over release scripts plus git steps (user confirms tag push):

| Command | When |
|---------|------|
| `/lsi:version` | On **`main`** — infer bump, update `version.txt` |
| `/lsi:changelog` | On **`main`** — run `generate_changelog.py` with mode flags |
| `/lsi:release` | On **`main`** — annotated tag + push to Bitbucket |
| `/lsi:bootstrap-release` | One-time — tag current `0.4.0` if no tag exists (no history replay) |

---

## Post-bump checklist (on `main`)

1. Update `version.txt`
2. Update `CHANGELOG.md` (`[Unreleased]` or finalized section)
3. `scripts/sync-version.sh --check`
4. Commit: `chore(release): bump to X.Y.Z`
5. `/lsi:release` when ready

---

## Lifecycle placement

```text
Feature: explore → propose → card setup (`/lsi:card`, `/lsi:card-link`, or `/lsi:trello-list` + branch) → apply → commit → readiness → review → PR → merge (staging)
Promotion: /lsi:promote → merge (main) → /lsi:close on main
Release (optional, on main): /lsi:version → /lsi:changelog → /lsi:release
```

Release is **orthogonal** to ticket close. Batch multiple merged changes into one release train.

---

## CI

- **Bitbucket Pipelines:** `uv run python scripts/check_version.py` in the test job
- Worker runtime reads version from `version.txt` via `src/__version__.py` (V1)

---

## Bitbucket tags

```bash
git tag -a "v$(cat version.txt)" -m "Release v$(cat version.txt)"
git push origin "v$(cat version.txt)"
```

Confirm with ops whether Bitbucket **Downloads** or a formal Releases UI is used for worker artifacts.
