# Ticket card info (search-service)

See core field format in bundle `docs/workflows/ticket-card-info.md`.

## Repo-specific technical notes

- Stack: Go 1.25, Typesense (`typesense-go`), stdlib `net/http`, Alpine multi-stage Docker
- Service role: indexing sidecar — `POST /index`, `GET /health` (not end-user search queries)
- Collection: Typesense `movies`; documents align with Rails `searchable_objects` / `MovieDoc`
- Env: `TYPESENSE_URL`, `TYPESENSE_API_KEY`, `INDEX_AUTH_TOKEN` (optional; requires `X-Index-Token`)
- Production: ECS `go-search-service` + `typesense` on cluster `production` (`us-east-1`); ECR `lsistreaming/go-search-service:latest`
- Local tests: see `PROJECT.md` `TEST_COMMAND` (`go test ./...`)
- `/lsi:card` branch suffix = OpenSpec change slug (kebab-case)
- `/lsi:card-link`, `/lsi:trello-branch`, `/lsi:trello-list` (confirm) require open OpenSpec — card body from `proposal.md` / `tasks.md`, redacted before Trello
