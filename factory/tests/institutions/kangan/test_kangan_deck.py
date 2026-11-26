"""Cases IKD-01 .. IKD-02 — factory/docs/test-plan.md.

Covers institutions/kangan/kangan_deck.py: the Kangan teaching-deck layouts. The pack is put on the
path per test by this folder's conftest, so the module is imported inside each test.
"""


def test_new_deck_starts_empty():
    """IKD-01"""
    import kangan_deck as K
    assert len(K.new_deck().slides) == 0


def test_build_a_small_teaching_deck():
    """IKD-02"""
    import kangan_deck as K
    prs = K.new_deck()
    K.title_slide(prs, 1, "Cloud Foundations", "Topic 1")
    K.divider_slide(prs, "1", "Concepts", "What you'll learn", K.GOLD)
    K.content_slide(prs, 2, "Regions and AZs", "Concepts", [(0, "A region has AZs"), (0, "AZs are isolated")])
    K.close_slide(prs, "Wrap up", ["See you next session"])
    assert len(prs.slides) == 4
