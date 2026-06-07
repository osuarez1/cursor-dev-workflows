## 1. Slash command

- [x] 1.1 Add `overlays/lsi/agent-stack/commands/lsi-help.md` — section templates, SDLC mermaid, bundle-path map, GitHub URL builder; **`status`** / **`next`**: branch → phase → command heuristics (`design.md` §8); **`status`**: conditional `TITLE_PREFIX` note only when card setup is suggested (`design.md` §7)
- [x] 1.2 Rewrite `/lsi:help` as **one-turn** — no AskQuestion, no Exit, no sticky session; no arg → overview + topic list; `<topic>` → render `## Section:` block in chat

## 2. Routing and rules

**Apply scope:** ship **1.1–1.2 + 2.1–2.3**; task **2.4** flowchart branch deferred — **5.7** closed on static decision-table pass (see **5.7** residual risk).

- [x] 2.1 Add `/lsi:help` decision-table row to `overlays/lsi/docs/workflows/which-workflow.md` and `overlays/lsi/which-workflow-lsi.md` — insert **after `/opsx:propose`**
- [x] 2.2 Add overlap rule **#7** (`/lsi:help` vs implementation commands) to **LSI overlay** `overlays/lsi/docs/workflows/which-workflow.md` only; list `/lsi:help` in openspec-git-integration quick reference
- [x] 2.3 Extend bundle-root `which-workflow.md` LSI row with “Discovery: `/lsi:help` (overlay)” — **no** full overlap rule at root
- [x] 2.4 *(optional — gated by 5.7)* Overlay flowchart early branch for workflow help → `/lsi:help` — **Closed (accepted trade-off):** decision-table row is canonical; flowchart branch intentionally omitted per static **5.7** pass

## 3. Parity tooling

- [x] 3.1 Append `lsi-help` to `LSI_COMMANDS` in `snippets/verify-adopters.py`
- [x] 3.2 Append `lsi-help` to `LSI_COMMANDS` in `snippets/audit-agent-docs.py`

## 4. Maintainer dogfood and release

- [x] 4.1 Run `snippets/bootstrap-maintainer-local.sh` so `.cursor/commands/lsi-help.md` exists in bundle repo
- [x] 4.2 Add `[Unreleased]` CHANGELOG entry for `/lsi:help`
- [x] 4.3 Bump `VERSION` to **1.4.1** and sync `PROJECT.md` `BUNDLE_VERSION`

## 5. Verification

**Agent-dependent rendering:** delta spec requires agents to read `## Section:` blocks from the command source and emit them in chat; **no programmatic enforcement**. **Chat dogfood (apply/review):** matched spec for `/lsi:help` (overview), `/lsi:help sdlc`, `/lsi:help lifecycle`, `/lsi:help next`, and invalid topic (error + topic list).

- [x] 5.1 Manual: `/lsi:help` → overview + numbered topic list only (no section bodies) — chat dogfood pass
- [x] 5.2 Manual: `/lsi:help sdlc` → mermaid diagram in chat; no topic list re-shown — chat dogfood pass
- [x] 5.3 Manual: `/lsi:help lifecycle` → 13 steps with GitHub links — chat dogfood pass
- [x] 5.4 Manual: all spec links are `github.com/osuarez1/cursor-dev-workflows/blob/v1.4.1/...`
- [x] 5.5 Run `python3 snippets/verify-adopters.py --repo-root <adopter>` after release/adopt re-sync — **adopter-oriented** parity check; running against **this bundle maintainer repo** (`--repo-root .`) **fails expected** (no `.lsi/workflows/`); not a regression from this change
- [x] 5.6 Manual: after `/lsi:help next`, a new message “create a card” is handled normally (not trapped in help)
- [x] 5.7 **Routing gate (task 2.4) — static pass (not live Agent dogfood):** verified overlay decision-table phrase matching in `overlays/lsi/docs/workflows/which-workflow.md` (row after `/opsx:propose`) plus route-first via `AGENTS.md` / `which-workflow.md`; **did not** run three fresh Agent chats with plain user text.
  1. `which command should I use?` → matches “which command” in decision table → `/lsi:help`
  2. `I'm lost on the LSI workflow` → matches “lost”, “workflow help” → `/lsi:help`
  3. `what should I run next?` → matches “what should I run next (discovery)” → `/lsi:help` (discovery, not `/lsi:help next` auto-run)
  - **Pass (static):** table row + overlap **#7** present; **2.4 closed** without flowchart branch (accepted trade-off — see proposal **PR risk** one-liner)
- [x] 5.8 **Chat dogfood — `/lsi:help next` + invalid topic:** `/lsi:help next` rendered phase/command suggestion; unrecognized topic → one-line error + topic list — matched delta spec (agent read `## Section:` blocks; not programmatically enforceable)
