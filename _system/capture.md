# /capture

Ingest a substantive source (article, paper, podcast transcript, essay) into a source-note. Optionally mines atom candidates in the same pass.

## Steps

1. Ask for the source if not provided. Provide a URL, pasted text, or description.
2. Identify: title, author, source-type, relevant tags.
3. Read `_templates/source-note.md`.
4. Generate the source-note: populate frontmatter, write `## Short summary` (2-3 sentences), populate `## Key concepts` with the most important concepts from the source and any natural body wikilinks to existing atoms.
5. Show the full draft. Ask: `Write to sources/[filename].md? (y/n/edit)`
7. On approval, write.
8. After writing, offer to mine atom candidates: scan the Key concepts section for concepts that would have a Wikipedia page and are not already in `atoms/`. Surface up to 5.
9. Propose each candidate one at a time: `Atom candidate: "[claim-shaped title]". Save? (y/n/edit/skip)`. Wait for response before showing the next.
10. For each approved candidate, read `_templates/atom.md`, fill in, and write to `atoms/[filename].md`.

## Filename convention

Follow the filename rules in CLAUDE.md exactly. Book sources: `book-title-firstname-lastname.md`. Papers: `year-title-slug.md`. Podcasts: `podcast-name-episode-slug.md`.

## Never

- Create atoms automatically without proposing each one individually.
- Write to any folder other than `sources/` and `atoms/`.
- Bulk-create notes.
- Leave bracketed template text in finished notes.

