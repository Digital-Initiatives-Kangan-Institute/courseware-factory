"""Cases HPB-01 .. HPB-03 — factory/docs/test-plan.md.

Covers common/helpers/pptx_brand.py: the branded slide deck for in-world scenario presentations.
"""
import importlib
import sys
import types

import pptx_brand
from pptx_brand import (
    new_deck, add_title_slide, add_content_slide, add_statement_slide,
    add_table_slide, add_closing_slide,
)


def test_new_deck_starts_empty():
    """HPB-01"""
    assert len(new_deck().slides) == 0


def test_build_a_small_branded_deck():
    """HPB-02"""
    prs = new_deck()
    add_title_slide(prs, "Design Review", "YAT LMS", ["Prepared by MTS", "v1.0"])
    add_content_slide(prs, "Agenda", [("Scope", 0), ("Approach", 0), ("Risks", 1)])
    add_statement_slide(prs, "Key point", "Availability is the driver", "99.9% target")
    add_table_slide(prs, "Costs", ["Item", "Year 1"], [["Compute", "$100"]])
    add_closing_slide(prs, "Questions", "thank you")
    assert len(prs.slides) == 5


def test_palette_comes_from_the_course_brand():
    """HPB-03 — a different course brand changes the deck's palette, font and disclosure."""
    other = types.ModuleType("brand")
    names = ["TEAL", "TERRACOTTA", "OCHRE", "CREAM", "CHARCOAL", "GREY", "STONE", "WHITE"]
    for i, name in enumerate(names):
        setattr(other, name, f"00000{i}")
    other.FONT = "Other Sans"
    other.DISCLOSURE = "Another course's disclosure."

    real = sys.modules.get("brand")
    sys.modules["brand"] = other
    try:
        reloaded = importlib.reload(pptx_brand)
        got = [getattr(reloaded, n) for n in names], reloaded.FONT, reloaded.DISCLOSURE
    finally:
        # Put the real brand back, then rebuild the module against it, so later tests are unaffected.
        if real is None:
            sys.modules.pop("brand", None)
        else:
            sys.modules["brand"] = real
        importlib.reload(pptx_brand)

    assert got == ([getattr(other, n) for n in names], "Other Sans", "Another course's disclosure.")
