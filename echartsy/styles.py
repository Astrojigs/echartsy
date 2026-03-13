"""Style presets and colour palettes for echartsy."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

# ── Reusable palettes ────────────────────────────────────────────────────

PALETTE_RUSTY = ["#893448", "#d95850", "#eb8146", "#ffb248", "#f2d643", "#ebdba4"]
PALETTE_CLINICAL = [
    "#5470C6", "#91CC75", "#FAC858", "#EE6666", "#73C0DE",
    "#3BA272", "#FC8452", "#9A60B4", "#EA7CCC",
]
PALETTE_DARK = [
    "#dd6b66", "#759aa0", "#e69d87", "#8dc1a9", "#ea7e53",
    "#eedd78", "#73a373", "#73b9bc", "#7289ab", "#91ca8c",
]


@dataclass(frozen=True)
class StylePreset:
    """Immutable bundle of visual defaults that can be applied to a Figure.

    Use one of the class-level constants (``CLINICAL``, ``DASHBOARD_DARK``,
    etc.) or build your own.

    Example
    -------
    >>> fig = Figure(style=StylePreset.CLINICAL)
    >>> fig = Figure(style=StylePreset(palette=("#ff0000", "#00ff00"), bg="#fafafa"))
    """

    palette: Tuple[str, ...] = tuple(PALETTE_CLINICAL)
    bg: Optional[str] = None
    font_family: str = "sans-serif"
    title_font_size: int = 16
    subtitle_font_size: int = 12
    axis_label_font_size: int = 12
    axis_label_color: str = "#666"
    grid_line_color: str = "#eee"
    tooltip_pointer: str = "cross"
    legend_orient: str = "horizontal"

    # Pre-built presets (populated after class definition)
    CLINICAL: "StylePreset" = None  # type: ignore[assignment]
    DASHBOARD_DARK: "StylePreset" = None  # type: ignore[assignment]
    KPI_REPORT: "StylePreset" = None  # type: ignore[assignment]
    MINIMAL: "StylePreset" = None  # type: ignore[assignment]


# Populate class-level presets after the class is defined
StylePreset.CLINICAL = StylePreset()  # type: ignore[misc]
StylePreset.DASHBOARD_DARK = StylePreset(  # type: ignore[misc]
    palette=tuple(PALETTE_DARK),
    bg="#333",
    axis_label_color="#ccc",
    grid_line_color="#555",
)
StylePreset.KPI_REPORT = StylePreset(  # type: ignore[misc]
    palette=tuple(PALETTE_RUSTY),
    title_font_size=18,
    grid_line_color="#f0f0f0",
)
StylePreset.MINIMAL = StylePreset(  # type: ignore[misc]
    palette=("#5470C6", "#91CC75", "#FAC858", "#EE6666"),
    title_font_size=14,
    axis_label_font_size=11,
)
