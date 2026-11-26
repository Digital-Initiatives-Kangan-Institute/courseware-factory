"""Cases IU-01 .. IU-30 — factory/docs/test-plan.md.

Fixtures are hand-written markdown in the shape a validated transcription takes: `##` section
headings, a table for the Elements and Foundation Skills sections, bullets for PE / KE / AC.

The extractor is what guarantees consolidation stays verbatim, and the step's gate builds its expected
set by calling it. So a fault here is not "one script is wrong" — it is the yardstick and the thing
being measured moving together.
"""
import subprocess
import sys

import inventory_uoc as I
import pytest
from conftest import INVENTORY

UNIT = """\
# ICTCLD501 Configure cloud services

## Application

This unit describes the skills and knowledge required to configure cloud services.

## Elements and Performance Criteria

| Element | Performance Criteria |
| --- | --- |
| 1. Prepare to configure | 1.1 Confirm cloud service requirements with the client<br>1.2 Identify security and access requirements |
| 2. Configure services | 2.1 Configure services according to organisational procedures |

## Foundation Skills

| Skill | Description |
| --- | --- |
| Oral communication | Presents information using clear language |
| Numeracy | Interprets service cost estimates |

## Performance Evidence

The candidate must demonstrate the ability to complete the tasks outlined in the elements.

- configure two cloud services
- document the configuration
  - including the access model

## Knowledge Evidence

- cloud service models
- organisational procedures

## Assessment Conditions

Skills must be demonstrated in a workplace or simulated environment.

- access to a cloud platform
- access to organisational procedures

Assessors of this unit must satisfy the requirements of the Standards for RTOs.
"""


def run_cli(*args):
    return subprocess.run([sys.executable, str(INVENTORY), *map(str, args)],
                          capture_output=True, text=True)


def write_unit(tmp_path, text=UNIT, name="ICTCLD501_Complete_R1.md"):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def rendered(code="ICTCLD501", md=UNIT, assessor_ac=False):
    """{section heading: [item lines]} for one unit."""
    return {header: items for header, items in I.inventory(code, md, assessor_ac)}


# ---------------------------------------------------------------------------
# section_body()
# ---------------------------------------------------------------------------

def test_text_between_headings_is_returned():
    """IU-01"""
    body = I.section_body(UNIT, "Knowledge Evidence")
    assert "cloud service models" in body
    assert "access to a cloud platform" not in body


def test_absent_heading_yields_nothing():
    """IU-02"""
    assert I.section_body(UNIT, "Range of Conditions").strip() == ""


def test_last_section_runs_to_the_end():
    """IU-03"""
    body = I.section_body(UNIT, "Assessment Conditions")
    assert "Assessors of this unit must satisfy" in body


# ---------------------------------------------------------------------------
# parse_pcs()
# ---------------------------------------------------------------------------

def test_each_criterion_becomes_an_item():
    """IU-04"""
    assert I.parse_pcs(UNIT)[0] == ("1.1", "1.1 Confirm cloud service requirements with the client")


def test_criteria_split_on_br():
    """IU-05 — two criteria share one cell in the source table."""
    assert [num for num, _ in I.parse_pcs(UNIT)] == ["1.1", "1.2", "2.1"]


def test_element_column_is_not_criteria():
    """IU-06 — `1. Prepare to configure` is an element, not a performance criterion."""
    assert all("Prepare to configure" not in text for _, text in I.parse_pcs(UNIT))


def test_cell_without_a_number_contributes_nothing():
    """IU-07"""
    md = "## Elements and Performance Criteria\n\n| Element | Performance Criteria |\n| --- | --- |\n"
    assert I.parse_pcs(md) == []


# ---------------------------------------------------------------------------
# parse_fs()
# ---------------------------------------------------------------------------

def test_each_row_becomes_skill_and_description():
    """IU-08"""
    assert I.parse_fs(UNIT)[0] == ("Oral communication", "Presents information using clear language")


def test_header_row_is_skipped():
    """IU-09"""
    assert [name for name, _ in I.parse_fs(UNIT)] == ["Oral communication", "Numeracy"]


def test_row_without_a_skill_name_is_skipped():
    """IU-10 — a continuation row belongs to the skill above it, not to a new one."""
    md = ("## Foundation Skills\n\n| Skill | Description |\n| --- | --- |\n"
          "| Numeracy | Interprets estimates |\n|  | and compares them |\n")
    assert I.parse_fs(md) == [("Numeracy", "Interprets estimates")]


# ---------------------------------------------------------------------------
# parse_bullets()
# ---------------------------------------------------------------------------

def test_each_top_level_bullet_is_an_item():
    """IU-11"""
    assert len(I.parse_bullets(UNIT, "Knowledge Evidence")) == 2


def test_sub_bullets_stay_with_their_parent():
    """IU-12 — a nested bullet is part of its parent item, not a second item."""
    blocks = I.parse_bullets(UNIT, "Performance Evidence")
    assert len(blocks) == 2
    assert blocks[1] == ["- document the configuration", "  - including the access model"]


def test_intro_prose_is_ignored():
    """IU-13 — the sentence before the bullets is not an item."""
    blocks = I.parse_bullets(UNIT, "Performance Evidence")
    assert all("must demonstrate the ability" not in b[0] for b in blocks)


