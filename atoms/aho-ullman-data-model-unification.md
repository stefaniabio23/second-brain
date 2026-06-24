---
type: atom
tags: [computer-science, mathematics]
derived-from: "[[sources/1992-alfred-aho-jeffrey-ullman-foundations-of-computer-science]]"
---
# Aho and Ullman unify algorithms and data structures under a single "data model" abstraction across five consecutive chapters

The 1992 Foundations of Computer Science devotes one chapter each to the tree data model (Ch 5), list data model (Ch 6), set data model (Ch 7), relational data model (Ch 8), and graph data model (Ch 9). The naming choice is the claim: each structure is framed as a data model, not as a "data structure" or "container." A data model carries operations, invariants, and a query surface, not just storage layout.

The unification matters because most undergraduate CS pedagogy splits these into two unrelated tracks: a data-structures course (lists, trees, graphs) and a separate databases course (relational, sometimes sets). Aho and Ullman collapse them under one umbrella, making the relational model a natural extension of the sequence rather than a database-specific oddity.

**Implication:** The framing predates and parallels how modern systems treat data: dataframes, JSON, graph DBs, and vector stores all live in the same conceptual space. Ullman's subsequent career (the canonical relational-databases textbook, then the data-mining textbook) reads as a continuation of this single-umbrella view.

**Related:**
- [[sources/1992-alfred-aho-jeffrey-ullman-foundations-of-computer-science]]
- [[aho-ullman-mechanization-of-abstraction-as-defining-act]]
