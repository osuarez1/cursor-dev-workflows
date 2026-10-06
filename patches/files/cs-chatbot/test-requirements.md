# Test requirements (cs-chatbot)

Policy from bundle `docs/workflows/test-requirements.md`; commands from [PROJECT.md](../../PROJECT.md):

- `TEST_COMMAND`: `uv run pytest`
- `TEST_ROOT`: `tests/`

Run affected tests when `app/` or `tests/` change. Mock LLM/provider calls in unit tests; keep golden/eval sets out of secret-bearing fixtures.
