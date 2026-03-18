"""Emphasis and focus styling for ECharts series and visual elements.

This module provides frozen dataclasses for configuring emphasis states, which are
the visual changes that occur when a user hovers over or interacts with chart elements.
All classes follow the pattern of converting Python snake_case attributes to ECharts
camelCase keys when serialized.

Example
-------
>>> item_style = ItemStyle(color="#ff0000", border_width=2)
>>> label = LabelStyle(show=True, font_size=12)
>>> emphasis = LineEmphasis(item_style=item_style, label=label, focus="series")
>>> chart_config = emphasis.to_dict()
"""
from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Literal, Optional, Union


# ── Shared helpers ────────────────────────────────────────────────────────


def _to_camel_case(snake_str: str) -> str:
    """Convert snake_case to camelCase."""
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def _dataclass_to_echarts_dict(obj) -> dict:
    """Convert a frozen dataclass to an ECharts camelCase dict.

    Omits ``None`` values and recursively serializes nested dataclasses
    that expose a ``to_dict()`` method.
    """
    result = {}
    for f in fields(obj):
        value = getattr(obj, f.name)
        if value is None:
            continue
        key = _to_camel_case(f.name)
        if hasattr(value, "to_dict"):
            result[key] = value.to_dict()
        else:
            result[key] = value
    return result


# ── Sub-style dataclasses ─────────────────────────────────────────────────────


@dataclass(frozen=True)
class ItemStyle:
    """Visual style for chart items (bars, points, etc.).

    Attributes
    ----------
    color : Optional[str]
        Fill color of the item.
    border_color : Optional[str]
        Border color (→ borderColor in ECharts).
    border_width : Optional[int]
        Border width in pixels (→ borderWidth).
    border_radius : Optional[int]
        Border radius in pixels (→ borderRadius).
    border_type : Optional[Union[str, list]]
        Border dash type (→ borderType), e.g. ``"solid"``, ``"dashed"``, or ``[5, 10]``.
    shadow_blur : Optional[int]
        Shadow blur radius (→ shadowBlur).
    shadow_color : Optional[str]
        Shadow color (→ shadowColor).
    shadow_offset_x : Optional[int]
        Horizontal shadow offset (→ shadowOffsetX).
    shadow_offset_y : Optional[int]
        Vertical shadow offset (→ shadowOffsetY).
    opacity : Optional[float]
        Opacity value between 0 and 1.
    decal : Optional[dict]
        Decal pattern configuration.
    """

    color: Optional[str] = None
    border_color: Optional[str] = None
    border_width: Optional[int] = None
    border_radius: Optional[int] = None
    border_type: Optional[Union[str, list]] = None
    shadow_blur: Optional[int] = None
    shadow_color: Optional[str] = None
    shadow_offset_x: Optional[int] = None
    shadow_offset_y: Optional[int] = None
    opacity: Optional[float] = None
    decal: Optional[dict] = None

    def to_dict(self) -> dict:
        """Convert to ECharts camelCase dictionary, omitting None values."""
        return _dataclass_to_echarts_dict(self)

    @staticmethod
    def _to_camel_case(snake_str: str) -> str:
        """Convert snake_case to camelCase."""
        return _to_camel_case(snake_str)


