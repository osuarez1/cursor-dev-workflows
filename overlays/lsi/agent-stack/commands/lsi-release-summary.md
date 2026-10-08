---
name: /lsi-release-summary
id: lsi-release-summary
category: Workflow
description: Chat-only executive brief for a released version from CHANGELOG.md
---

Produce a chat-only executive brief for one released version, sourced from `CHANGELOG.md` and `version.txt`.

**Canonical source:** [`docs/workflows/versioning-and-releases.md`](../../docs/workflows/versioning-and-releases.md)

**Canonical skeleton:** this file, § *Shared summary skeleton* — [`/lsi:change-summary`](lsi-change-summary.md) reuses it unchanged.


**Input:** Optional version or tag (`0.21.0`, `v0.21.0`). Optional audience flag `--mgmt` (default) or `--ops`.

**Steps**

1. **Resolve the version**

   - Argument when given — strip a leading `v`.
   - Else `cat version.txt`.
   - Else the top-most `## [X.Y.Z]` section in `CHANGELOG.md`.

   Confirm `CHANGELOG.md` contains `## [X.Y.Z]` for the resolved version. **Stop with an error when it does not** — do not summarize a version that has no changelog section.

2. **Resolve the audience** — `--ops` when passed, otherwise `--mgmt`. Audience changes **section 5 only**.

3. **Gather facts (read-only)**

   ```bash
   # REPO_NAME from PROJECT.md (fallback: git remote basename)
   git branch --show-current
   cat version.txt   # or VERSION when that is the repo canonical file
   sed -n "/^## \[${VERSION}\]/,/^## \[/p" CHANGELOG.md
   git tag --list "v${VERSION}"
   ```

   - Read deploy-gate docs **only when the changelog entry references them**.
   - Every claim MUST trace to the changelog section, a referenced doc, or git tag state. **Never invent** scope, dates, PR numbers, or risks.

4. **Emit the shared skeleton in chat** — H1 header (repo **before** branch), then meta table, then sections 1–10, in order.

---

## Shared summary skeleton

**H1 header** (required shape — repo name before branch):

```markdown
## Release summary — <REPO_NAME> / <branch> — v0.21.0
```

Example: `## Release summary — cursor-dev-workflows / main — v2.1.0`

**Meta table** (always first after the H1; **Repo** before **Branch**):

| Field | Value |
|-------|-------|
| Repo | `cursor-dev-workflows` (`REPO_NAME` from PROJECT.md) |
| Branch | `main` (`git branch --show-current`) |
| Subject | `v0.21.0` |
| Type | Release |
| Date | 2026-08-20 (changelog section date) |
| Audience | Management (`--mgmt`) |
| Sources | `CHANGELOG.md` § `[0.21.0]`, `version.txt` |
| Status | Tagged / not tagged |

**Sections** (numbered 1–10, in this order, every time):

| # | Section | Content | When empty |
|---|---------|---------|------------|
| 1 | Verdict | One line — what shipped and whether it is safe to roll out | Never empty |
| 2 | What this does | 3–6 bullets of user-visible change, no commit prefixes | `N/A` |
| 3 | Who is affected | Audiences (members, admins, operators, integrations) | `N/A — no user-facing surface` |
| 4 | What people should expect | Observable behavior after rollout | `N/A` |
| 5 | What to do | Audience-dependent checklist — see below | `N/A — no action required` |
| 6 | Behavior matrix | **Table** — path / condition → behavior before vs after | `N/A — single behavior` |
| 7 | Flow diagram | **Mermaid** when the release has multiple paths or stages | `No diagram — linear change.` |
| 8 | Risks and go/no-go | **Table** — risk, likelihood/impact, mitigation, go or no-go | `N/A — no known risks` |
| 9 | Suggested follow-ups | Concrete next steps, owner hint when known | `N/A` |
| 10 | Related links | CHANGELOG section, PRs, deploy docs, archived OpenSpec changes | `N/A` |

**Section 5 tone by audience** — same facts everywhere, different actions:

| Audience | Section 5 contains |
|----------|--------------------|
| `--mgmt` (default) | Business impact, customer comms, support/CS talking points, what to watch commercially, who signs off |
| `--ops` | Deploy gates and order, credential prerequisites, migrations, verification commands, rollback trigger |

**Skeleton rules**

- H1 MUST be `## Release summary — <REPO_NAME> / <branch> — vX.Y.Z` (repo before branch; never omit either).
- Meta table MUST list **Repo** then **Branch** before Subject.
- Sections 1–10 always appear, in order, even when the content is `N/A`.
- Sections 2–4 and 6–10 are **identical** regardless of audience flag; only section 5 changes.
- Section 7 emits mermaid when the subject has multiple paths, stages, or actors; otherwise it states `No diagram — linear change.` — never an empty section.
- Sections 6 and 8 are markdown tables, never prose.

**Output**

```markdown
## Release summary — cursor-dev-workflows / main — v0.21.0

| Field | Value |
|-------|-------|
| Repo | `cursor-dev-workflows` |
| Branch | `main` |
| Subject | `v0.21.0` |
| Type | Release |
| Date | 2026-08-20 |
| Audience | Management (`--mgmt`) |
| Sources | `CHANGELOG.md` § `[0.21.0]` |
| Status | Tagged |

### 1. Verdict
<one line>

### 2. What this does
- <bullet>

### 3. Who is affected
...

### 10. Related links
- `CHANGELOG.md` § `[0.21.0]`
```

**Guardrails**

- **Chat only** — never write `docs/releases/`, summary files, or any repo file
- **No side effects** — no commit, tag, push, or version write; use `/lsi:release-train` to conduct a release
- Read-only on any branch — the summary does not require `main`
- Strip `type(scope):` prefixes; changelog bullets are the source, not commit subjects
- `--mgmt` when the audience flag is omitted
- Stop with an error rather than summarizing a version with no `## [X.Y.Z]` section
- Do not invent PR numbers, dates, risks, or deploy gates that the sources do not state
- Never emit a PR title or body draft — `/lsi:pr` (feature → `staging`) and `/lsi:promote` (promotion → `main`) own the draft; name the command instead.
- MUST emit the Output skeleton; MUST NOT invent alternate report shapes or append follow-up questions.
- No `Next:` footer (D11).
