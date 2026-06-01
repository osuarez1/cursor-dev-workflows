# User rule: only commit when asked

Copy the block below into **Cursor → Settings → Rules** (user rules) for your profile or team.

---

## Committing changes with git

Only create commits when I explicitly ask you to commit. If unclear, ask first.

When I ask you to commit:

1. Run `git status`, `git diff`, and `git log` to understand changes and message style.
2. If multiple logical changes exist, show a **commit plan** first (ordered list with `type(scope): subject`, body bullets, and files per commit). See commits-logical-order workflow.
3. Use **Conventional Commits**: imperative subject, optional scope, blank line, body for why. One logical change per commit. Do not squash unrelated work into one commit.
4. Stage only relevant files; commit with a HEREDOC message; run `git status` after.
5. Do not amend, squash, or use `--no-verify` unless I explicitly request.
6. Do not push unless I explicitly ask.

Never hand-write ticket footers that git hooks add automatically from the branch name (if your repo uses them).

---

Adjust paths to point at your adopted `docs/workflows/commits-logical-order.md` if needed.
