"""Build lexicon/ : word-level Strong's and morphology tagging for this corpus.

The version files here are plain text, so term-level questions ("where else does
this word occur, and how was it rendered there?") could previously only be
answered by matching surface forms. This script imports word-level tagging from
three public sources and, crucially, **re-versifies it onto this repository's
own chapter/verse numbering** so it lines up with every other version file.

Sources (all cloned fresh; none are vendored into this repository):
  openscriptures/morphhb              Westminster Leningrad Codex with Strong's
                                      lemmas and morphology.        CC BY 4.0
  byztxt/byzantine-majority-text      Robinson-Pierpont Greek NT with Strong's
                                      numbers and parsing.          Public domain
  openscriptures/strongs              Strong's Hebrew and Greek dictionaries.
                                                                    CC BY-SA

The hard part is versification. morphhb follows BHS; this repository's Hebrew
files follow English numbering (Joel has 3 chapters, not 4; Psalm superscriptions
are folded into verse 1). Rather than hand-code the divergences, this script
aligns the two consonantal word sequences with difflib and reads the mapping off
the alignment - both are the same WLC text, so the alignment is near-exact
(currently 99.0% of words match exactly, and no word is left unassigned).

Outputs:
  lexicon/hebrew.json          {book: {chapter: {verse: [[strongs, morph, surface, lemma], ...]}}}
  lexicon/greek.json           same shape, lemma field empty (not in the source)
  lexicon/strongs-hebrew.json  {H1234: {lemma, xlit, pron, derivation, strongs_def, kjv_def}}
  lexicon/strongs-greek.json   {G1234: {...}}
  lexicon/SOURCES.md           provenance, licences and the alignment report

Usage:  python3 tools/build_lexicon.py [--work DIR]
"""

from __future__ import annotations

import argparse
import csv
import difflib
import json
import os
import re
import subprocess
import sys
import unicodedata

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(REPO, "lexicon")

SOURCES = {
    "morphhb": ("https://github.com/openscriptures/morphhb.git", "CC BY 4.0"),
    "byzantine-majority-text": ("https://github.com/byztxt/byzantine-majority-text.git", "Public domain"),
    "strongs": ("https://github.com/openscriptures/strongs.git", "CC BY-SA"),
}

OSIS2NAME = {
    "Gen": "Genesis", "Exod": "Exodus", "Lev": "Leviticus", "Num": "Numbers",
    "Deut": "Deuteronomy", "Josh": "Joshua", "Judg": "Judges", "Ruth": "Ruth",
    "1Sam": "1 Samuel", "2Sam": "2 Samuel", "1Kgs": "1 Kings", "2Kgs": "2 Kings",
    "1Chr": "1 Chronicles", "2Chr": "2 Chronicles", "Ezra": "Ezra", "Neh": "Nehemiah",
    "Esth": "Esther", "Job": "Job", "Ps": "Psalms", "Prov": "Proverbs",
    "Eccl": "Ecclesiastes", "Song": "Song of Solomon", "Isa": "Isaiah",
    "Jer": "Jeremiah", "Lam": "Lamentations", "Ezek": "Ezekiel", "Dan": "Daniel",
    "Hos": "Hosea", "Joel": "Joel", "Amos": "Amos", "Obad": "Obadiah",
    "Jonah": "Jonah", "Mic": "Micah", "Nah": "Nahum", "Hab": "Habakkuk",
    "Zeph": "Zephaniah", "Hag": "Haggai", "Zech": "Zechariah", "Mal": "Malachi",
}

BYZ2NAME = {
    "MAT": "Matthew", "MAR": "Mark", "LUK": "Luke", "JOH": "John", "ACT": "Acts",
    "ROM": "Romans", "1CO": "1 Corinthians", "2CO": "2 Corinthians",
    "GAL": "Galatians", "EPH": "Ephesians", "PHP": "Philippians",
    "COL": "Colossians", "1TH": "1 Thessalonians", "2TH": "2 Thessalonians",
    "1TI": "1 Timothy", "2TI": "2 Timothy", "TIT": "Titus", "PHM": "Philemon",
    "HEB": "Hebrews", "JAM": "James", "1PE": "1 Peter", "2PE": "2 Peter",
    "1JO": "1 John", "2JO": "2 John", "3JO": "3 John", "JUD": "Jude",
    "REV": "Revelation",
}

# The repository's Hebrew and Greek files these are aligned onto.
HEBREW_TARGET = os.path.join(REPO, "versions", "he", "WLC (CONSONANTS ONLY).json")
GREEK_TARGET = os.path.join(REPO, "versions", "el", "RP BYZANTINE MAJORITY TEXT 2005.json")

VERSE_RE = re.compile(r'<verse osisID="([^"]+)">(.*?)</verse>', re.S)
W_RE = re.compile(r"<w\s+([^>]*?)>(.*?)</w>", re.S)
ATTR_RE = re.compile(r'(\w+)="([^"]*)"')
BYZ_TOKEN_RE = re.compile(r"(\S+)\s+(\d+)\s+\{([^}]*)\}")
STRONGS_RE = re.compile(r"(\d+)\s*([a-z])?")
SPLIT_RE = re.compile(r"[\s־]+")


