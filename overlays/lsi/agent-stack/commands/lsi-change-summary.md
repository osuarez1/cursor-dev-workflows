---
name: /lsi-change-summary
id: lsi-change-summary
category: Workflow
description: Chat-only executive brief for one OpenSpec change (active or archived)
---

Produce a chat-only executive brief for a single OpenSpec change, sourced from its `proposal.md`, `design.md`, `specs/`, and `tasks.md`.

**Canonical source:** [`docs/workflows/openspec-git-integration.md`](../../docs/workflows/openspec-git-integration.md)

**Canonical skeleton:** [`lsi-release-summary.md`](lsi-release-summary.md) § *Shared summary skeleton* — same meta table, same sections 1–10, same audience rules.


**Input:** Change slug **or** path under `openspec/changes/` or `openspec/changes/archive/` (required). Optional audience flag `--mgmt` (default) or `--ops`.

**Steps**

1. **Resolve the change** — first match wins:

   ```bash
   openspec list --json                                  # active changes
   ls -d openspec/changes/<slug> 2>/dev/null             # active by slug
   ls -d openspec/changes/archive/*-<slug> 2>/dev/null   # archived (date-prefixed)
   ```

   - A path argument is used as given when the directory exists.
   - Archived folders are `archive/<YYYY-MM-DD>-<slug>/` — match on the slug suffix.
   - **Multiple archive matches:** list them and ask which one; do not guess.
   - **No match:** stop with an error naming the slug and where it was looked for. **Do not invent a summary** for a change that does not resolve.

2. **Resolve the audience** — `--ops` when passed, otherwise `--mgmt`. Audience changes **section 5 only**.

3. **Read the artifacts that exist**

   ```bash
   ls <change-dir>
   cat <change-dir>/proposal.md <change-dir>/design.md <change-dir>/tasks.md
   cat <change-dir>/specs/*/spec.md
   ```

   Artifacts are optional — an archived change may lack `design.md`, a young change may lack `specs/`. Record which artifacts were read in the meta table and say `not present` for the rest. Every claim MUST trace to an artifact; **never invent** requirements, PR numbers, or risks.

4. **Emit the shared skeleton in chat** — meta table then sections 1–10, in order, per [`lsi-release-summary.md`](lsi-release-summary.md) § *Shared summary skeleton*.

**Meta table for a change**

| Field | Value |
|-------|-------|
| Subject | `migrate-android-push-fcm-v1` |
| Type | OpenSpec change |
| Status | Archived 2026-08-19 (or Active — 9/9 tasks) |
| Audience | Management (`--mgmt`) |
| Sources | `proposal.md`, `design.md`, `specs/push-notifications/spec.md`, `tasks.md` |
| Shipped in | PR #2570 / `v0.21.0` when the artifacts state it, else `N/A` |

**Section 6 is domain-adaptive**

Choose columns from the change's own domain — never reuse another change's columns:

| Change domain | Example section 6 columns |
|---------------|---------------------------|
| Push / delivery | Platform → transport → audit outcome |
| Payments / membership | Provider or plan → eligibility → resulting state |
| Encoder / media | Input layout → track or ladder selection → refusal behavior |
| Admin UI / access | Role → visible surface → permitted action |
| Workflow / tooling | Command → branch precondition → output |

When the change genuinely has one behavior, write `N/A — single behavior` rather than padding the table.

**Section 7 for a change** — mermaid when the change has multiple actors, states, or decision branches (typical for API/worker/state-machine work); otherwise `No diagram — linear change.`

**Output**

```markdown
## Change summary — migrate-android-push-fcm-v1

| Field | Value |
|-------|-------|
| Subject | `migrate-android-push-fcm-v1` |
| Type | OpenSpec change |
| Status | Archived 2026-08-19 |
| Audience | Operations (`--ops`) |
| Sources | `proposal.md`, `design.md`, `specs/…/spec.md`, `tasks.md` |
| Shipped in | PR #2570 |

### 1. Verdict
<one line>

### 2. What this does
- <bullet>

...

### 10. Related links
- `openspec/changes/archive/2026-08-19-migrate-android-push-fcm-v1/`
```

**Guardrails**

- **Chat only** — never write files; in particular never edit `tasks.md`, `proposal.md`, or specs of the summarized change
- **Read-only** — no `/opsx:apply`, `/opsx:sync`, `/opsx:archive`, commits, or branch changes
- Works on any branch — summarizing does not require `main`
- `--mgmt` when the audience flag is omitted
- Stop with an error when the slug resolves to nothing; ask when it resolves to more than one archived folder
- Adapt section 6 to the change's domain — do not hard-code one product area
- Do not restate raw requirement text; translate specs into reader-facing behavior
- Never emit a PR title or body draft — `/lsi:pr` (feature → `staging`) and `/lsi:promote` (promotion → `main`) own the draft; name the command instead.
- MUST emit the Output skeleton; MUST NOT invent alternate report shapes or append follow-up questions.
- No `Next:` footer (D11).
