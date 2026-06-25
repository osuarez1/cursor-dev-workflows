---
description: LSI workflow onboarding — orientation for new developers
---

Walk a new developer through the LSI workflow: tools, key concepts, and first steps.

**Canonical source:** [`overlays/lsi/docs/workflows/openspec-git-integration.md`](../../overlays/lsi/docs/workflows/openspec-git-integration.md) · [which-workflow.md](../../docs/workflows/which-workflow.md)

**Input:** Optional focus topic (`git`, `openspec`, `trello`, `pr`, `all`). Default: `all`.

**Steps**

1. **Greet and orient** — explain the three-layer model: OpenSpec (scope), Trello (delivery), Bitbucket (code review).

2. **Key tools checklist**

   | Tool | Setup check |
   |------|-------------|
   | `openspec` CLI | `openspec --version` |
   | `git ts` / `git tb` | `git ts --help` |
   | Trello access | Verify TRELLO_API_KEY in env |
   | Cursor or Claude agent | Confirm slash commands installed |

3. **Workflow overview** — summarize lifecycle from [openspec-git-integration.md](../../overlays/lsi/docs/workflows/openspec-git-integration.md):
   - Propose → Card + Branch → Apply → Commit → PR → Promote → Close

4. **First task suggestion**

   - If repo has active changes: show them via `openspec list --json`.
   - Otherwise: suggest `/opsx:new <slug>` or `/opsx:explore` to start.

5. **Pointer to docs**

   - [which-workflow.md](../../docs/workflows/which-workflow.md) — routing guide.
   - [openspec-git-integration.md](../../overlays/lsi/docs/workflows/openspec-git-integration.md) — full lifecycle.
   - `/lsi:help` — command reference.

**Output**

```
## LSI Workflow Onboarding

**Setup:** <tool check results>

**Lifecycle summary:** Propose → Card → Apply → Commit → PR → Promote → Close

**Your next step:** <suggestion>

Docs: which-workflow.md · openspec-git-integration.md · /lsi:help
```

**Guardrails**

- Do not run any implementation commands during onboarding — orientation only.
- If tools are missing, explain how to install before suggesting next steps.
