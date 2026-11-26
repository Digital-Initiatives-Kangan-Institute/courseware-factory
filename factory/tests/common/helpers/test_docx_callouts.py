"""Cases HDCO-01 .. HDCO-02 — factory/docs/test-plan.md.

Covers common/helpers/docx_callouts.py."""


from docx import Document
from docx.oxml.ns import qn

from docx_callouts import add_applicability_note, add_convention_box
from brand import TERRACOTTA, CREAM, TEAL


def test_applicability_note_text_and_colour():
    """HDCO-01"""
    p = add_applicability_note(Document(), "high-availability deployments")
    r = p.runs[0]
    assert r.text.startswith("Applicability: complete for high-availability deployments")
    assert r.italic is True
    assert str(r.font.color.rgb) == TERRACOTTA


def test_convention_box_shaded_cell_and_bold_head():
    """HDCO-02"""
    t = add_convention_box(Document(), [("Convention", "use ISO dates"), ("Tip", "")])
    cell = t.rows[0].cells[0]
    assert cell._tc.tcPr.find(qn("w:shd")).get(qn("w:fill")) == CREAM
    head_run = cell.paragraphs[0].runs[0]
    assert head_run.text == "Convention" and head_run.bold is True
    assert str(head_run.font.color.rgb) == TEAL
