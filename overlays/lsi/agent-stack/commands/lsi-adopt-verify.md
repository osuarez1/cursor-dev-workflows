---
name: /lsi-adopt-verify
id: lsi-adopt-verify
category: Workflow
description: Structural + deep accuracy verification after adopt/update
---

Run structural adopter verification and a deep accuracy review for hallucinated or drifted adopt content.

**Canonical source:** [adopt-and-update.md](../../docs/adopt-and-update.md) · [adopt-new-repo.md](../../docs/adopt-new-repo.md)

**Input:** Optional `--repo-root` (default: cwd). Optional bundle path for scripts.

**Steps**

1. **Structural layer** — run from the bundle (or known path):

   ```bash
   python3 <bundle>/snippets/verify-adopters.py --repo-root .
   python3 <bundle>/snippets/audit-agent-docs.py --repo-root . --fail-on error
   ```

   Report PASS/FAIL for parity, links, and audit.

2. **Deep accuracy layer** — agent checklist (no auto-commit):

   - Compare `PROJECT.md` tokens to repo reality (protected branches, `TEST_COMMAND` presence, `SOURCE_ROOT` / `TEST_ROOT`, remote)
   - Flag unresolved `{{…}}` placeholders
   - Flag wrong-repo domain copy and AGENTS domain claims that contradict the codebase
   - Severity: blocker / major / minor

3. **Stop** after findings — do not chain install, cleanup, or PR commands.

**Output**

```
## Adopt verify: <repo>

**Structural:** PASS | FAIL
**Deep accuracy:** PASS | FINDINGS

### Structural
| Check | Status |
|-------|--------|
| Parity | ✓/✗ |
| Links | ✓/✗ |
| Audit | ✓/✗ |

### Findings
| Severity | Location | Issue | Fix |
|----------|----------|-------|-----|
| (none) | | | |
```

**Output (refuse)**

```
## Refuse: /lsi-adopt-verify

**Reason:** <not an adopter layout | scripts missing>
**Fix:** <one line>
```

**Guardrails**

- Do not auto-commit fixes
- MUST emit the Output skeleton; MUST NOT invent alternate report shapes or append follow-up questions
- No `Next:` footer (D11)
