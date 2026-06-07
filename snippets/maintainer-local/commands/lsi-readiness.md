---
name: /lsi-readiness
id: lsi-readiness
category: Workflow
description: PR production readiness with pytest coverage gate
---

Run PR production readiness checks for the active OpenSpec change before opening or merging a PR.

**Canonical source:** [pr-production-readiness.md](../../.lsi/workflows/pr-production-readiness.md) · [`.lsi/workflows/openspec-git-integration.md` § PR production readiness](../../.lsi/workflows/openspec-git-integration.md#pr-production-readiness)

**Input:** Optionally specify change slug. Use **promotion mode** when invoked from `/lsi:promote` or when the PR target is **`main`**.

**Modes**

| Mode | When | Diff base | PR target | Branch |
|------|------|-----------|-----------|--------|
| **Feature** (default) | `/lsi:pr`, first PR | `staging` | `staging` | Ticket branch only; refuse `main` or `staging` |
| **Promotion** | `/lsi:promote`, production PR | `main` (`BASE_BRANCH`) | `main` | Ticket branch or **`staging`**; refuse `main` |

In **promotion mode**, substitute `main` for `staging` in all diff/log commands below. On **`staging`** branch, skip ticket/Trello branch-pattern checks; confirm staging QA passed instead.

**Steps**

1. **Resolve change** — announce slug and mode (feature or promotion).

2. **Branch and ticket checks**

   | Check | Pass criteria (feature) | Pass criteria (promotion) |
   |-------|-------------------------|---------------------------|
   | Branch | Ticket pattern; not `main` or `staging` | Ticket branch or **`staging`**; not `main` |
   | Ticket | Suffix matches `openspec/changes/<slug>/` | Same when on ticket branch; N/A on `staging` |
   | Trello id | 24-char id in branch name | Same when on ticket branch; N/A on `staging` |
   | Secrets | No `.env`, credentials, `key.bin`, or keys in diff | Same |

3. **Run CI gates locally (required)**

   ```bash
   uv run pytest --cov=src --cov=dev --cov-fail-under=100
   ```

   - Fix failures before reporting `Ready`.
   - Docs-only changes: still run pytest if `src/` changed; document exemption in output only if user explicitly confirms and CI would not apply.
   - Release script tests (`tests/test_release_*.py`, `tests/test_check_version.py`) run separately — outside the 100% `COVERAGE_ROOTS` (`src/`, `dev/`) gate.

4. **Review diff scope**

   Feature mode:

   ```bash
   git diff staging...HEAD --stat
   ```

   Promotion mode:

   ```bash
   git diff main...HEAD --stat
   ```

   Read `proposal.md`, `design.md`, `tasks.md` — confirm implementation matches ticket.

5. **PR metadata preview**

   - Title: Conventional Commits — primary theme of change
   - Body sections: Overview, Changes, Potential risks, Testing, Related
   - Related: `openspec/changes/<slug>/proposal.md` + Trello card id/URL
   - PR target: **`staging`** (feature) or **`main`** (promotion)
   - Promotion: note staging QA passed; call out if diff is a cumulative staging catch-up

6. **Verdict**

   Output exactly one of: **`Ready`** | **`Needs fixes`** | **`Blocked`**

**Output**

```
## PR Production Readiness: <slug>

**Verdict:** <Ready|Needs fixes|Blocked>

### Checks
| Check | Status |
|-------|--------|
| Branch | ✓/✗ |
| Ticket match | ✓/✗ |
| Trello id in branch | ✓/✗ |
| uv run pytest --cov=src --cov=dev --cov-fail-under=100 | ✓/✗ |
| Secrets scan | ✓/✗ |

### Issues (if any)
- ...

### Next
- Ready → `/lsi:review`
- Needs fixes → address items, re-run readiness
- Blocked → explain blocker
```

**Guardrails**

- Do not report `Ready` if pytest coverage gate failed locally.
- Never post readiness report to Bitbucket unless user asks.
- Feature mode: refuse on `main` or `staging`.
- Promotion mode: refuse on `main` only; **`staging`** branch is allowed.
