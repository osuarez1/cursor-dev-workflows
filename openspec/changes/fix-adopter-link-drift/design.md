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
- GitHub URLs for **tier 1** cross-spec links (installed workflow docs stay relative in-repo)
- Copying maintainer-only bundle docs into adopters just to satisfy link verify
- Expanding `LINK_REWRITES` as the primary link-fix strategy (regex whack-a-mole)

## Three-tier link policy

All content that `adopt.py` installs into adopters MUST follow this policy. Maintainer-only bundle docs (`docs/adopt-and-update.md`, `patches/README.md`, etc.) may use bundle layout paths freely.

| Tier | When | Link style | Examples |
|------|------|------------|----------|
| **1 — Installed, in daily use** | Target exists in adopter repo after full adopt; agents read it during workflow routing | **Relative path** valid from the containing file | `.lsi/workflows/` siblings (`openspec-git-integration.md`); cross-tree install paths (`../../.cursor/commands/lsi-help.md`, `../../.lsi/workflows/…` from `docs/ai/`) |
| **2 — Not installed (maintainer-only)** | Target never copied to adopter (`patches/`, `MAINTAINER.md`, `docs/adopt-new-repo.md`, bundle `overlays/lsi/…` navigation) | **GitHub blob URL** pinned to `v{{BUNDLE_VERSION}}`, or **plain prose** (no broken relative href) | `https://github.com/osuarez1/cursor-dev-workflows/blob/v{{BUNDLE_VERSION}}/docs/adopt-new-repo.md`; "contact bundle maintainer to register a patch" |
| **3 — Small install extras** | Adopters need a tiny artifact that is not a full spec; copying is cheaper than remote-only | **Copy into adopt output once**, then **tier 1 relative** link | Both `docs/ci/check_version-*.yml` → `.lsi/workflows/ci/`; adopter doc links `ci/check_version-web.yml` |

### Authoring rules

1. **Ask:** Does the target exist in the adopter tree after `adopt.py`? → tier **1** (relative). Does adopt install it elsewhere (`.cursor/`, `docs/ai/`)? → tier **1** with cross-tree relative path.
2. **Ask:** Is the target bundle-maintainer-only? → tier **2** (GitHub URL with `v{{BUNDLE_VERSION}}` substituted at adopt time, or prose — never `../patches/`, `../../overlays/lsi/`, etc.).
3. **Ask:** Is it a small file adopters must copy-paste (CI snippet)? → tier **3** (copy in `adopt.py`, link relatively from `.lsi/workflows/`).
4. **Do not** use GitHub URLs for tier 1 — adopted specs are local canon (`CANONICAL_DOCS_PATH=.lsi/workflows/`); relative links work offline and in IDE `@` navigation. `/lsi:help` chat output may use GitHub URLs (different consumer).
5. **Source layout:** Author tier 1 content under **`overlays/lsi/adopter-docs/`** when the bundle maintainer layout differs from the adopter layout (start with `adopt-and-update.md`; expand over time toward a full adopter-shaped tree).
6. **`LINK_REWRITES` are a transition aid, not primary authoring.** Fix links at source (decisions 1–2). Rewrites catch accidental bundle-layout hrefs during copy only. Pattern rules (decision 5) and regression tests (decision 4) enforce that maintainers cannot rely on rewrites as the main strategy.

### Verify gate alignment

| Check | Tier |
|-------|------|
| `adoption-verify-links.py` relative resolution under `.lsi/workflows/` | 1 + 3 |
| Pattern violations for `](overlays/lsi/` and `](agent-stack/` inside canonical tree | Blocks tier 2 mistakes smuggled as relative |
| `https://` links | Skipped by verify (tier 2 OK) |
| `--extra-dirs docs/ai` in verify-adopters | **Out of scope** for adopter parity default; **`test_adopt_links.py`** uses `extra_dirs=["docs/ai"]` to regression-test `openspec.md` cross-tree links after adopt |

## Decisions

