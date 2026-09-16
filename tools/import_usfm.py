"""Convert a USFM Bible into this repository's versions/<locale>/<NAME>.json shape.

Used to add the historical English versions the corpus was missing. USFM is the
format ebible.org and most translation projects publish in; this reduces it to
the {book: {chapter: {verse: text}}} structure the rest of the repository uses.

    python3 tools/import_usfm.py SRCDIR "GENEVA BIBLE" --locale en

Markers are handled as follows: \\c and \\v drive the structure; character-level
markup (\\add, \\wj, \\nd ...) is unwrapped and its text kept; notes (\\f, \\x)
are dropped, since the version files in this repository carry no apparatus.
"""

from __future__ import annotations

import argparse
import json
import os
import re

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

USFM2NAME = {
    "GEN": "Genesis", "EXO": "Exodus", "LEV": "Leviticus", "NUM": "Numbers",
    "DEU": "Deuteronomy", "JOS": "Joshua", "JDG": "Judges", "RUT": "Ruth",
    "1SA": "1 Samuel", "2SA": "2 Samuel", "1KI": "1 Kings", "2KI": "2 Kings",
    "1CH": "1 Chronicles", "2CH": "2 Chronicles", "EZR": "Ezra", "NEH": "Nehemiah",
    "EST": "Esther", "JOB": "Job", "PSA": "Psalms", "PRO": "Proverbs",
    "ECC": "Ecclesiastes", "SNG": "Song of Solomon", "ISA": "Isaiah",
    "JER": "Jeremiah", "LAM": "Lamentations", "EZK": "Ezekiel", "DAN": "Daniel",
    "HOS": "Hosea", "JOL": "Joel", "AMO": "Amos", "OBA": "Obadiah", "JON": "Jonah",
    "MIC": "Micah", "NAM": "Nahum", "HAB": "Habakkuk", "ZEP": "Zephaniah",
    "HAG": "Haggai", "ZEC": "Zechariah", "MAL": "Malachi",
    "MAT": "Matthew", "MRK": "Mark", "LUK": "Luke", "JHN": "John", "ACT": "Acts",
    "ROM": "Romans", "1CO": "1 Corinthians", "2CO": "2 Corinthians",
    "GAL": "Galatians", "EPH": "Ephesians", "PHP": "Philippians",
    "COL": "Colossians", "1TH": "1 Thessalonians", "2TH": "2 Thessalonians",
    "1TI": "1 Timothy", "2TI": "2 Timothy", "TIT": "Titus", "PHM": "Philemon",
    "HEB": "Hebrews", "JAS": "James", "1PE": "1 Peter", "2PE": "2 Peter",
    "1JN": "1 John", "2JN": "2 John", "3JN": "3 John", "JUD": "Jude",
    "REV": "Revelation",
}
CANONICAL = list(USFM2NAME.values())

NOTE_RE = re.compile(r"\\(f|x|fe)\b.*?\\\1\*", re.S)
CHAR_CLOSE_RE = re.compile(r"\\\+?(\w+)\*")
CHAR_OPEN_RE = re.compile(r"\\\+?(add|wj|nd|bk|it|bd|em|sc|qt|tl|pn|sig|ord|no|w|rq|va|vp)\s")
PARA_RE = re.compile(r"\\\w+\d?\s?")
ID_RE = re.compile(r"\\id\s+(\w+)")
C_RE = re.compile(r"\\c\s+(\d+)")
V_RE = re.compile(r"\\v\s+(\d+[a-z]?(?:-\d+[a-z]?)?)\s?")


def clean(text: str) -> str:
    text = NOTE_RE.sub(" ", text)
    text = CHAR_CLOSE_RE.sub("", text)
    text = CHAR_OPEN_RE.sub("", text)
    text = PARA_RE.sub(" ", text)
    text = text.replace("\u00a0", " ")
    return re.sub(r"\s+", " ", text).strip()


def parse_book(raw: str) -> tuple[str | None, dict]:
    m = ID_RE.search(raw)
    code = m.group(1).upper() if m else None
    book = USFM2NAME.get(code)
    if book is None:
        return None, {}
    raw = NOTE_RE.sub(" ", raw)
    chapters: dict = {}
    chapter = None
    # Split on chapter markers, then on verse markers inside each chapter.
    for chunk in re.split(r"(?=\\c\s+\d+)", raw):
        cm = C_RE.match(chunk.strip())
        if not cm:
            continue
        chapter = cm.group(1)
        verses: dict = {}
        pieces = re.split(r"(?=\\v\s+\d)", chunk)
        for piece in pieces[1:]:
            vm = V_RE.match(piece)
            if not vm:
                continue
            body = clean(piece[vm.end():])
            if not body:
                continue
            label = vm.group(1)
            # A \v 1-2 range is stored under its first number.
            number = label.split("-")[0].rstrip("abcdefg") or label
            verses[number] = (verses.get(number, "") + " " + body).strip()
        if verses:
            chapters[chapter] = verses
    return book, chapters


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", help="directory of .usfm files")
    ap.add_argument("name", help="version name, e.g. \"GENEVA BIBLE\"")
    ap.add_argument("--locale", default="en")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    books: dict = {}
    for fn in sorted(os.listdir(args.source)):
        if not fn.lower().endswith((".usfm", ".sfm")):
            continue
        raw = open(os.path.join(args.source, fn), encoding="utf-8-sig").read()
        book, chapters = parse_book(raw)
        if book and chapters:
            books[book] = chapters

    ordered = {b: books[b] for b in CANONICAL if b in books}
    verses = sum(len(c) for b in ordered.values() for c in b.values())
    print(f"{args.name}: {len(ordered)} books, {verses} verses")
    if not ordered:
        print("nothing parsed", flush=True)
        return 1
    if args.dry_run:
        first = next(iter(ordered))
        ch = next(iter(ordered[first]))
        v = next(iter(ordered[first][ch]))
        print(f"  sample {first} {ch}:{v} -> {ordered[first][ch][v][:120]}")
        return 0

    out_dir = os.path.join(REPO, "versions", args.locale)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{args.name}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(ordered, fh, ensure_ascii=False, indent=1)
    print(f"  wrote {os.path.relpath(path, REPO)} ({os.path.getsize(path)/1e6:.1f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
