# cursor-dev-workflows

Portable **Cursor agent workflows** for any language or framework: ticket cards, branch policy, PR/production readiness, PR merge commit text, code review, senior analysis, and logical commits.

**Repository:** Clone or copy this tree anywhere on your machine; treat **this directory** as the bundle’s **git repository root**. Teams often keep it as a sibling of the application repo, but the path is up to you. After adoption, agents and Cursor rules should read workflows from `CANONICAL_DOCS_PATH` in the **application** repo (see [adoption-checklist.md](adoption-checklist.md)), not from your local clone path.

## Quick start

**Agents:** start at [AGENTS.md](AGENTS.md).

**LSI adopters** ([registered repos](patches/README.md)):

1. Maintain `patches/<repo>.yaml` in this bundle.
2. Run [docs/adopt-and-update.md](docs/adopt-and-update.md) — `snippets/adopt.py` installs `.lsi/workflows/` and agent stack.
3. Do **not** hand-edit `.lsi/workflows/` in application repos.

**New repo:** [docs/adopt-new-repo.md](docs/adopt-new-repo.md).

**Bundle maintainers:** [MAINTAINER.md.example](MAINTAINER.md.example) · verify all: `./snippets/verify-all-adopters.sh`

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
| `CANONICAL_DOCS_PATH` | `.lsi/workflows/` | Adopt-managed specs in LSI repos ([docs/adoption-layout.md](docs/adoption-layout.md)) |
| `ADOPTION_LAYOUT` | `lsi` | Single layout for all LSI adopters |
| `VERSION_FILE` | `version.txt` or `VERSION` | App semver file for `check_version.py` |
| `BUNDLE_VERSION` | `v1.0.0` or commit SHA | Version of this bundle recorded in adopted `PROJECT.md` when copying or re-syncing |
| `WORKFLOWS_BUNDLE_PATH` | `~/src/cursor-dev-workflows` | Optional: where you cloned this bundle locally; for maintainer notes only — do not commit machine-specific paths |

## Workflow routing

Not sure which doc to use? See [which-workflow.md](which-workflow.md).

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

## Cursor modes

| Mode | Use for |
|------|---------|
| **Plan** | Large or ambiguous work; design before coding; read-only exploration |
| **Agent** | Implementation on a ticket-linked feature branch |
| **Ask** | Questions and reviews without edits |

**Branch policy applies in every mode:** do not implement task work on `PROTECTED_BRANCHES`. See [branch-workflow.md](docs/workflows/branch-workflow.md).

## Adoption (LSI layout)

Registered LSI repos adopt via **`snippets/adopt.py`** — do not hand-copy specs into application repos. Full guide: [docs/adopt-and-update.md](docs/adopt-and-update.md).

1. Add or maintain `patches/<repo>.yaml` in this bundle ([patches/README.md](patches/README.md)).
2. Audit, adopt, and verify per [adoption-checklist.md](adoption-checklist.md) (`--audit-only` → adopt → `verify-adopters.py`).
3. Set `CANONICAL_DOCS_PATH=.lsi/workflows/` in the app repo's `PROJECT.md`.

Layout spec: [docs/adoption-layout.md](docs/adoption-layout.md). New repo: [docs/adopt-new-repo.md](docs/adopt-new-repo.md).

## Versioning

| Artifact | Purpose |
|----------|---------|
| [VERSION](VERSION) | Current released bundle version |
| [CHANGELOG.md](CHANGELOG.md) | History and **Adopter action** notes for breaking releases |
| [docs/versioning.md](docs/versioning.md) | Semver policy for this bundle |

Record `BUNDLE_VERSION` in your adopted `PROJECT.md` when you copy or re-sync.

**Bundle maintainers — pre-`VERSION` gate:** `python3 snippets/test_adoption_verify_links.py`, `python3 snippets/test_adopt_links.py`, `python3 snippets/test_check_workflow_link_sources.py`, and `python3 snippets/check-workflow-link-sources.py` must pass before bumping [VERSION](VERSION) or tagging a release.

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
  adoption-layout.md         # LSI layout (.lsi/workflows/), link verification
  adoption-verify-architecture.md  # Verification gate design reference
  versioning.md              # Semver policy
  workflows/                 # Bundle source specs (copied by adopt.py)
overlays/lsi/                # LSI overlay (docs, agent stack, release scripts)
patches/                     # Per-repo adopt YAML + file overlays
templates/
examples/
snippets/
  adopt.py                   # LSI adopt entry point
  adoption-verify-links.py   # Post-adoption link verification (.lsi/workflows/)
  verify-adopters.py         # Parity checklist + audit gate
  test_adoption_verify_links.py  # Fixture regression (python3 snippets/test_adoption_verify_links.py)
  test_adopt_links.py            # Temp adopt + verify gate (python3 snippets/test_adopt_links.py)
  test_check_workflow_link_sources.py  # Source-grep regression (python3 snippets/test_check_workflow_link_sources.py)
  check-workflow-link-sources.py # Manual pre-PR grep for tier 2 paths in workflow sources
  test_adopt_tokens.py           # Adopt token + YAML tests (python3 snippets/test_adopt_tokens.py)
  fixtures/adoption-verify/  # Test fixture trees
  cursor-rules/              # Canonical Cursor rules (adopters + local install)
  user-rule-only-commit-when-asked.md
  gitignore-local-artifacts.txt
.cursor/                     # gitignored — local Cursor install (see MAINTAINER.md)
LICENSE
```

## License

[MIT](LICENSE)
