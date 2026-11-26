"""Word-XML builders: a .docx assembled from literal strings.

**Independence.** Every fixture here is written by hand. Nothing is produced by the transcriber, because
`docx_text` is the module the transcriber and the validator BOTH read through — a reader tested against
its own consumer's output would only prove the two agree with each other. These strings are the ground
truth the reader is checked against.

Only the zip parts under test are written (`word/document.xml`, plus header/footer parts where a case
needs them): enough for a zip-reading extractor, not a Word-openable document.
"""
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

WNS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

DOC_OPEN = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    f'<w:document xmlns:w="{WNS}">'
    "<w:body>"
)
DOC_CLOSE = "</w:body></w:document>"


def runs(text: str) -> str:
    """Text -> run XML. A tab character becomes ``<w:tab/>``, a newline becomes ``<w:br/>``."""
    out = []
    for i, line in enumerate(text.split("\n")):
        if i:
            out.append("<w:br/>")
        for j, chunk in enumerate(line.split("\t")):
            if j:
                out.append("<w:tab/>")
            if chunk:
                out.append(f'<w:t xml:space="preserve">{escape(chunk)}</w:t>')
    return f"<w:r>{''.join(out)}</w:r>"


def p(text: str, style: str | None = None) -> str:
    """A paragraph, optionally carrying a paragraph style."""
    pPr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    return f"<w:p>{pPr}{runs(text)}</w:p>"


def h(level: int, text: str) -> str:
    """A heading paragraph."""
    return p(text, style=f"Heading{level}")


def bullet(text: str, depth: int = 0) -> str:
    """A list paragraph. Depth comes from the style suffix: ListBullet, ListBullet2, ListBullet3."""
    return p(text, style="ListBullet" + (str(depth + 1) if depth else ""))


def raw_p(inner: str) -> str:
    """A paragraph whose run XML is supplied verbatim — for elements ``runs`` cannot express."""
    return f"<w:p><w:r>{inner}</w:r></w:p>"


def tbl(rows: list[list[str]], cell_style: str | None = None) -> str:
    """A table. A newline inside a cell starts a new paragraph in that cell."""
    out = ["<w:tbl>"]
    for row in rows:
        out.append("<w:tr>")
        for cell in row:
            paras = "".join(p(part, style=cell_style) for part in cell.split("\n"))
            out.append(f"<w:tc>{paras}</w:tc>")
        out.append("</w:tr>")
    out.append("</w:tbl>")
    return "".join(out)


def sdt(*blocks: str) -> str:
    """A structured-document tag wrapping body-level blocks — Word's content-control container."""
    return f"<w:sdt><w:sdtContent>{''.join(blocks)}</w:sdtContent></w:sdt>"


def wrap(tag: str, *blocks: str) -> str:
    """Body-level blocks inside an arbitrary container, for the unrecognised-wrapper case."""
    return f"<w:{tag}>{''.join(blocks)}</w:{tag}>"


def make_docx(tmp_path: Path, blocks: list[str], furniture: bool = False,
              name: str = "unit.docx") -> Path:
    """Zip the given body blocks into a .docx. ``furniture`` adds header/footer parts with content."""
    return _write(tmp_path, DOC_OPEN + "".join(blocks) + DOC_CLOSE, furniture, name)


def make_docx_raw(tmp_path: Path, document_xml: str, name: str = "unit.docx") -> Path:
    """Zip a complete ``word/document.xml`` supplied verbatim — for a document with no body at all."""
    return _write(tmp_path, document_xml, False, name)


def _write(tmp_path: Path, document_xml: str, furniture: bool, name: str) -> Path:
    path = tmp_path / name
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("word/document.xml", document_xml)
        if furniture:
            for part, text in (
                ("word/header1.xml", "ICTCLD501 Configure cloud services"),
                ("word/footer1.xml", "Approved Page 3 of 5 IT Training Package"),
            ):
                z.writestr(
                    part,
                    DOC_OPEN.replace("w:document", "w:hdr") + p(text) + "</w:body></w:hdr>",
                )
    return path
