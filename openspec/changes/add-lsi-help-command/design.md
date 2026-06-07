## Context

The LSI agent stack ships 18+ `/lsi:*` slash commands and adopted specs under `.lsi/workflows/`, but onboarding and “which command next?” routing rely on reading long markdown files. **`/lsi:help`** provides one-response-per-invocation workflow discovery: overview + topic list, or `/lsi:help <topic>` for a single section in chat.

**`/lsi:ask`** (ask-before-decide gating) remains deferred — help is read-only consultation, not decision gating.

## Goals / Non-Goals

**Goals:**

- Specify one-turn `/lsi:help` behavior in overlay command source.
- No-arg invocation: overview + numbered topic list only.
- Topic arg: full section rendered in one response from command templates.
- Separate **SDLC diagram** section (mermaid) distinct from numbered lifecycle text.
- GitHub blob URLs for all bundle spec links in help output (`v{BUNDLE_VERSION}` ref).
- Normative delta spec for parity and UX scenarios.

**Non-Goals (this change):**

- Implementing `lsi-help.md` or editing bundle routers (see `tasks.md`).
- `/opsx:sync`, archive, VERSION bump, adopter re-sync.
- Bitbucket or relative `.lsi/workflows/` links in help output.
- `/lsi:ask` meta-command.

## Decisions

### 1. One response per invocation (strict one-turn)

**Choice:** Each `/lsi:help` invocation produces exactly one chat response. No multi-turn help state. No AskQuestion menu loop.

- **No arg:** overview + numbered topic list (eight ids); user runs `/lsi:help <topic>` for content.
- **With `<topic>`:** read `## Section: \`{topic}\`` from command source, substitute `{ref}`, emit full section; stop.

**Rationale:** Multi-turn session state failed in dogfood — follow-up turns did not re-inject command prompts, so section content was skipped. One-turn + explicit topic arg is deterministic.

**Alternative rejected:** Sticky session until Exit with AskQuestion re-menu — agents lost session context on follow-up turns.

### 2. Eight topics (no Exit)

**Choice:** Topic ids: `sdlc`, `lifecycle`, `status`, `commands`, `policies`, `overlap`, `links`, `next`.

**Rationale:** Covers SDLC visual, numbered lifecycle, context, command table, policies, overlap/card paths, deep links, and next-step routing. No Exit — each invocation is self-contained.

### 3. SDLC diagram as separate section

**Choice:** `sdlc` section emits mermaid flowchart only (staging-first happy path). `lifecycle` section is numbered text (13 steps) without mermaid.

**Rationale:** User requested diagram as its own section; avoids duplicating visual + list in overview.

### 4. GitHub-only spec links

**Choice:** All spec links in help output use:

`https://github.com/osuarez1/cursor-dev-workflows/blob/{ref}/{bundle-path}`

where `{ref}` = `v{BUNDLE_VERSION}` from repo `PROJECT.md`, fallback `main`.

**Rationale:** Confirmed product decision — links open canonical bundle source on GitHub, not adopter Bitbucket repos or local IDE paths.

**Alternative rejected:** Relative `.lsi/workflows/` paths — not clickable outside repo; mixed clickability in examples.

### 5. Topic arg renders section (one response)

**Choice:** `/lsi:help <topic>` emits the matching section in one response (optional one-line intro only). Agent **must** read command source and render `## Section: \`{topic}\``.

Topics: `lifecycle`, `sdlc`, `status`, `commands`, `policies`, `overlap`, `links`, `next`.

**Alternative rejected:** Topic arg + mandatory re-menu — contradicts one-turn model.

### 6. Overlap rule in LSI overlay router only

**Choice:** Add overlap rule **#7** to `overlays/lsi/docs/workflows/which-workflow.md` only — not a full rule in bundle-root `which-workflow.md`. At most extend the root LSI decision-table row with “discovery → `/lsi:help` (overlay)” so maintainers know where to look.

**Suggested overlay text (one paragraph; link to `lsi-help.md` for detail):**

> **`/lsi:help` vs implementation commands** — `/lsi:help` is read-only reference output (one response per invocation); it may suggest the next command but does **not** run `/lsi:*`, `/opsx:*`, `git ts`/`git tb`, Trello API, `adopt.py`, or commits. When the user wants to **do** work (card, apply, PR, close), use the implementation command.

**Rationale:** Matches existing overlay overlap rules framed as consultation vs side effects (commit plan vs execution, card vs implementation). Agents read `which-workflow.md` before picking a workflow; without this rule, routing docs and command guardrails can diverge. `/opsx:explore` stays table-only (single-turn, less sticky); `/lsi:help` justifies a dedicated rule.

