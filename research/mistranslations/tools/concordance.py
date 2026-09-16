"""Word-occurrence search across the corpus, without lemma tagging.

This repository ships no Strong's numbers or morphology (see COVERAGE.md), so
term-level questions - "where else does this word appear, and how was it
rendered there?" - have to be answered by matching surface forms. That is
workable because the corpus includes the unpointed Westminster Leningrad Codex
and because Greek diacritics can be stripped mechanically.

Two operations cover most of the work a mistranslation study needs:

    find(...)      every occurrence of a term in one version, with a parallel
                   rendering from another version alongside it
    renderings(...) for a set of references, which of several candidate terms a
                   target version used there - e.g. did the Septuagint write
                   parthenos or neanis at each place the Hebrew has 'almah?

Both return plain dicts so a study builder can format them.
"""

from __future__ import annotations

import re
import sys
import unicodedata
from dataclasses import dataclass, field

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from bible import Bible, Ref  # noqa: E402

# Hebrew: matres lectionis and prefixed particles that attach to a stem.
HEBREW_PREFIXES = "הבוכלמש"  # h b w k l m sh
HEBREW_PUNCT = "׃־׀.,;:!?\"'()[]׳״"
TOKEN_SPLIT = re.compile(r"[\s־·]+")


def strip_diacritics(text: str) -> str:
    """Fold Greek accents/breathings and Hebrew points away for matching."""
    return "".join(
        ch for ch in unicodedata.normalize("NFD", text)
        if not unicodedata.combining(ch)
    )


def normalise(text: str) -> str:
    return strip_diacritics(text).lower()


@dataclass
class Occurrence:
    book: str
    chapter: int
    verse: int
    token: str
    parallel: str | None = None
    excluded: str | None = None      # reason this hit is not a real instance

    @property
    def ref(self) -> str:
        return f"{self.book} {self.chapter}:{self.verse}"


@dataclass
class Concordance:
    bible: Bible = field(default_factory=Bible)

    def _canonical_order(self, version_key: str) -> list[str]:
        return list(self.bible._load(version_key).keys())

    def find(
        self,
        version_key: str,
        pattern: str,
        *,
        parallel: str | None = None,
        whole_token: bool = True,
        exclusions: dict[str, str] | None = None,
    ) -> list[Occurrence]:
        """Every token in `version_key` matching `pattern` (a regex).

        `pattern` is matched against the diacritic-stripped token. Set
        `whole_token=False` to match anywhere inside a token. `exclusions` maps
        a reference string to the reason it is not a genuine instance; excluded
        hits are still returned, flagged, so a study can show what it filtered.
        """
        exclusions = exclusions or {}
        data = self.bible._load(version_key)
        matcher = re.compile(pattern, re.IGNORECASE)
        order = list(data.keys())
        out: list[Occurrence] = []
        for book, chapters in data.items():
            for chapter, verses in chapters.items():
                for verse, text in verses.items():
                    for raw in TOKEN_SPLIT.split(text):
                        token = raw.strip(HEBREW_PUNCT)
                        if not token:
                            continue
                        probe = normalise(token)
                        hit = matcher.fullmatch(probe) if whole_token else matcher.search(probe)
                        if not hit:
                            continue
                        ref = f"{book} {int(chapter)}:{int(verse)}"
                        out.append(Occurrence(
                            book=book, chapter=int(chapter), verse=int(verse),
                            token=token,
                            parallel=self.bible.try_verse(parallel, ref) if parallel else None,
                            excluded=exclusions.get(ref),
                        ))
        out.sort(key=lambda o: (order.index(o.book), o.chapter, o.verse))
        return out

    def renderings(
        self,
        refs: list[str],
        target_version: str,
        candidates: dict[str, str],
    ) -> list[dict]:
        """At each reference, which candidate term does `target_version` use?

        `candidates` maps a diacritic-insensitive substring to a label, e.g.
        {"παρθεν": "virgin", "νεαν": "young woman"}. This is how you show that a
        translator had more than one equivalent available and chose between them.
        """
        rows = []
        for ref in refs:
            text = self.bible.try_verse(target_version, ref)
            found = []
            if text:
                probe = normalise(text)
                for needle, label in candidates.items():
                    if normalise(needle) in probe:
                        found.append(label)
            rows.append({
                "ref": ref,
                "text": text,
                "matched": found,
                "status": "absent" if text is None else (", ".join(found) or "neither"),
            })
        return rows

    def version_table(self, ref: str, version_keys: list[str]) -> list[dict]:
        """One reference rendered across many versions."""
        return [
            {"version": key, "text": self.bible.try_verse(key, ref)}
            for key in version_keys
        ]


# -- Strong's-number search -------------------------------------------------
#
# Surface-form matching (above) was the only option before lexicon/ existed.
# Where a term has a Strong's number, prefer these: they are lemma-accurate, so
# they need no exclusion list and they catch forms that share no spelling.

class TaggedConcordance(Concordance):
    """Concordance backed by lexicon/ word-level tagging."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        import os as _os
        import sys as _sys
        _sys.path.insert(0, _os.path.join(
            _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(__file__)))), "tools"))
        from lexicon import Lexicon  # noqa: E402
        self.lex = Lexicon()

    def by_strongs(
        self,
        strongs: str,
        *,
        parallel: str | None = None,
        exact: bool = False,
    ) -> list[Occurrence]:
        """Every occurrence of a Strong's number, with a parallel rendering."""
        out: list[Occurrence] = []
        for ref in self.lex.occurrences(strongs, exact=exact):
            book, _, rest = ref.rpartition(" ")
            chapter, _, verse = rest.partition(":")
            forms = [
                w.surface for w in self.lex.words(ref)
                if w.strongs == strongs or (not exact and w.strongs.rstrip("abcdefg") == strongs)
            ]
            out.append(Occurrence(
                book=book, chapter=int(chapter), verse=int(verse),
                token=" / ".join(dict.fromkeys(forms)) or "?",
                parallel=self.bible.try_verse(parallel, ref) if parallel else None,
            ))
        return out

    def define(self, strongs: str) -> dict | None:
        return self.lex.define(strongs)
