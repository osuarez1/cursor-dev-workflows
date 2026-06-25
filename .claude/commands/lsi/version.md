---
description: Infer semver from commits since last tag and update version.txt
---

Propose and apply the next version bump on `main` using the release script.

**Canonical source:** [`overlays/lsi/docs/workflows/versioning-and-releases.md`](../../overlays/lsi/docs/workflows/versioning-and-releases.md)

**Input:** Optional target version override. User must confirm before writing `version.txt`.

**Steps**

1. **Verify branch** — MUST be `main`. Stop on ticket branches or `staging`.

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

Next: `/lsi:changelog` then commit `chore(release): v0.4.1`
```

**Guardrails**

- Worker product semver in `version.txt` — not separate from CHANGELOG version
- Invoke `scripts/release/infer_version.py` — do not reimplement bump logic inline
- **`main`-only** — refuse on `staging` and ticket branches
