---
name: /lsi-bootstrap-release
id: lsi-bootstrap-release
category: Workflow
description: Optional baseline tag for current version if no tag exists
---

Optionally tag the current `version.txt` baseline when no `v*` tag exists yet. Does **not** replay full git history into CHANGELOG.

**Canonical source:** [`docs/workflows/versioning-and-releases.md`](../../docs/workflows/versioning-and-releases.md) § Historical bootstrap

**Steps**

0. **Verify branch** — MUST be `main`. On any other branch, emit Refuse and stop.

1. **Verify state**

   ```bash
   git fetch --tags
   git tag --list "v*"
   cat version.txt
   ```

   - Current canonical baseline: **`0.4.0`** in `CHANGELOG.md`
   - If `v0.4.0` (or current `version.txt`) tag already exists, stop and report.

2. **Confirm anchor SHA**

   ```bash
   git log -1 --oneline
   ```

   User confirms SHA for optional baseline tag.

3. **Optional tag (user confirms)**

   Run `/lsi:release` with `--target <sha>` for `v$(cat version.txt)`.

   ```bash
   VERSION=$(cat version.txt)
   git tag -a "v${VERSION}" <sha> -m "Release v${VERSION} (bootstrap)"
   git push origin "v${VERSION}"
   ```

**Output**

```
## Bootstrap complete

**Version:** 0.4.0 (unchanged in version.txt)
**CHANGELOG:** existing [0.4.0] section is canonical — no history replay

Optional: tag v0.4.0 @ <sha> if no tag existed
```

**Output (refuse)**

```
## Refuse: /lsi-bootstrap-release

**Reason:** Must run on main (release-train family).
**Fix:** checkout main; re-run
```

**Guardrails**

- Do **not** replay semver across full git history
- Do **not** bump `version.txt` during bootstrap
- Do **not** run `npm run release:changelog -- --mode bootstrap` — forward-only policy
- User confirms tag push; no `gh release create`
- **`main`-only** — refuse on `staging` and ticket branches
- **Never nest** inside `/lsi:readiness`, `/lsi:review`, `/lsi:pr`, `/lsi:promote`, `/lsi:close`, or bot sessions
- MUST emit the Output skeleton; MUST NOT invent alternate report shapes or append follow-up questions.
- No `Next:` footer (D11).
