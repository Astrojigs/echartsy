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
from typing import Literal, Optional


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
    """

    color: Optional[str] = None
    border_color: Optional[str] = None
    border_width: Optional[int] = None
    border_radius: Optional[int] = None
    shadow_blur: Optional[int] = None
    shadow_color: Optional[str] = None
    shadow_offset_x: Optional[int] = None
    shadow_offset_y: Optional[int] = None
    opacity: Optional[float] = None

    def to_dict(self) -> dict:
        """Convert to ECharts camelCase dictionary, omitting None values."""
        result = {}
        for field in fields(self):
            value = getattr(self, field.name)
            if value is not None:
                # Convert snake_case to camelCase
                key = self._to_camel_case(field.name)
                result[key] = value
        return result

    @staticmethod
    def _to_camel_case(snake_str: str) -> str:
        """Convert snake_case to camelCase."""
        components = snake_str.split("_")
        return components[0] + "".join(x.title() for x in components[1:])


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
    color : Optional[str]
        Text color.
    """

    show: Optional[bool] = None
    position: Optional[str] = None
    formatter: Optional[str] = None
    font_size: Optional[int] = None
    font_weight: Optional[str] = None
    color: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to ECharts camelCase dictionary, omitting None values."""
        result = {}
        for field in fields(self):
            value = getattr(self, field.name)
            if value is not None:
                key = ItemStyle._to_camel_case(field.name)
                result[key] = value
        return result


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
    opacity : Optional[float]
        Opacity value between 0 and 1.
    """

    color: Optional[str] = None
    width: Optional[int] = None
    type: Optional[Literal["solid", "dashed", "dotted"]] = None
    shadow_blur: Optional[int] = None
    opacity: Optional[float] = None

    def to_dict(self) -> dict:
        """Convert to ECharts camelCase dictionary, omitting None values."""
        result = {}
        for field in fields(self):
            value = getattr(self, field.name)
            if value is not None:
                key = ItemStyle._to_camel_case(field.name)
                result[key] = value
        return result


@dataclass(frozen=True)
class AreaStyle:
    """Style for filled areas.

    Attributes
    ----------
    color : Optional[str]
        Fill color.
    opacity : Optional[float]
        Opacity value between 0 and 1.
    """

    color: Optional[str] = None
    opacity: Optional[float] = None

    def to_dict(self) -> dict:
        """Convert to ECharts camelCase dictionary, omitting None values."""
        result = {}
        for field in fields(self):
            value = getattr(self, field.name)
            if value is not None:
                key = ItemStyle._to_camel_case(field.name)
                result[key] = value
        return result


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
        result = {}
        for field in fields(self):
            value = getattr(self, field.name)
            if value is not None:
                key = ItemStyle._to_camel_case(field.name)
                result[key] = value
        return result


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
        result = {}
        for field in fields(self):
            value = getattr(self, field.name)
            if value is None:
                continue

            key = ItemStyle._to_camel_case(field.name)

            # Serialize nested dataclasses
            if hasattr(value, "to_dict"):
                result[key] = value.to_dict()
            else:
                result[key] = value

        return result


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
    end_label : Optional[LabelStyle]
        Label style for line endpoints (→ endLabel).
    """

    line_style: Optional[LineStyle] = None
    area_style: Optional[AreaStyle] = None
    end_label: Optional[LabelStyle] = None

    def to_dict(self) -> dict:
        """Convert to ECharts camelCase dictionary, omitting None values."""
        result = super().to_dict()

        # Add LineEmphasis-specific fields
        if self.line_style is not None:
            result["lineStyle"] = self.line_style.to_dict()
        if self.area_style is not None:
            result["areaStyle"] = self.area_style.to_dict()
        if self.end_label is not None:
            result["endLabel"] = self.end_label.to_dict()

        return result


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
        result = super().to_dict()

        if self.scale is not None:
            result["scale"] = self.scale

        return result


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
        result = super().to_dict()

        if self.scale is not None:
            result["scale"] = self.scale
        if self.scale_size is not None:
            result["scaleSize"] = self.scale_size
        if self.label_line is not None:
            result["labelLine"] = self.label_line.to_dict()

        return result


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
        result = super().to_dict()

        if self.line_style is not None:
            result["lineStyle"] = self.line_style.to_dict()
        if self.area_style is not None:
            result["areaStyle"] = self.area_style.to_dict()

        return result


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
        result = super().to_dict()

        if self.line_style is not None:
            result["lineStyle"] = self.line_style.to_dict()

        return result


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
        result = super().to_dict()

        if self.label_line is not None:
            result["labelLine"] = self.label_line.to_dict()

        return result


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
        result = super().to_dict()

        if self.label_line is not None:
            result["labelLine"] = self.label_line.to_dict()
        if self.upper_label is not None:
            result["upperLabel"] = self.upper_label.to_dict()

        return result
