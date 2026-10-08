# adopt-local-artifacts-gitignore Specification

## Purpose
Adopt-managed .gitignore block for .reviews/ and .senior-analyses/.

## Requirements
### Requirement: Adopt manages a local-artifacts gitignore block

`snippets/adopt.py` SHALL upsert a marker-delimited block (`# >>> lsi:local-artifacts … >>>` / `# <<< lsi:local-artifacts <<<`) in the adopter's `.gitignore` whose entries come from `snippets/gitignore-local-artifacts.txt` and include at least `.reviews/` and `.senior-analyses/`. It SHALL create `.gitignore` if absent and SHALL NOT alter lines outside the markers.

#### Scenario: Idempotent upsert

- **WHEN** adopt runs twice
- **THEN** `.gitignore` contains exactly one managed block with identical content

#### Scenario: Adopter lines preserved

- **WHEN** `.gitignore` already lists `.reviews/` outside the block plus unrelated entries
- **THEN** those lines are unchanged and the managed block is added

### Requirement: Verify checks ignore coverage

`snippets/verify-adopters.py` SHALL fail when the managed block is missing or when `git check-ignore` does not ignore `.reviews/` and `.senior-analyses/` paths in the adopter.

#### Scenario: Missing block fails verify

- **WHEN** an adopter's `.gitignore` lacks the managed block
- **THEN** verify reports `missing lsi:local-artifacts gitignore block`
