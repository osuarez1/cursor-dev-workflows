---
name: /lsi-update
id: lsi-update
category: Workflow
description: Re-sync workflow bundle — adopt for adopters, bootstrap for bundle maintainer
---

Re-sync the **cursor-dev-workflows** bundle after a release or overlay command edit.

**Canonical source:** [adopt-and-update.md](../../docs/adopt-and-update.md) · Bundle maintainer: gitignored [MAINTAINER.md](../../MAINTAINER.md)

**Helper script:** `python3 snippets/update-workflows.py` (auto-detects repo type)

**Input:** Optional `--dry-run`, `--local-only` (maintainer bootstrap only), `--adopters-only` (skip bootstrap), `--bundle <path>` (adopter repos). Invoking counts as consent to run adopt/bootstrap (not `git commit`).

**Steps**

1. **Detect repo type**

   ```bash
   pwd
   test -f snippets/adopt.py && test -d overlays/lsi && echo bundle-maintainer
   test -d .lsi/workflows && echo adopter
   ```

   | Detection | Repo | Action |
   |-----------|------|--------|
   | `snippets/adopt.py` + `overlays/lsi/` + `PROJECT.md` `REPO_NAME=cursor-dev-workflows` | **Bundle maintainer** | Bootstrap + optional adopter loop |
   | `.lsi/workflows/which-workflow.md` | **LSI adopter** | `adopt.py` from bundle → this repo |
   | Neither | **Unknown** | Stop — not an LSI layout |

2. **Bundle maintainer — local Cursor install**

   ```bash
   ./snippets/bootstrap-maintainer-local.sh
   ```

   Syncs `overlays/lsi/agent-stack/commands/` → `.cursor/commands/` and maintainer rules → `.cursor/rules/`. **Re-run after every overlay command edit.**

3. **Bundle maintainer — registered adopters (default unless `--local-only`)**

   Read gitignored [MAINTAINER.md](../../MAINTAINER.md) for `maintainer-adopters.local.yaml` and the adopt loop. If that file is missing, only bootstrap runs.

   ```bash
   python3 snippets/update-workflows.py
   # adopters-only (skip bootstrap):
   python3 snippets/update-workflows.py --adopters-only
   ```

   Skip missing adopter directories with a warning. After adopt, remind maintainer to commit + open PR in each adopter repo with updated `BUNDLE_VERSION` in `PROJECT.md`.

4. **LSI adopter — self re-sync**

   Resolve bundle path (first match):

   - `--bundle /path/to/cursor-dev-workflows`
   - `$WORKFLOWS_BUNDLE_PATH`
   - Ask user once if unset

   ```bash
   python3 "$WORKFLOWS_BUNDLE_PATH/snippets/update-workflows.py" --bundle "$WORKFLOWS_BUNDLE_PATH"
   ```

   Matches `REPO_NAME` in [PROJECT.md](../../PROJECT.md) to `patches/<repo>.yaml`, runs adopt, then verify.

5. **Parity check (runs automatically after adopt)**

   After adopt, `update-workflows.py` runs `check_agent_stack_parity` against the adopter's `.cursor/commands/` and `.cursor/rules/`:

   - **Missing expected files** → warn (re-run adopt to install)
   - **Surplus files not in expected set** → error; lists each path and asks adopter which to remove
   - **Legacy alias pairs both present** (e.g., `code_review.mdc` + `code-review.mdc`) → error; asks adopter to confirm removal

   **Adopter decides**: only confirmed paths are deleted. Decline = surplus stays; add to `preserve_agent_stack` in patch YAML to allowlist intentional extras without being asked again.

6. **Dry-run (optional)**

   ```bash
   python3 snippets/update-workflows.py --dry-run
   ```

   Shows adopt/bootstrap commands without writing files.

7. **Report**

   - Bundle version adopted (from bundle `VERSION`)
   - Files changed summary (`git status --short` in target repo)
   - Verify result (PASS/FAIL)
   - **Do not auto-commit** — user runs `/lsi:commit` when ready

**Output (maintainer)**

```
## Workflow update — bundle maintainer

**Bootstrap:** 30 commands → .cursor/commands/
**Adopters synced:** <from maintainer-adopters.local.yaml; skipped if missing>
**Parity:** <clean | N surplus items listed — adopter confirmed removal>
**Bundle version:** 1.4.x

Review adopter repo diffs and commit when asked.
```

**Output (adopter)**

```
## Workflow update — adopter

**Repo:** <REPO_NAME>
**Bundle:** <path-to-cursor-dev-workflows> @ 1.3.0
**Verify:** PASS

Next: review diff; `/lsi:commit` when ready.
```

**Guardrails**

- **Never** run `adopt.py --target .` on the bundle maintainer repo — use bootstrap only for local `.cursor/`.
- **Never** auto-commit adopted files unless user explicitly asks.
- On adopt audit errors, stop and point to `--audit-only` + `audit-resolutions.yaml`.
- Adopter repos: refuse if bundle path cannot be resolved.
- Protected branches: updating workflows is allowed; do not mix with feature implementation on `main`/`staging` unless user intent is sync-only.
