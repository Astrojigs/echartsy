"""Jupyter Notebook rendering backend.

Renders the chart inline as an interactive HTML widget using
``IPython.display.HTML`` with an embedded IFrame.
"""
from __future__ import annotations

import base64
import uuid
from typing import Optional

from echartslib.renderers._html_template import build_jupyter_html


def render_jupyter(
    option: dict,
    height: str = "400px",
    width: str = "100%",
    theme: Optional[str] = None,
    renderer: str = "canvas",
) -> dict:
    """Render an ECharts chart inline in a Jupyter notebook cell.

    Uses an IFrame with a ``srcdoc`` data-URI so no temp files or
    external server are needed.

    Parameters
    ----------
    option : dict
        ECharts option dict.
    height, width : str
        CSS dimensions.
    theme : str or None
        ECharts theme.
    renderer : str
        ``"canvas"`` or ``"svg"``.

    Returns
    -------
    dict
        The original option dict (pass-through).
    """
    try:
        from IPython.display import HTML, display
    except ImportError:
        raise ImportError(
            "IPython is required for the 'jupyter' engine. "
            "Install it with:  pip install echartslib[jupyter]"
        )

    chart_id = f"ec_{uuid.uuid4().hex[:10]}"
    html_content = build_jupyter_html(
        option, height=height, width=width,
        theme=theme, renderer=renderer, chart_id=chart_id,
    )

    # Parse the numeric portion of height for the iframe
    h_px = _parse_css_px(height, default=400)
    w_css = width if width != "100%" else "100%"

    # Encode the HTML as a base64 data-URI so it works without a server
    encoded = base64.b64encode(html_content.encode("utf-8")).decode("ascii")

    iframe_html = (
        f'<iframe src="data:text/html;base64,{encoded}" '
        f'width="{w_css}" height="{h_px + 20}px" '
        f'style="border:none; overflow:hidden;" '
        f'sandbox="allow-scripts allow-same-origin">'
        f'</iframe>'
    )

    display(HTML(iframe_html))
    return option


def _parse_css_px(value: str, default: int = 400) -> int:
    """Extract the numeric pixel value from a CSS string like ``"500px"``."""
    s = value.strip().lower()
    if s.endswith("px"):
        try:
            return int(s[:-2])
        except ValueError:
            pass
    try:
        return int(s)
    except ValueError:
        return default
