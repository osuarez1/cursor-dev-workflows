---
description: Conduct version → changelog → commit → tag on main, then emit a release summary
---

Conduct the full release train on `main` in one command: infer the version, rewrite the changelog, commit, tag, push — behind **three mandatory confirmations** (version write, release commit, push + tag) — then emit a chat-only release summary.

The changelog rewrite sits between Gate 1 and Gate 2: it is **reviewed as a diff and approved as part of Gate 2**, not a fourth gate. Do not invent extra gates, and do not treat the changelog as unreviewed.

**Canonical source:** [`overlays/lsi/docs/workflows/versioning-and-releases.md`](../../overlays/lsi/docs/workflows/versioning-and-releases.md)

**Composes:** [`/lsi:version`](lsi-version.md) → [`/lsi:changelog`](lsi-changelog.md) → release commit → [`/lsi:release`](lsi-release.md) → [`/lsi:release-summary`](lsi-release-summary.md). This command **conducts** those steps and reuses their scripts — it does not reimplement bump, parser, or tag logic.


**Input:** Optional target version override. Optional audience flag `--mgmt` (default) or `--ops`, passed through to the closing summary.

**Steps**

0. **Preflight — refuse off `main`**

   ```bash
   git branch --show-current
   git status --short
   git fetch --tags
   ```

   - Branch MUST be `main`. On `staging` or a ticket branch, **stop immediately** — do not write `version.txt`, do not touch `CHANGELOG.md`, do not tag.
   - Report a dirty working tree and let the user decide before continuing.

1. **Infer the version** (`/lsi:version` step)

   ```bash
   uv run python scripts/release/infer_version.py --json
   ```

   Show current, proposed, bump type, reason, and the commit signals since the last tag. Use the user's override when they passed one.

   > **Gate 1 — confirm before writing `version.txt`.** Nothing is written until the user approves the version.

   On approval, write `version.txt` only.

2. **Rewrite the changelog** (`/lsi:changelog` step)

   ```bash
   uv run python scripts/release/generate_changelog.py --mode since-tag --finalize ${VERSION} --compare
   ```

   Generator output is a **draft input**. Apply the rewrite rules in [`lsi-changelog.md`](lsi-changelog.md) § 3: strip `type(scope):` prefixes, one detailed bullet per user-visible change, collapse duplicates, fold OpenSpec sync/archive into one Changed line, group under `### Added` / `### Fixed` / `### Changed`.

   Show the `CHANGELOG.md` diff for review — a review step, not a gate. The user approves this content when they approve the commit at Gate 2.

3. **Release commit**

   > **Gate 2 — confirm before committing.** Show the exact files and subject first.

   ```bash
   git add version.txt CHANGELOG.md
   git commit -m "chore(release): v${VERSION}"
   ```

4. **Tag and push** (`/lsi:release` semantics)

   ```bash
   git tag --list "v${VERSION}"      # must be empty — stop if the tag exists
   ```

   > **Gate 3 — confirm before pushing.** State the branch push and the annotated tag together.

   ```bash
   git push origin main
   git tag -a "v${VERSION}" HEAD -m "Release v${VERSION}"
   git push origin "v${VERSION}"
   ```

   Verify `CHANGELOG.md` contains `## [${VERSION}]` and `version.txt` matches before tagging.

5. **Emit the release summary**

   Run [`/lsi:release-summary`](lsi-release-summary.md) for `${VERSION}` with the audience flag the user passed (`--mgmt` when omitted). Chat only — no summary file is written.

**Abandoning mid-train**

Gate 1 and step 2 leave `version.txt` and `CHANGELOG.md` modified but uncommitted. When a later gate is rejected or a step fails, report what is left behind: discard with `git checkout -- version.txt CHANGELOG.md` before retrying — `infer_version.py` reads `version.txt` as **current**, so a stale bump skews the next proposal. When the release commit already exists and only the push was refused, leave it or `git reset --soft HEAD~1` — the user's call, never automatic.

**Output**

```
## Release train — v0.22.0

**Branch:** main
**Version:** 0.21.0 → 0.22.0 (minor)
**Changelog:** ## [0.22.0] written and reviewed
**Commit:** chore(release): v0.22.0 @ <sha>
**Tag:** v0.22.0 pushed to origin

Release summary (--mgmt) follows below.
```

Then the full [`/lsi:release-summary`](lsi-release-summary.md) skeleton — meta table plus sections 1–10.

**Guardrails**

- **`main`-only** — refuse on `staging` and ticket branches **before** any write
- **Three confirmations are mandatory** — version write, release commit, and push/tag each require an explicit user yes; never batch them into one approval
- Stop at the failing step and report what is left in the working tree — never continue past a rejected gate or a failed command
- Invoke `scripts/release/infer_version.py` and `scripts/release/generate_changelog.py` — do not duplicate bump or parser logic
- Never force-push tags; stop when `v${VERSION}` already exists
- Prefer remote tags via git; use host release UI only when the team does
- Push with the explicit branch name (`git push origin main`); repo hooks reject `git push -u origin HEAD`
- Never leave `type(scope):` commit subjects in `CHANGELOG.md`
- The closing summary is **chat only** — no `docs/releases/` file
- Never emit a PR title or body draft — `/lsi:pr` (feature → `staging`) and `/lsi:promote` (promotion → `main`) own the draft; name the command instead.
- MUST emit the Output skeleton; MUST NOT invent alternate report shapes or append follow-up questions.
- No `Next:` footer (D11).
