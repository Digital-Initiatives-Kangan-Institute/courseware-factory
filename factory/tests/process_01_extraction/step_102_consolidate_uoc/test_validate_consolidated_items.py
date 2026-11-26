"""Cases VCI-01 .. VCI-26 — factory/docs/test-plan.md.

`consolidated_uoc.md` is the last point where the source of truth is still checkable: nothing downstream
reads the units again. An item lost here does not surface later as a gap — it surfaces as 100% coverage
of a set that is quietly short.

Cases run through the CLI, which is the shape the gate is actually used in, and leaves the internals free
to change. Fixtures are unit `.md` and consolidated `.md` written by hand, so the expectations are
independent of the parsers under test.
"""
import subprocess
import sys
from pathlib import Path

import pytest
from conftest import ITEMS_VALIDATOR

UNIT_A = """# ICTTEST101 Configure cloud services

## Elements and Performance Criteria

| ELEMENTS | PERFORMANCE CRITERIA |
| --- | --- |
| Elements describe the essential outcomes. | Performance criteria describe the performance. |
| 1. Prepare | 1.1 Confirm cloud service requirements with the client<br>1.2 Identify security and access requirements |

## Foundation Skills

| SKILL | DESCRIPTION |
| --- | --- |
| Oral communication | Presents information using clear language |

## Performance Evidence

The candidate must demonstrate the ability to:

- configure two cloud services
- document the configuration

## Knowledge Evidence

- industry standards used in cloud computing
- functions and differences of cloud models, including:
  - public cloud
  - private cloud

## Assessment Conditions

- cloud vendor service provider

Assessors of this unit must satisfy the requirements for assessors.

## Links

Companion volume implementation guides are found at the link.
"""

UNIT_B = """# ICTTEST202 Monitor cloud services

## Elements and Performance Criteria

| ELEMENTS | PERFORMANCE CRITERIA |
| --- | --- |
| Elements describe the essential outcomes. | Performance criteria describe the performance. |
| 1. Monitor | 1.1 Review service metrics against agreed targets |

## Foundation Skills

| SKILL | DESCRIPTION |
| --- | --- |
| Reading | Interprets technical documentation |

## Performance Evidence

- report on service performance

## Knowledge Evidence

- monitoring tools available on a cloud platform

## Assessment Conditions

- access to monitoring tooling

Assessors of this unit must satisfy the requirements for assessors.

## Links

Companion volume implementation guides are found at the link.
"""

# The faithful consolidation: the editorial layer, with every item line as the extractor emits it.
ITEMS = [
    "- 1.1 Confirm cloud service requirements with the client [ICTTEST101 PC 1.1]",
    "- 1.2 Identify security and access requirements [ICTTEST101 PC 1.2]",
    "- **Oral communication** — Presents information using clear language [ICTTEST101 FS Oral communication]",
    "- configure two cloud services [ICTTEST101 PE 1]",
    "- document the configuration [ICTTEST101 PE 2]",
    "- industry standards used in cloud computing [ICTTEST101 KE 1]",
    "- functions and differences of cloud models, including: [ICTTEST101 KE 2]\n"
    "  - public cloud\n  - private cloud",
    "- cloud vendor service provider [ICTTEST101 AC 1]",
    "- Assessors of this unit must satisfy the requirements for assessors. [ICTTEST101 AC 2]",
    "- 1.1 Review service metrics against agreed targets [ICTTEST202 PC 1.1]",
    "- **Reading** — Interprets technical documentation [ICTTEST202 FS Reading]",
    "- report on service performance [ICTTEST202 PE 1]",
    "- monitoring tools available on a cloud platform [ICTTEST202 KE 1]",
    "- access to monitoring tooling [ICTTEST202 AC 1]",
    "- Assessors of this unit must satisfy the requirements for assessors. [ICTTEST202 AC 2]",
]

PREAMBLE = """# S1-CL9 Test Cluster — Consolidated UoC

> **STATUS: DRAFT.** Every assessable item quoted verbatim and referenced `[UNIT SECTION numbering]` —
> for example `[ICTTEST101 PC 1.1]` or `[ICTTEST202 KE 1]`.

## Group 1 — Preparing and configuring

**Why grouped:** one artefact could plausibly evidence the whole group.

"""


def consolidated(items=None) -> str:
    return PREAMBLE + "\n".join(ITEMS if items is None else items) + "\n"


