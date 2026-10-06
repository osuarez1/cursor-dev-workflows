---
name: /lsi-adopt-clean
id: lsi-adopt-clean
category: Workflow
description: Dry-run or confirm cleanup of adopt-managed LSI artifacts
---

Run or document `cleanup-adopt.sh` so a subsequent `install-adopt.sh` can perform a fresh install.

**Canonical source:** [adopt-new-repo.md](../../docs/adopt-new-repo.md)

**Input:** Optional `--yes` (confirm delete). Optional `--bundle` / `--repo-name` for preserve globs.

**Steps**

1. Prefer the bundle script:

   ```bash
   <bundle>/snippets/cleanup-adopt.sh --bundle <bundle> --repo-name <name>
   # then, after user confirms:
   <bundle>/snippets/cleanup-adopt.sh --bundle <bundle> --repo-name <name> --yes
   ```

2. Dry-run by default — list paths; require explicit confirm / `--yes` before delete.
3. Never delete `PROJECT.md` or application source under `SOURCE_ROOT`.
4. Honor patch `preserve` / `preserve_agent_stack`.
5. **Stop** after cleanup — do not run install-adopt or `/lsi:adopt-verify`.

**Output**

```
## Adopt clean: <repo>

**Mode:** dry-run | deleted
**Paths:** N

### Listed / removed
- ...

### Kept (preserve)
- (none)
```

**Output (refuse)**

```
## Refuse: /lsi-adopt-clean

**Reason:** <user declined confirm>
**Fix:** re-run with --yes when ready
```

**Guardrails**

- Single-purpose: cleanup only
- MUST emit the Output skeleton; MUST NOT invent alternate report shapes or append follow-up questions
- No `Next:` footer (D11)
