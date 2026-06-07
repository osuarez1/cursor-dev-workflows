# Ticket card output example

Paste-ready blocks for [ticket-card-info.md](../docs/workflows/ticket-card-info.md).

**Task type (copy below):**

```text
feature
```

**Task title (copy below):**

```text
MyApp | Add webhook signature verification
```

**Task description (copy below):**

```markdown
**Context/Goal**
Accept partner webhooks only when HMAC signature matches shared secret.

**Acceptance Criteria**
- [ ] Invalid signature returns 401 without side effects.
- [ ] Valid signature enqueues processing job.
- [ ] Related tests pass (`TEST_COMMAND` or `tests/api/webhook.test.ts`).
- [ ] Documentation updated for webhook headers.

**Technical Notes**
- Touch `src/api/webhook.ts`, `src/api/webhook.test.ts`.
- Branch: `feature/<ticket-id>-webhook-hmac`.
- Commits: [commits-logical-order.md](../docs/workflows/commits-logical-order.md).
```
