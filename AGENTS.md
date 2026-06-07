# Agent instructions — cursor-dev-workflows

Portable Cursor workflow bundle. **Docs-only repository** — no application code, tests, or build commands.

Resolved placeholders for this repo: [PROJECT.md](PROJECT.md).

**Bundle version:** [VERSION](VERSION) (see [CHANGELOG.md](CHANGELOG.md)). For bundle **release** or **sync maintenance**, read gitignored `AGENTS-LOCAL.md` and `MAINTAINER.md` if present (from [AGENTS-LOCAL.md.example](AGENTS-LOCAL.md.example) and [MAINTAINER.md.example](MAINTAINER.md.example)).

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

## Commit and PR conventions (always on)

Enforced by [snippets/cursor-rules/commit-pr-conventions.mdc](snippets/cursor-rules/commit-pr-conventions.mdc) (bundle maintainer: install locally per gitignored [MAINTAINER.md](MAINTAINER.md) when present).

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

- **Docs-only:** no `TEST_COMMAND`, `SOURCE_ROOT`, or protected-branch enforcement applies to edits in this tree
- **Do not commit** unless the user explicitly asks
- **Do not amend, squash, or use `--no-verify`** unless the user explicitly requests
- **Senior analysis ≠ code review** — different verdict words; see [which-workflow.md](which-workflow.md) overlap rules

## Cursor modes

| Mode | Use for |
|------|---------|
| **Plan** | Large or ambiguous work; design before coding; read-only exploration |
| **Agent** | Implementation and doc edits |
| **Ask** | Questions and reviews without edits |

## Adoption into application repos

**LSI adopters:** use **`snippets/adopt.py`** — [docs/adopt-and-update.md](docs/adopt-and-update.md), [adoption-checklist.md](adoption-checklist.md), layout [docs/adoption-layout.md](docs/adoption-layout.md) (`.lsi/workflows/` only).

Human-oriented overview and placeholder registry: [README.md](README.md).