### 1. Adopter-shaped source for `adopt-and-update.md` (tiers 1–3)

**Choice:** Add `overlays/lsi/adopter-docs/adopt-and-update.md` written for `.lsi/workflows/` layout following the **three-tier link policy**; `copy_core_bundle()` copies this file instead of `docs/adopt-and-update.md`. Keep `docs/adopt-and-update.md` as the maintainer-facing superset (may link to bundle paths freely). Add `overlays/lsi/adopter-docs/README.md` documenting the three tiers for future authors.

**Rationale:** `adopt-and-update.md` has the most tier 2 violations today. A dedicated adopter copy avoids regex whack-a-mole and is the first step toward a full adopter-shaped source tree.

**Alternatives considered:**

- *Expand `LINK_REWRITES` only* — fragile; every new maintainer link needs a new regex
- *Copy `docs/ci/` into `.lsi/workflows/ci/`* — works for CI snippets but not for `patches/` or `MAINTAINER.md`

**Adopter copy content:**

| Maintainer link | Tier | Adopter replacement |
|-----------------|------|---------------------|
| `ci/check_version-web.yml` | **3** | Copy **both** `docs/ci/check_version-web.yml` and `docs/ci/check_version-ai-agent.yml` unconditionally → `.lsi/workflows/ci/` during every adopt; adopter doc links both relatively |
| `../MAINTAINER.md.example` | **2** | Prose only — no relative link |
| `adopt-new-repo.md` | **2** | GitHub blob URL with `v{{BUNDLE_VERSION}}` or inline summary + "contact bundle maintainer" |
| `../patches/README.md` | **2** | Remove relative link; adopter uses `/lsi:update`; optional GitHub URL to bundle `patches/README.md` |

### 2. Fix overlay and core workflow cross-links at source (tier 1)

**Choice:** Edit source files so links match **post-adopt** locations (tier 1 relative only):

| File | Fix |
|------|-----|
| `docs/workflows/integrations.md` | `openspec-git-integration.md` (sibling) |
| `docs/workflows/ticket-card-info.md` | `openspec-git-integration.md` (sibling) |
| `docs/workflows/branch-workflow.md` | `git-trello.md` → `sdlc/git-trello.md` |
| `overlays/lsi/docs/workflows/which-workflow.md` | `lsi-help.md` → `../../.cursor/commands/lsi-help.md`; `adopt-and-update.md` → `adopt-and-update.md` |
| `overlays/lsi/docs/ai/openspec.md` | `../workflows/openspec-git-integration.md` → `../../.lsi/workflows/openspec-git-integration.md` (valid from `docs/ai/` after adopt) |
| Root `which-workflow.md` (LSI row) | `openspec-git-integration.md` overlay note — use sibling name only in overlay copy; bundle root may keep maintainer path for dogfood |

Overlay `which-workflow.md` **overwrites** core router via `merge_which_workflow_lsi()` — fix the overlay file as primary.

### 3. Extend `LINK_REWRITES` as safety net (transition aid — not primary authoring)

**Choice:** Add catch-all rewrites in `adopt.py` for tier 1 paths that may reappear when maintainers accidentally author bundle layout hrefs. **Do not** treat new rewrites as the default fix — extend the table only for known accidental patterns during transition, not as a substitute for source edits.

```python
(r"\]\(\.\./\.\./overlays/lsi/docs/workflows/", "](",),
(r"\]\(\.\./\.\./overlays/lsi/docs/sdlc/", "](sdlc/",),
(r"\]\(\.\./\.\./agent-stack/commands/", "](../../.cursor/commands/",),
(r"\]\(\.\./\.\./\.\./docs/adopt-and-update\.md\)", "](adopt-and-update.md)"),
```

**Rationale:** Belt-and-suspenders while sources are corrected (decisions 1–2). **Pattern rules + tests enforce the boundary:** adopted output must not contain smuggled tier 2 path substrings; verify fails even if a rewrite would paper over a bad href. Rewrites run on every copied file but must not become the primary authoring strategy.

