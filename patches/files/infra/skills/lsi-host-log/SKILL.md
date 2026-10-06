---
name: lsi-host-log
description: >-
  Capture per-change SSH host logging notes for infra deploy/ops work.
  Use when the user asks for host logs, SSH session notes, or infra change
  host evidence tied to an OpenSpec change or deploy.
---

# lsi-host-log (infra only)

Record **which hosts** were touched for an OpenSpec change or deploy, with timestamps and evidence pointers. Infra-only skill — not installed for other adopters.

## When to use

- User asks to log SSH hosts for a change, deploy, or incident
- Closing or summarizing infra work that required host access

## Steps

1. Resolve change slug (branch suffix or user input) and date (UTC).
2. Collect host identifiers (hostname / inventory name), role, and access method (SSH bastion, SSM, etc.) from the user or session — **do not invent hosts**.
3. Emit a chat-only log table (unless the user asks to write a file under an infra-owned path they name).

## Output

```
## Host log: <slug or deploy>

**Date:** YYYY-MM-DD
**Operator:** <name or unknown>

| Host | Role | Access | Notes |
|------|------|--------|-------|
| ... | ... | SSH/SSM | ... |

### Evidence
- (none)
```

## Guardrails

- Never store credentials, private keys, or secrets in the log
- Do not invent hosts; ask when unknown
- Infra patch only — other repos should not install this skill
