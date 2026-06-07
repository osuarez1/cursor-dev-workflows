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
- **Bundle adopt-link regression test** (`test_adopt_links.py`) — highest-value deliverable for long-term maintenance; required gate before `VERSION` bump (local + CI when present)
- Minimal adopter churn — re-sync only, no hand-edits under `.lsi/workflows/`
- Seed **`overlays/lsi/adopter-docs/`** for docs where maintainer layout diverges from adopter layout (this change: `adopt-and-update.md` only; expand long-term — see below)

**Non-Goals:**

- Rewriting `/lsi:help` GitHub blob URLs (already adopter-safe)
- Link-checking `.cursor/commands/*.md` or `.mdc` rules (out of verify scope today)
- External URL reachability
- Retrofitting Profile A/B layouts
- GitHub URLs for **tier 1** cross-spec links (installed workflow docs stay relative in-repo)
- Copying maintainer-only bundle docs into adopters just to satisfy link verify
- Expanding `LINK_REWRITES` as the primary link-fix strategy (regex whack-a-mole)
- Completing the full `adopter-docs/` tree in this change — seed `adopt-and-update.md` only; long-term expansion is follow-on work

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
| Bundle source grep for `](overlays/lsi/` and (when §2 clean) `](agent-stack/` in `docs/workflows/`, `overlays/lsi/docs/workflows/` | Manual gate this change; CI when pipeline lands (decision 6, task 4.6) |
| `https://` links | Skipped by verify (tier 2 OK) |
| `BUNDLE_VERSION` in tier 2 GitHub URLs | `substitute_tokens` at adopt time; `update_project_md` writes same value to adopter `PROJECT.md`; assert in `test_adopt_links.py` |
| `--extra-dirs docs/ai` in verify-adopters | **Out of scope** for adopter parity default; **`test_adopt_links.py`** uses `extra_dirs=["docs/ai"]` to regression-test `openspec.md` cross-tree links after adopt |

## Decisions

### 1. Adopter-shaped source for `adopt-and-update.md` (tiers 1–3)

**Choice:** Add `overlays/lsi/adopter-docs/adopt-and-update.md` written for `.lsi/workflows/` layout following the **three-tier link policy**; `copy_core_bundle()` copies this file instead of `docs/adopt-and-update.md`. Keep `docs/adopt-and-update.md` as the maintainer-facing superset (may link to bundle paths freely). Add `overlays/lsi/adopter-docs/README.md` documenting the three tiers for future authors.

**Rationale:** `adopt-and-update.md` has the most tier 2 violations today. A dedicated adopter copy avoids regex whack-a-mole and is the **first** step toward a full adopter-shaped source tree (see **Long-term direction** below).

**Long-term (not this change):** Expand `overlays/lsi/adopter-docs/` for **any** doc where the bundle maintainer layout diverges from post-adopt adopter layout. When a file copied into adopters cannot be authored correctly in the maintainer tree without tier 2 hrefs or fragile rewrites, add an adopter-shaped copy under `adopter-docs/` (mirroring install path) and point `adopt.py` at it. Prefer in-place tier 1 fixes in `docs/workflows/` and `overlays/lsi/docs/workflows/` when maintainer and adopter layouts already align (decision 2). `adopter-docs/README.md` documents the expansion criterion for future maintainers.

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
| Root `which-workflow.md` (LSI row) | **Optional** bundle dogfood — may keep maintainer paths (e.g. `overlays/lsi/docs/workflows/…`); not adopter canon |

**Router canonicality (`which-workflow.md`):** Adopters read **`.lsi/workflows/which-workflow.md`** after adopt. **`merge_which_workflow_lsi()`** overwrites the core-copied router with **`overlays/lsi/docs/workflows/which-workflow.md`** (after `rewrite_links`) — that overlay file is the **authoritative edit source**. Sync **`overlays/lsi/which-workflow-lsi.md`** with overlay router rows/links for maintainer reference; it is **not** installed to adopters. Bundle-root **`which-workflow.md`** is maintainer dogfood only (optional LSI row review in task 2.5). Document this table in `adopter-docs/README.md` or adoption-verify architecture to prevent future confusion.