def build(tmp_path, doc=None, unit_a=UNIT_A, unit_b=UNIT_B) -> Path:
    """A cluster laid out the way the validator expects to find one."""
    cluster = tmp_path / "S1-CL9-Test"
    (cluster / "units_of_competency").mkdir(parents=True)
    (cluster / "units_of_competency/ICTTEST101.md").write_text(unit_a, encoding="utf-8")
    (cluster / "units_of_competency/ICTTEST202.md").write_text(unit_b, encoding="utf-8")
    (cluster / "consolidated_uoc.md").write_text(
        consolidated() if doc is None else doc, encoding="utf-8")
    return cluster


def run(cluster: Path, assessor_ac=True, units=None) -> subprocess.CompletedProcess:
    units = units or ["ICTTEST101=units_of_competency/ICTTEST101.md",
                      "ICTTEST202=units_of_competency/ICTTEST202.md"]
    args = [sys.executable, str(ITEMS_VALIDATOR), "--cluster", str(cluster)]
    for unit in units:
        args += ["--unit", unit]
    if assessor_ac:
        args.append("--assessor-ac")
    return subprocess.run(args, capture_output=True, text=True)


def without(reference: str) -> list[str]:
    return [i for i in ITEMS if f"[{reference}]" not in i]


def replace(reference: str, new_line: str) -> list[str]:
    return [new_line if f"[{reference}]" in i else i for i in ITEMS]


# ---------------------------------------------------------------------------
# Baseline — the gate must not cry wolf on the editorial layer
# ---------------------------------------------------------------------------

def test_a_faithful_consolidation_passes(tmp_path):
    """VCI-01 — if this fails, every FAIL-side case below proves nothing."""
    result = run(build(tmp_path))
    assert result.returncode == 0, result.stdout


def test_editorial_prose_is_not_treated_as_items(tmp_path):
    """VCI-02 — group headings, rationale and status notes appear in no unit."""
    result = run(build(tmp_path))
    assert result.returncode == 0, result.stdout
    assert "UNEXPECTED" not in result.stdout


def test_backticked_example_references_are_not_occurrences(tmp_path):
    """VCI-03 — the preamble cites two real references inside code spans."""
    result = run(build(tmp_path))
    assert result.returncode == 0, result.stdout
    assert "DUPLICATED" not in result.stdout


def test_an_editorial_bullet_citing_references_is_not_an_item(tmp_path):
    """VCI-04 — prose ABOUT an item is not the item, and its text is not the unit's text.

    Placed before the real items so it would win if it were counted.
    """
    doc = (PREAMBLE
           + "- **AT1 — Design** — evidences `[ICTTEST101 PC 1.1]` and `[ICTTEST101 PE 1]`.\n\n"
           + "\n".join(ITEMS) + "\n")
    result = run(build(tmp_path, doc))
    assert result.returncode == 0, result.stdout


# ---------------------------------------------------------------------------
# MISSING — nothing lost
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("reference", ["ICTTEST101 PC 1.2", "ICTTEST101 FS Oral communication",
                                       "ICTTEST101 PE 2", "ICTTEST101 KE 1", "ICTTEST101 AC 1"])
def test_a_dropped_item_is_missing(tmp_path, reference):
    """VCI-05 — one item lost from each section; each is a different parse path."""
    result = run(build(tmp_path, consolidated(without(reference))))
    assert result.returncode == 1
    assert "MISSING" in result.stdout and reference in result.stdout


def test_a_dropped_unit_is_missing_throughout(tmp_path):
    """VCI-06"""
    result = run(build(tmp_path, consolidated([i for i in ITEMS if "ICTTEST202" not in i])))
    assert result.returncode == 1
    assert result.stdout.count("ICTTEST202") >= 6


def test_assessor_paragraph_required_when_the_flag_is_set(tmp_path):
    """VCI-07"""
    result = run(build(tmp_path, consolidated(without("ICTTEST101 AC 2"))))
    assert result.returncode == 1 and "ICTTEST101 AC 2" in result.stdout


def test_a_backticked_item_reference_does_not_count_as_present(tmp_path):
    """VCI-08 — references count only unwrapped, so a code-spanned one reads as MISSING."""
    doc = consolidated(replace("ICTTEST101 PE 1",
                               "- configure two cloud services `[ICTTEST101 PE 1]`"))
    result = run(build(tmp_path, doc))
    assert result.returncode == 1 and "ICTTEST101 PE 1" in result.stdout


