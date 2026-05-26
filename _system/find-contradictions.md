# /find-contradictions

**Frame: Pyrrhonian skepticism.** Withhold premature certainty by placing a claim beside serious counterclaims until the mind sees the limits of its own confidence. This is not "deny everything." It is a discipline of surfacing the scope and fragility of a claim before accepting it.

Skill behaviour: find serious contradictions, counterexamples, tensions, and scope limits for a note's central claim.

## Usage

- `/find-contradictions [[note]]`: targets one note
- `/find-contradictions`: vault-wide pass, surfaces notes with strong claims and no contradiction annotations yet

## Steps (note-targeted)

1. Read the target note. Extract the central claim in one sentence.
2. Ask internally: "What would have to be true for this claim to be wrong? What is its scope limit? What mechanism could reverse this?"
3. Search the vault for:
   - Opposite mechanisms (note A says X stabilises Y; another says X destabilises Y)
   - Scope limits (note A makes a general claim; another shows it fails under a named condition)
   - Causal reversals (A causes B vs. B causes A)
   - Mechanism conflicts (same outcome explained through incompatible mechanisms)
   - Same `derived-from:` source, different conclusions (different readings of the same book)
4. Propose contradictions one at a time:

```
[[target-note]]
Conflict: This note argues symbolic systems orient intelligence. The target note argues
they can narrow what the system is capable of perceiving.
Severity: moderate (scope limit, not direct reversal)
Confidence: 0.73
Add contradicts annotation? (y/n)
```

5. On approval: write `contradicts [[wikilink]]` as a plain body annotation. Add one sentence beneath it explaining the specific tension in plain language.

## Steps (vault-wide)

1. Identify notes with strong, unqualified claims and no existing `contradicts` body annotation.
2. Score by claim strength and breadth (broader claims are higher priority targets).
3. Output a list of the top candidates.
4. Offer to run note-targeted version on each. Do not write anything automatically.

## Severity scale

- **Direct**: the claims flatly contradict each other. One must be wrong.
- **Moderate**: one claim is a scope limit or counterexample to the other. Both can be true in different conditions.
- **Tangential**: the notes are in tension but address different aspects of the same domain

## Never

- Write anything without approval.
- Propose contradictions for notes that merely address different topics.
- Confuse "different perspective" with "contradiction". Surface only genuine epistemic conflict.
- Add `contradicts:` to frontmatter. Body annotation only.
