# Ticket card info (stream-api)

See core [ticket-card-info.md](../../docs/workflows/ticket-card-info.md) for field format.

## stream-api-specific technical notes

- Stack: Ruby 3.2 / Rails 7 API-only, PostgreSQL (shared `lsistreaming_*` with web), Redis, Sidekiq
- Local tests: `bundle exec rspec` (coverage: `COVERAGE=1 bundle exec rspec`)
- Test DB: Postgres.app via `bin/setup-test-databases` — see `docs/workflows/postgres-app-test-database.md`
- No migrations in this repo — schema owned by web
