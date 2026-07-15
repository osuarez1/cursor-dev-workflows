# OpenSpec + Git workflow (stream-api)

**LSI overlay** for [cursor-dev-workflows](https://github.com/osuarez1/cursor-dev-workflows) v{{BUNDLE_VERSION}}. Generic workflow rules live in [which-workflow.md](which-workflow.md); this doc maps them to the **stream-api** (Rails API) repo.

## Quick reference (stream-api)

| Concept | stream-api |
|---------|------------|
| Scope ticket | OpenSpec change slug |
| Delivery ticket | Trello card (24-char id in branch) |
| Branch | `feature\|bugfix\|hotfix\|chore/{id}-<change-slug>` |
| Protected branches | **`main`**, **`staging`**, **`master`** |
| Source root | `app/`, `lib/` |
| Test root | `spec/` |
| Test command | `{{TEST_COMMAND}}` |
| PR host | Bitbucket — `lsistreaming/stream-api` |

OpenSpec `opsx-*` slash commands remain installed alongside `/lsi:*` — adopt never removes them.

---

## Commit mapping (stream-api)

Map tasks.md sections to Conventional Commits scopes:

| Area | Typical scope |
|------|---------------|
| Controllers / routes / Apipie | `feat(api):` / `fix(api):` |
| Models / ActiveRecord | `feat(model):` / `fix(model):` |
| Store tools / services | `feat(iap):` / `fix(iap):` / `feat(svc):` |
| Sidekiq jobs | `feat(job):` / `fix(job):` |
| RSpec tests | `test(<scope>):` |
| OpenSpec / workflow docs | `docs(openspec):` / `chore(docs):` |
| CI / Bitbucket pipelines | `ci:` / `chore(ci):` |
| Release / version | `chore(release):` |
| Test DB / Postgres.app helpers | `chore(db):` / `docs(db):` |

Do **not** land schema migrations here — schema is owned by the web monolith.

Optional footer: `Refs: openspec/changes/<change-slug>`

---

## PR production readiness (stream-api)

| Check | Feature | Promotion |
|-------|---------|-----------|
| Branch | Ticket pattern; not `main`/`staging`/`master` | Ticket branch or **`staging`**; not `main` |
| Ticket match | Suffix matches `openspec/changes/<slug>/` | Same on ticket branch |
| Trello id | 24-char id in branch name | Same on ticket branch |
| Tests | `{{TEST_COMMAND}}` when `app/` or `lib/` or `spec/` changed | Same |
| Coverage | `COVERAGE=1` gate on CI; local when touching covered paths | Same |
| Version | `scripts/check_version.py` when `version.txt` bumped | Same |
| Secrets | None in diff; no schema dumps with secrets | Same |
| Schema | No migrations/`schema.rb` authorship in this repo | Same |

---

## Code review (stream-api)

| Area | When to check |
|------|---------------|
| Auth / tokens | `Authorization: Api-Token`, UserToken / PlatformToken |
| IAP / TVOD | Optimistic accept (HTTP + job enqueue) vs async verification |
| Shared DB | No migrations; `_test` guards; postgres workflow docs |
| API contracts | Apipie / request specs vs OpenSpec product specs |
| Test coverage | SimpleCov 100% with documented skips only |
| Secrets | No `.env`, credentials, or keys in diff |

---

## Senior analysis tier signals (stream-api)

| Tier | When |
|------|------|
| **Deep** | Store entitlement semantics, auth/token flows, shared-DB coordination with web |
| **Light** | ≤ ~3 `tasks.md` sections, docs-only OpenSpec |
| **Skip** | Docs / OpenSpec planning only → point to `/lsi:review` |
