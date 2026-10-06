# Ticket card info (recurly_wp_plugin)

See core field format in canonical `.lsi/workflows/ticket-card-info.md`.

## Repo-specific technical notes

- Stack: PHP (WordPress plugin), Recurly.js v4, MaxMind GeoIP2 (`maxmind-db/reader`), Foundation CSS/JS
- Plugin: Living Scriptures Inc - Recurly (`wp-lsi-recurly`); entry `wp-lsi-recurly.php`
- Role: WordPress checkout UI + site utilities; payment tokenization in-browser via Recurly.js; account/subscription posts to `stream.livingscriptures.com`
- No Recurly webhooks or server-side Recurly PHP API usage in application code
- Local smoke: see `PROJECT.md` `TEST_COMMAND` (`php -l wp-lsi-recurly.php`); no PHPUnit suite yet
- `/lsi:card` branch suffix = OpenSpec change slug (kebab-case)
- `/lsi:card-link`, `/lsi:trello-branch`, `/lsi:trello-list` (confirm) require open OpenSpec — card body from `proposal.md` / `tasks.md`, redacted before Trello