### 4. Bundle regression: `test_adopt_links.py`

**Choice:** New unittest that:

1. Creates temp dir with minimal adopter skeleton (`PROJECT.md`, patch config from `_template.yaml`)
2. Runs `adopt.py --target <tmp> --config patches/_template.yaml --accept-policy-defaults` (or invokes `copy_core_bundle` + `copy_overlay` helpers if full adopt is heavy)
3. Runs `adoption-verify-links.verify()` on `.lsi/workflows/` and asserts `broken == []`
4. Runs the same `verify(..., extra_dirs=[Path("docs/ai")])` and asserts `broken == []` — catches regressions in `docs/ai/openspec.md` cross-tree links to `../../.lsi/workflows/openspec-git-integration.md` (bundle test only; `verify-adopters.py` default unchanged per task 5.2)
5. Optionally asserts no `overlays/lsi/` or `agent-stack/` substrings in `.lsi/workflows/**/*.md`

**Alternatives considered:**

- *Fixture-only static files* — does not catch transform regressions in `adopt.py`
- *Run verify-adopters on real adopters in CI* — out of bundle repo scope; keep as maintainer post-release step

### 5. Pattern rule in `adoption-verify-links.py` (enforce tier boundaries)

**Choice:** Add pattern violations for `](overlays/lsi/` and `](agent-stack/` inside canonical tree (same severity as doubled `docs/workflows/` prefix). These catch **tier 2 paths written as tier 1 relative links**.

**Rationale:** Clearer failure message than "file not found"; encodes tier 1 vs tier 2 boundary in [adoption-verify-architecture.md](../../docs/adoption-verify-architecture.md). Together with `test_adopt_links.py` substring checks (decision 4), ensures rewrites remain a transition aid — authors must fix sources, not add regex to `LINK_REWRITES`.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Dual `adopt-and-update.md` copies diverge | Adopter copy is short; maintainer doc links to it; test asserts adopter copy links |
| `.cursor/commands/` missing during verify if adopt partial | Regression test runs full adopt install including agent stack |
| Rewrites mask bad source links silently | Pattern rules fail on smuggled tier 2 paths; substring assertion in test; source fixes are primary (§2) |
| CI snippet copy duplicates bundle | Small tier 3 files; versioned with bundle; acceptable |
| Tier 2 GitHub URLs stale after adopter lag on re-sync | Pin to `v{{BUNDLE_VERSION}}` in source; adopter `PROJECT.md` updated on re-sync |
| Authors confuse tier 1 vs tier 2 | `adopter-docs/README.md` + pattern rules + `test_adopt_links.py` |

## Migration Plan

1. Implement bundle fixes on feature branch (`chore/bundle-fix-adopter-link-drift` or similar — **not on `main`**).
2. Bump `VERSION` / `CHANGELOG.md` with adopter re-sync note.
3. Maintainer adopt loop: re-sync each registered adopter; `verify-adopters.py --repo-root <adopter>` must pass.
4. Rollback: revert bundle release; adopters keep previous `.lsi/workflows/` until re-sync.

## Resolved decisions

### `docs/ai/openspec.md` links (task 5.2)

**Choice:** Fix at source — change `../workflows/openspec-git-integration.md` → `../../.lsi/workflows/openspec-git-integration.md` in `overlays/lsi/docs/ai/openspec.md` (both occurrences).

**Do not** add `--extra-dirs docs/ai` to `verify-adopters.py` default — outside the current adopter parity gate. **`test_adopt_links.py`** (task 4.1) calls `verify(..., extra_dirs=[Path("docs/ai")])` after temp adopt to catch cross-tree link regressions in bundle CI.

### CI snippet copy (task 1.3)

**Choice:** Copy **both** `docs/ci/check_version-web.yml` and `docs/ci/check_version-ai-agent.yml` unconditionally into `.lsi/workflows/ci/` on every adopt. Cheap, avoids per-patch conditionals, matches adopter doc linking both snippets.
