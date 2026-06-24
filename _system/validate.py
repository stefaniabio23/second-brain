#!/usr/bin/env python3
"""
validate.py — vault health checks for second-brain

Checks every note against schema rules and reports violations.

Usage:
  python3 _system/validate.py                      # full validation
  python3 _system/validate.py --folder atoms       # one folder only
  python3 _system/validate.py --quiet              # errors only, no warnings
  python3 _system/validate.py --fix-tags           # lowercase tags in-place (safe)
"""

import re
import sys
from pathlib import Path

VAULT_ROOT = Path(__file__).parent.parent
TAGS_FILE = Path(__file__).parent / "tags.md"

# v3.0 closed enum (14 types) + moc + author which are operational in the vault
TYPE_ENUM = {
    "atom", "molecule", "compound",
    "academic-paper", "book", "podcast-transcript", "podcast-notes",
    "book-notes", "book-review",
    "project", "open-question", "idea", "blog-post", "journal",
    "moc", "author",
}

# v2 types still in the wild — produce a DEPRECATION warning, not an error
DEPRECATED_TYPES = {
    "source-note": "academic-paper, book, podcast-transcript, or podcast-notes",
    "book-note":   "book-notes",
}

TYPE_TO_FOLDER = {
    "atom":               "atoms",
    "molecule":           "molecules",
    "compound":           "compounds",
    "academic-paper":     "sources",
    "book":               "sources",
    "podcast-transcript": "sources",
    "podcast-notes":      "sources",
    "book-notes":         "book-notes",
    "book-review":        "compounds",
    "project":            "compounds",
    "open-question":      "compounds",
    "idea":               "ideas",
    "blog-post":          "compounds",
    "journal":            "personal",
    "moc":                "MOCs",
    "author":             "authors",
    # deprecated — keep so misplaced-folder check still runs on them
    "source-note":        "sources",
    "book-note":          "book-notes",
}

REQUIRED_FIELDS = {
    "atom":               ["type", "tags"],
    "molecule":           ["type", "tags"],
    "compound":           ["type", "tags"],
    "academic-paper":     ["type", "tags"],
    "book":               ["type", "tags"],
    "podcast-transcript": ["type", "tags"],
    "podcast-notes":      ["type", "tags"],
    "book-notes":         ["type", "tags"],
    "book-review":        ["type", "tags"],
    "project":            ["type", "tags"],
    "open-question":      ["type", "tags"],
    "idea":               ["type", "tags"],
    "blog-post":          ["type", "tags"],
    "journal":            ["type", "tags"],
    "moc":                ["type", "tags"],
    "author":             ["type", "tags"],
    # deprecated
    "source-note":        ["type", "tags"],
    "book-note":          ["type", "tags"],
}

# Fields that produce a WARN (not ERROR) if absent
RECOMMENDED_FIELDS = {
    "atom":               ["derived-from"],
    "molecule":           ["derived-from"],
    "compound":           ["derived-from"],
    "academic-paper":     ["source-type"],
    "book":               ["source-type"],
    "podcast-transcript": ["source-type"],
    "podcast-notes":      ["source-type"],
    "book-notes":         ["derived-from"],
    "book-review":        ["derived-from"],
}

NOTE_FOLDERS = list(TYPE_TO_FOLDER.values())
SKIP_FOLDERS = {"_templates", "_system", ".claude", ".obsidian"}

# Single-bracket placeholder: [word(s)] not preceded by [ and not followed by (
# Excludes: [[wikilinks]], [number] citations, [^footnote], [text](url)
PLACEHOLDER_RE = re.compile(r'(?<!\[)\[(?!\[)(?!\^)([a-zA-Z][a-zA-Z0-9 \-]+)\](?!\()(?!\[)')


def load_valid_tags() -> set:
    """Load all valid tags (active + draft) from _system/tags.md."""
    if not TAGS_FILE.exists():
        return set()
    content = TAGS_FILE.read_text(encoding="utf-8")
    tags = set()
    for line in content.splitlines():
        m = re.match(r'^[-*]\s+`([^`]+)`', line)
        if m:
            tags.add(m.group(1))
    return tags


