"""Global configuration for echartslib rendering engine."""
from __future__ import annotations

from typing import Literal, Optional

EngineType = Literal["python", "jupyter", "streamlit"]

_current_engine: EngineType = "python"


def config(engine: EngineType) -> None:
    """Set the global rendering engine.

    Parameters
    ----------
    engine : ``"python"`` | ``"jupyter"`` | ``"streamlit"``
        - ``"python"``    — Opens an interactive HTML chart in the default
          browser (similar to ``plt.show()``).
        - ``"jupyter"``   — Renders an inline interactive widget in Jupyter
          Notebook / JupyterLab cells.
        - ``"streamlit"`` — Renders via ``streamlit-echarts`` inside a
          Streamlit application.

    Example
    -------
    >>> import echartslib as ec
    >>> ec.config(engine="jupyter")
    """
    global _current_engine
    valid = ("python", "jupyter", "streamlit")
    if engine not in valid:
        raise ValueError(
            f"Unknown engine {engine!r}. Choose from: {', '.join(valid)}"
        )
    _current_engine = engine


def get_engine() -> EngineType:
    """Return the currently configured rendering engine."""
    return _current_engine
