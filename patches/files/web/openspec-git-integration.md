# OpenSpec + Git workflow (web)

**LSI overlay** for [cursor-dev-workflows](https://github.com/osuarez1/cursor-dev-workflows) v{{BUNDLE_VERSION}}. Generic workflow rules live in [which-workflow.md](which-workflow.md); this doc maps them to the **web** (Rails) repo.

## Quick reference (web)

| Concept | web |
|---------|-----|
| Scope ticket | OpenSpec change slug |
| Delivery ticket | Trello card (24-char id in branch) |
| Branch | `feature\|bugfix\|hotfix\|chore/{id}-<change-slug>` |
| Protected branches | **`main`**, **`staging`**, **`master`** |
| Source root | `app/`, `lib/` |
| Test command | `{{TEST_COMMAND}}` |
| PR host | Bitbucket — `lsistreaming/web` |

---

## Commit mapping (web)

Map tasks.md sections to Conventional Commits scopes:

| Area | Typical scope |
|------|---------------|
| Rails controllers / routes | `feat(api):` / `fix(api):` |
| Models / ActiveRecord | `feat(model):` / `fix(model):` |
| Database migrations | `feat(db):` / `fix(db):` |
| Views / ERB / frontend assets | `feat(ui):` / `fix(ui):` |
| RSpec tests | `test(<scope>):` |
| OpenSpec / workflow docs | `docs(openspec):` / `chore(docs):` |
| CI / Bitbucket pipelines | `ci:` / `chore(ci):` |
| Release / version | `chore(release):` |
| Schema / DB migrations | `feat(schema):` / `fix(schema):` |

Optional footer: `Refs: openspec/changes/<change-slug>`

---

## PR production readiness (web)

| Check | Feature | Promotion |
|-------|---------|-----------|
| Branch | Ticket pattern; not `main`/`staging`/`master` | Ticket branch or **`staging`**; not `main` |
| Ticket match | Suffix matches `openspec/changes/<slug>/` | Same on ticket branch |
| Trello id | 24-char id in branch name | Same on ticket branch |
| Tests | `{{TEST_COMMAND}}` when `app/` or `lib/` or `spec/` changed | Same |
| Version | `scripts/check_version.py` when `version.txt` bumped | Same |
| Secrets | None in diff | Same |

---

## Code review (web)

| Area | When to check |
|------|---------------|
| Rails security | `before_action`, mass assignment, strong parameters, `permit!` |
| Database | Migration reversibility, index coverage, `NOT NULL` without default |
| API contracts | Request/response shape vs `docs/contracts/` |
| Schema sync | `bin/check-schema-sync` passes |
| Test coverage | `{{TEST_COMMAND}}` passes; critical paths have spec |
| Secrets | No `.env`, credentials, or keys in diff |

---

## Senior analysis tier signals (web)

| Tier | When |
|------|------|
| **Deep** | Schema migration on large table, multi-service API contract change, auth flow |
| **Light** | ≤ ~3 `tasks.md` sections, UI-only changes |
| **Skip** | Docs / OpenSpec only → point to `/lsi:review` |
