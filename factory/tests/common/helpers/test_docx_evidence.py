"""Cases HDEV-01 .. HDEV-02 — factory/docs/test-plan.md.

Covers common/helpers/docx_evidence.py."""


from docx import Document
from docx.shared import Pt

from docx_evidence import (
    add_not_applicable, add_described_evidence,
    NOT_APPLICABLE_FONT_SIZE_PT, EVIDENCE_FONT_SIZE_PT,
)
from brand import TERRACOTTA, TEAL, GREY


def test_not_applicable_text_bold_terracotta():
    """HDEV-01"""
    p = add_not_applicable(Document(), "deferred to AT3 hardening")
    r = p.runs[0]
    assert r.text == "Not applicable — deferred to AT3 hardening"
    assert r.bold is True
    assert r.font.size == Pt(NOT_APPLICABLE_FONT_SIZE_PT)
    assert str(r.font.color.rgb) == TERRACOTTA


def test_described_evidence_tag_and_desc():
    """HDEV-02"""
    p = add_described_evidence(Document(), "SCREENSHOT", "should show CREATE_COMPLETE")
    tag, desc = p.runs[0], p.runs[1]
    assert tag.text == "[SCREENSHOT] " and tag.bold is True
    assert str(tag.font.color.rgb) == TEAL
    assert desc.text == "— should show CREATE_COMPLETE" and desc.italic is True
    assert str(desc.font.color.rgb) == GREY
    assert desc.font.size == Pt(EVIDENCE_FONT_SIZE_PT)
