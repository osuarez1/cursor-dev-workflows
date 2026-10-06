# OpenSpec + Git workflow (search-service)

**LSI overlay** for [cursor-dev-workflows](https://github.com/osuarez1/cursor-dev-workflows) v{{BUNDLE_VERSION}}. Generic workflow rules live in [which-workflow.md](which-workflow.md); this doc maps them to the **search-service** (Go / Typesense indexer) repo.

## Quick reference (search-service)

| Concept | search-service |
|---------|----------------|
| Scope ticket | OpenSpec change slug |
| Delivery ticket | Trello card (24-char id in branch) |
| Branch | `feature\|bugfix\|hotfix\|chore/{id}-<change-slug>` |
| Protected branches | **`main`**, **`staging`** |
| Source root | repo root (`main.go`, handlers) |
| Test root | repo root (`main_test.go`) |
| Test command | `{{TEST_COMMAND}}` |
| PR host | Bitbucket — `lsistreaming/search-service` |

---

## Commit mapping (search-service)

| Area | Typical scope |
|------|---------------|
| HTTP handlers (`/index`, `/health`) | `feat(api):` / `fix(api):` |
| Config / env loading | `feat(config):` / `fix(config):` |
| Typesense schema / collection | `feat(schema):` / `fix(schema):` |
| MovieDoc / indexing payload | `feat(indexing):` / `fix(indexing):` |
| Service lifecycle / timeouts | `feat(server):` / `fix(server):` |
| Tests | `test(<scope>):` |
| OpenSpec / workflow docs | `docs(openspec):` / `chore(docs):` |
| Docker / build | `build:` / `chore(docker):` |
| CI / Bitbucket pipelines | `ci:` / `chore(ci):` |
| Release / version | `chore(release):` |

Optional footer: `Refs: openspec/changes/<change-slug>`

---

## PR production readiness (search-service)

| Check | Feature | Promotion |
|-------|---------|-----------|
| Branch | Ticket pattern; not `main`/`staging` | Ticket branch or **`staging`**; not `main` |
| Ticket match | Suffix matches `openspec/changes/<slug>/` when OpenSpec change exists | Same on ticket branch |
| Trello id | 24-char id in branch name | Same on ticket branch |
| Tests | `{{TEST_COMMAND}}` when `*.go` or tests changed | Same |
| Version | `scripts/check_version.py` when `version.txt` bumped | Same |
| Secrets | No `.env`, Typesense keys, or `INDEX_AUTH_TOKEN` values in diff | Same |

---

## Code review (search-service)

| Area | When to check |
|------|---------------|
| Indexing API | `POST /index` — auth (`X-Index-Token`), body size, JSON validation, upsert errors |
| Health | `GET /health` — Typesense probe timeout and 503 contract |
| Schema | `ensureSchema` / `movies` collection fields vs `MovieDoc` producers (Rails) |
| Config | Env defaults and production warnings for missing keys/tokens |
| Security | No committed secrets; indexing auth when `INDEX_AUTH_TOKEN` set |
| Tests | `{{TEST_COMMAND}}` covers handler success and failure paths |

---

## Senior analysis tier signals (search-service)

| Tier | When |
|------|------|
| **Deep** | Schema migrations, auth model changes, request-size / timeout hardening, or multi-capability OpenSpec change |
| **Light** | ≤ ~3 `tasks.md` sections |
| **Skip** | Docs / OpenSpec only → point to `/lsi:review` |
