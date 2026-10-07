# Ticket card info (cs-chatbot)

See core field format in bundle `docs/workflows/ticket-card-info.md`.

## Repo-specific technical notes

- Stack: `frontend/` Next.js · `backend/` Rails · `intelligence/` FastAPI+uv (+ Streamlit ops UI) · `ingestion/` offline; Postgres+pgvector; OpenSpec at repo root
- Call path: Frontend → Backend → Intelligence; escalate persist on Backend only
- Decision log: root `DECISIONS.md` (Accepted only with evidence + course/OpenSpec cites)
- Local tests: see `PROJECT.md` `TEST_COMMAND` (`uv run pytest`)
- `/lsi:card` branch suffix = OpenSpec change slug (kebab-case)
- `/lsi:card-link`, `/lsi:trello-branch`, `/lsi:trello-list` (confirm) require open OpenSpec — card body from `proposal.md` / `tasks.md`, redacted before Trello
- Primary knowledge: call recordings; Freshdesk canned is supplemental; refunds always escalate
