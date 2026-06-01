# Adoption checklist

Bootstrap **cursor-dev-workflows** into a target project repository.

**Layout rules (read first):** [docs/adoption-layout.md](docs/adoption-layout.md) — choose Profile A or B, copy map, link verification.

## 1. Copy the bundle

- [ ] Copy this folder as the new repo root **or** subtree (e.g. `vendor/cursor-dev-workflows/` or git submodule).
- [ ] If subtree, keep a single `CANONICAL_DOCS_PATH` in the **application** repo for day-to-day agent reads.
- [ ] Choose **Profile A (mirror, default)** or **Profile B (flatten)** per [docs/adoption-layout.md](docs/adoption-layout.md) and record in `PROJECT.md` (e.g. `ADOPTION_PROFILE = A`).

## 2. Set placeholders

Fill the [README.md](README.md) registry for the target project:

- [ ] `REPO_NAME`, `TITLE_PREFIX`
- [ ] `BASE_BRANCH`, `PROTECTED_BRANCHES`
- [ ] `SOURCE_ROOT`, `TEST_ROOT`, `TEST_COMMAND`, `LINT_COMMAND`
- [ ] `TICKET_TOOL`, `TICKET_ID_PATTERN`, `BRANCH_PATTERN`
- [ ] `PR_HOST`, `CANONICAL_DOCS_PATH`
- [ ] `BUNDLE_VERSION` — git tag (e.g. `v1.0.0`) or full commit SHA from the bundle you copied ([VERSION](VERSION), [CHANGELOG.md](CHANGELOG.md))
- [ ] Optional: `WORKFLOWS_BUNDLE_PATH` in local or gitignored notes only — never commit absolute clone paths

Optional: create `PROJECT.md` in the app repo with resolved values and link from `AGENTS.md`.

## 3. Install workflow docs and support files

