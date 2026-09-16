"""Convert a scrollmapper bible_databases JSON file into this repository's shape.

scrollmapper publishes {"translation": ..., "books": [{"name", "chapters": [
{"chapter", "verses": [{"verse", "text"}]}]}]}. This flattens it to
{book: {chapter: {verse: text}}} and normalises book names to the ones this
repository uses.

    python3 tools/import_scrollmapper.py Rotherham.json "ROTHERHAM EMPHASISED BIBLE"
"""

from __future__ import annotations

import argparse
import json
import os

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# scrollmapper uses a few spellings this repository does not.
ROMAN = {"I": "1", "II": "2", "III": "3", "IV": "4"}

RENAME = {
    "Song of Songs": "Song of Solomon",
    "Canticles": "Song of Solomon",
    "Psalm": "Psalms",
    "Revelation of John": "Revelation",
    "The Revelation": "Revelation",
    "Acts of the Apostles": "Acts",
}


def normalise(name: str) -> str:
    """'I Chronicles' -> '1 Chronicles'; then any explicit rename."""
    head, _, tail = name.partition(" ")
    if head in ROMAN and tail:
        name = f"{ROMAN[head]} {tail}"
    return RENAME.get(name, name)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("name")
    ap.add_argument("--locale", default="en")
    ap.add_argument("--apocrypha", action="store_true",
                    help="also write non-canonical books to apocrypha-versions/")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    raw = json.load(open(args.source, encoding="utf-8"))
    canonical = list(json.load(
        open(os.path.join(REPO, "versions", "en", "KING JAMES BIBLE.json"), encoding="utf-8")).keys())

    out: dict = {}
    apocrypha: dict = {}
    unknown = []
    for book in raw["books"]:
        name = normalise(book["name"])
        chapters: dict = {}
        for chapter in book["chapters"]:
            verses = {
                str(v["verse"]): " ".join(v["text"].split())
                for v in chapter["verses"] if v.get("text", "").strip()
            }
            if verses:
                chapters[str(chapter["chapter"])] = verses
        if not chapters:
            continue
        if name in canonical:
            out[name] = chapters
        else:
            apocrypha[name] = chapters
            unknown.append(name)

    ordered = {b: out[b] for b in canonical if b in out}
    verses = sum(len(c) for b in ordered.values() for c in b.values())
    print(f"{args.name}: {len(ordered)} books, {verses} verses"
          + (f"  + {len(apocrypha)} deuterocanonical: {', '.join(sorted(set(unknown)))}" if unknown else ""))
    if args.dry_run:
        return 0
    path = os.path.join(REPO, "versions", args.locale, f"{args.name}.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(ordered, fh, ensure_ascii=False, indent=1)
    print(f"  wrote {os.path.relpath(path, REPO)} ({os.path.getsize(path)/1e6:.1f} MB)")
    if apocrypha and args.apocrypha:
        apath = os.path.join(REPO, "apocrypha-versions", f"{args.name}.json")
        os.makedirs(os.path.dirname(apath), exist_ok=True)
        with open(apath, "w", encoding="utf-8") as fh:
            json.dump(apocrypha, fh, ensure_ascii=False, indent=1)
        print(f"  wrote {os.path.relpath(apath, REPO)} ({len(apocrypha)} books)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