**PR checklist (task 2.5):** Implementation PR **Testing** section must include: `[ ] which-workflow-lsi.md synced with overlay router (task 2.4)` — sync is easy to defer when fixing overlay links alone.

### 3. Extend `LINK_REWRITES` as safety net (transition aid — not primary authoring)

**Choice:** Add catch-all rewrites in `adopt.py` for tier 1 paths that may reappear when maintainers accidentally author bundle layout hrefs. **Do not** treat new rewrites as the default fix — extend the table only for known accidental patterns during transition, not as a substitute for source edits.

```python
(r"\]\(\.\./\.\./overlays/lsi/docs/workflows/", "](",),
(r"\]\(\.\./\.\./overlays/lsi/docs/sdlc/", "](sdlc/",),
(r"\]\(\.\./\.\./agent-stack/commands/", "](../../.cursor/commands/",),
(r"\]\(\.\./\.\./\.\./docs/adopt-and-update\.md\)", "](adopt-and-update.md)"),
```

**Rationale:** Belt-and-suspenders while sources are corrected (decisions 1–2). **Pattern rules + tests enforce the boundary:** adopted output must not contain smuggled tier 2 path substrings; verify fails even if a rewrite would paper over a bad href. Rewrites run on every copied file but must not become the primary authoring strategy.

### 4. Bundle regression: `test_adopt_links.py` (highest-value deliverable)

**Choice:** New unittest that exercises **full adopt → verify** end-to-end. This is the **highest-value deliverable** for long-term maintenance — it catches link drift in bundle sources and transforms before adopter re-sync or release.

**Release gate:** `python3 snippets/test_adopt_links.py` and `python3 snippets/test_adoption_verify_links.py` **MUST pass** before any `VERSION` / `CHANGELOG.md` bump on the bundle repo. Document in [adoption-verify-architecture.md](../../docs/adoption-verify-architecture.md), [README.md](../../README.md), and maintainer pre-release checklist.

**CI (when bundle pipeline lands — task 4.6):** Add a pipeline step that runs **both** modules on every PR (block merge on failure):

```bash
python3 snippets/test_adoption_verify_links.py
python3 snippets/test_adopt_links.py
```

No `VERSION` bump or release tag until this job is green locally and in CI. Source grep (decision 6) and `test_adopt_tokens.py` may join the same job when wired.

1. Creates temp dir with minimal adopter skeleton (`PROJECT.md`, patch config from `_template.yaml`)
2. Runs `adopt.py --target <tmp> --config patches/_template.yaml --accept-policy-defaults` (or invokes `copy_core_bundle` + `copy_overlay` helpers if full adopt is heavy)
3. Runs `adoption-verify-links.verify()` on `.lsi/workflows/` and asserts `broken == []`
4. Runs the same `verify(..., extra_dirs=[Path("docs/ai")])` and asserts `broken == []` — catches regressions in `docs/ai/openspec.md` cross-tree links to `../../.lsi/workflows/openspec-git-integration.md` (bundle test only; `verify-adopters.py` default unchanged per task 5.2)
5. Asserts no `overlays/lsi/` or `agent-stack/` substrings in `.lsi/workflows/**/*.md`
6. Asserts **`BUNDLE_VERSION` token parity** — after adopt, adopter `PROJECT.md` includes `BUNDLE_VERSION` matching bundle `VERSION`; adopted docs with tier 2 GitHub URLs contain `v{VERSION}` and no literal `{{BUNDLE_VERSION}}` placeholder (existing `substitute_tokens` + `update_project_md` path; one assertion — no new adopt logic)

**Alternatives considered:**

