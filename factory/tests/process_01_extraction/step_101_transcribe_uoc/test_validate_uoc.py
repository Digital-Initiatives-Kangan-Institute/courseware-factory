"""Cases VU-01 .. VU-46 — factory/docs/test-plan.md.

The gate's job is to prove a `.md` transcription is verbatim against its source `.docx`. Three failure
modes must be caught: content in the source MISSING from the transcription, content in the transcription
NOT IN the source, and content MISTRANSCRIBED. It must equally NOT cry wolf on markdown syntax, page
furniture, whitespace, or Word's own typography.

**Independence.** Every fixture is built from literal strings and the expected `.md` is written by hand —
never produced by `transcribe_uoc.py`. A gate fed its own subject's output would only prove the two agree
with each other. That matters more since both scripts read words through the same `docx_text`: the shape
check, which reads bullet nesting from the paragraph styles, is the half that still sees what the word
diff cannot.
"""
import subprocess
import sys

import pytest

import validate_uoc as V
from conftest import VALIDATOR
from docx_fixtures import bullet, h, make_docx, p, raw_p, tbl

# Losing or inventing a whole bullet trips both axes — the words differ AND the shape differs. Either
# blocks the gate, so those cases assert failure rather than a particular class.
FAILS = ("substantive", "structure")


def verdict(tmp_path, docx, md_text: str) -> str:
    """Reduce a pair to its verdict: exact | cosmetic | substantive | structure."""
    md = tmp_path / "unit.md"
    md.write_text(md_text, encoding="utf-8")
    f = V.compare(docx, md, "fixture")
    if f["structure_diff"]:
        return "structure"
    if f["exact_match"]:
        return "exact"
    if f["cosmetic_match"]:
        return "cosmetic"
    return "substantive"


def write_md(tmp_path, text: str, name="unit.md"):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def run_cli(*args):
    return subprocess.run([sys.executable, str(VALIDATOR), *map(str, args)],
                          capture_output=True, text=True)


# ---------------------------------------------------------------------------
# A representative source unit and its faithful transcription
# ---------------------------------------------------------------------------

BLOCKS = [
    h(1, "ICTCLD501 Configure cloud services"),
    h(2, "Elements and Performance Criteria"),
    tbl([
        ["Element", "Performance Criteria"],
        ["1. Prepare to configure", "1.1 Confirm cloud service requirements with the client\n"
                                    "1.2 Identify security and access requirements"],
        ["2. Configure services", "2.1 Configure services according to organisational procedures"],
    ]),
    h(2, "Performance Evidence"),
    p("The candidate must demonstrate the ability to complete the tasks outlined in the "
      "elements, performance criteria and knowledge evidence of this unit."),
    bullet("configure two cloud services"),
    bullet("document the configuration"),
    h(2, "Foundation Skills"),
    tbl([
        ["Skill", "Description"],
        ["Oral communication", "Presents information using clear language"],
    ]),
]

MD = """# ICTCLD501 Configure cloud services

## Elements and Performance Criteria

| Element | Performance Criteria |
| --- | --- |
| 1. Prepare to configure | 1.1 Confirm cloud service requirements with the client<br>1.2 Identify security and access requirements |
| 2. Configure services | 2.1 Configure services according to organisational procedures |

## Performance Evidence

The candidate must demonstrate the ability to complete the tasks outlined in the elements, performance criteria and knowledge evidence of this unit.

- configure two cloud services
- document the configuration

## Foundation Skills

| Skill | Description |
| --- | --- |
| Oral communication | Presents information using clear language |
"""


@pytest.fixture
def source(tmp_path):
    return make_docx(tmp_path, BLOCKS)


# ---------------------------------------------------------------------------
# md_to_text() — strip markdown, leave the words
# ---------------------------------------------------------------------------

def test_heading_markers_are_stripped(tmp_path):
    """VU-01"""
    assert V.md_to_text(write_md(tmp_path, "## Performance Evidence\n")).strip() == "Performance Evidence"


def test_bullet_marker_is_stripped(tmp_path):
    """VU-02"""
    assert V.md_to_text(write_md(tmp_path, "- configure two services\n")).strip() == "configure two services"


def test_numbered_marker_is_stripped(tmp_path):
    """VU-03"""
    assert V.md_to_text(write_md(tmp_path, "1. Prepare to configure\n")).strip() == "Prepare to configure"


def test_table_row_becomes_one_line_per_cell(tmp_path):
    """VU-04"""
    text = V.md_to_text(write_md(tmp_path, "| Element | Performance Criteria |\n"))
    assert [ln for ln in text.splitlines() if ln] == ["Element", "Performance Criteria"]


