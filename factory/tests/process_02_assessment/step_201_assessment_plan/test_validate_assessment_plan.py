"""Cases VAP-01 .. VAP-28 — factory/docs/test-plan.md.

The assessment plan is where a cluster decides WHAT WILL BE ASSESSED. An item no AT claims is an item
nobody builds an instrument for, and it surfaces much later as a coverage gap in a document nobody
expected to be short.

Cases run through the CLI, which is how the gate is used. Fixtures are a hand-written plan and a
hand-written consolidated UoC, so the expectations are independent of the parsers under test. The
format standard is the real one — the section list is driven by its skeleton, so a fixture skeleton
would be testing a document nobody uses.
"""
import subprocess
import sys
from pathlib import Path

from conftest import VALIDATOR

CONSOLIDATED = """\
# S1-CL9 Test Cluster — Consolidated UoC

> **STATUS: DRAFT.**

## Group 1 — Everything

- 1.1 Confirm requirements [ICTTEST101 PC 1.1]
- 1.2 Identify constraints [ICTTEST101 PC 1.2]
- 1.3 Agree the approach [ICTTEST101 PC 1.3]
- 1.4 Record the decision [ICTTEST101 PC 1.4]
- **Numeracy** — interprets estimates [ICTTEST101 FS Numeracy]
- configure two services [ICTTEST101 PE 1]
- industry standards [ICTTEST101 KE 1]
- cloud service models [ICTTEST101 KE 2]
- a cloud platform [ICTTEST101 AC 1]
"""

# Every PC/PE/KE/FS item above, claimed across two ATs. AC 1 is discharged via the SR register.
COVERAGE_AT1 = "[ICTTEST101 PC 1.1-1.4] · [ICTTEST101 FS Numeracy]"
COVERAGE_AT2 = "[ICTTEST101 PE 1] · [ICTTEST101 KE 1, 2]"


def plan(*, title="# S1-CL9 Test Cluster — Cluster Assessment Plan",
         status="> **STATUS: DRAFT.** A first pass.",
         binding="> **Scenario binding:** maps to the YAT scenario — see the scenario plan.",
         at_table="| AT | Working title | Mode | Format | Unit focus |\n| --- | --- | --- | --- | --- |\n| AT1 | Design | Individual | Report | ICTTEST101 el 1 |",
         at_blocks=None, sr_rows=None, sections=None) -> str:
    """A plan built from parts, so a case mutates exactly one thing."""
    if at_blocks is None:
        at_blocks = (
            f"### AT1 — Design\n"
            f"- **UoC coverage:** {COVERAGE_AT1}\n"
            f"- **Scenario requirements:** SR-CL9-01\n\n"
            f"### AT2 — Build\n"
            f"- **UoC coverage:** {COVERAGE_AT2}\n"
            f"- **Scenario requirements:** SR-CL9-02\n"
        )
    if sr_rows is None:
        sr_rows = ("| SR-CL9-01 | A baseline system | AT1 | [ICTTEST101 AC 1] |\n"
                   "| SR-CL9-02 | A stakeholder | AT2 | — |\n")
    if sections is None:
        sections = ["## 1. Integration approach", "## 2. Scenario", "## 3. Assessment structure",
                    "## 4. Provenance", "## 5. Coverage verification",
                    "## 6. Scenario requirements register", "## 7. Worklist",
                    "## 8. Open questions / TBDs", "## Changelog"]

    body = {
        "## 3. Assessment structure": f"{at_table}\n\n{at_blocks}",
        "## 6. Scenario requirements register":
            "| SR | Condition | AT(s) | AC link |\n| --- | --- | --- | --- |\n" + sr_rows,
    }
    parts = [p for p in (title, status, binding) if p]
    for heading in sections:
        parts.append(f"\n{heading}\n")
        parts.append(body.get(heading, "Prose for this section."))
    return "\n".join(parts) + "\n"


def build(tmp_path, plan_text=None, consolidated=CONSOLIDATED) -> Path:
    cluster = tmp_path / "S1-CL9-Test"
    (cluster / "assessments").mkdir(parents=True, exist_ok=True)
    (cluster / "assessments" / "assessment_plan.md").write_text(
        plan() if plan_text is None else plan_text, encoding="utf-8")
    if consolidated is not None:
        (cluster / "consolidated_uoc.md").write_text(consolidated, encoding="utf-8")
    return cluster


def run(cluster: Path, *extra) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(VALIDATOR), "--cluster", str(cluster), *extra],
                          capture_output=True, text=True)


# ---------------------------------------------------------------------------
# Format — structure
# ---------------------------------------------------------------------------

