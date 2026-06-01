# Commit plan example

Use with [commits-logical-order.md](../docs/workflows/commits-logical-order.md). **Do not run `git commit` until the user asks.**

## Proposed commit plan (3 commits)

### 1. feat(api): add webhook signature verification

**Includes:**

- `src/api/webhook.ts`
- `src/config/webhook.ts`

**Body:**

- Verify HMAC-SHA256 of raw body before JSON parse
- Reject missing or invalid signatures with 401

### 2. test(api): add regression for invalid webhook signature

**Includes:**

- `src/api/webhook.test.ts`

**Body:**

- Assert 401 and no enqueue when signature does not match

### 3. docs(api): document webhook authentication headers

**Includes:**

- `docs/api/webhooks.md`

**Body:**

- List required `X-Signature` header and signing algorithm

---

After user approval, execute commits **one at a time** in this order.
