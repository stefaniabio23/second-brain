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

All files: kebab-case, no spaces, no capitals. Papers and books include a year prefix; atoms and molecules do not.

| Type | Convention | Example |
|---|---|---|
| source-note (book) | `YYYY-firstname-lastname-book-title.md` | `1962-carl-jung-memories-dreams-reflections.md` |
| source-note (paper) | `YYYY-title-slug.md` | `2011-hallmarks-of-cancer.md` |
| source-note (podcast) | `YYYY-podcast-name-episode-slug.md` | `2023-invest-like-the-best-howard-marks.md` |
| source-note (university-module) | `YYYY-name-of-module.md` | `2021-molecular-basis-of-disease.md` |
| book-note | `book-slug-chapter-n-chapter-name.md` | `atlas-shrugged-chapter-1-theme.md` |
| atom | `concept-slug.md` | `knudson-two-hit-hypothesis.md` |
| molecule | `insight-slug.md` | `senescence-as-checkpoint-not-endpoint.md` |
| compound | `title-slug.md` | `longevity-investment-thesis.md` |
| moc | `topic-moc.md` | `cancer-biology-moc.md` |
| author | `firstname-lastname.md` | `carl-jung.md` |

### H1 title convention

Source-note H1: `Author Name Title` — author first, no separator, no em dash. For multi-author papers: primary author et al. For ancient texts: conventional author name first.

## Body conventions

- Frontmatter = routing, lineage, filtering only
- Body = meaning, connections, contradictions
- Connections use both placements:
  1. **Inline in prose** — embed `[[wikilink]]` inside the Implication or Evidence paragraph where the mechanism is being explained. The link lives inside a sentence that says *why* the two notes relate.
  2. **`Related:` section** — a dedicated block at the end of the body, one bullet per connection. Each bullet is a full sentence naming the mechanism with the wikilink embedded. Example: "DNA methylation at CpG islands can epigenetically silence a tumour suppressor's promoter, acting as an alternative second hit in [[knudson-two-hit-hypothesis]] alongside mutation and deletion."
  A bare `[[wikilink]]` with no explanatory sentence is not a valid connection in either location. `/find-connections` surfaces candidates and drafts both placements before writing.
- Contradictions: write `contradicts [[wikilink]]` as a plain body annotation. `/find-contradictions` writes this on approval only.
- No `related:` or `contradicts:` in frontmatter. Body wikilinks handle both.
- `[[wikilinks]]` are for note links only. Never use brackets for anything else in the body.
- Tags come from `_system/tags.md`. New tags go there first.

## Pre-write rule

Every skill that writes prose to the vault runs `/stop-slop` and `/writing-voice` on the draft before writing to disk. These are external skills installed globally at `~/.claude/skills/`. If either is not installed, the skill flags it and asks whether to proceed without the check.

`/writing-voice` is the primary call — it handles voice calibration and calls `/stop-slop` internally for mechanical checks. Run both explicitly until you confirm the chain is wired in your installation.

## Graph rules

- Use folder path groups for note type (`path:atoms/`, `path:molecules/`, `path:sources/`, `path:compounds/`, `path:MOCs/`). Native Obsidian graph groups work with `path:` and `tags:`, not arbitrary frontmatter fields.
- Use tags for topic overlays.
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

External skills — install separately at `~/.claude/skills/`:

| Skill | What it does |
|---|---|
| `/stop-slop` | Mechanical writing quality checks: em dashes, banned filler, passive constructions. Called before any prose is written to disk. |
| `/writing-voice` | Voice calibration for prose output. Calls `/stop-slop` internally. Primary pre-write call for all prose-writing skills. |
| `/book-notes` | Chapter-level book extraction. Output lands in `book-notes/` with `type: book-note` and `derived-from:` pointing at the source note. |

