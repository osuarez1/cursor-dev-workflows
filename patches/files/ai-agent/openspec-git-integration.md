# OpenSpec + Git workflow (ai-agent)

**LSI overlay** for [cursor-dev-workflows](https://github.com/osuarez1/cursor-dev-workflows) v{{BUNDLE_VERSION}}. Generic workflow rules live in [which-workflow.md](which-workflow.md); this doc maps them to the **ai-agent** (monorepo: frontend + backend) repo.

## Quick reference (ai-agent)

| Concept | ai-agent |
|---------|----------|
| Scope ticket | OpenSpec change slug |
| Delivery ticket | Trello card (24-char id in branch) |
| Branch | `feature\|bugfix\|hotfix\|chore/{id}-<change-slug>` |
| Protected branches | **`main`**, **`staging`**, **`test`** |
| Source root | `frontend/`, `backend/` |
| Test command | `{{TEST_COMMAND}}` |
| PR host | Bitbucket — `lsistreaming/ai-agent` |

---

## Commit mapping (ai-agent)

| Area | Typical scope |
|------|---------------|
| Backend API / FastAPI routes | `feat(api):` / `fix(api):` |
| Frontend React / UI | `feat(ui):` / `fix(ui):` |
| Backend models / DB | `feat(model):` / `fix(model):` |
| LLM integration / prompts | `feat(llm):` / `fix(llm):` |
| Tests (frontend or backend) | `test(<scope>):` |
| OpenSpec / workflow docs | `docs(openspec):` / `chore(docs):` |
| CI / Bitbucket pipelines | `ci:` / `chore(ci):` |
| Release / version | `chore(release):` |

Optional footer: `Refs: openspec/changes/<change-slug>`

---

## PR production readiness (ai-agent)

| Check | Feature | Promotion |
|-------|---------|-----------|
| Branch | Ticket pattern; not `main`/`staging`/`test` | Ticket branch or **`staging`**; not `main` |
| Ticket match | Suffix matches `openspec/changes/<slug>/` | Same on ticket branch |
| Trello id | 24-char id in branch name | Same on ticket branch |
| Tests | `{{TEST_COMMAND}}` when `frontend/` or `backend/` changed | Same |
| Version | `scripts/check_version.py` when `VERSION` bumped | Same |
| Secrets | No `.env`, credentials, API keys in diff | Same |

---

## Code review (ai-agent)

| Area | When to check |
|------|---------------|
| LLM security | No prompt injection via user input; API keys not hardcoded |
| API contracts | Request/response shape consistent frontend ↔ backend |
| Frontend | Type safety, no console.error in production paths |
| Backend | FastAPI dependency injection, Pydantic schema correctness |
| Data handling | No PII logged; proper sanitization |
| Test coverage | `{{TEST_COMMAND}}` passes; critical LLM paths mocked |

---

## Senior analysis tier signals (ai-agent)

| Tier | When |
|------|------|
| **Deep** | New LLM integration, multi-service contract change, auth flow |
| **Light** | ≤ ~3 `tasks.md` sections, UI-only changes |
| **Skip** | Docs / OpenSpec only → point to `/lsi:review` |