def test_separator_row_contributes_nothing(tmp_path):
    """VU-05"""
    text = V.md_to_text(write_md(tmp_path, "| A | B |\n| --- | --- |\n"))
    assert "-" not in text


def test_br_inside_a_cell_becomes_a_line_break(tmp_path):
    """VU-06 — matching how the source cell's two paragraphs read."""
    text = V.md_to_text(write_md(tmp_path, "| 1.1 Confirm<br>1.2 Identify |\n"))
    assert [ln for ln in text.splitlines() if ln] == ["1.1 Confirm", "1.2 Identify"]


def test_br_in_prose_becomes_a_line_break(tmp_path):
    """VU-07"""
    text = V.md_to_text(write_md(tmp_path, "first line<br>second line\n"))
    assert [ln for ln in text.splitlines() if ln] == ["first line", "second line"]


# ---------------------------------------------------------------------------
# List shape — bullet identity, which the word diff cannot see
# ---------------------------------------------------------------------------

def test_list_paragraphs_contribute_their_depth(tmp_path):
    """VU-08"""
    docx = make_docx(tmp_path, [p("The candidate must:"), bullet("configure"), bullet("record", depth=1)])
    assert V.docx_list_shape(docx) == [0, 1]


def test_any_list_prefixed_style_counts(tmp_path):
    """VU-09 — wider than the transcriber's List(Bullet|Number|Paragraph) rule, deliberately.

    An unhandled style becomes a paragraph in the transcription; counting it here is what turns that
    into a visible failure instead of a silent flattening.
    """
    assert V.docx_list_shape(make_docx(tmp_path, [p("configure", style="List")])) == [0]


def test_list_styled_table_cell_is_not_a_bullet(tmp_path):
    """VU-10 — the real UoC documents style many table-cell paragraphs `List`."""
    docx = make_docx(tmp_path, [tbl([["Element", "PC"], ["1. Prepare", "1.1 Confirm"]], cell_style="List")])
    assert V.docx_list_shape(docx) == []


def test_empty_list_paragraph_contributes_no_depth(tmp_path):
    """VU-11 — a spacer styled as a bullet would otherwise invent one the markdown cannot have."""
    docx = make_docx(tmp_path, [bullet("configure"), p("", style="ListBullet"), bullet("record")])
    assert V.docx_list_shape(docx) == [0, 0]


def test_markdown_depth_comes_from_indentation(tmp_path):
    """VU-12"""
    md = write_md(tmp_path, "- parent\n  - child\n    - grandchild\n")
    assert V.md_list_shape(md) == [0, 1, 2]


# ---------------------------------------------------------------------------
# Not crying wolf — legitimate differences pass
# ---------------------------------------------------------------------------

def test_faithful_transcription_is_exact(tmp_path, source):
    """VU-13 — the baseline. If this fails, every FAIL-side case below is meaningless."""
    assert verdict(tmp_path, source, MD) == "exact"


def test_page_furniture_is_not_missing_content(tmp_path):
    """VU-14 — headers/footers carry unit codes and attribution that are deliberately not transcribed."""
    assert verdict(tmp_path, make_docx(tmp_path, BLOCKS, furniture=True), MD) == "exact"


def test_tabs_and_line_breaks_are_structure(tmp_path):
    """VU-15"""
    docx = make_docx(tmp_path, [p("PC\t1.1\tConfirm requirements"), p("first line\nsecond line")])
    assert verdict(tmp_path, docx, "PC 1.1 Confirm requirements\n\nfirst line<br>second line\n") == "exact"


def test_multi_paragraph_cell_is_exact(tmp_path):
    """VU-16 — two paragraphs in one cell transcribe as `a<br>b`: the same content, not an insertion."""
    docx = make_docx(tmp_path, [tbl([["Element", "PC"], ["1. Prepare", "1.1 Confirm\n1.2 Identify"]])])
    md = "| Element | PC |\n| --- | --- |\n| 1. Prepare | 1.1 Confirm<br>1.2 Identify |\n"
    assert verdict(tmp_path, docx, md) == "exact"


def test_word_typography_grades_cosmetic(tmp_path):
    """VU-17 — smart quotes, en dashes and ellipses are Word's, not the author's."""
    docx = make_docx(tmp_path, [p("The candidate’s work – as scoped – must… continue")])
    assert verdict(tmp_path, docx, "The candidate's work - as scoped - must... continue\n") == "cosmetic"


# ---------------------------------------------------------------------------
# Failure mode 1 — content in the source is MISSING from the transcription
# ---------------------------------------------------------------------------

def test_dropped_word_fails(tmp_path, source):
    """VU-18"""
    assert verdict(tmp_path, source, MD.replace("clear language", "language")) == "substantive"