@dataclass(frozen=True)
class LabelStyle:
    """Style for text labels.

    Attributes
    ----------
    show : Optional[bool]
        Whether to display the label.
    position : Optional[str]
        Label position (e.g., "top", "bottom", "left", "right").
    formatter : Optional[str]
        Label text formatter string or template.
    font_size : Optional[int]
        Font size in pixels (→ fontSize).
    font_weight : Optional[str]
        Font weight (e.g., "bold", "normal", "400", "700").
    font_family : Optional[str]
        Font family (→ fontFamily).
    color : Optional[str]
        Text color.
    rotate : Optional[int]
        Label rotation in degrees.
    offset : Optional[list]
        Label offset ``[x, y]`` in pixels.
    align : Optional[str]
        Horizontal text alignment (e.g., "left", "center", "right").
    """

    show: Optional[bool] = None
    position: Optional[str] = None
    formatter: Optional[str] = None
    font_size: Optional[int] = None
    font_weight: Optional[str] = None
    font_family: Optional[str] = None
    color: Optional[str] = None
    rotate: Optional[int] = None
    offset: Optional[list] = None
    align: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to ECharts camelCase dictionary, omitting None values."""
        return _dataclass_to_echarts_dict(self)


@dataclass(frozen=True)
class LineStyle:
    """Style for lines and strokes.

    Attributes
    ----------
    color : Optional[str]
        Line color.
    width : Optional[int]
        Line width in pixels.
    type : Optional[Literal["solid", "dashed", "dotted"]]
        Line dash type.
    shadow_blur : Optional[int]
        Shadow blur radius (→ shadowBlur).
    shadow_color : Optional[str]
        Shadow color (→ shadowColor).
    shadow_offset_x : Optional[int]
        Horizontal shadow offset (→ shadowOffsetX).
    shadow_offset_y : Optional[int]
        Vertical shadow offset (→ shadowOffsetY).
    opacity : Optional[float]
        Opacity value between 0 and 1.
    cap : Optional[Literal["butt", "round", "square"]]
        Line cap style.
    join : Optional[Literal["bevel", "round", "miter"]]
        Line join style.
    """

    color: Optional[str] = None
    width: Optional[int] = None
    type: Optional[Literal["solid", "dashed", "dotted"]] = None
    shadow_blur: Optional[int] = None
    shadow_color: Optional[str] = None
    shadow_offset_x: Optional[int] = None
    shadow_offset_y: Optional[int] = None
    opacity: Optional[float] = None
    cap: Optional[Literal["butt", "round", "square"]] = None
    join: Optional[Literal["bevel", "round", "miter"]] = None

    def to_dict(self) -> dict:
        """Convert to ECharts camelCase dictionary, omitting None values."""
        return _dataclass_to_echarts_dict(self)


@dataclass(frozen=True)
class AreaStyle:
    """Style for filled areas.

    Attributes
    ----------
    color : Optional[str]
        Fill color.
    opacity : Optional[float]
        Opacity value between 0 and 1.
    origin : Optional[Literal["auto", "start", "end"]]
        Area fill origin.
    shadow_blur : Optional[int]
        Shadow blur radius (→ shadowBlur).
    shadow_color : Optional[str]
        Shadow color (→ shadowColor).
    """

    color: Optional[str] = None
    opacity: Optional[float] = None
    origin: Optional[Literal["auto", "start", "end"]] = None
    shadow_blur: Optional[int] = None
    shadow_color: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to ECharts camelCase dictionary, omitting None values."""
        return _dataclass_to_echarts_dict(self)


@dataclass(frozen=True)
class LabelLineStyle:
    """Style for lines connecting labels to data points.

    Attributes
    ----------
    show : Optional[bool]
        Whether to display the label line.
    length : Optional[int]
        Length of the first segment of the line.
    length2 : Optional[int]
        Length of the second segment of the line.
    """

    show: Optional[bool] = None
    length: Optional[int] = None
    length2: Optional[int] = None

    def to_dict(self) -> dict:
        """Convert to ECharts camelCase dictionary, omitting None values."""
        return _dataclass_to_echarts_dict(self)


# ── New sub-style dataclasses ─────────────────────────────────────────────


