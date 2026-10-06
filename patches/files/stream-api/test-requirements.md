# Test requirements (stream-api)

See core bundle policy; stream-api-specific commands from [PROJECT.md](../../PROJECT.md):

- `TEST_COMMAND`: `bundle exec rspec`
- Coverage gate: `COVERAGE=1 bundle exec rspec` (SimpleCov `minimum_coverage 100`)
- `TEST_ROOT`: `spec/`
- Test DB bootstrap: `bin/setup-test-databases` (alias `bin/setup-test-db`); diagnose: `bin/diagnose-test-databases`
- Local DB: host Postgres.app, shared `lsistreaming_test` / user `livingscriptures` — see `docs/workflows/postgres-app-test-database.md`
- CI: Bitbucket **RSpec + Coverage** uses Docker Postgres 15 + Redis; loads `db/structure.sql` by default (`bin/refresh-ci-schema`); optional secured `DATABASE_SCHEMA_SQL` / `DATABASE_SCHEMA_URL` override

Never run migrations in this repo; schema is owned by web.