- *Fixture-only static files* — does not catch transform regressions in `adopt.py`
- *Run verify-adopters on real adopters in CI* — out of bundle repo scope; keep as maintainer post-release step
- *Manual smoke only before release* — insufficient; automated gate prevents drift from shipping in tagged releases

### 5. Pattern rule in `adoption-verify-links.py` (enforce tier boundaries)

**Choice:** Add pattern violations for `](overlays/lsi/` and `](agent-stack/` inside canonical tree (same severity as doubled `docs/workflows/` prefix). These catch **tier 2 paths written as tier 1 relative links**.

**Rationale:** Clearer failure message than "file not found"; encodes tier 1 vs tier 2 boundary in [adoption-verify-architecture.md](../../docs/adoption-verify-architecture.md). Together with `test_adopt_links.py` substring checks (decision 4), ensures rewrites remain a transition aid — authors must fix sources, not add regex to `LINK_REWRITES`.

### 6. Bundle-side source grep (manual gate now — CI when pipeline lands)

**Choice:** Add a lightweight script (e.g. `snippets/check-workflow-link-sources.sh` or Python equivalent) that fails when any `*.md` under **`docs/workflows/`** or **`overlays/lsi/docs/workflows/`** contains forbidden markdown-link substrings.

**Wiring (this change vs later):**

| Mechanism | This change | When pipeline lands (task 4.6) |
|-----------|-------------|--------------------------------|
| **Script** | Ship under `snippets/` | Same script |
| **Pre-commit / git hooks** | **No** — bundle has no shared pre-commit config; maintainer local hooks are optional/gitignored | Optional maintainer install; not a repo deliverable |
| **Manual gate** | **Yes** — document in README, adoption-verify architecture, pre-release checklist: run before PR / `VERSION` bump | Still valid locally |
| **CI** | **No** — docs-only repo, no pipeline today | Add to same job as both test modules |

Do not block this change on hook infrastructure — script + documented manual run is sufficient until CI exists.

**Phased patterns:**

| Phase | Pattern | When |
|-------|---------|------|
| **1** | `](overlays/lsi/` | Ship with this change (after §2 source fixes) |
| **2** | `](agent-stack/` | **Extend grep once overlay workflow sources are clean** (after task 2.4 — e.g. `which-workflow.md` `lsi-help` → `../../.cursor/commands/`) |

Both phases scan the same directories; phase 2 enables the second pattern in the same script — not a separate tool.

**Scope:** Workflow spec sources that copy into `.lsi/workflows/` only. **Exclude** maintainer-only trees (`docs/adopt-and-update.md`, `openspec/`, root `which-workflow.md`, `patches/`, `README.md`) where bundle-layout navigation is valid. Do **not** grep `overlays/lsi/agent-stack/` — commands install to `.cursor/commands/`, not workflow docs tree.

**Rationale:** Cheapest fail-fast gate — catches tier 2 maintainer paths at commit/PR time, before running temp-adopt regression. Phase 1 targets the highest-signal drift; phase 2 closes the `agent-stack/commands/` smuggling path once §2 removes existing violations (avoid grep failing on known-in-flight fixes).

**Alternatives considered:**

- *Post-adopt verify only* — slower feedback; drift may land on branch before full regression runs
- *Broad repo-wide grep* — false positives in OpenSpec changes, maintainer docs, and CHANGELOG cross-references
- *Enable both patterns day one* — would fail until §2.4 completes; phased rollout keeps CI green during apply

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Dual `adopt-and-update.md` copies diverge | Checklist (1.5) — **watch new `##` sections** in maintainer doc without adopter copy updates; `test_adopt_links.py` catches broken links not missing sections; heading lint (7.2) when second dual doc enters `adopter-docs/` |
| `.cursor/commands/` missing during verify if adopt partial | Regression test runs full adopt install including agent stack |
| Rewrites mask bad source links silently | Pattern rules fail on smuggled tier 2 paths; substring assertion in test; source fixes are primary (§2) |
| CI snippet copy duplicates bundle | Small tier 3 files; versioned with bundle; acceptable |
| Tier 2 GitHub URLs stale after adopter lag on re-sync | Pin to `v{{BUNDLE_VERSION}}` in source; `substitute_tokens` at adopt; `update_project_md` upserts `BUNDLE_VERSION` in adopter `PROJECT.md`; `test_adopt_links.py` asserts parity |
| Authors confuse tier 1 vs tier 2 | `adopter-docs/README.md` + pattern rules + source grep + `test_adopt_links.py` |

