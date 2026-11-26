"""Kangan instrument templates — filling them with a workbook instrument.

The engine derives an instrument's marking apparatus (`workbook_instrument`) and lays its content out
(`instrument_layout`); putting that into the institution's template is the institution pack's job,
because it is shaped entirely by that template's tables. The templates are in `templates/` beside this.

Depends on the factory engine's helpers (`docx_tables`, `instrument_layout`) being importable.

Cases: IKT-01 .. IKT-08 in factory/docs/test-plan.md.
"""
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent / "templates"

BOILERPLATE = [
    "Add or delete rows as required",
    "If questioning or observation is incorporated into this assessment task, you can incorporate "
    "a Practical Observation Checklist.",
]

def assemble(template_path, spec, mode, render_body, benchmark=None):
    """Fill a Kangan instrument template and render a workbook into it.

    `spec` holds the front matter every instrument supplies: `details`, `overview` /
    `student_overview`, `tasks`, `time_allowed`, `resources` / `student_resources`, `criteria`,
    `conditions`, `criteria_map` and `marking_rows`. `render_body(doc, mode)` renders the
    workbook itself.

    The student template carries one extra leading row in its Details table. That offset is the
    only structural difference between the two templates, and it lives here rather than being
    rediscovered in every builder.
    """
    from docx import Document
    from docx_tables import clear_table_rows, find_instruction_row, set_cell_content
    from instrument_layout import render_benchmark

    student = mode != "assessor"
    doc = Document(template_path)

    details = doc.tables[0]
    off = 1 if student else 0
    for i, key in enumerate(("qualification", "units", "task_title", "task_number")):
        set_cell_content(details.rows[1 + off + i].cells[1], spec["details"][key])

    instr = doc.tables[1]
    set_cell_content(find_instruction_row(instr, "Assessment overview"),
                     spec["student_overview"] if student else spec["overview"])
    set_cell_content(find_instruction_row(instr, "Task"), spec["tasks"])
    set_cell_content(find_instruction_row(instr, "Time allowed"), spec["time_allowed"])
    set_cell_content(find_instruction_row(instr, "Resources required"),
                     spec["student_resources"] if student else spec["resources"])
    set_cell_content(find_instruction_row(instr, "Assessment criteria"), spec["criteria"])
    if not student:
        set_cell_content(find_instruction_row(instr, "Location"), "")
        row = instr.add_row()
        set_cell_content(row.cells[0], "Assessment Conditions & Setup Requirements")
        for run in row.cells[0].paragraphs[0].runs:
            run.bold = True
        set_cell_content(row.cells[1], spec["conditions"])

    # The student sees the criterion statements; the assessor sees them with their UoC lines.
    mark = doc.tables[2]
    clear_table_rows(mark, 2)
    rows = ([[f"{c['code']} {c['text']}"] for c in spec["criteria_map"]] if student
            else spec["marking_rows"])
    for lines in rows:
        row = mark.add_row()
        set_cell_content(row.cells[0], lines)
        set_cell_content(row.cells[1], spec.get("check", "☐ Yes  ☐ No"))

    for text in BOILERPLATE:
        for p in doc.paragraphs:
            if p.text.strip() == text:
                p._element.getparent().remove(p._element)
                break

    render_body(doc, mode)

    if not student and benchmark:
        def render_table(d, rws):
            t = d.add_table(rows=len(rws), cols=len(rws[0]))
            try:
                t.style = "Table Grid"
            except KeyError:
                pass
            for r, cells in enumerate(rws):
                for c, val in enumerate(cells):
                    set_cell_content(t.rows[r].cells[c], val)
            d.add_paragraph()

        render_benchmark(doc, benchmark, render_table,
                         {"h1": "Heading 1", "h2": "Heading 2", "p": "Normal"})
    return doc
