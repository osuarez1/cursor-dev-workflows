# Code review output template

Use with [code-review.md](../code-review.md).

```markdown
## Summary
<1–2 sentences: overall readiness>

## Critical issues
- <issue with file:line reference, or "None">

## Suggestions
- <optional improvement, or "None">

## Test coverage
- <what exists, what is missing>
- Run: `TEST_COMMAND`

**Verdict:** Ready | Needs fixes | Blocked
```

### Log-ready comment (remote — only when user asks)

```text
**Code review — YYYY-MM-DD HH:MM (local)**
**Base:** BASE_BRANCH...HEAD (<N> commits)
**Verdict:** Ready | Needs fixes | Blocked

**Summary**
...

**Critical issues**
- ...

**Suggestions**
- ...

**Test coverage**
- ...
```
