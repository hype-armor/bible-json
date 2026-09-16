"""Turn a declarative study spec into a worked example.

A study is a JSON file in `studies/` naming a case and a sequence of blocks.
Every block that makes a factual claim is *computed* from the version files, so
a study cannot drift away from the corpus: re-run the builder and either the
numbers still hold or the build changes.

Block types:

  prose        hand-written commentary (the only block that is not computed)
  verse_table  one reference across many versions
  interlinear  a hand-supplied word-by-word gloss, checked against the verse
  concordance  every occurrence of a term, with a parallel gloss and a filter
  renderings   which of several candidate terms a target version used at each
               of a list of references
  contrast     several references side by side across the same versions

Usage:  python3 tools/build_study.py [study-id ...]   (default: all)
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bible import Bible  # noqa: E402
from concordance import Concordance, normalise  # noqa: E402

HERE = os.path.dirname(__file__)
STUDIES = os.path.join(HERE, "..", "studies")


def short(key: str) -> str:
    return key.split("/", 1)[1] if "/" in key else key


class StudyBuilder:
    def __init__(self) -> None:
        self.conc = Concordance()
        self.bible: Bible = self.conc.bible
        self.checks: list[str] = []

    # -- blocks ----------------------------------------------------------

    def prose(self, block) -> list[str]:
        return [block["text"].strip(), ""]

    def verse_table(self, block) -> list[str]:
        ref = block["ref"]
        out = [f"**{ref}**", ""]
        out += ["| Version | Reading |", "| --- | --- |"]
        for row in self.conc.version_table(ref, block["versions"]):
            text = row["text"]
            if text is None:
                self.checks.append(f"MISSING {row['version']} @ {ref}")
                text = "_(not in this version)_"
            out.append(f"| `{short(row['version'])}` | {text} |")
        out.append("")
        return out

    def interlinear(self, block) -> list[str]:
        ref, version = block["ref"], block["version"]
        text = self.bible.verse(version, ref)
        out = [f"**{ref}** — `{short(version)}`", "", f"> {text}", ""]
        out += ["| Word | Translit | Gloss |", "| --- | --- | --- |"]
        probe = normalise(text)
        for word, translit, gloss in block["words"]:
            # Verify each glossed word actually occurs in the verse.
            if word and normalise(word) not in probe:
                self.checks.append(f"INTERLINEAR {ref}: {word!r} not found in {short(version)}")
            out.append(f"| {word} | *{translit}* | {gloss} |")
        out.append("")
        return out

    def concordance(self, block) -> list[str]:
        exclusions = block.get("exclusions", {})
        hits = self.conc.find(
            block["version"], block["pattern"],
            parallel=block.get("parallel"),
            exclusions=exclusions,
        )
        kept = [h for h in hits if not h.excluded]
        dropped = [h for h in hits if h.excluded]
        expected = block.get("expect_kept")
        if expected is not None and len(kept) != expected:
            self.checks.append(
                f"CONCORDANCE {block.get('title','?')}: expected {expected} genuine hits, found {len(kept)}"
            )
        out = []
        if block.get("title"):
            out += [f"**{block['title']}**", ""]
        out += ["| Reference | Form | Rendering |", "| --- | --- | --- |"]
        limit_rows = block.get("limit")
        shown = kept[:limit_rows] if limit_rows else kept
        for h in shown:
            gloss = (h.parallel or "").strip()
            limit = block.get("gloss_chars", 110)
            if len(gloss) > limit:
                gloss = gloss[:limit].rsplit(" ", 1)[0] + " …"
            out.append(f"| {h.ref} | {h.token} | {gloss} |")
        if limit_rows and len(kept) > limit_rows:
            out.append(f"| … | | _{len(kept) - limit_rows} further occurrences_ |")
        out.append("")
        out.append(f"**{len(kept)} genuine occurrences.**")
        if dropped:
            out.append("")
            out.append(f"{len(dropped)} further hits on the same consonants were excluded:")
            out.append("")
            reasons: dict[str, list[str]] = {}
            for h in dropped:
                reasons.setdefault(h.excluded, []).append(h.ref)
            for reason, refs in reasons.items():
                out.append(f"- {reason} — {', '.join(refs)}")
        out.append("")
        return out

    def strongs(self, block) -> list[str]:
        """Occurrences of a Strong's number, from lexicon/ rather than spelling."""
        from concordance import TaggedConcordance
        if not isinstance(self.conc, TaggedConcordance):
            self.conc = TaggedConcordance()
            self.bible = self.conc.bible
        number = block["number"]
        entry = self.conc.define(number)
        hits = self.conc.by_strongs(number, parallel=block.get("parallel"))
        expected = block.get("expect")
        if expected is not None and len(hits) != expected:
            self.checks.append(
                f"STRONGS {number}: expected {expected} occurrences, lexicon gives {len(hits)}")
        out = []
        if block.get("title"):
            out += [f"**{block['title']}**", ""]
        if entry:
            out += [f"`{number}` — {entry.get('lemma','')} (*{entry.get('xlit') or entry.get('translit','')}*) — "
                    f"{(entry.get('strongs_def') or '').strip()} · KJV renders it: {entry.get('kjv_def','')}", ""]
        out += ["| Reference | Form | Rendering |", "| --- | --- | --- |"]
        for h in hits:
            gloss = (h.parallel or "").strip()
            limit = block.get("gloss_chars", 100)
            if len(gloss) > limit:
                gloss = gloss[:limit].rsplit(" ", 1)[0] + " …"
            out.append(f"| {h.ref} | {h.token} | {gloss} |")
        out += ["", f"**{len(hits)} occurrences**, from word-level tagging — no exclusion list, no "
                    "surface-form guessing.", ""]
        return out

    def renderings(self, block) -> list[str]:
        rows = self.conc.renderings(block["refs"], block["target"], block["candidates"])
        out = []
        if block.get("title"):
            out += [f"**{block['title']}**", ""]
        out += [f"| Reference | `{short(block['target'])}` uses | Text |", "| --- | --- | --- |"]
        for row in rows:
            text = (row["text"] or "_(verse not present)_")
            limit = block.get("text_chars", 95)
            if len(text) > limit:
                text = text[:limit].rsplit(" ", 1)[0] + " …"
            out.append(f"| {row['ref']} | **{row['status']}** | {text} |")
        out.append("")
        labels = {r["status"] for r in rows if r["status"] not in ("absent", "neither")}
        if len(labels) > 1:
            out.append(
                f"The same translator used {len(labels)} different equivalents for one source word: "
                + ", ".join(sorted(f"**{x}**" for x in labels))
                + ". The choice at each verse was a decision, not a default."
            )
            out.append("")
        return out

    def contrast(self, block) -> list[str]:
        out = []
        if block.get("title"):
            out += [f"**{block['title']}**", ""]
        out += ["| Reference | Version | Reading |", "| --- | --- | --- |"]
        for ref in block["refs"]:
            for version in block["versions"]:
                text = self.bible.try_verse(version, ref)
                if text is None:
                    continue
                limit = block.get("text_chars", 150)
                if len(text) > limit:
                    text = text[:limit].rsplit(" ", 1)[0] + " …"
                out.append(f"| {ref} | `{short(version)}` | {text} |")
        out.append("")
        return out

    # -- driver ----------------------------------------------------------

    def build(self, spec: dict) -> str:
        handlers = {
            "prose": self.prose, "verse_table": self.verse_table,
            "interlinear": self.interlinear, "concordance": self.concordance,
            "renderings": self.renderings, "contrast": self.contrast,
            "strongs": self.strongs,
        }
        lines = [f"# {spec['title']}", ""]
        if spec.get("case_id"):
            lines.append(
                f"Worked example for case [`{spec['case_id']}`](../mistranslations.json). "
                "Generated by `tools/build_study.py` — every table below is computed from "
                "this repository's version files."
            )
            lines.append("")
        if spec.get("question"):
            lines += [f"> **{spec['question']}**", ""]
        for block in spec["blocks"]:
            if block.get("heading"):
                lines.append(f"## {block['heading']}")
                lines.append("")
            handler = handlers.get(block["type"])
            if handler is None:
                raise ValueError(f"unknown block type {block['type']!r}")
            lines += handler(block)
        return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str]) -> int:
    builder = StudyBuilder()
    wanted = set(argv) or None
    specs = sorted(f for f in os.listdir(STUDIES) if f.endswith(".json"))
    built = 0
    for name in specs:
        spec = json.load(open(os.path.join(STUDIES, name), encoding="utf-8"))
        if wanted and spec["id"] not in wanted:
            continue
        text = builder.build(spec)
        out = os.path.join(STUDIES, spec["id"] + ".md")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"wrote studies/{spec['id']}.md ({len(text.splitlines())} lines)")
        built += 1
    if builder.checks:
        print("\n-- consistency checks failed --")
        for c in builder.checks:
            print("  " + c)
        return 1
    print(f"\n{built} study/studies built, all consistency checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
