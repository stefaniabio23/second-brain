# /maintain

Vault-wide periodic health pass. Not note-targeted. Run this when the vault needs structural review, not when working on a specific note. All output in chat only. Nothing written to disk without explicit approval.

This skill aggregates the other skills and applies their standards across the full vault.

## Steps

Run all five in sequence. Output findings as a prioritised action queue at the end.

### 1. Frontmatter audit

Walk every note in `sources/`, `atoms/`, `molecules/`, `compounds/`, `authors/`, `MOCs/`.

Check required fields by type using the schema table in CLAUDE.md (already in context). CLAUDE.md is the single source of truth for required fields. Do not rely on a cached copy.

List every violation. For each: `[filename] missing [field]. Fix? (y/n)`. Wait for approval before writing.

Also flag: notes with `title:` in frontmatter (should be dropped), notes with `reference:` instead of `derived-from:` (old schema, should be updated).

### 2. Relink pass

Find note pairs that share tags or `derived-from:` lineage but have no body wikilink between them. Score by signal overlap. Output the top 5-10 pairs. For each: `Offer to run /find-connections on [[note-a]] and [[note-b]]? (y/n)`

Do not write links directly. Delegate to `/find-connections`.

### 3. Tags audit

Count tag usage across all notes.

Flag:
- Tags used fewer than 3 times, candidate for removal or aliasing
- Near-duplicates (e.g. `bio` and `biology`, `market` and `markets`)
- Tags not listed in `_system/tags.md`

Propose canonical list updates. Do not change tags without approval.

### 4. Orphan detection

Find notes with no inbound wikilinks: nothing in the vault links to them. These are the notes most at risk of being forgotten.

For every note in `atoms/`, `molecules/`, `compounds/`, `MOCs/`: search all other notes for `[[filename-stem]]`. If no match, flag as orphan.

Output: list of orphaned notes, ordered by type. For each: `[[filename]] has no inbound links. Add to a molecule, MOC, or find-connections pass? (y/n/skip)`

Do not write anything. Offer to pass each to `/find-connections` if the user wants to surface where it might connect.

### 5. Bottleneck surface

Apply the lens of each primitive skill across the full vault:

- **Sources with no extracted atoms**: flag for `/capture` or `/atom`
- **Atoms never referenced in any molecule**: flag for `/molecule`
- **Notes with no body wikilinks at all**: flag for `/find-connections`
- **Notes with strong, unqualified claims and no `contradicts` annotation**: flag for `/find-contradictions`
- **Topics with 3+ atoms and no MOC**: flag for `/moc`

## Output format

After all four steps, produce a single prioritised action queue:

```
## /maintain findings: [date]

### Must fix (schema violations)
- [filename]: missing derived-from
- [filename]: title: still in frontmatter

### High-signal opportunities
- /find-connections: [[atom-a]] and [[atom-b]] share mechanism language (confidence 0.81)
- /find-contradictions: [[atom-c]] makes a broad claim with no counterclaim in vault

### Low-priority
- Tags: 'bio' and 'biology' are near-duplicates
- /moc: cancer-biology has 8 atoms and no MOC
```

Hand each item to the appropriate primitive skill. Never auto-execute.

## Never

- Write anything without approval.
- Auto-run `/find-connections` or `/find-contradictions` on a batch silently.
- Generate report files to disk.