def test_dropped_negation_fails(tmp_path):
    """VU-19 — the smallest possible omission that inverts an assessment requirement."""
    docx = make_docx(tmp_path, [p("The candidate must not use a pre-built template")])
    assert verdict(tmp_path, docx, "The candidate must use a pre-built template\n") == "substantive"


def test_dropped_bullet_fails(tmp_path, source):
    """VU-20 — a whole PE item lost silently reduces what the cluster must assess."""
    assert verdict(tmp_path, source, MD.replace("- document the configuration\n", "")) in FAILS


def test_dropped_table_cell_fails(tmp_path, source):
    """VU-21 — a PC lost from inside a table cell, where it is easiest to miss by eye."""
    broken = MD.replace("<br>1.2 Identify security and access requirements", "")
    assert verdict(tmp_path, source, broken) == "substantive"


def test_truncated_trailing_section_fails(tmp_path, source):
    """VU-22 — the whole Foundation Skills table gone."""
    assert verdict(tmp_path, source, MD.split("## Foundation Skills")[0]) == "substantive"


# ---------------------------------------------------------------------------
# Failure mode 2 — content in the transcription is NOT IN the source
# ---------------------------------------------------------------------------

def test_added_sentence_fails(tmp_path, source):
    """VU-23 — invented content becomes a requirement nobody must actually meet."""
    assert verdict(tmp_path, source, MD + "\nCandidates may resubmit once.\n") == "substantive"


def test_added_bullet_fails(tmp_path, source):
    """VU-24"""
    broken = MD.replace("- document the configuration",
                        "- document the configuration\n- test the configuration")
    assert verdict(tmp_path, source, broken) in FAILS


def test_added_table_row_fails(tmp_path, source):
    """VU-25"""
    broken = MD.replace(
        "| 2. Configure services | 2.1 Configure services according to organisational procedures |",
        "| 2. Configure services | 2.1 Configure services according to organisational procedures |\n"
        "| 3. Review | 3.1 Review the configuration |",
    )
    assert verdict(tmp_path, source, broken) == "substantive"


def test_duplicated_item_fails(tmp_path, source):
    """VU-26 — copy-paste during hand-editing: the same PE bullet twice."""
    broken = MD.replace("- configure two cloud services\n", "- configure two cloud services\n" * 2)
    assert verdict(tmp_path, source, broken) in FAILS


# ---------------------------------------------------------------------------
# Failure mode 3 — content is MISTRANSCRIBED
# ---------------------------------------------------------------------------

def test_changed_word_fails(tmp_path, source):
    """VU-27"""
    broken = MD.replace("Confirm cloud service", "Identify cloud service")
    assert verdict(tmp_path, source, broken) == "substantive"


def test_changed_item_number_fails(tmp_path, source):
    """VU-28 — PC numbering is the identity every downstream UoC tag is built from."""
    assert verdict(tmp_path, source, MD.replace("2.1 Configure", "2.2 Configure")) == "substantive"


def test_changed_quantity_fails(tmp_path, source):
    """VU-29 — `two cloud services` -> `three` changes what a candidate must produce."""
    broken = MD.replace("configure two cloud", "configure three cloud")
    assert verdict(tmp_path, source, broken) == "substantive"


def test_changed_case_fails(tmp_path, source):
    """VU-30 — Foundation Skills are keyed by the skill name verbatim, case included."""
    assert verdict(tmp_path, source, MD.replace("Oral communication", "Oral Communication")) == "substantive"


def test_reordered_items_fail(tmp_path, source):
    """VU-31 — PE bullets are numbered 1..N in source order downstream."""
    broken = MD.replace(
        "- configure two cloud services\n- document the configuration",
        "- document the configuration\n- configure two cloud services",
    )
    assert verdict(tmp_path, source, broken) == "substantive"


def test_respaced_compound_fails(tmp_path):
    """VU-32 — `IaaS/PaaS/SaaS` retyped as `IaaS / PaaS / SaaS` is a changed token, not whitespace."""
    docx = make_docx(tmp_path, [p("Identify whether the component is IaaS/PaaS/SaaS")])
    assert verdict(tmp_path, docx, "Identify whether the component is IaaS / PaaS / SaaS\n") == "substantive"


# ---------------------------------------------------------------------------
# Blind spots — a green gate over genuinely missing content is the worst outcome available
# ---------------------------------------------------------------------------

def test_empty_source_is_never_a_pass(tmp_path):
    """VU-33 — an unreadable body would otherwise agree with an empty `.md` over zero content."""
    assert verdict(tmp_path, make_docx(tmp_path, []), "") == "substantive"


