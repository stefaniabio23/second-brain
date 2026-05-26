# second-brain

Purpose: operate this `second-brain/` repository as a graph-native knowledge system. This repository is a knowledge base, not a generic file archive. Optimize for retrieval, synthesis, graph clarity, and long-term compounding of understanding.
Pipeline: sources to atoms to molecules to compounds.

## Operating principles

- Keep the system simple enough to use daily.
- Prefer body wikilinks with explanation over heavy frontmatter.
- Use frontmatter only for routing, lineage, and filtering.
- Claude may propose connections, atoms, and molecule candidates.
- When uncertain, ask one precise question or make the smallest reversible proposal.

## Folder structure

```
second-brain/
├── CLAUDE.md
├── sources/          # reference notes, one per source
├── book-notes/       # chapter extractions from books
├── atoms/            # single concepts, self-contained
├── molecules/        # personal insights in your own words
├── compounds/        # re-synthesis: essays, theses, blog posts, projects
├── authors/          # author nodes (created when author links to 2+ sources)
├── MOCs/             # semi-structured navigation indexes on a topic
├── _templates/       # note type templates, excluded from Obsidian graph
└── _system/          # skills and scripts, excluded from Obsidian graph
```

## Obsidian setup

Exclude system folders from graph and search:

Settings > Files and links > Excluded files > Manage. Add:
- `_templates/`
- `_system/`
- `.claude/`

In Graph view, use Groups to colour nodes by folder:
- `path:atoms/`
- `path:molecules/`
- `path:compounds/`
- `path:sources/`
- `path:MOCs/`

## Note types

Closed enum: `source-note`, `book-note`, `atom`, `molecule`, `compound`, `moc`, `author`

Full templates are in `_templates/`. When generating any note, read the template for its type, then:
- Fill required fields with real values.
- Remove unused optional fields entirely.
- Delete all `[bracket placeholders]`, including the brackets and their contents.
- Never leave bracketed text, empty fields, or placeholder values in a finished note.

### Schema table

| Type | Required frontmatter | Folder |
|---|---|---|
| source-note | `type`, `source-type`, `tags` | sources/ |
| book-note | `type`, `tags`, `derived-from` | book-notes/ |
| atom | `type`, `derived-from`, `tags` | atoms/ |
| molecule | `type`, `derived-from`, `tags` | molecules/ |
| compound | `type`, `compound-type`, `derived-from`, `tags` | compounds/ |
| moc | `type`, `tags` | MOCs/ |
| author | `type`, `tags`, `aliases` | authors/ |

Optional fields for source-note: `author`, `source-file`, `url`. Use only what exists.

### Filename conventions

All files: kebab-case, no spaces, no capitals. Never include a date unless the date is the content.

| Type | Convention | Example |
|---|---|---|
| source-note (book) | `book-title-firstname-lastname.md` | `memories-dreams-reflections-carl-jung.md` |
| source-note (paper) | `year-title-slug.md` | `2011-hallmarks-of-cancer.md` |
| source-note (podcast) | `podcast-name-episode-slug.md` | `invest-like-the-best-howard-marks.md` |
| book-note | `book-slug-chapter-n-chapter-name.md` | `atlas-shrugged-chapter-1-theme.md` |
| atom | `concept-slug.md` | `knudson-two-hit-hypothesis.md` |
| molecule | `insight-slug.md` | `senescence-as-checkpoint-not-endpoint.md` |
| compound | `title-slug.md` | `longevity-investment-thesis.md` |
| moc | `topic-moc.md` | `cancer-biology-moc.md` |
| author | `firstname-lastname.md` | `carl-jung.md` |

## Body conventions

- Frontmatter = routing, lineage, filtering only
- Body = meaning, connections, contradictions
- Connections: write `[[wikilink]]` in body prose where the relationship is relevant. `/find-connections` adds explanatory prose alongside approved links.
- Contradictions: write `contradicts [[wikilink]]` as a plain body annotation. `/find-contradictions` writes this on approval only.
- No `related:` or `contradicts:` in frontmatter. Body wikilinks handle both.
- `[[wikilinks]]` are for note links only. Never use brackets for anything else in the body.
- Tags come from `_system/tags.md`. New tags go there first.

## Graph rules

- Colour nodes by `type:` for structure, by `tag:` for topic
- No generated entity nodes. Author nodes and MOCs are the only hubs, and both require deliberate creation.
- `_templates/`, `_system/`, `.claude/` excluded from graph via Obsidian settings

## Skills

Skills live in `_system/`. Run them by name in Claude Code.

| Skill | Frame | What it does |
|---|---|---|
| `/capture` | | Ingest a source into a source-note. Optionally mines 2-5 atom candidates. |
| `/atom` | | Write one atom. Forces claim-shaped title. Never creates automatically. |
| `/molecule` | | Proposes molecule candidates from atoms. You write; Claude surfaces. |
| `/find-connections` | Hermetic correspondence | Find analogies, recurring mechanisms, mirrored patterns, cross-domain correspondences. Proposes body wikilinks with explanation. Writes on approval. |
| `/find-contradictions` | Pyrrhonian skepticism | Place a claim beside serious counterclaims to see the limits of its confidence. Proposes `contradicts [[wikilink]]` annotations. Writes on approval only. |
| `/moc` | | Create or update a MOC. Groupings are proposals; you curate. |
| `/maintain` | | Vault-wide health pass. Aggregates all skills. Chat output only; nothing written without approval. |