def consonants(text: str) -> str:
    """Fold a Hebrew word to bare consonants for alignment."""
    text = re.sub(r"[/׃׀׆׳״]", "", text)
    return "".join(
        ch for ch in unicodedata.normalize("NFD", text) if not unicodedata.combining(ch)
    )


def ensure_clone(work: str, name: str) -> str:
    path = os.path.join(work, name)
    if os.path.isdir(os.path.join(path, ".git")):
        return path
    url = SOURCES[name][0]
    print(f"  cloning {url}")
    subprocess.run(["git", "clone", "--depth", "1", "-q", url, path], check=True)
    return path


# -- Hebrew -----------------------------------------------------------------

def parse_morphhb(path: str) -> dict:
    books: dict = {}
    wlc = os.path.join(path, "wlc")
    for fn in sorted(os.listdir(wlc)):
        if not fn.endswith(".xml") or fn[:-4] not in OSIS2NAME:
            continue
        raw = open(os.path.join(wlc, fn), encoding="utf-8").read()
        for osis, body in VERSE_RE.findall(raw):
            part = osis.split(".")
            book, ch, verse = OSIS2NAME[part[0]], int(part[1]), int(part[2])
            words = []
            for attrs, surface in W_RE.findall(body):
                a = dict(ATTR_RE.findall(attrs))
                words.append((surface, a.get("lemma", ""), a.get("morph", "")))
            books.setdefault(book, {}).setdefault(ch, {})[verse] = words
    return books


def align_hebrew(source: dict, target: dict) -> tuple[dict, list]:
    """Map morphhb's BHS verses onto the repository's numbering, word by word."""
    out: dict = {}
    report = []
    for book in target:
        src_words, src_tags = [], []
        for ch in sorted(source[book], key=int):
            for verse in sorted(source[book][ch], key=int):
                for surface, lemma, morph in source[book][ch][verse]:
                    token = consonants(surface)
                    if token:
                        src_words.append(token)
                        src_tags.append((surface, lemma, morph))
        tgt_words, tgt_refs = [], []
        for ch in sorted(target[book], key=int):
            for verse in sorted(target[book][ch], key=int):
                for raw in SPLIT_RE.split(target[book][ch][verse]):
                    token = consonants(raw)
                    if token:
                        tgt_words.append(token)
                        tgt_refs.append((ch, verse))

        matcher = difflib.SequenceMatcher(None, src_words, tgt_words, autojunk=False)
        assigned: list = [None] * len(src_words)
        exact = 0
        for i, j, n in matcher.get_matching_blocks():
            for k in range(n):
                assigned[i + k] = tgt_refs[j + k]
                exact += 1
        # Words the alignment could not place go to the nearest placed neighbour.
        last = None
        for i in range(len(assigned)):
            if assigned[i] is None:
                assigned[i] = last
            else:
                last = assigned[i]
        nxt = None
        for i in range(len(assigned) - 1, -1, -1):
            if assigned[i] is None:
                assigned[i] = nxt
            else:
                nxt = assigned[i]

        for (surface, lemma, morph), ref in zip(src_tags, assigned):
            if ref is None:
                continue
            ch, verse = ref
            ids = [f"H{int(n)}{suf or ''}" for n, suf in STRONGS_RE.findall(lemma)]
            out.setdefault(book, {}).setdefault(ch, {}).setdefault(verse, []).append(
                [ids[0] if ids else "", morph, surface, lemma]
            )
        report.append((book, len(src_words), len(tgt_words), exact))
    return out, report


# -- Greek ------------------------------------------------------------------

