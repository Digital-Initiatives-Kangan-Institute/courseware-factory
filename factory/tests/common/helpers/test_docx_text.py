"""Cases HDX-01 .. HDX-23 — factory/docs/test-plan.md.

The one docx reader both step-01 scripts go through. Element coverage carries most of the file: a type
this module ignores is lost from the transcription and from the text the transcription is compared
against at the same time, so the gate agrees with itself over dropped content. Fixtures are hand-written
Word XML (`docx_fixtures`), never the transcriber's own output.
"""
import docx_text as D
from docx_fixtures import WNS, make_docx, make_docx_raw, p, raw_p, sdt, tbl, wrap

NO_BODY = f'<w:document xmlns:w="{WNS}"></w:document>'

W = D.W


def only_para(tmp_path, block):
    """The first paragraph of a one-block document — the subject of the para_* cases."""
    return D.body(make_docx(tmp_path, [block])).find(f"{W}p")


# ---------------------------------------------------------------------------
# body() — reaching the document body
# ---------------------------------------------------------------------------

def test_body_is_returned_from_a_docx(tmp_path):
    """HDX-01"""
    assert D.body(make_docx(tmp_path, [p("Configure cloud services")])) is not None


def test_document_without_a_body_returns_none(tmp_path):
    """HDX-02"""
    assert D.body(make_docx_raw(tmp_path, NO_BODY)) is None


def test_header_and_footer_parts_are_not_read(tmp_path):
    """HDX-03 — page furniture is excluded by construction, not by filtering."""
    docx = make_docx(tmp_path, [p("Element 1")], furniture=True)
    text = D.docx_to_text(docx)
    assert "Element 1" in text
    assert "Approved Page" not in text
    assert "IT Training Package" not in text


# ---------------------------------------------------------------------------
# para_text() — every element that carries text
# ---------------------------------------------------------------------------

def test_text_runs_concatenate_in_source_order(tmp_path):
    """HDX-04"""
    para = only_para(tmp_path, raw_p("<w:t>Confirm </w:t><w:t>requirements</w:t>"))
    assert D.para_text(para) == "Confirm requirements"


def test_tab_becomes_a_tab_character(tmp_path):
    """HDX-05"""
    assert D.para_text(only_para(tmp_path, p("1.1\tConfirm"))) == "1.1\tConfirm"


def test_break_becomes_a_newline(tmp_path):
    """HDX-06"""
    assert D.para_text(only_para(tmp_path, p("first\nsecond"))) == "first\nsecond"


def test_carriage_return_becomes_a_newline(tmp_path):
    """HDX-07 — the validator handles w:cr today and the transcriber does not."""
    para = only_para(tmp_path, raw_p("<w:t>first</w:t><w:cr/><w:t>second</w:t>"))
    assert D.para_text(para) == "first\nsecond"


def test_symbol_renders_its_char_attribute(tmp_path):
    """HDX-08 — a symbol run holds its character in an attribute, not in w:t."""
    para = only_para(tmp_path, raw_p('<w:t>bullet </w:t><w:sym w:font="Symbol" w:char="F0B7"/>'))
    assert D.para_text(para) == "bullet "


def test_non_breaking_hyphen_renders_as_a_hyphen(tmp_path):
    """HDX-09"""
    para = only_para(tmp_path, raw_p("<w:t>cloud</w:t><w:noBreakHyphen/><w:t>based</w:t>"))
    assert D.para_text(para) == "cloud‑based"


def test_empty_text_element_contributes_an_empty_string(tmp_path):
    """HDX-10 — <w:t/> has node.text of None."""
    para = only_para(tmp_path, raw_p("<w:t/><w:t>Element</w:t>"))
    assert D.para_text(para) == "Element"


def test_text_inside_a_wrapper_element_is_found(tmp_path):
    """HDX-11 — a run nested in a hyperlink is still the paragraph's text."""
    block = f"<w:p><w:hyperlink>{'<w:r><w:t>training.gov.au</w:t></w:r>'}</w:hyperlink></w:p>"
    assert D.para_text(only_para(tmp_path, block)) == "training.gov.au"