def test_an_empty_consolidation_is_not_a_pass(tmp_path):
    """VCI-09"""
    result = run(build(tmp_path, PREAMBLE))
    assert result.returncode == 1 and "MISSING" in result.stdout


# ---------------------------------------------------------------------------
# UNEXPECTED and DUPLICATED
# ---------------------------------------------------------------------------

def test_a_phantom_item_number_is_unexpected(tmp_path):
    """VCI-10"""
    result = run(build(tmp_path, consolidated(ITEMS + ["- invented criterion [ICTTEST101 PC 9.9]"])))
    assert result.returncode == 1 and "UNEXPECTED" in result.stdout and "PC 9.9" in result.stdout


def test_an_item_from_outside_the_cluster_is_unexpected(tmp_path):
    """VCI-11"""
    result = run(build(tmp_path, consolidated(ITEMS + ["- borrowed item [ICTCLD999 KE 1]"])))
    assert result.returncode == 1 and "UNEXPECTED" in result.stdout


def test_the_same_item_in_two_groups_is_duplicated(tmp_path):
    """VCI-12"""
    doc = consolidated(ITEMS + ["\n## Group 2 — Also relevant\n",
                                "- configure two cloud services [ICTTEST101 PE 1]"])
    result = run(build(tmp_path, doc))
    assert result.returncode == 1 and "DUPLICATED" in result.stdout


# ---------------------------------------------------------------------------
# MISTRANSCRIBED — the item's text is the source's text
# ---------------------------------------------------------------------------

def test_a_reworded_item_fails(tmp_path):
    """VCI-13 — present, exactly once, correctly referenced, and no longer what the unit says."""
    doc = consolidated(replace("ICTTEST101 PC 1.1",
                               "- 1.1 Check the client's cloud requirements [ICTTEST101 PC 1.1]"))
    result = run(build(tmp_path, doc))
    assert result.returncode == 1, result.stdout
    assert "ICTTEST101 PC 1.1" in result.stdout


def test_a_truncated_item_fails(tmp_path):
    """VCI-14"""
    doc = consolidated(replace("ICTTEST101 PC 1.1",
                               "- 1.1 Confirm cloud service [ICTTEST101 PC 1.1]"))
    result = run(build(tmp_path, doc))
    assert result.returncode == 1, result.stdout
    assert "MISTRANSCRIBED" in result.stdout and "ICTTEST101 PC 1.1" in result.stdout


def test_dropped_sub_bullets_fail(tmp_path):
    """VCI-15 — the defect found in CL1: parent kept, children dropped, the item left on a colon."""
    doc = consolidated(replace(
        "ICTTEST101 KE 2",
        "- functions and differences of cloud models, including: [ICTTEST101 KE 2]"))
    result = run(build(tmp_path, doc))
    assert result.returncode == 1, result.stdout
    assert "ICTTEST101 KE 2" in result.stdout


def test_swapped_references_fail(tmp_path):
    """VCI-16 — both present, both once, each carrying the other's reference.

    Reference presence alone reports a clean sweep, which is why identity has to be checked.
    """
    doc = consolidated([
        "- configure two cloud services [ICTTEST101 PE 2]" if "[ICTTEST101 PE 1]" in i else
        "- document the configuration [ICTTEST101 PE 1]" if "[ICTTEST101 PE 2]" in i else i
        for i in ITEMS])
    result = run(build(tmp_path, doc))
    assert result.returncode == 1, result.stdout
    assert "MISTRANSCRIBED" in result.stdout, result.stdout
    for label in ("MISSING", "UNEXPECTED", "DUPLICATED"):
        assert label not in result.stdout, result.stdout


def test_a_cosmetic_difference_passes(tmp_path):
    """VCI-17 — a smart apostrophe is Word's, not the author's."""
    unit = UNIT_A.replace("- configure two cloud services",
                          "- configure the business’s two services")
    doc = consolidated(replace("ICTTEST101 PE 1",
                               "- configure the business's two services [ICTTEST101 PE 1]"))
    result = run(build(tmp_path, doc, unit_a=unit))
    assert result.returncode == 0, result.stdout


# ---------------------------------------------------------------------------
# Grouping invariance — the judgement layer must not move the verdict
# ---------------------------------------------------------------------------

