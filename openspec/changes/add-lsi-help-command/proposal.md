## Why

LSI adopters have many slash commands and workflow specs under `.lsi/workflows/`, but no single entry point for developers to discover the staging-first SDLC, pick the right command, or deep-link to bundle documentation. Dumping the full lifecycle and command tables in one chat response is hard to scan. **`/lsi:help`** — overview plus `/lsi:help <topic>` for one section per invocation — gives discoverable workflow help without implementation side effects.

## What Changes

- Add **`/lsi:help`** (`overlays/lsi/agent-stack/commands/lsi-help.md`) — read-only one response per invocation: no arg → overview + numbered topic list; `<topic>` → full section from command templates; separate **SDLC diagram** section (mermaid); **`status`** / **`next`** branch → phase → command heuristics; all spec links use **GitHub blob URLs** pinned to `v{BUNDLE_VERSION}` from adopter `PROJECT.md`
- Add `/lsi:help` decision-table row to overlay routing docs after `/opsx:propose`
- Add overlap rule **#7** (`/lsi:help` vs implementation commands) to overlay `which-workflow.md` only
- Extend bundle-root `which-workflow.md` LSI row with “Discovery: `/lsi:help` (overlay)”
- List `/lsi:help` in openspec-git-integration quick reference; append `lsi-help` to parity scripts
- Bootstrap maintainer `.cursor/commands/lsi-help.md`; bump bundle to **v1.4.1**

## Capabilities

### New Capabilities

- `lsi-help-slash-command`: One-turn `/lsi:help` — overview + topic list or single section per invocation, SDLC diagram section, GitHub bundle spec links, adopter parity expectations.

### Modified Capabilities

- *(none — no existing normative spec in `openspec/specs/` is changed by this change)*

## Impact

- `overlays/lsi/agent-stack/commands/lsi-help.md` — slash command; bootstrap → gitignored `.cursor/commands/lsi-help.md`
- Overlay routing docs — decision-table row; overlap rule **#7**
- `VERSION`, `PROJECT.md`, `CHANGELOG.md` — release **v1.4.1**
- Adopters: receive `/lsi:help` after bundle release and `adopt.py` / `/lsi:update` re-sync
