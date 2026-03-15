"""Streamlit rendering backend.

Renders the chart inside a Streamlit app using ``st.components.v1.html()``
with ECharts loaded from CDN. Automatically adapts to the Streamlit app's
dark/light theme. No third-party Streamlit component required.
"""
from __future__ import annotations

import json
import re
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

    Automatically detects the Streamlit theme (dark/light) and adapts
    chart colours accordingly. When the user has set
    ``ec.config(adaptive="dark")``, dark mode is forced regardless of
    the Streamlit theme.

    Parameters
    ----------
    option : dict
        ECharts option dict.
    height : str
        CSS height.
    width : str or None
        CSS width (``None`` = Streamlit container width).
    theme : str or None
        ECharts theme. When ``None``, auto-detected from Streamlit.
    renderer : str
        ``"canvas"`` or ``"svg"``.
    key : str or None
        Explicit Streamlit widget key.
    **render_kw
        Extra kwargs (reserved for future use).

    Returns
    -------
    dict
        The original option dict (pass-through).
    """
    _html_render(option, height, width, theme, renderer, key=key)
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


def _resolve_adaptive(explicit_theme: Optional[str]) -> str:
    """Determine the adaptive mode to use for the chart.

    Priority:
    1. User's ``ec.config(adaptive=...)`` setting (if not "auto")
    2. Streamlit's detected theme
    3. Fall back to "auto" (uses CSS media query in the browser)
    """
    from echartsy._config import get_adaptive

    adaptive = get_adaptive()  # "auto", "light", or "dark"

    # If user explicitly forced a mode, respect it
    if adaptive != "auto":
        return adaptive

    # If an explicit ECharts theme was passed (e.g. theme="dark"), don't override
    if explicit_theme:
        return "light"  # no adaptive patching needed, theme handles it

    # Try to detect Streamlit's theme
    st_theme = _detect_streamlit_theme()
    if st_theme == "dark":
        return "dark"
    if st_theme == "light":
        return "light"

    # Fall back to browser-level auto-detection
    return "auto"


def _html_render(
    option: dict,
    height: str = "400px",
    width: Optional[str] = None,
    theme: Optional[str] = None,
    renderer: str = "svg",
    key: Optional[str] = None,
) -> None:
    """Render using st.components.v1.html() with ECharts from CDN.

    Uses the shared adaptive dark-mode script from ``_html_template``
    so colour patching is consistent across all rendering engines.
    """
    try:
        import streamlit.components.v1 as components
    except ImportError:
        print(json.dumps(option, indent=2, default=str))
        return

    from echartsy.renderers._html_template import (
        ECHARTS_CDN,
        _build_adaptive_script,
        _json_default,
    )

    height_px = _parse_css_px(height, 400)
    width_css = width or "100%"
    # Validate CSS dimensions to prevent injection
    if not re.match(r'^[\d.]+(px|%|em|rem|vw|vh)?$', width_css):
        raise ValueError(f"width must be a valid CSS dimension (e.g. '100%', '800px'), got '{width_css}'")
    adaptive = _resolve_adaptive(theme)
    option_json = json.dumps(option, default=_json_default)

    script_body = _build_adaptive_script(
        option_json=option_json,
        chart_id="chart",
        theme=theme,
        renderer=renderer,
        adaptive=adaptive,
    )

    html = f"""\
<!DOCTYPE html>
<html><head><meta charset="utf-8">
<script src="{ECHARTS_CDN}"></script>
<style>
  * {{ margin: 0; padding: 0; }}
  @media (prefers-color-scheme: dark) {{ body {{ background: transparent; }} }}
</style>
</head><body>
<div id="chart" style="width:{width_css};height:{height_px}px;"></div>
<script>
{script_body}
</script>
</body></html>"""

    if key is not None:
        import streamlit as st
        with st.container(key=key):
            components.html(html, height=height_px + 10, scrolling=False)
    else:
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
