"""Jupyter Notebook rendering backend.

Renders the chart inline as an interactive HTML widget using a
base64-encoded data-URI inside an ``<iframe>``.
"""
from __future__ import annotations

import base64
import uuid
import warnings
from typing import Optional

from echartsy.renderers._html_template import build_jupyter_html


def render_jupyter(
    option: dict,
    height: str = "400px",
    width: str = "100%",
    theme: Optional[str] = None,
    renderer: str = "svg",
    adaptive: str = "auto",
) -> None:
    """Render an ECharts chart inline in a Jupyter notebook cell.

    Uses a base64 data-URI ``<iframe>`` so no temp files or external
    server are needed.

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
    adaptive : str
        ``"auto"`` | ``"light"`` | ``"dark"`` — dark-mode adaptation.
    """
    try:
        from IPython.display import HTML, display
    except ImportError:
        raise ImportError(
            "IPython is required for the 'jupyter' engine. "
            "Install it with:  pip install echartsy[jupyter]"
        )

    chart_id = f"ec_{uuid.uuid4().hex[:10]}"
    html_content = build_jupyter_html(
        option, height=height, width=width,
        theme=theme, renderer=renderer, chart_id=chart_id,
        adaptive=adaptive,
    )

    h_px = _parse_css_px(height, default=400)
    w_css = width if width != "100%" else "100%"

    encoded = base64.b64encode(html_content.encode("utf-8")).decode("ascii")

    iframe_html = (
        f'<iframe src="data:text/html;base64,{encoded}" '
        f'width="{w_css}" height="{h_px + 20}px" '
        f'style="border:none; overflow:hidden;" '
        f'sandbox="allow-scripts allow-same-origin allow-downloads">'
        f'</iframe>'
    )

    # Suppress the "Consider using IPython.display.IFrame" warning —
    # IFrame cannot serve data-URIs or temp files reliably across all
    # Jupyter environments, so the HTML approach is intentional.
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message=".*Consider using IPython.display.IFrame.*",
            category=UserWarning,
        )
        display(HTML(iframe_html))


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
