# Adoption checklist

Bootstrap **cursor-dev-workflows** into a target project repository.

## 1. Copy the bundle

- [ ] Copy this folder as the new repo root **or** subtree (e.g. `vendor/cursor-dev-workflows/` or git submodule).
- [ ] If subtree, keep a single `CANONICAL_DOCS_PATH` in the **application** repo for day-to-day agent reads.

## 2. Set placeholders

Fill the [README.md](README.md) registry for the target project:

- [ ] `REPO_NAME`, `TITLE_PREFIX`
- [ ] `BASE_BRANCH`, `PROTECTED_BRANCHES`
- [ ] `SOURCE_ROOT`, `TEST_ROOT`, `TEST_COMMAND`, `LINT_COMMAND`
- [ ] `TICKET_TOOL`, `TICKET_ID_PATTERN`, `BRANCH_PATTERN`
- [ ] `PR_HOST`, `CANONICAL_DOCS_PATH`
- [ ] Optional: `WORKFLOWS_BUNDLE_PATH` in local or gitignored notes only — never commit absolute clone paths

Optional: create `PROJECT.md` in the app repo with resolved values and link from `AGENTS.md`.

## 3. Install workflow docs in the app repo

- [ ] Copy (or symlink) workflow markdown into `CANONICAL_DOCS_PATH`, e.g.:
  - [ticket-card-info.md](ticket-card-info.md)
  - `code-review.md`, `senior-analysis.md`, `pull-requests.md`, etc.
- [ ] Search/replace placeholders in copied files with real commands and paths.

## 4. Cursor rules

- [ ] Copy [snippets/cursor-rules/](snippets/cursor-rules/) → `.cursor/rules/`
- [ ] Edit each `.mdc` file so pointers match `CANONICAL_DOCS_PATH`
- [ ] Keep `alwaysApply: false` unless you want a rule always on

## 5. Agent entry points

- [ ] Add a “Workflows” section to `AGENTS.md`, `CLAUDE.md`, or `.cursorrules` linking:
  - Branch policy → `branch-workflow.md`
  - Routing → `which-workflow.md`
  - Commits → `commits-logical-order.md` + Conventional Commits doc

## 6. User rules (recommended)

- [ ] Paste [snippets/user-rule-only-commit-when-asked.md](snippets/user-rule-only-commit-when-asked.md) into Cursor **Settings → Rules**

## 7. Gitignore

- [ ] Append [snippets/gitignore-local-artifacts.txt](snippets/gitignore-local-artifacts.txt) to application `.gitignore`

## 8. Optional integrations

- [ ] [integrations.md](integrations.md) — git-trello-tool, PR comment logging, Jira/Linear mapping

## 9. Verify

- [ ] Ask agent to route “code review” → code-review doc ([which-workflow.md](which-workflow.md))
- [ ] Ask agent to draft a ticket card → three fenced blocks ([ticket-card-info.md](ticket-card-info.md))
- [ ] Confirm agent refuses task work on `PROTECTED_BRANCHES` ([branch-workflow.md](branch-workflow.md))
- [ ] Confirm agent outputs commit plan but does not commit until asked

## 10. Team communication

- [ ] Link PR template to [templates/pr-description.template.md](templates/pr-description.template.md)
- [ ] Document `TEST_COMMAND` in CONTRIBUTING or README

## Related

- [README.md](README.md)  
- [integrations.md](integrations.md)  
