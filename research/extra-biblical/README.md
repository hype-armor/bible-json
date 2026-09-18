# Things Christians Believe That Aren't in the Bible

A companion to [`../mistranslations`](../mistranslations). That dataset is about text
being **rendered wrongly**. This one is about text that was **never there**.

24 cases · 19 with a machine-checkable claim · 0 errors

## The method that makes this different

Most lists of "things not in the Bible" are assertions. With 142 versions on disk,
absence is **provable**: a phrase that appears in 0 of 57 English Bibles is a result, not
an opinion. `tools/verify.py` runs every such claim on demand and exits non-zero if one
fails, so the dataset cannot quietly drift away from the corpus.

```bash
python3 research/extra-biblical/tools/verify.py   # validate + regenerate ABSENCE.md
```

Two check kinds:

| Kind | Proves | Example |
| --- | --- | --- |
| `phrase` | A wording appears in at most N versions | "God helps those who help themselves" — **0 of 57** |
| `strongs_absent` | A source word never occurs in a given book | Hebrew *tappuach* "apple" (`H8598`) — **6× in the Bible, 0× in Genesis** |

Five cases are historical claims (when a doctrine was formulated, who coined a phrase).
Those carry citations instead, and the summary always reports the ratio so you can see
how much of the dataset is machine-backed.

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
| `misattributed-quote` | 6 | Sayings quoted as scripture that appear nowhere in it |
| `later-doctrine` | 7 | Formulated after the New Testament |
| `imported-imagery` | 3 | From art, poetry and drama rather than scripture |
| `detail-supplied` | 3 | The text is silent; tradition filled it in |
| `detail-altered` | 3 | The text says something different |
| `figures-merged` | 2 | Distinct people or things conflated |

Graded `strong` 14 · `majority` 4 · `contested` 3.

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
| `ABSENCE.md` | **Generated.** Every mechanical check and its result |
| `tools/verify.py` | Validates the dataset and runs the checks |

Reuses `research/mistranslations/tools/bible.py` and the repo-root `tools/lexicon.py`.
No dependencies beyond the standard library.
