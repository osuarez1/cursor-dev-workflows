---
name: /lsi-readiness
id: lsi-readiness
category: Workflow
description: PR production readiness with local TEST_COMMAND gate
---

Run PR production readiness checks for the active OpenSpec change before opening or merging a PR. Required for every Mode **A**, **B**, and **C** review (standalone, `/lsi:pr-bot-docs`, or `/lsi:pr-bot`).

**Canonical source:** [pr-production-readiness.md](../../docs/workflows/pr-production-readiness.md) · [`docs/workflows/openspec-git-integration.md` § PR production readiness](../../docs/workflows/openspec-git-integration.md#pr-production-readiness) · [PROJECT.md](../../PROJECT.md) (`TEST_COMMAND`)

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
   | Secrets | No `.env`, credentials, or key material in diff | Same |

3. **Run CI gates locally (required)**

   Use **`TEST_COMMAND` from [PROJECT.md](../../PROJECT.md)**. Cite the integration doc § PR production readiness for repo-specific notes.

   - Fix failures before reporting `Ready`.
   - Docs-only / OpenSpec-only with no `SOURCE_ROOT` / `TEST_ROOT` changes: document exemption (**N/A**) instead of inventing a suite.
   - Do **not** hardcode adopter test runners in this shared command.

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

5. **Release-train files (required)**

   Version bumps and changelog finalization belong to **`/lsi:release-train`** on **`main`**, not feature or promotion PRs.

   Against the mode’s diff base, fail the check when any of these paths change:

   | Path | Notes |
   |------|--------|
   | `VERSION` | Bundle canonical SemVer (when present) |
   | `version.txt` | Adopter/app canonical SemVer (when present) |
   | `CHANGELOG.md` | Keep a Changelog (including `[Unreleased]` edits) |
   | `PROJECT.md` | Only when the `BUNDLE_VERSION` row changes |

   ```bash
   # Feature example — non-empty → check fails
   git diff staging...HEAD --name-only -- VERSION version.txt CHANGELOG.md
   git diff staging...HEAD -- PROJECT.md | grep -E 'BUNDLE_VERSION' || true
   ```

   - **Pass:** none of the above changed (or `PROJECT.md` changed without `BUNDLE_VERSION`).
   - **Fail:** list the paths; verdict at most **`Needs fixes`** (not `Ready`). Fix: revert those files; leave version/changelog to `/lsi:release-train`.
   - Do **not** treat release-script or tag work on a ticket branch as in-scope for this PR.

6. **Verdict only** — do **not** draft PR title or body (that is `/lsi:pr`).

   Output exactly one of: **`Ready`** | **`Needs fixes`** | **`Blocked`**

**Output**

```
## PR Production Readiness: <slug>

**Verdict:** <Ready|Needs fixes|Blocked>
**Mode:** feature | promotion
**TEST_COMMAND:** <from PROJECT.md or N/A docs-only>

### Checks
| Check | Status |
|-------|--------|
| Branch | ✓/✗ |
| Ticket match | ✓/✗ |
| Trello id in branch | ✓/✗ |
| TEST_COMMAND | ✓/✗/N/A |
| Secrets scan | ✓/✗ |
| Release-train files clean | ✓/✗ |

### Issues
- (none)
```

**Output (refuse)**

```
## Refuse: /lsi-readiness

**Reason:** <wrong branch for mode>
**Fix:** <one line>
```

**Guardrails**

- Do not report `Ready` if test gate failed locally (unless documented N/A).
- Do not report `Ready` if release-train files (`VERSION` / `version.txt`, `CHANGELOG.md`, `BUNDLE_VERSION`) changed on a feature or promotion PR.
- Never post readiness report to Bitbucket unless user asks.
- Never draft PR title/body — name `/lsi:pr` instead.
- Feature mode: refuse on `main` or `staging`.
- Promotion mode: refuse on `main` only; **`staging`** branch is allowed.
- MUST emit the Output skeleton; MUST NOT invent alternate report shapes or append follow-up questions.
- No `Next:` footer (D11).
