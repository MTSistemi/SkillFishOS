"""Tests for the Hub's pure logic (no display needed — nothing is instantiated)."""
import importlib.machinery
import importlib.util
import pathlib

import pytest

HUB = pathlib.Path(__file__).resolve().parents[1] / "apps" / "hub" / "skillfish-hub"


@pytest.fixture(scope="module")
def hub():
    pytest.importorskip("PyQt6.QtWidgets")  # import-only; no QApplication created
    loader = importlib.machinery.SourceFileLoader("hub_mod", str(HUB))
    spec = importlib.util.spec_from_loader("hub_mod", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


def test_top_category_routing(hub):
    assert hub.top_category_of(["ActionGame", "Game"]) == "Game"
    assert hub.top_category_of(["IDE", "Development"]) == "Development"
    # routing keys off the top-level freedesktop category (AppStream always
    # includes it); a bare sub-category falls back to Utility
    assert hub.top_category_of(["IDE"]) == "Utility"
    assert hub.top_category_of([]) == "Utility"
    assert hub.top_category_of(["NoSuchCategory"]) == "Utility"


def test_subcats_are_unique_per_category(hub):
    for cat, subs in hub.SUBCATS.items():
        ids = [s for s, _n in subs]
        assert len(ids) == len(set(ids)), f"duplicate sub-category id in {cat}"


def test_app_defaults_are_safe(hub):
    a = hub.App("apt", "x.y", "pkg", "Name")
    assert a.rating == 0.0 and a.rating_n == 0
    assert a.screens == [] and a.cats == []
    assert a.odrs_id == "x.y"  # falls back to the appid for ratings lookup
