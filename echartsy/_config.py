"""Global configuration for echartsy rendering engine."""
from __future__ import annotations

from typing import Literal, Optional

EngineType = Literal["python", "jupyter", "streamlit"]
AdaptiveType = Literal["auto", "light", "dark"]

_current_engine: EngineType = "python"
_adaptive_theme: AdaptiveType = "auto"
_overlap_warnings: bool = True


def config(
    engine: EngineType,
    adaptive: AdaptiveType = "auto",
    overlap_warnings: Optional[bool] = None,
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
    overlap_warnings : bool, optional
        Whether to emit :class:`OverlapWarning` when the layout resolver
        auto-rotates labels or adjusts margins.  Defaults to ``True``.
        Set to ``False`` to silence the warnings while keeping the
        automatic layout fixes.

    Example
    -------
    >>> import echartsy as ec
    >>> ec.config(engine="jupyter")                   # auto-adapts
    >>> ec.config(engine="jupyter", adaptive="dark")  # force dark
    >>> ec.config(engine="jupyter", overlap_warnings=False)  # silent auto-fix
    """
    global _current_engine, _adaptive_theme, _overlap_warnings
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
    if overlap_warnings is not None:
        _overlap_warnings = overlap_warnings


def get_engine() -> EngineType:
    """Return the currently configured rendering engine."""
    return _current_engine


def get_adaptive() -> AdaptiveType:
    """Return the currently configured adaptive theme mode."""
    return _adaptive_theme


def get_overlap_warnings() -> bool:
    """Return whether overlap warnings are enabled."""
    return _overlap_warnings