def test_a_well_formed_plan_passes(tmp_path):
    """VAP-01 — the baseline. If this fails, every FAIL-side case below proves nothing."""
    result = run(build(tmp_path))
    assert result.returncode == 0, result.stdout


def test_missing_section_fails_naming_it(tmp_path):
    """VAP-02 — the section list comes from the format standard's skeleton."""
    sections = ["## 1. Integration approach", "## 2. Scenario", "## 3. Assessment structure",
                "## 4. Provenance", "## 6. Scenario requirements register", "## 7. Worklist",
                "## 8. Open questions / TBDs", "## Changelog"]
    result = run(build(tmp_path, plan(sections=sections)))
    assert result.returncode == 1
    assert "5. Coverage verification" in result.stdout


def test_sections_out_of_order_fail(tmp_path):
    """VAP-03 — a plan read out of order is a plan whose reader loses the thread."""
    sections = ["## 2. Scenario", "## 1. Integration approach", "## 3. Assessment structure",
                "## 4. Provenance", "## 5. Coverage verification",
                "## 6. Scenario requirements register", "## 7. Worklist",
                "## 8. Open questions / TBDs", "## Changelog"]
    result = run(build(tmp_path, plan(sections=sections)))
    assert result.returncode == 1
    assert "order" in result.stdout.lower()


def test_missing_status_line_fails(tmp_path):
    """VAP-04 — the plan is a proposal until someone says otherwise; the banner is where it says so."""
    result = run(build(tmp_path, plan(status="")))
    assert result.returncode == 1 and "STATUS" in result.stdout


def test_missing_scenario_binding_fails(tmp_path):
    """VAP-05 — an unbound plan cannot be cross-checked against a scenario."""
    result = run(build(tmp_path, plan(binding="")))
    assert result.returncode == 1 and "Scenario binding" in result.stdout


def test_missing_title_fails(tmp_path):
    """VAP-06"""
    result = run(build(tmp_path, plan(title="")))
    assert result.returncode == 1 and "title" in result.stdout.lower()


# ---------------------------------------------------------------------------
# Section 3 — the AT structure
# ---------------------------------------------------------------------------

def test_no_at_table_row_fails(tmp_path):
    """VAP-07 — the roster table is how a reader sees the shape of the assessment at a glance."""
    table = "| AT | Working title | Mode | Format | Unit focus |\n| --- | --- | --- | --- | --- |"
    result = run(build(tmp_path, plan(at_table=table)))
    assert result.returncode == 1 and "AT table" in result.stdout


def test_no_per_at_blocks_fail(tmp_path):
    """VAP-08 — without per-AT blocks nothing declares coverage, so nothing can be checked."""
    result = run(build(tmp_path, plan(at_blocks="No detail blocks here.\n")))
    assert result.returncode == 1 and "ATn" in result.stdout


def test_at_without_uoc_coverage_fails_naming_it(tmp_path):
    """VAP-09"""
    blocks = ("### AT1 — Design\n- **Scenario requirements:** SR-CL9-01\n\n"
              f"### AT2 — Build\n- **UoC coverage:** {COVERAGE_AT2}\n"
              "- **Scenario requirements:** SR-CL9-02\n")
    result = run(build(tmp_path, plan(at_blocks=blocks)))
    assert result.returncode == 1
    assert "AT1" in result.stdout and "UoC coverage" in result.stdout


def test_at_without_scenario_requirements_fails_naming_it(tmp_path):
    """VAP-10"""
    blocks = (f"### AT1 — Design\n- **UoC coverage:** {COVERAGE_AT1}\n\n"
              f"### AT2 — Build\n- **UoC coverage:** {COVERAGE_AT2}\n"
              "- **Scenario requirements:** SR-CL9-01 · SR-CL9-02\n")
    result = run(build(tmp_path, plan(at_blocks=blocks)))
    assert result.returncode == 1
    assert "AT1" in result.stdout and "Scenario requirements" in result.stdout


def test_unresolved_reference_fails_naming_it(tmp_path):
    """VAP-11 — an abbreviated reference with no unit to inherit names nothing."""
    blocks = ("### AT1 — Design\n- **UoC coverage:** [PC 1.1]\n"
              "- **Scenario requirements:** SR-CL9-01\n\n"
              f"### AT2 — Build\n- **UoC coverage:** {COVERAGE_AT2}\n"
              "- **Scenario requirements:** SR-CL9-02\n")
    result = run(build(tmp_path, plan(at_blocks=blocks)))
    assert result.returncode == 1 and "unresolved" in result.stdout.lower()


# ---------------------------------------------------------------------------
# Section 6 — the SR register
# ---------------------------------------------------------------------------

