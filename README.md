# cursor-dev-workflows

Portable **Cursor agent workflows** for any language or framework: ticket cards, branch policy, PR/production readiness, code review, senior analysis, and logical commits.

**Repository:** Clone or copy this tree anywhere on your machine; treat **this directory** as the bundle’s **git repository root**. Teams often keep it as a sibling of the application repo, but the path is up to you. After adoption, agents and Cursor rules should read workflows from `CANONICAL_DOCS_PATH` in the **application** repo (see [adoption-checklist.md](adoption-checklist.md)), not from your local clone path.

## Quick start

**Agents:** start at [AGENTS.md](AGENTS.md).

1. Copy this entire folder into a new git repository (or use it as the repo root).
2. Replace placeholders in the table below for your project.
3. Read [docs/adoption-layout.md](docs/adoption-layout.md) — choose Profile A (default) or B.
4. Follow [adoption-checklist.md](adoption-checklist.md).
5. Copy [snippets/cursor-rules/](snippets/cursor-rules/) into your target repo’s `.cursor/rules/` and adjust paths to your canonical docs.

## Placeholder registry

Set these once per target repository. Search/replace tokens in docs after copying, or maintain a small `PROJECT.md` in the target repo with the resolved values.

| Token | Example | Meaning |
|-------|---------|---------|
| `REPO_NAME` | `MyApp` | Short product or repo name |
| `TITLE_PREFIX` | `MyApp \| ` | Ticket/card title prefix (name, pipe, space) |
| `BASE_BRANCH` | `main` | Default integration branch for diffs and PRs |
| `PROTECTED_BRANCHES` | `main`, `master`, `staging` | Branches where agents must not implement task work |
| `TEST_COMMAND` | `npm test` / `pytest` / `make test` | Command to run affected tests |
| `LINT_COMMAND` | `npm run lint` | Optional lint/typecheck command |
| `SOURCE_ROOT` | `src/` | Application source root(s), comma-separated if several |
| `TEST_ROOT` | `tests/` | Test tree root |
| `TICKET_TOOL` | `Trello` / `Jira` / `Linear` | Issue tracker |
| `TICKET_ID_PATTERN` | `24-char hex` / `PROJ-123` | Required id in branch names, if enforced |
| `BRANCH_PATTERN` | `feature/<id>-slug` | Branch naming convention |
| `PR_HOST` | `GitHub` / `GitLab` / `Bitbucket` | Where pull requests live |
| `CANONICAL_DOCS_PATH` | `docs/workflows/` | Where adopted copies of these specs live in the target repo (use in rules and agent docs) |
| `ADOPTION_PROFILE` | `A` | Layout profile: **A** mirror bundle (default) or **B** flatten — see [docs/adoption-layout.md](docs/adoption-layout.md) |
| `BUNDLE_VERSION` | `v1.0.0` or commit SHA | Version of this bundle recorded in adopted `PROJECT.md` when copying or re-syncing |
| `WORKFLOWS_BUNDLE_PATH` | `~/src/cursor-dev-workflows` | Optional: where you cloned this bundle locally; for maintainer notes only — do not commit machine-specific paths |

## Workflow routing

Not sure which doc to use? See [which-workflow.md](which-workflow.md).

| Need | Document |
|------|----------|
| Draft ticket/card | [ticket-card-info.md](docs/workflows/ticket-card-info.md) |
| Branch / ticket rules | [branch-workflow.md](docs/workflows/branch-workflow.md) |
| PR title / description conventions | [pull-requests.md](docs/workflows/pull-requests.md) |
| Ready for PR or production? | [pr-production-readiness.md](docs/workflows/pr-production-readiness.md) |
| Merge-gate review | [code-review.md](docs/workflows/code-review.md) |
| Design / alternatives | [senior-analysis.md](docs/workflows/senior-analysis.md) |
| Commit plan / messages | [commits-logical-order.md](docs/workflows/commits-logical-order.md) |
| When tests are required | [test-requirements.md](docs/workflows/test-requirements.md) |
| Optional tooling | [integrations.md](docs/workflows/integrations.md) |
| Agent mistakes | [common-mistakes.md](docs/workflows/common-mistakes.md) |

