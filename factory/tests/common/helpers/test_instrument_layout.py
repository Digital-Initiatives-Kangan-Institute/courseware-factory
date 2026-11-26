"""Cases HIL-01 .. HIL-17 — factory/docs/test-plan.md.

Covers common/helpers/instrument_layout.py: turning an instrument's flat content into navigable layout.
Body text uses the test institution pack's BODY_STYLE (tests/_fixtures/institution.py).
"""
from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

import instrument_layout as IL
from institution import BODY_STYLE

URL = "https://example.test/page"


def _texts(doc):
    return [p.text for p in doc.paragraphs]


def _link(paragraph):
    return paragraph._p.find(qn("w:hyperlink"))


def _link_target(paragraph):
    return paragraph.part.rels[_link(paragraph).get(qn("r:id"))].target_ref


# --- add_hyperlink (HIL-01 .. HIL-02) --------------------------------------

def test_hyperlink_targets_the_url_externally():
    """HIL-01"""
    p = Document().add_paragraph()
    IL.add_hyperlink(p, "the site", URL)
    rel = p.part.rels[_link(p).get(qn("r:id"))]
    assert rel.target_ref == URL and rel.is_external
    assert _link(p).find(qn("w:r")).find(qn("w:t")).text == "the site"


def test_hyperlink_is_underlined_link_blue_and_sized():
    """HIL-02"""
    p = Document().add_paragraph()
    IL.add_hyperlink(p, "x", URL, size_pt=9)
    props = _link(p).find(qn("w:r")).find(qn("w:rPr"))
    assert props.find(qn("w:u")).get(qn("w:val")) == "single"
    assert props.find(qn("w:color")).get(qn("w:val")) == IL.LINK_BLUE
    assert props.find(qn("w:sz")).get(qn("w:val")) == "18"   # half-points


# --- render_prose (HIL-03 .. HIL-06) ---------------------------------------

def test_item_entry_bolds_its_lead_in():
    """HIL-03"""
    doc = Document()
    IL.render_prose(doc, [("Part A — the business case", "item")])
    runs = doc.paragraphs[-1].runs
    assert [r.text for r in runs] == ["• ", "Part A", " — the business case"]
    assert runs[1].bold is True


def test_bullet_entry_is_a_plain_bulleted_line():
    """HIL-04"""
    doc = Document()
    IL.render_prose(doc, [("Bring your notes", "bullet")])
    p = doc.paragraphs[-1]
    assert p.text == "• Bring your notes"
    assert not any(r.bold for r in p.runs)


def test_link_entry_is_a_bulleted_clickable_link():
    """HIL-05"""
    doc = Document()
    IL.render_prose(doc, [("the intranet", f"link|{URL}")])
    p = doc.paragraphs[-1]
    assert p.runs[0].text == "• "
    assert _link_target(p) == URL


def test_other_style_is_a_paragraph_in_that_style():
    """HIL-06"""
    doc = Document()
    IL.render_prose(doc, [("Instructions", "Heading 2"), ("Read carefully.", "Normal")])
    heading, body = doc.paragraphs[-2], doc.paragraphs[-1]
    assert heading.style.name == "Heading 2" and heading.paragraph_format.space_before == Pt(12)
    assert body.style.name == "Normal" and body.paragraph_format.space_after == Pt(8)


# --- set_cell_rich (HIL-07 .. HIL-08) --------------------------------------

def test_cell_content_is_replaced_keeping_its_style():
    """HIL-07"""
    cell = Document().add_table(rows=1, cols=1).cell(0, 0)
    cell.paragraphs[0].style = "Body Text"
    cell.paragraphs[0].add_run("old text")
    cell.add_paragraph("old second paragraph")
    IL.set_cell_rich(cell, [("new text", "p")])
    assert [p.text for p in cell.paragraphs] == ["new text"]
    assert cell.paragraphs[0].style.name == "Body Text"


