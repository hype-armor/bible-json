# Mistranslations That Shaped Christianity

A research dataset of translation decisions, transmission errors and interpolations
that measurably changed Christian doctrine, practice, art or law — each one anchored
to verses that resolve against the version files in this repository.

36 cases · 1 worked example · 1,280 verified lookups · 566 witnesses · 18 Strong's-anchored terms · 0 broken references

## Why this repository is a good place to do this

*(Updated: the three gaps the first audit named are now closed or narrowed — see
[`COVERAGE.md`](COVERAGE.md). The corpus now carries word-level Strong's tagging in
`lexicon/`, a metadata manifest in `versions.json`, and Wycliffe, Tyndale and Geneva
in `versions/en/`.)*


Most JSON Bible corpora hold English translations only, which lets you see *that*
versions disagree but never *what they were translating from*. This one ships the
sources: three Hebrew Masoretic texts, Swete's Septuagint, the Clementine Vulgate,
and — unusually — six Greek New Testaments spanning all three major text-types.

That last point does most of the work. Because the Textus Receptus, the Byzantine
Majority Text and three critical editions are all here, several cases can be
demonstrated **inside the Greek files alone**, before any English version is opened.
The Comma Johanneum is visible as a clause present in Scrivener and Stephanus and
absent from Westcott-Hort, Nestle, Tischendorf *and* the Byzantine text — no
commentary required.

See [`COVERAGE.md`](COVERAGE.md) for the full audit, including what is missing.

## Layout

| Path | What it is |
| --- | --- |
| `mistranslations.json` | The dataset. Hand-curated, cited, graded for scholarly consensus. |
| `evidence.json` / `EVIDENCE.md` | **Generated.** The actual verse text for every witness of every case, quoted verbatim from `versions/`. |
| `COVERAGE.md` | **Generated.** Whether this corpus can support the research, and what it cannot yet do. |
| `studies/*.json` → `studies/*.md` | **Generated.** Worked examples: a declarative spec in, a study with computed tables out. |
| `tools/bible.py` | Cross-version verse access. Resolves "Isaiah 7:14" in the Hebrew, the Vulgate (`Isaias`) and the Greek NT (`ΚΑΤΑ ΜΑΤΘΑΙΟΝ`) alike. |
| `tools/validate.py` | Checks every case against the real files. Non-zero exit on failure. |
| `tools/build_evidence.py` | Regenerates `evidence.json` and `EVIDENCE.md`. |
| `tools/coverage_report.py` | Regenerates `COVERAGE.md`. |
| `tools/concordance.py` | Word-occurrence search over unpointed Hebrew and diacritic-stripped Greek, plus source→target rendering comparison. |
| `tools/build_study.py` | Builds `studies/*.md` from their specs. |

```bash
python3 research/mistranslations/tools/validate.py        # verify the dataset
python3 research/mistranslations/tools/build_evidence.py  # regenerate evidence
python3 research/mistranslations/tools/coverage_report.py # regenerate coverage
python3 research/mistranslations/tools/build_study.py     # regenerate worked examples
```

No dependencies beyond the standard library.

## How a case is recorded

```jsonc
{
  "id": "rom-5-12-eph-ho-in-quo",
  "type": "grammatical-misreading",     // one of nine categories, see `taxonomy`
  "consensus": "strong",                // strong | majority | contested | debunked
  "references": ["Romans 5:12"],
  "source_term":  { "form": "ἐφ’ ᾧ",   "gloss": "because / inasmuch as" },
  "rendered_as":  { "form": "in quo",  "gloss": "in whom" },
  "transmission_chain": ["Greek NT", "Vulgate", "Augustine", "Douay-Rheims"],
  "what_happened":     "...",
  "doctrinal_impact":  "...",
  "witnesses": {                        // version keys present in THIS repository
    "source":    ["el/WESTCOTT AND HORT 1881"],
    "shifted":   ["la/LATIN: VULGATA CLEMENTINA", "en/DOUAY-RHEIMS BIBLE"],
    "corrected": ["en/NEW REVISED STANDARD VERSION", "en/NET BIBLE"]
  },
  "caveat":  "...",                     // where the case is weaker than it looks
  "sources": ["https://..."]
}
```

`witnesses` is the part that makes the dataset falsifiable: every version key names a
real file, and `validate.py` confirms that every listed witness actually resolves the
case's references. Run it and the claim "the Douay-Rheims reads *in whom all have
sinned*" stops being something you take on trust.

## Worked examples

A case record is a summary. A **study** is the argument, with every table computed from the
corpus. The first one is [`studies/isa-7-14-almah.md`](studies/isa-7-14-almah.md) — *The Virgin
of Isaiah 7:14* — and it is built to be copied.

Studies are declarative. `studies/isa-7-14-almah.json` names a sequence of blocks; only the
`prose` blocks are written by hand:

