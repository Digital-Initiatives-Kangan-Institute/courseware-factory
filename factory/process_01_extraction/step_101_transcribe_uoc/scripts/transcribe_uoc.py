#!/usr/bin/env python3
"""Transcribe a .docx unit-of-competency document into verbatim Markdown.

The content is taken **straight from the Word runs** via `docx_text` — never retyped — so the
transcription is faithful by construction: no paraphrasing, no omission, no "tidying". The only thing
this script reasons about is STRUCTURE, from the source paragraph styles:

    Title / Heading1..6   -> '# ' .. '###### ' headings
    ListBullet / numbered -> '- ' bullets, two spaces of indent per nesting level
    table (w:tbl)         -> a Markdown table; multi-paragraph cells joined with '<br>'
    everything else       -> a plain paragraph
    empty / spacer paras  -> dropped

So the failure mode is never "a word changed" — at most "a heading or bullet was mis-shaped", which the
step's gate catches and which is fixed once, here, for every future unit.

Page furniture (headers, footers, page numbers) is excluded by construction: `docx_text` opens only
`word/document.xml`, and those live in separate zip parts.

The gate `validate_uoc.py` reads the same source through the same `docx_text`, then compares. Its
list-shape check is the part that stays independent of this script, so a flattened bullet is caught
even though both sides agree on the words.

Behaviour is specified by cases TU-01 .. TU-30 in factory/docs/test-plan.md. The full style mapping
observed across the ICT and BSB corpus, and the behaviours that look like bugs and are not, are in the
companion `transcribe_uoc.md` beside this file.

stdlib only — runs anywhere with python3, no virtualenv.

Usage:  python3 transcribe_uoc.py <source.docx> [output.md]
        (writes to stdout if no output path is given)
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "common" / "helpers"))

import docx_text as dx  # noqa: E402

W = dx.W


def inline(text: str) -> str:
    """Extracted text as a single Markdown line.

    Internal line breaks become <br>. Runs of horizontal whitespace (stray double spaces and tabs
    left in the source Word doc) collapse to a single space — this only ever touches spacing, never
    a word, so the verbatim word sequence the gate checks is unchanged while the output stays clean.
    """
    return re.sub(r"[ \t]+", " ", text).replace("\n", "<br>").strip()


def heading_level(style: str | None) -> int | None:
    """The heading depth this style denotes, or None when it is not a heading.

    Title and Heading1 are both top-level: the UoC documents use Title for the unit name.
    """
    if not style:
        return None
    if style == "Title":
        return 1
    m = re.fullmatch(r"Heading([1-6])", style)
    return int(m.group(1)) if m else None


def list_level(para, style: str | None) -> int | None:
    """The 0-based nesting depth if this paragraph is a list item, else None.

    Depth comes from the style-name suffix the ICT UoC documents use (ListBullet -> 0,
    ListBullet2 -> 1, ...), falling back to a numbered list's own indent level (w:numPr/w:ilvl)
    where there is no List* style to read. The suffix is 1-based and the depth is 0-based because
    the consolidation step counts only top-level bullets and treats sub-bullets as part of their
    parent item.
    """
    if style:
        m = re.fullmatch(r"List(?:Bullet|Number|Paragraph)(\d*)", style)
        if m:
            return int(m.group(1)) - 1 if m.group(1) else 0

    pPr = para.find(f"{W}pPr")
    if pPr is not None:
        numPr = pPr.find(f"{W}numPr")
        if numPr is not None:
            ilvl = numPr.find(f"{W}ilvl")
            return int(ilvl.get(f"{W}val")) if ilvl is not None else 0
    return None


def cell_md(cell) -> str:
    """A table cell's content: its non-empty paragraphs joined with <br>.

    Empty paragraphs are dropped rather than rendered, so a spacer inside a cell cannot leave a
    dangling separator in the middle of the markdown cell.
    """
    paras = [inline(text) for text in dx.cell_paras(cell)]
    return "<br>".join(text for text in paras if text)


def render_table(tbl) -> str:
    """A Word table as a Markdown table, with the separator under the first row."""
    out = []
    for index, row in enumerate(tbl.findall(f"{W}tr")):
        cells = [cell_md(cell) for cell in row.findall(f"{W}tc")]
        out.append("| " + " | ".join(cells) + " |")
        if index == 0:
            out.append("| " + " | ".join("---" for _ in cells) + " |")
    return "\n".join(out)


def transcribe(docx_path: Path) -> str:
    """The whole document as Markdown, blocks separated by a blank line.

    Consecutive bullets accumulate into one tight list; anything else — a heading, a table, an
    empty spacer paragraph — closes it, so a list block in the output means a run of bullets in
    the source.
    """
    body = dx.body(docx_path)
    if body is None:
        return ""

    blocks: list[str] = []
    listbuf: list[str] = []

    def flush():
        if listbuf:
            blocks.append("\n".join(listbuf))
            listbuf.clear()

    for kind, elem in dx.iter_blocks(body):
        if kind == "tbl":
            flush()
            blocks.append(render_table(elem))
            continue

        style = dx.para_style(elem)
        text = inline(dx.para_text(elem))
        if not text:                        # spacer paragraph — also ends any open list
            flush()
            continue

        level = heading_level(style)
        depth = list_level(elem, style)
        if level is not None:
            flush()
            blocks.append("#" * level + " " + text)
        elif depth is not None:
            listbuf.append("  " * depth + "- " + text)
        else:
            flush()
            blocks.append(text)

    flush()
    return "\n\n".join(blocks) + "\n"


def main() -> int:
    args = sys.argv[1:]
    if not 1 <= len(args) <= 2:
        print("Usage: transcribe_uoc.py <source.docx> [output.md]", file=sys.stderr)
        return 2

    markdown = transcribe(Path(args[0]))
    if len(args) == 2:
        out = Path(args[1])
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(markdown, encoding="utf-8")
        print(f"Wrote {out}", file=sys.stderr)
    else:
        sys.stdout.write(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
