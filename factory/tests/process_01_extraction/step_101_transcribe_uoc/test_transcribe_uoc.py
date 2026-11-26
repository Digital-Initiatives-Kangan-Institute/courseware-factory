"""Cases TU-01 .. TU-30 — factory/docs/test-plan.md.

The transcriber's own job is STRUCTURE: which style is a heading, which is a bullet, where a table
starts, and how those assemble into Markdown. Getting the text out of the .docx belongs to `docx_text`
and is covered by HDX-*, so nothing here re-tests extraction.

Fixtures are hand-written Word XML (`docx_fixtures`) — the transcriber is never fed its own output.
"""
import subprocess
import sys

import docx_text as D
import transcribe_uoc as T
from conftest import TRANSCRIBER
from docx_fixtures import WNS, make_docx, make_docx_raw, p, tbl

W = D.W
NO_BODY = f'<w:document xmlns:w="{WNS}"></w:document>'


def first_para(tmp_path, block):
    return D.body(make_docx(tmp_path, [block])).find(f"{W}p")


def first_table(tmp_path, rows):
    return D.body(make_docx(tmp_path, [tbl(rows)])).find(f"{W}tbl")


def numbered_p(text, ilvl=None):
    """A paragraph carrying a w:numPr but no List* style — Word's other way of saying 'bullet'."""
    level = f'<w:ilvl w:val="{ilvl}"/>' if ilvl is not None else ""
    return f"<w:p><w:pPr><w:numPr>{level}<w:numId w:val=\"3\"/></w:numPr></w:pPr>" \
           f"<w:r><w:t>{text}</w:t></w:r></w:p>"


def run_cli(*args):
    return subprocess.run([sys.executable, str(TRANSCRIBER), *map(str, args)],
                          capture_output=True, text=True)


# ---------------------------------------------------------------------------
# inline() — extracted text as one markdown line
# ---------------------------------------------------------------------------

def test_runs_of_whitespace_collapse_to_one_space():
    """TU-01 — only ever spacing, never a word, so the verbatim word sequence is unchanged."""
    assert T.inline("Confirm  cloud\t\tservice") == "Confirm cloud service"


def test_internal_line_break_becomes_br():
    """TU-02"""
    assert T.inline("1.1 Confirm\n1.2 Identify") == "1.1 Confirm<br>1.2 Identify"


def test_surrounding_whitespace_is_stripped():
    """TU-03"""
    assert T.inline("  Element 1  ") == "Element 1"


# ---------------------------------------------------------------------------
# heading_level()
# ---------------------------------------------------------------------------

def test_title_is_level_one():
    """TU-04"""
    assert T.heading_level("Title") == 1


def test_heading3_is_level_three():
    """TU-05"""
    assert T.heading_level("Heading3") == 3


def test_non_heading_style_yields_no_level():
    """TU-06"""
    assert T.heading_level("ListBullet") is None


def test_absent_style_yields_no_level():
    """TU-07"""
    assert T.heading_level(None) is None


# ---------------------------------------------------------------------------
# list_level()
# ---------------------------------------------------------------------------

def test_list_bullet_is_depth_zero(tmp_path):
    """TU-08"""
    para = first_para(tmp_path, p("configure two services", style="ListBullet"))
    assert T.list_level(para, "ListBullet") == 0


def test_list_bullet3_is_depth_two(tmp_path):
    """TU-09 — the style suffix is 1-based, the depth is 0-based."""
    para = first_para(tmp_path, p("a sub-point", style="ListBullet3"))
    assert T.list_level(para, "ListBullet3") == 2


def test_number_and_paragraph_are_list_styles(tmp_path):
    """TU-10"""
    para = first_para(tmp_path, p("step one", style="ListNumber"))
    assert T.list_level(para, "ListNumber") == 0
    assert T.list_level(para, "ListParagraph2") == 1


def test_depth_falls_back_to_the_numbering_level(tmp_path):
    """TU-11 — Word's other way of saying 'bullet', with no List* style to read."""
    para = first_para(tmp_path, numbered_p("document the configuration", ilvl=1))
    assert T.list_level(para, None) == 1


def test_numbering_without_a_level_is_depth_zero(tmp_path):
    """TU-12"""
    para = first_para(tmp_path, numbered_p("document the configuration"))
    assert T.list_level(para, None) == 0


def test_plain_paragraph_is_not_a_list_item(tmp_path):
    """TU-13"""
    para = first_para(tmp_path, p("The candidate must demonstrate"))
    assert T.list_level(para, None) is None


# ---------------------------------------------------------------------------
# cell_md() and render_table()
# ---------------------------------------------------------------------------

def test_cell_paragraphs_join_with_br(tmp_path):
    """TU-14"""
    cell = first_table(tmp_path, [["1.1 Confirm\n1.2 Identify"]]).find(f"{W}tr").find(f"{W}tc")
    assert T.cell_md(cell) == "1.1 Confirm<br>1.2 Identify"


