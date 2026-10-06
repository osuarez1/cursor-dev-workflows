# OpenSpec + Git workflow (office-assistant)

**LSI overlay** for [cursor-dev-workflows](https://github.com/osuarez1/cursor-dev-workflows) v{{BUNDLE_VERSION}}. Generic workflow rules live in [which-workflow.md](which-workflow.md); this doc maps them to the **office-assistant** monorepo.

## Quick reference (office-assistant)

| Concept | office-assistant |
|---------|------------------|
| Scope ticket | OpenSpec change slug |
| Delivery ticket | Trello card (24-char id in branch) |
| Branch | `feature\|bugfix\|hotfix\|chore/{id}-<change-slug>` |
| Protected branches | **`main`**, **`staging`** |
| Source roots | `frontend/`, `backend/`, `intelligence/` |
| Test command | `{{TEST_COMMAND}}` |
| PR host | Bitbucket — `lsistreaming/office-assistant` |

### Tier layout

| Tier | Path | Stack |
|------|------|-------|
| Frontend | `frontend/` | Next.js 16, React 19, Tailwind 4 — internal control plane |
| Backend | `backend/` | Rails API-only — orchestrator, auth, business data |
| Intelligence | `intelligence/` | Python 3.14 + uv, FastAPI — LLM/agent operations |

**Call path:** Frontend → Backend → Intelligence only. Frontend must never call Intelligence directly.

Constitution and cross-tier rules: [`openspec/project.md`](../../openspec/project.md).

---

## Commit mapping (office-assistant)

| Area | Typical scope |
|------|---------------|
| Frontend UI / Next.js | `feat(frontend):` / `fix(frontend):` |
| Backend API / Rails | `feat(backend):` / `fix(backend):` |
| Intelligence / FastAPI / LLM | `feat(intelligence):` / `fix(intelligence):` |
| Docker / compose / infra | `chore(infra):` / `fix(infra):` |
| Tests (any tier) | `test(<tier>):` |
| OpenSpec / workflow docs | `docs(openspec):` / `chore(docs):` |
| CI / Bitbucket pipelines | `ci:` / `chore(ci):` |
| Release / version | `chore(release):` |

Optional footer: `Refs: openspec/changes/<change-slug>`

---

## PR production readiness (office-assistant)

| Check | Feature | Promotion |
|-------|---------|-----------|
| Branch | Ticket pattern; not `main`/`staging` | Ticket branch or **`staging`**; not `main` |
| Ticket match | Suffix matches `openspec/changes/<slug>/` | Same on ticket branch |
| Trello id | 24-char id in branch name | Same on ticket branch |
| Tests | `{{TEST_COMMAND}}` when any of `frontend/`, `backend/`, `intelligence/` changed | Same |
| Version | `scripts/check_version.py` when `VERSION` bumped | Same |
| Secrets | No `.env`, credentials, API keys in diff | Same |
| Tier boundaries | No Frontend → Intelligence calls; Backend brokers Intelligence | Same |

---

## Code review (office-assistant)

| Area | When to check |
|------|---------------|
| Tier boundaries | Frontend uses `NEXT_PUBLIC_API_URL` only; Backend uses `INTELLIGENCE_API_URL` for Intelligence |
| Intelligence | uv-only deps; Alembic touches `assistant_intelligence_dev` only |
| Backend | Rails API-only; migrations touch `assistant_backend_dev` only |
| Frontend | App Router only; strict TypeScript |
| LLM security | No prompt injection via user input; API keys not hardcoded |
| Auth / data | No PII logged; secrets from env only |
| Test coverage | `{{TEST_COMMAND}}` passes for touched tiers |

---

## Senior analysis tier signals (office-assistant)

| Tier | When |
|------|------|
| **Deep** | Cross-tier contract change, auth flow, new agent orchestration, database ownership change |
| **Light** | ≤ ~3 `tasks.md` sections, single-tier UI or API change |
| **Skip** | Docs / OpenSpec only → point to `/lsi:review` |
