## 1. Slash command

- [x] 1.1 Add `overlays/lsi/agent-stack/commands/lsi-help.md` — section templates, SDLC mermaid, bundle-path map, GitHub URL builder; **`status`** / **`next`**: branch → phase → command heuristics (`design.md` §8); **`status`**: conditional `TITLE_PREFIX` note only when card setup is suggested (`design.md` §7)
- [x] 1.2 Rewrite `/lsi:help` as **one-turn** — no AskQuestion, no Exit, no sticky session; no arg → overview + topic list; `<topic>` → render `## Section:` block in chat

## 2. Routing and rules

**Apply scope:** ship **1.1–1.2 + 2.1–2.3** in this change; **do not** implement **2.4** until routing gate **5.7** fails.

- [x] 2.1 Add `/lsi:help` decision-table row to `overlays/lsi/docs/workflows/which-workflow.md` and `overlays/lsi/which-workflow-lsi.md` — insert **after `/opsx:propose`**
- [x] 2.2 Add overlap rule **#7** (`/lsi:help` vs implementation commands) to **LSI overlay** `overlays/lsi/docs/workflows/which-workflow.md` only; list `/lsi:help` in openspec-git-integration quick reference
- [x] 2.3 Extend bundle-root `which-workflow.md` LSI row with “Discovery: `/lsi:help` (overlay)” — **no** full overlap rule at root
- [ ] 2.4 *(optional — gated by 5.7)* Overlay flowchart early branch for workflow help → `/lsi:help` — **If 5.7 pass:** mark **2.4 closed**; **If 5.7 fail:** implement **2.4** before release close

## 3. Parity tooling

- [x] 3.1 Append `lsi-help` to `LSI_COMMANDS` in `snippets/verify-adopters.py`
- [x] 3.2 Append `lsi-help` to `LSI_COMMANDS` in `snippets/audit-agent-docs.py`

## 4. Maintainer dogfood and release

- [x] 4.1 Run `snippets/bootstrap-maintainer-local.sh` so `.cursor/commands/lsi-help.md` exists in bundle repo
- [x] 4.2 Add `[Unreleased]` CHANGELOG entry for `/lsi:help`
- [x] 4.3 Bump `VERSION` to **1.4.1** and sync `PROJECT.md` `BUNDLE_VERSION`

## 5. Verification

- [x] 5.1 Manual: `/lsi:help` → overview + numbered topic list only (no section bodies)
- [x] 5.2 Manual: `/lsi:help sdlc` → mermaid diagram in chat; no topic list re-shown
- [x] 5.3 Manual: `/lsi:help lifecycle` → 13 steps with GitHub links
- [x] 5.4 Manual: all spec links are `github.com/osuarez1/cursor-dev-workflows/blob/v1.4.1/...`
- [x] 5.5 Run `python3 snippets/verify-adopters.py` after bootstrap (bundle repo smoke)
- [x] 5.6 Manual: after `/lsi:help next`, a new message “create a card” is handled normally (not trapped in help)
- [ ] 5.7 **Routing gate (task 2.4):** three fresh Agent chats — plain user text only; agent routes to **`/lsi:help`** via overlay decision table:
  1. `which command should I use?`
  2. `I'm lost on the LSI workflow`
  3. `what should I run next?`
  - **Pass (all 3):** check **2.4 closed**
  - **Fail (any):** implement **2.4** before marking change complete
