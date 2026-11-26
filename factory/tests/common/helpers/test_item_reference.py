"""Cases HIR-01 .. HIR-36 — factory/docs/test-plan.md.

Two properties carry most of the weight. The pattern accepts **any** correctly-formed unit code, because
the factory is meant to serve any qualification — the codes below deliberately span three training
packages and an accredited course. And `find_all` does **not** de-duplicate, because the consolidation
gate counts occurrences to catch an item placed in two groups.

The resolution half (HIR-18 onward) is about what a *written* reference names: ranges, comma lists,
abbreviated references inheriting a unit, and compound references. Every coverage check downstream
counts items, so a compressed reference left unexpanded silently shrinks the register.
"""
import item_reference as R


# ---------------------------------------------------------------------------
# format()
# ---------------------------------------------------------------------------

def test_reference_renders_in_canonical_form():
    """HIR-01"""
    assert R.format("ICTCLD501", "PC", "1.2") == "[ICTCLD501 PC 1.2]"


def test_foundation_skill_numbering_keeps_its_spaces():
    """HIR-02 — an FS is referenced by its verbatim skill name, which contains spaces."""
    assert R.format("ICTCLD501", "FS", "Oral communication") == "[ICTCLD501 FS Oral communication]"


# ---------------------------------------------------------------------------
# first() — what a reference is, and what is not one
# ---------------------------------------------------------------------------

def test_well_formed_reference_is_parsed():
    """HIR-03"""
    assert R.first("- Confirm requirements [ICTCLD501 PC 1.2]") == ("ICTCLD501", "PC", "1.2")


def test_numbering_whitespace_is_stripped():
    """HIR-04"""
    assert R.first("[ICTCLD501 PE 3 ]") == ("ICTCLD501", "PE", "3")


def test_any_training_package_is_accepted():
    """HIR-05 — the whole point of the generalisation: HLT, CHC, SIT, anything correctly formed."""
    assert R.first("[HLTAAP001 PC 1.2]") == ("HLTAAP001", "PC", "1.2")
    assert R.first("[CHCCOM005 KE 4]") == ("CHCCOM005", "KE", "4")
    assert R.first("[BSBXTW401 FS Numeracy]") == ("BSBXTW401", "FS", "Numeracy")


def test_accredited_course_unit_code_is_accepted():
    """HIR-06 — a Victorian accredited unit, not a national training-package one."""
    assert R.first("[VU23226 PE 1]") == ("VU23226", "PE", "1")


def test_code_without_trailing_digits_is_not_a_reference():
    """HIR-07 — otherwise a bracketed word beside a section keyword would read as an item."""
    assert R.first("[NOTE PE 1]") is None
    assert R.first("[TBD KE 3]") is None


def test_course_code_is_not_a_unit_reference():
    """HIR-08 — 22603VIC is the accredited COURSE; its units are the VU codes."""
    assert R.first("[22603VIC AC 1]") is None


def test_unrecognised_section_is_not_a_reference():
    """HIR-09 — the five sections are the whole vocabulary."""
    assert R.first("[ICTCLD501 XX 1]") is None


def test_text_without_a_reference_yields_none():
    """HIR-10 — the legacy copies went straight to .group(1) here and raised AttributeError."""
    assert R.first("- an item line that carries no reference at all") is None
    assert R.first("") is None


# ---------------------------------------------------------------------------
# find_all()
# ---------------------------------------------------------------------------

def test_every_reference_in_document_order():
    """HIR-11"""
    text = ("- Confirm requirements [ICTCLD501 PC 1.1]\n"
            "- Identify access needs [ICTCLD501 PC 1.2]\n"
            "- **Numeracy** — reads estimates [BSBXTW401 FS Numeracy]\n")
    assert R.find_all(text) == [
        ("ICTCLD501", "PC", "1.1"),
        ("ICTCLD501", "PC", "1.2"),
        ("BSBXTW401", "FS", "Numeracy"),
    ]


def test_line_without_a_reference_contributes_nothing():
    """HIR-12"""
    text = "**Why grouped:** these share the disaster-recovery competency.\n\n- item [ICTCLD501 PE 2]\n"
    assert R.find_all(text) == [("ICTCLD501", "PE", "2")]


def test_repeated_reference_is_not_deduplicated():
    """HIR-13 — the gate counts occurrences to catch an item placed in two groups."""
    text = "- item [ICTCLD501 PE 2]\n\n## Group 4\n\n- item [ICTCLD501 PE 2]\n"
    assert R.find_all(text) == [("ICTCLD501", "PE", "2")] * 2


# ---------------------------------------------------------------------------
# strip_code_spans()
# ---------------------------------------------------------------------------

def test_wrapped_reference_is_removed():
    """HIR-14 — editorial prose cites references in backticks; those are not items."""
    assert "ICTCLD501" not in R.strip_code_spans("covers `[ICTCLD501 PC 1.1]` and more")


def test_unwrapped_reference_survives():
    """HIR-15"""
    assert R.first(R.strip_code_spans("- item [ICTCLD501 PE 2]")) == ("ICTCLD501", "PE", "2")


def test_prose_around_a_removed_span_survives():
    """HIR-16"""
    assert R.strip_code_spans("covers `[ICTCLD501 PC 1.1]` and more") == "covers  and more"


def test_format_and_first_round_trip():
    """HIR-17 — the writer and the reader must agree; that is why they share a module."""
    for unit, section, numbering in (("ICTCLD501", "PC", "1.2"),
                                     ("HLTAAP001", "KE", "7"),
                                     ("BSBXTW401", "FS", "Oral communication"),
                                     ("VU23226", "AC", "1")):
        assert R.first(R.format(unit, section, numbering)) == (unit, section, numbering)


