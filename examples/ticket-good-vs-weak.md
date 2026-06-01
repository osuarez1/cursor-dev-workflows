# Ticket card: good vs weak

See [ticket-card-info.md](../ticket-card-info.md).

## Weak

**Title:** `webhook fix`

**Description:**

```markdown
Fix the webhook. Make sure it works correctly.
```

**Why weak:** No `TITLE_PREFIX`; vague acceptance criteria; no test or path notes.

---

## Strong

### Task type

```text
feature
```

### Task title

```text
MyApp | Add webhook HMAC verification
```

### Task description

```markdown
**Context/Goal**
Partners send signed payloads; we must reject tampered requests before enqueueing jobs.

**Acceptance Criteria**
- [ ] Missing `X-Signature` returns 401.
- [ ] Invalid signature returns 401 without enqueue.
- [ ] Valid signature enqueues `ProcessWebhookJob`.
- [ ] `TEST_COMMAND` passes for `src/api/webhook.test.ts`.

**Technical Notes**
- Files: `src/api/webhook.ts`, `src/api/webhook.test.ts`.
- Branch: `feature/<ticket-id>-webhook-hmac`.
```

**Why strong:** Testable checkboxes, clear scope, commands and paths for reviewers and agents.
