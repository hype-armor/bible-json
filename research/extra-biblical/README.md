# Things Christians Believe That Aren't in the Bible

A companion to [`../mistranslations`](../mistranslations). That dataset is about text
being **rendered wrongly**. This one is about text that was **never there**.

24 cases · 19 lexical checks · 101 support passages quoted · 0 errors

## Two questions, not one

A regex proves that a **wording** is absent. That is the easy half, and on its own it is
close to worthless — it would let you "prove" that a belief is unbiblical when the idea is
all over the text in different words.

So every case answers two separate questions.

### 1. Is the wording there? — mechanical

`tools/verify.py` runs these against all 142 versions and exits non-zero on failure:

| Kind | Example |
| --- | --- |
| `phrase` | "God helps those who help themselves" — **0 of 57** English versions |
| `strongs_absent` | *tappuach* "apple" (`H8598`) — **6× in the Bible, 0× in Genesis** |

Output: [`ABSENCE.md`](ABSENCE.md).

### 2. Could someone derive the idea anyway? — the part that matters

Every case carries a **`conceptual_support`** block: the passages a reasonable reader could
build the belief from, the passages that cut **against** it, a one-line reason for each, and
a graded verdict. All 101 references are resolved and quoted by the verifier, so the
**quotations are mechanical while the gradings are judgement** — kept visibly separate.

The verifier **refuses a case that has a lexical check but no support audit**, so "not in the
Bible" can never rest on a regex alone. A verdict of `none` with any supporting passage cited
is also an error.

Output: [`SUPPORT.md`](SUPPORT.md).

| Verdict | Cases | |
| --- | ---: | --- |
| `strong` | 4 | The idea is well supported; only the wording or label is post-biblical |
| `partial` | 11 | Part is supported, part imported or disputed |
| `weak` | 5 | The text gestures at it; the belief adds most of the content |
| `none` | 3 | No passage supplies it |
| `contradicted` | 1 | The text addresses the point and says the opposite |

**Only 3 of 24 beliefs have no textual basis at all.** That is the honest headline, and it is
the opposite of what a list of "things not in the Bible" usually implies.

### Where the lexical check actively misleads

- **The serpent in Eden is Satan** — graded `strong`. Genesis never says it, and the regex
  duly returns near-zero. But Revelation 12:9 and 20:2 both say "that ancient serpent, who
  is called the Devil and Satan", explicitly. The belief is thoroughly biblical; it is just
  not in Genesis. A lexical-only dataset would file this as a myth.
- **"Spare the rod and spoil the child"** — graded `strong`. The rhyme is Samuel Butler's,
  but Proverbs 13:24, 22:15, 23:13 and 29:15 say the thing. This is a misattributed
  *quotation*, not a misattributed *belief* — a distinction absence-testing cannot make.
- **"God works in mysterious ways"** — graded `strong`. Cowper wrote the line; Isaiah 55:8-9,
  Romans 11:33 and Deuteronomy 29:29 supply the idea.
- **Satan rules hell** — the only `contradicted` verdict. The *ruler* language is real
  (John 12:31, 2 Corinthians 4:4) but attached to **this world**. Revelation 20:10 has him
  thrown into the lake of fire and tormented there.

## The fairness problem, handled up front

**"Not in the Bible" is only a criticism under a theology that makes scripture the sole
authority.** Catholic and Orthodox Christianity holds scripture and sacred tradition
together, so a doctrine developed after the New Testament is not thereby suspect — it is
how those traditions expect doctrine to work.

So every case carries a **`held_by`** field naming who actually holds the belief, and the
sharp cases are flagged as such: the ones where people believe something **is** in the
text and it is not, and where a tradition claims biblical warrant the text doesn't supply.

`purgatory` is graded `contested` rather than `strong` for exactly this reason: Catholic
theology never claimed it was described in scripture.

## Composition

| Category | Cases | |
| --- | ---: | --- |
| `later-doctrine` | 7 | Formulated after the New Testament |
| `misattributed-quote` | 6 | Sayings quoted as scripture that appear nowhere in it |
| `imported-imagery` | 4 | From art, poetry and drama rather than scripture |
| `detail-supplied` | 3 | The text is silent; tradition filled it in |
| `detail-altered` | 2 | The text says something different |
| `figures-merged` | 2 | Distinct people or things conflated |

Graded `strong` 14 · `majority` 6 · `contested` 4.

## A few results

**The forbidden fruit was never an apple.** Genesis 3:6 says *peri* — generic fruit. The
Hebrew word for apple, *tappuach* (`H8598`), occurs six times in the Bible — Proverbs,
Song of Solomon, Joel — and **never in Genesis**. The apple is a Latin pun: the tree is of
*bonum et malum*, and *malum* means both "evil" and "apple".

**There is no innkeeper.** *Kataluma* (`G2646`) occurs three times in the New Testament,
and in the other two — Luke 22:11, Mark 14:14 — it is the **guest room of the Last
Supper**. Luke uses a different word for a commercial inn. No innkeeper, no stable, no
animals appear in the account at all.

**Satan does not rule hell.** Revelation 20:10 has the devil *thrown into* the lake of
fire and tormented there. He is its prisoner, not its warden. The kingdom, the throne and
the pitchfork are Dante and Milton.

**Mary Magdalene was never a prostitute.** The conflation is datable to a single homily —
Pope Gregory the Great, 14 September 591 — and the Catholic Church corrected it in 1969.
The Eastern churches never made the error.

**One version supplies the belief inside the verse.** Running the Genesis check turned up
the best evidence in the dataset: the Amplified Bible reads *"And the serpent **(Satan)**
said to the woman"*. The identification the Hebrew declines to make, added in a
parenthesis.

## Deliberate controls

The same discipline as the companion dataset — a case is included when its *history* is
documented, not when it scores a point.

- **`christmas-december-25`** is in because **both** the belief and its usual debunking
  overreach. The date is certainly not biblical, but the confident "stolen from Sol
  Invictus" claim is contested: no early Christian writer describes such a borrowing, and
  the first suggestion of it is 12th century. It's a control on this dataset's own method
  — *"not in the Bible"* is far easier to establish than *"therefore it came from here."*
- **`the-word-trinity`** notes that a post-biblical *word* says nothing about whether the
  doctrine it names fairly summarises the texts.
- **`spare-the-rod-spoil-the-child`** is graded `majority`, not `strong`, because the
  underlying Proverbs verses really do exist.

## Links to the mistranslations dataset

Three cases here rest on cases there, which is the strongest evidence that the two
problems compound:

| This dataset | rests on | That dataset |
| --- | --- | --- |
| `original-sin-inherited-guilt` | Latin *in quo*, "in whom" | `rom-5-12-eph-ho-in-quo` |
| `immaculate-conception` | *gratia plena* and *ipsa conteret* | `luke-1-28-kecharitomene`, `gen-3-15-ipsa-conteret` |
| `hell-as-dantes-underworld` | four words flattened into "hell" | `hell-sheol-hades-gehenna` |

## Files

| Path | |
| --- | --- |
| `beliefs.json` | The dataset |
| `ABSENCE.md` | **Generated.** Every lexical check and its result |
| `SUPPORT.md` | **Generated.** Every support passage, quoted, with its grading |
| `tools/verify.py` | Validates the dataset, runs the checks, writes both reports |

Reuses `research/mistranslations/tools/bible.py` and the repo-root `tools/lexicon.py`.
No dependencies beyond the standard library.
