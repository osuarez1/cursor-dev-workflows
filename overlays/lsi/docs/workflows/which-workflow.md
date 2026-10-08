# Which workflow?

Use this routing guide when the user’s request could match more than one document.

Full OpenSpec + Git lifecycle: [openspec-git-integration.md](openspec-git-integration.md).

## Decision table

| User says (examples) | Use | Command | Output / verdict |
|----------------------|-----|---------|------------------|
| explore idea, think through change | [openspec-git-integration.md](openspec-git-integration.md) | `/opsx:explore` | Discussion; docs-only on protected branches |
| propose OpenSpec change | [openspec-git-integration.md](openspec-git-integration.md) | `/opsx:propose` | proposal, design, tasks |
| which command, workflow help, lost, LSI onboarding, what should I run next (discovery) | [lsi-help.md](../../.cursor/commands/lsi-help.md) | `/lsi:help` | Overview + topic list; `/lsi:help <topic>` for section — read-only one-shot |
| sync delta specs | [openspec-git-integration.md](openspec-git-integration.md) | `/opsx:sync` | Main specs updated |
| create Trello card and branch, `/lsi:card` | [openspec-git-integration.md](openspec-git-integration.md) | `/lsi:card` | Card + branch via `git ts` from `main`/`staging` |
| link Trello card to existing branch, `/lsi:card-link` | [openspec-git-integration.md](openspec-git-integration.md) | `/lsi:card-link` | Requires open OpenSpec; card body redacted from artifacts |
| list Trello To Do cards, `/lsi:trello-list` | [git-trello.md](../sdlc/git-trello.md) | `/lsi:trello-list` | Picker → confirm; requires OpenSpec to branch |
| branch from existing Trello card, `/lsi:trello-branch` | [git-trello.md](../sdlc/git-trello.md) | `/lsi:trello-branch` | Requires open OpenSpec; sync card then `git tb` |
| draft ticket card, task type/title/description (no CLI) | [ticket-card-info.md](ticket-card-info.md) | — | Three labeled copy-paste blocks (type, title, description); use `/lsi:card` for card + branch |
| create branch, wrong branch, on main | [branch-workflow.md](branch-workflow.md) | `/lsi:branch` | Refuse or redirect to ticket branch |
| draft PR title, PR description, PR copy | [pull-requests.md](pull-requests.md) | `/lsi:pr` | Title + markdown body |
| production promotion PR (staging → main) | [openspec-git-integration.md](openspec-git-integration.md) | `/lsi:promote` | Promotion PR to `main` |
| close after promotion merge | [openspec-git-integration.md](openspec-git-integration.md) | `/lsi:close` | Sync + archive + CLOSED.md on **`main`** only after `/lsi:promote` merges |
| ready for PR, production ready, ship checklist | [pr-production-readiness.md](pr-production-readiness.md) | `/lsi:readiness` | Checklist + verdict |
| code review, review branch | [code-review.md](code-review.md) | `/lsi:review` | Summary + verdict |
| unattended PR bot, Mode A/B bot session, apply-bot | [integrations.md](integrations.md) · [bot-sessions.md](bot-sessions.md) | `/lsi:pr-bot`, `/lsi:pr-bot-docs`, `/lsi:apply-bot` | Posted session + Close verdict |
| senior analysis, design alternatives | [senior-analysis.md](senior-analysis.md) | `/lsi:senior` | Full report + verdict |
| merge extended description (Bitbucket) | [openspec-git-integration.md](openspec-git-integration.md) | `/lsi:merge-desc` | Extended merge body |
| commit plan, logical commits | [commits-logical-order.md](commits-logical-order.md) | `/lsi:commit` | Commit plan; commit only if asked |
| version bump, changelog, release tag | [versioning-and-releases.md](versioning-and-releases.md) | `/lsi:version`, `/lsi:changelog`, `/lsi:release`, `/lsi:bootstrap-release` | Release train on `main` |
| re-sync bundle, adopt update, workflow update | [adopt-and-update.md](adopt-and-update.md) | `/lsi:update` | Re-sync adopted workflows from bundle |
| when are tests required | [test-requirements.md](test-requirements.md) | — | Policy |
| OpenSpec apply / archive | [openspec-git-integration.md](openspec-git-integration.md) | `/opsx:apply`, `/opsx:archive` | Archive via `/lsi:close` on **`main`** after promote merges — see overlay |

## Overlap rules