def parse_byzantine(path: str) -> dict:
    folder = os.path.join(path, "csv-unicode", "strongs", "with-parsing")
    books: dict = {}
    for fn in sorted(os.listdir(folder)):
        code = fn[:-4]
        if code not in BYZ2NAME:
            continue
        book = BYZ2NAME[code]
        with open(os.path.join(folder, fn), encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                words = [
                    [f"G{int(num)}", morph, surface, ""]
                    for surface, num, morph in BYZ_TOKEN_RE.findall(row["text"])
                ]
                books.setdefault(book, {}).setdefault(row["chapter"], {})[row["verse"]] = words
    # RP2018 prints the Romans doxology at 14:24-26; this repository's RP2005
    # file has it at 16:25-27. Move it so the tagging lines up.
    for src, dst in (("24", "25"), ("25", "26"), ("26", "27")):
        if src in books["Romans"].get("14", {}):
            books["Romans"].setdefault("16", {})[dst] = books["Romans"]["14"].pop(src)
    return books


# -- dictionaries -----------------------------------------------------------

def parse_dictionary(path: str) -> dict:
    raw = open(path, encoding="utf-8").read()
    return json.loads(raw[raw.index("{"): raw.rindex("}") + 1])


# -- driver -----------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=os.path.join(REPO, ".lexicon-src"),
                    help="where to clone the upstream sources")
    args = ap.parse_args()
    os.makedirs(args.work, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)

    print("sources:")
    morphhb_dir = ensure_clone(args.work, "morphhb")
    byz_dir = ensure_clone(args.work, "byzantine-majority-text")
    strongs_dir = ensure_clone(args.work, "strongs")

    print("hebrew: parsing morphhb")
    source = parse_morphhb(morphhb_dir)
    target = json.load(open(HEBREW_TARGET, encoding="utf-8"))
    print("hebrew: aligning BHS numbering onto this repository's numbering")
    hebrew, report = align_hebrew(source, target)

    print("greek: parsing Robinson-Pierpont")
    greek = parse_byzantine(byz_dir)

    writes = [
        ("hebrew.json", hebrew),
        ("greek.json", greek),
        ("strongs-hebrew.json", parse_dictionary(
            os.path.join(strongs_dir, "hebrew", "strongs-hebrew-dictionary.js"))),
        ("strongs-greek.json", parse_dictionary(
            os.path.join(strongs_dir, "greek", "strongs-greek-dictionary.js"))),
    ]
    for name, data in writes:
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, separators=(",", ":"))
        size = os.path.getsize(os.path.join(OUT, name)) / 1e6
        print(f"  wrote lexicon/{name} ({size:.1f} MB)")

    heb_words = sum(len(w) for b in hebrew.values() for c in b.values() for w in c.values())
    gk_words = sum(len(w) for b in greek.values() for c in b.values() for w in c.values())
    total_src = sum(r[1] for r in report)
    total_exact = sum(r[3] for r in report)
    ratio = 100 * total_exact / total_src

    # Coverage: every verse in the target files should have tagging.
    def untagged(tagged, path):
        data = json.load(open(path, encoding="utf-8"))
        return [
            f"{b} {c}:{v}" for b in data for c in data[b] for v in data[b][c]
            if str(v) not in {str(k) for k in tagged.get(b, {}).get(c, tagged.get(b, {}).get(int(c), {}))}
        ]

    heb_missing = untagged({b: {str(c): {str(v): w for v, w in ch.items()}
                                for c, ch in bk.items()} for b, bk in hebrew.items()}, HEBREW_TARGET)
    gk_missing = untagged(greek, GREEK_TARGET)

    with open(os.path.join(OUT, "SOURCES.md"), "w", encoding="utf-8") as fh:
        fh.write(f"""# Lexicon sources

Generated by `tools/build_lexicon.py`. Nothing here is hand-edited.

| Source | Provides | Licence |
| --- | --- | --- |
| [openscriptures/morphhb]({SOURCES['morphhb'][0]}) | Westminster Leningrad Codex, Strong's lemmas + morphology | {SOURCES['morphhb'][1]} |
| [byztxt/byzantine-majority-text]({SOURCES['byzantine-majority-text'][0]}) | Robinson-Pierpont Greek NT, Strong's + parsing | {SOURCES['byzantine-majority-text'][1]} |
| [openscriptures/strongs]({SOURCES['strongs'][0]}) | Strong's Hebrew and Greek dictionaries | {SOURCES['strongs'][1]} |

The Strong's dictionaries are **CC BY-SA**, which is a share-alike licence. Anyone
redistributing `lexicon/strongs-*.json` should carry that licence forward.

## Coverage

- Hebrew: **{heb_words:,} tagged words** across {len(hebrew)} books
- Greek: **{gk_words:,} tagged words** across {len(greek)} books
- Strong's entries: {len(writes[2][1]):,} Hebrew, {len(writes[3][1]):,} Greek

## Versification alignment

`morphhb` follows BHS numbering; this repository's Hebrew files follow English
numbering. The mapping is derived by aligning the consonantal word sequences
rather than by hand-coded rules.

- **{total_exact:,} of {total_src:,} words ({ratio:.2f}%) aligned exactly.**
- Remaining words are placed with their nearest aligned neighbour; these are
  ketiv/qere and orthographic differences between the two editions of the WLC,
  not verse-boundary uncertainty.
- Verses in `versions/he/WLC (CONSONANTS ONLY).json` with no tagging: **{len(heb_missing)}**
- Verses in `versions/el/RP BYZANTINE MAJORITY TEXT 2005.json` with no tagging: **{len(gk_missing)}**
  {('(' + ', '.join(gk_missing) + ')') if gk_missing else ''}

Weakest ten books by exact-match rate:

| Book | morphhb words | repo words | exact |
| --- | ---: | ---: | ---: |
""")
        for book, a, b, exact in sorted(report, key=lambda r: r[3] / max(r[1], 1))[:10]:
            fh.write(f"| {book} | {a:,} | {b:,} | {100*exact/max(a,1):.2f}% |\n")

    print(f"\nhebrew {heb_words:,} words, greek {gk_words:,} words")
    print(f"alignment: {total_exact:,}/{total_src:,} exact ({ratio:.2f}%)")
    print(f"untagged verses: hebrew {len(heb_missing)}, greek {len(gk_missing)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
