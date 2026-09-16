# 📖 Bible Versions JSON Dataset

A free, open-source collection of **56 English Bible versions** and **38 total languages** in **JSON format**, structured by book, chapter, and verse. Some versions include the **Full Bible**, while others are **New Testament only**.
This is the **most comprehensive JSON dataset of English Bible translations** available, including popular versions like **NLT, NIV, NKJV, NASB, ESV, KJV, and more**.
Each translation is stored as its own `.json` file for easy parsing, analysis, app development, or AI projects.

## 🗂️ Structure

Each file represents a single Bible version (e.g., `niv.json`, `kjv.json`, `esv.json`).  
Verses are stored in a consistent JSON structure:

```json
{
  "Genesis": {
    "1": {
      "1": "In the beginning God created the heavens and the earth.",
      "2": "Now the earth was formless and empty..."
    },
    "2": { ... }
  },
  "Exodus": { ... }
}
```

This structure makes it easy to:

- Iterate through chapters or verses
- Build Bible search tools
- Compare translations
- Feed data into apps, websites, or AI/NLP models


- ✅ Top-level keys = Book names
- ✅ Second-level keys = Chapter numbers
- ✅ Third-level keys = Verse numbers

## 🧠 Use Cases

- Bible apps and APIs
- AI and NLP text analysis
- Theological research
- Cross-version comparison tools
- Verse similarity or embedding models
- Scripture memorization apps

## 📜 About Non-Canonical / Deuterocanonical Books

This dataset includes access to books often referred to as the "Apocrypha" or "Deuterocanonical" books. While not included in the standard Protestant canon of 66 books, they hold significant historical, theological, and literary value.

### Why are they important?
These texts bridge the historical gap (often called the "Intertestamental Period") between the Old and New Testaments. They provide crucial context for understanding the cultural and political landscape of Judea leading up to the time of Jesus, particularly the struggles against Hellenism and the origins of Jewish festivals like Hanukkah.

### Who follows them?
* **Catholic & Orthodox Traditions:** Recognize most of these books as **Deuterocanonical** ("second canon"), meaning they are considered inspired scripture and are used to establish doctrine.
* **Anglican & Lutheran Traditions:** Often view these books as useful for instruction and "examples of life and instruction of manners," though generally not used to establish doctrine.
* **Coptic Tradition:** Includes books like the Prayer of Manasseh in their canonical lists.

### How were they found?
Most of these books were preserved through the **Septuagint (LXX)**, the Greek translation of the Old Testament widely used by early Christians and the writers of the New Testament. In modern times, the discovery of the **Dead Sea Scrolls** at Qumran provided significant archaeological evidence, containing Hebrew and Aramaic fragments of books like Tobit and Sirach, confirming their ancient usage and circulation alongside canonical texts.

### Included Books
The following books are available in relevant versions within this dataset:

* **Tobit**
* **Judith**
* **Wisdom of Solomon**
* **Sirach (Ecclesiasticus)**
* **Baruch (including the Epistle of Jeremiah)**
* **First Maccabees**
* **Second Maccabees**
* **Prayer of Manasseh** (Found in Coptic canons; sometimes appended to Chronicles)

## 📜 Historical English Versions

The corpus now carries an unbroken English line from 1395, which makes it possible to date a
rendering rather than only observe it:

| Year | Version | Why it matters |
| ---: | --- | --- |
| 1395 | Wycliffe Bible | Translated from the **Vulgate**, so it shows which Latin readings reached English before the Greek did |
| 1526 | Tyndale New Testament | First English NT from the Greek; most of the KJV's wording is his |
| 1599 | Geneva Bible | The Bible of Shakespeare and the Pilgrims |
| 1853 | Leeser Old Testament | First Jewish translation into English, 64 years before the JPS |
| 1862 | Targum Onkelos (Etheridge) | English of the authoritative Aramaic paraphrase of the Pentateuch |
| 1869 | Noyes Translation | Critical-text American translation |
| 1873 | KJV Cambridge Paragraph Bible | Scrivener's critical edition of the KJV text itself |
| 1890 | Darby Bible | Darby also originated the pre-tribulational rapture scheme |
| 1902 | Rotherham Emphasised Bible | Transliterates Sheol and Hades instead of flattening both to "hell" |
| 1949 | Bible in Basic English | ~1,000-word controlled vocabulary forces interpretive choices into the open |
| 2016 | Family 35 New Testament | CC BY-SA |
| 2022 | Text-Critical English New Testament | CC BY |