def test_empty_sr_register_fails(tmp_path):
    """VAP-12 — the register is the contract the scenario plan is validated against."""
    result = run(build(tmp_path, plan(sr_rows="")))
    assert result.returncode == 1 and "SR" in result.stdout


def test_foreign_cluster_sr_id_fails(tmp_path):
    """VAP-13 — SR ids are cluster-scoped; a borrowed id makes the union ambiguous."""
    rows = ("| SR-CL9-01 | A baseline system | AT1 | — |\n"
            "| SR-CL2-02 | A stakeholder | AT2 | — |\n")
    blocks = (f"### AT1 — Design\n- **UoC coverage:** {COVERAGE_AT1}\n"
              "- **Scenario requirements:** SR-CL9-01\n\n"
              f"### AT2 — Build\n- **UoC coverage:** {COVERAGE_AT2}\n"
              "- **Scenario requirements:** SR-CL2-02\n")
    result = run(build(tmp_path, plan(sr_rows=rows, at_blocks=blocks)))
    assert result.returncode == 1 and "SR-CL2-02" in result.stdout


def test_undefined_sr_reference_fails(tmp_path):
    """VAP-14 — an AT depending on something the register never asks the scenario to build."""
    blocks = (f"### AT1 — Design\n- **UoC coverage:** {COVERAGE_AT1}\n"
              "- **Scenario requirements:** SR-CL9-01 · SR-CL9-09\n\n"
              f"### AT2 — Build\n- **UoC coverage:** {COVERAGE_AT2}\n"
              "- **Scenario requirements:** SR-CL9-02\n")
    result = run(build(tmp_path, plan(at_blocks=blocks)))
    assert result.returncode == 1 and "SR-CL9-09" in result.stdout


def test_unreferenced_sr_is_advisory(tmp_path):
    """VAP-15 — world-building the scenario supplies but no AT leans on is allowed, not an error."""
    rows = ("| SR-CL9-01 | A baseline system | AT1 | — |\n"
            "| SR-CL9-02 | A stakeholder | AT2 | — |\n"
            "| SR-CL9-03 | An unused prop | — | — |\n")
    result = run(build(tmp_path, plan(sr_rows=rows)))
    assert result.returncode == 0, result.stdout
    assert "SR-CL9-03" in result.stdout


# ---------------------------------------------------------------------------
# Coverage
# ---------------------------------------------------------------------------

def test_full_coverage_passes(tmp_path):
    """VAP-16"""
    result = run(build(tmp_path))
    assert result.returncode == 0 and "COVERAGE: PASS" in result.stdout


def test_uncovered_pc_is_missing(tmp_path):
    """VAP-17 — a performance criterion no AT claims is a requirement nobody assesses."""
    blocks = (f"### AT1 — Design\n- **UoC coverage:** [ICTTEST101 PC 1.1-1.3] · "
              "[ICTTEST101 FS Numeracy]\n- **Scenario requirements:** SR-CL9-01\n\n"
              f"### AT2 — Build\n- **UoC coverage:** {COVERAGE_AT2}\n"
              "- **Scenario requirements:** SR-CL9-02\n")
    result = run(build(tmp_path, plan(at_blocks=blocks)))
    assert result.returncode == 1
    assert "MISSING" in result.stdout and "PC 1.4" in result.stdout


def test_uncovered_ke_is_missing(tmp_path):
    """VAP-18"""
    blocks = (f"### AT1 — Design\n- **UoC coverage:** {COVERAGE_AT1}\n"
              "- **Scenario requirements:** SR-CL9-01\n\n"
              "### AT2 — Build\n- **UoC coverage:** [ICTTEST101 PE 1] · [ICTTEST101 KE 1]\n"
              "- **Scenario requirements:** SR-CL9-02\n")
    result = run(build(tmp_path, plan(at_blocks=blocks)))
    assert result.returncode == 1
    assert "MISSING" in result.stdout and "KE 2" in result.stdout


def test_phantom_reference_fails(tmp_path):
    """VAP-19 — claiming an item no unit contains: a typo, or a stale number after a reissue."""
    blocks = (f"### AT1 — Design\n- **UoC coverage:** {COVERAGE_AT1} · [ICTTEST101 PC 9.9]\n"
              "- **Scenario requirements:** SR-CL9-01\n\n"
              f"### AT2 — Build\n- **UoC coverage:** {COVERAGE_AT2}\n"
              "- **Scenario requirements:** SR-CL9-02\n")
    result = run(build(tmp_path, plan(at_blocks=blocks)))
    assert result.returncode == 1
    assert "PHANTOM" in result.stdout and "PC 9.9" in result.stdout


