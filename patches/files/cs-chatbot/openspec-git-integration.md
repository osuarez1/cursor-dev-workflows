# OpenSpec + Git workflow (cs-chatbot)

**LSI overlay** for [cursor-dev-workflows](https://github.com/osuarez1/cursor-dev-workflows) v{{BUNDLE_VERSION}}. Generic workflow rules live in [which-workflow.md](which-workflow.md); this doc maps them to the **cs-chatbot** repo (Living Scriptures+ customer-service agent).

## Quick reference (cs-chatbot)

| Concept | cs-chatbot |
|---------|-----------|
| Scope ticket | OpenSpec change slug |
| Delivery ticket | Trello card (24-char id in branch) |
| Branch | `feature\|bugfix\|hotfix\|chore/{id}-<change-slug>` |
| Protected branches | **`main`**, **`staging`** |
| Source root | `app/` |
| Test command | `{{TEST_COMMAND}}` |
| PR host | Bitbucket — `lsistreaming/cs-chatbot` |
| Decision log | Root [`DECISIONS.md`](../../DECISIONS.md) |

---

## Commit mapping (cs-chatbot)

| Area | Typical scope |
|------|---------------|
| FastAPI routes / service layer | `feat(api):` / `fix(api):` |
| Ingest / ASR / embeddings | `feat(ingest):` / `fix(ingest):` |
| Retrieval / RAG / CAG | `feat(rag):` / `fix(rag):` |
| LLM prompts / structured output | `feat(llm):` / `fix(llm):` |
| Actions / tools / escalation | `feat(actions):` / `fix(actions):` |
| Streamlit / client UI | `feat(ui):` / `fix(ui):` |
| Tests | `test(<scope>):` |
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
| Tests | `{{TEST_COMMAND}}` when `app/` or `tests/` changed | Same |
| Version | `scripts/check_version.py` when `VERSION` bumped | Same |
| Secrets | No `.env`, credentials, API keys, call audio, or PII maps in diff | Same |
| Decision governance | New Accepted ADRs have evidence + accurate course/OpenSpec cites | Same |

---

## Code review (cs-chatbot)

| Area | When to check |
|------|---------------|
| Customer-facing safety | Abstention/escalation paths; no cross-customer PII in answers or logs |
| Actions | Cancel gated + HITL as required; refund always escalates (no auto-refund) |
| Knowledge | Calls primary; canned supplemental; citations safe |
| LLM security | No prompt injection via user input; API keys from env only |
| Stack | uv-only Python deps; FastAPI layered under `app/` |
| Test coverage | `{{TEST_COMMAND}}` passes; LLM/provider calls mocked in unit tests |

---

## Senior analysis tier signals (cs-chatbot)

| Tier | When |
|------|------|
| **Deep** | New action tool, retrieval architecture change, PII pipeline, auth/account integration |
| **Light** | ≤ ~3 `tasks.md` sections, prompt-only or UI-only |
| **Skip** | Docs / OpenSpec / DECISIONS-only → point to `/lsi:review` |
