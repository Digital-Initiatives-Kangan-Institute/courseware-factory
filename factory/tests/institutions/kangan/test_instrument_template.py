"""Cases IKT-01 .. IKT-08 — factory/docs/test-plan.md.

Covers institutions/kangan/instrument_template.py: filling the Kangan Project Assessment templates.
The pack is put on the path per test by this folder's conftest, so the module is imported in a fixture.
"""
import pytest

SPEC = {
    "details": {"qualification": "QUAL01 Diploma of Testing", "units": "UNIT001 Test a thing",
                "task_title": "AT1 — The test task", "task_number": "1 of 3"},
    "overview": "Assessor overview text", "student_overview": "Student overview text",
    "tasks": "Complete the workbook", "time_allowed": "Four hours",
    "resources": "Assessor resources", "student_resources": "Student resources",
    "criteria": "See the marking guide", "conditions": "Conditions for the assessor",
    "criteria_map": [{"code": "A1", "text": "Identifies the requirements"}],
    "marking_rows": [["A1 Identifies the requirements", "[UNIT001 PC 1.1]"]],
}
BENCHMARK = [("h1", "Marking Benchmark — UoC traceability"), ("p", "Benchmark intro")]


@pytest.fixture
def T():
    import instrument_template
    return instrument_template


def _build(T, mode, benchmark=None):
    seen = []
    name = "Project Assessment - Assessor.docx" if mode == "assessor" else "Project Assessment - Student.docx"

    def render_body(doc, m):
        seen.append(m)
        doc.add_paragraph("WORKBOOK BODY")
    doc = T.assemble(T.TEMPLATES / name, SPEC, mode, render_body, benchmark)
    return doc, seen


def _value(table, label):
    row = next(r for r in table.rows if r.cells[0].text.strip().startswith(label))
    return row.cells[1].text.strip()


def _texts(doc):
    return [p.text.strip() for p in doc.paragraphs]


def test_assessor_details_are_filled(T):
    """IKT-01"""
    details = _build(T, "assessor")[0].tables[0]
    assert _value(details, "Qualification code") == "QUAL01 Diploma of Testing"
    assert _value(details, "Unit code") == "UNIT001 Test a thing"
    assert _value(details, "Assessment task title") == "AT1 — The test task"
    assert _value(details, "Assessment task number") == "1 of 3"


def test_student_details_sit_one_row_lower(T):
    """IKT-02 — the student template leads with a 'Student name' row, which stays blank."""
    details = _build(T, "student")[0].tables[0]
    assert _value(details, "Student name") == ""
    assert _value(details, "Qualification code") == "QUAL01 Diploma of Testing"
    assert _value(details, "Assessment task number") == "1 of 3"


def test_instruction_rows_follow_the_copy(T):
    """IKT-03"""
    assessor = _build(T, "assessor")[0].tables[1]
    student = _build(T, "student")[0].tables[1]
    assert _value(assessor, "Assessment overview") == "Assessor overview text"
    assert _value(assessor, "Resources required") == "Assessor resources"
    assert _value(student, "Assessment overview") == "Student overview text"
    assert _value(student, "Resources required") == "Student resources"
    for table in (assessor, student):
        assert _value(table, "Task(s)") == "Complete the workbook"
        assert _value(table, "Time allowed") == "Four hours"


def test_conditions_row_is_assessor_only(T):
    """IKT-04"""
    assessor = _build(T, "assessor")[0].tables[1]
    student = _build(T, "student")[0].tables[1]
    assert _value(assessor, "Location") == ""
    assert _value(assessor, "Assessment Conditions") == "Conditions for the assessor"
    assert not any(r.cells[0].text.startswith("Assessment Conditions") for r in student.rows)


def test_marking_table_follows_the_copy(T):
    """IKT-05"""
    assessor = _build(T, "assessor")[0].tables[2]
    student = _build(T, "student")[0].tables[2]
    assert [c.text for c in assessor.rows[-1].cells] == [
        "A1 Identifies the requirements\n[UNIT001 PC 1.1]", "☐ Yes  ☐ No"]
    assert student.rows[-1].cells[0].text == "A1 Identifies the requirements"
    assert "[UNIT001" not in "".join(c.text for r in student.rows for c in r.cells)


def test_template_boilerplate_is_removed(T):
    """IKT-06"""
    for mode in ("assessor", "student"):
        texts = _texts(_build(T, mode)[0])
        assert not any(b in texts for b in T.BOILERPLATE)


def test_body_is_rendered_by_the_caller(T):
    """IKT-07"""
    doc, seen = _build(T, "student")
    assert seen == ["student"]
    assert "WORKBOOK BODY" in _texts(doc)


def test_benchmark_is_assessor_only(T):
    """IKT-08"""
    assessor = _texts(_build(T, "assessor", BENCHMARK)[0])
    student = _texts(_build(T, "student", BENCHMARK)[0])
    assert "Marking Benchmark — UoC traceability" in assessor
    assert assessor.index("Marking Benchmark — UoC traceability") > assessor.index("WORKBOOK BODY")
    assert "Marking Benchmark — UoC traceability" not in student
