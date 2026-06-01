# Code review: good vs weak

See [code-review.md](../code-review.md).

## Weak

```markdown
Looks good to me! Ship it.
```

**Why weak:** No critical/suggestion/test sections; no verdict; no file references; conflates with senior analysis praise.

---

## Strong

```markdown
## Summary
Webhook verification is sound; missing test for clock-skew replay window.

## Critical issues
- None

## Suggestions
- `src/api/webhook.ts:42` — consider constant-time compare for signature (timing leak).

## Test coverage
- Happy path and invalid signature covered.
- Missing: expired timestamp rejection.
- Run: `npm test -- src/api/webhook.test.ts`

**Verdict:** Needs fixes
```

**Why strong:** Actionable, scoped verdict, concrete next step, separates suggestions from blockers.