| Block | Answers | Reusable for |
| --- | --- | --- |
| `contrast` | Is the doctrine actually resting on this verse? | Separating a claim from its proof-text |
| `interlinear` | What does the source literally say? | Definiteness, verb aspect, word order — things translation flattens |
| `concordance` | How is this word used elsewhere, and how often? | `arsenokoitai`, `authentein`, `diakonos`, `sheol`, `ezer` |
| `renderings` | Did the translator have alternatives, and use them elsewhere? | Any source→target pair: Hebrew→LXX, Greek→Vulgate |
| `verse_table` | Where did the versions land? | Every case |

`concordance` and `renderings` are the two that matter, because together they answer the
question that decides most of these cases: **did the translator have a choice, and what did
they do with it elsewhere?**

The Isaiah study is the proof. The Septuagint rendered `'almāh` as *neanis* ("young woman")
at four of the seven places it occurs — and chose *parthenos* ("virgin") at Isaiah 7:14. That
single computed table rules out both of the usual arguments at once: it was not a lexical
accident, because the translator demonstrably knew the other word; and it was not a Christian
invention, because the Septuagint is pre-Christian Jewish work. What is left is an interpretive
decision, which is exactly what the case record grades it as.

Two guardrails are built into the builder. `expect_kept` pins the number of genuine occurrences,
so the build fails rather than quietly reporting a different number if the corpus changes.
`exclusions` requires every filtered hit to carry a stated reason, printed below the table — the
seven `'almāh` occurrences survive after seven homographs are excluded **in public**.

Since the corpus has no lemma tagging (see `COVERAGE.md`), `concordance.py` matches surface
forms on the unpointed Westminster Leningrad Codex and on diacritic-stripped Greek. It is not
lemmatisation: it misses suppletive forms and catches homographs, which is why `exclusions`
exists. It is enough to answer the question, and it partially closes the gap the audit flagged
as most costly.

## The case that is now effectively settled

**Genesis 3:15.** The Vulgate reads "*ipsa* conteret caput tuum" — "**she** shall crush thy head" —
which is the textual basis for the Marian reading of the protoevangelium, for Mary-standing-on-the-
serpent imagery, and for a citation in the 1854 bull defining the Immaculate Conception.

With the ancient witnesses now in the corpus:

