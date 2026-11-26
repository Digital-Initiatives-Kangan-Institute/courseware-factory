"""Cases HDBT-01 .. HDBT-08 — factory/docs/test-plan.md.

Covers common/helpers/docx_body_text.py."""


from docx import Document
from docx.shared import Pt

from docx_body_text import (
    add_body_paragraph,
    add_bullet_list,
    add_guidance_text,
    add_response_placeholder,
    BODY_FONT_SIZE_PT,
    GUIDANCE_FONT_SIZE_PT,
)
from brand import GREY


def test_guidance_text_is_italic_grey_at_guidance_size():
    """HDBT-01"""
    p = add_guidance_text(Document(), "Write this last.")
    run = p.runs[0]
    assert run.italic is True
    assert run.font.size == Pt(GUIDANCE_FONT_SIZE_PT)
    assert str(run.font.color.rgb) == GREY


def test_response_placeholder_default_label_italic():
    """HDBT-02"""
    p = add_response_placeholder(Document())
    assert p.runs[0].text == "[ Write your response here ]"
    assert p.runs[0].italic is True


def test_body_paragraph_text_and_size():
    """HDBT-03"""
    p = add_body_paragraph(Document(), "Hello world")
    assert p.text == "Hello world"
    assert p.runs[0].font.size == Pt(BODY_FONT_SIZE_PT)


def test_body_paragraph_returns_one_paragraph():
    """HDBT-04"""
    doc = Document()
    before = len(doc.paragraphs)
    add_body_paragraph(doc, "x")
    assert len(doc.paragraphs) == before + 1


def test_one_paragraph_per_item():
    """HDBT-05"""
    paras = add_bullet_list(Document(), ["First", "Second", "Third"])
    assert len(paras) == 3


def test_text_and_bullet_style():
    """HDBT-06"""
    paras = add_bullet_list(Document(), ["Alpha", "Beta"])
    assert [p.text for p in paras] == ["Alpha", "Beta"]
    assert all(p.style.name == "List Bullet" for p in paras)


def test_body_font_size():
    """HDBT-07"""
    paras = add_bullet_list(Document(), ["x"])
    assert paras[0].runs[0].font.size == Pt(BODY_FONT_SIZE_PT)


def test_empty_is_noop():
    """HDBT-08"""
    assert add_bullet_list(Document(), []) == []
