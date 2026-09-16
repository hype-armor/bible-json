"""Cross-version verse access for the bible-json dataset.

The repository stores each version as `versions/<locale>/<VERSION NAME>.json`
with the shape `{book: {chapter: {verse: text}}}`. Book keys are *not* uniform:
English-language and Hebrew files use English book names, while the Vulgate uses
Latin ones ("Isaias") and several Greek files use Greek ones ("ΚΑΤΑ ΜΑΤΘΑΙΟΝ").
`book_name_mapping.json` maps English -> local names for most of those versions.

This module normalises all of that behind `Bible.verse(version, ref)` so a study
can quote the same reference from the Hebrew, the Septuagint, the Vulgate and
forty English versions without caring how any one file spells "Isaiah".
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from functools import lru_cache

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
VERSIONS_DIR = os.path.join(REPO_ROOT, "versions")
APOCRYPHA_DIR = os.path.join(REPO_ROOT, "apocrypha-versions")
MAPPING_PATH = os.path.join(REPO_ROOT, "book_name_mapping.json")

# `book_name_mapping.json` still carries a few keys under names the version files
# no longer use. Map the stale key onto the file that superseded it.
MAPPING_ALIASES = {
    "RP BYZANTINE MAJORITY TEXT 2005": "BYZANTINE/MAJORITY TEXT (2000) - TRANSLITERATED",
    "WESTCOTT AND HORT 1881 - TRANSLITERATED": "WESTCOTT/HORT - TRANSLITERATED",
}


class VerseNotFound(KeyError):
    """A reference does not exist in the requested version."""


@dataclass(frozen=True)
class Ref:
    book: str
    chapter: int
    verse: int
    end_verse: int | None = None

    @classmethod
    def parse(cls, text: str) -> "Ref":
        """Parse 'Isaiah 7:14' or '1 John 5:7-8'."""
        m = re.fullmatch(r"\s*(.+?)\s+(\d+):(\d+)(?:-(\d+))?\s*", text)
        if not m:
            raise ValueError(f"unparseable reference: {text!r}")
        book, ch, v, end = m.groups()
        return cls(book, int(ch), int(v), int(end) if end else None)

    @property
    def verses(self) -> list[int]:
        return list(range(self.verse, (self.end_verse or self.verse) + 1))

    def __str__(self) -> str:
        tail = f"-{self.end_verse}" if self.end_verse else ""
        return f"{self.book} {self.chapter}:{self.verse}{tail}"


@dataclass(frozen=True)
class Version:
    key: str      # "en/KING JAMES BIBLE"
    locale: str
    name: str
    path: str

    @property
    def corpus(self) -> str:
        return "apocrypha" if self.path.startswith(APOCRYPHA_DIR) else "canonical"


class Bible:
    def __init__(self) -> None:
        self._mapping = json.load(open(MAPPING_PATH, encoding="utf-8"))
        for file_name, mapping_key in MAPPING_ALIASES.items():
            if mapping_key in self._mapping:
                self._mapping.setdefault(file_name, self._mapping[mapping_key])
        self.versions: dict[str, Version] = {}
        for locale in sorted(os.listdir(VERSIONS_DIR)):
            locale_dir = os.path.join(VERSIONS_DIR, locale)
            if not os.path.isdir(locale_dir):
                continue
            for file_name in sorted(os.listdir(locale_dir)):
                if not file_name.endswith(".json"):
                    continue
                name = file_name[:-5]
                key = f"{locale}/{name}"
                self.versions[key] = Version(key, locale, name, os.path.join(locale_dir, file_name))
        if os.path.isdir(APOCRYPHA_DIR):
            for file_name in sorted(os.listdir(APOCRYPHA_DIR)):
                if not file_name.endswith(".json"):
                    continue
                name = file_name[:-5]
                key = f"apocrypha/{name}"
                self.versions[key] = Version(key, "apocrypha", name, os.path.join(APOCRYPHA_DIR, file_name))

    # -- loading ---------------------------------------------------------

    @lru_cache(maxsize=None)
    def _load(self, version_key: str) -> dict:
        try:
            version = self.versions[version_key]
        except KeyError:
            raise KeyError(f"unknown version: {version_key!r}") from None
        return json.load(open(version.path, encoding="utf-8"))

    # -- book-name resolution --------------------------------------------

    def local_book(self, version_key: str, book: str) -> str | None:
        """Translate a canonical English book name into this version's key."""
        data = self._load(version_key)
        if book in data:
            return book
        name = self.versions[version_key].name
        local = self._mapping.get(name, {}).get(book)
        if local and local in data:
            return local
        # Greek NT files title books in uppercase Greek; the mapping covers the
        # transliterated twins, so reuse a sibling version's mapping by shape.
        for mapped in self._mapping.values():
            candidate = mapped.get(book)
            if candidate and candidate in data:
                return candidate
        return None

    # -- lookup ----------------------------------------------------------

    def verse(self, version_key: str, ref: Ref | str) -> str:
        """Return the text of `ref` in `version_key`, joining a verse range."""
        if isinstance(ref, str):
            ref = Ref.parse(ref)
        data = self._load(version_key)
        book = self.local_book(version_key, ref.book)
        if book is None:
            raise VerseNotFound(f"{version_key} has no book {ref.book!r}")
        chapter = data[book].get(str(ref.chapter))
        if chapter is None:
            raise VerseNotFound(f"{version_key} has no {ref.book} {ref.chapter}")
        parts = []
        for number in ref.verses:
            text = chapter.get(str(number))
            if text is None:
                raise VerseNotFound(f"{version_key} has no {ref.book} {ref.chapter}:{number}")
            parts.append(text.strip())
        return " ".join(parts)

    def try_verse(self, version_key: str, ref: Ref | str) -> str | None:
        try:
            return self.verse(version_key, ref)
        except (VerseNotFound, KeyError):
            return None

    def has(self, version_key: str, ref: Ref | str) -> bool:
        return self.try_verse(version_key, ref) is not None

    # -- convenience -----------------------------------------------------

    def in_locale(self, locale: str) -> list[str]:
        return [k for k, v in self.versions.items() if v.locale == locale]

    def books(self, version_key: str) -> list[str]:
        return list(self._load(version_key).keys())

    def verse_count(self, version_key: str) -> int:
        data = self._load(version_key)
        return sum(len(ch) for book in data.values() for ch in book.values())
