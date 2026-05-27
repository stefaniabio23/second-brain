# second-brain

This repository contains my implementation of second-brain concepts built into a graph-native knowledge system for Obsidian, operated with Claude Code. Read more about my exploration for this system in my ([blog post](https://stephanierebecca.com/posts/second-brain/)). 

This is my personal workflow, heavily influenced by my friend Robert Martin's detailed system ([MolecularNotes](https://github.com/robertmartin8/MolecularNotes)). Since this is a personal implementation, not a generic template, anyone forking it should understand they're adapting rather than copying wholesale. Robert's MolecularNotes is the direct structural inspiration, folder naming, and scripts approach implemented here. I have simply added a layer of Claude Code functionality, and some small structural additions to suit my own work-style. This system also heavily references Niklas Luhmann's Zettelkasten methodology ([zettelkasten.de](https://zettelkasten.de/introduction/)) as the underlying intellectual framework.

## Pipeline

```
sources  →  atoms  →  molecules  →  compounds
```

- **sources/** — one note per reference (book, paper, podcast, article)
- **book-notes/** — chapter-level extractions from books, derived from a source note
- **atoms/** — single atomic claims, each derived from a source
- **molecules/** — personal insights synthesising two or more atoms, written in your own words
- **compounds/** — re-synthesis outputs: essays, theses, blog posts, investment theses
- **authors/** — author nodes, created when an author links to two or more sources
- **MOCs/** — semi-structured navigation indexes on a topic

## Example notes

`sources/` and `atoms/` contain a small set of real notes from my own vault (cancer biology and molecular disease) included to demonstrate the pipeline and schema in practice. The `derived-from` links in the example atoms point to the example source notes — this is intentional and illustrative of how provenance works in the system, not schema drift.

**Before using this as a base for your own vault: delete the example notes in `sources/` and `atoms/` and replace them with your own.**

## Skills

Run skills in Claude Code from the vault root (`cd second-brain && claude`).

| Skill | What it does |
|---|---|
| `/capture` | Ingest a source into a source-note. Mines up to 5 atom candidates. |
| `/atom` | Write one atom with a claim-shaped title. Never creates automatically. |
| `/molecule` | Surface molecule candidates from existing atoms. You write; Claude proposes. |
| `/find-connections` | Find analogous mechanisms and cross-domain correspondences across the vault. Proposes body wikilinks with explanation. Writes on approval only. |
| `/find-contradictions` | Surface claims that conflict with a target note. Proposes `contradicts [[wikilink]]` annotations. Writes on approval only. |
| `/moc` | Create or update a Map of Content for a topic. |
| `/maintain` | Vault-wide health pass: frontmatter audit, orphan detection, relink opportunities, tag drift, bottlenecks. Nothing written without approval. |

## External skills

Three skills used by this system are installed globally in Claude Code, not bundled here:

| Skill | Role |
|---|---|
| `/stop-slop` | Mechanical quality checks before any prose is written to disk. |
| `/writing-voice` | Voice calibration for prose output. Calls `/stop-slop` internally. |
| `/book-notes` | Chapter-level book extraction. Output lands in `book-notes/`. |

Without these, skills will flag the missing dependency and ask whether to proceed. The vault functions without them; prose quality checking is disabled.

## Obsidian setup

1. Open `second-brain/` as your vault in Obsidian.

2. Go to **Settings > Files and links > Excluded files** and add:
   - `_templates/`
   - `_system/`
   - `.claude/`

3. Go to **Settings > Core plugins** and enable:
   - **Backlinks** — shows what links to the current note (right sidebar)
   - **Quick switcher** — press `Cmd O` to jump to any note by name
   - **Page preview** — hover over any `[[wikilink]]` to preview the linked note
   - **Templates** — insert note templates from `_templates/`

   Graph view, Outgoing links, and Tags are built into newer versions of Obsidian and do not need to be enabled separately.

4. Configure **Templates**: go to **Settings > Templates**, set Template folder location to `_templates`. Then go to **Settings > Hotkeys**, search "Insert template", and assign `Cmd T`. To use: open any note, press `Cmd T`, select a template type, and fill in the placeholders — deleting all `[bracket]` text.

5. Configure **Graph view groups**: open Graph view from the left sidebar, click the settings icon, go to **Groups**, and add one group per folder:
   - `path:atoms/`
   - `path:sources/`
   - `path:molecules/`
   - `path:compounds/`
   - `path:MOCs/`

6. Optionally change the colour theme: **Settings > Appearance > Themes**.

## Claude Code

Open the vault in Claude Code:

```
cd ~/Desktop/second-brain && claude
```

`CLAUDE.md` loads automatically. Skills live in `_system/` and are invoked by name. No additional registration needed.

## Scripts

**`embed.py` — semantic search**

Embeds vault notes using OpenAI's text-embedding-3-small. Caches to `_system/embeddings.json`. Powers semantic candidate search in `/find-connections`. Estimates API cost and asks for confirmation before calling the API.

```bash
pip install openai numpy
export OPENAI_API_KEY=your-key

python3 _system/embed.py --build              # first run
python3 _system/embed.py --update             # after adding new notes
python3 _system/embed.py --search atoms/note.md   # find unlinked similar notes
python3 _system/embed.py --query "concept"    # free text search
```

`embeddings.json` is gitignored. Rebuild after cloning with `--build`.

**`organise.py` — file misplaced notes**

Moves `.md` files in the vault root to their correct folder based on `type:` frontmatter.

```bash
python3 _system/organise.py --dry-run   # preview
python3 _system/organise.py             # execute
```

Optional shell aliases:

```bash
# add to ~/.zshrc or ~/.bashrc
alias sb-embed="python3 ~/Desktop/second-brain/_system/embed.py"
alias sb-org="python3 ~/Desktop/second-brain/_system/organise.py"
```

## Roadmap / Open Questions

This system is still evolving. A few design questions I am interested in exploring:

### 1. Linear event tracking inside an interlinked second brain

Can a second brain support both linear chronology and nonlinear conceptual synthesis?

Most knowledge systems are either timeline-based, like journals and logs, or graph-based, like Zettelkasten and Obsidian vaults. I am interested in whether ongoing events, decisions, experiments, and project histories can be tracked linearly while still feeding into atoms, molecules, and higher-order synthesis.

### 2. Emergent intelligence through Claude and skills

Can AI-assisted skills help the system become more intelligent over time?

So far, this system includes skills for surfacing supportive and contrasting claims. But there are many possible ways to build connective tissue between disparate ideas: contradiction detection, analogy finding, source clustering, claim lineage, open-question tracking, and synthesis prompts.

The goal is not for Claude to own the knowledge base, but to act as an advisor on the graph: surfacing possible connections, tensions, and missing structure.

### 3. Projects and knowledge fragments

Should projects live inside the knowledge base or adjacent to it?

Currently, projects live adjacent to the knowledge base. This keeps the second brain focused on durable knowledge rather than execution clutter. But a more advanced version could treat project work as a source of reusable knowledge fragments, where project decisions, experiments, failures, and insights can eventually be promoted into atoms, molecules, or compounds.

### 4. Status promotion ritual

How should notes mature from seedling to evergreen?

A future version may introduce a more explicit promotion ritual, where notes move through stages such as:

- `seedling`
- `active`
- `evergreen`
- `archived`

This would make the system less static and more developmental: notes would not just accumulate, they would evolve.
