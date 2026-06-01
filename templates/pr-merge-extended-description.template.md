# PR merge extended description template

Normative rules: [pull-requests.md](../docs/workflows/pull-requests.md) — **PR merge commit**.  
Use when merging on GitHub with a **merge commit** (not squash).

**Commit message (first field):** leave GitHub’s default:

```text
Merge pull request #<N> from <owner>/<branch>
```

**Extended description (second field):** paste the block below (plain text, not markdown headings).

```text
<One or two sentences: why this merged; align with PR Overview.>

Changes:
- <path or area> — <what changed>
- <path or area> — <what changed>

Commits merged:
- <conventional commit subject from branch>
- <conventional commit subject from branch>

Post-merge: <tag, deploy, notify, or "none" if nothing required>
```

Gather branch commits (oldest first; omit sync merges from `BASE_BRANCH`):

```bash
git log BASE_BRANCH..HEAD --oneline --reverse --no-merges
```

Example: [examples/pr-merge-commit-good-vs-weak.md](../examples/pr-merge-commit-good-vs-weak.md).