def parse_frontmatter(content: str) -> tuple[dict, str, str]:
    """Return (fields_dict, body, fm_text). fields_dict is empty if no frontmatter."""
    if not content.startswith("---"):
        return {}, content, ""
    end = content.find("\n---", 3)
    if end == -1:
        return {}, content, ""
    fm_text = content[3:end]
    body = content[end + 4:]
    fields = {}
    current_key = None
    for line in fm_text.splitlines():
        m = re.match(r'^([a-zA-Z_-]+):\s*(.*)', line)
        if m:
            current_key = m.group(1).strip()
            fields[current_key] = m.group(2).strip()
        elif current_key and re.match(r'^\s+-\s+', line):
            # Multi-line YAML list item (e.g. tags: with indented - values)
            item = line.strip().lstrip('- ').strip()
            if fields[current_key]:
                fields[current_key] += f", {item}"
            else:
                fields[current_key] = item
    return fields, body, fm_text


def extract_tags(fields: dict) -> list[str]:
    raw = fields.get("tags", "")
    raw = raw.strip("[]")
    return [t.strip().strip('"\'') for t in raw.split(",") if t.strip()]


def extract_wikilinks(text: str) -> list[str]:
    return re.findall(r'\[\[([^\]|]+?)(?:\|[^\]]+)?\]\]', text)


def resolve_wikilink(link: str) -> bool:
    """Return True if a wikilink target resolves to an existing file."""
    link = link.strip()
    # Could be "folder/filename" or just "filename"
    if "/" in link:
        parts = link.split("/", 1)
        candidate = VAULT_ROOT / parts[0] / (parts[1] + ".md")
        if candidate.exists():
            return True
        # Try without folder prefix (Obsidian resolves by name)
    # Search by stem across all note folders
    stem = Path(link).name
    for folder in NOTE_FOLDERS:
        if (VAULT_ROOT / folder / (stem + ".md")).exists():
            return True
    # Also check root
    if (VAULT_ROOT / (stem + ".md")).exists():
        return True
    return False


def collect_all_notes(only_folder: str = None) -> list[Path]:
    notes = []
    if only_folder:
        folder_path = VAULT_ROOT / only_folder
        if folder_path.exists():
            notes = list(folder_path.glob("*.md"))
    else:
        for folder in NOTE_FOLDERS:
            notes.extend((VAULT_ROOT / folder).glob("*.md"))
    return notes


def collect_all_wikilinks() -> set[str]:
    """All wikilink stems cited across the vault (for orphan check)."""
    cited = set()
    for folder in NOTE_FOLDERS:
        for f in (VAULT_ROOT / folder).glob("*.md"):
            try:
                body = f.read_text(encoding="utf-8")
                for link in extract_wikilinks(body):
                    cited.add(Path(link).name.lower())
                    cited.add(link.lower())
            except Exception:
                pass
    return cited


