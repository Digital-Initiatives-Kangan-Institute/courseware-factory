"""Cases IKD-01 .. IKD-02 — factory/docs/test-plan.md.

Covers institutions/kangan/kangan_deck.py: the Kangan teaching-deck layouts.
"""
from kangan_deck import (
    new_deck, title_slide, divider_slide, content_slide, close_slide, GOLD,
)


def test_new_deck_starts_empty():
    """IKD-01"""
    assert len(new_deck().slides) == 0


def test_build_a_small_teaching_deck():
    """IKD-02"""
    prs = new_deck()
    title_slide(prs, 1, "Cloud Foundations", "Topic 1")
    divider_slide(prs, "1", "Concepts", "What you'll learn", GOLD)
    content_slide(prs, 2, "Regions and AZs", "Concepts", [(0, "A region has AZs"), (0, "AZs are isolated")])
    close_slide(prs, "Wrap up", ["See you next session"])
    assert len(prs.slides) == 4
