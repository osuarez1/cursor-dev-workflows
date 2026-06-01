# Commit plan: good vs weak

See [commits-logical-order.md](../commits-logical-order.md).

## Weak

Single commit for entire branch without user asking:

```text
fix: webhook and tests and docs
```

**Why weak:** Multiple logical changes compacted; no plan; user did not ask to commit; non-conventional subject.

---

## Strong

User: “Prepare commits but don’t commit yet.”

```markdown
## Proposed commit plan (3 commits)

### 1. feat(api): add webhook HMAC verification
**Includes:** src/api/webhook.ts
**Body:** Verify signature before parse; 401 on failure.

### 2. test(api): add regression for invalid signature
**Includes:** src/api/webhook.test.ts

### 3. docs(api): document webhook auth headers
**Includes:** docs/api/webhooks.md
```

After user: “commit the first one only” — agent runs `git commit` for item 1 only.

**Why strong:** Logical split, conventional subjects, bodies explain why, execution only when asked.