1. **PR conventions vs readiness vs code review** — [pull-requests.md](pull-requests.md) defines title/body format. [pr-production-readiness.md](pr-production-readiness.md) is the readiness checklist and verdict. [code-review.md](code-review.md) walks logic, security, performance, and tests in depth. Run readiness **before** opening a PR; run code review before merge.
2. **Senior analysis vs code review** — Senior analysis explains design and alternatives; it does **not** replace security/performance/test gates. Use different verdict words (never `Ready` for senior analysis).
3. **Bot session vs standalone review** — `/lsi:pr-bot` / `/lsi:pr-bot-docs` / `/lsi:apply-bot` authorize posting (and with `--fix`/apply, commit/push) for one PR/change that session only. Standalone `/lsi:review` / `/lsi:senior` keep “ask before post” defaults — [integrations.md](integrations.md).
4. **Ticket card vs implementation** — Card drafting does not authorize coding on a protected branch. Use **`/lsi:card`** when the user wants card + branch from `main`/`staging`; use **`/lsi:card-link`** when work already exists on a branch without a Trello id; draft-only blocks when they want copy-paste fields only.
5. **`/lsi:card` vs `/lsi:card-link` vs trello commands vs `git ts`** — `/lsi:card` runs `git ts` (new branch). `/lsi:card-link` and trello flows require OpenSpec and redact card copy before Trello API. `/lsi:trello-list` is interactive picker → confirm → optional `git tb`. Never run raw `git ts` when linking an existing card.
6. **Commit plan vs commit execution** — Always show a plan before the first commit on a branch when multiple logical changes exist. Run `git commit` only when the user explicitly asks (bot sessions: via `.lsi/bin/lsi-bitbucket`).
7. **`tasks.md` vs close** — `/opsx:apply` completes `tasks.md` deliverables only. Do **not** add `/opsx:sync`, `/opsx:archive`, or `/lsi:close` as tasks; run `/lsi:close` on **`main`** after the promotion PR merges.
8. **`/lsi:help` vs implementation commands** — `/lsi:help` is read-only reference output (one response per invocation); it may suggest the next command but does **not** run `/lsi:*`, `/opsx:*`, `git ts`/`git tb`, Trello API, `adopt.py`, or commits. When the user wants to **do** work (card, apply, PR, close), use the implementation command. Session detail: [lsi-help.md](../../.cursor/commands/lsi-help.md).

## Flowchart

```mermaid
flowchart TD
  start[User request]
  start --> explore{Explore or propose?}
  explore -->|explore| opsxExplore["/opsx:explore"]
  explore -->|propose| opsxPropose["/opsx:propose"]
  explore -->|no| ticket{Card + branch?}
  ticket -->|yes /lsi:card| lsiCard["/lsi:card → git ts"]
  ticket -->|link existing branch| lsiCardLink["/lsi:card-link"]
  ticket -->|existing To Do card| lsiTrelloList["/lsi:trello-list → trello-branch"]
  ticket -->|draft only| ticketInfo[ticket-card-info.md]
  ticket -->|no| branch{On protected branch or no ticket?}
  branch -->|yes| bw[branch-workflow.md]
  branch -->|no| intent{Primary intent?}
  intent -->|design or alternatives| sa[senior-analysis.md]
  intent -->|review code| cr[code-review.md]
  intent -->|draft PR title or body| prConv[pull-requests.md]
  intent -->|PR or production ready| pr[pr-production-readiness.md]
  intent -->|commits| co[commits-logical-order.md]
  intent -->|release| rel[versioning-and-releases.md]
  intent -->|unclear| ask[Ask one focused question then route]
```

## Recommended order (large feature)

1. `/opsx:explore` (optional) — clarify problem  
2. `/opsx:propose <slug>` — proposal, design, tasks  
3. `/lsi:senior` — when design is large (runtime-critical, integration-heavy, multi-module)  
4. `/lsi:card` from **`main`** or **`staging`** — Trello card + ticket branch  
5. `/opsx:apply` — implement `tasks.md`  
6. [test-requirements.md](test-requirements.md) — while coding  
7. `/lsi:commit` — when user asks  
8. `/lsi:readiness` — before PR  
9. `/lsi:review` — before merge  
10. `/lsi:pr` mode **A** — OpenSpec docs only to **`staging`**
11. After Mode A merge — `/lsi:merge-desc`; keep change active
12. `/opsx:apply` → commits → readiness → review → `/lsi:pr` mode **B** to **`staging`**
13. After Mode B merge — `/lsi:merge-desc`; **do not** sync or archive yet
14. Staging QA → `/lsi:promote` — target **`main`** (change still active)
15. After main merge → `/lsi:merge-desc` then `/lsi:close` on **`main`** only; optional release-train on **`main`**

## Related

- [PROJECT.md](../../PROJECT.md) — placeholders and adoption
- [openspec-git-integration.md](openspec-git-integration.md) — OpenSpec + Git overlay  
- [versioning-and-releases.md](versioning-and-releases.md) — release commands  
- [common-mistakes.md](common-mistakes.md) — confusing workflows  
