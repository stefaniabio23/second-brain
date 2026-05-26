# /atom

Write one atom. An atom is a single concept that is self-contained and would plausibly have a Wikipedia page.

## Steps

1. Identify the concept. If unclear, ask: "What is the concept? What source does it come from?"
2. Force a claim-shaped title: an assertion, not a topic noun. If given a topic noun, propose a claim version: `This reads as a topic. Claim form: "[assertion]". Use this? (y/n/edit)` Wait for response.
3. Read `_templates/atom.md`.
4. Draft the atom body: 50-250 words, one concept only. Use plain language. No academic compound nouns where a common word fits.
5. Set `derived-from:` to the source note. If source does not exist in `sources/`, flag: "Source note not found. Create it first with /capture, or specify the path."
6. Show full draft. Ask: `Write to atoms/[filename].md? (y/n/edit)`
8. On approval, write.
9. After writing, scan `atoms/` for existing notes that should be linked from the body. If found, propose as body wikilinks one at a time. Do not write without approval.

## Claim-shaped title rule

Good: `Both alleles of a tumor suppressor must be inactivated for cancer to develop`
Bad: `Knudson two-hit hypothesis` (topic noun, not assertion)

The title should read like a sentence someone might say out loud. Drop academic compound nouns and nominalised abstractions.

## Never

- Create without asking.
- Write the body of a molecule or compound when asked for an atom.
- Exceed 250 words in the body.
- Leave `derived-from:` empty.