## Long-term direction

**Expand `overlays/lsi/adopter-docs/`** for any doc where maintainer bundle layout diverges from adopter install layout.

| Situation | Approach |
|-----------|----------|
| Same tree after adopt; links wrong (e.g. `../../overlays/lsi/…`) | Fix hrefs at source in `docs/workflows/` or `overlays/lsi/docs/workflows/` (decision 2) |
| Maintainer doc mixes adopter-facing content with bundle-only paths (`patches/`, `MAINTAINER.md`, `docs/adopt-new-repo.md`) | Adopter-shaped copy under `adopter-docs/`; maintainer superset stays in bundle layout |
| Small artifact adopters need but bundle does not install by default | Tier 3 copy in `adopt.py`, then tier 1 relative link (CI snippets) |

**This change** seeds the pattern with `adopt-and-update.md` only. Future docs enter `adopter-docs/` when link verify or authoring review shows maintainer layout cannot produce clean adopt output without rewrites. Do not grow `LINK_REWRITES` instead.

**Dual-doc heading lint (task 7.2):** Defer until a **second** dual doc joins `adopter-docs/` (task 7.1). One dual doc does not justify lint tooling — maintainer checklist + link regression is enough.

## Migration Plan

1. Implement bundle fixes on feature branch (`chore/bundle-fix-adopter-link-drift` or similar — **not on `main`**).
2. **Run adopt-link regression gate** — `python3 snippets/test_adopt_links.py` and `python3 snippets/test_adoption_verify_links.py` must pass; source grep (decision 6) should pass on workflow doc changes.
3. Bump `VERSION` / `CHANGELOG.md` and tag release (only after step 2). **Release note must clearly state:** registered LSI adopters need **`/lsi:update`** after pulling this bundle release.
4. **Maintainer adopt loop (task 6.1)** — re-sync each registered adopter; `verify-adopters.py --repo-root <adopter>` must pass on every repo. **Adopter parity is the real acceptance test** — do not treat bundle temp-adopt tests alone as ship-ready.
5. **Announce only after step 4** — team/adopter notification that the release is live and `/lsi:update` is required waits until adopt loop passes on all registered adopters.
6. Rollback: revert bundle release; adopters keep previous `.lsi/workflows/` until re-sync.

## Resolved decisions

### `docs/ai/openspec.md` links (task 5.2)

**Choice:** Fix at source — change `../workflows/openspec-git-integration.md` → `../../.lsi/workflows/openspec-git-integration.md` in `overlays/lsi/docs/ai/openspec.md` (both occurrences).

**Do not** add `--extra-dirs docs/ai` to `verify-adopters.py` default — outside the current adopter parity gate. **`test_adopt_links.py`** (task 4.1) calls `verify(..., extra_dirs=[Path("docs/ai")])` after temp adopt to catch cross-tree link regressions in bundle CI.

### CI snippet copy (task 1.3)

**Choice:** Copy **both** `docs/ci/check_version-web.yml` and `docs/ci/check_version-ai-agent.yml` unconditionally into `.lsi/workflows/ci/` on every adopt. Cheap, avoids per-patch conditionals, matches adopter doc linking both snippets.

### Release gate (tasks 4.5, 4.6, 5.3)

**Choice:** `test_adopt_links.py` + `test_adoption_verify_links.py` are **required** before any bundle `VERSION` bump — local maintainer gate always; **CI step for both modules when bundle pipeline lands** (task 4.6). Do not tag or bump `VERSION` on failing adopt-link regression.