def test_regrouping_does_not_change_the_verdict(tmp_path):
    """VCI-18 — the same register, differently arranged."""
    shuffled = list(reversed(ITEMS))
    doc = (PREAMBLE + "\n".join(shuffled[:5])
           + "\n\n## Group 2 — Monitoring\n\n" + "\n".join(shuffled[5:]) + "\n")
    result = run(build(tmp_path, doc))
    assert result.returncode == 0, result.stdout


def test_renaming_group_headings_does_not_change_the_verdict(tmp_path):
    """VCI-19"""
    doc = consolidated().replace("Group 1 — Preparing and configuring", "Topic 4 — Something else")
    result = run(build(tmp_path, doc))
    assert result.returncode == 0, result.stdout


# ---------------------------------------------------------------------------
# Harness
# ---------------------------------------------------------------------------

def test_every_defect_class_is_reported_in_one_run(tmp_path):
    """VCI-20 — a run must not stop at the first class; the human fixes the document at once."""
    items = without("ICTTEST101 PE 2") + [
        "- invented [ICTTEST101 PC 9.9]",
        "- industry standards used in cloud computing [ICTTEST101 KE 1]"]
    result = run(build(tmp_path, consolidated(items)))
    assert result.returncode == 1
    for label in ("MISSING", "UNEXPECTED", "DUPLICATED"):
        assert label in result.stdout, result.stdout


def test_a_missing_consolidated_file_is_an_error(tmp_path):
    """VCI-21 — and it names the file, so the human knows what to go and look for."""
    cluster = build(tmp_path)
    (cluster / "consolidated_uoc.md").unlink()
    result = run(cluster)
    assert result.returncode == 2, result.stdout
    assert "consolidated_uoc.md" in result.stderr


def test_an_absent_section_is_an_error_naming_it(tmp_path):
    """VCI-22 — the expected set must never shrink silently.

    It surfaces as an ERROR naming the section, not a pile of phantom UNEXPECTED references: the
    message is what tells the human the unit .md is at fault rather than the consolidation.

    Widened during the port. The legacy case renamed the heading's CASE, which errored because the
    legacy extractor matched case-sensitively; the ported one is case-insensitive, so the case had to
    become a genuinely absent section to still test the intent.
    """
    result = run(build(tmp_path, unit_a=UNIT_A.replace("## Knowledge Evidence", "## Background")))
    assert result.returncode == 2, result.stdout
    assert "ERROR" in result.stderr and "Knowledge Evidence" in result.stderr


def test_assessor_ac_off_does_not_expect_the_trailing_paragraph(tmp_path):
    """VCI-23"""
    doc = consolidated([i for i in ITEMS if "AC 2]" not in i])
    result = run(build(tmp_path, doc), assessor_ac=False)
    assert result.returncode == 0, result.stdout


def test_any_training_package_validates(tmp_path):
    """VCI-24 — the generalisation proving itself at the gate, not only in the helper.

    HLT is a real training package the legacy allow-list would have crashed on.
    """
    unit = UNIT_A.replace("ICTTEST101", "HLTAAP001")
    doc = consolidated([i.replace("ICTTEST101", "HLTAAP001") for i in ITEMS
                        if "ICTTEST202" not in i])
    cluster = tmp_path / "S1-CL9-Test"
    (cluster / "units_of_competency").mkdir(parents=True)
    (cluster / "units_of_competency/HLTAAP001.md").write_text(unit, encoding="utf-8")
    (cluster / "consolidated_uoc.md").write_text(doc, encoding="utf-8")
    result = run(cluster, units=["HLTAAP001=units_of_competency/HLTAAP001.md"])
    assert result.returncode == 0, result.stdout + result.stderr


def test_unit_paths_resolve_relative_or_absolute(tmp_path):
    """VCI-25 — relative to the cluster dir, or absolute as given."""
    cluster = build(tmp_path)
    absolute = cluster / "units_of_competency/ICTTEST202.md"
    result = run(cluster, units=["ICTTEST101=units_of_competency/ICTTEST101.md",
                                 f"ICTTEST202={absolute}"])
    assert result.returncode == 0, result.stdout + result.stderr


def test_a_malformed_unit_argument_is_an_error(tmp_path):
    """VCI-26 — a bare path with no code would build an expected set with no references."""
    cluster = build(tmp_path)
    result = run(cluster, units=["units_of_competency/ICTTEST101.md"])
    assert result.returncode == 2, result.stdout
    assert "--unit" in result.stderr
