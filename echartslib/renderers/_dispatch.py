"""Central render dispatcher — routes to the active engine."""
from __future__ import annotations

from typing import Any, Optional

from echartslib._config import get_engine


def render(
    option: dict,
    height: str = "400px",
    width: Optional[str] = None,
    theme: Optional[str] = None,
    renderer: str = "canvas",
    key: Optional[str] = None,
    **render_kw: Any,
) -> dict:
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

    Returns
    -------
    dict
        The option dict (pass-through from the renderer).
    """
    engine = get_engine()

    if engine == "jupyter":
        from echartslib.renderers._jupyter import render_jupyter
        return render_jupyter(
            option, height=height, width=width or "100%",
            theme=theme, renderer=renderer,
        )

    if engine == "streamlit":
        from echartslib.renderers._streamlit import render_streamlit
        return render_streamlit(
            option, height=height, width=width, theme=theme,
            renderer=renderer, key=key, **render_kw,
        )

    # Default: "python" — open in browser
    from echartslib.renderers._python import render_python
    return render_python(
        option, height=height, width=width or "100%",
        theme=theme, renderer=renderer,
    )
