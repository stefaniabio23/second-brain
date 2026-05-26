# /find-connections

**Frame: Hermetic correspondence.** Find analogies, recurring mechanisms, mirrored patterns, and cross-domain correspondences. The goal is not to link notes that share a topic. The goal is to find notes where the same underlying structure appears in different contexts.

## Usage

- `/find-connections [[note]]`: targets one note
- `/find-connections`: vault-wide pass, surfaces the highest-signal connection opportunities

## Candidate sources

Before running step 2, check whether `_system/embeddings.json` exists (built by `_system/embed.py`).

If it exists: run `python3 _system/embed.py --search [note-path]` first and include the embedding candidates in the search pool. Embedding similarity finds cross-domain correspondences that tag and lineage matching miss entirely.

If it does not exist: proceed with tag and lineage matching only.

## Steps (note-targeted)

1. Read the target note. Identify: core mechanism, claim, pattern, tags, `derived-from:` lineage, existing body wikilinks.
2. Search the vault by:
   - Embedding similarity (from `embed.py --search`, if available — highest signal)
   - Shared tags (same domain, necessary but not sufficient for a good connection)
   - Shared `derived-from:` lineage (same source, different concept)
   - Similar mechanism language (feedback, constraint, threshold, emergence, lineage, selection)
   - Wikilink neighbourhood ("what do my neighbours link to that I don't?")
3. For each candidate, identify the relation type:
   - Analogous mechanism: same structure, different domain
   - Same concept, different context: the concept appears in both but neither links to the other
   - Prerequisite knowledge: understanding one note requires the other
   - Parallel discovery: two sources reach the same conclusion independently
   - Structural mirror: the logic of one inverts or completes the logic of the other
4. Filter out weak connections: two notes being in the same topic domain is not a connection. A shared mechanism or mirrored structure is.
5. Propose connections as a ranked list, one at a time or as a batch for review:

```
[[target-note]]
Relation: analogous mechanism
Reason: Both describe stability emerging from negative feedback. The RAS checkpoint
mechanism mirrors the control systems principle in [other-note].
Confidence: 0.81
Add to body? (y/n)
```

6. On approval: write a prose sentence in the body of the current note explaining why the link matters, with `[[wikilink]]` embedded naturally in the sentence.

## Steps (vault-wide)

1. Find note pairs that share tags or `derived-from:` lineage but have no body wikilink between them.
2. Score by signal overlap (shared tags + shared lineage + mechanism similarity).
3. Output a prioritised list of the top 5-10 pairs.
4. Offer to run the note-targeted version on each pair. Do not write anything vault-wide automatically.

## Never

- Write a connection without approval.
- Add a `related:` frontmatter field. Body only.
- Propose a connection because two notes share a topic tag alone.
- Write more than one prose sentence per approved connection unless the user asks.
