# cursor-dev-workflows

Portable **Cursor agent workflows** for any language or framework: ticket cards, branch policy, PR/production readiness, code review, senior analysis, and logical commits.

**Repository:** Clone or copy this tree anywhere on your machine; treat **this directory** as the bundle’s **git repository root**. Teams often keep it as a sibling of the application repo, but the path is up to you. After adoption, agents and Cursor rules should read workflows from `CANONICAL_DOCS_PATH` in the **application** repo (see [adoption-checklist.md](adoption-checklist.md)), not from your local clone path.

## Quick start

1. Copy this entire folder into a new git repository (or use it as the repo root).
2. Replace placeholders in the table below for your project.
3. Follow [adoption-checklist.md](adoption-checklist.md).
4. Copy [snippets/cursor-rules/](snippets/cursor-rules/) into your target repo’s `.cursor/rules/` and adjust paths to your canonical docs.

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
| `WORKFLOWS_BUNDLE_PATH` | `~/src/cursor-dev-workflows` | Optional: where you cloned this bundle locally; for maintainer notes only — do not commit machine-specific paths |

## Workflow routing

Not sure which doc to use? See [which-workflow.md](which-workflow.md).

| Need | Document |
|------|----------|
| Draft ticket/card | [ticket-card-info.md](ticket-card-info.md) |
| Branch / ticket rules | [branch-workflow.md](branch-workflow.md) |
| Ready for PR or production? | [pr-production-readiness.md](pr-production-readiness.md) |
| Merge-gate review | [code-review.md](code-review.md) |
| Design / alternatives | [senior-analysis.md](senior-analysis.md) |
| Commit plan / messages | [commits-logical-order.md](commits-logical-order.md) |
| When tests are required | [test-requirements.md](test-requirements.md) |
| Optional tooling | [integrations.md](integrations.md) |
| Agent mistakes | [common-mistakes.md](common-mistakes.md) |

## Cursor modes

| Mode | Use for |
|------|---------|
| **Plan** | Large or ambiguous work; design before coding; read-only exploration |
| **Agent** | Implementation on a ticket-linked feature branch |
| **Ask** | Questions and reviews without edits |

**Branch policy applies in every mode:** do not implement task work on `PROTECTED_BRANCHES`. See [branch-workflow.md](branch-workflow.md).

## Adoption recipe (target repo)

1. Copy workflow markdown into `CANONICAL_DOCS_PATH` (or keep a submodule/subtree of this repo).
2. Install thin rules from [snippets/cursor-rules/](snippets/cursor-rules/) → `.cursor/rules/`.
3. Add pointers in `AGENTS.md`, `CLAUDE.md`, or `.cursorrules`.
4. Paste [snippets/user-rule-only-commit-when-asked.md](snippets/user-rule-only-commit-when-asked.md) into Cursor **Settings → Rules** (optional but recommended).
5. Append [snippets/gitignore-local-artifacts.txt](snippets/gitignore-local-artifacts.txt) to `.gitignore`.

Full steps: [adoption-checklist.md](adoption-checklist.md).

## Maintainer notes

If you sync this bundle from an internal source repo, keep the **file mapping** (bundle path → canonical path in the app repo) in maintainer-only notes — gitignored `MAINTAINER.md`, a private wiki, or similar. Do not commit org names, internal repo slugs, or machine-specific clone paths.

When merging updates from a source repo, diff each workflow file against its adopted copy under `CANONICAL_DOCS_PATH` and record the sync date in your commit message or local notes.

## Repository layout

```text
README.md
LICENSE
which-workflow.md
branch-workflow.md
test-requirements.md
common-mistakes.md
adoption-checklist.md
integrations.md
ticket-card-info.md
pr-production-readiness.md
code-review.md
senior-analysis.md
commits-logical-order.md
templates/
snippets/
examples/
```

## License

[MIT](LICENSE)
