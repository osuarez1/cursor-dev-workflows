## Context

`snippets/adopt.py` assembles `.lsi/workflows/` from three sources:

1. **Core bundle** — `docs/workflows/*.md`, root `which-workflow.md`, `templates/`, `examples/`, `docs/adopt-and-update.md`
2. **LSI overlay** — `overlays/lsi/docs/workflows/*.md`, `sdlc/`, `docs/ai/` (to repo `docs/ai/`)
3. **Link rewrites** — `LINK_REWRITES` regex table strips `docs/workflows/` prefixes and remaps some bundle paths

Recent overlay work (card-link, Trello flows, `/lsi:update`, branch-workflow, OpenSpec integration, `AGENTS.md`, `docs/ai/openspec.md`) added links authored for **maintainer navigation** (`../../overlays/lsi/docs/…`, `../../agent-stack/commands/lsi-help.md`, `../../../docs/adopt-and-update.md`). Those paths are valid in `cursor-dev-workflows` but break after copy to `.lsi/workflows/` in adopters. `verify-adopters.py` delegates to `adoption-verify-links.py`, which fails the adopter parity gate.

Current rewrites do not cover overlay paths, agent-stack paths, or `docs/adopt-and-update.md` maintainer-only sections (CI snippets, `MAINTAINER.md.example`, `patches/README.md`, `adopt-new-repo.md`).

## Goals / Non-Goals

**Goals:**

- Zero broken relative links in `.lsi/workflows/**/*.md` after adopt
- Fix root cause in bundle sources so maintainers edit links once
- Bundle-side regression test (adopt → verify) before adopter re-sync
- Minimal adopter churn — re-sync only, no hand-edits under `.lsi/workflows/`

**Non-Goals:**

- Rewriting `/lsi:help` GitHub blob URLs (already adopter-safe)
- Link-checking `.cursor/commands/*.md` or `.mdc` rules (out of verify scope today)
- External URL reachability
- Retrofitting Profile A/B layouts

## Decisions

### 1. Adopter-shaped source for `adopt-and-update.md`

**Choice:** Add `overlays/lsi/adopter-docs/adopt-and-update.md` written for `.lsi/workflows/` layout; `copy_core_bundle()` copies this file instead of `docs/adopt-and-update.md`. Keep `docs/adopt-and-update.md` as the maintainer-facing superset (may link to bundle paths freely).

**Rationale:** `adopt-and-update.md` has the most maintainer-only links. A dedicated adopter copy avoids regex whack-a-mole and matches the user's "source folder that matches the adopter tree" idea.

**Alternatives considered:**

- *Expand `LINK_REWRITES` only* — fragile; every new maintainer link needs a new regex
- *Copy `docs/ci/` into `.lsi/workflows/ci/`* — works for CI snippets but not for `patches/` or `MAINTAINER.md`

**Adopter copy content:**

| Maintainer link | Adopter replacement |
|-----------------|---------------------|
| `ci/check_version-web.yml` | Copy `docs/ci/check_version-*.yml` → `.lsi/workflows/ci/` and link `ci/check_version-web.yml` |
| `../MAINTAINER.md.example` | Prose: "see bundle maintainer `MAINTAINER.md`" — no link, or link to `adopt-and-update.md` § bundle update |
| `adopt-new-repo.md` | Inline summary + "contact bundle maintainer to register patch" — no broken relative link |
| `../patches/README.md` | Remove link; adopter uses `/lsi:update`, not patch registry |

### 2. Fix overlay and core workflow cross-links at source

**Choice:** Edit source files so links match **post-adopt** locations:

| File | Fix |
|------|-----|
| `docs/workflows/integrations.md` | `openspec-git-integration.md` (sibling) |
| `docs/workflows/ticket-card-info.md` | `openspec-git-integration.md` (sibling) |
| `docs/workflows/branch-workflow.md` | `git-trello.md` → `sdlc/git-trello.md` |
| `overlays/lsi/docs/workflows/which-workflow.md` | `lsi-help.md` → `../../.cursor/commands/lsi-help.md`; `adopt-and-update.md` → `adopt-and-update.md` |
| Root `which-workflow.md` (LSI row) | `openspec-git-integration.md` overlay note — use sibling name only in overlay copy; bundle root may keep maintainer path for dogfood |

Overlay `which-workflow.md` **overwrites** core router via `merge_which_workflow_lsi()` — fix the overlay file as primary.

### 3. Extend `LINK_REWRITES` as safety net

**Choice:** Add catch-all rewrites in `adopt.py` for paths that may reappear:

```python
(r"\]\(\.\./\.\./overlays/lsi/docs/workflows/", "](",),
(r"\]\(\.\./\.\./overlays/lsi/docs/sdlc/", "](sdlc/",),
(r"\]\(\.\./\.\./agent-stack/commands/", "](../../.cursor/commands/",),
(r"\]\(\.\./\.\./\.\./docs/adopt-and-update\.md\)", "](adopt-and-update.md)"),
```

**Rationale:** Belt-and-suspenders if a maintainer path slips into a shared doc. Rewrites run on every copied file.

### 4. Bundle regression: `test_adopt_links.py`

**Choice:** New unittest that:

1. Creates temp dir with minimal adopter skeleton (`PROJECT.md`, patch config from `_template.yaml`)
2. Runs `adopt.py --target <tmp> --config patches/_template.yaml --accept-policy-defaults` (or invokes `copy_core_bundle` + `copy_overlay` helpers if full adopt is heavy)
3. Runs `adoption-verify-links.verify()` and asserts `broken == []`
4. Optionally asserts no `overlays/lsi/` or `agent-stack/` substrings in `.lsi/workflows/**/*.md`

**Alternatives considered:**

- *Fixture-only static files* — does not catch transform regressions in `adopt.py`
- *Run verify-adopters on real adopters in CI* — out of bundle repo scope; keep as maintainer post-release step

### 5. Optional pattern rule in `adoption-verify-links.py`

**Choice:** Add pattern violations for `](overlays/lsi/` and `](agent-stack/` inside canonical tree (same severity as doubled `docs/workflows/` prefix).

**Rationale:** Clearer failure message than "file not found"; documents intent in [adoption-verify-architecture.md](../../docs/adoption-verify-architecture.md).

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Dual `adopt-and-update.md` copies diverge | Adopter copy is short; maintainer doc links to it; test asserts adopter copy links |
| `.cursor/commands/` missing during verify if adopt partial | Regression test runs full adopt install including agent stack |
| Rewrites mask bad source links silently | Pattern rule + substring assertion in test |
| CI snippet copy duplicates bundle | Small YAML files; versioned with bundle; acceptable |

## Migration Plan

1. Implement bundle fixes on feature branch (`chore/bundle-fix-adopter-link-drift` or similar — **not on `main`**).
2. Bump `VERSION` / `CHANGELOG.md` with adopter re-sync note.
3. Maintainer adopt loop: re-sync each registered adopter; `verify-adopters.py --repo-root <adopter>` must pass.
4. Rollback: revert bundle release; adopters keep previous `.lsi/workflows/` until re-sync.

## Open Questions

- Should `docs/ai/openspec.md` links be scanned via `--extra-dirs docs/ai` in verify-adopters? (Currently only `.lsi/workflows/` + `AGENTS.md` — `openspec.md` uses `../workflows/` paths that resolve in adopter `docs/ai/`. Confirm in apply task.)
- Copy both CI snippets to `.lsi/workflows/ci/` or only the one referenced in each adopter's patch overlay?
