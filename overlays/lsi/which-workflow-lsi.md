# LSI overlay rows for which-workflow.md

Merge these rows into the decision table when adopting with `--overlay lsi`.

| User says (examples) | Use | Command | Output / verdict |
|----------------------|-----|---------|------------------|
| explore idea, think through change | [openspec-git-integration.md](openspec-git-integration.md) | `/opsx:explore` | Discussion; docs-only on protected branches |
| propose OpenSpec change | [openspec-git-integration.md](openspec-git-integration.md) | `/opsx:propose` | proposal, design, tasks |
| which command, workflow help, lost, LSI onboarding, what should I run next (discovery) | [lsi-help.md](agent-stack/commands/lsi-help.md) | `/lsi:help` | Overview + topic list; `/lsi:help <topic>` for section — read-only one-shot |
| sync delta specs | [openspec-git-integration.md](openspec-git-integration.md) | `/opsx:sync` | Main specs updated |
| create Trello card and branch, `/lsi:card` | [openspec-git-integration.md](openspec-git-integration.md) | `/lsi:card` | Card + branch via `git ts` from `main`/`staging` |
| link Trello card to existing branch | [openspec-git-integration.md](openspec-git-integration.md) | `/lsi:card-link` | OpenSpec required; redacted card + rename branch |
| list Trello To Do cards | [git-trello.md](docs/sdlc/git-trello.md) | `/lsi:trello-list` | Interactive picker; OpenSpec required to branch |
| branch from existing Trello card | [git-trello.md](docs/sdlc/git-trello.md) | `/lsi:trello-branch` | OpenSpec required; sync card + `git tb` |
| production promotion PR (staging → main) | [openspec-git-integration.md](openspec-git-integration.md) | `/lsi:promote` | Promotion PR to `main` |
| production close (sync + archive on main) | [openspec-git-integration.md](openspec-git-integration.md) | `/lsi:close` | Close change after main merge |
| merge extended description (Bitbucket) | [openspec-git-integration.md](openspec-git-integration.md) | `/lsi:merge-desc` | Extended merge body |
| version bump, changelog, release tag | [versioning-and-releases.md](versioning-and-releases.md) | `/lsi:version`, `/lsi:changelog`, `/lsi:release`, `/lsi:bootstrap-release` | Release train on `main` |
| re-sync bundle / adopt update | [adopt-and-update.md](../../../docs/adopt-and-update.md) | `/lsi:update` | Re-sync adopted workflows from bundle |
| OpenSpec apply / archive | [openspec-git-integration.md](openspec-git-integration.md) | `/opsx:apply`, `/opsx:archive` | Archive on `main` only — see overlay |
