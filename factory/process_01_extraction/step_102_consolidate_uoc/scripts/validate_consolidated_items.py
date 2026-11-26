#!/usr/bin/env python3
"""Prove a cluster's consolidated_uoc.md holds every assessable item, exactly once, verbatim.

One of step 02's two gate scripts. This one reads the deliverable PLUS every source unit; its sibling
`validate_consolidated_format.py` reads only the deliverable and its format standard.

`consolidated_uoc.md` is the last point in the run-sheet where the source of truth is still checkable.
Nothing downstream reads the units again -- the assessment plan's coverage rollup, every AT's
traceability, the mapping documents and the cluster-coverage capstone all build their expected item set
from this one document. An item lost here does not surface later as a gap; it surfaces as 100% coverage
of a set that is quietly short.

Four things must hold about the ITEM layer, while the gate stays indifferent to the EDITORIAL layer
around it (group headings, rationale, assessment ideas -- legitimately in no unit):

  MISSING         every assessable item from every unit is present
  UNEXPECTED      nothing is present that no unit contains
  DUPLICATED      each item appears exactly once
  MISTRANSCRIBED  each item's text is the source's text, under the reference identifying it

Behaviour is specified by cases VCI-01 .. VCI-26 in factory/docs/test-plan.md.

stdlib only.

Usage:
  validate_consolidated_items.py --cluster <CLUSTER_DIR> \\
      --unit ICTCLD504=units_of_competency/ICTCLD504_Complete_R1.md \\
      --unit BSBXTW401=units_of_competency/BSBXTW401_Complete_R2.md \\
      [--assessor-ac]

Exit 0 = PASS, 1 = defects found, 2 = the inputs could not be read.
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "common" / "helpers"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import cosmetic  # noqa: E402
import inventory_uoc  # noqa: E402
import item_reference as ref  # noqa: E402

BULLET = re.compile(r"^[-*] ")
CHILD_BULLET = re.compile(r"^\s+[-*] ")
BR = re.compile(r"<br\s*/?>")
LEADING_BULLET = re.compile(r"^\s*[-*]\s+", re.M)


def build_inventory(units: list[tuple[str, Path]], assessor_ac: bool) -> dict[str, str]:
    """The expected items, {reference: verbatim item block}, from the source units.

    Itemisation is delegated to `inventory_uoc` -- the same extractor that produced the item lines in
    the first place. There is deliberately no second copy of the parsing rules here: two mirrored
    parsers that must agree are a maintenance hazard, not independent evidence. The independent check
    on the .md's structure lives upstream at Gate 01, where the .docx is the oracle.
    """
    expected = {}
    for unit, md_path in units:
        md = md_path.read_text(encoding="utf-8")
        for _header, items in inventory_uoc.inventory(unit, md, assessor_ac):
            for block in items:
                found = ref.first(block)
                if found is None:                # the extractor emits a reference on every item
                    raise ValueError(f"{unit}: an extracted item carries no reference: {block[:60]!r}")
                expected[" ".join(found)] = block
    return expected


def item_blocks(text: str) -> dict[str, str]:
    """{reference: item block} for the consolidated document's tagged bullet lines.

    An item line is a bullet carrying its reference OUTSIDE a code span -- editorial prose cites
    references in backticks, and must not be mistaken for an item. The block runs on through any
    following indented, unreferenced sub-bullets, which belong to that item.
    """
    lines = text.splitlines()
    blocks = {}
    for i, line in enumerate(lines):
        if not BULLET.match(line):
            continue
        found = ref.first(ref.strip_code_spans(line))
        if found is None:
            continue

        block = [line]
        for following in lines[i + 1:]:
            if (CHILD_BULLET.match(following)
                    and ref.first(ref.strip_code_spans(following)) is None):
                block.append(following)
            else:
                break
        blocks.setdefault(" ".join(found), "\n".join(block))
    return blocks


def item_words(block: str) -> list[str]:
    """An item's text as a word sequence, for comparison against its source.

    Everything that is rendering rather than content is removed: the reference, bullet markers and
    indentation, bold markers, and <br> cell separators. Word's cosmetic substitutions are folded with
    the same rule Gate 01 uses, so a smart quote is not a mistranscription.
    """
    text = ref.PATTERN.sub("", block)
    text = BR.sub(" ", text).replace("**", "")
    text = LEADING_BULLET.sub("", text)
    return cosmetic.normalise(text).split()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cluster", required=True, type=Path)
    ap.add_argument("--unit", required=True, action="append", help="CODE=relative/or/abs/path.md")
    ap.add_argument("--assessor-ac", action="store_true",
                    help="count the trailing assessor-requirements paragraph as an AC item")
    args = ap.parse_args()

    units = []
    for spec in args.unit:
        code, _, path = spec.partition("=")
        if not code or not path:
            ap.error(f"--unit must be CODE=PATH, got {spec!r}")
        p = Path(path)
        units.append((code, p if p.is_absolute() else args.cluster / p))

    consolidated_path = args.cluster / "consolidated_uoc.md"
    if not consolidated_path.is_file():
        print(f"ERROR: no consolidated_uoc.md at {consolidated_path}", file=sys.stderr)
        return 2

    try:
        expected = build_inventory(units, args.assessor_ac)
    except (ValueError, OSError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    consolidated = consolidated_path.read_text(encoding="utf-8")
    found = [" ".join(r) for r in ref.find_all(ref.strip_code_spans(consolidated))]
    counts = Counter(found)
    found_set = set(found)

    missing = sorted(set(expected) - found_set)
    unexpected = sorted(found_set - set(expected))
    duplicated = sorted((r, c) for r, c in counts.items() if c > 1)

    # Every item present under the right reference must also still say what the source says.
    blocks = item_blocks(consolidated)
    mistranscribed = []
    for r in sorted(set(expected) & found_set):
        block = blocks.get(r)
        if block is None:
            mistranscribed.append((r, "no item line carries this reference (cited in prose only)"))
        elif item_words(block) != item_words(expected[r]):
            mistranscribed.append((r, "text differs from the source unit"))

    print(f"Cluster:          {args.cluster.name}")
    print(f"Units:            {', '.join(u for u, _ in units)}")
    print(f"Assessor-AC mode: {'on' if args.assessor_ac else 'off'}")
    print(f"Expected items:   {len(expected)}")
    print(f"Found references: {len(found)} ({len(found_set)} unique)")
    print()

    if missing:
        print(f"MISSING ({len(missing)}):")
        for r in missing:
            print(f"  - {r}")
        print()

    if unexpected:
        print(f"UNEXPECTED ({len(unexpected)}):")
        for r in unexpected:
            print(f"  - {r}  (count={counts[r]})")
        print()

    if duplicated:
        print(f"DUPLICATED ({len(duplicated)}):")
        for r, c in duplicated:
            print(f"  - {r}  ({c} times)")
        print()

    if mistranscribed:
        print(f"MISTRANSCRIBED ({len(mistranscribed)}):")
        for r, why in mistranscribed:
            print(f"  - {r}  ({why})")
            print(f"      source: {' '.join(item_words(expected[r]))[:160]}")
            if r in blocks:
                print(f"      doc:    {' '.join(item_words(blocks[r]))[:160]}")
        print()

    if missing or unexpected or duplicated or mistranscribed:
        print("RESULT: FAIL")
        return 1

    print("RESULT: PASS — every expected item appears exactly once, verbatim, nothing extra.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
