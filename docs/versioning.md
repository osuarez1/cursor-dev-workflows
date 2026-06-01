# Bundle versioning

Semantic versioning for **cursor-dev-workflows** as a portable workflow bundle (not an application library).

## Version sources

| Artifact | Purpose |
|----------|---------|
| [VERSION](../VERSION) | Current released bundle version (single line) |
| [CHANGELOG.md](../CHANGELOG.md) | Human-readable history and adopter actions |
| Git tags | `vMAJOR.MINOR.PATCH` on `main` (e.g. `v1.0.0`) |

Adopters should record **`BUNDLE_VERSION`** in their `PROJECT.md` (git tag or full commit SHA when syncing).

## When to bump

| Bump | When |
|------|------|
| **MAJOR** | Adopter-breaking: workflow path moves, required PR/review output shape changes, `alwaysApply` rule behavior changes, removed workflow files |
| **MINOR** | New workflow doc, new optional snippet, non-breaking template or example additions |
| **PATCH** | Typos, clarifications, examples that do not change required agent output |

## Releases

1. Accumulate changes under `## [Unreleased]` in [CHANGELOG.md](../CHANGELOG.md).
2. When ready, rename to `## [X.Y.Z] - YYYY-MM-DD`, update [VERSION](../VERSION), commit on `main`.
3. Tag: `git tag -a vX.Y.Z -m "cursor-dev-workflows vX.Y.Z"`.
4. Optional: GitHub Release using the changelog section body.

**Maintainers:** copy [MAINTAINER.md.example](../MAINTAINER.md.example) → gitignored `MAINTAINER.md` for org-specific sync mapping and checklists.

**Agents (release tasks):** read gitignored `AGENTS-LOCAL.md` if present (from [AGENTS-LOCAL.md.example](../AGENTS-LOCAL.md.example)).

## Adopter sync

On copy or re-sync from this bundle:

1. Diff your `CANONICAL_DOCS_PATH` against [docs/workflows/](workflows/) in this bundle.
2. Re-copy [snippets/cursor-rules/](../snippets/cursor-rules/) when paths or `alwaysApply` rules changed.
3. Update `BUNDLE_VERSION` in your `PROJECT.md`.
4. Read the **Adopter action** bullets in the changelog for your target version.
5. Re-run link verification per [adoption-layout.md](adoption-layout.md) before merge.

See [adoption-layout.md](adoption-layout.md) and [adoption-checklist.md](../adoption-checklist.md).
