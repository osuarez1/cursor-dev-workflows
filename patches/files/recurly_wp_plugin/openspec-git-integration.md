# OpenSpec + Git workflow (recurly_wp_plugin)

**LSI overlay** for [cursor-dev-workflows](https://github.com/osuarez1/cursor-dev-workflows) v{{BUNDLE_VERSION}}. Generic workflow rules live in [which-workflow.md](which-workflow.md); this doc maps them to the **recurly_wp_plugin** (WordPress Recurly checkout) repo.

## Quick reference (recurly_wp_plugin)

| Concept | recurly_wp_plugin |
|---------|-------------------|
| Scope ticket | OpenSpec change slug |
| Delivery ticket | Trello card (24-char id in branch) |
| Branch | `feature\|bugfix\|hotfix\|chore/{id}-<change-slug>` |
| Protected branches | **`main`**, **`staging`**, **`master`** (legacy default) |
| Source root | `includes/`, `admin/`, `public/`, `wp-lsi-recurly.php` |
| Test root | `tests/` (reserved) |
| Test command | `{{TEST_COMMAND}}` |
| PR host | Bitbucket — `lsistreaming/recurly_wp_plugin` |

---

## Commit mapping (recurly_wp_plugin)

| Area | Typical scope |
|------|---------------|
| Checkout forms / Recurly.js | `feat(checkout):` / `fix(checkout):` |
| Shortcodes | `feat(shortcodes):` / `fix(shortcodes):` |
| Admin settings / geo / ImageIt | `feat(admin):` / `fix(admin):` |
| Site utilities (cache, redirects, analytics) | `feat(site):` / `fix(site):` |
| Security / reCAPTCHA / allowlists | `feat(security):` / `fix(security):` |
| Stream backend payload / auth contracts | `feat(stream):` / `fix(stream):` |
| GeoIP / redirects | `feat(geo):` / `fix(geo):` |
| OpenSpec / workflow docs | `docs(openspec):` / `chore(docs):` |
| Composer / npm assets | `build:` / `chore(deps):` |
| CI / Bitbucket pipelines | `ci:` / `chore(ci):` |
| Release / version | `chore(release):` |

Optional footer: `Refs: openspec/changes/<change-slug>`

---

## PR production readiness (recurly_wp_plugin)

| Check | Feature | Promotion |
|-------|---------|----------|
| Branch | Ticket pattern; not `main`/`staging`/`master` | Ticket branch or **`staging`**; not `main` |
| Ticket match | Suffix matches `openspec/changes/<slug>/` when OpenSpec change exists | Same on ticket branch |
| Trello id | 24-char id in branch name | Same on ticket branch |
| Tests | `{{TEST_COMMAND}}` when PHP/JS under source roots change; manual checkout verify when UI/partials change | Same |
| OpenSpec | `openspec validate --strict` when specs change | Same |
| Version | `scripts/check_version.py` when `version.txt` bumped; keep plugin header in sync | Same |
| Secrets | No Recurly private keys, GeoIP DB paths with secrets, or stream credentials in diff | Same |

---

## Code review (recurly_wp_plugin)

| Area | When to check |
|------|---------------|
| Checkout modes | Paid, gift buy/redeem, sales-rep, free, upgrade, TVOD — shared partials stay in sync |
| Recurly.js | Tokenization stays browser-side; no new server-side Recurly PHP API unless intentional |
| Stream contracts | Payload/query flags for `stream.livingscriptures.com` (staging/ngrok variants) |
| Shortcodes / page detection | Slug and attribute contracts remain stable |
| Admin | Settings → LSI Recurly; `admin_post` handlers and capability checks |
| Security | Tokens, reCAPTCHA, IP allowlists, no secret leakage |
| Specs | Align with `openspec/specs/<capability>/spec.md` |

---

## Senior analysis tier signals (recurly_wp_plugin)

| Tier | When |
|------|------|
| **Deep** | Stream backend contract changes, checkout auth/security, multi-mode shared partial refactors, or multi-capability OpenSpec change |
| **Light** | ≤ ~3 `tasks.md` sections |
| **Skip** | Docs / OpenSpec only → point to `/lsi:review` |
