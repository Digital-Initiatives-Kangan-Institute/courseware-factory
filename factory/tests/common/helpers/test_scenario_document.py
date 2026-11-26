"""Cases HSD-01 .. HSD-03 — factory/docs/test-plan.md.

Covers common/helpers/scenario_document.py."""


from docx import Document
from docx.shared import Pt

from scenario_document import configure_styles, build_header_footer, wordmark
from brand import FONT, TEAL, TERRACOTTA, DISCLOSURE, ORG_NAME, ORG_WORDMARK


def test_configure_styles_sets_normal_and_title():
    """HSD-01"""
    doc = Document()
    configure_styles(doc)
    assert doc.styles["Normal"].font.name == FONT
    assert doc.styles["Normal"].font.size == Pt(10.5)
    assert str(doc.styles["Title"].font.color.rgb) == TEAL


def test_wordmark_two_runs_branded():
    """HSD-02"""
    p = Document().add_paragraph()
    wordmark(p)
    assert [r.text for r in p.runs] == list(ORG_WORDMARK)
    assert str(p.runs[0].font.color.rgb) == TEAL
    assert str(p.runs[1].font.color.rgb) == TERRACOTTA


def test_header_footer_disclosure_and_page_field():
    """HSD-03"""
    doc = Document()
    section = doc.sections[0]
    build_header_footer(section)
    assert DISCLOSURE in section.header.paragraphs[0].text
    assert ORG_NAME in section.footer.paragraphs[0].text
