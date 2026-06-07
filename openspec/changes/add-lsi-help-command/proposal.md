## Why

LSI adopters have many slash commands and workflow specs under `.lsi/workflows/`, but no single entry point for developers to discover the staging-first SDLC, pick the right command, or deep-link to bundle documentation. Dumping the full lifecycle and command tables in one chat response is hard to scan. An interactive **`/lsi:help`** command — overview first, then a menu-driven session until Exit — gives discoverable workflow help without implementation side effects.

## What Changes

- Add **`/lsi:help`** (`overlays/lsi/agent-stack/commands/lsi-help.md`) — read-only interactive session: overview once, then AskQuestion menu (9 sections + Exit); user stays in help until Exit; every section response re-displays the menu; separate **SDLC diagram** section (mermaid, staging-first happy path); **`status`** / **`next`** branch → phase → command heuristics; all spec links use **GitHub blob URLs** on [osuarez1/cursor-dev-workflows](https://github.com/osuarez1/cursor-dev-workflows), pinned to `v{BUNDLE_VERSION}` from adopter `PROJECT.md`
- Add `/lsi:help` decision-table row to overlay routing docs (`overlays/lsi/docs/workflows/which-workflow.md`, `overlays/lsi/which-workflow-lsi.md`) after `/opsx:propose`
- Add overlap rule **#7** (`/lsi:help` vs implementation commands) to overlay `which-workflow.md` only
- Extend bundle-root `which-workflow.md` LSI row with “Discovery: `/lsi:help` (overlay)” — no full overlap rule at root
- List `/lsi:help` in `overlays/lsi/agent-stack/openspec-git-integration.mdc` and `overlays/lsi/docs/workflows/openspec-git-integration.md` quick reference
- Append `lsi-help` to `LSI_COMMANDS` in `snippets/verify-adopters.py` and `snippets/audit-agent-docs.py`
- Bootstrap maintainer `.cursor/commands/lsi-help.md` via `snippets/bootstrap-maintainer-local.sh` (or `install-maintainer-local.py`)
- Bump bundle to **v1.4.1** — `VERSION`, `PROJECT.md` `BUNDLE_VERSION`, and `[Unreleased]` `CHANGELOG.md` entry for `/lsi:help`

## Capabilities

### New Capabilities

- `lsi-help-slash-command`: Interactive `/lsi:help` slash command — overview, section menu, session loop until Exit, SDLC diagram section, GitHub bundle spec links, adopter parity expectations.

### Modified Capabilities

- *(none — no existing normative spec in `openspec/specs/` is changed by this change)*

## Impact

- `overlays/lsi/agent-stack/commands/lsi-help.md` — new slash command; bootstrap → gitignored `.cursor/commands/lsi-help.md` in bundle repo
- `overlays/lsi/docs/workflows/which-workflow.md`, `overlays/lsi/which-workflow-lsi.md` — decision-table row; overlap rule **#7** in overlay `which-workflow.md` only
- `which-workflow.md` (bundle root) — LSI discovery pointer to `/lsi:help`
- `overlays/lsi/agent-stack/openspec-git-integration.mdc`, `overlays/lsi/docs/workflows/openspec-git-integration.md` — quick-reference listing
- `snippets/verify-adopters.py`, `snippets/audit-agent-docs.py` — `lsi-help` in `LSI_COMMANDS`
- `VERSION`, `PROJECT.md`, `CHANGELOG.md` — release **v1.4.1** and `/lsi:help` changelog entry
- Overlay flowchart early branch for workflow help → `/lsi:help` — **not in initial apply**; task **2.4** gated by dogfood routing test **5.7** (close 2.4 on pass; implement on fail)
- Adopters: receive `/lsi:help` after bundle release and `adopt.py` / `/lsi:update` re-sync