# ---------------------------------------------------------------------------
# expand() — a compressed numbering into its members
# ---------------------------------------------------------------------------

def test_plain_number_passes_through():
    """HIR-18"""
    assert R.expand("2.3") == ["2.3"]
    assert R.expand("7") == ["7"]


def test_integer_range_expands():
    """HIR-19 — a KE range names six items, and every coverage check counts items."""
    assert R.expand("1-6") == ["1", "2", "3", "4", "5", "6"]


def test_dotted_range_expands_within_its_major():
    """HIR-20"""
    assert R.expand("1.1-1.4") == ["1.1", "1.2", "1.3", "1.4"]


def test_comma_list_expands():
    """HIR-21"""
    assert R.expand("3, 4, 6") == ["3", "4", "6"]


def test_comma_list_containing_a_range_expands():
    """HIR-22"""
    assert R.expand("1, 3-5, 8") == ["1", "3", "4", "5", "8"]


def test_range_across_majors_yields_endpoints():
    """HIR-23 — 1.4-2.1 is not a range anyone means; do not invent 1.5 .. 1.9."""
    assert R.expand("1.4-2.1") == ["1.4", "2.1"]


def test_skill_name_passes_through():
    """HIR-24 — a Foundation Skill is referenced by its verbatim name."""
    assert R.expand("Oral communication") == ["Oral communication"]


def test_trailing_qualifier_is_dropped():
    """HIR-25 — `4.3 - partial` is still item 4.3."""
    assert R.expand("4.3 - partial") == ["4.3"]


# ---------------------------------------------------------------------------
# resolve() — every reference a line makes, expanded and attributed
# ---------------------------------------------------------------------------

def test_full_reference_resolves():
    """HIR-26"""
    assert list(R.resolve("- criterion [ICTCLD501 PC 1.2]")) == [
        (("ICTCLD501", "PC", "1.2"), "full")]


def test_abbreviated_reference_inherits_the_unit():
    """HIR-27 — authors write the unit once and abbreviate after it."""
    out = list(R.resolve("evidences [ICTCLD501 PC 1.1] and [PC 2.3]"))
    assert out == [(("ICTCLD501", "PC", "1.1"), "full"),
                   (("ICTCLD501", "PC", "2.3"), "abbrev")]


def test_abbreviated_without_a_unit_is_unresolved():
    """HIR-28 — no unit to inherit, so the unit is None and the form says so."""
    assert list(R.resolve("evidences [PC 2.1]")) == [((None, "PC", "2.1"), "unresolved")]


def test_compressed_reference_yields_each_member():
    """HIR-29"""
    out = list(R.resolve("[ICTCLD501 KE 1-3]"))
    assert out == [(("ICTCLD501", "KE", "1"), "compressed"),
                   (("ICTCLD501", "KE", "2"), "compressed"),
                   (("ICTCLD501", "KE", "3"), "compressed")]


def test_compound_reference_splits_on_the_middle_dot():
    """HIR-30 — two units named in one bracket."""
    out = [ref for ref, _form in R.resolve("[ICTCLD401 KE 1 · ICTCLD502 KE 1]")]
    assert out == [("ICTCLD401", "KE", "1"), ("ICTCLD502", "KE", "1")]


def test_compound_parts_are_classified_compressed():
    """HIR-31 — each part names one item, but the REFERENCE was compressed."""
    forms = {form for _ref, form in R.resolve("[ICTCLD401 KE 1 · ICTCLD502 KE 1]")}
    assert forms == {"compressed"}


def test_unit_inheritance_carries_across_brackets():
    """HIR-32 — the nearest preceding full reference wins, not the first on the line."""
    out = list(R.resolve("[ICTCLD501 PC 1.1] then [ICTCLD502 PC 1.1] then [PC 2.2]"))
    assert out[-1] == (("ICTCLD502", "PC", "2.2"), "abbrev")


def test_bracketed_prose_is_ignored():
    """HIR-33 — a bracket is not a reference; unresolved is for a real reference missing its unit."""
    assert list(R.resolve("see [the appendix] and [TBD] for detail")) == []


def test_references_are_yielded_in_line_order():
    """HIR-34"""
    out = [ref for ref, _form in R.resolve("[ICTCLD501 KE 2] [ICTCLD501 PC 1.1] [ICTCLD501 AC 1]")]
    assert out == [("ICTCLD501", "KE", "2"), ("ICTCLD501", "PC", "1.1"), ("ICTCLD501", "AC", "1")]


# ---------------------------------------------------------------------------
# valid_set() — the references a document defines
# ---------------------------------------------------------------------------

def test_valid_set_is_deduplicated():
    """HIR-35 — unlike find_all, this is a set: what exists, not how often."""
    text = "- a [ICTCLD501 PE 1]\n- b [ICTCLD501 PE 2]\n- a again [ICTCLD501 PE 1]\n"
    assert R.valid_set(text) == {("ICTCLD501", "PE", "1"), ("ICTCLD501", "PE", "2")}


def test_valid_set_excludes_wrapped_references():
    """HIR-36 — the preamble cites example references in backticks; those define nothing."""
    text = "Tags look like `[ICTCLD501 PC 1.1]`.\n\n- real item [ICTCLD501 PE 1]\n"
    assert R.valid_set(text) == {("ICTCLD501", "PE", "1")}
