"""Build versions.json: a metadata manifest for every version file in this repo.

A corpus about how translation changed over time needs a time axis. The version
files carry none - no publication date, no base text, no translation philosophy,
no tradition - so any chronological claim had to live in the researcher's head.

Structural fields (locale, book and verse counts, testament coverage) are
computed from the files. Editorial fields come from the table below. Where a
date or base text is genuinely uncertain the value is null rather than a guess.

Usage:  python3 tools/build_versions_manifest.py
"""

from __future__ import annotations

import json
import os

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(REPO, "versions.json")

MT = "Masoretic Text"
TR = "Textus Receptus"
CRIT = "Critical (Alexandrian)"
BYZ = "Byzantine/Majority"
LXX = "Septuagint"
VUL = "Vulgate"
ECL = "Eclectic"

# key: (year, base_text, philosophy, tradition, note)
#   philosophy: formal | dynamic | optimal | paraphrase | interlinear | source
META: dict[str, tuple] = {
    # --- source texts -----------------------------------------------------
    "he/WESTMINSTER LENINGRAD CODEX": (1008, None, "source", "Jewish (Masoretic)", "Leningrad Codex B19A, the oldest complete Hebrew Bible. Digital edition re-versified here to English numbering."),
    "he/ALEPPO CODEX": (930, None, "source", "Jewish (Masoretic)", "The Aleppo Codex; portions lost in 1947."),
    "he/WLC (CONSONANTS ONLY)": (1008, None, "source", "Jewish (Masoretic)", "Consonantal skeleton of the WLC, without vowel points. Useful for testing vocalization-dependent cases."),
    "el/SWETE'S SEPTUAGINT": (-200, None, "source", "Hellenistic Jewish", "Greek Old Testament, c. 3rd-2nd c. BCE; Swete's edition 1887-94. The translation Matthew and Paul quote."),
    "el/WESTCOTT AND HORT 1881": (1881, CRIT, "source", "Critical scholarship", "The edition that displaced the Textus Receptus in scholarship."),
    "el/WESTCOTT AND HORT 1881 - TRANSLITERATED": (1881, CRIT, "source", "Critical scholarship", None),
    "el/NESTLE GREEK NEW TESTAMENT 1904": (1904, CRIT, "source", "Critical scholarship", "Ancestor of the Nestle-Aland editions."),
    "el/NESTLE GREEK NEW TESTAMENT 1904 - TRANSLITERATED": (1904, CRIT, "source", "Critical scholarship", None),
    "el/TISCHENDORF 8TH EDITION": (1872, CRIT, "source", "Critical scholarship", "Tischendorf discovered Codex Sinaiticus; his edition leans on it heavily."),
    "el/GREEK NT: TISCHENDORF 8TH ED. - TRANSLITERATED": (1872, CRIT, "source", "Critical scholarship", None),
    "el/SCRIVENER'S TEXTUS RECEPTUS 1894": (1894, TR, "source", "Protestant (TR tradition)", "Reconstructs the Greek behind the KJV. Contains the Comma Johanneum."),
    "el/SCRIVENER'S TEXTUS RECEPTUS (1894) - TRANSLITERATED": (1894, TR, "source", "Protestant (TR tradition)", None),
    "el/STEPHANUS TEXTUS RECEPTUS 1550": (1550, TR, "source", "Protestant (TR tradition)", "Stephanus' fourth edition; introduced modern verse numbering."),
    "el/STEPHENS TEXTUS RECEPTUS (1550) - TRANSLITERATED": (1550, TR, "source", "Protestant (TR tradition)", None),
    "el/RP BYZANTINE MAJORITY TEXT 2005": (2005, BYZ, "source", "Byzantine priority", "Robinson-Pierpont. Omits the Comma Johanneum, unlike the TR - which makes the Comma's late entry visible inside the Greek alone."),
    "el/GREEK ORTHODOX CHURCH 1904": (1904, BYZ, "source", "Eastern Orthodox", "The Patriarchal Text, official for the Greek Orthodox Church."),
    "la/LATIN: VULGATA CLEMENTINA": (1592, VUL, "formal", "Roman Catholic", "Clementine edition of Jerome's Vulgate (c. 400). The Bible of Western Christendom for a millennium; the source of 'in quo', 'cornuta', 'Lucifer', 'paenitentiam agite' and 'sacramentum'."),

    # --- historical English -----------------------------------------------
    "en/WYCLIFFE BIBLE": (1395, VUL, "formal", "Lollard / pre-Reformation", "Translated from the Vulgate, not the Hebrew or Greek - so it shows which Latin-derived readings reached English before the source texts did. This public-domain edition covers 9 books only (Pentateuch and the four Gospels)."),
    "en/TYNDALE NEW TESTAMENT": (1526, TR, "formal", "English Reformation", "First English NT from the Greek. Much of the KJV's wording is Tyndale's, including 'ester' at Acts 12:4."),
    "en/GENEVA BIBLE 1599": (1599, TR, "formal", "Calvinist / English Puritan", "The Bible of Shakespeare, Bunyan and the Pilgrims. Its readings at Exodus 22:18 ('witch') and Isaiah 14:12 ('Lucifer') predate the KJV."),
    "en/DOUAY-RHEIMS BIBLE": (1610, VUL, "formal", "Roman Catholic", "Challoner revision. Translated from the Vulgate, so it carries the Latin readings into English."),
    "en/KING JAMES BIBLE": (1611, TR, "formal", "Protestant (Church of England)", "The most influential English Bible; based on the Textus Receptus and heavily dependent on Tyndale."),
    "en/WEBSTER'S BIBLE TRANSLATION": (1833, TR, "formal", "Protestant", "Noah Webster's light revision of the KJV. Quietly corrects 'Easter' to 'the passover'."),
    "en/YOUNG'S LITERAL TRANSLATION": (1862, TR, "formal", "Protestant", "Extremely literal, preserving Hebrew and Greek tense and idiom at the cost of English."),
    "en/SMITH'S LITERAL TRANSLATION": (1876, TR, "formal", "Protestant", "Julia E. Smith's translation - the first complete Bible into English by a woman."),
    "en/ENGLISH REVISED VERSION": (1885, CRIT, "formal", "Protestant (British)", "First major revision of the KJV; the first English Bible to drop the Comma Johanneum. Its attributive reading of 2 Timothy 3:16 caused an outcry."),
    "en/AMERICAN STANDARD VERSION": (1901, CRIT, "formal", "Protestant (American)", "American counterpart of the ERV. Transliterates Sheol and Hades separately instead of both as 'hell'."),
    "en/JPS TANAKH 1917": (1917, MT, "formal", "Jewish", "The Jewish Publication Society's Old Testament. Reads 'young woman' at Isaiah 7:14; follows the KJV's 'help meet' at Genesis 2:18."),
    "en/BRENTON SEPTUAGINT TRANSLATION": (1851, LXX, "formal", "Anglican", "English of the Greek Old Testament, so it shows what the Septuagint says rather than the Hebrew."),
    "en/WEYMOUTH NEW TESTAMENT": (1903, CRIT, "dynamic", "Protestant", None),
    "en/WORRELL NEW TESTAMENT": (1904, CRIT, "formal", "Protestant", None),
    "en/GODBEY NEW TESTAMENT": (1905, CRIT, "formal", "Holiness movement", None),
    "en/MACE NEW TESTAMENT": (1729, TR, "dynamic", "Protestant", "An early attempt at colloquial English."),
    "en/WORSLEY NEW TESTAMENT": (1770, TR, "formal", "Protestant", None),
    "en/HAWEIS NEW TESTAMENT": (1795, TR, "formal", "Protestant", None),
    "en/ANDERSON NEW TESTAMENT": (1864, TR, "formal", "Restoration movement", None),

    # --- modern English ----------------------------------------------------
    "en/NEW AMERICAN BIBLE": (1970, ECL, "optimal", "Roman Catholic", "The American Catholic Bible. Reads 'the young woman' at Isaiah 7:14 - the philology is accepted while the doctrine is not at stake."),
    "en/NEW AMERICAN STANDARD BIBLE": (2020, ECL, "formal", "Evangelical Protestant", None),
    "en/NASB 1977": (1977, ECL, "formal", "Evangelical Protestant", "Descends from the ASV; the NASB line originates partly in reaction to the RSV."),
    "en/NASB 1995": (1995, ECL, "formal", "Evangelical Protestant", None),
    "en/LEGACY STANDARD BIBLE": (2021, ECL, "formal", "Evangelical Protestant", "NASB revision rendering the divine name as Yahweh."),
    "en/NEW INTERNATIONAL VERSION": (2011, ECL, "optimal", "Evangelical Protestant", "The best-selling modern English Bible. The 2011 edition changed several contested renderings, including 'assume authority' at 1 Timothy 2:12."),
    "en/NEW KING JAMES VERSION": (1982, TR, "formal", "Evangelical Protestant", "Modernises the KJV while keeping the Textus Receptus - so it retains the Comma Johanneum but corrects 'Easter'."),
    "en/NEW REVISED STANDARD VERSION": (1989, ECL, "formal", "Ecumenical / mainline", "Successor to the RSV. Restored Junia at Romans 16:7."),
    "en/ENGLISH STANDARD VERSION": (2016, ECL, "formal", "Evangelical Protestant", "An RSV revision in a more conservative direction. Its 2016 change at Malachi 2:16 was contentious."),
    "en/CHRISTIAN STANDARD BIBLE": (2017, ECL, "optimal", "Southern Baptist", None),
    "en/HOLMAN CHRISTIAN STANDARD BIBLE": (2004, ECL, "optimal", "Southern Baptist", "Predecessor of the CSB."),
    "en/NEW LIVING TRANSLATION": (2015, ECL, "dynamic", "Evangelical Protestant", None),
    "en/GOOD NEWS TRANSLATION": (1976, ECL, "dynamic", "Ecumenical (American Bible Society)", None),
    "en/CONTEMPORARY ENGLISH VERSION": (1995, ECL, "dynamic", "Ecumenical (American Bible Society)", None),
    "en/GOD'S WORD® TRANSLATION": (1995, ECL, "dynamic", "Lutheran", None),
    "en/NET BIBLE": (2005, ECL, "optimal", "Evangelical Protestant", "Carries tens of thousands of translator notes - none of which are in this corpus, which is why some of its readings look unqualified here."),
    "en/INTERNATIONAL STANDARD VERSION": (2011, ECL, "optimal", "Evangelical Protestant", None),
    "en/AMPLIFIED BIBLE": (2015, ECL, "paraphrase", "Evangelical Protestant", "Expands words with bracketed alternatives rather than choosing."),
    "en/LITERAL STANDARD VERSION": (2020, ECL, "formal", "Protestant", None),
    "en/BEREAN STANDARD BIBLE": (2022, ECL, "optimal", "Evangelical Protestant", None),
    "en/BEREAN LITERAL BIBLE": (2016, ECL, "interlinear", "Evangelical Protestant", None),
    "en/MAJORITY STANDARD BIBLE": (2023, BYZ, "optimal", "Evangelical Protestant", None),
    "en/WORLD ENGLISH BIBLE": (2000, BYZ, "formal", "Public-domain project", None),
    "en/NEW HEART ENGLISH BIBLE": (2010, ECL, "formal", "Public-domain project", None),
    "en/CATHOLIC PUBLIC DOMAIN VERSION": (2009, VUL, "formal", "Roman Catholic", "Modern English from the Vulgate."),
    "en/LAMSA BIBLE": (1933, "Syriac Peshitta", "formal", "Assyrian Church of the East", "George Lamsa's translation from the Syriac, so it renders from the Aramaic side."),
    "en/PESHITTA HOLY BIBLE TRANSLATED": (2019, "Syriac Peshitta", "formal", "Aramaic primacy", None),
    "en/ARAMAIC BIBLE IN PLAIN ENGLISH": (2010, "Syriac Peshitta", "formal", "Aramaic primacy", "Shows the Petros/petra wordplay that Greek-derived versions lose."),

    # --- other languages ---------------------------------------------------
    "de/GERMAN: LUTHER (1912)": (1912, ECL, "dynamic", "Lutheran", "Revision of Luther's 1534 Bible, the founding text of modern German."),
    "de/GERMAN: MODERNIZED": (1545, TR, "dynamic", "Lutheran", "Luther's own text, modernised orthography."),
    "de/GERMAN: TEXTBIBEL (1899)": (1899, CRIT, "formal", "German Protestant", None),
    "fr/FRENCH: LOUIS SEGOND (1910)": (1910, CRIT, "formal", "French Protestant", None),
    "fr/FRENCH: DARBY": (1885, CRIT, "formal", "Plymouth Brethren", None),
    "fr/FRENCH: MARTIN (1744)": (1744, TR, "formal", "French Protestant", None),
    "es/REINA VALERA 1909": (1909, TR, "formal", "Spanish Protestant", None),
    "es/REINA VALERA GÓMEZ": (2010, TR, "formal", "Spanish Protestant", None),
    "es/SAGRADAS ESCRITURAS 1569": (1569, TR, "formal", "Spanish Protestant", "The Biblia del Oso tradition."),
    "es/LA BIBLIA DE LAS AMÉRICAS": (1986, ECL, "formal", "Evangelical Protestant", None),
    "es/LA NUEVA BIBLIA DE LOS HISPANOS": (2005, ECL, "formal", "Evangelical Protestant", None),
    "it/ITALIAN: GIOVANNI DIODATI BIBLE (1649)": (1649, TR, "formal", "Italian Protestant", None),
    "it/ITALIAN: RIVEDUTA BIBLE (1927)": (1927, CRIT, "formal", "Italian Protestant", None),
    "nl/DUTCH STATEN VERTALING": (1637, TR, "formal", "Dutch Reformed", None),
    "cs/CZECH BKR": (1613, TR, "formal", "Czech Brethren", "The Kralice Bible."),
    "ru/RUSSIAN: SYNODAL TRANSLATION (1876)": (1876, "Masoretic/Septuagint/Byzantine", "formal", "Russian Orthodox", None),
    "sv/SWEDISH (1917)": (1917, CRIT, "formal", "Church of Sweden", None),
    "hu/HUNGARIAN: KAROLI": (1590, TR, "formal", "Hungarian Reformed", None),
    "fi/FINNISH: BIBLE (1776)": (1776, TR, "formal", "Lutheran", None),
    "pt/PORTUGESE BIBLE": (1898, TR, "formal", "Portuguese Protestant", "Almeida tradition."),
    "pt/BÍBLIA KING JAMES ATUALIZADA PORTUGUÊS": (2012, ECL, "optimal", "Brazilian Protestant", None),
    "ro/ROMANIAN: CORNILESCU": (1924, ECL, "dynamic", "Romanian Protestant", None),
    "no/NORWEGIAN: DET NORSK BIBELSELSKAP (1930)": (1930, CRIT, "formal", "Lutheran", None),
    "da/DANISH": (1931, CRIT, "formal", "Lutheran", None),
    "vi/VIETNAMESE (1934)": (1934, TR, "formal", "Protestant", None),
    "tr/TURKISH": (2001, ECL, "dynamic", "Protestant", None),
    "ar/ARABIC: SMITH & VAN DYKE": (1865, TR, "formal", "Protestant", None),
    "zh/CHINESE BIBLE: UNION (TRADITIONAL)": (1919, CRIT, "formal", "Chinese Protestant", None),
    "zh/CHINESE BIBLE: UNION (SIMPLIFIED)": (1919, CRIT, "formal", "Chinese Protestant", None),
    "ko/KOREAN": (1961, ECL, "formal", "Korean Protestant", None),
    "eo/ESPERANTO": (1926, MT, "formal", "Protestant", None),
    "af/AFRIKAANS PWL": (2016, "Aramaic/Hebrew", "dynamic", "Protestant", None),
    "lt/LITHUANIAN": (1999, TR, "formal", "Protestant", None),
    "hr/CROATIAN BIBLE": (1968, ECL, "formal", "Croatian", None),
    "sq/ALBANIAN": (1994, ECL, "formal", "Protestant", None),
    "bg/BULGARIAN": (1940, TR, "formal", "Bulgarian Orthodox/Protestant", None),
    "uk/UKRAINIAN: NT": (1871, TR, "formal", "Ukrainian", None),
    "mi/MAORI": (1887, TR, "formal", "Anglican mission", None),
    "id/INDONESIAN - TERJEMAHAN LAMA (TL)": (1958, TR, "formal", "Protestant", None),
    "th/THAI: FROM KJV": (2003, TR, "formal", "Protestant", None),
    "lv/LATVIAN NEW TESTAMENT": (1937, VUL, "formal", "Roman Catholic", None),
    "hy/ARMENIAN (WESTERN): NT": (1853, "Armenian", "formal", "Armenian Apostolic", None),
    "eu/BASQUE (NAVARRO-LABOURDIN): NT": (1571, TR, "formal", "Protestant", None),
    "es/TAGALOG: ANG DATING BIBLIA (1905)": (1905, TR, "formal", "Protestant", "Tagalog, not Spanish - filed under the es/ locale in this repository, which is a data error worth knowing about."),
    "ru/RUSSIAN KOI8R": (1876, "Masoretic/Septuagint/Byzantine", "formal", "Russian Orthodox", "The Synodal text in KOI8-R encoding."),
    "zh/中文标准译本 (CSB SIMPLIFIED)": (2011, ECL, "optimal", "Chinese Protestant", None),
    "zh/中文標準譯本 (CSB TRADITIONAL)": (2011, ECL, "optimal", "Chinese Protestant", None),
    "zh/现代标点和合本 (CUVMP SIMPLIFIED)": (1919, CRIT, "formal", "Chinese Protestant", "Chinese Union Version with modern punctuation."),
    "zh/現代標點和合本 (CUVMP TRADITIONAL)": (1919, CRIT, "formal", "Chinese Protestant", "Chinese Union Version with modern punctuation."),
    "sw/SWAHILI NT": (None, None, "formal", "Protestant mission", None),
    "bar/BAVARIAN": (None, None, "dynamic", "Regional", None),
}

