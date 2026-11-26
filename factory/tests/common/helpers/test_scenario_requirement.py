"""Cases HSR-01 .. HSR-10 — factory/docs/test-plan.md.

The fixture is shaped like the places SR references actually appear: a §6 register table with bold ids,
and a §3 per-AT block referencing them in prose.
"""
import scenario_requirement as SR

REGISTER = """\
## 3. Assessment structure

### AT1 — Design

Scenario requirements: SR-CL9-01, SR-CL9-03

## 6. Scenario requirements register

| SR | Condition | Why | Where |
| --- | --- | --- | --- |
| **SR-CL9-01** | An intranet page | AT1 reads it | website |
| **SR-CL9-02** | A lab artefact | AT2 deploys it | lab-pack |
| **SR-CL9-03** | A named stakeholder | AT1 interviews them | website |
"""


# ---------------------------------------------------------------------------
# find_all()
# ---------------------------------------------------------------------------

def test_every_reference_in_document_order():
    """HSR-01"""
    assert SR.find_all(REGISTER) == [
        "SR-CL9-01", "SR-CL9-03",                       # §3 references
        "SR-CL9-01", "SR-CL9-02", "SR-CL9-03",          # §6 definitions
    ]


def test_reference_is_returned_as_written():
    """HSR-02 — padding is the author's; do not normalise it away."""
    assert SR.find_all("satisfies SR-CL9-07") == ["SR-CL9-07"]
    assert SR.find_all("satisfies SR-CL9-7") == ["SR-CL9-7"]


def test_repeated_reference_is_not_deduplicated():
    """HSR-03 — callers dedupe when they want a set; both callers compare sets of refs vs defs."""
    assert SR.find_all("SR-CL9-01 and again SR-CL9-01") == ["SR-CL9-01", "SR-CL9-01"]


def test_text_without_a_reference_yields_nothing():
    """HSR-04"""
    assert SR.find_all("**Why grouped:** one artefact could evidence the group.") == []


def test_reference_in_a_bold_table_cell_is_found():
    """HSR-05 — the register renders ids bold, and that must not hide them."""
    assert SR.find_all("| **SR-CL9-02** | A lab artefact |") == ["SR-CL9-02"]


def test_malformed_id_is_not_a_reference():
    """HSR-06 — a partial id is a typo to surface, not a reference to resolve."""
    assert SR.find_all("SR-CL9 and SR--01 and SR-9-01") == []


def test_cluster_token_is_any_letters_then_digits():
    """HSR-07 — ten clusters must not break the format."""
    assert SR.find_all("SR-CL10-01 SR-CYB2-14") == ["SR-CL10-01", "SR-CYB2-14"]


# ---------------------------------------------------------------------------
# parse()
# ---------------------------------------------------------------------------

def test_id_parses_into_its_components():
    """HSR-08"""
    assert SR.parse("SR-CL9-01") == ("CL", 9, 1)


def test_parse_sorts_numerically():
    """HSR-09 — sorted as strings, SR-CL10-01 lands before SR-CL2-01 and the register mis-orders."""
    ids = ["SR-CL10-01", "SR-CL2-01", "SR-CL9-99", "SR-CL2-10", "SR-CL2-02"]
    assert sorted(ids, key=SR.parse) == [
        "SR-CL2-01", "SR-CL2-02", "SR-CL2-10", "SR-CL9-99", "SR-CL10-01"]
    assert sorted(ids) != sorted(ids, key=SR.parse)     # the fixture proves the hazard is real


def test_malformed_id_parses_to_none():
    """HSR-10"""
    assert SR.parse("SR-CL9") is None
    assert SR.parse("") is None
