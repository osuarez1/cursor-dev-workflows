---
name: /lsi-changelog
id: lsi-changelog
category: Workflow
description: Generate or update CHANGELOG.md via release scripts
---

Update root `CHANGELOG.md` from merged PRs, OpenSpec archives, and conventional commits.

**Canonical source:** [`.lsi/workflows/versioning-and-releases.md`](../../.lsi/workflows/versioning-and-releases.md)

**Input:** Mode — `since-tag`, `unreleased`, or flags: `--finalize X.Y.Z`, `--compare`, `--group-by openspec|pr|scope`

**Steps**

1. **Verify branch** — MUST be `main` for release prep.

2. **Run generator**

   ```bash
   # Since last tag
   uv run python scripts/release/generate_changelog.py --mode since-tag

   # Finalize release section
   uv run python scripts/release/generate_changelog.py --mode since-tag --finalize 0.4.1 --compare

   # Append to [Unreleased] after merges
   uv run python scripts/release/generate_changelog.py --mode unreleased --append
   ```

3. **Show diff** — user reviews `CHANGELOG.md` before commit.

**Output**

```
## Changelog updated

**Mode:** since-tag
**File:** CHANGELOG.md

Next: commit with `/lsi:commit` or `/lsi:release` when ready
```

**Guardrails**

- Invoke `scripts/release/generate_changelog.py` — do not duplicate parser logic
- Source priority: PR Changes → merge desc → OpenSpec → grouped commits
- Forward-only — no full git history replay; use `/lsi:bootstrap-release` for optional baseline tag only
- **`main`-only**
