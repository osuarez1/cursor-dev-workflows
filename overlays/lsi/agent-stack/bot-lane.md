# Bot lane playbook (steps 9–19)

Coding-agent checklist for OpenSpec implementation after Mode A docs are on **`staging`**. Humans own steps 1–8 and 20–24 (close, promote, release) — see [openspec-git-integration.md](../docs/workflows/openspec-git-integration.md).

**Agents:** Cursor, Claude Code, OpenCode (when opted in). Load this playbook + `AGENTS.md`; invoke slash commands as listed. Do **not** emit `Next:` footers from individual commands — this file is the sequencer.

## Preconditions

- Ticket branch: `feature|bugfix|hotfix|chore/{24-char-id}-<change-slug>`
- Active change: `openspec/changes/<slug>/` with `tasks.md`
- Mode A docs PR merged (unless Mode C opt-in)

## Checklist

**Unattended path (preferred when Bitbucket + bot token):** **`/lsi:apply-bot <slug>`** covers steps 9–18 (apply by section, gate loops, Mode B PR) per [bot-sessions.md](bot-sessions.md). Mode A review: **`/lsi:pr-bot-docs <PR>`** (includes `/lsi:readiness`). Mode B/C review: **`/lsi:pr-bot <PR> [--fix]`** (includes `/lsi:readiness`).

Manual step-by-step (same outcomes):

9. **`/opsx:apply`** — implement `tasks.md`; mark checkboxes; do not sync/archive/close.
10. **`/lsi:commit`** — when the human asks; Conventional Commits from `tasks.md` sections.
11. **`/opsx:verify`** — report Aligned / Partial / Discrepancy; stop (no Next).
12. **`/lsi:address-verify`** — if verify is Partial/Discrepancy; fix + commit as deliverable.
13. **`/lsi:readiness`** — feature mode vs `staging`; stop after verdict.
14. **`/lsi:address-readiness`** — if Needs fixes / Blocked; fix + commit.
15. **`/lsi:review`** — feature mode; **auto-run `/lsi:address-prowler`** first when an open PR has a comment starting with `Prowler · Grok Bot review`; then review findings; no Next.
16. **`/lsi:address-review`** — if Request changes / blockers; fix + commit.
17. Re-run readiness/review as needed until Ready + Approve (or Approve with nits).
18. **`/lsi:pr` mode B** — draft/push PR to **`staging`** only (do not run readiness/review/verify inside `/lsi:pr`).
19. After merge — **`/lsi:merge-desc`** when asked; leave change **active**.

## Forbidden in bot lane

- `/lsi:close`, `/lsi:promote`, `/lsi:release-train`, `/lsi:version` / release tagging
- `/opsx:sync`, `/opsx:archive` (human close step)
- Task work on `main` or `staging`
- Inventing Next footers or opportunistic command chains outside a command’s documented deliverable

## Related

- Lifecycle lanes: [openspec-git-integration.md](../docs/workflows/openspec-git-integration.md)
- Address-findings: `/lsi:address-senior`, `/lsi:address-review`, `/lsi:address-verify`, `/lsi:address-readiness`, `/lsi:address-prowler`