| Tradition | Subject | In this repo |
| --- | --- | --- |
| Masoretic Hebrew | masculine (*hu'*) | `he/WESTMINSTER LENINGRAD CODEX` |
| **Samaritan Pentateuch** (split c. 200 BCE) | **masculine** | `he/SAMARITAN PENTATEUCH` |
| Septuagint | masculine | `el/SWETE'S SEPTUAGINT` |
| **Targum Onkelos** (Aramaic) | **masculine** | `en/TARGUM ONKELOS (ETHERIDGE)` |
| Vulgate — Sixtine 1590 | **feminine** | `la/LATIN: VULGATA SIXTINA` |
| Vulgate — Clementine 1592 | **feminine** | `la/LATIN: VULGATA CLEMENTINA` |
| Wycliffe 1395, from the Latin | **"sche schal breke thin heed"** | `en/WYCLIFFE BIBLE` |

Four independent ancient traditions read masculine. Only the Latin reads feminine — and it does so
in *both* official printed editions, so this was not a printing accident. Then Wycliffe carries it
into English.

**And a counter-example in the same dataset.** At Deuteronomy 32:8 the Samaritan Pentateuch was
expected to side with the Septuagint's "sons of God" against the Masoretic "sons of Israel". It
does not — it reads "sons of Israel", leaving the Greek standing alone. The same form of argument
points opposite ways at the two verses, which is a useful corrective against treating "the ancient
witnesses agree" as a reusable move.

## The finding that most surprised me

The RSV is usually credited — or blamed — with putting "young woman" into Isaiah 7:14 in 1952,
and copies were burned from American pulpits for it. Adding the 19th-century English versions
shows that story is wrong:

| Year | Version | Isaiah 7:14 |
| ---: | --- | --- |
| 1853 | Leeser (Jewish) | "this **young woman** shall conceive" |
| 1869 | Noyes | "the **damsel** shall conceive" |
| 1949 | Bible in Basic English | "a **young woman** is now with child" |
| 1952 | RSV | "a young woman shall conceive" |

A century of English Bibles already had the reading. What changed in 1952 was not the
scholarship but the **venue** — the reading reached a mainline pulpit Bible with denominational
backing. The controversy was about authority, not philology.

This is the kind of thing the corpus can now settle, and could not before.

## What the historical versions changed

Adding Wycliffe (1395), Tyndale (1526) and Geneva (1599) corrected four cases on arrival.
This is what the missing English lineage had been costing:

| Case | What the dataset said | What the early versions show |
| --- | --- | --- |
| `acts-12-4-easter` | The KJV rendered *pascha* as "Easter" | **Tyndale** wrote "after ester" in 1526, and **Geneva** had already corrected it to "after the Passeouer" in 1599. The KJV had the right reading in front of it and reverted. |
| `exod-22-18-mekhashephah-witch` | "Witch" was fixed by the KJV | **Wycliffe**: "Thou schalt not suffre witchis to lyue". **Geneva** has the KJV's exact sentence, 12 years early. The KJV inherited it. |
| `gen-3-15-ipsa-conteret` | The Vulgate's *ipsa* stayed in Latin and Catholic English | **Wycliffe**, translating the Vulgate: "sche schal breke thin heed". **Geneva**, from the Hebrew: "He shall breake thine head". The pronoun flips exactly where the source language does. |
| `mal-2-16-hates-divorce` | The third-person reading is a 2010s revision | **Geneva 1599**: "If thou hatest her, put her away". The "I hate divorce" reading is the innovation, not the correction. |

And one that makes the Reformation legible in two words — `matt-4-17-paenitentiam-agite`:

> **Wycliffe (1395, from the Vulgate):** "Do ye penaunce, for the kyngdom of heuenes schal come niy."
> **Tyndale (1526, from Erasmus' Greek):** "repet for ye kigdome of heven is at honed."

## Word-level search

`lexicon/` carries Strong's numbers and morphology for **306,785 Hebrew words** and
**140,149 Greek words**, re-versified onto this repository's own numbering so a reference
that works against a version file works against the tagging too.

```python
from lexicon import Lexicon          # repo-root tools/
lex = Lexicon()
lex.occurrences("H5959")             # every verse with 'almah — 7 of them
lex.words("Isaiah 7:14")             # the verse, word by word, tagged
lex.define("G733")                   # arsenokoites
```

18 cases now carry a `strongs` field, and `validate.py` checks every number exists and is
attested. The payoff shows in the Isaiah study: the surface-form method needs seven
homographs excluded by hand to reach seven occurrences of `'almāh`; the tagged method
reaches the same seven knowing nothing about spelling. Two independent methods, one answer.

## What a case is not

Five cases carry a `distinguish_from` field naming the doctrine people attach to the verse and
the texts that doctrine **actually** rests on. This is the guard against the commonest failure
mode in this subject — treating a translation shift in a proof-text as though it invented the
belief.

| Case | Claim | Actually rests on |
| --- | --- | --- |
| `isa-7-14-almah-parthenos` | The virgin birth | Luke 1:27, 1:34; Matthew 1:18 — Greek originals |
| `1john-5-7-comma-johanneum` | The Trinity | Matthew 28:19; John 1:1 — Nicaea's bishops had no Comma |
| `isa-14-12-lucifer` | Satan's fall | Luke 10:18; Revelation 12:9 |
| `1cor-6-9-arsenokoitai-malakoi` | Prohibition of same-sex acts | Leviticus 18:22; Romans 1:26–27 |
| `ps-22-16-kaaru-pierced` | That Jesus was crucified | John 19:18, 19:37; Mark 15:24 |

Every reference is validated. The pattern generalises: for each case, ask what would survive if
the disputed verse were deleted. Usually the doctrine survives and a *prophecy* does not.

## Composition

| Consensus | Cases | Meaning |
| --- | ---: | --- |
| `strong` | 17 | Broad cross-confessional agreement that the rendering departs from the source. |
| `majority` | 10 | Most critical scholars agree; a reasoned minority defends the traditional reading. |
| `contested` | 8 | Live dispute. The dataset records the dispute, not a verdict. |
| `debunked` | 1 | A popular mistranslation claim that fails on the evidence. |

Nine categories, led by `semantic-narrowing` (11) and `grammatical-misreading` (10).
Impact spans soteriology, ecclesiology, marriage, art, civil law and — in two cases —
executions.

## Some of what is in here

- **Romans 5:12.** Greek *eph' hō*, "because", became Latin *in quo*, "in whom". Augustine
  built inherited guilt on the Latin. The Greek East, reading Greek, never did. The largest
  doctrinal divergence between Eastern and Western Christianity rests on one preposition.
- **Matthew 4:17.** *Metanoeite*, "change your mind", became *paenitentiam agite*, "do penance".
  Erasmus flagged it in 1516; Luther's first thesis is about this word. The Reformation starts here.
- **Isaiah 14:12.** A taunt-song against a Babylonian king calls him "shining one, son of dawn".
  Latin *lucifer* was the ordinary word for the morning star. English capitalised it, and the
  devil acquired a name and a fall narrative the Bible never tells.
- **Exodus 34:29.** Moses' face *qāran* — sent out rays. Jerome read the root *qeren*, "horn".
  A thousand years of horned Moses in Western art, and a durable antisemitic trope.
- **Romans 16:7.** Junia, an apostle, was printed as "Junias" — a male name unattested anywhere
  in antiquity — from 1927 through most of the 20th century, exactly while women's ordination
  was being argued.
- **Matthew 19:24.** The camel that was supposedly a rope. It wasn't. Included as a negative
  control: every Greek witness here reads *kamēlos*, and a pipeline that flags this verse is
  finding something that is not there.

Full text and quoted evidence for all 36 in [`EVIDENCE.md`](EVIDENCE.md).

## Principles this dataset tries to hold to

**Grade the consensus, don't launder it.** Isaiah 7:14 and the 1946 RSV rendering of
*arsenokoitai* are the two cases most likely to be cited as settled. Neither is, and both
carry a `caveat` field saying where the popular framing overreaches.

**Newer is not automatically truer.** Two cases are recorded with the labels inverted on
purpose. At 2 Timothy 3:16 the majority of grammarians favour the KJV's reading over the
Revised Version's. At Genesis 1:6 the modern retreat from "firmament" to "expanse" is itself
arguably the tendentious move, softening an ancient cosmology to protect a doctrine of
scripture. A dataset that always scores the newest version as correct is measuring fashion.

**Keep a negative control.** `matt-19-24-camel-rope` is in the dataset precisely because the
claim is false. So is `1tim-6-10-root-of-all-evil`, where the KJV is fine and the *proverb*
is wrong — a reception problem wearing a translation problem's clothes. Any analysis built on
this data should be able to tell those apart.

**Check the claims against the texts, then fix them.** Building `EVIDENCE.md` caught ten
witness misclassifications in the first draft of this dataset — cases where the version I had
filed as correcting a rendering turned out to reproduce it. The NET Bible reads "servant" at
Romans 16:1 and "deacons" at 1 Timothy 3:8, putting it on the side of the problem. The JPS
TANAKH 1917 reads "an help meet for him", word for word with the KJV. The KJV, NRSV and NET all
obscure the *Petros*/*petra* wordplay exactly as the Vulgate does; only the two Peshitta-derived
versions show it. Every one of those corrections is in the dataset, and they exist because the
tooling quotes the actual text rather than trusting the note.

**Say where the evidence isn't.** Several cases turn on witnesses this repository does not
have: the RSV 1946, the New World Translation, Qumran fragments, Tyndale. Those cases carry
the gap in their `caveat`, and `COVERAGE.md` lists them all.

## Is the corpus complete enough? Yes — with three gaps

The audit's verdict, in short:

1. ~~No word-level tagging.~~ **Closed.** `lexicon/` — 446,934 tagged words, built by
   `tools/build_lexicon.py` from morphhb and Robinson-Pierpont. The Septuagint is still untagged.
2. ~~The English lineage jumps from 1611 to the 20th century.~~ **Closed for everything that can
   legally be redistributed.** 13 versions added — an unbroken line from Wycliffe (1395) to 2022.
   The RSV, NRSVue and New World Translation are in copyright; three cases carry that limitation
   in their `caveat`.
3. ~~No version metadata.~~ **Closed.** `versions.json` — 125 versions, 113 with curated dates,
   plus base text, translation philosophy and tradition.

The largest remaining gap is the **absence of a textual apparatus**: versions that *bracket*
Mark 16:9–20 look identical here to versions that print it plainly, and the NET Bible's
translator notes are invisible, which is why some of its readings look unqualified.

Two further findings worth knowing before citing anything:

- **The Hebrew files are re-versified to English numbering** (verified: Joel has 3 chapters,
  not the Masoretic 4; Psalm superscriptions are folded into verse 1). Excellent for
  alignment, but `WLC Malachi 4:1` is a reference no printed Hebrew Bible contains.
- **There is no textual apparatus.** Versions that *bracket* Mark 16:9–20 are indistinguishable
  here from versions that print it plainly. Two cases are flagged for this.

## Backlog

Researched but not yet written up: Leviticus 18:22 *to'evah*; 1 Corinthians 11:3 *kephalē*;
Genesis 3:16 *teshuqah*; Ephesians 5:22 and the missing verb; Colossians 1:15 *prototokos*;
Romans 9:5 punctuation; *ekklesia* → "church" and *baptizō* → "baptize" as translation-mandate
decisions; John 3:3 *anōthen*; Isaiah 45:7 *ra'*; 1 Samuel 13:1's broken numerals;
Hebrews 11:1 *hypostasis*; Acts 20:28; Titus 2:13 and the Granville Sharp rule.

## Caution

This is a research artifact about the history of translation, not a devotional or polemical
one. Cases are included because their *history* is documented, on all sides of every
confessional divide — the Vulgate, the KJV and the modern critical versions each appear in the
"shifted" column somewhere. Where scholarship is genuinely divided, the dataset says so rather
than picking a winner.
