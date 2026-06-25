# OpenSpec + Git workflow

**LSI overlay** for [cursor-dev-workflows](https://github.com/osuarez1/cursor-dev-workflows) v{{BUNDLE_VERSION}}. Generic commit/PR/branch/review rules live in [docs/workflows/which-workflow.md](which-workflow.md); this doc maps them to **OpenSpec + Trello + Bitbucket**.

## Dual ticketing

| System | Role |
|--------|------|
| **OpenSpec** | Scope, specs, `tasks.md`, design — PR **Related** path `openspec/changes/<slug>/` |
| **Trello** | 24-char id in branch, pipeline list moves — via [git-trello-tool](https://github.com/osuarez1/git-trello-tool) |

Both align on the same **`<change-slug>`** (OpenSpec folder name). Card commands **`/lsi:card`**, **`/lsi:card-link`**, **`/lsi:trello-branch`**, and **`/lsi:trello-list`** (confirm path) draft Trello descriptions from OpenSpec artifacts only, redacted before API calls.

---

## Quick reference

| Concept | Value |
|---------|-------|
| Scope ticket | OpenSpec change slug |
| Delivery ticket | Trello card (24-char id in branch) |
| Branch | `feature\|bugfix\|hotfix\|chore/{id}-<change-slug>` via **`/lsi:card`**, **`/lsi:card-link`**, or **`/lsi:trello-list`** / **`/lsi:trello-branch`** |
| Protected branches | **`{{PROTECTED_BRANCHES}}`** — no task work (except card-setup: `/lsi:card`, `/lsi:trello-list`, `/lsi:trello-branch` on protected branches) |
| Implement | `/opsx:apply` on ticket branch |
| Close ticket | After **`main`** promotion: **`/lsi:close`** (or `/opsx:sync` → `/opsx:archive` on `main`) |
| Normative specs | [`openspec/specs/`](../../openspec/specs/) after production close on `main` |

| Upstream workflow | Link | Command |
|-------------------|------|---------|
| Trello card + branch | [ticket-card-info.md](ticket-card-info.md) | `/lsi:card` |
| Link card to existing branch | [ticket-card-info.md](ticket-card-info.md) | `/lsi:card-link` |
| List To Do cards | [git-trello.md](../sdlc/git-trello.md) | `/lsi:trello-list` |
| Branch from existing card | [git-trello.md](../sdlc/git-trello.md) | `/lsi:trello-branch` |
| Branch verify | [branch-workflow.md](branch-workflow.md) | `/lsi:branch` |
| Commits | [commits-logical-order.md](commits-logical-order.md) | `/lsi:commit` |
| Pull requests | [pull-requests.md](pull-requests.md) | `/lsi:pr` |
| Production promotion | [pull-requests.md](pull-requests.md) | `/lsi:promote` |
| Production close | [openspec-git-integration.md](openspec-git-integration.md) | `/lsi:close` |
| PR readiness | [pr-production-readiness.md](pr-production-readiness.md) | `/lsi:readiness` |
| Code review | [code-review.md](code-review.md) | `/lsi:review` |
| Senior analysis | [senior-analysis.md](senior-analysis.md) | `/lsi:senior` |
| Merge extended description | [commit-pr-conventions.mdc](../../.cursor/rules/commit-pr-conventions.mdc) | `/lsi:merge-desc` |
| Version bump | [versioning-and-releases.md](versioning-and-releases.md) | `/lsi:version` |
| Changelog | [versioning-and-releases.md](versioning-and-releases.md) | `/lsi:changelog` |
| Tag + Bitbucket | [versioning-and-releases.md](versioning-and-releases.md) | `/lsi:release` |
| Optional baseline tag | [versioning-and-releases.md](versioning-and-releases.md) | `/lsi:bootstrap-release` |

**OpenSpec:** `/opsx:explore`, `/opsx:propose`, `/opsx:apply`, `/opsx:sync`, `/opsx:archive` — provided by OpenSpec (`openspec init` / config profile); this bundle does not install or manage OpenSpec slash commands.

**LSI (git):** `/lsi:help`, `/lsi:card`, `/lsi:card-link`, `/lsi:trello-list`, `/lsi:trello-branch`, `/lsi:branch`, `/lsi:senior`, `/lsi:commit`, `/lsi:readiness`, `/lsi:review`, `/lsi:pr`, `/lsi:promote`, `/lsi:merge-desc`, `/lsi:close`, `/lsi:version`, `/lsi:changelog`, `/lsi:release`, `/lsi:bootstrap-release`, `/lsi:update`

**Release scripts:** `scripts/check_version.py` (version bump, changelog, and tag via `/lsi:version`, `/lsi:changelog`, `/lsi:release`)

---

## Lifecycle

1. **Explore** (optional) — `/opsx:explore`; docs-only on protected branches.
2. **Propose** — `/opsx:propose <slug>`.
3. **Senior analysis** (large changes) — `/lsi:senior` after `design.md`.
4. **Card + branch** — choose one (OpenSpec change must exist for all except list-only exit):
   - **`/lsi:card`** from **`main`** or **`staging`** → `git ts` (new card + branch)
   - **`/lsi:card-link`** on existing branch without Trello id → API + `git branch -m`
   - **`/lsi:trello-list`** → confirm → **`/lsi:trello-branch`** flow for existing To Do card → `git tb`
   - Card title/body from OpenSpec artifacts, redacted before Trello API
5. **Apply** — `/opsx:apply`; complete `tasks.md`.
6. **Commit** (when asked) — `/lsi:commit`.
7. **Readiness + review** (when asked) — `/lsi:readiness` → `/lsi:review`.
8. **PR to staging** (when asked) — `/lsi:pr`; default target **`staging`**.
9. **After staging merge** — `/lsi:merge-desc`; keep `openspec/changes/<slug>/` **active**; run `openspec list` to track in-flight changes.
10. **Staging QA** — validate on staging environment.
11. **Promotion PR** (when asked) — `/lsi:promote`; target **`main`** after QA passes.
12. **Production close** (after main merge) — checkout **`main`**, pull; **`/lsi:close`** → update `AGENTS.md` archive list.

**Rule:** A spec change is not normative truth until code runs in production. Do **not** run `/opsx:sync` or `/opsx:archive` when a feature PR merges to **`staging`** only.

**`tasks.md` rule:** Do **not** add `/opsx:sync`, `/opsx:archive`, or `/lsi:close` as implementation tasks. Those steps belong to **production close** on **`main`** (step 12 below), not `/opsx:apply`. When all `tasks.md` checkboxes are complete, the change is ready for PR — not archived.

---

## Protected branches

| Branch | Task implementation | `/lsi:card` | `/opsx:propose` |
|--------|---------------------|-------------|-----------------|
| `main` | Forbidden | **Allowed** (card only) | Allowed (docs) |
| `staging` | Forbidden | **Allowed** (card only) | Allowed (docs) |
| ticket branch | Allowed | N/A | Allowed |

---

## Branch checklist

- [ ] Not on `main` or `staging` (except card-setup from `main` or `staging`: `/lsi:card`, `/lsi:trello-list`, `/lsi:trello-branch`)
- [ ] Branch matches `feature|bugfix|hotfix|chore/{24-char-id}-<change-slug>`
- [ ] Suffix matches active OpenSpec change (`openspec list --json`)
- [ ] Trello card exists (via `git ts` or `git tb`)
- [ ] `PR_TARGET_BRANCH` (`staging`) merged/rebased before final PR review (use `BASE_BRANCH` for promotion PRs to `main`)

**Never** `git checkout -b feature/<slug>` without Trello id.

---

## PR promotion

| PR target | When | Command |
|-----------|------|---------|
| **`staging`** | Default for feature/fix/chore PRs | `/lsi:pr` |
| **`main`** | Production promotion after staging validation | `/lsi:promote` |

PR **Related:** `openspec/changes/<slug>/` + Trello card id/URL.

Template: [templates/pr-description.template.md](templates/pr-description.template.md)

### Staging-first archive policy

| Phase | Branch | `openspec/changes/<slug>/` | Sync / archive |
|-------|--------|----------------------------|----------------|
| Develop | Ticket branch | Active | Neither |
| Staging QA | After merge to `staging` | **Still active** | **Do not** sync or archive |
| Production | After merge to `main` | Archive on `main` | `/lsi:close` |

Use `openspec list` to see in-flight changes accumulated on staging.

### Hotfix path

1. Implement on `hotfix/{id}-<slug>` or minimal delta on `main` (OpenSpec artifacts only on protected branches).
2. Merge to **`main`**.
3. Run **`/lsi:close`** on **`main`**.
4. Merge **`main`** back into **`staging`** so environments and specs do not drift.

### Environment drift prevention

Any change merged to **`main`** (including hotfixes) MUST be back-merged to **`staging`** before the next staging QA cycle.

---

## Commit mapping

Map [commits-logical-order.md](commits-logical-order.md) to **`tasks.md` sections**.

Repo-specific commit scopes and area mapping are documented in the `openspec-git-integration.md` overlay for this repo (from `patches/files/<repo>/openspec-git-integration.md`).

| Area | Typical type |
|------|--------------|
| Source code | `feat(<scope>):` / `fix(<scope>):` |
| Tests | `test(<scope>):` |
| OpenSpec / workflow docs | `docs(openspec):` / `chore(docs):` |
| CI / pipelines | `ci:` / `chore(ci):` |
| Release / version | `chore(release):` |

Optional footer: `Refs: openspec/changes/<change-slug>`

---

## Review gates

**Order:** senior analysis (large) → implement → readiness → code review → PR.

### PR production readiness

Command: `/lsi:readiness`. Two modes — **feature** (default, PR target `staging`) and **promotion** (from `/lsi:promote`, PR target `main`).

| Mode | When | Diff base | PR target | Branch |
|------|------|-----------|-----------|--------|
| **Feature** | `/lsi:pr`, first PR | `staging` | `staging` | Ticket branch only; refuse `main` or `staging` |
| **Promotion** | `/lsi:promote` | `main` | `main` | Ticket branch or **`staging`**; refuse `main` |

In **promotion mode**, substitute `main` for `staging` in diff/log commands. On **`staging`** branch, skip ticket/Trello branch-pattern checks; confirm staging QA passed instead.

| Check | Feature | Promotion |
|-------|---------|-----------|
| Branch | Ticket pattern; not `main`/`staging` | Ticket branch or **`staging`**; not `main` |
| Ticket match | Suffix matches `openspec/changes/<slug>/` | Same on ticket branch; N/A on **`staging`** |
| Trello id | 24-char id in branch name | Same on ticket branch; N/A on **`staging`** |
| Tests | `{{TEST_COMMAND}}` when `{{SOURCE_ROOT}}` touched | Same |
| Version | `scripts/check_version.py` when version file bumped | Same |
| Secrets | None in diff | Same |

**Verdict:** `Ready` | `Needs fixes` | `Blocked`

### Code review

Command: `/lsi:review`. Same **feature** vs **promotion** modes as readiness — feature diffs `staging...HEAD`; promotion diffs `main...HEAD` and allows ticket branch or **`staging`**.

Follow [code-review.md](code-review.md). Repo-specific focus areas (critical components, security constraints, version scope) are documented in the per-repo `openspec-git-integration.md` overlay.

Save locally when asked: `.reviews/`, `.senior-analyses/` (gitignored).

---

## Pull request (from OpenSpec)

| PR section | Source |
|------------|--------|
| Overview | `proposal.md` → Why |
| Changes | What Changes + `design.md` |
| Potential risks | `design.md` + review |
| Testing | `tasks.md` + `{{TEST_COMMAND}}` from [PROJECT.md](../../PROJECT.md) |
| Related | `openspec/changes/<slug>/` + Trello id |

---

## Merge extended description (Bitbucket)

When user asks after PR approval — `/lsi:merge-desc`:

```text
<type>(<scope>): <imperative description>

Overview
--------
<Why>

Changes
-------
- <area> — <outcome>

Commits (N logical)
-------------------
1. <type>(<scope>): <subject>

Potential risks
---------------
- <concerns>

Testing
-------
- <steps>

Related
-------
openspec/changes/<slug>/
<Trello card id or URL>
```

---

## Full lifecycle (on demand)

Do **not** auto-run branch → propose → apply → commits → PR → promote → close unless user explicitly requests full lifecycle. Ask once to confirm scope.

---

## Post-staging merge (do not close)

After a feature PR merges to **`staging`**:

1. `/lsi:merge-desc` for Bitbucket extended merge description.
2. Keep `openspec/changes/<slug>/` **active**.
3. Do **not** run `/opsx:sync` or `/opsx:archive`.

<a id="production-close-after-main-merge"></a>

## Production close (after main merge)

Run on **`main`** only — use **`/lsi:close`** or manual steps:

1. All `tasks.md` `[x]`.
2. `/opsx:sync` if normative deltas exist.
3. `/opsx:archive`.
4. Update [`AGENTS.md`](../../AGENTS.md) archived-changes list.
5. If hotfix path: merge `main` → `staging`.

**Future (optional):** Bitbucket Pipeline hook to run archive automatically when a PR merges to `main` — not implemented yet.

---

## Platform release (optional, on `main`)

```text
/lsi:version → /lsi:changelog → chore(release): vX.Y.Z → /lsi:release
```

See [versioning-and-releases.md](versioning-and-releases.md). Forward-only from current `CHANGELOG.md` baseline.

---

## Command syntax

Cursor stores slash commands as files under `.cursor/commands/` with **hyphen** names (e.g. `lsi-card.md`, `lsi-commit.md`). In chat, invoke with **colon** syntax: `/lsi:card`, `/lsi:commit`. The mapping is one-to-one: `/lsi:card` → `lsi-card.md`. OpenSpec commands (`opsx-*`) follow the same pattern but are provided by OpenSpec, not this bundle.

---

## What we do not do

- Manual branches without Trello id.
- Task work on `main` or `staging` (except card-setup: `/lsi:card`, `/lsi:trello-list`, `/lsi:trello-branch` on protected branches).
- `gh pr create` or GitHub releases.
- Auto-commit or auto-open PRs without explicit request.
