"""Read access to lexicon/ : word-level Strong's tagging for this corpus.

    from lexicon import Lexicon
    lex = Lexicon()
    lex.words("Isaiah 7:14")              -> [Word(strongs='H5959', ...), ...]
    lex.occurrences("H5959")              -> ['Genesis 24:43', ..., 'Isaiah 7:14']
    lex.define("H5959")                   -> {'lemma': 'עַלְמָה', 'xlit': ..., ...}

Because the tagging is re-versified onto this repository's own numbering
(see tools/build_lexicon.py), references here are the same references that work
against every version file - no offset tables, no BHS/English conversion.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from functools import lru_cache

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LEXICON = os.path.join(REPO, "lexicon")
REF_RE = re.compile(r"\s*(.+?)\s+(\d+):(\d+)\s*")


@dataclass(frozen=True)
class Word:
    strongs: str      # "H5959" / "G3972"; "" where the source gives no number
    morph: str        # morphology code, e.g. "HTd/Ncfsa" or "N-NSM"
    surface: str      # the word as printed, with points/accents
    lemma: str        # morphhb's raw lemma field (Hebrew only)

    @property
    def language(self) -> str:
        return {"H": "hebrew", "G": "greek"}.get(self.strongs[:1], "unknown")


class Lexicon:
    def __init__(self) -> None:
        self._data: dict[str, dict] = {}
        self._dicts: dict[str, dict] = {}
        self._index: dict[str, list[str]] | None = None

    # -- loading ---------------------------------------------------------

    def _corpus(self, language: str) -> dict:
        if language not in self._data:
            path = os.path.join(LEXICON, f"{language}.json")
            self._data[language] = json.load(open(path, encoding="utf-8"))
        return self._data[language]

    def _dictionary(self, language: str) -> dict:
        if language not in self._dicts:
            path = os.path.join(LEXICON, f"strongs-{language}.json")
            self._dicts[language] = json.load(open(path, encoding="utf-8"))
        return self._dicts[language]

    # -- lookup ----------------------------------------------------------

    def words(self, ref: str) -> list[Word]:
        """Tagged words at a reference, in order. Empty if untagged."""
        m = REF_RE.fullmatch(ref)
        if not m:
            raise ValueError(f"unparseable reference: {ref!r}")
        book, chapter, verse = m.group(1), m.group(2), m.group(3)
        for language in ("hebrew", "greek"):
            chapters = self._corpus(language).get(book)
            if not chapters:
                continue
            row = chapters.get(chapter, {}).get(verse)
            if row:
                return [Word(*w) for w in row]
        return []

    @lru_cache(maxsize=None)
    def _build_index(self) -> dict[str, tuple[str, ...]]:
        index: dict[str, list[str]] = {}
        for language in ("hebrew", "greek"):
            for book, chapters in self._corpus(language).items():
                for chapter, verses in chapters.items():
                    for verse, words in verses.items():
                        ref = f"{book} {chapter}:{verse}"
                        for strongs, *_ in words:
                            if not strongs:
                                continue
                            bucket = index.setdefault(strongs, [])
                            if not bucket or bucket[-1] != ref:
                                bucket.append(ref)
        return {k: tuple(v) for k, v in index.items()}

    def occurrences(self, strongs: str, *, exact: bool = False) -> list[str]:
        """Every reference containing this Strong's number, in canonical order.

        Hebrew numbers carry homonym suffixes in morphhb ("H1121a"). By default a
        bare number matches all of its homonyms; pass exact=True to require the
        suffix to match too.
        """
        strongs = strongs.strip()
        index = self._build_index()
        if exact or not re.fullmatch(r"[HG]\d+", strongs):
            return list(index.get(strongs, ()))
        refs: list[str] = []
        for key, bucket in index.items():
            if key == strongs or re.fullmatch(re.escape(strongs) + r"[a-z]", key):
                refs.extend(bucket)
        order = self._book_order()
        seen, out = set(), []
        for ref in sorted(set(refs), key=lambda r: self._sort_key(r, order)):
            if ref not in seen:
                seen.add(ref)
                out.append(ref)
        return out

    @lru_cache(maxsize=None)
    def _book_order(self) -> tuple[str, ...]:
        books: list[str] = []
        for language in ("hebrew", "greek"):
            books.extend(self._corpus(language).keys())
        return tuple(books)

    @staticmethod
    def _sort_key(ref: str, order: tuple[str, ...]):
        m = REF_RE.fullmatch(ref)
        book, chapter, verse = m.group(1), int(m.group(2)), int(m.group(3))
        return (order.index(book) if book in order else 999, chapter, verse)

    def define(self, strongs: str) -> dict | None:
        language = {"H": "hebrew", "G": "greek"}.get(strongs[:1])
        if not language:
            return None
        entry = self._dictionary(language).get(strongs)
        if entry is None and re.fullmatch(r"[HG]\d+[a-z]", strongs):
            entry = self._dictionary(language).get(strongs[:-1])
        return entry

    def strongs_at(self, ref: str, surface_contains: str) -> list[Word]:
        """The tagged words at `ref` whose surface form contains a substring."""
        return [w for w in self.words(ref) if surface_contains in w.surface]
