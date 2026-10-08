---
name: /lsi-version
id: lsi-version
category: Workflow
description: Infer semver from commits since last tag and update version.txt
---

Propose and apply the next version bump on `main` using the release script.

**Canonical source:** [`docs/workflows/versioning-and-releases.md`](../../docs/workflows/versioning-and-releases.md)

**Input:** Optional target version override. User must confirm before writing `version.txt`.

**Steps**

1. **Verify branch** — MUST be `main`. On any other branch, emit Refuse and stop — do not write `version.txt` / `VERSION` / `BUNDLE_VERSION`.

2. **Run inference**

   ```bash
   uv run python scripts/release/infer_version.py --json
   ```

3. **Show proposal** — current, proposed, bump type, reason, commit signals since last tag.

4. **Apply (when user confirms)**

   - Update `version.txt` only
   - Run `scripts/sync-version.sh --check` to verify `src/__version__.py` alignment
   - Do not auto-commit unless user invoked `/lsi:commit`

**Output**

```
## Version proposal

**Current:** 0.4.0
**Proposed:** 0.4.1 (patch)
**Reason:** <from infer script>

```

**Output (refuse)**

```
## Refuse: /lsi-version

**Reason:** Must run on main (release-train family).
**Fix:** checkout main after promotion + close; use /lsi:release-train or re-run here
```

**Guardrails**

- Worker product semver in `version.txt` — not separate from CHANGELOG version
- Invoke `scripts/release/infer_version.py` — do not reimplement bump logic inline
- **`main`-only** — refuse on `staging` and ticket branches before any write
- **Never nest** inside `/lsi:readiness`, `/lsi:review`, `/lsi:pr`, `/lsi:promote`, `/lsi:close`, or bot sessions — release-train (or this command alone) owns version bumps
- MUST emit the Output skeleton; MUST NOT invent alternate report shapes or append follow-up questions.
- No `Next:` footer (D11).