**Layer ownership (avoid duplication):**

| Layer | Owns |
|-------|------|
| LSI overlay `which-workflow.md` overlap #7 | Routing disambiguation: help reference ≠ implementation |
| `lsi-help.md` | One-turn steps, topic list, section templates, no auto-run |
| Delta spec | Testable scenarios (read-only, one response, topic render) |
| Help `overlap` section | Summarize existing overlap rules + this one |

**Optional (overlay flowchart):** Early branch for “workflow help / which command / LSI onboarding” → `/lsi:help`, before the card/branch fork. **Not implemented** — task **2.4** closed: decision table routes discovery; flowchart omits early help branch. **No code change required** unless optional live routing dogfood (**5.7** follow-up) fails.

**Alternative rejected:** Full overlap rule in bundle-root `which-workflow.md` — root overlap rules are workflow-spec disambiguation (PR vs readiness vs review), not slash-command session behavior.

### 7. Status section — conditional `TITLE_PREFIX` note only

**Choice:** The **`status`** section shows branch, active OpenSpec, phase, and suggested next command. Do **not** emit a standing line about whether this repo defines `TITLE_PREFIX`. When the inferred phase or suggested next step involves **card setup** (`/lsi:card`, `/lsi:card-link`, `/lsi:trello-list` → branch), add one conditional note framed as a **token rule**: read `TITLE_PREFIX` from `PROJECT.md` for card titles; when the token is absent, use `REPO_NAME |` per [ticket-card-info.md](docs/workflows/ticket-card-info.md).

**Rationale:** `TITLE_PREFIX` is adopter-specific; help should not bake in bundle-maintainer exceptions. Card setup is the only common status turn where the token matters.

**Alternative rejected:** Always mention `TITLE_PREFIX` in status — noise on most phases; reads as bundle-specific lore instead of portable workflow guidance.

### 8. Next and status heuristics (branch → phase → command)

**Choice:** Both **`status`** and **`next`** infer phase from read-only signals, then suggest **one** slash command + short rationale. Same inference table; `status` adds branch/OpenSpec summary; `next` emits the command recommendation only.

**Inputs (read-only):**

1. `git branch --show-current`
2. `openspec list --json`
3. Optional: `git status --short`; `openspec/changes/<slug>/design.md` exists; skim `tasks.md` for unchecked boxes

**Branch classification:**

| Pattern | Match |
|---------|--------|
| Protected integration | `^(main\|staging)$` |
| Ticket-linked | `^(feature\|bugfix\|hotfix\|chore)/[a-f0-9]{24}-.+$` |
| Other | Non-ticket or legacy branch names |

Extract `{id}` and `{change-slug}` from ticket branch suffix. Compare `{change-slug}` to active OpenSpec change name when one change is in progress.

**Phase → suggested command** (first matching row wins; stop at first match):

| Branch class | OpenSpec / signals | Phase label | Suggested command |
|--------------|-------------------|-------------|-------------------|
| Other | Active change; branch lacks 24-char id | Wrong branch | `/lsi:branch` — then `/lsi:card-link` if on feature work without id |
| Protected | No in-progress change | Pre-change | `/opsx:explore` (optional) or `/opsx:propose` |
| Protected | In-progress; `design.md` present; apply not started | Design review (optional) | `/lsi:senior` — then card setup |
| Protected | In-progress; ready for card | Card setup | `/lsi:card` from `main`/`staging` — or `/lsi:trello-list` → branch for existing card |
| Ticket | Suffix ≠ active change slug | Branch mismatch | `/lsi:branch` |
| Ticket | `tasks.md` has unchecked apply items | Implement | `/opsx:apply` |
| Ticket | Uncommitted changes; user likely committing | Commit | `/lsi:commit` (only when user asks to commit) |
| Ticket | Apply complete; pre-PR | Readiness | `/lsi:readiness` |
| Ticket | After readiness pass | Review | `/lsi:review` |
| Ticket | After review; ready to open PR | PR to staging | `/lsi:pr` |
| Protected `main` | Change still in-progress after staging (infer from context) | Promotion | `/lsi:promote` — **only when user context indicates staging QA passed** |
| Protected `main` | After production merge | Production close | `/lsi:close` |

**Ambiguity rules:**

- When two rows could apply, prefer the **earlier lifecycle step** (implement before readiness).
- When staging merge / promotion / close cannot be inferred from branch + OpenSpec alone, say **phase unclear** and suggest **`lifecycle`** or **`/lsi:branch`** — do not guess promotion or close.
- **`next` never auto-runs** the suggested command; name it + one-line why only.

