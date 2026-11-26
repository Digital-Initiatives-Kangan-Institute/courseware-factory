"""Reading text and block structure out of a .docx body.

The **one** reader for step 01: the transcriber goes through it to build the markdown, and the validator
goes through it to say independently what the source document contains. Two consumers, one
implementation — a second copy is how an element type ends up handled on one side and not the other,
which is exactly the fault the gate cannot see (the character would be missing from the transcription
AND from the text it is compared against, so the two would agree over dropped content).

The validator's list-shape check is deliberately NOT built on this module: reading bullet nesting from
paragraph styles is a genuinely independent second opinion on structure, and folding it in here would
cost that independence.

Reads only `word/document.xml`, so page furniture — headers, footers, page numbers — is excluded by
construction rather than by filtering: those live in separate zip parts that are never opened.

Behaviour is specified by cases HDX-01 .. HDX-23 in factory/docs/test-plan.md.
"""
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def body(docx_path: Path):
    """The `<w:body>` element of a .docx, or None when the document has no body."""
    with zipfile.ZipFile(docx_path) as z:
        with z.open("word/document.xml") as f:
            tree = ET.parse(f)
    return tree.getroot().find(f"{W}body")


def para_text(para) -> str:
    """One paragraph's text, from every element that carries any.

    Walks descendants rather than direct children, so a run nested inside a hyperlink or other
    inline wrapper still contributes. Each branch below is a way Word stores something a reader
    would call text; anything missing here is silently lost from both sides of the gate.
    """
    parts = []
    for node in para.iter():
        tag = node.tag
        if tag == f"{W}t":
            parts.append(node.text or "")
        elif tag == f"{W}tab":
            parts.append("\t")
        elif tag in (f"{W}br", f"{W}cr"):
            parts.append("\n")
        elif tag == f"{W}sym":
            # A symbol run carries its character in an attribute, not in w:t.
            code = node.get(f"{W}char")
            if code:
                parts.append(chr(int(code, 16)))
        elif tag == f"{W}noBreakHyphen":
            parts.append("‑")  # folded to a plain hyphen by the cosmetic tier
    return "".join(parts)


def para_style(para) -> str | None:
    """The paragraph's `w:pStyle` value, or None when it has none."""
    pPr = para.find(f"{W}pPr")
    if pPr is None:
        return None
    style = pPr.find(f"{W}pStyle")
    return style.get(f"{W}val") if style is not None else None


def iter_blocks(parent):
    """Yield ``("p" | "tbl", element)`` in document order, descending through containers.

    Anything that is neither a paragraph nor a table is recursed into rather than skipped, so a
    content control (`w:sdt`) or any other wrapper cannot hide content from a caller. An element
    with no blocks beneath it — a `w:sectPr`, say — simply contributes nothing.
    """
    for child in parent:
        tag = child.tag
        if tag == f"{W}p":
            yield ("p", child)
        elif tag == f"{W}tbl":
            yield ("tbl", child)
        else:
            yield from iter_blocks(child)


def cell_paras(cell) -> list[str]:
    """A table cell's paragraphs, in order."""
    return [para_text(para) for para in cell.findall(f"{W}p")]


def docx_to_text(docx_path: Path) -> str:
    """The document's textual content in document order, paragraphs and table cells one per line.

    A cell's own paragraphs are joined with a newline, so a multi-paragraph cell lines up with the
    `<br>` the transcription uses in the same place.
    """
    root = body(docx_path)
    if root is None:
        return ""

    lines = []
    for kind, elem in iter_blocks(root):
        if kind == "p":
            lines.append(para_text(elem))
        else:
            for row in elem.findall(f"{W}tr"):
                for cell in row.findall(f"{W}tc"):
                    lines.append("\n".join(cell_paras(cell)))
    return "\n".join(lines)
