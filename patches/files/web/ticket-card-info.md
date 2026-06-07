# Ticket card info (web)

See core [ticket-card-info.md](../../docs/workflows/ticket-card-info.md) for field format.

## Web-specific technical notes

- Stack: Ruby on Rails, PostgreSQL, Sidekiq
- Local tests: `bin/check-schema-sync && bin/rspec-changed`
- Docker: see `AGENTS.md` domain section
