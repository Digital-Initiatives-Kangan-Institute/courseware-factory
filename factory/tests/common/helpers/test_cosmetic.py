"""Cases HCOS-01 .. HCOS-10 — factory/docs/test-plan.md.

Every character under test is written as an escape rather than pasted. Three of them — the soft hyphen,
the byte-order mark and the non-breaking space — are invisible in a source file, so a literal would be
unreadable and an editor tidying the file could change one without anyone seeing.
"""
import cosmetic

LSQUO, RSQUO = "‘", "’"          # ' '
LDQUO, RDQUO = "“", "”"          # " "
EN, EM, MINUS, NBHYPHEN = "–", "—", "−", "‑"
NBSP = " "
ELLIPSIS = "…"
SOFT_HYPHEN = "­"
BOM = "﻿"


def test_curly_single_quotes_become_straight():
    """HCOS-01"""
    assert cosmetic.normalise(f"the candidate{RSQUO}s work") == "the candidate's work"
    assert cosmetic.normalise(f"{LSQUO}scoped{RSQUO}") == "'scoped'"


def test_curly_double_quotes_become_straight():
    """HCOS-02"""
    assert cosmetic.normalise(f"{LDQUO}as scoped{RDQUO}") == '"as scoped"'


def test_every_dash_becomes_a_plain_hyphen():
    """HCOS-03 — en, em, minus, non-breaking."""
    for dash in (EN, EM, MINUS, NBHYPHEN):
        assert cosmetic.normalise(f"cloud{dash}based") == "cloud-based"


def test_non_breaking_space_becomes_a_space():
    """HCOS-04"""
    assert cosmetic.normalise(f"2{NBSP}instances") == "2 instances"


def test_ellipsis_becomes_three_dots():
    """HCOS-05"""
    assert cosmetic.normalise(f"must{ELLIPSIS} continue") == "must... continue"


def test_soft_hyphen_is_removed():
    """HCOS-06 — invisible in Word, so it must not survive as a character."""
    assert cosmetic.normalise(f"config{SOFT_HYPHEN}uration") == "configuration"


def test_byte_order_mark_is_removed():
    """HCOS-07"""
    assert cosmetic.normalise(f"{BOM}Element 1") == "Element 1"


def test_decomposed_characters_are_composed():
    """HCOS-08 — the same visible text, typed two ways, must compare equal."""
    composed = "résumé"            # e-acute as one codepoint
    decomposed = "résumé"        # e + combining acute
    assert composed != decomposed            # the fixture is doing what it claims
    assert cosmetic.normalise(decomposed) == cosmetic.normalise(composed) == composed


def test_ordinary_text_is_unchanged():
    """HCOS-09 — including the whitespace, which is not this function's business."""
    text = "Confirm cloud service requirements\twith  the client\n1.2 Identify"
    assert cosmetic.normalise(text) == text


def test_normalising_is_idempotent():
    """HCOS-10 — no substitution may produce a character another substitution then changes."""
    text = f"{BOM}{LDQUO}the candidate{RSQUO}s{RDQUO} work {EN} e{NBHYPHEN}learning{ELLIPSIS} " \
           f"config{SOFT_HYPHEN}uration{NBSP}here"
    once = cosmetic.normalise(text)
    assert cosmetic.normalise(once) == once
