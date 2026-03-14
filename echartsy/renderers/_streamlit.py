"""Streamlit rendering backend.

Renders the chart inside a Streamlit app. Uses ``st.components.v1.html()``
with ECharts loaded from CDN — no third-party Streamlit component required.
Falls back to ``st.json`` if Streamlit itself is not available.
"""
from __future__ import annotations

import json
from typing import Any, Optional


def render_streamlit(
    option: dict,
    height: str = "400px",
    width: Optional[str] = None,
    theme: Optional[str] = None,
    renderer: str = "svg",
    key: Optional[str] = None,
    **render_kw: Any,
) -> dict:
    """Render an ECharts chart in a Streamlit app.

    Parameters
    ----------
    option : dict
        ECharts option dict.
    height : str
        CSS height.
    width : str or None
        CSS width (``None`` = Streamlit container width).
    theme : str or None
        ECharts theme.
    renderer : str
        ``"canvas"`` or ``"svg"``.
    key : str or None
        Explicit Streamlit widget key.
    **render_kw
        Extra kwargs forwarded to ``st_echarts()`` (only used when
        streamlit-echarts is installed and preferred).

    Returns
    -------
    dict
        The original option dict (pass-through).
    """
    _html_render(option, height, width, theme, renderer)
    return option


def _html_render(
    option: dict,
    height: str = "400px",
    width: Optional[str] = None,
    theme: Optional[str] = None,
    renderer: str = "svg",
) -> None:
    """Render using st.components.v1.html() with ECharts from CDN."""
    try:
        import streamlit as st
        import streamlit.components.v1 as components
    except ImportError:
        print(json.dumps(option, indent=2, default=str))
        return

    from echartsy.renderers._html_template import ECHARTS_CDN, _json_default

    height_px = _parse_css_px(height, 400)
    width_css = width or "100%"
    theme_js = json.dumps(theme) if theme else "null"
    option_json = json.dumps(option, default=_json_default)

    html = f"""\
<!DOCTYPE html>
<html><head><meta charset="utf-8">
<script src="{ECHARTS_CDN}"></script>
</head><body style="margin:0;padding:0;">
<div id="chart" style="width:{width_css};height:{height_px}px;"></div>
<script>
var chart = echarts.init(document.getElementById('chart'), {theme_js}, {{renderer: '{renderer}'}});
chart.setOption({option_json});
window.addEventListener('resize', function() {{ chart.resize(); }});
</script>
</body></html>"""

    components.html(html, height=height_px + 10, scrolling=False)


def _parse_css_px(value: str, default: int) -> int:
    """Extract integer pixel value from a CSS height string like '400px'."""
    v = str(value).strip().lower()
    if v.endswith("px"):
        v = v[:-2]
    try:
        return int(float(v))
    except (ValueError, TypeError):
        return default
