#!/usr/bin/env python3
"""Extract every PC / FS / PE / KE / AC from a cluster's transcribed UoC .md files as pre-tagged,
verbatim item lines — the faithful raw material for consolidation.

The point is the transcriber's, one step on: consolidation should ARRANGE items into topic groups,
never RETYPE them. This lifts each item's text straight from the (already validated) transcription
and stamps it with its source reference `[UNIT SECTION numbering]`, so the editorial step only moves
tagged lines around and can never drop, alter or mis-tag an item.

The itemisation and numbering rules are the ones the step's gate builds its expected set from — the
gate calls this module rather than carrying a second copy, because two mirrored parsers that must
agree are a maintenance hazard, not independent evidence. The independent check lives upstream at
Gate 01, where the .docx is the oracle.

  PC        the "N.N ..." entries in the Elements & Performance Criteria table
  FS        each row of the Foundation Skills table (skill name -> reference, description -> text)
  PE/KE/AC  top-level bullets numbered 1..N in source order, with the special case that a section
            whose ONLY top-level bullet ends in ':' is a parent whose immediate sub-bullets are the
            items. Nested sub-bullets under a normal item stay indented beneath it, as one item.
  the trailing "Assessors of this unit must satisfy..." paragraph is emitted as one extra AC item
  only when --assessor-ac is given.

Behaviour is specified by cases IU-01 .. IU-30 in factory/docs/test-plan.md.

stdlib only.

Usage:
  inventory_uoc.py --unit CODE=path/to/UNIT.md [--unit CODE=path ...] [--assessor-ac]
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "common" / "helpers"))

import md_table  # noqa: E402

HEADING = re.compile(r"^#{1,6}\s")
TOP_BULLET = re.compile(r"^- ")
CHILD_BULLET = re.compile(r"^\s+- ")
CRITERION = re.compile(r"^(\d+\.\d+)\s")


def section_body(md: str, heading: str) -> str:
    """The text between a heading and the next heading, or the end of the document.

    The heading matches case-insensitively as a substring of a heading line at any level, which is
    the same rule `md_table` uses — so a section is found the same way whether its content is a
    table or a list of bullets.
    """
    lines = md.splitlines()
    needle = heading.lower()

    start = None
    for i, line in enumerate(lines):
        if HEADING.match(line) and needle in line.lower():
            start = i + 1
            break
    if start is None:
        return ""

    body = []
    for line in lines[start:]:
        if HEADING.match(line):
            break
        body.append(line)
    return "\n".join(body)


def parse_pcs(md: str):
    """[(num, 'N.N text'), ...] from the performance-criteria column.

    Only the second column is read: the first holds the element, which is a grouping label rather
    than an assessable item. One cell often carries several criteria separated by `<br>`, because
    that is how the transcriber renders a multi-paragraph Word cell.
    """
    out = []
    for cells, _line_no in md_table.rows_under_heading(md, "Elements and Performance Criteria"):
        if len(cells) < 2:
            continue
        for piece in cells[1].split("<br>"):
            piece = piece.strip()
            match = CRITERION.match(piece)
            if match:
                out.append((match.group(1), piece))
    return out


def parse_fs(md: str):
    """[(skill_name, description), ...] from the Foundation Skills table.

    A row with no skill name is a continuation of the row above it, not a new skill.
    """
    out = []
    for cells, _line_no in md_table.rows_under_heading(md, "Foundation Skills"):
        if len(cells) < 2 or not cells[0]:
            continue
        if cells[0].lower().startswith("skill"):        # the header row
            continue
        out.append((cells[0], cells[1]))
    return out


def parse_bullets(md: str, heading: str):
    """One list of markdown lines per item: the parent bullet plus any nested children.

    Non-bullet lines — intro paragraphs, blanks — are not items and are ignored.

    The special case: a section whose ONLY top-level bullet ends in ':' is a parent introducing the
    real items, so its immediate sub-bullets become the items (e.g. ICTICT517 PE). With a sibling
    present, a trailing colon is just punctuation.
    """
    blocks = []
    for line in section_body(md, heading).splitlines():
        if TOP_BULLET.match(line):
            blocks.append([line])
        elif CHILD_BULLET.match(line) and blocks:
            blocks[-1].append(line)

    if len(blocks) == 1 and blocks[0][0].rstrip().endswith(":"):
        return [[CHILD_BULLET.sub("- ", child)] for child in blocks[0][1:]]
    return blocks


def trailing_assessor_ac(md: str):
    """The 'Assessors of this unit must satisfy...' paragraph text, or None."""
    for line in section_body(md, "Assessment Conditions").splitlines():
        if line.strip().startswith("Assessors of this unit must"):
            return line.strip()
    return None


def emit_item(tag: str, parent_line: str, children=None) -> str:
    """One tagged item in house style: '- text [tag]' plus any indented child lines.

    The reference sits at the end of the parent line; nested sub-bullets follow it untagged, because
    they are part of this one item rather than items of their own.
    """
    text = TOP_BULLET.sub("", parent_line).strip()
    return "\n".join([f"- {text} [{tag}]", *(children or [])])


def inventory(code: str, md: str, assessor_ac: bool):
    """Yield ('## CODE — SECTION', [rendered item lines]) for each of the five sections.

    Every one of the five is assessable and mandatory in a training-package UoC, so a section that
    yields nothing is an extraction failure rather than an empty section — see the raise below.
    """
    sections = [
        (f"## {code} — Performance Criteria",
         [f"- {text} [{code} PC {num}]" for num, text in parse_pcs(md)]),
        (f"## {code} — Foundation Skills",
         [f"- **{name}** — {desc} [{code} FS {name}]" for name, desc in parse_fs(md)]),
    ]

    for sec, heading in (("PE", "Performance Evidence"), ("KE", "Knowledge Evidence")):
        blocks = parse_bullets(md, heading)
        sections.append((f"## {code} — {heading}",
                         [emit_item(f"{code} {sec} {i}", b[0], b[1:])
                          for i, b in enumerate(blocks, 1)]))

    blocks = parse_bullets(md, "Assessment Conditions")
    items = [emit_item(f"{code} AC {i}", b[0], b[1:]) for i, b in enumerate(blocks, 1)]
    if assessor_ac:
        paragraph = trailing_assessor_ac(md)
        if paragraph:
            items.append(f"- {paragraph} [{code} AC {len(blocks) + 1}]")
    sections.append((f"## {code} — Assessment Conditions", items))

    empty = [header.split(" — ", 1)[1] for header, items in sections if not items]
    if empty:
        # A silently empty section shrinks the item register without failing anything: the gate
        # builds its expected set by these same rules, so it would measure the consolidated doc
        # against a yardstick short by a whole section, and pass.
        raise ValueError(
            f"{code}: no items extracted from {', '.join(empty)}. The heading is missing or "
            f"renamed, or the items are not formatted as bullets/table rows.")

    yield from sections


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--unit", required=True, action="append", help="CODE=path/to/UNIT.md")
    ap.add_argument("--assessor-ac", action="store_true",
                    help="emit the trailing assessor-requirements paragraph as one extra AC item")
    args = ap.parse_args()

    out = []
    total = 0
    for spec in args.unit:
        code, _, path = spec.partition("=")
        if not code or not path:
            ap.error(f"--unit must be CODE=PATH, got {spec!r}")

        md = Path(path).read_text(encoding="utf-8")
        out.append(f"# {code}")
        try:
            sections = list(inventory(code, md, args.assessor_ac))
        except ValueError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 2

        for header, items in sections:
            out.append(header)
            out.extend(items)
            out.append("")
            total += len(items)

    sys.stdout.write("\n".join(out).rstrip() + "\n")
    print(f"\n<!-- {total} items extracted across {len(args.unit)} unit(s) -->", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