def test_ac_items_are_informational(tmp_path):
    """VAP-20 — AC is discharged through the SR register, so claiming one is noted, not required.

    The consolidated UoC carries AC 1 and the baseline plan claims nothing AC — that alone must not
    fail. Claiming it explicitly is also fine, and is reported as information.
    """
    assert run(build(tmp_path)).returncode == 0        # unclaimed AC does not fail the plan

    blocks = (f"### AT1 — Design\n- **UoC coverage:** {COVERAGE_AT1} · [ICTTEST101 AC 1]\n"
              "- **Scenario requirements:** SR-CL9-01\n\n"
              f"### AT2 — Build\n- **UoC coverage:** {COVERAGE_AT2}\n"
              "- **Scenario requirements:** SR-CL9-02\n")
    result = run(build(tmp_path, plan(at_blocks=blocks)))
    assert result.returncode == 0, result.stdout
    assert "AC" in result.stdout                        # counted as info, not as a requirement


def test_compressed_reference_covers_every_member(tmp_path):
    """VAP-21 — [PC 1.1-1.4] is four items. Read as one, three requirements go unassessed silently.

    Asserting the COUNT is what proves expansion happened: 4 PC + 1 FS + 1 PE + 2 KE = 8 required
    items. Unexpanded, the plan would claim five and three PCs would report MISSING.
    """
    result = run(build(tmp_path))
    assert result.returncode == 0, result.stdout
    assert "8" in result.stdout and "MISSING" not in result.stdout


def test_abbreviated_reference_counts_as_coverage(tmp_path):
    """VAP-22 — the unit is named once and inherited by what follows on the line."""
    blocks = ("### AT1 — Design\n- **UoC coverage:** [ICTTEST101 PC 1.1] · [PC 1.2-1.4] · "
              "[FS Numeracy]\n- **Scenario requirements:** SR-CL9-01\n\n"
              f"### AT2 — Build\n- **UoC coverage:** {COVERAGE_AT2}\n"
              "- **Scenario requirements:** SR-CL9-02\n")
    result = run(build(tmp_path, plan(at_blocks=blocks)))
    assert result.returncode == 0, result.stdout


def test_absent_consolidated_skips_coverage(tmp_path):
    """VAP-23 — reported as skipped, not silently passed and not failed."""
    result = run(build(tmp_path, consolidated=None))
    assert "SKIPPED" in result.stdout


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def test_cli_exits_zero_on_a_good_plan(tmp_path):
    """VAP-24"""
    result = run(build(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "RESULT: PASS" in result.stdout


def test_cli_exits_one_on_a_format_failure(tmp_path):
    """VAP-25"""
    result = run(build(tmp_path, plan(status="")))
    assert result.returncode == 1 and "RESULT: FAIL" in result.stdout


def test_cli_exits_one_on_a_coverage_failure(tmp_path):
    """VAP-26 — a well-formed plan that leaves a requirement unassessed still fails."""
    blocks = (f"### AT1 — Design\n- **UoC coverage:** [ICTTEST101 PC 1.1]\n"
              "- **Scenario requirements:** SR-CL9-01\n\n"
              f"### AT2 — Build\n- **UoC coverage:** {COVERAGE_AT2}\n"
              "- **Scenario requirements:** SR-CL9-02\n")
    result = run(build(tmp_path, plan(at_blocks=blocks)))
    assert result.returncode == 1
    assert "FORMAT: PASS" in result.stdout and "COVERAGE: FAIL" in result.stdout


def test_cli_exits_two_on_a_missing_plan(tmp_path):
    """VAP-27 — a missing plan is an unreadable input, distinct from a plan with defects."""
    cluster = build(tmp_path)
    (cluster / "assessments" / "assessment_plan.md").unlink()
    result = run(cluster)
    assert result.returncode == 2
    assert "assessment_plan.md" in (result.stdout + result.stderr)


def test_cli_path_overrides_are_honoured(tmp_path):
    """VAP-28 — a plan and a consolidated UoC that live outside the conventional layout."""
    cluster = build(tmp_path)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    moved_plan = elsewhere / "plan.md"
    moved_plan.write_text(plan(), encoding="utf-8")
    moved_uoc = elsewhere / "uoc.md"
    moved_uoc.write_text(CONSOLIDATED, encoding="utf-8")
    (cluster / "assessments" / "assessment_plan.md").unlink()
    (cluster / "consolidated_uoc.md").unlink()

    result = run(cluster, "--plan", str(moved_plan), "--consolidated", str(moved_uoc))
    assert result.returncode == 0, result.stdout + result.stderr