# ---------------------------------------------------------------------------
# para_style() — the structure classifier's input
# ---------------------------------------------------------------------------

def test_paragraph_style_value_is_returned(tmp_path):
    """HDX-12"""
    assert D.para_style(only_para(tmp_path, p("Foundation Skills", style="Heading2"))) == "Heading2"


def test_paragraph_without_properties_has_no_style(tmp_path):
    """HDX-13"""
    assert D.para_style(only_para(tmp_path, p("plain prose"))) is None


def test_properties_without_a_style_has_no_style(tmp_path):
    """HDX-14"""
    block = "<w:p><w:pPr><w:spacing w:after=\"120\"/></w:pPr><w:r><w:t>x</w:t></w:r></w:p>"
    assert D.para_style(only_para(tmp_path, block)) is None


# ---------------------------------------------------------------------------
# iter_blocks() — document order, through containers
# ---------------------------------------------------------------------------

def test_blocks_are_tagged_and_in_document_order(tmp_path):
    """HDX-15"""
    docx = make_docx(tmp_path, [p("before"), tbl([["a", "b"]]), p("after")])
    assert [kind for kind, _ in D.iter_blocks(D.body(docx))] == ["p", "tbl", "p"]


def test_content_inside_an_sdt_is_yielded_in_place(tmp_path):
    """HDX-16"""
    docx = make_docx(tmp_path, [p("before"), sdt(p("inside")), p("after")])
    texts = [D.para_text(e) for kind, e in D.iter_blocks(D.body(docx)) if kind == "p"]
    assert texts == ["before", "inside", "after"]


def test_blocks_inside_an_unrecognised_container_are_yielded(tmp_path):
    """HDX-17 — the transcriber walks past these today; a wrapper must not hide content."""
    docx = make_docx(tmp_path, [p("before"), wrap("customXml", p("inside")), p("after")])
    texts = [D.para_text(e) for kind, e in D.iter_blocks(D.body(docx)) if kind == "p"]
    assert texts == ["before", "inside", "after"]


def test_a_non_block_element_contributes_nothing(tmp_path):
    """HDX-18 — every real body ends with a w:sectPr."""
    docx = make_docx(tmp_path, [p("Element 1"), "<w:sectPr><w:pgSz w:w=\"11906\"/></w:sectPr>"])
    assert [kind for kind, _ in D.iter_blocks(D.body(docx))] == ["p"]


# ---------------------------------------------------------------------------
# cell_paras() and docx_to_text() — tables, and the flat extraction
# ---------------------------------------------------------------------------

def test_cell_paragraphs_are_returned_in_order(tmp_path):
    """HDX-19"""
    docx = make_docx(tmp_path, [tbl([["1.1 Confirm\n1.2 Identify"]])])
    cell = D.body(docx).find(f"{W}tbl").find(f"{W}tr").find(f"{W}tc")
    assert D.cell_paras(cell) == ["1.1 Confirm", "1.2 Identify"]


def test_paragraphs_are_joined_by_newline_in_document_order(tmp_path):
    """HDX-20"""
    docx = make_docx(tmp_path, [p("Performance Evidence"), p("The candidate must")])
    assert D.docx_to_text(docx) == "Performance Evidence\nThe candidate must"


def test_each_table_cell_contributes_its_own_entry(tmp_path):
    """HDX-21"""
    docx = make_docx(tmp_path, [tbl([["Element", "Performance Criteria"], ["1.", "2."]])])
    assert D.docx_to_text(docx).splitlines() == ["Element", "Performance Criteria", "1.", "2."]


def test_multi_paragraph_cell_joins_with_a_newline(tmp_path):
    """HDX-22 — lines up with the <br> the transcription uses inside a cell."""
    docx = make_docx(tmp_path, [tbl([["1.1 Confirm\n1.2 Identify"]])])
    assert D.docx_to_text(docx) == "1.1 Confirm\n1.2 Identify"


def test_document_without_a_body_yields_empty_text(tmp_path):
    """HDX-23"""
    assert D.docx_to_text(make_docx_raw(tmp_path, NO_BODY)) == ""
