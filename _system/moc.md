# /moc

Create or update a MOC (Map of Content) for a topic. A MOC is a semi-structured navigation index. It lists and loosely groups the atoms, molecules, sources, and compounds on a topic. MOCs are written by Claude but curated by the user.

## When to run

- `/maintain` surfaces 3+ atoms on a topic with no existing MOC, triggering a prompt to run `/moc`
- Manually when a topic feels dense enough to need a map

## Steps

1. Identify the topic from the user's argument or from `/maintain` output.
2. Search the vault:
   - All notes with matching tags
   - Notes in `derived-from:` chains related to the topic
   - Body wikilinks in topic-adjacent notes that point to unlisted notes
3. Group findings into: Sources, Atoms, Molecules, Compounds.
4. Draft a short summary (2-3 sentences) explaining what this MOC covers and why it exists as a map.
5. Run `/stop-slop` and `/writing-voice` on the summary prose. If either is not installed: `[skill] not found. Proceed without the check? (y/n)` — continue only on confirmation.
6. Read `_templates/moc.md`.
7. Show the full draft. Ask: `Write to MOCs/[topic]-moc.md? (y/n/edit)`
7. Flag any groupings that feel uncertain: "I put [[note]] under Atoms but it could be a Molecule. Check this."

## Updating an existing MOC

1. Read the existing MOC file.
2. Search vault for notes on the topic added since the MOC was last updated (check for notes not yet listed).
3. Propose additions to the relevant sections. Ask before writing.

## Never

- Create a MOC for fewer than 3 atoms on a topic. Flag the shortfall to the user instead.
- Write automatically.
- Impose rigid structure. MOC groupings are proposals, not taxonomy.
