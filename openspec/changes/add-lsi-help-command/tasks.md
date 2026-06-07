## 1. Slash command

- [x] 1.1 Add `overlays/lsi/agent-stack/commands/lsi-help.md` — **help session guardrails block at top** (per `design.md` command outline); overview template, AskQuestion menu ids, per-section templates, SDLC mermaid, bundle-path map, session loop guardrails, GitHub URL builder; **`status`** / **`next`**: branch → phase → command heuristics (`design.md` §10); **`status`**: conditional `TITLE_PREFIX` note only when card setup is suggested (`design.md` §9)

## 2. Routing and rules

**Apply scope:** ship **1.1 + 2.1–2.3** in this change; **do not** implement **2.4** until routing gate **5.7** fails.

- [x] 2.1 Add `/lsi:help` decision-table row to `overlays/lsi/docs/workflows/which-workflow.md` and `overlays/lsi/which-workflow-lsi.md` — insert **after `/opsx:propose`**; row text per `design.md` §11 (“which command / help / lost …” → `/lsi:help`)
- [x] 2.2 Add overlap rule **#7** (`/lsi:help` vs implementation commands) to **LSI overlay** `overlays/lsi/docs/workflows/which-workflow.md` only — one paragraph per `design.md` §8; link to `lsi-help.md`; do not paste full guardrail list. **Same commit:** list `/lsi:help` in `overlays/lsi/agent-stack/openspec-git-integration.mdc` and `overlays/lsi/docs/workflows/openspec-git-integration.md` quick reference (was task 2.5)
- [x] 2.3 Extend bundle-root `which-workflow.md` LSI row with “Discovery: `/lsi:help` (overlay)” — **no** full overlap rule at root
- [ ] 2.4 *(optional — gated by 5.7)* Overlay flowchart early branch for workflow help / which command → `/lsi:help` — **out of initial apply**; run **5.7** after 2.1–2.3 + bootstrap. **If 5.7 pass:** mark **2.4 closed** (decision table sufficient; no flowchart branch). **If 5.7 fail:** implement 2.4 before release close

## 3. Parity tooling

- [x] 3.1 Append `lsi-help` to `LSI_COMMANDS` in `snippets/verify-adopters.py`
- [x] 3.2 Append `lsi-help` to `LSI_COMMANDS` in `snippets/audit-agent-docs.py`

## 4. Maintainer dogfood and release

- [x] 4.1 Run `snippets/bootstrap-maintainer-local.sh` (or `install-maintainer-local.py`) so `.cursor/commands/lsi-help.md` exists in bundle repo
- [x] 4.2 Add `[Unreleased]` CHANGELOG entry for `/lsi:help`
- [x] 4.3 Bump `VERSION` to **1.4.1** and sync `PROJECT.md` `BUNDLE_VERSION`

## 5. Verification

- [ ] 5.1 Manual: `/lsi:help` first turn = overview + AskQuestion only
- [ ] 5.2 Manual: each section pick ends with AskQuestion; Exit ends session
- [ ] 5.3 Manual: `sdlc` section shows mermaid only
- [ ] 5.4 Manual: all spec links are `github.com/osuarez1/cursor-dev-workflows/blob/v.../...`
- [x] 5.5 Run `python3 snippets/verify-adopters.py` after bootstrap (bundle repo smoke)
- [ ] 5.6 Manual: mid-session user says “create a card” → agent stays read-only until Exit (may suggest `/lsi:card` or relevant help section; does not run Trello API, `git ts`/`git tb`, or other implementation commands)
- [ ] 5.7 **Routing gate (task 2.4):** after **2.1–2.3** + **4.1** bootstrap, three **fresh Agent** chats — plain user text only (no `/lsi:help` invocation). Agent must route to **`/lsi:help`** via overlay `which-workflow.md` decision table (not `/opsx:explore`, not implementation commands, not a generic doc dump without naming `/lsi:help`):
  1. `which command should I use?`
  2. `I'm lost on the LSI workflow`
  3. `what should I run next?`
  - **Pass (all 3):** check **2.4 closed** — flowchart branch not needed; record pass in apply notes or PR Testing
  - **Fail (any):** implement **2.4** before marking change complete