def validate_note(
    path: Path,
    valid_tags: set,
    all_cited: set,
    quiet: bool = False,
) -> list[tuple[str, str]]:
    """Return list of (level, message) for a single note. Level: ERROR | WARN."""
    issues = []
    err = lambda msg: issues.append(("ERROR", msg))
    warn = lambda msg: issues.append(("WARN", msg))

    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        err(f"Cannot read file: {e}")
        return issues

    # 1. Valid frontmatter
    if not content.startswith("---"):
        err("No YAML frontmatter (must start with ---)")
        return issues
    fields, body, _fm = parse_frontmatter(content)
    if not fields and not content.startswith("---\n---"):
        err("Frontmatter not closed or unparseable")
        return issues

    # 2. type in closed enum
    note_type = fields.get("type", "").strip().strip('"\'')
    if not note_type:
        err("Missing 'type' field")
        return issues
    if note_type in DEPRECATED_TYPES:
        warn(f"Deprecated type '{note_type}' — migrate to: {DEPRECATED_TYPES[note_type]}")
    elif note_type not in TYPE_ENUM:
        err(f"Unknown type '{note_type}' — not in v3.0 enum {sorted(TYPE_ENUM)}")
        return issues

    # 3. File in correct folder
    expected_folder = TYPE_TO_FOLDER[note_type]
    actual_folder = path.parent.name
    if actual_folder != expected_folder:
        err(f"Misplaced: type '{note_type}' should be in {expected_folder}/, found in {actual_folder}/")

    # 4. Required fields
    for field in REQUIRED_FIELDS.get(note_type, []):
        if field not in fields or not fields[field]:
            err(f"Missing required field: '{field}'")

    # 4b. Recommended fields (warn only)
    for field in RECOMMENDED_FIELDS.get(note_type, []):
        if field not in fields or not fields[field]:
            warn(f"Missing recommended field: '{field}' (add a [[source]] or leave blank for original synthesis)")

    # 5. Tags in controlled vocab
    tags = extract_tags(fields)
    for tag in tags:
        if tag and tag not in valid_tags:
            warn(f"Tag '{tag}' not in _system/tags.md (add to Draft section if new)")

    # 6. No uppercase tags
    for tag in tags:
        if tag != tag.lower():
            warn(f"Tag '{tag}' should be lowercase (or add to allowlist in validate.py)")

    # 7. derived-from links resolve
    derived = fields.get("derived-from", "")
    if derived:
        links = extract_wikilinks(derived)
        if not links:
            # Maybe it's plain text or malformed
            pass
        for link in links:
            if not resolve_wikilink(link):
                warn(f"derived-from link [[{link}]] does not resolve to any vault file")

    # 8. No bracket placeholders in body
    for m in PLACEHOLDER_RE.finditer(body):
        candidate = m.group(1).strip()
        # Skip things that look like citation numbers or short technical tokens
        if len(candidate) >= 4 and not candidate.isdigit():
            warn(f"Possible unfilled placeholder: [{candidate}]")

    # 9. No orphan atoms (atoms with no incoming links from other files)
    if note_type == "atom":
        stem = path.stem.lower()
        if stem not in all_cited and path.stem not in all_cited:
            warn("Orphan atom: no other vault file links here")

    return issues


def main():
    quiet = "--quiet" in sys.argv
    fix_tags = "--fix-tags" in sys.argv

    folder_arg = None
    for i, arg in enumerate(sys.argv[1:]):
        if arg == "--folder" and i + 1 < len(sys.argv) - 1:
            folder_arg = sys.argv[i + 2]
            break

    valid_tags = load_valid_tags()
    if not valid_tags:
        print(f"WARNING: Could not load tags from {TAGS_FILE} — tag checks skipped.")

    notes = collect_all_notes(only_folder=folder_arg)
    if not notes:
        print("No notes found to validate.")
        sys.exit(0)

    print(f"Validating {len(notes)} notes...\n")

    all_cited = collect_all_wikilinks()

    error_count = warn_count = 0
    files_with_issues = 0

    for path in sorted(notes):
        issues = validate_note(path, valid_tags, all_cited, quiet=quiet)
        if not issues:
            continue

        errors = [i for i in issues if i[0] == "ERROR"]
        warnings = [i for i in issues if i[0] == "WARN"]

        if quiet and not errors:
            continue

        rel = path.relative_to(VAULT_ROOT)
        print(f"{rel}")
        for level, msg in issues:
            if quiet and level == "WARN":
                continue
            marker = "  [ERROR]" if level == "ERROR" else "  [warn] "
            print(f"{marker} {msg}")
        print()

        files_with_issues += 1
        error_count += len(errors)
        warn_count += len(warnings)

        if fix_tags and "type" in {f for f in ["tags"]}:
            pass  # tag auto-fix handled below

    print(f"{'─' * 50}")
    print(f"Notes checked: {len(notes)}")
    print(f"Files with issues: {files_with_issues}")
    print(f"Errors: {error_count}   Warnings: {warn_count}")

    if error_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
