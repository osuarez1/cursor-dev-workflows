## Why

LSI adopters have many slash commands and workflow specs under `.lsi/workflows/`, but no single entry point for developers to discover the staging-first SDLC, pick the right command, or deep-link to bundle documentation. Dumping the full lifecycle and command tables in one chat response is hard to scan. An interactive **`/lsi:help`** command — overview first, then a menu-driven session until Exit — gives discoverable workflow help without implementation side effects.

## What Changes

**This change adds OpenSpec artifacts only.** Bundle implementation is deferred to a follow-on `/opsx:apply` on the same change slug.

**Future implementation (documented in `tasks.md`, not in this PR scope):**

- Add **`/lsi:help`** (`lsi-help.md`) to `overlays/lsi/agent-stack/commands/`
- Update routing docs and `openspec-git-integration.mdc` to list the command
- Extend `verify-adopters.py` and `audit-agent-docs.py` parity lists
- Bootstrap maintainer `.cursor/commands/`; bump bundle to **v1.4.1** with CHANGELOG entry

**Behavior (specified in `design.md` and delta spec):**

- Read-only interactive session: overview once, then AskQuestion menu (9 sections + Exit)
- User stays in help until Exit; every section response re-displays the menu
- Separate **SDLC diagram** menu section (mermaid, staging-first happy path)
- All spec links in help output point to **GitHub blob URLs** on [osuarez1/cursor-dev-workflows](https://github.com/osuarez1/cursor-dev-workflows), pinned to `v{BUNDLE_VERSION}` from adopter `PROJECT.md`

## Capabilities

### New Capabilities

- `lsi-help-slash-command`: Interactive `/lsi:help` slash command — overview, section menu, session loop until Exit, SDLC diagram section, GitHub bundle spec links, adopter parity expectations.

### Modified Capabilities

- *(none — no existing normative spec in `openspec/specs/` is changed by this change)*

## Impact

- **This change:** `openspec/changes/add-lsi-help-command/` artifacts only
- **Follow-on apply:** bundle overlay command, router rows, parity scripts, VERSION 1.4.1
- **Adopters:** receive `/lsi:help` after bundle release and `adopt.py` / `/lsi:update` re-sync
