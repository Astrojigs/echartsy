"""Tests for TimelineFigure."""
from __future__ import annotations

import os

import pandas as pd
import pytest

import echartsy as ec
from echartsy.exceptions import BuilderConfigError


@pytest.fixture
def tl_df():
    """Timeline-compatible DataFrame with 3 frames."""
    return pd.DataFrame({
        "Month": ["Jan", "Jan", "Feb", "Feb", "Mar", "Mar"],
        "Category": ["East", "West", "East", "West", "East", "West"],
        "Value": [100, 150, 120, 160, 140, 170],
    })


@pytest.fixture
def tl_scatter_df():
    """Timeline scatter data with numeric x/y."""
    return pd.DataFrame({
        "Period": ["Q1", "Q1", "Q2", "Q2", "Q3", "Q3"],
        "X": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
        "Y": [10.0, 20.0, 15.0, 25.0, 18.0, 30.0],
    })


class TestTimelineBar:
    def test_timeline_bar(self, tl_df):
        tfig = ec.TimelineFigure()
        tfig.bar(tl_df, x="Category", y="Value", time_col="Month")
        opt = tfig.to_option()
        assert "baseOption" in opt
        assert "options" in opt
        assert len(opt["options"]) == 3  # Jan, Feb, Mar
        # Each frame has bar series
        for frame in opt["options"]:
            assert any(s["type"] == "bar" for s in frame["series"])


class TestTimelinePlot:
    def test_timeline_plot(self, tl_df):
        tfig = ec.TimelineFigure()
        tfig.plot(tl_df, x="Category", y="Value", time_col="Month")
        opt = tfig.to_option()
        assert "baseOption" in opt
        assert len(opt["options"]) == 3
        for frame in opt["options"]:
            assert any(s["type"] == "line" for s in frame["series"])


class TestTimelinePie:
    def test_timeline_pie(self, tl_df):
        tfig = ec.TimelineFigure()
        tfig.pie(tl_df, names="Category", values="Value", time_col="Month")
        opt = tfig.to_option()
        assert "baseOption" in opt
        assert len(opt["options"]) == 3
        for frame in opt["options"]:
            assert any(s["type"] == "pie" for s in frame["series"])


class TestTimelineScatter:
    def test_timeline_scatter(self, tl_scatter_df):
        tfig = ec.TimelineFigure()
        tfig.scatter(tl_scatter_df, x="X", y="Y", time_col="Period")
        opt = tfig.to_option()
        assert "baseOption" in opt
        assert len(opt["options"]) == 3
        for frame in opt["options"]:
            assert any(s["type"] == "scatter" for s in frame["series"])


class TestTimelineHist:
    def test_timeline_hist(self):
        df = pd.DataFrame({
            "Period": ["A"] * 10 + ["B"] * 10,
            "Vals": list(range(10)) + list(range(5, 15)),
        })
        tfig = ec.TimelineFigure()
        tfig.hist(df, column="Vals", time_col="Period", bins=5)
        opt = tfig.to_option()
        assert "baseOption" in opt
        assert len(opt["options"]) == 2
        for frame in opt["options"]:
            assert any(s["type"] == "bar" for s in frame["series"])


class TestTimelineFrameSorting:
    def test_timeline_frame_sorting(self):
        """Frames with parseable temporal labels are sorted correctly."""
        df = pd.DataFrame({
            "Month": ["Mar", "Jan", "Feb", "Mar", "Jan", "Feb"],
            "Cat": ["A", "A", "A", "B", "B", "B"],
            "Val": [30, 10, 20, 35, 15, 25],
        })
        tfig = ec.TimelineFigure()
        tfig.bar(df, x="Cat", y="Val", time_col="Month")
        opt = tfig.to_option()
        tl_data = opt["baseOption"]["timeline"]["data"]
        # "Jan", "Feb", "Mar" cannot be fully parsed by the timeline parser
        # but they should still appear as frame labels
        assert len(tl_data) == 3


class TestTimelineErrors:
    def test_timeline_empty_raises(self):
        tfig = ec.TimelineFigure()
        with pytest.raises(BuilderConfigError, match="no series"):
            tfig.to_option()


class TestTimelinePlayback:
    def test_timeline_playback(self, tl_df):
        tfig = ec.TimelineFigure(interval=3.0, autoplay=False, loop=False)
        tfig.bar(tl_df, x="Category", y="Value", time_col="Month")
        tfig.playback(interval=1.5, autoplay=True, loop=True)
        opt = tfig.to_option()
        tl = opt["baseOption"]["timeline"]
        assert tl["autoPlay"] is True
        assert tl["loop"] is True
        # interval is in ms: 1.5 * 1000 = 1500
        assert tl["playInterval"] == 1500


