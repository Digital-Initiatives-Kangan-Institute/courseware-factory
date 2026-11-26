"""Cases HDI-01 .. HDI-11 — factory/docs/test-plan.md.

Covers common/helpers/deck_images.py: resolving a slide plan's `image:` directive into a placement.
"""
import hashlib
import subprocess

import pytest

import deck_images as DI


@pytest.fixture
def topic(tmp_path):
    """A topic folder with an empty images/ directory."""
    (tmp_path / "images").mkdir()
    return tmp_path


def test_empty_or_none_means_no_image(topic):
    """HDI-01"""
    assert DI.resolve_image("", topic) is None
    assert DI.resolve_image("none", topic) is None


def test_placeholder_is_labelled(topic):
    """HDI-02"""
    assert DI.resolve_image("placeholder hero shot of a data centre", topic) == {
        "label": "hero shot of a data centre"}


def test_bare_placeholder_is_labelled_with_the_keyword(topic):
    """HDI-03"""
    assert DI.resolve_image("placeholder", topic) == {"label": "placeholder"}


def test_reuse_places_a_committed_file(topic):
    """HDI-04"""
    img = topic / "images" / "regions.png"
    img.write_bytes(b"png")
    assert DI.resolve_image("reuse regions.png", topic) == {"path": img, "label": "regions.png"}


def test_reuse_stem_matches_any_extension(topic):
    """HDI-05"""
    img = topic / "images" / "regions.jpg"
    img.write_bytes(b"jpg")
    assert DI.resolve_image("reuse regions", topic)["path"] == img


def test_reuse_missing_file_is_a_placeholder(topic):
    """HDI-06"""
    assert DI.resolve_image("reuse not-dropped-in-yet.png", topic) == {"label": "not-dropped-in-yet.png"}


def test_gen_cache_hit_is_placed_without_allow_gen(topic):
    """HDI-07"""
    prompt = "a calm server room"
    cached = topic / "images" / ("gen-" + hashlib.md5(prompt.encode("utf-8")).hexdigest()[:8] + ".png")
    cached.write_bytes(b"png")
    assert DI.resolve_image(f"gen {prompt}", topic) == {"path": cached, "label": prompt}


def test_gen_miss_without_allow_gen_calls_nothing(topic, monkeypatch):
    """HDI-08 — generating a missing image calls a paid model; without allow_gen nothing runs."""
    def refuse(*args, **kwargs):
        raise AssertionError("a subprocess was started")
    monkeypatch.setattr(subprocess, "run", refuse)
    assert DI.resolve_image("gen a calm server room", topic) == {"label": "GEN (not run): a calm server room"}


def test_unknown_keyword_is_a_placeholder(topic):
    """HDI-09"""
    assert DI.resolve_image("photo of a rack", topic) == {"label": "photo of a rack"}


def test_diagram_without_spec_raises_naming_the_path(topic):
    """HDI-10"""
    with pytest.raises(FileNotFoundError, match=r"diagrams/network\.json"):
        DI.resolve_image("diagram network", topic)


def test_keyword_is_case_insensitive(topic):
    """HDI-11"""
    assert DI.resolve_image("Placeholder later", topic) == {"label": "later"}
