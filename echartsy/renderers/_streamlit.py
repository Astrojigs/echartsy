"""Streamlit rendering backend.

Renders the chart inside a Streamlit app using ``st.components.v1.html()``
with ECharts loaded from CDN.  Uses a minimal HTML fragment approach so
charts persist reliably across ``st.tabs()`` switches.
"""
from __future__ import annotations

import json
import re
from typing import Any, Optional

_CHART_COUNTER = 0


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

    Dark-mode adaptation is **opt-in**: charts use the default (light)
    ECharts theme unless the caller passes an explicit ``theme`` or sets
    ``ec.config(adaptive="dark")``.

    Parameters
    ----------
    option : dict
        ECharts option dict.
    height : str
        CSS height.
    width : str or None
        CSS width (``None`` = Streamlit container width).
    theme : str or None
        ECharts theme.  ``None`` = default (light).
    renderer : str
        ``"canvas"`` or ``"svg"``.
    key : str or None
        Accepted for backward compatibility; **not used**.
    **render_kw
        Extra kwargs (reserved for future use).

    Returns
    -------
    dict
        The original option dict (pass-through).
    """
    _html_render(option, height, width, theme, renderer)
    return option


def _detect_streamlit_theme() -> Optional[str]:
    """Detect the active Streamlit theme.

    Returns ``"dark"``, ``"light"``, or ``None`` if detection fails.
    """
    try:
        import streamlit as st
        base = st.get_option("theme.base")
        if base in ("dark", "light"):
            return base
    except Exception:
        pass
    return None


def _resolve_theme(explicit_theme: Optional[str]) -> Optional[str]:
    """Determine the ECharts theme to use.

    Priority:
    1. User's ``ec.config(adaptive=...)`` setting (if not "auto")
    2. Explicit theme passed to the function
    3. Streamlit's detected theme
    4. ``None`` (ECharts default)
    """
    from echartsy._config import get_adaptive

    adaptive = get_adaptive()  # "auto", "light", or "dark"

    # If user explicitly forced dark, use the "dark" ECharts theme
    if adaptive == "dark":
        return "dark"
    if adaptive == "light":
        return explicit_theme  # respect explicit or default

    # If an explicit ECharts theme was passed, use it
    if explicit_theme:
        return explicit_theme

    # Try to detect Streamlit's theme
    st_theme = _detect_streamlit_theme()
    if st_theme == "dark":
        return "dark"

    return None


def _html_render(
    option: dict,
    height: str = "400px",
    width: Optional[str] = None,
    theme: Optional[str] = None,
    renderer: str = "svg",
) -> None:
    """Render using st.components.v1.html() with a minimal HTML fragment.

    Uses a simple ``<div>`` + ``<script>`` approach with a globally unique
    div ID.  No full HTML document, no adaptive JS, no ``key`` parameter —
    this ensures charts persist across ``st.tabs()`` switches.
    """
    try:
        import streamlit.components.v1 as components
    except ImportError:
        print(json.dumps(option, indent=2, default=str))
        return

    from echartsy.renderers._html_template import (
        ECHARTS_CDN,
        _json_default,
        _VALID_RENDERERS,
        _VALID_THEMES,
    )

    if renderer not in _VALID_RENDERERS:
        raise ValueError(f"renderer must be one of {_VALID_RENDERERS}, got '{renderer}'")
    if theme is not None and theme not in _VALID_THEMES:
        raise ValueError(f"theme must be one of {sorted(_VALID_THEMES)} or None, got '{theme}'")

    height_px = _parse_css_px(height, 400)
    width_css = width or "100%"
    if not re.match(r'^[\d.]+(px|%|em|rem|vw|vh)?$', width_css):
        raise ValueError(f"width must be a valid CSS dimension (e.g. '100%', '800px'), got '{width_css}'")

    # Theme: only auto-detect when user explicitly opted in via
    # ec.config(adaptive="dark"|"light").  Default ("auto") skips
    # detection and uses the explicit theme as-is — matching the simple
    # fragment pattern that reliably survives st.tabs() switches.
    from echartsy._config import get_adaptive

    adaptive = get_adaptive()
    if adaptive != "auto":
        resolved_theme = _resolve_theme(theme)
    else:
        resolved_theme = theme

    # Escape </ to prevent script-tag breakout in embedded JSON.
    option_json = json.dumps(option, default=_json_default).replace("</", "<\\/")

    global _CHART_COUNTER
    _CHART_COUNTER += 1
    div_id = f"ec{_CHART_COUNTER}"

    theme_js = f"'{resolved_theme}'" if resolved_theme else "null"

    html = (
        f'<div id="{div_id}" style="width:{width_css};height:{height_px}px;"></div>\n'
        f'<script src="{ECHARTS_CDN}"></script>\n'
        f"<script>\n"
        f"var c=echarts.init(document.getElementById('{div_id}'),{theme_js},"
        f"{{renderer:'{renderer}'}});\n"
        f"c.setOption({option_json});\n"
        f"new ResizeObserver(function(){{c.resize();}})"
        f".observe(document.getElementById('{div_id}'));\n"
        f"</script>"
    )

    components.html(html, height=height_px + 10)


def _parse_css_px(value: str, default: int) -> int:
    """Extract integer pixel value from a CSS height string like '400px'."""
    v = str(value).strip().lower()
    if v.endswith("px"):
        v = v[:-2]
    try:
        return int(float(v))
    except (ValueError, TypeError):
        return default
