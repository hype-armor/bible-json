# Mistranslations That Shaped Christianity

A research dataset of translation decisions, transmission errors and interpolations
that measurably changed Christian doctrine, practice, art or law — each one anchored
to verses that resolve against the version files in this repository.

36 cases · 61 verse references · 557 verified cross-version verse lookups · 0 broken references

## Why this repository is a good place to do this

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
| `tools/bible.py` | Cross-version verse access. Resolves "Isaiah 7:14" in the Hebrew, the Vulgate (`Isaias`) and the Greek NT (`ΚΑΤΑ ΜΑΤΘΑΙΟΝ`) alike. |
| `tools/validate.py` | Checks every case against the real files. Non-zero exit on failure. |
| `tools/build_evidence.py` | Regenerates `evidence.json` and `EVIDENCE.md`. |
| `tools/coverage_report.py` | Regenerates `COVERAGE.md`. |

```bash
python3 research/mistranslations/tools/validate.py        # verify the dataset
python3 research/mistranslations/tools/build_evidence.py  # regenerate evidence
python3 research/mistranslations/tools/coverage_report.py # regenerate coverage
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

1. **No word-level tagging.** Every case here had to be anchored to a verse by hand. Without
   Strong's numbers or morphology you cannot ask "where *else* does this version render
   *diakonos* differently?" — which is exactly the question that makes the Phoebe case, or the
   whole *sheol*/*hades*/*gehenna* family, analysable at scale. Highest-value addition by far.
2. **The English lineage jumps from 1611 to the 20th century.** No Wycliffe, Tyndale, Geneva,
   Bishops', or RSV. The dataset can show *that* a rendering changed, but often not *when* or
   *with whom*. All four are public domain.
3. **No version metadata.** Publication year, base text and translation philosophy exist
   nowhere in the repository. A study about change over time currently has no time axis
   except the one in the researcher's head. Cheapest fix, and every analysis wants it.

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
