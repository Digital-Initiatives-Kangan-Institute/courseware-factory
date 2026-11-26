"""Cases HWI-01 .. HWI-13 — factory/docs/test-plan.md.

Covers common/helpers/workbook_instrument.py: deriving the marking apparatus from a workbook's own tags.
"""
import pytest

import workbook_instrument as WI

TASKS = [
    {"n": 1, "uoc": ["ICTCLD501 PC 1.1"]},
    {"n": 2, "uoc": ["ICTCLD501 PC 1.2", "ICTCLD501 PC 1.1"]},
    {"n": 3, "uoc": ["ICTCLD501 KE 2"]},
    {"n": 4, "uoc": []},
]
QUESTIONS = [{"n": 1, "uoc": ["ICTCLD503 PE 1"]}]
ELEMENTS = WI.collect_elements(TASKS, (QUESTIONS, "Q"))
CRITERIA = [
    {"code": "A1", "text": "Identifies the requirements", "tasks": ["1-2"]},
    {"code": "A2", "text": "Explains the knowledge", "tasks": [3, "Q1"]},
]

CONSOLIDATED = """\
# Consolidated UoC

- 1.1 Identify disaster recovery plan requirements [ICTCLD501 PC 1.1]
- 1.2 Determine existing organisational recovery plans [ICTCLD501 PC 1.2]
- 1.10 A tenth criterion [ICTCLD501 PC 1.10]
- Recovery point objectives<br>and how they are set [ICTCLD501 KE 2]
- **Oral communication** — Uses listening and questioning techniques [ICTCLD501 FS Oral communication]
- Access to a cloud environment [ICTCLD501 AC 1]
- Apply infection prevention procedures [HLTINF006 PC 1.1]
Prose mentioning [ICTCLD501 PC 9.9] is not a bullet, so it is not an item.
"""


@pytest.fixture
def uoc(tmp_path):
    p = tmp_path / "consolidated_uoc.md"
    p.write_text(CONSOLIDATED, encoding="utf-8")
    return WI.load_uoc_text(p)


def test_tasks_and_questions_are_keyed_separately():
    """HWI-01"""
    assert set(ELEMENTS) == {"1", "2", "3", "4", "Q1"}
    assert ELEMENTS["Q1"] is QUESTIONS[0]


def test_criterion_tasks_accept_numbers_q_keys_and_ranges():
    """HWI-02"""
    rows = WI.marking_guide([{"code": "A9", "text": "x", "tasks": [3, "Q1", "1-2"]}], ELEMENTS)
    assert rows[0][1] == "[ICTCLD501 KE 2] · [ICTCLD503 PE 1] · [ICTCLD501 PC 1.1] · [ICTCLD501 PC 1.2]"


def test_uoc_line_is_the_ordered_union_of_task_tags():
    """HWI-03 — PC 1.1 appears on tasks 1 and 2, and is listed once, where it first appears."""
    assert WI.marking_guide(CRITERIA, ELEMENTS)[0] == [
        "A1 Identifies the requirements", "[ICTCLD501 PC 1.1] · [ICTCLD501 PC 1.2]"]


def test_unknown_task_raises_naming_it():
    """HWI-04"""
    with pytest.raises(KeyError, match="'7'"):
        WI.marking_guide([{"code": "A1", "text": "x", "tasks": [7]}], ELEMENTS)


def test_untagged_criterion_raises():
    """HWI-05"""
    with pytest.raises(ValueError, match="free-floating"):
        WI.marking_guide([{"code": "A1", "text": "x", "tasks": [4]}], ELEMENTS)


def test_benchmark_comes_from_the_marking_derivation():
    """HWI-06"""
    lines = [line for _, line in WI.marking_guide(CRITERIA, ELEMENTS)]
    assert WI.benchmark_sections(CRITERIA, ELEMENTS, "AT1") == [
        ("AT1", [("A1", lines[0]), ("A2", lines[1])])]


def test_item_text_is_read_verbatim_and_normalised(uoc):
    """HWI-07"""
    assert uoc["ICTCLD501 PC 1.1"] == "1.1 Identify disaster recovery plan requirements"
    assert uoc["ICTCLD501 KE 2"] == "Recovery point objectives and how they are set"
    assert uoc["ICTCLD501 FS Oral communication"] == "Oral communication — Uses listening and questioning techniques"
    assert "ICTCLD501 PC 9.9" not in uoc


def test_reverse_map_is_per_unit_and_ordered(uoc):
    """HWI-08 — PC 1.10 sorts after PC 1.2; the ICTCLD503 tag belongs to another unit's map."""
    elements = WI.collect_elements([
        {"n": 1, "uoc": ["ICTCLD501 KE 2", "ICTCLD501 PC 1.10", "ICTCLD503 PE 1"]},
        {"n": 2, "uoc": ["ICTCLD501 PC 1.2"]},
    ])
    criteria = [{"code": "A1", "text": "x", "tasks": [1]}, {"code": "A2", "text": "y", "tasks": [1, 2]}]
    rows = WI.build_reverse_map(criteria, elements, uoc, "ICTCLD501")
    assert [r[0].split("]")[0] + "]" for r in rows[1:]] == [
        "[ICTCLD501 PC 1.2]", "[ICTCLD501 PC 1.10]", "[ICTCLD501 KE 2]"]
    assert rows[2][1] == "A1 · A2"


def test_phantom_tag_raises(uoc):
    """HWI-09"""
    elements = WI.collect_elements([{"n": 1, "uoc": ["ICTCLD501 PC 7.7"]}])
    with pytest.raises(ValueError, match="phantom.*ICTCLD501 PC 7.7"):
        WI.build_reverse_map([{"code": "A1", "text": "x", "tasks": [1]}], elements, uoc, "ICTCLD501")


def test_conditions_are_pre_condition_rows(uoc):
    """HWI-10"""
    rows = WI.build_reverse_map(CRITERIA, ELEMENTS, uoc, "ICTCLD501", {"ICTCLD501 AC 1": "C1"})
    assert rows[-1] == ["[ICTCLD501 AC 1] Access to a cloud environment", "C1 (pre-condition)"]


def test_unevidenced_items_are_reported_in_order():
    """HWI-11"""
    expected = ["ICTCLD501 PC 1.1", "ICTCLD501 PC 2.1", "ICTCLD501 KE 1"]
    assert WI.unevidenced_items(CRITERIA, ELEMENTS, {}, expected) == ["ICTCLD501 PC 2.1", "ICTCLD501 KE 1"]


def test_benchmark_body_has_one_table_per_unit(tmp_path):
    """HWI-12"""
    p = tmp_path / "consolidated_uoc.md"
    p.write_text(CONSOLIDATED + "- Apply a performance evidence [ICTCLD503 PE 1]\n", encoding="utf-8")
    body = WI.reverse_map_body(CRITERIA, ELEMENTS, p, [("ICTCLD501", "ICTCLD501 items"), ("ICTCLD503", "ICTCLD503 items")])
    assert [k for k, _ in body] == ["h1", "p", "p", "tbl", "p", "tbl"]
    assert body[1] == ("p", WI.INTRO)


def test_any_training_package_unit_is_recognised(uoc):
    """HWI-13"""
    assert uoc["HLTINF006 PC 1.1"] == "Apply infection prevention procedures"
