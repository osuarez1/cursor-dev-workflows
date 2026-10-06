# Migrate AGENTS archive lists → `openspec/CLOSED.md`

One-time adopter migration when adopting close-before-promote + CLOSED.md.

## Steps

1. Create `openspec/CLOSED.md` from the bundle template (or copy the header from this repo’s `openspec/CLOSED.md`).
2. Export each archived-change bullet currently under `AGENTS.md` (or similar) into CLOSED.md using the entry format.
3. Replace the AGENTS bullet list with a single pointer:

   ```markdown
   - **Closed OpenSpec changes:** [openspec/CLOSED.md](openspec/CLOSED.md)
   ```

4. Do not keep both a full AGENTS archive list and CLOSED.md long-term.

Web/infra and other adopters with historical AGENTS archive sections should run this once after `/lsi:update` lands the new close policy.
