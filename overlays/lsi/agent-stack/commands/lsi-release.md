---
name: /lsi-release
id: lsi-release
category: Workflow
description: Tag and push release to Bitbucket from CHANGELOG
---

Create annotated git tag and push to Bitbucket after version and changelog are committed.

**Canonical source:** [`docs/workflows/versioning-and-releases.md`](../../docs/workflows/versioning-and-releases.md)

**Input:** Optional `--target <sha>` for retroactive baseline tag (bootstrap).

**Steps**

1. **Verify branch** — MUST be `main`.

2. **Verify artifacts**

   - `version.txt` matches intended release (e.g. `0.4.1`)
   - `scripts/sync-version.sh --check` passes
   - `CHANGELOG.md` contains `## [X.Y.Z]` section for that version
   - Working tree clean for release commit (or user confirms)

3. **Check remote tags**

   ```bash
   git fetch --tags
   git tag --list "v${VERSION}"
   ```

   Fail if tag already exists.

4. **Create tag (user confirms)**

   ```bash
   git tag -a "v${VERSION}" ${TARGET_SHA:-HEAD} -m "Release v${VERSION}"
   git push origin "v${VERSION}"
   ```

5. **Bitbucket release notes (user confirms)**

   Extract notes from CHANGELOG section for version. Instruct user to add release notes in Bitbucket **Downloads / Tags** UI if the team uses formal releases.

   **Do not** run `gh release create` — Bitbucket only.

**Output**

```
## Release published

**Version:** v0.4.1
**Tag:** v0.4.1 @ <sha>
**Remote:** Bitbucket (tag pushed)

Next: confirm Bitbucket release notes if your team uses the Releases/Downloads UI.
```

**Guardrails**

- User MUST confirm tag push
- Never force-push tags
- **`main`-only**
- Squash merge PRs use PR title for squash subject — this command is for merge-commit + annotated tags