Follow the [copy map](docs/adoption-layout.md#copy-map) for your profile.

**Profile A (default — mirror bundle layout):**

- [ ] Copy normative specs into `CANONICAL_DOCS_PATH`, e.g.:
  - [ticket-card-info.md](docs/workflows/ticket-card-info.md)
  - `code-review.md`, `senior-analysis.md`, `pull-requests.md`, etc.
- [ ] Copy [which-workflow.md](which-workflow.md) to **app repo root** (do not place inside `CANONICAL_DOCS_PATH`).
- [ ] Copy [templates/](templates/) and [examples/](examples/) to **app repo root**.
- [ ] Search/replace placeholders in copied files with real commands and paths.

**Profile B (flatten — link rewrites required):**

- [ ] Copy specs **and** [which-workflow.md](which-workflow.md) into `CANONICAL_DOCS_PATH`.
- [ ] Copy [templates/](templates/) and [examples/](examples/) under `CANONICAL_DOCS_PATH` or a documented sibling path.
- [ ] Apply [link rewrites](docs/adoption-layout.md#link-rewrites-profile-b) per `docs/adoption-layout.md`.
- [ ] Search/replace placeholders in copied files with real commands and paths.

### Merging existing docs (existing app repo)

Use when the target repo already has `AGENTS.md`, `.cursor/rules/`, CONTRIBUTING, PR templates, or workflow markdown. Full rules: [docs/adoption-layout.md § Merging existing docs](docs/adoption-layout.md#merging-existing-docs).

- [ ] **Inventory** — List agent entry points (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`), `.cursor/rules/`, docs under `docs/`, PR templates, and CONTRIBUTING.
- [ ] **Classify each file** — Bundle equivalent (replace with bundle spec), app-only (keep; link from `AGENTS.md` or [integrations.md](docs/workflows/integrations.md)), or overlap (merge then retire duplicate).
- [ ] **Normative specs** — One canonical file per workflow under `CANONICAL_DOCS_PATH`. Replace or supersede old PR/review/commit docs; port app-specific commands into placeholders in `PROJECT.md`, not forked bundle paths.
- [ ] **Router** — Copy bundle [which-workflow.md](which-workflow.md) per profile (§3 above). If `AGENTS.md` already routes agents, add a **Workflows** section (§5) rather than duplicating the full decision table.
- [ ] **AGENTS.md / PROJECT.md** — **Merge**, do not blindly overwrite: keep domain and architecture sections; add Workflows pointers and link to `PROJECT.md` for resolved placeholders and `BUNDLE_VERSION`.
- [ ] **`.cursor/rules/`** — Merge bundle snippets with existing rules; set `alwaysApply: true` on `commit-pr-conventions.mdc`; remove duplicate commit/PR rules superseded by the bundle.
- [ ] **Templates / examples** — Copy bundle [templates/](templates/) and [examples/](examples/) to repo root (Profile A). On name collision, rename app-specific files (e.g. `templates/pr-description.app.md`) or keep app templates under `docs/`; link human PR templates to bundle shape in §10.
- [ ] **Team overlays** — Internal SDLC docs (git-trello, CONVENTION, etc.) stay **beside** `CANONICAL_DOCS_PATH`; link from [integrations.md](docs/workflows/integrations.md) or local maintainer notes — do not weave into bundle link paths.
- [ ] **Retire or redirect** — After merge, add a one-line stub in superseded docs pointing to the bundle spec, or remove after team sign-off.
- [ ] **Do not commit** — `MAINTAINER.md`, `AGENTS-LOCAL.md`, or absolute `WORKFLOWS_BUNDLE_PATH` values into the app repo.

## 4. Cursor rules

- [ ] Copy [snippets/cursor-rules/](snippets/cursor-rules/) → `.cursor/rules/` (including `commit-pr-conventions.mdc`, `pull-requests.mdc`, `code-review.mdc`, `ticket-card-info.mdc`, `senior-analysis.mdc`)
- [ ] Edit each `.mdc` file so pointers match `CANONICAL_DOCS_PATH` and router location (Profile A: root `which-workflow.md`; Profile B: `CANONICAL_DOCS_PATH/which-workflow.md`)
- [ ] Set `alwaysApply: true` on `commit-pr-conventions.mdc` for baseline commit/PR enforcement
- [ ] Keep task-specific rules (`code-review.mdc`, `senior-analysis.mdc`, etc.) at `alwaysApply: false`

## 5. Agent entry points

- [ ] Copy or adapt [AGENTS.md](AGENTS.md) and [PROJECT.md](PROJECT.md) into the app repo (or link from existing agent docs). If the app repo already has these files, follow [§3 Merging existing docs](#merging-existing-docs-existing-app-repo).
- [ ] Add a “Workflows” section to `AGENTS.md`, `CLAUDE.md`, or `.cursorrules` linking (adjust paths for Profile B):
  - Branch policy → `docs/workflows/branch-workflow.md`
  - Routing → `which-workflow.md` (Profile A: repo root; Profile B: `docs/workflows/which-workflow.md`)
  - Commits → `docs/workflows/commits-logical-order.md`
  - PR conventions → `docs/workflows/pull-requests.md`

## 6. User rules (recommended)

- [ ] Paste [snippets/user-rule-only-commit-when-asked.md](snippets/user-rule-only-commit-when-asked.md) into Cursor **Settings → Rules**

## 7. Gitignore

- [ ] Append [snippets/gitignore-local-artifacts.txt](snippets/gitignore-local-artifacts.txt) to application `.gitignore`

## 8. Optional integrations

- [ ] [integrations.md](docs/workflows/integrations.md) — git-trello-tool, PR comment logging, Jira/Linear mapping

## 9. Verify

### Link verification (required before merge)

From the **application repo root**, run checks in [docs/adoption-layout.md § Link verification](docs/adoption-layout.md#link-verification):

- [ ] Run [snippets/adoption-verify-links.py](snippets/adoption-verify-links.py) (Profile A or B matching `ADOPTION_PROFILE`; `--canonical` = your `CANONICAL_DOCS_PATH`) — exit code 0
- [ ] Optional: `rg` pattern spot-check if the script is unavailable

### Agent smoke tests

- [ ] Ask agent to route “code review” → code-review doc ([which-workflow.md](which-workflow.md) or your Profile B router path)
- [ ] Ask agent to draft a ticket card → three fenced blocks ([ticket-card-info.md](docs/workflows/ticket-card-info.md))
- [ ] Ask agent to draft a PR description → body includes **Potential risks** ([pull-requests.md](docs/workflows/pull-requests.md))
- [ ] Confirm agent refuses task work on `PROTECTED_BRANCHES` ([branch-workflow.md](docs/workflows/branch-workflow.md))
- [ ] Confirm agent outputs commit plan but does not commit until asked

## 10. Team communication

- [ ] Link PR template to [templates/pr-description.template.md](templates/pr-description.template.md)
- [ ] Document `TEST_COMMAND` in CONTRIBUTING or README
- [ ] On re-sync from upstream bundle, update `BUNDLE_VERSION`, read **Adopter action** in [CHANGELOG.md](CHANGELOG.md), and re-run §9 link verification

## Related

- [docs/adoption-layout.md](docs/adoption-layout.md) — layout profiles, copy map, link rules
- [README.md](README.md)
- [integrations.md](docs/workflows/integrations.md)
