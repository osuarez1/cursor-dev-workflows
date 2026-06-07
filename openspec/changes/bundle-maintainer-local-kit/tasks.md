## 1. Templates and scripts

- [x] 1.1 Finalize `snippets/maintainer-local/` templates (MAINTAINER, AGENTS-LOCAL, local-*.mdc, openspec scaffold)
- [x] 1.2 Ensure `snippets/bootstrap-maintainer-local.sh` supports `--force` and `--refresh-commands`
- [x] 1.3 Complete `snippets/install-maintainer-local-commands.py` link rewrites and overlay source discovery
- [x] 1.4 Implement `snippets/verify-maintainer-local.sh` required-path checks per spec

## 2. Gitignore and examples

- [x] 2.1 Extend `.gitignore` for `local-*.mdc`, `.cursor/commands/`
- [x] 2.2 Add tracked `openspec/config.yaml` and `docs/ai/openspec.md`
- [x] 2.3 Slim `MAINTAINER.md.example` and `AGENTS-LOCAL.md.example` to pointers into `snippets/maintainer-local/`

## 3. Documentation

- [x] 3.1 Add `docs/adopter-boundaries.md` with adopt / never / human / maintainer-only zones
- [x] 3.2 Update `AGENTS.md` and `README.md` with bootstrap, verify, and layout references
- [x] 3.3 Complete `snippets/maintainer-local/README.md` (setup, refresh, boundaries, tracked openspec note)

## 4. Validation

- [x] 4.1 Run bootstrap on clean clone path; confirm all gitignored artifacts install
- [x] 4.2 Run verify; confirm exit 0 when complete and exit 1 when missing
- [x] 4.3 Spot-check rewritten slash command links (`opsx-propose`, `lsi-card`) resolve in bundle layout
- [x] 4.4 Add `[Unreleased]` CHANGELOG entry (MINOR — maintainer-only tooling)