**Rationale:** Gives deterministic guidance without duplicating full lifecycle text; conservative on post-staging phases that need human QA context.

### 9. Decision-table row (discovery → `/lsi:help`)

**Choice:** Add a decision-table row to **LSI overlay** `which-workflow.md` and `which-workflow-lsi.md` — **yes**, placed **after `/opsx:propose`** (discovery before card/implementation). Do **not** add a full row to bundle-root `which-workflow.md`; optional one-line pointer in the existing LSI row only (see task 2.3).

**Suggested row** (same text in overlay + `which-workflow-lsi.md`):

| User says (examples) | Use | Command | Output / verdict |
|----------------------|-----|---------|------------------|
| which command, workflow help, lost, LSI onboarding, what should I run next (discovery) | [`lsi-help.md`](../../agent-stack/commands/lsi-help.md) | `/lsi:help` | Overview + topic list; `/lsi:help <topic>` for section — read-only one-shot |

**Rationale:** Routes “which command / help / lost” before agents pick an implementation slash command or ask a generic clarifying question. Complements overlap rule #7 (help explains; does not run). Distinct from `/opsx:explore` (problem exploration, single-turn docs).

**Alternative rejected:** Rely on flowchart-only routing — table is what agents scan first; row is the canonical discovery entry.

## One-turn help flow

```mermaid
flowchart LR
  noTopic["/lsi:help"]
  withTopic["/lsi:help topic"]
  overview["Overview + topic list"]
  section["Full section in chat"]
  noTopic --> overview
  withTopic --> section
```

### Rules

| Rule | Detail |
|------|--------|
| One response | Each invocation ends after one agent response |
| Topic for content | Section bodies require `/lsi:help <topic>` |
| Read-only | No commits, Trello API, adopt, other slash commands |
| No auto-run | Do not execute `/lsi:*` or `/opsx:*` from help output |
| Render from source | On `<topic>`, read `## Section:` block from `lsi-help.md` and emit in chat |

## Command outline (`lsi-help.md`)

### Frontmatter

```yaml
---
name: /lsi-help
id: lsi-help
category: Workflow
description: LSI workflow help — one topic per invocation
---
```

### One-shot help guardrails (required at top of `lsi-help.md`)

- **One response per invocation** — no multi-turn help state
- **Topic arg:** read `## Section: \`{topic}\``, substitute `{ref}`, emit full section in chat
- **Read-only** — no git commit, Trello API, adopt, other slash commands
- **Suggest, don't run** — `next` topic names one command + rationale only

### Agent steps

1. Read `PROJECT.md` → `{ref}` from `BUNDLE_VERSION`.
2. If `<topic>`: optional read-only git/openspec for `status`/`next`; render section; stop.
3. If no arg: overview + numbered topic list; stop.
4. Invalid topic: error + topic list; stop.

**`status` / `next` sections:** apply §8 branch → phase → command heuristics (read-only inputs only).

### Overview template

```markdown
## LSI workflow overview

- **Dual ticketing:** OpenSpec + Trello (24-char branch id) — staging-first to `main`
- **Typical path:** propose → card/branch → apply → commit → readiness/review → PR → promote → close
- **Bundle:** [cursor-dev-workflows](https://github.com/osuarez1/cursor-dev-workflows) @ `{ref}`

Run `/lsi:help <topic>` for a section (see topic list below).
```

### Topic list (eight ids — no Exit)

| id | label |
|----|-------|
| `sdlc` | SDLC diagram |
| `lifecycle` | Full lifecycle (13 steps) |
| `status` | Where you are now |
| `commands` | Command reference by phase |
| `policies` | Key policies |
| `overlap` | Overlap rules and card paths |
| `links` | Deep dive spec links |
| `next` | Suggested next command |

Each `## Section:` block includes: *When topic matches, emit this entire block in chat (substitute `{ref}`).*

### SDLC diagram section (`sdlc`)

Emit mermaid (staging-first feature flow):

```mermaid
flowchart TD
  explore["/opsx:explore optional"]
  propose["/opsx:propose"]
  senior["/lsi:senior optional"]
  card["Card + branch"]
  cardTs["/lsi:card git ts"]
  cardLink["/lsi:card-link"]
  trello["/lsi:trello-list → trello-branch"]
  apply["/opsx:apply"]
  commit["/lsi:commit when asked"]
  readiness["/lsi:readiness"]
  review["/lsi:review"]
  prStaging["/lsi:pr → staging"]
  mergeDesc["/lsi:merge-desc"]
  stagingQA["Staging QA"]
  promote["/lsi:promote → main"]
  closeMain["/lsi:close on main"]
  release["/lsi:version → changelog → release optional"]
  explore --> propose
  propose --> senior
  senior --> card
  propose --> card
  card --> cardTs
  card --> cardLink
  card --> trello
  cardTs --> apply
  cardLink --> apply
  trello --> apply
  apply --> commit
  commit --> readiness
  readiness --> review
  review --> prStaging
  prStaging --> mergeDesc
  mergeDesc --> stagingQA
  stagingQA --> promote
  promote --> closeMain
  closeMain -.-> release
```

