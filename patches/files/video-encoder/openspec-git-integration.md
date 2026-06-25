# OpenSpec + Git workflow (video-encoder)

**LSI overlay** for [cursor-dev-workflows](https://github.com/osuarez1/cursor-dev-workflows) v{{BUNDLE_VERSION}}. Generic workflow rules live in [which-workflow.md](which-workflow.md); this doc maps them to the **video-encoder** (Python worker) repo.

## Quick reference (video-encoder)

| Concept | video-encoder |
|---------|---------------|
| Scope ticket | OpenSpec change slug |
| Delivery ticket | Trello card (24-char id in branch) |
| Branch | `feature\|bugfix\|hotfix\|chore/{id}-<change-slug>` |
| Protected branches | **`main`**, **`staging`** |
| Source root | `src/` |
| Test root | `tests/` |
| Test command | `{{TEST_COMMAND}}` |
| PR host | Bitbucket — `lsistreaming/video-encoder` |

---

## Commit mapping (video-encoder)

| Area | Typical scope |
|------|---------------|
| Worker / `main.py` | `feat(worker):` / `fix(worker):` |
| FFmpeg / HLS pipeline | `feat(ffmpeg):` / `fix(ffmpeg):` |
| S3 / AWS CLI upload | `feat(s3):` / `fix(s3):` |
| Webhook / HTTP client | `feat(webhook):` / `fix(webhook):` |
| Contracts / job payload | `feat(contracts):` / `fix(contracts):` |
| Tests under `tests/` | `test(<scope>):` |
| OpenSpec / workflow docs | `docs(openspec):` / `chore(docs):` |
| CI / Bitbucket pipelines | `ci:` / `chore(ci):` |
| Release / version | `chore(release):` |

Optional footer: `Refs: openspec/changes/<change-slug>`

---

## PR production readiness (video-encoder)

| Check | Feature | Promotion |
|-------|---------|-----------|
| Branch | Ticket pattern; not `main`/`staging` | Ticket branch or **`staging`**; not `main` |
| Ticket match | Suffix matches `openspec/changes/<slug>/` | Same on ticket branch |
| Trello id | 24-char id in branch name | Same on ticket branch |
| Tests | `{{TEST_COMMAND}}` (`pytest`) when `src/` or `tests/` changed | Same |
| Version | `scripts/check_version.py` when `version.txt` bumped | Same |
| Secrets | No `.env`, credentials, `key.bin`, or keys in diff | Same |

---

## Code review (video-encoder)

| Area | When to check |
|------|---------------|
| FFmpeg / HLS | `ffmpeg_pipeline.py`, segment naming, encryption key consumption (no key generation) |
| Redis queue | BLPOP/BRPOP, job payload parsing, error handling |
| S3 / AWS CLI | `s3_manager.py` — `aws s3 sync` subprocess only; no boto3 bulk upload |
| Contracts | Payload shape vs `docs/contracts/`; webhook callbacks |
| Security | No secrets in repo; `tmp/` cleanup after job success/failure |
| Version scope | No V2/V3 modules (`workflow_executor`, multi-queue) during V1 tasks |
| Test coverage | `{{TEST_COMMAND}}` passes; 100% coverage on `src/` and `dev/` |

---

## Senior analysis tier signals (video-encoder)

| Tier | When |
|------|------|
| **Deep** | Worker runtime, FFmpeg pipeline changes, contracts, S3 upload, or multi-capability change |
| **Light** | ≤ ~3 `tasks.md` sections |
| **Skip** | Docs / OpenSpec only → point to `/lsi:review` |