def test_flattened_bullet_is_detected(tmp_path):
    """VU-34 — a list paragraph transcribed as prose. Same words, one fewer assessable item."""
    docx = make_docx(tmp_path, [bullet("configure the service"), bullet("record the result")])
    assert verdict(tmp_path, docx, "- configure the service\n\nrecord the result\n") == "structure"


def test_invented_bullet_is_detected(tmp_path):
    """VU-35 — the mirror: a source paragraph transcribed as a bullet invents an item."""
    docx = make_docx(tmp_path, [bullet("configure the service"), p("record the result")])
    assert verdict(tmp_path, docx, "- configure the service\n- record the result\n") == "structure"


def test_lost_nesting_depth_is_detected(tmp_path):
    """VU-36 — a child promoted to top level turns one item into two."""
    docx = make_docx(tmp_path, [bullet("for one organisation:"), bullet("configure the service", depth=1)])
    assert verdict(tmp_path, docx, "- for one organisation:\n- configure the service\n") == "structure"


def test_lost_symbol_character_fails(tmp_path):
    """VU-37 — a w:sym run carries its character in an attribute, not in w:t."""
    docx = make_docx(tmp_path, [raw_p(
        '<w:t xml:space="preserve">Deploy </w:t>'
        '<w:sym w:font="Symbol" w:char="F0B3"/>'
        '<w:t xml:space="preserve"> 2 instances</w:t>'
    )])
    assert verdict(tmp_path, docx, "Deploy 2 instances\n") == "substantive"


def test_lost_non_breaking_hyphen_fails(tmp_path):
    """VU-38 — dropping it silently welds two words together."""
    docx = make_docx(tmp_path, [raw_p("<w:t>e</w:t><w:noBreakHyphen/><w:t>learning</w:t>")])
    assert verdict(tmp_path, docx, "elearning\n") == "substantive"


def test_non_breaking_hyphen_as_hyphen_is_cosmetic(tmp_path):
    """VU-39 — ...but transcribing it as a plain hyphen is the right answer, and must pass."""
    docx = make_docx(tmp_path, [raw_p("<w:t>e</w:t><w:noBreakHyphen/><w:t>learning</w:t>")])
    assert verdict(tmp_path, docx, "e-learning\n") == "cosmetic"


def test_lost_carriage_return_fails(tmp_path):
    """VU-40 — w:cr is a line break like w:br. Dropping it welds the words either side together."""
    docx = make_docx(tmp_path, [raw_p("<w:t>first line</w:t><w:cr/><w:t>second line</w:t>")])
    assert verdict(tmp_path, docx, "first linesecond line\n") == "substantive"


# ---------------------------------------------------------------------------
# The CLI — exit codes are the gate's actual verdict when run from the run-sheet
# ---------------------------------------------------------------------------

def test_cli_exits_zero_on_a_faithful_pair(tmp_path, source):
    """VU-41"""
    result = run_cli(source, write_md(tmp_path, MD))
    assert result.returncode == 0, result.stdout + result.stderr


def test_cli_exits_one_on_a_substantive_diff(tmp_path, source):
    """VU-42"""
    md = write_md(tmp_path, MD.replace("- document the configuration\n", ""))
    assert run_cli(source, md).returncode == 1


def test_cli_exits_one_on_a_structure_only_diff(tmp_path):
    """VU-43 — the words match exactly and only the shape differs. A green word diff is not a pass."""
    docx = make_docx(tmp_path, [bullet("configure the service"), bullet("record the result")])
    md = write_md(tmp_path, "- configure the service\n\nrecord the result\n")
    result = run_cli(docx, md)
    assert result.returncode == 1, result.stdout
    assert "LIST STRUCTURE DIFFERS" in result.stdout


def test_cli_exits_zero_on_cosmetic_only(tmp_path):
    """VU-44"""
    docx = make_docx(tmp_path, [p("The candidate’s work – as scoped")])
    md = write_md(tmp_path, "The candidate's work - as scoped\n")
    assert run_cli(docx, md).returncode == 0


def test_cli_rejects_an_unpaired_argument(tmp_path, source):
    """VU-45 — pairs are positional, so a forgotten `.md` must be an error, never a silent skip."""
    assert run_cli(source).returncode == 2


def test_cli_reports_every_pair_before_failing(tmp_path, source):
    """VU-46 — the run-sheet validates a whole cluster; one bad pair must not mask the rest."""
    bad = write_md(tmp_path, MD.replace("- document the configuration\n", ""), name="bad.md")
    good = write_md(tmp_path, MD, name="good.md")
    result = run_cli(source, bad, source, good)
    assert result.returncode == 1
    assert result.stdout.count("RESULT:") == 2, result.stdout
