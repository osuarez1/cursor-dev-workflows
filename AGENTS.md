# Agent instructions — cursor-dev-workflows

Portable Cursor workflow bundle. **Docs-only repository** — no application code, tests, or build commands.

**Entry points:** [AGENTS.md](AGENTS.md) (canonical). [CLAUDE.md](CLAUDE.md) is a **symlink** to this file for Claude Code.

Resolved placeholders for this repo: [PROJECT.md](PROJECT.md).

**Bundle version:** [VERSION](VERSION) (see [CHANGELOG.md](CHANGELOG.md)). For bundle **release** or **sync maintenance**, read gitignored `AGENTS-LOCAL.md` and `MAINTAINER.md` if present (from [AGENTS-LOCAL.md.example](AGENTS-LOCAL.md.example) and [MAINTAINER.md.example](MAINTAINER.md.example)).

## Bundle maintainers (local kit)

One-time setup for gitignored slash commands and adopt-loop playbooks:

```bash
./snippets/bootstrap-maintainer-local.sh
./snippets/verify-maintainer-local.sh
```

Installs gitignored `MAINTAINER.md`, `AGENTS-LOCAL.md`, `.cursor/rules/local-*.mdc`, and `.cursor/commands/`. Templates: [snippets/maintainer-local/README.md](snippets/maintainer-local/README.md).

**OpenSpec** is tracked under **`openspec/`** — see [docs/ai/openspec.md](docs/ai/openspec.md). **Do not** run `adopt.py --target .` on this repo; edit `docs/workflows/` and `overlays/lsi/` as source.

## Read first

1. **Route the request** — [which-workflow.md](which-workflow.md) (decision table + flowchart)
2. **Read the matching spec** — [docs/workflows/](docs/workflows/) (normative rules)
3. **Check examples** — [examples/](examples/) (good vs weak output)

## Canonical docs (`docs/workflows/`)

All normative workflow specs live here. This repo dogfoods `CANONICAL_DOCS_PATH = docs/workflows/`.

| Need | Document |
|------|----------|
| Draft ticket/card | [ticket-card-info.md](docs/workflows/ticket-card-info.md) |
| Branch / ticket rules | [branch-workflow.md](docs/workflows/branch-workflow.md) |
| PR title / description / merge commit text | [pull-requests.md](docs/workflows/pull-requests.md) |
| Ready for PR or production? | [pr-production-readiness.md](docs/workflows/pr-production-readiness.md) |
| Merge-gate review | [code-review.md](docs/workflows/code-review.md) |
| Design / alternatives | [senior-analysis.md](docs/workflows/senior-analysis.md) |
| Commit plan / messages | [commits-logical-order.md](docs/workflows/commits-logical-order.md) |
| When tests are required | [test-requirements.md](docs/workflows/test-requirements.md) |
| Optional tooling | [integrations.md](docs/workflows/integrations.md) |
| Agent mistakes | [common-mistakes.md](docs/workflows/common-mistakes.md) |

**LSI overlay (bundle authoring):** extension specs under `overlays/lsi/docs/workflows/` when present in the bundle (e.g. `openspec-git-integration.md`, `versioning-and-releases.md`). OpenSpec lifecycle: [docs/ai/openspec.md](docs/ai/openspec.md). Adopters receive overlay specs via `adopt.py`; do not create `.lsi/workflows/` in this repo.

## Commit and PR conventions (always on)

Enforced by [.cursor/rules/commit-pr-conventions.mdc](.cursor/rules/commit-pr-conventions.mdc).

- **Commits:** Conventional Commits — `type(scope): imperative subject`, ≤ ~72 chars, no trailing period; one logical change per commit; show a commit plan before the first commit when multiple concerns exist
- **Only run `git commit` when the user explicitly asks**
- **PR title:** Same format as commit subject
- **PR body sections:** Overview, Changes, Potential risks, Testing, Related
- **PR merge commit (merge-commit strategy):** default `Merge pull request #…` subject; extended description with Summary, `Changes:`, `Commits merged:`, `Post-merge:`

Full specs: [docs/workflows/commits-logical-order.md](docs/workflows/commits-logical-order.md), [docs/workflows/pull-requests.md](docs/workflows/pull-requests.md)

Examples: [examples/commit-messages-good-vs-weak.md](examples/commit-messages-good-vs-weak.md), [examples/pr-description-good-vs-weak.md](examples/pr-description-good-vs-weak.md), [examples/pr-merge-commit-good-vs-weak.md](examples/pr-merge-commit-good-vs-weak.md)

## Support artifacts

| Folder | Purpose |
|--------|---------|
| [examples/](examples/) | Good vs weak illustrations for agent output |
| [templates/](templates/) | Copy-paste output shapes (PR body, review, ticket card, etc.) |
| [snippets/](snippets/) | Adoption exports — Cursor rules, user rules, gitignore fragments |

## Boundaries (this repo)

- **Docs-only:** no application `TEST_COMMAND` or `SOURCE_ROOT`; bundle source is `docs/workflows/`, `overlays/lsi/`, `snippets/`, `templates/`, `examples/`
- **Branch policy:** with maintainer local kit installed, **never implement bundle features on `main`** — use `feat/<slug>` or `chore/bundle-<slug>`; see [branch-workflow.md](docs/workflows/branch-workflow.md) and gitignored `local-branch-workflow.mdc`
- **Adopt vs maintainer paths:** [docs/adopter-boundaries.md](docs/adopter-boundaries.md)
- **Do not commit** unless the user explicitly asks
- **Do not amend, squash, or use `--no-verify`** unless the user explicitly requests
- **Senior analysis ≠ code review** — different verdict words; see [which-workflow.md](which-workflow.md) overlap rules

## Cursor modes

| Mode | Use for |
|------|---------|
| **Plan** | Large or ambiguous work; design before coding; read-only exploration |
| **Agent** | Implementation on a feature branch (bundle: `chore/bundle-*` or ticket-linked `feat/*`) |
| **Ask** | Questions and reviews without edits |

**Branch policy applies in every mode** when the local kit is installed — do not implement on `main`.

## Versioning

| Artifact | Purpose |
|----------|---------|
| [VERSION](VERSION) | Current released bundle version |
| [CHANGELOG.md](CHANGELOG.md) | History and **Adopter action** notes |
| [docs/versioning.md](docs/versioning.md) | Semver policy |

Bundle **release** steps: gitignored [AGENTS-LOCAL.md](AGENTS-LOCAL.md) when present.

## Archived OpenSpec changes

Completed changes under `openspec/changes/archive/` (updated by `/lsi:close` on `main`):

- _(none yet)_

## Adoption into application repos

1. Read [docs/adoption-layout.md](docs/adoption-layout.md) — choose Profile A (default) or B; copy map and link rules.
2. Follow [adoption-checklist.md](adoption-checklist.md).
3. In the app repo, symlink `CLAUDE.md` → `AGENTS.md` or merge a Workflows section per [adoption-layout.md](docs/adoption-layout.md#agent-entry-points).

Human-oriented overview and placeholder registry: [README.md](README.md).