def test_single_parent_ending_in_colon_promotes_children():
    """IU-14 — e.g. ICTICT517 PE, where one parent introduces the real items."""
    md = ("## Performance Evidence\n\n- for one organisation:\n"
          "  - configure the service\n  - record the result\n")
    assert I.parse_bullets(md, "Performance Evidence") == [
        ["- configure the service"], ["- record the result"]]


def test_promotion_needs_exactly_one_parent():
    """IU-15 — with a sibling present, a trailing colon is just punctuation."""
    md = ("## Performance Evidence\n\n- for one organisation:\n"
          "  - configure the service\n- document the outcome\n")
    blocks = I.parse_bullets(md, "Performance Evidence")
    assert [b[0] for b in blocks] == ["- for one organisation:", "- document the outcome"]


# ---------------------------------------------------------------------------
# trailing_assessor_ac() and emit_item()
# ---------------------------------------------------------------------------

def test_assessor_paragraph_is_found():
    """IU-16"""
    assert I.trailing_assessor_ac(UNIT).startswith("Assessors of this unit must satisfy")


def test_section_without_an_assessor_paragraph_yields_nothing():
    """IU-17"""
    assert I.trailing_assessor_ac("## Assessment Conditions\n\n- access to a cloud platform\n") is None


def test_reference_is_appended_to_the_line():
    """IU-18"""
    assert I.emit_item("ICTCLD501 PE 1", "- configure two services") == \
        "- configure two services [ICTCLD501 PE 1]"


def test_child_lines_keep_their_indentation():
    """IU-19 — the child stays untagged and indented: it is part of the parent's item."""
    out = I.emit_item("ICTCLD501 PE 2", "- document it", ["  - including the access model"])
    assert out == "- document it [ICTCLD501 PE 2]\n  - including the access model"


def test_bullet_marker_is_not_duplicated():
    """IU-20"""
    assert I.emit_item("X PE 1", "- text").count("- ") == 1


# ---------------------------------------------------------------------------
# inventory()
# ---------------------------------------------------------------------------

def test_five_sections_in_order():
    """IU-21"""
    headers = [h for h, _ in I.inventory("ICTCLD501", UNIT, False)]
    assert headers == [
        "## ICTCLD501 — Performance Criteria",
        "## ICTCLD501 — Foundation Skills",
        "## ICTCLD501 — Performance Evidence",
        "## ICTCLD501 — Knowledge Evidence",
        "## ICTCLD501 — Assessment Conditions",
    ]


def test_pc_items_carry_their_number():
    """IU-22"""
    items = rendered()["## ICTCLD501 — Performance Criteria"]
    assert items[0].endswith("[ICTCLD501 PC 1.1]")
    assert items[-1].endswith("[ICTCLD501 PC 2.1]")


def test_fs_items_are_tagged_by_skill_name():
    """IU-23"""
    items = rendered()["## ICTCLD501 — Foundation Skills"]
    assert items[0] == ("- **Oral communication** — Presents information using clear language "
                        "[ICTCLD501 FS Oral communication]")


def test_bullet_sections_are_numbered_in_source_order():
    """IU-24"""
    items = rendered()["## ICTCLD501 — Knowledge Evidence"]
    assert items[0].endswith("[ICTCLD501 KE 1]")
    assert items[1].endswith("[ICTCLD501 KE 2]")


def test_assessor_ac_adds_one_numbered_item():
    """IU-25 — numbered after the last real AC bullet."""
    items = rendered(assessor_ac=True)["## ICTCLD501 — Assessment Conditions"]
    assert len(items) == 3
    assert items[-1].startswith("- Assessors of this unit must satisfy")
    assert items[-1].endswith("[ICTCLD501 AC 3]")


def test_without_assessor_ac_the_paragraph_is_absent():
    """IU-26"""
    items = rendered(assessor_ac=False)["## ICTCLD501 — Assessment Conditions"]
    assert len(items) == 2
    assert all("Assessors of this unit" not in item for item in items)


def test_empty_section_raises():
    """IU-27 — the gate measures against these same rules, so a quiet gap would pass a short doc."""
    without_ke = UNIT.replace("- cloud service models\n- organisational procedures\n", "")
    with pytest.raises(ValueError, match="Knowledge Evidence"):
        list(I.inventory("ICTCLD501", without_ke, False))


# ---------------------------------------------------------------------------
# main() — the CLI
# ---------------------------------------------------------------------------

def test_units_are_emitted_in_order(tmp_path):
    """IU-28"""
    first = write_unit(tmp_path, name="ICTCLD501_Complete_R1.md")
    second = write_unit(tmp_path, name="ICTCLD503_Complete_R1.md")
    result = run_cli(f"--unit=ICTCLD501={first}", f"--unit=ICTCLD503={second}")
    assert result.returncode == 0, result.stderr
    assert result.stdout.index("# ICTCLD501") < result.stdout.index("# ICTCLD503")


def test_malformed_unit_argument_is_an_error(tmp_path):
    """IU-29 — a bare path with no code would produce untagged items."""
    assert run_cli(f"--unit={write_unit(tmp_path)}").returncode != 0


def test_extraction_failure_exits_two(tmp_path):
    """IU-30"""
    broken = write_unit(tmp_path, UNIT.replace("## Knowledge Evidence", "## Knowledge"))
    result = run_cli(f"--unit=ICTCLD501={broken}")
    assert result.returncode == 2
    assert "Knowledge Evidence" in result.stderr
