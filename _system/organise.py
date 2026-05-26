#!/usr/bin/env python3
"""
organise.py — move misplaced notes to their correct folder by type: frontmatter

Useful when notes are created in the vault root during quick capture and need
filing. /capture and /atom file directly, so this is a fallback for manual
notes or bulk imports.

Usage:
  python3 _system/organise.py             # move notes to correct folders
  python3 _system/organise.py --dry-run   # preview moves without touching files
"""

import re
import sys
import shutil
from pathlib import Path

VAULT_ROOT = Path(__file__).parent.parent

TYPE_TO_FOLDER = {
    "source-note": "sources",
    "book-note": "book-notes",
    "atom": "atoms",
    "molecule": "molecules",
    "compound": "compounds",
    "moc": "MOCs",
    "author": "authors",
}

SKIP_FILES = {"CLAUDE.md"}
SKIP_FOLDERS = {"_templates", "_system", ".claude", ".obsidian",
                "sources", "book-notes", "atoms", "molecules",
                "compounds", "MOCs", "authors"}


def get_type(content: str) -> str | None:
    match = re.search(r'^type:\s*(\S+)', content, re.MULTILINE)
    return match.group(1).strip().strip('"').strip("'") if match else None


def main():
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        print("DRY RUN — no files will be moved.\n")

    moved = skipped = errors = 0

    for md_file in VAULT_ROOT.glob("*.md"):
        if md_file.name in SKIP_FILES:
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception as e:
            print(f"  ERROR reading {md_file.name}: {e}")
            errors += 1
            continue

        note_type = get_type(content)

        if not note_type:
            print(f"  SKIP (no type field): {md_file.name}")
            skipped += 1
            continue

        if note_type not in TYPE_TO_FOLDER:
            print(f"  SKIP (unknown type '{note_type}'): {md_file.name}")
            skipped += 1
            continue

        target_folder = VAULT_ROOT / TYPE_TO_FOLDER[note_type]
        target_path = target_folder / md_file.name

        if target_path.exists():
            print(f"  SKIP (already exists in target): {md_file.name}")
            skipped += 1
            continue

        print(f"  MOVE  {md_file.name}  ->  {TYPE_TO_FOLDER[note_type]}/")
        if not dry_run:
            target_folder.mkdir(exist_ok=True)
            shutil.move(str(md_file), str(target_path))
        moved += 1

    action = "Would move" if dry_run else "Moved"
    print(f"\n{action} {moved} note(s). Skipped {skipped}. Errors {errors}.")


if __name__ == "__main__":
    main()