## Cursor modes

| Mode | Use for |
|------|---------|
| **Plan** | Large or ambiguous work; design before coding; read-only exploration |
| **Agent** | Implementation on a ticket-linked feature branch |
| **Ask** | Questions and reviews without edits |

**Branch policy applies in every mode:** do not implement task work on `PROTECTED_BRANCHES`. See [branch-workflow.md](docs/workflows/branch-workflow.md).

## Adoption recipe (target repo)

**Default (Profile A — mirror bundle):**

For submodule or subtree installs ([adoption-checklist.md §1](adoption-checklist.md)), copy specs into `CANONICAL_DOCS_PATH` in the **application** repo; still use Profile A for router, `templates/`, and `examples/` at the app repo root.

1. Copy normative specs from [`docs/workflows/`](docs/workflows/) into `CANONICAL_DOCS_PATH`.
2. Copy [`which-workflow.md`](which-workflow.md), [`templates/`](templates/), and [`examples/`](examples/) to the **app repo root** (do not nest under `CANONICAL_DOCS_PATH`).
3. Install thin rules from [snippets/cursor-rules/](snippets/cursor-rules/) → `.cursor/rules/`.
4. Add pointers in `AGENTS.md`, `CLAUDE.md`, or `.cursorrules`.
5. Run link verification and agent smoke tests ([adoption-checklist.md §9](adoption-checklist.md)).
6. Paste [snippets/user-rule-only-commit-when-asked.md](snippets/user-rule-only-commit-when-asked.md) into Cursor **Settings → Rules** (optional but recommended).
7. Append [snippets/gitignore-local-artifacts.txt](snippets/gitignore-local-artifacts.txt) to `.gitignore`.

Layout profiles, copy map, and link rules: [docs/adoption-layout.md](docs/adoption-layout.md). Full checklist: [adoption-checklist.md](adoption-checklist.md).

## Versioning

| Artifact | Purpose |
|----------|---------|
| [VERSION](VERSION) | Current released bundle version |
| [CHANGELOG.md](CHANGELOG.md) | History and **Adopter action** notes for breaking releases |
| [docs/versioning.md](docs/versioning.md) | Semver policy for this bundle |

Record `BUNDLE_VERSION` in your adopted `PROJECT.md` when you copy or re-sync.

## Maintainer notes

Copy [MAINTAINER.md.example](MAINTAINER.md.example) → gitignored `MAINTAINER.md` and fill in local paths, sync mapping, and release checklists. For bundle release tasks, copy [AGENTS-LOCAL.md.example](AGENTS-LOCAL.md.example) → gitignored `AGENTS-LOCAL.md`.

Do not commit org names, internal repo slugs, or machine-specific clone paths.

## Repository layout

```text
AGENTS.md                    # Agent entry point
CLAUDE.md                    # Points to AGENTS.md
PROJECT.md                   # Resolved placeholders (this repo)
README.md
VERSION                      # Released bundle version
CHANGELOG.md
which-workflow.md            # Workflow router
adoption-checklist.md
MAINTAINER.md.example        # Copy → MAINTAINER.md (gitignored)
AGENTS-LOCAL.md.example      # Copy → AGENTS-LOCAL.md (gitignored)
docs/
  adoption-layout.md         # Layout profiles, copy map, link verification
  versioning.md              # Semver policy
  workflows/                 # CANONICAL_DOCS_PATH — normative specs
templates/
examples/
snippets/
  adoption-verify-links.py   # Post-adoption link verification (Profile A/B)
  cursor-rules/
  user-rule-only-commit-when-asked.md
  gitignore-local-artifacts.txt
.cursor/
  rules/
    commit-pr-conventions.mdc   # alwaysApply: true (this repo)
LICENSE
```

## License

[MIT](LICENSE)