def test_cell_blocks_render_by_kind():
    """HIL-08"""
    cell = Document().add_table(rows=1, cols=1).cell(0, 0)
    IL.set_cell_rich(cell, [("Steps", "h"), ("Open the console", "b"), ("the guide", f"link|{URL}")])
    head, bullet, link = cell.paragraphs
    assert head.runs[0].bold is True and head.text == "Steps"
    assert bullet.text == "• Open the console"
    assert _link_target(link) == URL


# --- render_benchmark (HIL-09 .. HIL-13) -----------------------------------

def _bench(blocks, tables=None):
    doc = Document()
    IL.render_benchmark(doc, blocks, lambda d, rows: tables.append(rows), {"h": "Heading 1"})
    return doc


def test_numbered_lines_become_headings():
    """HIL-09"""
    doc = _bench([("p", "3. Marking the design"), ("p", "7.1 Benchmark answer")])
    assert [p.style.name for p in doc.paragraphs[-2:]] == ["Heading 2", "Heading 3"]


def test_uoc_evidenced_line_is_muted_italic_small():
    """HIL-10"""
    run = _bench([("p", "UoC evidenced: [ICTCLD502 PC 2.1]")]).paragraphs[-1].runs[0]
    assert run.italic is True and run.font.size == Pt(9)
    assert run.font.color.rgb == RGBColor(0x59, 0x59, 0x59)


def test_nys_line_has_a_bold_lead_in():
    """HIL-11"""
    runs = _bench([("p", "NYS: the design has a single point of failure")]).paragraphs[-1].runs
    assert [r.text for r in runs] == ["NYS: ", "the design has a single point of failure"]
    assert runs[0].bold is True and not runs[1].bold


def test_label_line_bullets_what_follows():
    """HIL-12"""
    doc = _bench([("p", "Satisfactory when:"), ("p", "two AZs are used"), ("p", "health checks pass")])
    label, *rest = doc.paragraphs[-3:]
    assert label.runs[0].bold is True
    assert [p.text for p in rest] == ["• two AZs are used", "• health checks pass"]


def test_table_block_is_handed_over_and_ends_bulleting():
    """HIL-13"""
    tables = []
    doc = _bench([("p", "Criteria:"), ("tbl", [["A1", "Yes"]]), ("p", "after the table")], tables)
    assert tables == [[["A1", "Yes"]]]
    assert doc.paragraphs[-1].text == "after the table"


# --- render_flat_prose (HIL-14 .. HIL-16) ----------------------------------

def test_heading_flag_decides_bulleting():
    """HIL-14"""
    doc = Document()
    IL.render_flat_prose(doc, ["What to submit", "your workbook", "About this task", "It is individual."],
                         {"What to submit": True, "About this task": False})
    assert [p.style.name for p in doc.paragraphs if p.text in ("What to submit", "About this task")] == [
        "Heading 2", "Heading 2"]
    assert "• your workbook" in _texts(doc)
    assert "It is individual." in _texts(doc)


def test_section_and_appendix_lines_have_a_bold_lead():
    """HIL-15"""
    doc = Document()
    IL.render_flat_prose(doc, ["§4 Recovery objectives", "Appendix B — the runbook"], {})
    for p, lead in zip(doc.paragraphs[-2:], ["§4", "Appendix"]):
        assert p.runs[0].text == "• " and p.runs[1].text == lead and p.runs[1].bold is True


def test_link_tuple_is_a_bulleted_clickable_link():
    """HIL-16"""
    doc = Document()
    IL.render_flat_prose(doc, [("the intranet", f"link|{URL}")], {})
    assert _link_target(doc.paragraphs[-1]) == URL


# --- the institution seam (HIL-17) -----------------------------------------

def test_body_text_uses_the_institution_body_style():
    """HIL-17"""
    doc = Document()
    IL.render_flat_prose(doc, ["Plain body text."], {})
    IL.render_prose(doc, [("A bullet", "bullet")])
    assert {p.style.name for p in doc.paragraphs[-2:]} == {BODY_STYLE}
