"""Tests for emphasis dataclasses and their serialization."""
from __future__ import annotations

import pytest

from echartsy.emphasis import (
    AreaStyle,
    Emphasis,
    FunnelEmphasis,
    GraphEmphasis,
    ItemStyle,
    LabelLineStyle,
    LabelStyle,
    LineEmphasis,
    LineStyle,
    PieEmphasis,
    RadarEmphasis,
    SankeyEmphasis,
    ScatterEmphasis,
    TreemapEmphasis,
)


# ═══════════════════════════════════════════════════════════════════════════
# Sub-style to_dict tests (snake_case -> camelCase)
# ═══════════════════════════════════════════════════════════════════════════

class TestItemStyle:
    def test_item_style_to_dict(self):
        style = ItemStyle(color="#ff0000", border_width=2, shadow_blur=5)
        d = style.to_dict()
        assert d["color"] == "#ff0000"
        assert d["borderWidth"] == 2
        assert d["shadowBlur"] == 5
        # snake_case keys should not appear
        assert "border_width" not in d
        assert "shadow_blur" not in d


class TestLabelStyle:
    def test_label_style_to_dict(self):
        style = LabelStyle(show=True, font_size=14, font_weight="bold", position="top")
        d = style.to_dict()
        assert d["show"] is True
        assert d["fontSize"] == 14
        assert d["fontWeight"] == "bold"
        assert d["position"] == "top"


class TestLineStyle:
    def test_line_style_to_dict(self):
        style = LineStyle(color="#333", width=3, type="dashed")
        d = style.to_dict()
        assert d["color"] == "#333"
        assert d["width"] == 3
        assert d["type"] == "dashed"


class TestAreaStyle:
    def test_area_style_to_dict(self):
        style = AreaStyle(color="#aaa", opacity=0.5)
        d = style.to_dict()
        assert d["color"] == "#aaa"
        assert d["opacity"] == 0.5


class TestLabelLineStyle:
    def test_label_line_style_to_dict(self):
        style = LabelLineStyle(show=True, length=15, length2=10)
        d = style.to_dict()
        assert d["show"] is True
        assert d["length"] == 15
        assert d["length2"] == 10


# ═══════════════════════════════════════════════════════════════════════════
# Emphasis class to_dict tests
# ═══════════════════════════════════════════════════════════════════════════

class TestEmphasisBase:
    def test_emphasis_base(self):
        item = ItemStyle(color="red", border_width=1)
        emph = Emphasis(focus="series", item_style=item)
        d = emph.to_dict()
        assert d["focus"] == "series"
        assert d["itemStyle"]["color"] == "red"
        assert d["itemStyle"]["borderWidth"] == 1

    def test_none_omitted(self):
        emph = Emphasis(focus="self")
        d = emph.to_dict()
        assert "itemStyle" not in d
        assert "label" not in d
        assert "blurScope" not in d
        assert "disabled" not in d
        assert d == {"focus": "self"}


class TestLineEmphasis:
    def test_line_emphasis(self):
        ls = LineStyle(color="#000", width=2)
        emph = LineEmphasis(focus="series", line_style=ls)
        d = emph.to_dict()
        assert d["focus"] == "series"
        assert d["lineStyle"]["color"] == "#000"
        assert d["lineStyle"]["width"] == 2


class TestScatterEmphasis:
    def test_scatter_emphasis(self):
        emph = ScatterEmphasis(focus="self", scale=True)
        d = emph.to_dict()
        assert d["focus"] == "self"
        assert d["scale"] is True


class TestPieEmphasis:
    def test_pie_emphasis(self):
        lls = LabelLineStyle(show=True, length=20)
        emph = PieEmphasis(scale=True, scale_size=10, label_line=lls)
        d = emph.to_dict()
        assert d["scale"] is True
        assert d["scaleSize"] == 10
        assert d["labelLine"]["show"] is True
        assert d["labelLine"]["length"] == 20


class TestRadarEmphasis:
    def test_radar_emphasis(self):
        ls = LineStyle(width=3)
        area = AreaStyle(opacity=0.3)
        emph = RadarEmphasis(focus="series", line_style=ls, area_style=area)
        d = emph.to_dict()
        assert d["focus"] == "series"
        assert d["lineStyle"]["width"] == 3
        assert d["areaStyle"]["opacity"] == 0.3


class TestSankeyEmphasis:
    def test_sankey_emphasis(self):
        emph = SankeyEmphasis(focus="adjacency")
        d = emph.to_dict()
        assert d["focus"] == "adjacency"


class TestFunnelEmphasis:
    def test_funnel_emphasis(self):
        lls = LabelLineStyle(show=True, length=10)
        emph = FunnelEmphasis(focus="self", label_line=lls)
        d = emph.to_dict()
        assert d["focus"] == "self"
        assert d["labelLine"]["show"] is True


class TestTreemapEmphasis:
    def test_treemap_emphasis(self):
        upper = LabelStyle(show=True, font_size=16)
        emph = TreemapEmphasis(focus="series", upper_label=upper)
        d = emph.to_dict()
        assert d["focus"] == "series"
        assert d["upperLabel"]["show"] is True
        assert d["upperLabel"]["fontSize"] == 16


class TestGraphEmphasis:
    def test_graph_emphasis(self):
        emph = GraphEmphasis(focus="adjacency")
        d = emph.to_dict()
        assert d["focus"] == "adjacency"


# ═══════════════════════════════════════════════════════════════════════════
# Frozen immutability test
# ═══════════════════════════════════════════════════════════════════════════

class TestFrozen:
    def test_frozen_immutability(self):
        style = ItemStyle(color="blue")
        with pytest.raises(AttributeError):
            style.color = "red"  # type: ignore[misc]

    def test_emphasis_frozen(self):
        emph = Emphasis(focus="self")
        with pytest.raises(AttributeError):
            emph.focus = "series"  # type: ignore[misc]
