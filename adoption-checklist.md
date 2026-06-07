# Adoption checklist

## LSI adopters (recommended)

Use **`snippets/adopt.py`** — do not hand-copy bundle files. Full guide: [docs/adopt-new-repo.md](docs/adopt-new-repo.md).

- [ ] Create `patches/<repo>.yaml` from [patches/_template.yaml](patches/_template.yaml)
- [ ] `adopt.py --audit-only` → resolve → adopt → `verify-adopters.py`
- [ ] Wire `check_version.py` in CI ([docs/ci/](docs/ci/))
- [ ] App-repo PR with audit summary

Registered repos: [patches/README.md](patches/README.md). Layout: [docs/adoption-layout.md](docs/adoption-layout.md) (`.lsi/workflows/` only).

### Verify (required before merge)

From the **application repo root** — design reference: [docs/adoption-verify-architecture.md](docs/adoption-verify-architecture.md).

- [ ] `python3 snippets/adoption-verify-links.py --repo-root . --canonical .lsi/workflows` — exit code 0
- [ ] `python3 snippets/verify-adopters.py --repo-root .` — parity gate
- [ ] Agent smoke: route “code review” → `.lsi/workflows/code-review.md`; draft PR body includes **Potential risks**; refuse task work on `PROTECTED_BRANCHES`

On re-sync, update `BUNDLE_VERSION` in app `PROJECT.md`, read **Adopter action** in [CHANGELOG.md](CHANGELOG.md), and re-run verify.

---

## Legacy manual bootstrap (removed in v1.3.0)

Profile A/B hand-copy was retired in bundle **v1.3.0**. Use **`snippets/adopt.py`** above. Pre-1.3.0 checklist steps are in git history before the [1.3.0](CHANGELOG.md) release.

## Related

- [docs/adoption-layout.md](docs/adoption-layout.md) — LSI layout and link verification
- [docs/adoption-verify-architecture.md](docs/adoption-verify-architecture.md) — verification gate design reference
- [README.md](README.md)
- [integrations.md](docs/workflows/integrations.md)
