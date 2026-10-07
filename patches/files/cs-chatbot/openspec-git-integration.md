# OpenSpec + Git workflow (cs-chatbot)

**LSI overlay** for [cursor-dev-workflows](https://github.com/osuarez1/cursor-dev-workflows) v{{BUNDLE_VERSION}}. Generic workflow rules live in [which-workflow.md](which-workflow.md); this doc maps them to the **cs-chatbot** repo (Living Scriptures+ customer-service agent).

## Quick reference (cs-chatbot)

| Concept | cs-chatbot |
|---------|-----------|
| Scope ticket | OpenSpec change slug |
| Delivery ticket | Trello card (24-char id in branch) |
| Branch | `feature\|bugfix\|hotfix\|chore/{id}-<change-slug>` |
| Protected branches | **`main`**, **`staging`** |
| Source roots | `frontend/`, `backend/`, `intelligence/`, `ingestion/` |
| Test command | `{{TEST_COMMAND}}` |
| PR host | Bitbucket — `lsistreaming/cs-chatbot` |
| Decision log | Root [`DECISIONS.md`](../../DECISIONS.md) |

### Tier layout

| Tier | Path | Stack | Role |
|------|------|-------|------|
| Frontend | `frontend/` | Next.js, React, Tailwind | Customer UI — calls **Backend only** |
| Backend | `backend/` | Rails API-only | Business logic, auth, cancel/HITL, escalation **SoR**; brokers Intelligence |
| Intelligence | `intelligence/` | FastAPI + uv | LLM/RAG/agents; Streamlit **ops UI/dashboard** |
| Ingestion | `ingestion/` | Python + uv | Offline catalog → clean → PII → embed → index |

**Call path:** Frontend → Backend → Intelligence. Frontend never calls intelligence or ingestion. Intelligence may **propose** escalate; Backend **persists** escalations.

---

## Commit mapping (cs-chatbot)

| Area | Typical scope |
|------|---------------|
| Frontend Next.js / React | `feat(frontend):` / `fix(frontend):` |
| Backend Rails API / policy | `feat(backend):` / `fix(backend):` |
| Intelligence FastAPI / LLM | `feat(intelligence):` / `fix(intelligence):` |
| Ingest / ASR / embeddings | `feat(ingest):` / `fix(ingest):` |
| Retrieval / RAG / CAG | `feat(rag):` / `fix(rag):` |
| Actions / tools / escalation | `feat(actions):` / `fix(actions):` |
| Streamlit ops UI | `feat(ops-ui):` / `fix(ops-ui):` |
| Tests | `test(<tier>):` |
| OpenSpec / DECISIONS / workflow docs | `docs(openspec):` / `chore(docs):` |
| CI / Bitbucket pipelines | `ci:` / `chore(ci):` |
| Release / version | `chore(release):` |

Optional footer: `Refs: openspec/changes/<change-slug>`

---

## PR production readiness (cs-chatbot)

| Check | Feature | Promotion |
|-------|---------|-----------|
| Branch | Ticket pattern; not `main`/`staging` | Ticket branch or **`staging`**; not `main` |
| Ticket match | Suffix matches `openspec/changes/<slug>/` | Same on ticket branch |
| Trello id | 24-char id in branch name | Same on ticket branch |
| Tests | `{{TEST_COMMAND}}` when any tier under `SOURCE_ROOT` changed | Same |
| Version | `scripts/check_version.py` when `VERSION` bumped | Same |
| Secrets | No `.env`, credentials, API keys, call audio, or PII maps in diff | Same |
| Tier boundaries | No Frontend → Intelligence; Backend brokers; escalate persist on Backend | Same |
| Decision governance | New Accepted ADRs have evidence + accurate course/OpenSpec cites + Recorded datetime | Same |

---

## Code review (cs-chatbot)

| Area | When to check |
|------|---------------|
| Customer-facing safety | Abstention/escalation paths; no cross-customer PII in answers or logs |
| Actions | Cancel gated + HITL on Backend; refund always escalates; intelligence only proposes escalate |
| Knowledge | Calls primary; canned supplemental; citations safe |
| LLM security | No prompt injection via user input; API keys from env only |
| Stack | Rails in `backend/`; uv-only in `intelligence/` + `ingestion/`; Next.js in `frontend/` |
| Test coverage | `{{TEST_COMMAND}}` passes; LLM/provider calls mocked in unit tests |

---

## Senior analysis tier signals (cs-chatbot)

| Tier | When |
|------|------|
| **Deep** | Cross-tier contract, new action tool, retrieval architecture, PII pipeline, auth/account integration |
| **Light** | ≤ ~3 `tasks.md` sections, single-tier UI or prompt-only |
| **Skip** | Docs / OpenSpec / DECISIONS-only → point to `/lsi:review` |
