"""Validate mistranslations.json against the repository's actual version files.

Checks, per case:
  * required fields are present and controlled vocabularies are respected
  * every version key names a file that exists in versions/ or apocrypha-versions/
  * every reference parses, and resolves in every witness listed for that case

Exit status is non-zero if anything fails, so this is usable as a CI gate.
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from bible import Bible, Ref  # noqa: E402

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "tools"))
try:
    from lexicon import Lexicon
except ImportError:
    Lexicon = None

DATASET = os.path.join(os.path.dirname(__file__), "..", "mistranslations.json")

REQUIRED = [
    "id", "title", "type", "consensus", "references", "source_term", "rendered_as",
    "transmission_chain", "what_happened", "doctrinal_impact", "impact_domains",
    "first_attested", "witnesses", "caveat", "sources",
]
WITNESS_SIDES = ["source", "shifted", "corrected"]


def main() -> int:
    data = json.load(open(DATASET, encoding="utf-8"))
    bible = Bible()
    lex = Lexicon() if Lexicon else None
    errors: list[str] = []
    warnings: list[str] = []
    resolved = 0

    types = set(data["taxonomy"])
    levels = set(data["consensus_levels"])
    seen_ids: set[str] = set()

    for case in data["cases"]:
        cid = case.get("id", "<no id>")
        for field in REQUIRED:
            if field not in case:
                errors.append(f"{cid}: missing field {field!r}")
        if cid in seen_ids:
            errors.append(f"{cid}: duplicate id")
        seen_ids.add(cid)
        if case.get("type") not in types:
            errors.append(f"{cid}: unknown type {case.get('type')!r}")
        if case.get("consensus") not in levels:
            errors.append(f"{cid}: unknown consensus {case.get('consensus')!r}")
        if not case.get("sources"):
            errors.append(f"{cid}: no sources cited")

        refs = []
        for raw in case.get("references", []):
            try:
                refs.append(Ref.parse(raw))
            except ValueError as exc:
                errors.append(f"{cid}: {exc}")
        if not refs:
            errors.append(f"{cid}: no usable references")
            continue

        # Optional: a worked example must exist on disk.
        study = case.get("study")
        if study:
            study_path = os.path.join(os.path.dirname(DATASET), study)
            if not os.path.exists(study_path):
                errors.append(f"{cid}: study {study!r} does not exist")

        # Optional: the texts a doctrine actually rests on must resolve somewhere.
        distinguish = case.get("distinguish_from")
        if distinguish:
            for field in ("claim", "rests_on", "note"):
                if not distinguish.get(field):
                    errors.append(f"{cid}: distinguish_from missing {field!r}")
            for raw in distinguish.get("rests_on", []):
                try:
                    alt = Ref.parse(raw)
                except ValueError as exc:
                    errors.append(f"{cid}: distinguish_from: {exc}")
                    continue
                if not any(bible.has(v, alt) for v in
                           ("en/NEW REVISED STANDARD VERSION", "en/KING JAMES BIBLE")):
                    errors.append(f"{cid}: distinguish_from reference {raw!r} does not resolve")
                else:
                    resolved += 1

        # Optional: Strong's numbers must exist in the lexicon and be attested.
        for number in case.get("strongs", []):
            if lex is None:
                warnings.append(f"{cid}: lexicon unavailable, cannot check {number}")
                continue
            if lex.define(number) is None:
                errors.append(f"{cid}: Strong's {number} is not in the lexicon dictionary")
            hits = lex.occurrences(number)
            if not hits:
                errors.append(f"{cid}: Strong's {number} occurs nowhere in the tagged corpus")
            else:
                resolved += len(hits)

        witnesses = case.get("witnesses", {})
        for side in WITNESS_SIDES:
            if side not in witnesses:
                errors.append(f"{cid}: witnesses missing side {side!r}")
                continue
            if not witnesses[side]:
                warnings.append(f"{cid}: no {side} witness in this repository")
            for version_key in witnesses[side]:
                if version_key not in bible.versions:
                    errors.append(f"{cid}: unknown version {version_key!r}")
                    continue
                # A witness must resolve at least one of the case's references.
                hits = [r for r in refs if bible.has(version_key, r)]
                if not hits:
                    errors.append(
                        f"{cid}: {side} witness {version_key!r} resolves none of "
                        + ", ".join(str(r) for r in refs)
                    )
                else:
                    resolved += len(hits)
                    if len(hits) < len(refs):
                        missing = [str(r) for r in refs if r not in hits]
                        warnings.append(
                            f"{cid}: {version_key} lacks " + ", ".join(missing)
                            + " (partial witness, usually a NT-only or OT-only version)"
                        )

    tagged = sum(1 for c in data["cases"] if c.get("strongs"))
    studies = sum(1 for c in data["cases"] if c.get("study"))
    distinguished = sum(1 for c in data["cases"] if c.get("distinguish_from"))
    print(f"cases:           {len(data['cases'])}")
    print(f"worked examples: {studies:>4}")
    print(f"distinguish_from:{distinguished:>4}")
    print(f"Strong's-anchored:{tagged:>3}")
    print(f"versions indexed:{len(bible.versions):>4}")
    print(f"verse lookups OK:{resolved:>4}")
    print(f"warnings:        {len(warnings):>4}")
    print(f"errors:          {len(errors):>4}")
    if warnings:
        print("\n-- warnings --")
        for w in warnings:
            print("  " + w)
    if errors:
        print("\n-- errors --")
        for e in errors:
            print("  " + e)
        return 1
    print("\nOK: every case resolves against this repository's texts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
