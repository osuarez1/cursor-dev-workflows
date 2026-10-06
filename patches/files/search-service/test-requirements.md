# Test requirements (search-service)

Policy from bundle `docs/workflows/test-requirements.md`; commands from [PROJECT.md](../../PROJECT.md):

- `TEST_COMMAND`: `go test ./...`
- `TEST_ROOT`: `.` (table-driven tests in `main_test.go`)
- `SOURCE_ROOT`: `.` (`main.go` and related packages at repo root)

## When tests are required

- Changes to HTTP handlers, config loading, schema ensure, or Typesense client usage **must** update or add Go tests under the repo root.
- Prefer httptest mocks for Typesense (existing pattern in `main_test.go`).
- Run `go test ./...` before opening a PR when `*.go` files change.