**Not included, for licensing reasons:** the RSV, NRSVue and New World Translation are in
copyright and cannot be redistributed. The modernised Wycliffe on ebible.org is CC BY-NC-**ND**,
whose No-Derivatives term forbids format conversion — the edition here is the original
public-domain 1395 text instead.

⚠️ **Two versification traps**, documented in `versions.json`: Wycliffe's **Psalms follow Vulgate
numbering** (Wycliffe Psalm 16 is the Hebrew Psalm 17), and Targum Onkelos' **Exodus is offset by
one verse**. Both resolve fine as references — they are just the wrong verse.

Converted by `tools/import_usfm.py` and `tools/import_scrollmapper.py`.

## 🔤 Word-Level Tagging (`lexicon/`)

Strong's numbers and morphology for every word of the Hebrew Old Testament and the Greek
New Testament, **re-versified onto this repository's own chapter and verse numbering** so a
reference that works against a version file works against the tagging too.

| File | Contents |
| --- | --- |
| `lexicon/hebrew.json` | 306,785 tagged words — `{book: {chapter: {verse: [[strongs, morph, surface, lemma], …]}}}` |
| `lexicon/greek.json` | 140,149 tagged words, same shape |
| `lexicon/strongs-hebrew.json` | 8,674 dictionary entries |
| `lexicon/strongs-greek.json` | 5,523 dictionary entries |
| `lexicon/SOURCES.md` | Provenance, licences and the alignment report |

```python
import sys; sys.path.insert(0, "tools")
from lexicon import Lexicon
lex = Lexicon()
lex.occurrences("H5959")      # ['Genesis 24:43', ..., 'Isaiah 7:14']
lex.words("Isaiah 7:14")      # word by word, with Strong's and morphology
lex.define("G26")             # ἀγάπη
```

Built by `tools/build_lexicon.py` from [morphhb](https://github.com/openscriptures/morphhb)
(CC BY 4.0), [byztxt](https://github.com/byztxt/byzantine-majority-text) (public domain) and
[openscriptures/strongs](https://github.com/openscriptures/strongs) (**CC BY-SA** — carry that
licence forward if you redistribute `strongs-*.json`).

Note the versification work: morphhb follows BHS, this repository follows English numbering.
The mapping is derived by aligning consonantal word sequences rather than hand-coded rules —
**99.01% of 306,785 words align exactly, and no verse is left untagged.**

## 📋 Version Metadata (`versions.json`)

Publication year, base text, translation philosophy, tradition, testament coverage and
book-naming convention for all 125 versions. 113 carry a curated date; the rest are `null`
rather than guessed.

```json
"en/KING JAMES BIBLE": {
  "year": 1611, "base_text": "Textus Receptus", "philosophy": "formal",
  "tradition": "Protestant (Church of England)", "testament": "both",
  "books": 66, "verses": 31102, "book_naming": "english"
}
```

Regenerate with `python3 tools/build_versions_manifest.py`. Structural fields are computed
from the files, so the manifest cannot drift out of sync with them.

## 🔬 Research: Mistranslations That Shaped Christianity

`research/mistranslations/` holds a dataset of 36 translation decisions, transmission errors
and interpolations with documented effects on Christian doctrine, practice, art or law — each
anchored to verses that resolve against the version files here, with tooling that verifies
every claim. See its [README](research/mistranslations/README.md).

## 🧰 Tools

| Script | Purpose |
| --- | --- |
| `tools/build_lexicon.py` | Build `lexicon/` from upstream tagged texts |
| `tools/lexicon.py` | Read access to the tagging |
| `tools/build_versions_manifest.py` | Build `versions.json` |
| `tools/import_usfm.py` | Convert a USFM Bible into this repository's JSON shape |

## 🛠️ Contributing

Pull requests are welcome! If you’d like to:

- Add new versions
- Fix formatting or verse issues
- Improve data consistency

…please open a PR or issue.

If you're feeling generous and want to see this get completed, consider supporting me below ↓

<a href="https://www.buymeacoffee.com/arrontaylor" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

## ❤️ Acknowledgments

Data was collected and structured to make Scripture easier to study, compare, and use in digital projects.
Special thanks to open Bible resources and the developer community for keeping these texts accessible.
