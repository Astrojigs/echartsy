"""Global configuration for echartsy rendering engine."""
from __future__ import annotations

from typing import Literal, Optional

EngineType = Literal["python", "jupyter", "streamlit"]
AdaptiveType = Literal["auto", "light", "dark"]

_current_engine: EngineType = "python"
_adaptive_theme: AdaptiveType = "auto"


def config(
    engine: EngineType,
    adaptive: AdaptiveType = "auto",
) -> None:
    """Set the global rendering engine and theme adaptation mode.

    Parameters
    ----------
    engine : ``"python"`` | ``"jupyter"`` | ``"streamlit"``
        - ``"python"``    — Opens an interactive HTML chart in the default
          browser (similar to ``plt.show()``).
        - ``"jupyter"``   — Renders an inline interactive widget in Jupyter
          Notebook / JupyterLab cells.
        - ``"streamlit"`` — Renders via ``streamlit-echarts`` inside a
          Streamlit application.
    adaptive : ``"auto"`` | ``"light"`` | ``"dark"``
        Controls how charts adapt to the environment's colour scheme.

        - ``"auto"``  — *(default)* Detect dark/light mode from the OS or
          browser ``prefers-color-scheme`` media query and adapt
          automatically.
        - ``"light"`` — Force light-mode text colours (original behaviour).
        - ``"dark"``  — Force dark-mode text colours and ECharts dark theme.

    Example
    -------
    >>> import echartsy as ec
    >>> ec.config(engine="jupyter")                   # auto-adapts
    >>> ec.config(engine="jupyter", adaptive="dark")  # force dark
    """
    global _current_engine, _adaptive_theme
    valid_engines = ("python", "jupyter", "streamlit")
    if engine not in valid_engines:
        raise ValueError(
            f"Unknown engine {engine!r}. Choose from: {', '.join(valid_engines)}"
        )
    valid_adaptive = ("auto", "light", "dark")
    if adaptive not in valid_adaptive:
        raise ValueError(
            f"Unknown adaptive mode {adaptive!r}. Choose from: {', '.join(valid_adaptive)}"
        )
    _current_engine = engine
    _adaptive_theme = adaptive


def get_engine() -> EngineType:
    """Return the currently configured rendering engine."""
    return _current_engine


def get_adaptive() -> AdaptiveType:
    """Return the currently configured adaptive theme mode."""
    return _adaptive_theme
