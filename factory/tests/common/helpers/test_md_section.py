"""Cases HMS-01 .. HMS-07 — factory/docs/test-plan.md.

The fixture is shaped like the documents this serves: a numbered plan whose sections end at the next
numbered section, with `###` subheadings inside them that must NOT end a section.
"""
import md_section

PLAN = """\
# S1-CL9 Cluster Assessment Plan

> **STATUS: DRAFT.**

## 1. Integration approach

One project across three units.

## 3. Assessment structure

| AT | Title |
| --- | --- |
| AT1 | Design |

### AT1 — Design

UoC coverage: [ICTCLD501 PC 1.1]

## 4. Provenance

Adapted from the CL2 plan.

## 6. Scenario requirements register

| SR | Need |
| --- | --- |
| SR-CL9-01 | An intranet page |
"""

NUMBERED = [r"^##\s+\d+\."]


def test_section_runs_to_the_first_end_match():
    """HMS-01"""
    section = md_section.span(PLAN, r"^##\s+3\.", NUMBERED)
    assert "Assessment structure" in section
    assert "Provenance" not in section


def test_start_line_is_included():
    """HMS-02 — a caller checking §3 usually wants the heading too."""
    assert md_section.span(PLAN, r"^##\s+3\.", NUMBERED).startswith("## 3. Assessment structure")


def test_end_line_is_excluded():
    """HMS-03 — the end line belongs to the next section."""
    assert not md_section.span(PLAN, r"^##\s+3\.", NUMBERED).rstrip().endswith("## 4. Provenance")


def test_absent_start_yields_none():
    """HMS-04 — 'no §7 at all' is a format failure; 'an empty §7' is not the same thing."""
    assert md_section.span(PLAN, r"^##\s+7\.", NUMBERED) is None


def test_no_end_match_runs_to_the_end():
    """HMS-05 — the last section of a document ends where the document does."""
    section = md_section.span(PLAN, r"^##\s+6\.", [r"^##\s+7\."])
    assert "SR-CL9-01" in section


def test_earliest_end_pattern_wins():
    """HMS-06 — the first MATCH in the document, not the first pattern in the list."""
    section = md_section.span(PLAN, r"^##\s+1\.", [r"^##\s+6\.", r"^##\s+3\."])
    assert "Integration approach" in section
    assert "Assessment structure" not in section


def test_end_pattern_before_the_start_is_ignored():
    """HMS-07 — only lines after the start can end the section."""
    section = md_section.span(PLAN, r"^##\s+4\.", [r"^##\s+1\.", r"^##\s+6\."])
    assert "Provenance" in section
    assert "Scenario requirements register" not in section


def test_subheading_does_not_end_the_section():
    """HMS-08 — a `###` inside §3 is part of it; only an `until` pattern ends a section.

    This is the whole reason it is not `md_table.rows_under_heading`, which stops at any heading.
    """
    assert "### AT1 — Design" in md_section.span(PLAN, r"^##\s+3\.", NUMBERED)
