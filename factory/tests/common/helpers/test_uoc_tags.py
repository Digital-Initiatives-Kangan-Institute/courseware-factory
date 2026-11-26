"""Cases HUT-01 .. HUT-02 — factory/docs/test-plan.md.

Covers common/helpers/uoc_tags.py."""


from docx import Document
from docx.shared import Pt

from uoc_tags import add_uoc_evidence_tag, UOC_TAG_FONT_SIZE_PT
from brand import TEAL


def test_evidence_tag_prefixes_text():
    """HUT-01"""
    p = add_uoc_evidence_tag(Document(), "[ICTCLD401 PC 4.3]")
    assert p.runs[0].text == "Evidences: [ICTCLD401 PC 4.3]"


def test_evidence_tag_is_small_italic_teal():
    """HUT-02"""
    run = add_uoc_evidence_tag(Document(), "x").runs[0]
    assert run.italic is True
    assert run.font.size == Pt(UOC_TAG_FONT_SIZE_PT)
    assert str(run.font.color.rgb) == TEAL
