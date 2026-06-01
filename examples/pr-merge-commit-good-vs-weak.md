# PR merge commit: good vs weak

See [pull-requests.md](../docs/workflows/pull-requests.md) — **PR merge commit**.

Applies when merging on `PR_HOST` with a **merge commit** (GitHub **Commit message** + **Extended description**).

## Weak extended description

```text
docs(adoption): add layout profiles and link verification for v1.1.0
```

**Why weak:** Only repeats the PR title; no summary, file-level changes, branch commits, or post-merge steps.

---

## Weak extended description (PR body pasted verbatim)

Full PR markdown with `## Overview`, checklists, and Testing steps copied into the merge dialog.

**Why weak:** Merge history should be scannable; use the structured merge format, not the PR review template.

---

## Strong

**Commit message** (GitHub default — do not replace unless the team explicitly uses another merge strategy):

```text
Merge pull request #1 from osuarez1/fix/workflows-router-pr-sections
```

**Extended description**

```text
Align which-workflow.md PR row with pull-requests.md, AGENTS.md, and
commit-pr-conventions.mdc so agents list all required PR body sections,
including Potential risks.

Changes:
- which-workflow.md — PR row output column updated
- CHANGELOG.md, VERSION, PROJECT.md — bundle PATCH release 1.0.1

Commits merged:
- fix(workflows): add Potential risks to router PR row
- chore(release): mark bundle v1.0.1

Post-merge: tag v1.0.1 on main and push the tag when ready.
```

**Why strong:** Summary explains why; Changes name paths and outcomes; Commits merged lists branch history; Post-merge gives a concrete follow-up.

---

## Squash merge

If the repo uses **squash and merge**, use the PR **title** as the squash commit subject and a shortened PR Overview in the body — not this extended-description format. See [pull-requests.md](../docs/workflows/pull-requests.md).
