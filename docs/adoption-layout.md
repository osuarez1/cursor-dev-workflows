# Adoption layout

Normative rules for copying **cursor-dev-workflows** into an application repository without broken links or router drift.

**Use with:** [adoption-checklist.md](../adoption-checklist.md) (step-by-step checklist).

## Why this exists

The bundle uses **root-relative paths**: the router (`which-workflow.md`), support folders (`templates/`, `examples/`), and normative specs (`docs/workflows/`) each link to the others assuming this layout. Copying files into a different tree without rewriting links produces doubled paths (e.g. `docs/workflows/docs/workflows/...`) or broken template links — the most common adopter failures.

## Choose a layout profile

Pick **one** profile per application repo and record it in `PROJECT.md` (e.g. `ADOPTION_PROFILE = A`).

| Profile | Summary | When to use |
|---------|---------|-------------|
| **A — Mirror bundle (default)** | Specs in `CANONICAL_DOCS_PATH`; router, `templates/`, and `examples/` at **app repo root** | Default; links work with minimal changes |
| **B — Flatten under `CANONICAL_DOCS_PATH`** | Router, specs, templates, and examples all under `CANONICAL_DOCS_PATH` | Only when the team refuses root-level workflow files |

**Rules:**

- Do **not** mix profiles (e.g. router inside `docs/workflows/` while `templates/` stay at root with `../docs/workflows/` links).
- Profile **A** is the bundle’s own layout — prefer it unless you have a documented reason for B.
- Profile **B** requires **mandatory link rewrites** after every copy or re-sync (see [Link rewrites](#link-rewrites-profile-b)).

## Copy map

Replace `CANONICAL_DOCS_PATH` with your adopted path (bundle default: `docs/workflows/`).

| Bundle path | Profile A (mirror) | Profile B (flatten) |
|-------------|-------------------|---------------------|
| `docs/workflows/*.md` | → `CANONICAL_DOCS_PATH/` | → `CANONICAL_DOCS_PATH/` |
| `which-workflow.md` | → **app repo root** | → `CANONICAL_DOCS_PATH/` + [rewrite links](#link-rewrites-profile-b) |
| `templates/` | → **app repo root** `templates/` | → under `CANONICAL_DOCS_PATH/` or sibling + rewrite links |
| `examples/` | → **app repo root** `examples/` | → under `CANONICAL_DOCS_PATH/` or sibling + rewrite links |
| `snippets/cursor-rules/*.mdc` | → `.cursor/rules/` | → `.cursor/rules/` |
| `AGENTS.md`, `PROJECT.md` | → app repo root (adapt placeholders) | → app repo root (adapt placeholders) |

**Rules:**

- Only **normative specs** live under `CANONICAL_DOCS_PATH`.
- Do **not** copy `MAINTAINER.md`, `AGENTS-LOCAL.md`, or maintainer-only notes into the app repo’s tracked tree.
- Team-specific overlays (e.g. internal SDLC docs) sit **beside** the bundle paths — do not fork bundle link paths for them.

## Link conventions

### Profile A — no link surgery on bundle files

| File location | Link to sibling in `CANONICAL_DOCS_PATH` |
|---------------|------------------------------------------|
| App repo root (`which-workflow.md`, `AGENTS.md`, `README`) | `docs/workflows/foo.md` |
| `CANONICAL_DOCS_PATH/*.md` | `(foo.md)` (same directory) |
| `templates/`, `examples/` at repo root | `../docs/workflows/foo.md` |
| Spec → router | `../../which-workflow.md` (when specs are one level below root, e.g. `docs/workflows/`) |

<a id="link-rewrites-profile-b"></a>

### Link rewrites (Profile B)

After copying into `CANONICAL_DOCS_PATH`, apply:

| Was (bundle root layout) | Must become (inside `CANONICAL_DOCS_PATH`) |
|--------------------------|---------------------------------------------|
| `(docs/workflows/foo.md)` in router | `(foo.md)` |
| `../docs/workflows/foo.md` in templates/examples | `(foo.md)` if co-located, or adjust per final folder |
| `../../which-workflow.md` in specs | `(which-workflow.md)` if router is co-located |

Run [link verification](#link-verification) before merging any adoption or re-sync PR.

## Merging existing docs

When the application repo already has agent docs, Cursor rules, or workflow markdown, **merge** bundle content instead of overwriting blindly. Checklist steps: [adoption-checklist.md §3](../adoption-checklist.md#merging-existing-docs-existing-app-repo).

### Principles

| Principle | Rule |
|-----------|------|
| Single source of truth | One canonical spec per workflow under `CANONICAL_DOCS_PATH` — no competing PR or review docs |
| Merge entry points | Keep app-specific `AGENTS.md` / `CLAUDE.md` content; add bundle Workflows section and `PROJECT.md` placeholders |
| Overlays beside bundle | Team SDLC docs live next to bundle paths; link from [integrations.md](workflows/integrations.md), do not fork bundle links |
| Replace vs merge | **Replace** old workflow specs with bundle equivalents; **merge** agent entry points and `.cursor/rules/` |

### By doc type

| Existing file | Action |
|---------------|--------|
| Old PR / review / commit guidelines | **Replace** with bundle spec in `CANONICAL_DOCS_PATH`; move app-only commands into `PROJECT.md` |
| `AGENTS.md`, `CLAUDE.md`, `.cursorrules` | **Merge** — keep domain rules; add router and spec links (see [Agent entry points](#agent-entry-points)) |
| `PROJECT.md` or equivalent | **Create or extend** with bundle placeholders, `ADOPTION_PROFILE`, `BUNDLE_VERSION` |
| `.cursor/rules/*.mdc` | **Merge** — copy bundle snippets; `commit-pr-conventions.mdc` → `alwaysApply: true`; drop duplicated commit/PR rules |
| GitHub/GitLab PR template | **Keep** for humans; point agents at [templates/pr-description.template.md](../templates/pr-description.template.md) |
| `templates/` or `examples/` at repo root | **Rename** app files on collision; copy bundle folders per [copy map](#copy-map) (Profile A) |
| Internal SDLC (git-trello, CONVENTION, etc.) | **Keep beside bundle** — document in [integrations.md](workflows/integrations.md) or gitignored maintainer notes |

### Adoption flow

1. Inventory existing agent docs before copying bundle files.
2. Classify: bundle equivalent, app-only, or overlap.
3. Install bundle per [copy map](#copy-map) and chosen profile.
4. Merge entry points and rules; retire or stub superseded workflow docs.
5. Run [link verification](#link-verification) and [agent smoke tests](#agent-smoke-tests).

## Agent entry points

Pointers in `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, and `.cursor/rules/*.mdc` must match the chosen profile.

**Profile A (default):**

- Router: `which-workflow.md` (repo root)
- Specs: `docs/workflows/pull-requests.md` (or your `CANONICAL_DOCS_PATH`)

**Profile B:**

- Router: `docs/workflows/which-workflow.md` (or your `CANONICAL_DOCS_PATH/which-workflow.md`)
- Specs: same directory, e.g. `docs/workflows/pull-requests.md`

## Link verification

Run from the **application repo root** after copy, path edits, or re-sync. Fix all failures before merge.

### Verification script (recommended)

Design reference: [adoption-verify-architecture.md](adoption-verify-architecture.md).

Copy [snippets/adoption-verify-links.py](../snippets/adoption-verify-links.py) into your app repo (or run from the bundle path). It checks link resolution, doubled-prefix patterns, and — for Profile **A** — root entry points (`which-workflow.md`, `AGENTS.md`, `README.md`) plus root `templates/` and `examples/`.

```bash
python3 snippets/adoption-verify-links.py \
  --profile A \
  --canonical docs/workflows \
  --repo-root .
```

Profile **B**:

```bash
python3 snippets/adoption-verify-links.py \
  --profile B \
  --canonical docs/workflows \
  --repo-root .
```

Profile **B** with `templates/` or `examples/` beside `CANONICAL_DOCS_PATH`:

```bash
python3 snippets/adoption-verify-links.py \
  --profile B \
  --canonical docs/workflows \
  --extra-dirs docs/templates \
  --extra-dirs docs/examples \
  --repo-root .
```

Profile **A** only: use `--no-support-dirs` to skip root `templates/` and `examples/`. Profile **B** never scans root support dirs; the router is verified inside `CANONICAL_DOCS_PATH`.

Exit code `0` means pass; non-zero prints broken links and pattern violations.

### Optional pattern checks (`rg`)

The script covers doubled-prefix detection. For a quick manual spot-check:

Profile **A** — expect **no matches** inside `CANONICAL_DOCS_PATH`:

```bash
rg '\]\(docs/workflows/' docs/workflows/
```

(`docs/workflows/` is the default path; substitute your `CANONICAL_DOCS_PATH`.)

Profile **A** — `../docs/workflows/` in root-level `templates/` and `examples/` is **expected and valid**.

Profile **B** — expect **no matches** for doubled prefixes anywhere under `CANONICAL_DOCS_PATH`:

```bash
rg '\]\(docs/workflows/' docs/workflows/
rg '\]\(\.\./docs/workflows/' docs/workflows/
```

Adjust paths if your `CANONICAL_DOCS_PATH` differs.

## Agent smoke tests

After link verification, confirm agent behavior (see [adoption-checklist.md §9](../adoption-checklist.md)):

- Route “code review” → `code-review` spec
- Draft ticket card → three fenced blocks
- Draft PR description → body includes **Overview**, **Changes**, **Potential risks**, **Testing**, **Related**
- Refuse task work on `PROTECTED_BRANCHES`
- Output commit plan but do not commit until asked

## Re-sync from upstream

On every bundle upgrade:

1. Read **Adopter action** in [CHANGELOG.md](../CHANGELOG.md) for the target version.
2. Update `BUNDLE_VERSION` in `PROJECT.md`.
3. Re-copy changed paths per the [copy map](#copy-map).
4. Re-apply link rewrites only if Profile **B** (Profile **A** usually needs none).
5. Re-run [link verification](#link-verification) and [agent smoke tests](#agent-smoke-tests).

Maintainer sync mapping: [MAINTAINER.md.example](../MAINTAINER.md.example).

## Related

- [adoption-checklist.md](../adoption-checklist.md) — full bootstrap checklist (including [merging existing docs](../adoption-checklist.md#merging-existing-docs-existing-app-repo))
- [adoption-verify-architecture.md](adoption-verify-architecture.md) — verification gate design reference
- [README.md](../README.md) — placeholder registry and bundle layout
- [docs/versioning.md](versioning.md) — semver and adopter sync policy
