# PR description: good vs weak

See [pull-requests.md](../docs/workflows/pull-requests.md).

## Weak title

```text
Fixed stuff
```

**Why weak:** Not Conventional Commits style; no type or scope.

---

## Weak body

```markdown
## Overview
Fixed things.

## Changes
- stuff

## Testing
Looks good.
```

**Why weak:** Vague overview; Changes do not describe behavior; Testing is not runnable.

---

## Strong

**Title**

```text
feat(api): add webhook HMAC verification for inbound events
```

**Body (excerpt)**

```markdown
## Overview
Partners send signed payloads; we currently accept unsigned bodies on the legacy endpoint.

## Changes
- Verify HMAC-SHA256 before parsing JSON on `/webhooks/inbound`
- Return 401 when signature header is missing or invalid

## Potential risks
- Existing integrators without signatures will receive 401 until they enable signing

## Testing
1. TEST_COMMAND (or: npm test -- src/api/webhook.test.ts)
2. POST sample payload with valid `X-Signature` — expect 200
3. Repeat with wrong signature — expect 401

## Related
- TICKET_TOOL link or PROJ-456
```

**Why strong:** Stand-alone title; each section is specific; Testing gives reviewer steps; risks are explicit.
