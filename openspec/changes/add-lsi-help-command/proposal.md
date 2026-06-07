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

## PR scope (staging → this branch)

**Do not treat this PR as a single-feature diff.** The ticket is `add-lsi-help-command`, but `staging...HEAD` bundles additional staging-integration work:

1. **Production-close `fix-review-nits`** — archive under `openspec/changes/archive/2026-06-07-fix-review-nits/`; delta specs synced to normative **`openspec/specs/`** (`adopt-bundle-version-token`, `maintainer-cursor-gitignore`, `trello-card-slash-commands`)
2. **Release train** — **`v1.4.0`** bump (CHANGELOG/VERSION/PROJECT) on staging integration path; **`v1.4.1`** for `/lsi:help` (including one-turn model refactor)
3. **Prior promotion merge** — `chore(release): promote bundle v1.3.0 and review fixes to main` (cumulative staging→main integration commit on this branch)
4. **`add-lsi-help-command`** (primary) — `/lsi:help` one-turn slash command, overlay routing, parity scripts, OpenSpec change artifacts

Reviewers: judge **`/lsi:help`** and **v1.4.1** against this change’s proposal/design/spec; treat archive/sync and **v1.4.0** promotion as bundled staging hygiene, not as lsi-help feature scope.

**Routing verification note:** task **5.7** is a **static** pass — decision-table phrase matching is **documented and accepted**; not live Agent dogfood. **Optional follow-up:** three fresh Agent chats with plain-text discovery prompts (`which command should I use?`, `I'm lost on the LSI workflow`, `what should I run next?`) to confirm real routing; implement task **2.4** flowchart branch if any fail.

**PR risk (flowchart gap — no code change unless live dogfood fails):** Overlay decision table routes discovery to `/lsi:help`; overlay mermaid flowchart still omits an early help branch — intentional per closed task **2.4**. Documented here; implement flowchart branch only if optional live routing dogfood (**5.7** follow-up) fails.

**PR testing note:** `python3 snippets/verify-adopters.py --repo-root .` fails on the bundle maintainer repo (no `.lsi/workflows/`) — expected; task **5.5** is adopter parity after adopt re-sync, not bundle maintainer smoke.

**PR risk (agent-dependent section rendering):** No programmatic enforcement — agents must read `## Section:` blocks from command source. Chat dogfood matched overview, `sdlc`, `lifecycle`, `next`, and invalid topic. **Residual risk for other agents/models only.**
