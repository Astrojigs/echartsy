"""Python / standalone rendering backend.

Opens the chart in the user's default web browser, similar to how
``matplotlib.pyplot.show()`` pops up a window.
"""
from __future__ import annotations

import tempfile
import webbrowser
from typing import Optional

from echartslib.renderers._html_template import build_html


def render_python(
    option: dict,
    height: str = "400px",
    width: str = "100%",
    theme: Optional[str] = None,
    renderer: str = "canvas",
) -> dict:
    """Write an HTML file to a temp location and open it in the browser.

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
    html = build_html(
        option, height=height, width=width, theme=theme, renderer=renderer,
    )

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", delete=False, prefix="echartslib_",
    ) as f:
        f.write(html)
        filepath = f.name

    webbrowser.open(f"file://{filepath}")
    return option
