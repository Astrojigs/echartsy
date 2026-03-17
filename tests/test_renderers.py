"""Tests for the HTML rendering template in echartsy.renderers._html_template."""
from __future__ import annotations

import json

import pytest

from echartsy.renderers._html_template import (
    ECHARTS_CDN,
    _sanitize_chart_id,
    build_html,
    build_jupyter_html,
)


# ═══════════════════════════════════════════════════════════════════════════
# build_html tests
# ═══════════════════════════════════════════════════════════════════════════

class TestBuildHtml:
    @pytest.fixture
    def sample_option(self):
        """Minimal ECharts option dict for testing."""
        return {
            "xAxis": {"type": "category", "data": ["A", "B"]},
            "yAxis": {"type": "value"},
            "series": [{"type": "bar", "data": [10, 20]}],
        }

    def test_build_html_output(self, sample_option):
        html = build_html(sample_option)
        assert html.startswith("<!DOCTYPE html>")

    def test_build_html_contains_echarts_cdn(self, sample_option):
        html = build_html(sample_option)
        assert ECHARTS_CDN in html

    def test_build_html_contains_option(self, sample_option):
        html = build_html(sample_option)
        # The JSON-serialized option should appear in the script
        assert '"xAxis"' in html
        assert '"series"' in html

    def test_build_html_chart_id(self, sample_option):
        html = build_html(sample_option, chart_id="my_chart")
        assert 'id="my_chart"' in html

    def test_build_html_dimensions(self, sample_option):
        html = build_html(sample_option, height="600px", width="80%")
        assert "600px" in html
        assert "80%" in html

    def test_build_html_adaptive_auto(self, sample_option):
        html = build_html(sample_option, adaptive="auto")
        # The adaptive JS has the mode set to "auto"
        assert '"auto"' in html

    def test_build_html_adaptive_dark(self, sample_option):
        html = build_html(sample_option, adaptive="dark")
        assert '"dark"' in html

    def test_build_html_invalid_renderer(self, sample_option):
        with pytest.raises(ValueError, match="renderer"):
            build_html(sample_option, renderer="webgl")

    def test_build_html_invalid_theme(self, sample_option):
        with pytest.raises(ValueError, match="theme"):
            build_html(sample_option, theme="nonexistent_theme")

    def test_build_html_valid_theme(self, sample_option):
        # Should not raise for valid built-in themes
        html = build_html(sample_option, theme="dark")
        assert "dark" in html


# ═══════════════════════════════════════════════════════════════════════════
# build_jupyter_html tests
# ═══════════════════════════════════════════════════════════════════════════

class TestBuildJupyterHtml:
    def test_build_jupyter_html(self):
        option = {"series": [{"type": "bar", "data": [1, 2]}]}
        html = build_jupyter_html(option)
        assert "<!DOCTYPE html>" in html
        assert ECHARTS_CDN in html
        # It should be a complete document fragment
        assert "<body>" in html


# ═══════════════════════════════════════════════════════════════════════════
# _sanitize_chart_id tests
# ═══════════════════════════════════════════════════════════════════════════

class TestSanitizeChartId:
    def test_sanitize_chart_id_normal(self):
        assert _sanitize_chart_id("my_chart-1") == "my_chart-1"

    def test_sanitize_chart_id_strips_special(self):
        result = _sanitize_chart_id("chart!@#$%id")
        # Only alphanumeric, underscore, and hyphen survive
        assert result == "chartid"

    def test_sanitize_chart_id_empty(self):
        with pytest.raises(ValueError, match="alphanumeric"):
            _sanitize_chart_id("!@#$%")

    def test_sanitize_chart_id_preserves_valid(self):
        assert _sanitize_chart_id("abc_DEF-123") == "abc_DEF-123"