def test_empty_paragraph_in_a_cell_is_dropped(tmp_path):
    """TU-15 — an empty source paragraph must not leave a dangling <br>."""
    cell = first_table(tmp_path, [["1.1 Confirm\n\n1.2 Identify"]]).find(f"{W}tr").find(f"{W}tc")
    assert T.cell_md(cell) == "1.1 Confirm<br>1.2 Identify"


def test_each_row_renders_pipe_delimited(tmp_path):
    """TU-16"""
    table = first_table(tmp_path, [["Element", "Performance Criteria"], ["1. Prepare", "1.1 Confirm"]])
    lines = T.render_table(table).splitlines()
    assert lines[0] == "| Element | Performance Criteria |"
    assert lines[2] == "| 1. Prepare | 1.1 Confirm |"


def test_separator_follows_the_header_row_only(tmp_path):
    """TU-17"""
    table = first_table(tmp_path, [["A", "B"], ["1", "2"], ["3", "4"]])
    lines = T.render_table(table).splitlines()
    assert lines[1] == "| --- | --- |"
    assert [i for i, ln in enumerate(lines) if set(ln) <= set("| -")] == [1]


# ---------------------------------------------------------------------------
# transcribe() — the assembly
# ---------------------------------------------------------------------------

def test_heading_renders_at_its_level(tmp_path):
    """TU-18"""
    md = T.transcribe(make_docx(tmp_path, [p("Foundation Skills", style="Heading2")]))
    assert md.startswith("## Foundation Skills")


def test_consecutive_bullets_stay_one_block(tmp_path):
    """TU-19 — a tight list, not one block per bullet."""
    md = T.transcribe(make_docx(tmp_path, [
        p("configure two services", style="ListBullet"),
        p("document the configuration", style="ListBullet"),
    ]))
    assert md == "- configure two services\n- document the configuration\n"


def test_nesting_renders_as_two_space_indent(tmp_path):
    """TU-20"""
    md = T.transcribe(make_docx(tmp_path, [
        p("parent", style="ListBullet"),
        p("child", style="ListBullet2"),
    ]))
    assert md == "- parent\n  - child\n"


def test_empty_paragraph_ends_an_open_list(tmp_path):
    """TU-21 — the two bullets are separate lists, not one four-line block."""
    md = T.transcribe(make_docx(tmp_path, [
        p("first", style="ListBullet"),
        p(""),
        p("second", style="ListBullet"),
    ]))
    assert md == "- first\n\n- second\n"


def test_empty_paragraph_contributes_nothing(tmp_path):
    """TU-22"""
    md = T.transcribe(make_docx(tmp_path, [p("before"), p(""), p("after")]))
    assert md == "before\n\nafter\n"


def test_table_ends_a_list_and_is_its_own_block(tmp_path):
    """TU-23"""
    md = T.transcribe(make_docx(tmp_path, [
        p("a bullet", style="ListBullet"),
        tbl([["Skill", "Description"]]),
    ]))
    assert md == "- a bullet\n\n| Skill | Description |\n| --- | --- |\n"


def test_blocks_are_separated_by_a_blank_line(tmp_path):
    """TU-24"""
    md = T.transcribe(make_docx(tmp_path, [p("Performance Evidence", style="Heading2"),
                                           p("The candidate must")]))
    assert md == "## Performance Evidence\n\nThe candidate must\n"


def test_output_ends_with_one_newline(tmp_path):
    """TU-25"""
    md = T.transcribe(make_docx(tmp_path, [p("Element 1")]))
    assert md.endswith("\n") and not md.endswith("\n\n")


def test_document_without_a_body_yields_nothing(tmp_path):
    """TU-26"""
    assert T.transcribe(make_docx_raw(tmp_path, NO_BODY)) == ""


def test_page_furniture_never_reaches_the_output(tmp_path):
    """TU-27"""
    md = T.transcribe(make_docx(tmp_path, [p("Element 1")], furniture=True))
    assert "Element 1" in md
    assert "Approved Page" not in md


# ---------------------------------------------------------------------------
# main() — the CLI
# ---------------------------------------------------------------------------

def test_output_path_is_written_creating_parents(tmp_path):
    """TU-28"""
    docx = make_docx(tmp_path, [p("Element 1")])
    out = tmp_path / "units_of_competency" / "ICTCLD501.md"
    assert run_cli(docx, out).returncode == 0
    assert out.read_text(encoding="utf-8") == "Element 1\n"


def test_markdown_goes_to_stdout_without_a_path(tmp_path):
    """TU-29"""
    result = run_cli(make_docx(tmp_path, [p("Element 1")]))
    assert result.returncode == 0
    assert result.stdout == "Element 1\n"


def test_wrong_argument_count_exits_two(tmp_path):
    """TU-30"""
    assert run_cli().returncode == 2
    assert run_cli("a.docx", "b.md", "c.extra").returncode == 2
