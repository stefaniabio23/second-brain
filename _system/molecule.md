# /molecule

Surface molecule candidates from a set of atoms. A molecule is a personal insight: self-contained, in the user's own words, something they are comfortable calling their own intuition.

Claude surfaces the signal. The user writes the molecule.

## Steps

1. Take a set of atoms, either specified by the user, or from a tag or topic search.
2. Read each atom in the set.
3. Look for:
   - Moments where two atoms, read together, imply something neither states alone
   - A conclusion that bridges two sources treating the same concept differently
   - A personal reframing of a concept in terms of another domain
   - A pattern that recurs across atoms from different sources
4. Propose candidates one at a time: `Molecule candidate: "[claim as assertion]". This bridges [[atom-a]] and [[atom-b]] because [one sentence]. Develop? (y/n/skip)`
5. If yes: show the `derived-from:` links and `tags:` that would go in frontmatter. Write a one-sentence prompt to start the body. Stop there.
6. Wait for the user to write the molecule body.
7. When the user is ready: read `_templates/molecule.md`, offer to write the frontmatter and filename to `molecules/[filename].md`.

## Never

- Write the molecule body. That synthesis belongs to the user.
- Present more than one candidate at a time.
- Create a molecule automatically.
- Propose a candidate that is merely a summary of a single atom. A molecule must bridge or reframe.