**CI step (task 4.6):** When the bundle repo gets a pipeline (`bitbucket-pipelines.yml`, GitHub Actions, etc.), add one job/step:

```bash
python3 snippets/test_adoption_verify_links.py
python3 snippets/test_adopt_links.py
```

Run on PRs to protected branches; block merge on non-zero exit. Include source grep (task 3.4) in the same job. Documents-only repo today — implement at pipeline introduction, not deferred to adopters.

**CHANGELOG requirement:** Every release that changes adopt output or link policy must include a prominent **Adopters** section (or equivalent callout) stating registered LSI adopters need **`/lsi:update`** after pulling the bundle release — not buried in a bullet; adopters must see the action without reading maintainer notes.

### Adopter parity before announce (task 6.1)

**Choice:** After the first (and every) bundle release that changes adopt output, run the **maintainer adopt loop** on all registered adopters and confirm `verify-adopters.py` passes **before announcing** the release. Temp-dir regression (`test_adopt_links.py`) gates the VERSION bump; **adopter parity on real repos is the real acceptance test** for ship confidence.

### Dual-copy drift (tasks 1.5, 7.2)

**Choice:** **Both, phased.**

1. **Now (this change):** Maintainer checklist in `docs/adopt-and-update.md` — banner at top: when editing adopter-facing content (**including new sections**), update `overlays/lsi/adopter-docs/adopt-and-update.md`; canonical process in `adopter-docs/README.md`. **Acceptable gap:** heading lint (7.2) deferred with one dual doc — **watch** maintainers adding `##` sections to `docs/adopt-and-update.md` without updating adopter copy (link tests won't catch missing sections).

2. **When a second dual doc enters `adopter-docs/` (task 7.2):** Add bundle lint comparing **adopter-relevant** section headings between each maintainer superset and its `adopter-docs/` copy — **not** naive full `##` parity, because structures intentionally diverge (maintainer keeps `patches/`, `MAINTAINER.md`, `adopt-new-repo.md` sections; adopter copy uses tier 2 GitHub/prose). Lint should warn when maintainer adds or renames shared-topic headings (e.g. Bundle update, Verify after adopt, CI) absent from adopter copy. Wire to CI alongside adopt-link regression (task 4.6). **Trigger:** second doc added under `adopter-docs/` via task 7.1 — not before; one dual doc (`adopt-and-update.md`) relies on checklist (1.5) + link tests only.

**Rationale:** Checklist catches human process immediately; link regression catches broken hrefs but not missing sections; heading lint closes the structural gap once the dual-doc pattern is proven and scope is clear enough to avoid false positives.

### Tier 2 `BUNDLE_VERSION` substitution (task 4.2)

**Choice:** Tier 2 GitHub URLs use `v{{BUNDLE_VERSION}}` in adopter-docs source; **existing adopt token path already covers substitution** — `adopt()` reads bundle `VERSION`, builds `tokens["BUNDLE_VERSION"]`, runs `substitute_tokens` on all copied markdown, and `update_project_md()` upserts the same value into adopter `PROJECT.md`. No new token machinery required.

**Test:** `test_adopt_links.py` adds **one assertion** after temp adopt: (1) `PROJECT.md` table contains `BUNDLE_VERSION` equal to bundle `VERSION`; (2) adopted `.lsi/workflows/adopt-and-update.md` (or any file with tier 2 URLs) has no unreplaced `{{BUNDLE_VERSION}}` and contains the pinned version string. Unit coverage for `substitute_tokens` remains in `test_adopt_tokens.py`.

### Source grep wiring (task 3.4)

**Choice:** Ship grep **script only** this change; document as **manual pre-PR / pre-`VERSION` gate**. Do **not** add repo pre-commit hooks — no shared `.pre-commit-config.yaml`, maintainer git hooks are optional. **When bundle pipeline lands (task 4.6):** run grep in CI alongside both test modules. Pre-commit remains optional per-maintainer install, not an apply deliverable.
