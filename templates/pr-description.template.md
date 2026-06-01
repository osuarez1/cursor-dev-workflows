# Pull request description template

Use with [pr-production-readiness.md](../pr-production-readiness.md). Replace placeholders for your project.

**Title (separate line):** `feat(scope): imperative description`

```markdown
## Overview
<Why this change exists; link to TICKET_TOOL card or issue.>

## Changes
- <major behavior or area>
- <major behavior or area>

## Potential risks
- <regression, migration, auth, deploy notes>

## Testing
1. <TEST_COMMAND or scoped variant>
2. <manual step a reviewer can run>

## Related
- <ticket URL, design doc, runbook>

## Checklist
- [ ] Tests added or updated for SOURCE_ROOT changes (see test-requirements.md)
- [ ] TEST_COMMAND passes (or Testing explains exemption)
- [ ] No unintended secrets or credentials
- [ ] Docs/config updated if applicable
```
