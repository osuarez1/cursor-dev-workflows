# Test requirements (recurly_wp_plugin)

Policy from canonical `.lsi/workflows/test-requirements.md`; commands from [PROJECT.md](../../PROJECT.md):

- `TEST_COMMAND`: `php -l wp-lsi-recurly.php` (syntax smoke only until a PHPUnit suite exists)
- `TEST_ROOT`: `tests/` (reserved; no automated suite yet)
- `SOURCE_ROOT`: `includes/`, `admin/`, `public/`, `wp-lsi-recurly.php`

## When tests / verification are required

- Checkout UI, shortcode, or public JS/partial changes: manual verify on a matching checkout page slug or shortcode (paid, gift, sales-rep, free, upgrade, TVOD as applicable).
- Shared form/JS partials: regression-check other checkout modes that share those partials.
- OpenSpec/spec edits: `openspec validate --strict`.
- Prefer adding automated tests under `tests/` when introducing non-trivial PHP logic; do not invent Recurly server-side PHP API or webhook coverage unless the change adds those surfaces.
