#!/usr/bin/env python3
"""
embed.py — semantic search for second-brain

Embeds vault notes using OpenAI's text-embedding-3-small model. Caches embeddings
locally. Finds notes that are semantically similar but not yet linked — feeding
better candidates to /find-connections than tag or lineage matching alone.

Usage:
  python3 _system/embed.py --build              # embed all notes
  python3 _system/embed.py --update             # embed new/changed notes only
  python3 _system/embed.py --search atoms/note.md   # find unlinked similar notes
  python3 _system/embed.py --query "concept text"   # search by free text

Requirements:
  pip install openai numpy
  export OPENAI_API_KEY=your-key

Cache: _system/embeddings.json (gitignored — derived data, can be rebuilt)
"""

import os
import re
import json
import hashlib
import argparse
import sys
import urllib.parse
from pathlib import Path

VAULT_ROOT = Path(__file__).parent.parent
CACHE_FILE = Path(__file__).parent / "embeddings.json"
EMBEDDING_MODEL = "text-embedding-3-small"
COST_PER_1M_TOKENS = 0.02
NOTE_FOLDERS = ["atoms", "molecules", "sources", "book-notes", "compounds", "MOCs"]
TOP_K = 10
SIMILARITY_THRESHOLD = 0.72


def get_client():
    try:
        from openai import OpenAI
    except ImportError:
        print("Error: openai not installed. Run: pip install openai numpy")
        sys.exit(1)
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        print("Error: OPENAI_API_KEY not set in environment.")
        sys.exit(1)
    return OpenAI(api_key=key)


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            return text[end + 3:].strip()
    return text.strip()


def extract_wikilinks(text: str) -> list:
    return re.findall(r'\[\[([^\]]+)\]\]', text)


def file_hash(content: str) -> str:
    return hashlib.md5(content.encode()).hexdigest()


def obsidian_uri(note_path: str) -> str:
    vault_name = VAULT_ROOT.name
    file_path = note_path.replace("\\", "/")
    if file_path.endswith(".md"):
        file_path = file_path[:-3]
    return f"obsidian://open?vault={urllib.parse.quote(vault_name)}&file={urllib.parse.quote(file_path)}"


def collect_notes() -> dict:
    notes = {}
    for folder in NOTE_FOLDERS:
        path = VAULT_ROOT / folder
        if not path.exists():
            continue
        for f in path.glob("*.md"):
            rel = str(f.relative_to(VAULT_ROOT))
            notes[rel] = f.read_text(encoding="utf-8")
    return notes


def load_cache() -> dict:
    if CACHE_FILE.exists():
        with open(CACHE_FILE) as f:
            return json.load(f)
    return {}


def save_cache(cache: dict):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)
    print(f"Cache saved: {CACHE_FILE}")


def embed(client, text: str) -> list:
    text = text[:8000]  # stay within token limit
    r = client.embeddings.create(input=text, model=EMBEDDING_MODEL)
    return r.data[0].embedding


def cosine(a: list, b: list) -> float:
    try:
        import numpy as np
    except ImportError:
        print("Error: numpy not installed. Run: pip install numpy")
        sys.exit(1)
    a, b = map(np.array, (a, b))
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def already_linked(target_links: list, candidate_path: str) -> bool:
    stem = Path(candidate_path).stem.lower()
    return any(stem in link.lower() for link in target_links)


# Commands

def build(update_only: bool = False):
    notes = collect_notes()
    cache = load_cache()

    to_embed = [
        (path, content)
        for path, content in notes.items()
        if not update_only
        or path not in cache
        or cache[path]["hash"] != file_hash(content)
    ]

    if not to_embed:
        print("Nothing new to embed.")
        return

    approx_tokens = sum(len(strip_frontmatter(c)) for _, c in to_embed) / 4
    approx_cost = (approx_tokens / 1_000_000) * COST_PER_1M_TOKENS
    print(f"Notes to embed: {len(to_embed)}")
    print(f"Estimated cost: ${approx_cost:.4f} ({approx_tokens:,.0f} tokens at ${COST_PER_1M_TOKENS}/1M)")
    confirm = input("Proceed? (y/n): ").strip().lower()
    if confirm != "y":
        print("Aborted.")
        return

    client = get_client()
    print(f"Embedding with {EMBEDDING_MODEL}...")
    for i, (path, content) in enumerate(to_embed, 1):
        body = strip_frontmatter(content)
        if not body.strip():
            continue
        vec = embed(client, body)
        cache[path] = {
            "hash": file_hash(content),
            "embedding": vec,
            "wikilinks": extract_wikilinks(content),
        }
        print(f"  [{i}/{len(to_embed)}] {path}")

    save_cache(cache)


def search(target_path: str):
    """Find semantically similar notes not yet linked from target_path."""
    cache = load_cache()

    if target_path not in cache:
        print(f"Not in cache: {target_path}")
        print("Run --update first.")
        return

    target = cache[target_path]
    target_vec = target["embedding"]
    target_links = target["wikilinks"]

    scores = []
    for path, data in cache.items():
        if path == target_path:
            continue
        if already_linked(target_links, path):
            continue
        sim = cosine(target_vec, data["embedding"])
        if sim >= SIMILARITY_THRESHOLD:
            scores.append((sim, path))

    scores.sort(reverse=True)

    print(f"\nSemantically similar, not yet linked to: {target_path}")
    print("Pass these to /find-connections\n")
    if not scores:
        print("  No candidates above threshold.")
        return
    for sim, path in scores[:TOP_K]:
        uri = obsidian_uri(path)
        print(f"  {sim:.3f}  {path}")
        print(f"         {uri}")


def query(text: str):
    """Search the vault by free text."""
    client = get_client()
    cache = load_cache()

    if not cache:
        print("Cache empty. Run --build first.")
        return

    vec = embed(client, text)
    scores = sorted(
        ((cosine(vec, d["embedding"]), p) for p, d in cache.items()),
        reverse=True
    )

    print(f"\nResults for: '{text}'\n")
    for sim, path in scores[:TOP_K]:
        uri = obsidian_uri(path)
        print(f"  {sim:.3f}  {path}")
        print(f"         {uri}")


def main():
    parser = argparse.ArgumentParser(description="Semantic search for second-brain")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--build", action="store_true",
                       help="Embed all notes from scratch")
    group.add_argument("--update", action="store_true",
                       help="Embed new or changed notes only")
    group.add_argument("--search", metavar="NOTE_PATH",
                       help="Find unlinked similar notes for a given note")
    group.add_argument("--query", metavar="TEXT",
                       help="Search by free text query")
    args = parser.parse_args()

    if args.build:
        build(update_only=False)
    elif args.update:
        build(update_only=True)
    elif args.search:
        search(args.search)
    elif args.query:
        query(args.query)


if __name__ == "__main__":
    main()
