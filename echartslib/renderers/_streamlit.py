"""Streamlit rendering backend.

Renders the chart inside a Streamlit app using ``streamlit-echarts``.
Falls back to ``st.json`` if the package is not installed.
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
        Extra kwargs forwarded to ``st_echarts()``.

    Returns
    -------
    dict
        The original option dict (pass-through).
    """
    st_echarts = _import_st_echarts()

    if st_echarts is None:
        _fallback_render(option, height)
        return option

    kw: dict = {
        "options": option,
        "height": height,
        "renderer": renderer,
    }
    if key:
        kw["key"] = key
    if width:
        kw["width"] = width
    if theme:
        kw["theme"] = theme
    kw.update(render_kw)

    st_echarts(**kw)
    return option


# ── Lazy import helpers ──────────────────────────────────────────────────

_ST_ECHARTS_AVAILABLE: Optional[bool] = None


def _import_st_echarts():
    """Return ``st_echarts`` callable, or ``None`` if the package is missing."""
    global _ST_ECHARTS_AVAILABLE
    if _ST_ECHARTS_AVAILABLE is None:
        try:
            from streamlit_echarts import st_echarts
            _ST_ECHARTS_AVAILABLE = True
            return st_echarts
        except ImportError:
            _ST_ECHARTS_AVAILABLE = False
            return None
    if _ST_ECHARTS_AVAILABLE:
        from streamlit_echarts import st_echarts
        return st_echarts
    return None


def _fallback_render(option: dict, height: str = "400px") -> None:
    """Render the raw JSON dict via ``st.json`` when streamlit-echarts is absent."""
    try:
        import streamlit as st
        st.warning(
            "streamlit-echarts is not installed. Showing raw ECharts JSON. "
            "Install with:  pip install streamlit-echarts"
        )
        st.json(option, expanded=False)
    except ImportError:
        print(json.dumps(option, indent=2, default=str))