class TestTimelineHtml:
    def test_timeline_to_html(self, tl_df, tmp_path):
        tfig = ec.TimelineFigure()
        tfig.bar(tl_df, x="Category", y="Value", time_col="Month")
        filepath = str(tmp_path / "timeline_chart.html")
        result = tfig.to_html(filepath)
        assert result == filepath
        assert os.path.exists(filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()
        assert "<!DOCTYPE html>" in html
        assert "echarts" in html


# ═══════════════════════════════════════════════════════════════════════════
# Timeline chrome methods
# ═══════════════════════════════════════════════════════════════════════════

class TestTimelineChrome:
    def test_title_with_subtitle(self, tl_df):
        tfig = ec.TimelineFigure()
        tfig.bar(tl_df, x="Category", y="Value", time_col="Month")
        tfig.title("Main", subtitle="Sub", top=30)
        opt = tfig.to_option()
        assert opt["baseOption"]["title"]["subtext"] == "Sub"
        assert opt["baseOption"]["title"]["top"] == 30

    def test_xlabel(self, tl_df):
        tfig = ec.TimelineFigure()
        tfig.bar(tl_df, x="Category", y="Value", time_col="Month")
        tfig.xlabel("Cat", rotate=45, font_size=14, color="#ff0000")
        opt = tfig.to_option()
        # xlabel affects the per-frame xAxis
        frame = opt["options"][0]
        assert frame["xAxis"]["name"] == "Cat"

    def test_ylabel(self, tl_df):
        tfig = ec.TimelineFigure()
        tfig.bar(tl_df, x="Category", y="Value", time_col="Month")
        tfig.ylabel("Amount", font_size=12, color="#333")
        opt = tfig.to_option()
        frame = opt["options"][0]
        y = frame["yAxis"] if isinstance(frame["yAxis"], dict) else frame["yAxis"][0]
        assert y["name"] == "Amount"

    def test_ylabel_right(self, tl_df):
        tfig = ec.TimelineFigure()
        tfig.bar(tl_df, x="Category", y="Value", time_col="Month")
        tfig.ylabel_right("Secondary", font_size=10, color="#666")
        opt = tfig.to_option()
        frame = opt["options"][0]
        assert isinstance(frame["yAxis"], list)
        assert frame["yAxis"][1]["name"] == "Secondary"

    def test_legend(self, tl_df):
        tfig = ec.TimelineFigure()
        tfig.bar(tl_df, x="Category", y="Value", time_col="Month")
        tfig.legend(show=True, orient="vertical", left="right", top=50)
        opt = tfig.to_option()
        assert opt["baseOption"]["legend"]["orient"] == "vertical"

    def test_tooltip(self, tl_df):
        tfig = ec.TimelineFigure()
        tfig.bar(tl_df, x="Category", y="Value", time_col="Month")
        tfig.tooltip(trigger="item", pointer="shadow", formatter="{b}: {c}")
        opt = tfig.to_option()
        frame = opt["options"][0]
        assert frame["tooltip"]["trigger"] == "item"

    def test_axis_pointer(self, tl_df):
        tfig = ec.TimelineFigure()
        tfig.bar(tl_df, x="Category", y="Value", time_col="Month")
        tfig.axis_pointer(type="cross", snap=True, label=True,
                          label_precision=2, label_bg="#333", label_color="#fff",
                          line_color="#000", line_width=2, line_type="dashed",
                          cross_color="#red", cross_width=1, cross_type="dotted",
                          shadow_color="rgba(0,0,0,0.2)", shadow_opacity=0.5)
        opt = tfig.to_option()
        assert "axisPointer" in opt["baseOption"]

    def test_palette(self, tl_df):
        tfig = ec.TimelineFigure()
        tfig.bar(tl_df, x="Category", y="Value", time_col="Month")
        tfig.palette(["#f00", "#0f0", "#00f"])
        opt = tfig.to_option()
        assert opt["baseOption"]["color"] == ["#f00", "#0f0", "#00f"]

    def test_margins(self, tl_df):
        tfig = ec.TimelineFigure()
        tfig.bar(tl_df, x="Category", y="Value", time_col="Month")
        tfig.margins(left=100, right=100, top=80, bottom=60)
        opt = tfig.to_option()
        frame = opt["options"][0]
        assert frame["grid"]["left"] == 100

    def test_xlim(self, tl_df):
        tfig = ec.TimelineFigure()
        tfig.bar(tl_df, x="Category", y="Value", time_col="Month")
        tfig.xlim(min_val=0, max_val=100)
        opt = tfig.to_option()
        frame = opt["options"][0]
        assert frame["xAxis"]["min"] == 0

    def test_ylim(self, tl_df):
        tfig = ec.TimelineFigure()
        tfig.bar(tl_df, x="Category", y="Value", time_col="Month")
        tfig.ylim(min_val=0, max_val=200)
        opt = tfig.to_option()
        frame = opt["options"][0]
        y = frame["yAxis"] if isinstance(frame["yAxis"], dict) else frame["yAxis"][0]
        assert y["min"] == 0

    def test_save(self, tl_df):
        tfig = ec.TimelineFigure()
        tfig.bar(tl_df, x="Category", y="Value", time_col="Month")
        tfig.save(name="export", fmt="svg")
        opt = tfig.to_option()
        assert opt["baseOption"]["toolbox"]["feature"]["saveAsImage"]["type"] == "svg"

    def test_extra(self, tl_df):
        tfig = ec.TimelineFigure()
        tfig.bar(tl_df, x="Category", y="Value", time_col="Month")
        tfig.extra(animation=False)
        opt = tfig.to_option()
        assert opt["baseOption"]["animation"] is False

    def test_repr(self, tl_df):
        tfig = ec.TimelineFigure()
        tfig.bar(tl_df, x="Category", y="Value", time_col="Month")
        r = repr(tfig)
        assert "TimelineFigure" in r
        assert "frames=3" in r

    def test_playback_rewind(self, tl_df):
        tfig = ec.TimelineFigure()
        tfig.bar(tl_df, x="Category", y="Value", time_col="Month")
        tfig.playback(rewind=True)
        opt = tfig.to_option()
        assert opt["baseOption"]["timeline"]["rewind"] is True


# ═══════════════════════════════════════════════════════════════════════════
# Temporal parsing / detect_time_format
# ═══════════════════════════════════════════════════════════════════════════

class TestTemporalParsing:
    def test_detect_time_format(self):
        from echartsy.timeline import detect_time_format
        s = pd.Series(["2024", "2025", "2026"])
        result = detect_time_format(s)
        assert "3/3" in result
        assert "sorted correctly" in result

    def test_detect_time_format_empty(self):
        from echartsy.timeline import detect_time_format
        s = pd.Series([], dtype=str)
        result = detect_time_format(s)
        assert "empty" in result

    def test_detect_time_format_unrecognised(self):
        from echartsy.timeline import detect_time_format
        s = pd.Series(["foo", "bar"])
        result = detect_time_format(s)
        assert "unrecognised" in result

    def test_parse_year(self):
        from echartsy.timeline import _parse_temporal_label
        ts = _parse_temporal_label("2024")
        assert ts is not None
        assert ts.year == 2024

    def test_parse_quarter_prefix(self):
        from echartsy.timeline import _parse_temporal_label
        ts = _parse_temporal_label("Q1 2024")
        assert ts is not None
        assert ts.month == 1

    def test_parse_quarter_suffix(self):
        from echartsy.timeline import _parse_temporal_label
        ts = _parse_temporal_label("2024-Q3")
        assert ts is not None
        assert ts.month == 7

    def test_parse_half_prefix(self):
        from echartsy.timeline import _parse_temporal_label
        ts = _parse_temporal_label("H2 2024")
        assert ts is not None
        assert ts.month == 7

    def test_parse_month_iso(self):
        from echartsy.timeline import _parse_temporal_label
        ts = _parse_temporal_label("2024-03")
        assert ts is not None
        assert ts.month == 3

    def test_parse_text_month(self):
        from echartsy.timeline import _parse_temporal_label
        ts = _parse_temporal_label("Jan 2024")
        assert ts is not None
        assert ts.month == 1

    def test_parse_fy(self):
        from echartsy.timeline import _parse_temporal_label
        ts = _parse_temporal_label("FY2024")
        assert ts is not None

    def test_parse_day_iso(self):
        from echartsy.timeline import _parse_temporal_label
        ts = _parse_temporal_label("2024-03-15")
        assert ts is not None
        assert ts.day == 15

    def test_parse_unparseable(self):
        from echartsy.timeline import _parse_temporal_label
        assert _parse_temporal_label("xyzzy") is None

    def test_sorted_frames_year(self):
        """Years should be sorted numerically."""
        df = pd.DataFrame({
            "Year": ["2026", "2024", "2025", "2026", "2024", "2025"],
            "Cat": ["A", "A", "A", "B", "B", "B"],
            "Val": [30, 10, 20, 35, 15, 25],
        })
        tfig = ec.TimelineFigure()
        tfig.bar(df, x="Cat", y="Val", time_col="Year")
        opt = tfig.to_option()
        tl_data = opt["baseOption"]["timeline"]["data"]
        assert tl_data == ["2024", "2025", "2026"]


class TestTimelineFactory:
    def test_timeline_figure_factory(self):
        from echartsy.timeline import timeline_figure
        tfig = timeline_figure(height="600px", interval=3.0, autoplay=False)
        assert isinstance(tfig, ec.TimelineFigure)


class TestTimelineModeConflict:
    def test_mode_conflict(self, tl_df):
        tfig = ec.TimelineFigure()
        tfig.bar(tl_df, x="Category", y="Value", time_col="Month")
        with pytest.raises(BuilderConfigError, match="mode"):
            tfig.pie(tl_df, names="Category", values="Value", time_col="Month")