@dataclass(frozen=True)
class EndLabelStyle:
    """Style for labels at the end of a line series."""

    show: Optional[bool] = None
    formatter: Optional[str] = None
    font_size: Optional[int] = None
    font_weight: Optional[str] = None
    color: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to ECharts camelCase dictionary, omitting None values."""
        return _dataclass_to_echarts_dict(self)


@dataclass(frozen=True)
class TooltipStyle:
    """Per-series tooltip configuration."""

    show: Optional[bool] = None
    formatter: Optional[str] = None
    value_formatter: Optional[str] = None
    background_color: Optional[str] = None
    border_color: Optional[str] = None
    border_width: Optional[int] = None
    text_color: Optional[str] = None
    text_size: Optional[int] = None

    def to_dict(self) -> dict:
        """Convert to ECharts camelCase dictionary, omitting None values.

        Maps ``text_color`` and ``text_size`` into a nested ``textStyle`` dict.
        """
        result = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if value is None:
                continue
            if f.name == "text_color":
                result.setdefault("textStyle", {})["color"] = value
            elif f.name == "text_size":
                result.setdefault("textStyle", {})["fontSize"] = value
            else:
                result[_to_camel_case(f.name)] = value
        return result


@dataclass(frozen=True)
class AnimationConfig:
    """Animation settings for a series."""

    animation: Optional[bool] = None
    animation_duration: Optional[int] = None
    animation_easing: Optional[str] = None
    animation_delay: Optional[int] = None

    def to_dict(self) -> dict:
        """Convert to ECharts camelCase dictionary, omitting None values."""
        return _dataclass_to_echarts_dict(self)


@dataclass(frozen=True)
class Blur:
    """Blur state configuration (visual style for non-focused elements)."""

    item_style: Optional[ItemStyle] = None
    label: Optional[LabelStyle] = None
    line_style: Optional[LineStyle] = None
    area_style: Optional[AreaStyle] = None

    def to_dict(self) -> dict:
        """Convert to ECharts camelCase dictionary, omitting None values."""
        return _dataclass_to_echarts_dict(self)


@dataclass(frozen=True)
class Select:
    """Select state configuration for selected chart elements."""

    disabled: Optional[bool] = None
    item_style: Optional[ItemStyle] = None
    label: Optional[LabelStyle] = None
    line_style: Optional[LineStyle] = None
    area_style: Optional[AreaStyle] = None

    def to_dict(self) -> dict:
        """Convert to ECharts camelCase dictionary, omitting None values."""
        return _dataclass_to_echarts_dict(self)


# ── Emphasis dataclasses ──────────────────────────────────────────────────────


@dataclass(frozen=True)
class Emphasis:
    """Base emphasis configuration for interactive hover and focus states.

    Emphasis controls the visual appearance when a user hovers over or focuses on
    chart elements.

    Attributes
    ----------
    disabled : Optional[bool]
        Whether emphasis is disabled.
    focus : Optional[Literal["none", "self", "series"]]
        What to focus on: "none" (no focus), "self" (only item), or "series" (entire series).
    blur_scope : Optional[Literal["coordinateSystem", "series", "global"]]
        Scope of the blur effect (→ blurScope).
    item_style : Optional[ItemStyle]
        Visual style for the item during emphasis.
    label : Optional[LabelStyle]
        Label style during emphasis.
    """

    disabled: Optional[bool] = None
    focus: Optional[Literal["none", "self", "series"]] = None
    blur_scope: Optional[Literal["coordinateSystem", "series", "global"]] = None
    item_style: Optional[ItemStyle] = None
    label: Optional[LabelStyle] = None

    def to_dict(self) -> dict:
        """Convert to ECharts camelCase dictionary, omitting None values."""
        return _dataclass_to_echarts_dict(self)


@dataclass(frozen=True)
class LineEmphasis(Emphasis):
    """Emphasis configuration for line charts.

    Adds line, area, and end label styling on top of base emphasis.

    Attributes
    ----------
    line_style : Optional[LineStyle]
        Line style during emphasis (→ lineStyle).
    area_style : Optional[AreaStyle]
        Area fill style during emphasis (→ areaStyle).
    end_label : Optional[EndLabelStyle]
        Label style for line endpoints (→ endLabel).
    """

    line_style: Optional[LineStyle] = None
    area_style: Optional[AreaStyle] = None
    end_label: Optional[EndLabelStyle] = None

    def to_dict(self) -> dict:
        """Convert to ECharts camelCase dictionary, omitting None values."""
        return _dataclass_to_echarts_dict(self)


@dataclass(frozen=True)
class ScatterEmphasis(Emphasis):
    """Emphasis configuration for scatter plots.

    Adds scale control on top of base emphasis.

    Attributes
    ----------
    scale : Optional[bool]
        Whether to scale the point during emphasis.
    """

    scale: Optional[bool] = None

    def to_dict(self) -> dict:
        """Convert to ECharts camelCase dictionary, omitting None values."""
        return _dataclass_to_echarts_dict(self)


@dataclass(frozen=True)
class PieEmphasis(Emphasis):
    """Emphasis configuration for pie charts.

    Adds scaling and label line styling on top of base emphasis.

    Attributes
    ----------
    scale : Optional[bool]
        Whether to scale the slice during emphasis.
    scale_size : Optional[int]
        Scale size in pixels (→ scaleSize).
    label_line : Optional[LabelLineStyle]
        Style for label connecting lines (→ labelLine).
    """

    scale: Optional[bool] = None
    scale_size: Optional[int] = None
    label_line: Optional[LabelLineStyle] = None

    def to_dict(self) -> dict:
        """Convert to ECharts camelCase dictionary, omitting None values."""
        return _dataclass_to_echarts_dict(self)


@dataclass(frozen=True)
class RadarEmphasis(Emphasis):
    """Emphasis configuration for radar charts.

    Adds line and area styling on top of base emphasis.

    Attributes
    ----------
    line_style : Optional[LineStyle]
        Line style during emphasis (→ lineStyle).
    area_style : Optional[AreaStyle]
        Area fill style during emphasis (→ areaStyle).
    """

    line_style: Optional[LineStyle] = None
    area_style: Optional[AreaStyle] = None

    def to_dict(self) -> dict:
        """Convert to ECharts camelCase dictionary, omitting None values."""
        return _dataclass_to_echarts_dict(self)


@dataclass(frozen=True)
class SankeyEmphasis(Emphasis):
    """Emphasis configuration for Sankey diagrams.

    Extends focus to include "adjacency" mode, and adds line styling.

    Attributes
    ----------
    focus : Optional[Literal["none", "self", "series", "adjacency"]]
        What to focus on: additionally supports "adjacency" for related nodes.
    line_style : Optional[LineStyle]
        Line style during emphasis (→ lineStyle).
    """

    focus: Optional[Literal["none", "self", "series", "adjacency"]] = None  # type: ignore[assignment]
    line_style: Optional[LineStyle] = None

    def to_dict(self) -> dict:
        """Convert to ECharts camelCase dictionary, omitting None values."""
        return _dataclass_to_echarts_dict(self)


@dataclass(frozen=True)
class FunnelEmphasis(Emphasis):
    """Emphasis configuration for funnel charts.

    Adds label line styling on top of base emphasis.

    Attributes
    ----------
    label_line : Optional[LabelLineStyle]
        Style for label connecting lines (→ labelLine).
    """

    label_line: Optional[LabelLineStyle] = None

    def to_dict(self) -> dict:
        """Convert to ECharts camelCase dictionary, omitting None values."""
        return _dataclass_to_echarts_dict(self)


@dataclass(frozen=True)
class TreemapEmphasis(Emphasis):
    """Emphasis configuration for treemap charts.

    Adds label line and upper label styling on top of base emphasis.

    Attributes
    ----------
    label_line : Optional[LabelLineStyle]
        Style for label connecting lines (→ labelLine).
    upper_label : Optional[LabelStyle]
        Style for the upper-level label (→ upperLabel).
    """

    label_line: Optional[LabelLineStyle] = None
    upper_label: Optional[LabelStyle] = None

    def to_dict(self) -> dict:
        """Convert to ECharts camelCase dictionary, omitting None values."""
        return _dataclass_to_echarts_dict(self)


@dataclass(frozen=True)
class GraphEmphasis(Emphasis):
    """Emphasis configuration for graph/network charts.

    Extends focus to include "adjacency" mode for connected nodes.

    Attributes
    ----------
    focus : Optional[Literal["none", "self", "series", "adjacency"]]
        What to focus on: additionally supports "adjacency" for connected nodes.
    line_style : Optional[LineStyle]
        Line style during emphasis (→ lineStyle).
    """

    focus: Optional[Literal["none", "self", "series", "adjacency"]] = None  # type: ignore[assignment]
    line_style: Optional[LineStyle] = None

    def to_dict(self) -> dict:
        """Convert to ECharts camelCase dictionary, omitting None values."""
        return _dataclass_to_echarts_dict(self)
