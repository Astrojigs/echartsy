"""Central render dispatcher — routes to the active engine."""
from __future__ import annotations

from typing import Any, Optional

from echartsy._config import get_adaptive, get_engine


def render(
    option: dict,
    height: str = "400px",
    width: Optional[str] = None,
    theme: Optional[str] = None,
    renderer: str = "canvas",
    key: Optional[str] = None,
    **render_kw: Any,
) -> None:
    """Dispatch to the currently configured rendering backend.

    Parameters
    ----------
    option : dict
        The assembled ECharts option dict.
    height : str
        CSS height.
    width : str or None
        CSS width.
    theme : str or None
        ECharts built-in theme.
    renderer : str
        ``"canvas"`` or ``"svg"``.
    key : str or None
        Widget key (Streamlit only).
    **render_kw
        Extra renderer-specific keyword arguments.
    """
    engine = get_engine()
    adaptive = get_adaptive()

    if engine == "jupyter":
        from echartsy.renderers._jupyter import render_jupyter
        render_jupyter(
            option, height=height, width=width or "100%",
            theme=theme, renderer=renderer, adaptive=adaptive,
        )
        return

    if engine == "streamlit":
        from echartsy.renderers._streamlit import render_streamlit
        render_streamlit(
            option, height=height, width=width, theme=theme,
            renderer=renderer, key=key, **render_kw,
        )
        return

    # Default: "python" — open in browser
    from echartsy.renderers._python import render_python
    render_python(
        option, height=height, width=width or "100%",
        theme=theme, renderer=renderer, adaptive=adaptive,
    )
