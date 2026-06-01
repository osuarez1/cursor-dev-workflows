# Senior analysis: good vs weak

See [senior-analysis.md](../docs/workflows/senior-analysis.md).

## Weak

```markdown
## Summary
The code looks fine. Ready to merge.
```

**Why weak:** Uses merge verdict `Ready`; no logical units; no alternatives; duplicates code review.

---

## Strong

```markdown
## Executive summary
Branch adds HMAC verification at the HTTP boundary before enqueue. Design is Sound with one follow-up on timestamp tolerance.

**Overall verdict:** Acceptable with follow-ups

## LC-1: Verify webhook at HTTP boundary

### Alternatives
| Option | Pros | Cons |
| A — middleware (chosen) | Fail fast, no poison jobs | Duplicates secret lookup if multiple routes |
| B — verify in worker | Single code path | Bad jobs already enqueued |

### Unit verdict
Sound

## Relationship to code review
Run code-review for timing-safe compare and expired-header tests before merge.
```

**Why strong:** Design verdict vocabulary, alternatives, clear handoff to code review — not merge approval.