TESTAMENT_OT = {"Genesis", "Malachi", "Isaiah", "Psalms"}
TESTAMENT_NT = {"Matthew", "Revelation", "Romans", "John"}


def classify(books: list[str]) -> str:
    names = set(books)
    has_ot = bool(names & {"Genesis", "Isaiah", "Psalms"}) or len(books) >= 39 and "Matthew" not in names
    has_nt = bool(names & {"Matthew", "Romans", "Revelation", "ΚΑΤΑ ΜΑΤΘΑΙΟΝ", "Matthaeus"})
    if len(books) >= 60:
        return "both"
    if has_nt and not has_ot:
        return "new-testament"
    if has_ot and not has_nt:
        return "old-testament"
    return "partial"


def main() -> int:
    versions: dict = {}
    roots = [("versions", False), ("apocrypha-versions", True)]
    for root, is_apoc in roots:
        base = os.path.join(REPO, root)
        if not os.path.isdir(base):
            continue
        entries = []
        if is_apoc:
            entries = [("apocrypha", f) for f in sorted(os.listdir(base)) if f.endswith(".json")]
        else:
            for locale in sorted(os.listdir(base)):
                d = os.path.join(base, locale)
                if os.path.isdir(d):
                    entries += [(locale, f) for f in sorted(os.listdir(d)) if f.endswith(".json")]
        for locale, fn in entries:
            name = fn[:-5]
            key = f"{locale}/{name}"
            path = os.path.join(base, fn) if is_apoc else os.path.join(base, locale, fn)
            data = json.load(open(path, encoding="utf-8"))
            books = list(data.keys())
            year, base_text, philosophy, tradition, note = META.get(key, (None, None, None, None, None))
            versions[key] = {
                "name": name,
                "locale": locale,
                "path": os.path.relpath(path, REPO),
                "year": year,
                "base_text": base_text,
                "philosophy": philosophy,
                "tradition": tradition,
                "testament": "apocrypha" if is_apoc else classify(books),
                "books": len(books),
                "verses": sum(len(c) for b in data.values() for c in b.values()),
                "book_naming": "english" if books[0] in ("Genesis", "Matthew") else "local",
                "note": note,
            }

    described = sum(1 for v in versions.values() if v["year"] is not None)
    manifest = {
        "schema_version": "1.0.0",
        "note": (
            "Metadata for every version file in this repository. Structural fields "
            "(locale, books, verses, testament) are computed from the files by "
            "tools/build_versions_manifest.py; editorial fields (year, base_text, "
            "philosophy, tradition) are curated. A null means genuinely unknown, "
            "not zero."
        ),
        "vocabularies": {
            "base_text": [
                "Masoretic Text", "Septuagint", "Vulgate", "Textus Receptus",
                "Byzantine/Majority", "Critical (Alexandrian)", "Eclectic",
                "Syriac Peshitta",
            ],
            "philosophy": [
                "source - a source-language edition, not a translation",
                "formal - formal equivalence, word-for-word",
                "optimal - mediating between formal and dynamic",
                "dynamic - dynamic/functional equivalence, thought-for-thought",
                "paraphrase - free restatement",
                "interlinear - source word order preserved",
            ],
            "testament": ["both", "old-testament", "new-testament", "partial", "apocrypha"],
        },
        "coverage": {
            "total_versions": len(versions),
            "with_year": described,
            "without_year": len(versions) - described,
        },
        "versions": versions,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=1)
    print(f"wrote versions.json: {len(versions)} versions, {described} with a curated date "
          f"({100*described/len(versions):.0f}%)")
    earliest = sorted((v for v in versions.values() if v["year"]), key=lambda v: v["year"])[:3]
    print("earliest:", ", ".join(f"{v['name']} ({v['year']})" for v in earliest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
