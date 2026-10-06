---
name: /lsi-changelog
id: lsi-changelog
category: Workflow
description: Generate or update CHANGELOG.md via release scripts
---

Update root `CHANGELOG.md` from merged PRs, OpenSpec archives, and conventional commits.

**Canonical source:** [`docs/workflows/versioning-and-releases.md`](../../docs/workflows/versioning-and-releases.md)

**Input:** Mode — `since-tag`, `unreleased`, or flags: `--finalize X.Y.Z`, `--compare`, `--group-by openspec|pr|scope`

**Steps**

1. **Verify branch** — MUST be `main` for release prep.

2. **Run generator** (path from versioning overlay / PROJECT — default below)

   ```bash
   # Since last tag
   uv run python scripts/release/generate_changelog.py --mode since-tag

   # Finalize release section
   uv run python scripts/release/generate_changelog.py --mode since-tag --finalize 0.4.1 --compare

   # Append to [Unreleased] after merges
   uv run python scripts/release/generate_changelog.py --mode unreleased --append
   ```

3. **Rewrite entries (required)** — Generator output and conventional-commit subjects are **draft inputs**, never final changelog lines.

   - Strip prefixes: `feat|fix|chore|docs|test|ci|refactor|perf|style` and `(scope):`.
   - Write **one detailed bullet per user-visible change** (what changed and why it matters); keep PR numbers when known.
   - Collapse duplicate commit lines into one bullet.
   - Fold pure OpenSpec sync/archive chore into a short “Archived OpenSpec…” Changed item; drop noise that adds no product meaning.
   - Group under `### Added` / `### Fixed` / `### Changed` as the file already uses.
   - **Never leave `type(scope):` commit subjects in `CHANGELOG.md`.**

4. **Show diff** — user reviews `CHANGELOG.md` before commit.

**Output**

```
## Changelog updated

**Mode:** <since-tag|unreleased|finalize>
**File:** CHANGELOG.md
**Rewrite:** applied (no type(scope): subjects left)
```

**Output (refuse)**

```
## Refuse: /lsi-changelog

**Reason:** <not on main | generator failed>
**Fix:** <one line>
```

**Guardrails**

- Invoke `scripts/release/generate_changelog.py` (or the path from the versioning overlay / PROJECT) — do not duplicate parser logic
- Source priority: PR Changes → merge desc → OpenSpec → grouped commits
- Forward-only — no full git history replay; use `/lsi:bootstrap-release` for optional baseline tag only
- **`main`-only**
- Never leave `type(scope):` commit subjects in `CHANGELOG.md`
- MUST emit the Output skeleton; MUST NOT invent alternate report shapes or append follow-up questions.
- No `Next:` footer (D11).
