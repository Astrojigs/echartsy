"""
echartslib — A matplotlib-style fluent builder API for Apache ECharts.

Quick-start
-----------
>>> import echartslib as ec
>>> ec.config(engine="jupyter")  # or "python" or "streamlit"
>>>
>>> (
...     ec.Figure(height="500px")
...     .bar(df, x="Month", y="Revenue", hue="Region", stack=True)
...     .plot(df_totals, x="Month", y="Target", smooth=True, axis=1)
...     .title("Revenue vs Target")
...     .ylabel("Revenue")
...     .ylabel_right("Target (%)")
...     .show()
... )
"""
from echartslib._config import config, get_engine
from echartslib.exceptions import (
    BuilderConfigError,
    BuilderError,
    DataValidationError,
    OverlapWarning,
    TimelineConfigError,
)
from echartslib.figure import Figure, figure
from echartslib.styles import (
    PALETTE_CLINICAL,
    PALETTE_DARK,
    PALETTE_RUSTY,
    StylePreset,
)
from echartslib.timeline import (
    TimelineFigure,
    detect_time_format,
    timeline_figure,
)

__version__ = "0.1.0"

__all__ = [
    # Config
    "config",
    "get_engine",
    # Figure
    "Figure",
    "figure",
    # Timeline
    "TimelineFigure",
    "timeline_figure",
    "detect_time_format",
    # Styles
    "StylePreset",
    "PALETTE_CLINICAL",
    "PALETTE_DARK",
    "PALETTE_RUSTY",
    # Exceptions
    "BuilderError",
    "BuilderConfigError",
    "DataValidationError",
    "TimelineConfigError",
    "OverlapWarning",
]