Legend: dashed edge = optional platform release on `main`; do not sync/archive on staging merge only.

Link to [which-workflow.md](https://github.com/osuarez1/cursor-dev-workflows/blob/{ref}/overlays/lsi/docs/workflows/which-workflow.md) for **routing** flowchart (ambiguous requests — different from SDLC diagram).

### Other sections (summary)

| id | Content |
|----|---------|
| `lifecycle` | Numbered 1–13 from which-workflow § Recommended order; GitHub links inline |
| `status` | Branch class, active OpenSpec, inferred **phase label**, suggested next command (§8 heuristics); **conditional** `TITLE_PREFIX` token note only when card setup is suggested (§7) |
| `commands` | Phase table with GitHub-linked Spec column |
| `policies` | Key policies with GitHub spec links |
| `overlap` | readiness vs review vs PR; card paths; **`/lsi:help` vs implementation** (cite overlay overlap #7) |
| `links` | Bullet list of all specs from bundle-path map |
| `next` | One `/lsi:*` or `/opsx:*` + rationale from §8 heuristics — suggest only, never invoke |

No re-menu after section — user invokes `/lsi:help` or `/lsi:help <topic>` again for more.

## GitHub bundle-path map

| Label | `bundle-path` |
|-------|---------------|
| `which-workflow.md` | `overlays/lsi/docs/workflows/which-workflow.md` |
| `openspec-git-integration.md` | `overlays/lsi/docs/workflows/openspec-git-integration.md` |
| `branch-workflow.md` | `overlays/lsi/docs/workflows/branch-workflow.md` |
| `git-trello.md` | `overlays/lsi/docs/sdlc/git-trello.md` |
| `ticket-card-info.md` | `docs/workflows/ticket-card-info.md` |
| `pull-requests.md` | `docs/workflows/pull-requests.md` |
| `pr-production-readiness.md` | `docs/workflows/pr-production-readiness.md` |
| `code-review.md` | `docs/workflows/code-review.md` |
| `senior-analysis.md` | `docs/workflows/senior-analysis.md` |
| `commits-logical-order.md` | `docs/workflows/commits-logical-order.md` |
| `versioning-and-releases.md` | `overlays/lsi/docs/workflows/versioning-and-releases.md` |
| `adopt-and-update.md` | `docs/adopt-and-update.md` |
| `common-mistakes.md` | `docs/workflows/common-mistakes.md` |
| `test-requirements.md` | `docs/workflows/test-requirements.md` |
| `integrations.md` | `docs/workflows/integrations.md` |
| `CONVENTION.commits.template` | `overlays/lsi/agent-stack/CONVENTION.commits.template` (adopted into repo-root `CONVENTION.md`) |

Example link:

`[senior-analysis.md](https://github.com/osuarez1/cursor-dev-workflows/blob/v1.4.0/docs/workflows/senior-analysis.md)`

## Risks / Trade-offs

- **Topic arg required for content** — no-arg shows list only; user must run `/lsi:help <topic>` (or agent routes them there).
- **GitHub-only links** — adopters on private forks must use their fork URL manually until a `DOCS_WEB_BASE` token exists (out of scope).
- **Agent-dependent section rendering** — delta spec requires agents to read `## Section:` blocks from command source; no programmatic enforcement. Chat dogfood matched overview, `sdlc`, `lifecycle`, `next`, and invalid topic. **Residual risk for other agents/models only.**
- **Routing gate 5.7 is static, not live** — decision-table phrase matching for three discovery prompts is documented and accepted; no fresh Agent chats in this change. **Optional follow-up:** plain-text discovery prompts in three fresh Agent chats to confirm real routing; task **2.4** flowchart branch if any fail.
- **Flowchart gap (accepted trade-off)** — overlay decision table routes discovery to `/lsi:help`; mermaid flowchart omits early help branch (task **2.4** closed intentionally). No code change unless live routing dogfood fails.
- **`verify-adopters.py` on bundle repo** — `--repo-root .` fails here (no `.lsi/workflows/`); expected for maintainer dogfood — parity script targets adopters after adopt re-sync, not this repo.
