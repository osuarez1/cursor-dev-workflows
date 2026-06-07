# Test requirements (web)

See core bundle policy; web-specific commands from [PROJECT.md](../../PROJECT.md):

- `TEST_COMMAND`: `bin/check-schema-sync && bin/rspec-changed`
- `TEST_ROOT`: `spec/`

Schema changes require `db/schema.rb` updates and migration review.
