# Test requirements

When automated tests are **required** on a change. Applies to humans and coding agents. Customize `SOURCE_ROOT`, `TEST_ROOT`, and `TEST_COMMAND` (see [README.md](../../README.md)).

## When tests are required

Any change that modifies **application behavior** under `SOURCE_ROOT` (e.g. `src/`, `app/`, `lib/`, `internal/`) must include added or updated tests unless a valid exemption applies.

### Path mapping (generic)

| Source | Tests (typical) |
|--------|-----------------|
| `src/foo/bar.ts` | `tests/foo/bar.test.ts` or `src/foo/bar.spec.ts` |
| `pkg/api/handler.go` | `pkg/api/handler_test.go` |
| Mirror your repo’s existing convention | Match neighboring files |

**Rule:** If the repo already mirrors paths, follow that pattern; do not invent a second convention.

### Change type expectations

| Type | Expectation |
|------|-------------|
| **Bugfix** | Regression test that would have failed before the fix |
| **Feature** | Tests for new or changed public behavior (API, service output, validation) |
| **Refactor** | Existing tests should still pass; add tests if behavior changed |

### Quality bar

- Test **behavior**, not trivial existence checks (`expect(fn).toBeDefined()` only).
- Prefer unit tests near the changed module; integration/e2e when the change is UI or cross-service.
- Name what broke or what contract is guaranteed.

## When tests are not required

State the exemption in the PR **Testing** section:

- Documentation only (`docs/`, `*.md`)
- Comments, formatting, or locale strings with **no** logic change
- Generated files committed intentionally by a documented generator
- Config-only changes with no runtime behavior change

Agents must not skip tests silently for application code.

## Commands

Document in the target repo:

```bash
# Replace with project standard
TEST_COMMAND    # e.g. npm test, pytest, go test ./...
LINT_COMMAND    # optional
```

For PR readiness, include `TEST_COMMAND` (or scoped variant) in checklists — see [pr-production-readiness.md](pr-production-readiness.md).

## Acceptance criteria on tickets

When drafting cards ([ticket-card-info.md](ticket-card-info.md)), include a checkbox such as:

```markdown
- [ ] Related tests pass (`TEST_COMMAND` or named paths) when SOURCE_ROOT changes
```

## Related

- [pr-production-readiness.md](pr-production-readiness.md)  
- [code-review.md](code-review.md) — Test coverage section  
- [ticket-card-info.md](ticket-card-info.md)  
