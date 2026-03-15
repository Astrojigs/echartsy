"""
Figure — the top-level chart canvas for echartsy.

Equivalent to ``plt.figure()`` + ``plt.subplots()`` in matplotlib.
Collects series incrementally via ``.plot()``, ``.bar()``, etc.,
stores axis / legend / tooltip configuration, and renders everything
in a single call to ``.show()``.
"""
from __future__ import annotations

import copy
import itertools
import warnings
from dataclasses import dataclass, field
from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    Union,
)

import numpy as np
import pandas as pd

from echartsy._helpers import (
    _coerce_numeric,
    _resolve_agg,
    _resolve_layout,
    _sort_categories,
    _validate_columns,
    _validate_df,
)
from echartsy.exceptions import BuilderConfigError, DataValidationError
from echartsy.renderers import render
from echartsy.styles import StylePreset
from echartsy.emphasis import (
    Emphasis, LineEmphasis, ScatterEmphasis, PieEmphasis,
    RadarEmphasis, SankeyEmphasis, FunnelEmphasis, TreemapEmphasis,
)


# ═══════════════════════════════════════════════════════════════════════════
# Internal series-builder dataclass
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class _SeriesMeta:
    """Book-keeping for one logical series."""
    chart_type: str
    name: str = ""
    y_axis_index: int = 0
    is_category_series: bool = True
    raw_config: dict = field(default_factory=dict)


_FIGURE_COUNTER = itertools.count()

# ═══════════════════════════════════════════════════════════════════════════
# ██  FIGURE  ██
# ═══════════════════════════════════════════════════════════════════════════

class Figure:
    """The top-level chart canvas — equivalent to ``plt.figure()``.

    Parameters
    ----------
    height : str
        CSS height of the rendered chart container (e.g. ``"500px"``).
    width : str or None
        CSS width; ``None`` means container width.
    renderer : ``{"canvas", "svg"}``
        ECharts renderer.
    theme : str or None
        ECharts built-in theme name (e.g. ``"dark"``).
    style : StylePreset or None
        Apply a :class:`StylePreset` bundle for palette, font sizes, etc.
    key : str or None
        Explicit Streamlit widget key. Auto-generated when ``None``.

    Example
    -------
    >>> import echartsy as ec
    >>> ec.config(engine="jupyter")
    >>> fig = ec.Figure(height="600px", style=ec.StylePreset.CLINICAL)
    >>> fig.bar(df, x="Month", y="Revenue").title("Monthly Revenue").show()
    """

    def __init__(
        self,
        height: str = "400px",
        width: Optional[str] = None,
        renderer: Literal["canvas", "svg"] = "canvas",
        theme: Optional[str] = None,
        style: Optional[StylePreset] = None,
        key: Optional[str] = None,
    ) -> None:
        self._height = height
        self._width = width
        self._renderer = renderer
        self._theme = theme
        self._key = key
        self._style = style or StylePreset.CLINICAL

        # Internal state
        self._series: List[dict] = []
        self._series_meta: List[_SeriesMeta] = []
        self._legend_items: List[str] = []
        self._user_set_rotate: bool = False  # True if user explicitly set label rotation

        # Axis storage
        self._x_axis: dict = {
            "type": "category",
            "data": [],
            "axisLabel": {
                "rotate": 0,
                "fontSize": self._style.axis_label_font_size,
                "color": self._style.axis_label_color,
            },
            "axisTick": {"show": False},
        }
        self._y_axes: List[dict] = [
            {
                "type": "value",
                "splitLine": {"show": True, "lineStyle": {"color": self._style.grid_line_color}},
                "axisLabel": {
                    "fontSize": self._style.axis_label_font_size,
                    "color": self._style.axis_label_color,
                },
            }
        ]
        self._x_categories: List[str] = []

        # Layout / chrome
        self._title_cfg: Optional[dict] = None
        self._legend_cfg: Optional[dict] = None
        self._tooltip_cfg: dict = {
            "trigger": "axis",
            "axisPointer": {"type": self._style.tooltip_pointer},
            "confine": True,
            "appendTo": "body",
        }
        self._grid_cfg: dict = {
            "left": 70, "right": 70,
            "top": 60, "bottom": 50,
            "containLabel": True,
        }
        self._toolbox_cfg: Optional[dict] = None
        self._datazoom_cfg: Optional[list] = None
        self._palette: Optional[Sequence[str]] = (
            list(self._style.palette) if self._style.palette else None
        )
        self._extra: dict = {}

        # Track chart mode for conflict detection
        self._chart_mode: Optional[str] = None  # "cartesian" | "pie" | "radar" | ...

    # ─── Repr ─────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        n = len(self._series)
        return f"<Figure series={n} height={self._height!r} mode={self._chart_mode!r}>"

    # ─── Private helpers ──────────────────────────────────────────────────

    def _ensure_mode(self, mode: str, caller: str) -> None:
        if self._chart_mode is None:
            self._chart_mode = mode
        elif self._chart_mode != mode:
            raise BuilderConfigError(
                f"{caller}() requires mode '{mode}' but figure is already in "
                f"'{self._chart_mode}' mode. Create a new Figure for a different chart type."
            )

    def _ensure_cartesian(self, caller: str) -> None:
        self._ensure_mode("cartesian", caller)

    def _merge_x_categories(self, new_cats: List[str]) -> None:
        existing = set(self._x_categories)
        for c in new_cats:
            if c not in existing:
                self._x_categories.append(c)
                existing.add(c)

    def _auto_key(self) -> str:
        return f"ecb_{next(_FIGURE_COUNTER)}"

    def _align_to_categories(
        self, df: pd.DataFrame, x: str, y: str, agg: str = "mean",
    ) -> List[Optional[float]]:
        agg_fn = _resolve_agg(agg)
        grouped = df.groupby(x)[y].agg(agg_fn)
        return [
            None if cat not in grouped.index or pd.isna(grouped.get(cat))
            else round(float(grouped.get(cat)), 4)
            for cat in self._x_categories
        ]

    # ═══════════════════════════════════════════════════════════════════════
    # Chrome configuration (title, axes, legend, tooltip, grid, …)
    # ═══════════════════════════════════════════════════════════════════════

    def title(
        self, text: str, subtitle: Optional[str] = None,
        left: str = "center", top: Optional[Union[str, int]] = None,
    ) -> "Figure":
        """Set the chart title (and optional subtitle).

        Returns self for chaining.
        """
        self._title_cfg = {
            "text": text, "left": left,
            "textStyle": {
                "fontSize": self._style.title_font_size,
                "fontFamily": self._style.font_family,
            },
        }
        if subtitle:
            self._title_cfg["subtext"] = subtitle
            self._title_cfg["subtextStyle"] = {"fontSize": self._style.subtitle_font_size}
        if top is not None:
            self._title_cfg["top"] = top
        return self

    def xlabel(
        self, name: str, rotate: Optional[int] = None,
        font_size: Optional[int] = None, color: Optional[str] = None,
    ) -> "Figure":
        """Configure the x-axis label and tick styling."""
        self._x_axis["name"] = name
        lbl = self._x_axis.setdefault("axisLabel", {})
        if rotate is not None:
            lbl["rotate"] = rotate
            self._user_set_rotate = True
        if font_size is not None:
            lbl["fontSize"] = font_size
        if color is not None:
            lbl["color"] = color
        return self

    def xticks(
        self, rotate: Optional[int] = None,
        interval: Optional[Union[int, str]] = None,
        formatter: Optional[str] = None,
    ) -> "Figure":
        """Fine-tune x-axis tick marks."""
        lbl = self._x_axis.setdefault("axisLabel", {})
        if rotate is not None:
            lbl["rotate"] = rotate
            self._user_set_rotate = True
        if interval is not None:
            lbl["interval"] = interval
        if formatter is not None:
            lbl["formatter"] = formatter
        return self

    def xlim(self, min_val: Optional[float] = None, max_val: Optional[float] = None) -> "Figure":
        """Set explicit x-axis bounds (value-type axes only)."""
        if self._chart_mode == "pie":
            raise BuilderConfigError("xlim() is not applicable to pie charts.")
        if min_val is not None:
            self._x_axis["min"] = min_val
        if max_val is not None:
            self._x_axis["max"] = max_val
        return self

    def ylabel(
        self, name: str, font_size: Optional[int] = None,
        color: Optional[str] = None,
    ) -> "Figure":
        """Set the primary (left) y-axis title."""
        self._y_axes[0]["name"] = name
        if font_size is not None:
            self._y_axes[0].setdefault("axisLabel", {})["fontSize"] = font_size
        if color is not None:
            self._y_axes[0].setdefault("axisLabel", {})["color"] = color
        return self

    def ylabel_right(
        self, name: str, font_size: Optional[int] = None,
        color: Optional[str] = None,
    ) -> "Figure":
        """Set the secondary (right) y-axis title, creating the axis if needed."""
        if len(self._y_axes) < 2:
            self._y_axes.append({
                "type": "value",
                "splitLine": {"show": False},
                "axisLabel": {
                    "fontSize": self._style.axis_label_font_size,
                    "color": self._style.axis_label_color,
                },
            })
        self._y_axes[1]["name"] = name
        if font_size is not None:
            self._y_axes[1].setdefault("axisLabel", {})["fontSize"] = font_size
        if color is not None:
            self._y_axes[1].setdefault("axisLabel", {})["color"] = color
        return self

    def ylim(
        self, min_val: Optional[float] = None,
        max_val: Optional[float] = None, axis: int = 0,
    ) -> "Figure":
        """Set y-axis bounds."""
        if axis < 0:
            raise ValueError("axis index must be non-negative")
        if axis >= len(self._y_axes):
            raise BuilderConfigError(
                f"ylim(axis={axis}) — only {len(self._y_axes)} y-axis(es) exist. "
                "Call ylabel_right() first to create a second axis."
            )
        if min_val is not None:
            self._y_axes[axis]["min"] = min_val
        if max_val is not None:
            self._y_axes[axis]["max"] = max_val
        return self

    def yticks(
        self, rotate: Optional[int] = None,
        interval: Optional[Union[int, str]] = None,
        formatter: Optional[str] = None, axis: int = 0,
    ) -> "Figure":
        """Configure y-axis tick display."""
        if axis >= len(self._y_axes):
            raise BuilderConfigError(f"yticks(axis={axis}) — axis does not exist yet.")
        lbl = self._y_axes[axis].setdefault("axisLabel", {})
        if rotate is not None:
            lbl["rotate"] = rotate
        if interval is not None:
            lbl["interval"] = interval
        if formatter is not None:
            lbl["formatter"] = formatter
        return self

    def grid(
        self, show: Optional[bool] = None,
        axis: Literal["x", "y", "both"] = "y",
        style: str = "solid", color: Optional[str] = None,
    ) -> "Figure":
        """Toggle grid-line visibility and styling."""
        targets = []
        if axis in ("y", "both"):
            targets.append(self._y_axes[0])
        if axis in ("x", "both"):
            targets.append(self._x_axis)
        for t in targets:
            sl = t.setdefault("splitLine", {})
            if show is not None:
                sl["show"] = show
            ls = sl.setdefault("lineStyle", {})
            ls["type"] = style
            if color:
                ls["color"] = color
        return self

    def margins(
        self, left: Optional[Union[int, str]] = None,
        right: Optional[Union[int, str]] = None,
        top: Optional[Union[int, str]] = None,
        bottom: Optional[Union[int, str]] = None,
    ) -> "Figure":
        """Set explicit grid margins."""
        if left is not None:
            self._grid_cfg["left"] = left
        if right is not None:
            self._grid_cfg["right"] = right
        if top is not None:
            self._grid_cfg["top"] = top
        if bottom is not None:
            self._grid_cfg["bottom"] = bottom
        return self

    def legend(
        self, show: bool = True,
        orient: Optional[Literal["horizontal", "vertical"]] = None,
        left: Optional[str] = None,
        top: Optional[Union[str, int]] = None,
        bottom: Optional[Union[str, int]] = None,
    ) -> "Figure":
        """Configure legend placement and visibility."""
        cfg: dict = {"show": show}
        cfg["orient"] = orient or self._style.legend_orient
        if left is not None:
            cfg["left"] = left
        if top is not None:
            cfg["top"] = top
        if bottom is not None:
            cfg["bottom"] = bottom
        self._legend_cfg = cfg
        return self

    def tooltip(
        self, trigger: Literal["item", "axis", "none"] = "axis",
        pointer: Literal["cross", "shadow", "line", "none"] = "cross",
        formatter: Optional[str] = None,
    ) -> "Figure":
        """Configure tooltip behaviour."""
        self._tooltip_cfg["trigger"] = trigger
        self._tooltip_cfg["axisPointer"] = {"type": pointer}
        if formatter:
            self._tooltip_cfg["formatter"] = formatter
        return self

    def save(
        self, name: str = "chart",
        fmt: Literal["png", "svg"] = "png",
        dpi: int = 3, bg: Optional[str] = "#ffffff",
    ) -> "Figure":
        """Enable the download button in the ECharts toolbox."""
        self._toolbox_cfg = {
            "show": True, "right": 10, "top": 10,
            "feature": {
                "saveAsImage": {
                    "show": True, "type": fmt, "name": name,
                    "pixelRatio": dpi, "backgroundColor": bg,
                },
                "restore": {"show": True},
            },
        }
        return self

    def toolbox(
        self, download: bool = True, zoom: bool = False,
        restore: bool = True,
    ) -> "Figure":
        """Configure which toolbox features are visible."""
        features: dict = {}
        if download:
            features["saveAsImage"] = {"show": True, "pixelRatio": 3}
        if zoom:
            features["dataZoom"] = {"show": True}
        if restore:
            features["restore"] = {"show": True}
        self._toolbox_cfg = {"show": True, "right": 10, "top": 10, "feature": features}
        return self

    def datazoom(
        self, start: int = 0, end: int = 100,
        orient: Literal["horizontal", "vertical"] = "horizontal",
        show_slider: bool = True,
    ) -> "Figure":
        """Add a data-zoom slider for long time-series or many categories."""
        if not (0 <= start <= 100) or not (0 <= end <= 100):
            raise ValueError("datazoom start/end must be between 0 and 100")
        zoom: list = [{"type": "inside", "start": start, "end": end, "orient": orient}]
        if show_slider:
            zoom.append({"type": "slider", "start": start, "end": end, "orient": orient})
        self._datazoom_cfg = zoom
        return self

    def palette(self, colors: Sequence[str]) -> "Figure":
        """Set the global colour cycle for all series."""
        self._palette = list(colors)
        return self

    def extra(self, **kwargs: Any) -> "Figure":
        """Merge arbitrary top-level ECharts options (escape hatch)."""
        self._extra.update(kwargs)
        return self

    def raw_series(self, config: dict) -> "Figure":
        """Inject a raw ECharts series dict (escape hatch for composite charts).

        Use this to overlay chart types that would normally conflict —
        for example, a small pie chart on top of a bar chart.

        The ``config`` dict is appended directly to the series list with
        no mode-locking or validation.

        Parameters
        ----------
        config : dict
            A raw ECharts series configuration, e.g.
            ``{"type": "pie", "radius": "30%", "center": ["75%", "25%"],
            "data": [{"name": "A", "value": 10}, ...]}``

        Returns
        -------
        Figure
            Self, for chaining.

        Example
        -------
        >>> (ec.Figure()
        ...  .bar(df, x="Month", y="Revenue")
        ...  .raw_series({
        ...      "type": "pie", "radius": "25%",
        ...      "center": ["80%", "25%"],
        ...      "data": [{"name": "A", "value": 40}, {"name": "B", "value": 60}],
        ...      "label": {"fontSize": 10},
        ...  })
        ...  .show())
        """
        self._series.append(config)
        self._series_meta.append(_SeriesMeta(
            chart_type=config.get("type", "custom"),
            name=config.get("name", ""),
            raw_config=config,
        ))
        # Extend legend if the raw series has named data items
        if "name" in config and config["name"]:
            self._legend_items.append(config["name"])
        return self

    # ═══════════════════════════════════════════════════════════════════════
    # Series methods
    # ═══════════════════════════════════════════════════════════════════════

    # ─── LINE ─────────────────────────────────────────────────────────────

    def plot(
        self, df: pd.DataFrame, x: str, y: str, *,
        hue: Optional[str] = None, smooth: bool = False,
        area: bool = False, area_opacity: float = 0.15,
        connect_nulls: bool = False, line_width: int = 2,
        symbol_size: int = 6, symbol: str = "circle",
        labels: bool = False, label_position: str = "top",
        label_prefix: str = "", label_suffix: str = "",
        agg: str = "mean", axis: int = 0, emphasis: Optional[LineEmphasis] = None, **series_kw: Any,
    ) -> "Figure":
        """Add one or more line series — equivalent to ``plt.plot()``.

        Parameters
        ----------
        df : pd.DataFrame
            Source data.
        x : str
            Category-axis column.
        y : str
            Value-axis column.
        hue : str or None
            Grouping column — one line per unique value.
        smooth : bool
            Bezier-smooth the line.
        area : bool
            Fill the area under the line.
        """
        self._ensure_cartesian("plot")
        df = _validate_df(df, "plot")
        _validate_columns(df, [x, y, hue], "plot")

        dff = df.copy()
        dff[x] = dff[x].astype(str).str.strip()
        dff[y] = _coerce_numeric(dff, y, "plot")
        if hue:
            dff[hue] = dff[hue].astype(str).str.strip()
            dff = dff.dropna(subset=[hue])
        n_before = len(dff)
        dff = dff.dropna(subset=[x, y])
        n_dropped = n_before - len(dff)
        if n_dropped > 0:
            warnings.warn(f"plot(): {n_dropped} rows dropped due to missing values", stacklevel=2)
        if dff.empty:
            warnings.warn("plot(): all rows dropped after removing missing values; chart will be empty", stacklevel=2)
            return self

        cats = _sort_categories(dff[x])
        self._merge_x_categories(cats)

        if axis == 1 and len(self._y_axes) < 2:
            self.ylabel_right("")

        base: dict = {
            "type": "line", "smooth": smooth,
            "connectNulls": connect_nulls, "showSymbol": True,
            "symbol": symbol, "symbolSize": symbol_size,
            "lineStyle": {"width": line_width}, "yAxisIndex": axis,
        }
        if area:
            base["areaStyle"] = {"opacity": area_opacity}
        if labels:
            base["label"] = {
                "show": True, "position": label_position,
                "formatter": f"{label_prefix}{{c}}{label_suffix}",
            }
        if emphasis is not None:
            base["emphasis"] = emphasis.to_dict()
        base.update(series_kw)

        groups = dff.groupby(hue) if hue else [(y, dff)]
        for name, grp in groups:
            name_str = str(name)
            values = self._align_to_categories(grp, x, y, agg)
            entry = {**base, "name": name_str, "data": values}
            self._series.append(entry)
            self._series_meta.append(_SeriesMeta("line", name_str, axis))
            if name_str not in self._legend_items:
                self._legend_items.append(name_str)

        return self

    # ─── BAR ──────────────────────────────────────────────────────────────

    def bar(
        self, df: pd.DataFrame, x: str, y: str, *,
        hue: Optional[str] = None, stack: bool = False,
        orient: Literal["v", "h"] = "v",
        bar_width: Optional[Union[int, str]] = None,
        bar_gap: Optional[str] = None,
        border_radius: int = 4, labels: bool = False,
        label_formatter: str = "{c}", label_font_size: int = 12,
        label_color: str = "#333",
        gradient: bool = False,
        gradient_colors: Tuple[str, str] = ("#83bff6", "#188df0"),
        agg: str = "sum", axis: int = 0, emphasis: Optional[Emphasis] = None, **series_kw: Any,
    ) -> "Figure":
        """Add one or more bar series — equivalent to ``plt.bar()``.

        Parameters
        ----------
        df : pd.DataFrame
        x : str
            Category column.
        y : str
            Value column.
        hue : str or None
            Grouping column.
        stack : bool
            Stack bars of different hue values.
        orient : ``"v"`` or ``"h"``
            ``"v"`` = vertical bars, ``"h"`` = horizontal bars.
        """
        self._ensure_cartesian("bar")
        df = _validate_df(df, "bar")
        _validate_columns(df, [x, y, hue], "bar")

        dff = df.copy()
        dff[x] = dff[x].astype(str).str.strip()
        dff[y] = _coerce_numeric(dff, y, "bar")
        if hue:
            dff[hue] = dff[hue].astype(str).str.strip()
            dff = dff.dropna(subset=[hue])
        n_before = len(dff)
        dff = dff.dropna(subset=[x, y])
        n_dropped = n_before - len(dff)
        if n_dropped > 0:
            warnings.warn(f"bar(): {n_dropped} rows dropped due to missing values", stacklevel=2)
        if dff.empty:
            warnings.warn("bar(): all rows dropped after removing missing values; chart will be empty", stacklevel=2)
            return self

        if orient == "h":
            self._x_axis["type"] = "value"
            cats = _sort_categories(dff[x])
            self._merge_x_categories(cats)
        else:
            cats = _sort_categories(dff[x])
            self._merge_x_categories(cats)

        if axis == 1 and len(self._y_axes) < 2:
            self.ylabel_right("")

        label_pos = "top" if orient == "v" else "right"
        item_style: dict = {"borderRadius": border_radius}
        if gradient:
            if len(gradient_colors) != 2:
                raise ValueError("gradient_colors must be a tuple of exactly 2 color strings")
            item_style["color"] = {
                "type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                "colorStops": [
                    {"offset": 0, "color": gradient_colors[0]},
                    {"offset": 1, "color": gradient_colors[1]},
                ],
            }

        base: dict = {
            "type": "bar",
            "label": {
                "show": labels, "position": label_pos,
                "formatter": label_formatter, "fontSize": label_font_size,
                "color": label_color,
            },
            "itemStyle": item_style, "yAxisIndex": axis,
        }
        if stack:
            base["stack"] = "total"
        if bar_width is not None:
            base["barMaxWidth"] = bar_width
        if bar_gap is not None:
            base["barGap"] = bar_gap
        if emphasis is not None:
            base["emphasis"] = emphasis.to_dict()
        base.update(series_kw)

        groups = dff.groupby(hue) if hue else [(y, dff)]
        for name, grp in groups:
            name_str = str(name)
            values = self._align_to_categories(grp, x, y, agg)
            entry = {**base, "name": name_str, "data": values}
            self._series.append(entry)
            self._series_meta.append(_SeriesMeta("bar", name_str, axis))
            if name_str not in self._legend_items:
                self._legend_items.append(name_str)

        if orient == "h":
            self._extra["_bar_orient_h"] = True

        return self

    # ─── SCATTER ──────────────────────────────────────────────────────────

    def scatter(
        self, df: pd.DataFrame, x: str, y: str, *,
        color: Optional[str] = None, size: Optional[str] = None,
        size_range: Tuple[int, int] = (5, 30), symbol: str = "circle",
        opacity: float = 0.7, labels: bool = False,
        emphasis: Optional[ScatterEmphasis] = None, **series_kw: Any,
    ) -> "Figure":
        """Add a scatter series — equivalent to ``plt.scatter()``."""
        self._ensure_cartesian("scatter")
        df = _validate_df(df, "scatter")
        _validate_columns(df, [x, y, color, size], "scatter")

        dff = df.copy()
        dff[x] = _coerce_numeric(dff, x, "scatter")
        dff[y] = _coerce_numeric(dff, y, "scatter")
        n_before = len(dff)
        dff = dff.dropna(subset=[x, y])
        n_dropped = n_before - len(dff)
        if n_dropped > 0:
            warnings.warn(f"scatter(): {n_dropped} rows dropped due to missing values", stacklevel=2)
        if dff.empty:
            warnings.warn("scatter(): all rows dropped after removing missing values; chart will be empty", stacklevel=2)
            return self

        self._x_axis["type"] = "value"
        self._x_axis.pop("data", None)
        self._tooltip_cfg["trigger"] = "item"

        def _build_scatter_data(sub: pd.DataFrame) -> List[list]:
            return [[float(r[x]), float(r[y])] for _, r in sub.iterrows()]

        def _calc_symbol_sizes(sub: pd.DataFrame) -> Optional[List[int]]:
            if size is None:
                return None
            vals = pd.to_numeric(sub[size], errors="coerce").fillna(0)
            if vals.max() == vals.min():
                return [int((size_range[0] + size_range[1]) / 2)] * len(vals)
            normed = (vals - vals.min()) / (vals.max() - vals.min())
            return [int(size_range[0] + n * (size_range[1] - size_range[0])) for n in normed]

        groups = dff.groupby(color) if color else [("scatter", dff)]
        for name, grp in groups:
            name_str = str(name)
            data = _build_scatter_data(grp)
            entry: dict = {
                "type": "scatter", "name": name_str, "data": data,
                "symbol": symbol, "itemStyle": {"opacity": opacity},
            }
            sizes = _calc_symbol_sizes(grp)
            if sizes is not None:
                entry["symbolSize"] = int(np.mean(sizes)) if len(set(sizes)) == 1 else sizes
            else:
                entry["symbolSize"] = 8
            if labels:
                entry["label"] = {"show": True, "position": "top", "formatter": "{@[1]}"}
            if emphasis is not None:
                entry["emphasis"] = emphasis.to_dict()
            entry.update(series_kw)
            self._series.append(entry)
            self._series_meta.append(_SeriesMeta("scatter", name_str))
            if color and name_str not in self._legend_items:
                self._legend_items.append(name_str)

        return self

    # ─── PIE ──────────────────────────────────────────────────────────────

    def pie(
        self, df: pd.DataFrame, names: str, values: str, *,
        inner_radius: Optional[str] = None, outer_radius: str = "60%",
        center: Optional[List[str]] = None,
        radius: Optional[Union[str, List[str]]] = None,
        border_radius: int = 0, start_angle: int = 45,
        label_inside: bool = False, label_outside: bool = True,
        label_formatter: str = "{b}: {c} ({d}%)",
        label_font_size: Optional[int] = None,
        center_on_hover: bool = False,
        center_formatter: str = "{b}\n{c}",
        center_font_size: int = 18,
        rose_type: Optional[Literal["radius", "area"]] = None,
        emphasis: Optional[PieEmphasis] = None, **series_kw: Any,
    ) -> "Figure":
        """Add a pie (or donut) chart — equivalent to ``plt.pie()``.

        When called on a figure that already has cartesian series (bar, line,
        etc.), the pie is rendered as an **overlay** positioned via *center*
        and *radius*.  This lets you place a small pie on top of a bar chart
        without needing ``raw_series()``.

        Parameters
        ----------
        center : list[str], optional
            ``["x%", "y%"]`` position of the pie centre inside the chart
            area (e.g. ``["80%", "25%"]``).  When provided on a non-pie
            figure the pie becomes an overlay and skips the mode lock.
        radius : str | list[str], optional
            Shorthand for ``[inner_radius, outer_radius]``.  Accepts a
            single string (``"30%"``) or a two-element list
            (``["15%", "25%"]``).  Overrides *inner_radius* / *outer_radius*
            when provided.
        label_font_size : int, optional
            Override the label font size (handy for small overlay pies).
        """
        # ── Overlay mode: allow pie on top of cartesian charts ─────────
        _OVERLAY_COMPATIBLE = ("cartesian",)
        is_overlay = (
            center is not None
            and self._chart_mode is not None
            and self._chart_mode != "pie"
        )
        if is_overlay and self._chart_mode not in _OVERLAY_COMPATIBLE:
            raise BuilderConfigError(
                f"pie() overlay (center={center!r}) is only supported on cartesian "
                f"figures (bar/line/scatter), but the current mode is "
                f"'{self._chart_mode}'. Use a separate Figure for this pie chart."
            )
        if not is_overlay:
            self._ensure_mode("pie", "pie")

        df = _validate_df(df, "pie")
        _validate_columns(df, [names, values], "pie")

        dff = df.copy()
        dff[values] = _coerce_numeric(dff, values, "pie")
        dff = dff.dropna(subset=[names, values])

        data = [
            {"name": str(n), "value": round(float(v), 4)}
            for n, v in zip(dff[names], dff[values])
        ]

        # Resolve radius: explicit `radius` param > inner/outer pair > default
        if radius is not None:
            resolved_radius = radius
        elif inner_radius:
            resolved_radius = [inner_radius, outer_radius]
        else:
            resolved_radius = outer_radius

        if label_inside:
            lbl = {"show": True, "position": "inside", "formatter": label_formatter}
            lbl_line = {"show": False}
        elif label_outside:
            lbl = {"show": True, "position": "outside", "formatter": label_formatter}
            lbl_line = {"show": True, "length": 15, "length2": 10}
        else:
            lbl = {"show": False}
            lbl_line = {"show": False}

        if label_font_size is not None:
            lbl["fontSize"] = label_font_size

        emphasis_dict: dict = {
            "itemStyle": {
                "shadowBlur": 10, "shadowOffsetX": 0,
                "shadowColor": "rgba(0, 0, 0, 0.5)",
            }
        }
        if center_on_hover:
            emphasis_dict["label"] = {
                "show": True, "position": "center",
                "formatter": center_formatter,
                "fontSize": center_font_size, "fontWeight": "bold",
            }

        # Allow user-provided emphasis to override the default, but keep overlay focus
        if emphasis is not None:
            emphasis_dict = emphasis.to_dict()
            if is_overlay and "focus" not in emphasis_dict:
                emphasis_dict["focus"] = "self"
        elif is_overlay:
            # For overlays with default emphasis, also add "focus self" so hovering the pie doesn't
            # dim the underlying cartesian series.
            emphasis_dict["focus"] = "self"

        entry: dict = {
            "type": "pie", "radius": resolved_radius, "startAngle": start_angle,
            "data": data, "avoidLabelOverlap": True,
            "label": lbl, "labelLine": lbl_line, "emphasis": emphasis_dict,
        }
        if center is not None:
            entry["center"] = center
        if border_radius:
            entry.setdefault("itemStyle", {})["borderRadius"] = border_radius
            entry["itemStyle"].setdefault("borderColor", "#fff")
            entry["itemStyle"].setdefault("borderWidth", 2)
        if rose_type:
            entry["roseType"] = rose_type
        entry.update(series_kw)

        # ── Overlay color offset ──────────────────────────────────────────
        # When the pie's categories differ from the existing legend items,
        # offset slice colours so they don't collide with the bar/line palette.
        if is_overlay:
            pie_names_set = {str(n) for n in dff[names]}
            existing_names_set = set(self._legend_items)
            if not pie_names_set & existing_names_set:
                # Categories are disjoint → offset colours
                pal = list(self._palette or (
                    "#5470C6", "#91CC75", "#FAC858", "#EE6666",
                    "#73C0DE", "#3BA272", "#FC8452", "#9A60B4", "#EA7CCC",
                ))
                offset = len(existing_names_set)
                for i, item in enumerate(data):
                    item["itemStyle"] = item.get("itemStyle", {})
                    item["itemStyle"]["color"] = pal[(offset + i) % len(pal)]

        self._series.append(entry)
        self._series_meta.append(_SeriesMeta("pie", names))

        # For standalone pies, overwrite the legend; for overlays, extend it.
        pie_names = [str(n) for n in dff[names]]
        if is_overlay:
            self._legend_items.extend(pie_names)
        else:
            self._legend_items = pie_names

        return self

    # ─── HISTOGRAM ────────────────────────────────────────────────────────

    def hist(
        self, df: pd.DataFrame, column: str, *,
        bins: int = 10, density: bool = False,
        bar_color: Optional[str] = None,
        border_radius: int = 2, labels: bool = False,
        emphasis: Optional[Emphasis] = None, **series_kw: Any,
    ) -> "Figure":
        """Add a histogram — equivalent to ``plt.hist()``."""
        self._ensure_cartesian("hist")
        df = _validate_df(df, "hist")
        _validate_columns(df, [column], "hist")

        if bins is not None and bins <= 0:
            raise ValueError("bins must be a positive integer")

        vals = df[column].dropna().astype(float).values
        if len(vals) == 0:
            raise DataValidationError(f"hist(): Column '{column}' has no non-null numeric values.")

        counts, edges = np.histogram(vals, bins=bins, density=density)
        bin_labels = [f"{edges[i]:.1f}\u2013{edges[i + 1]:.1f}" for i in range(len(counts))]
        self._merge_x_categories(bin_labels)

        entry: dict = {
            "type": "bar",
            "data": [round(float(c), 6) for c in counts],
            "name": column,
            "label": {"show": labels, "position": "top"},
            "itemStyle": {"borderRadius": border_radius},
        }
        if bar_color:
            entry["itemStyle"]["color"] = bar_color
        if emphasis is not None:
            entry["emphasis"] = emphasis.to_dict()
        entry.update(series_kw)

        self._series.append(entry)
        self._series_meta.append(_SeriesMeta("bar", column))
        self._y_axes[0].setdefault("name", "Density" if density else "Count")
        self._x_axis["name"] = column

        # Histogram bin labels (e.g. "34.5–45.2") are inherently long;
        # pre-rotate to avoid OverlapWarning from the layout resolver.
        self._x_axis.setdefault("axisLabel", {}).setdefault("rotate", 30)
        self._user_set_rotate = True

        return self

    # ─── RADAR ────────────────────────────────────────────────────────────

    def radar(
        self, indicators: Sequence[dict],
        data: Sequence[Sequence[float]], *,
        series_names: Optional[Sequence[str]] = None,
        show_labels: bool = True, area_opacity: float = 0.15,
        radius: Union[int, str] = 150,
        center: Optional[List[str]] = None,
        emphasis: Optional[RadarEmphasis] = None, **series_kw: Any,
    ) -> "Figure":
        """Add a radar chart."""
        self._ensure_mode("radar", "radar")

        if not indicators:
            raise DataValidationError("radar(): indicators list must not be empty.")
        if not data:
            raise DataValidationError("radar(): data list must not be empty.")
        for i, row in enumerate(data):
            if len(row) != len(indicators):
                raise DataValidationError(
                    f"radar(): data[{i}] has {len(row)} values but there are "
                    f"{len(indicators)} indicators."
                )

        series_data = []
        for i, vals in enumerate(data):
            name = series_names[i] if series_names and i < len(series_names) else f"Series {i + 1}"
            series_data.append({"value": list(vals), "name": name, "label": {"show": show_labels}})
            self._legend_items.append(name)

        entry: dict = {
            "type": "radar", "data": series_data,
            "areaStyle": {"opacity": area_opacity},
        }
        if emphasis is not None:
            entry["emphasis"] = emphasis.to_dict()
        entry.update(series_kw)
        self._series.append(entry)
        self._series_meta.append(_SeriesMeta("radar", "radar"))

        self._extra["_radar_cfg"] = {
            "indicator": list(indicators),
            "radius": radius,
            "center": center or ["50%", "55%"],
        }
        return self

    # ─── KDE ──────────────────────────────────────────────────────────────

    def kde(
        self, df: pd.DataFrame, column: str, *,
        hue: Optional[str] = None, bandwidth: Optional[float] = None,
        grid_size: int = 200, show_median: bool = True,
        emphasis: Optional[LineEmphasis] = None, **series_kw: Any,
    ) -> "Figure":
        """Add a KDE (kernel density estimate) curve — like ``sns.kdeplot()``.

        Requires ``scipy``. Install with ``pip install echartsy[scipy]``.
        """
        from scipy.stats import gaussian_kde as _gaussian_kde

        self._ensure_cartesian("kde")
        df = _validate_df(df, "kde")
        _validate_columns(df, [column, hue], "kde")

        vals_all = df[column].dropna().astype(float).values
        if len(vals_all) < 2:
            raise DataValidationError(f"kde(): Column '{column}' needs at least 2 non-null values.")

        xmin, xmax = float(vals_all.min()), float(vals_all.max())
        xs = np.linspace(xmin, xmax, grid_size)

        self._x_axis["type"] = "value"
        self._x_axis.pop("data", None)
        self._x_axis.setdefault("name", column)

        groups = df.groupby(hue) if hue else [(column, df)]
        for lvl, sub in groups:
            arr = sub[column].dropna().astype(float).values
            if len(arr) < 2:
                continue
            kde_fn = _gaussian_kde(arr, bw_method=bandwidth)
            ys = kde_fn(xs)
            median = float(np.median(arr))
            name = f"{lvl} (Median: {median:.1f})" if show_median else str(lvl)

            entry: dict = {
                "type": "line", "name": name, "smooth": True,
                "data": list(zip(xs.tolist(), ys.tolist())),
                "showSymbol": False,
            }
            if emphasis is not None:
                entry["emphasis"] = emphasis.to_dict()
            entry.update(series_kw)
            self._series.append(entry)
            self._series_meta.append(_SeriesMeta("line", name))
            if name not in self._legend_items:
                self._legend_items.append(name)

        self._y_axes[0].setdefault("name", "Density")
        return self

    # ─── HEATMAP ──────────────────────────────────────────────────────────

    def heatmap(
        self, df: pd.DataFrame, x: str, y: str, value: str, *,
        label_show: bool = True, label_formatter: str = "{c}",
        visual_min: Optional[float] = None,
        visual_max: Optional[float] = None,
        in_range_colors: Optional[List[str]] = None,
        emphasis: Optional[Emphasis] = None, **series_kw: Any,
    ) -> "Figure":
        """Add a heatmap — similar to ``sns.heatmap()``."""
        self._ensure_mode("heatmap", "heatmap")
        df = _validate_df(df, "heatmap")
        _validate_columns(df, [x, y, value], "heatmap")

        dff = df.copy()
        dff[value] = _coerce_numeric(dff, value, "heatmap")
        n_before = len(dff)
        dff = dff.dropna(subset=[x, y, value])
        n_dropped = n_before - len(dff)
        if n_dropped > 0:
            warnings.warn(f"heatmap(): {n_dropped} rows dropped due to missing values", stacklevel=2)
        if dff.empty:
            warnings.warn("heatmap(): all rows dropped after removing missing values; chart will be empty", stacklevel=2)
            return self

        x_cats = list(dict.fromkeys(dff[x].astype(str).tolist()))
        y_cats = list(dict.fromkeys(dff[y].astype(str).tolist()))

        x_lookup = {cat: i for i, cat in enumerate(x_cats)}
        y_lookup = {cat: i for i, cat in enumerate(y_cats)}
        data = []
        for _, r in dff.iterrows():
            xk, yk = str(r[x]), str(r[y])
            if xk not in x_lookup or yk not in y_lookup:
                continue
            data.append([x_lookup[xk], y_lookup[yk], round(float(r[value]), 4)])

        self._x_axis = {"type": "category", "data": x_cats, "splitArea": {"show": True}}
        self._y_axes = [{"type": "category", "data": y_cats, "splitArea": {"show": True}}]

        vmin = visual_min if visual_min is not None else float(dff[value].min())
        vmax = visual_max if visual_max is not None else float(dff[value].max())
        colors = in_range_colors or [
            "#313695", "#4575b4", "#74add1", "#abd9e9",
            "#e0f3f8", "#ffffbf", "#fee090", "#fdae61",
            "#f46d43", "#d73027", "#a50026",
        ]

        self._extra["visualMap"] = {
            "min": vmin, "max": vmax, "calculable": True,
            "orient": "horizontal", "left": "center", "bottom": "5%",
            "inRange": {"color": colors},
        }

        emphasis_dict = {"itemStyle": {"shadowBlur": 10, "shadowColor": "rgba(0,0,0,0.5)"}}
        if emphasis is not None:
            emphasis_dict = emphasis.to_dict()

        entry: dict = {
            "type": "heatmap", "data": data,
            "label": {"show": label_show, "formatter": label_formatter},
            "emphasis": emphasis_dict,
        }
        entry.update(series_kw)
        self._series.append(entry)
        self._series_meta.append(_SeriesMeta("heatmap", value))
        self._tooltip_cfg["trigger"] = "item"
        return self

    # ─── SANKEY ───────────────────────────────────────────────────────────

    def sankey(
        self, df: pd.DataFrame, levels: Sequence[str], value: str, *,
        node_width: Union[int, str] = 20, node_gap: int = 8,
        layout: Literal["none", "orthogonal"] = "none",
        orient: Literal["horizontal", "vertical"] = "horizontal",
        emphasis: Optional[Union[SankeyEmphasis, dict]] = None, **series_kw: Any,
    ) -> "Figure":
        """Add an N-stage Sankey diagram."""
        self._ensure_mode("sankey", "sankey")
        df = _validate_df(df, "sankey")
        _validate_columns(df, list(levels) + [value], "sankey")

        if len(levels) < 2:
            raise BuilderConfigError("sankey() requires at least 2 levels.")

        links = []
        for src_col, tgt_col in zip(levels, levels[1:]):
            grouped = df.groupby([src_col, tgt_col], as_index=False)[value].sum()
            for _, row in grouped.iterrows():
                links.append({
                    "source": str(row[src_col]),
                    "target": str(row[tgt_col]),
                    "value": float(row[value]),
                })

        unique_nodes = pd.unique(df[list(levels)].values.ravel())
        nodes = [{"name": str(n)} for n in unique_nodes]

        entry: dict = {
            "type": "sankey", "layout": layout, "orient": orient,
            "data": nodes, "links": links,
            "nodeWidth": node_width, "nodeGap": node_gap,
        }
        if emphasis is not None:
            if isinstance(emphasis, dict):
                import warnings as _w
                _w.warn(
                    "Passing emphasis as a dict is deprecated. "
                    "Use SankeyEmphasis(...) instead.",
                    DeprecationWarning, stacklevel=2,
                )
                entry["emphasis"] = emphasis
            else:
                entry["emphasis"] = emphasis.to_dict()
        entry.update(series_kw)

        self._series.append(entry)
        self._series_meta.append(_SeriesMeta("sankey", "sankey"))
        self._tooltip_cfg = {"trigger": "item", "triggerOn": "mousemove", "confine": True}
        return self

    # ─── TREEMAP ──────────────────────────────────────────────────────────

    def treemap(
        self, df: pd.DataFrame, path: List[str],
        value: Optional[str] = None, *,
        leaf_depth: Optional[int] = 2, roam: bool = True,
        gap_width: int = 2, border_width: int = 1,
        label_formatter: str = "{b}\n{c}", emphasis: Optional[TreemapEmphasis] = None, **series_kw: Any,
    ) -> "Figure":
        """Add a treemap chart."""
        self._ensure_mode("treemap", "treemap")
        df = _validate_df(df, "treemap")
        _validate_columns(df, path + ([value] if value else []), "treemap")

        val_col = value
        work = df.copy()
        if val_col is None:
            work["__count__"] = 1
            val_col = "__count__"

        for lvl in path:
            work[lvl] = work[lvl].astype(object).where(pd.notna(work[lvl]), "<NA>")

        g = work.groupby(path, dropna=False)[val_col].sum().reset_index()

        root: dict = {}
        for _, row in g.iterrows():
            node = root
            for lvl in path:
                key = str(row[lvl])
                node = node.setdefault(key, {"__val": 0, "__ch": {}})
                node["__val"] += float(row[val_col])
                node = node["__ch"]

        def _build(subtree: dict) -> list:
            out = []
            for name, meta in subtree.items():
                item: dict = {"name": name, "value": round(meta["__val"], 2)}
                children = _build(meta["__ch"])
                if children:
                    item["children"] = children
                out.append(item)
            return out

        data = _build(root)

        default_levels = [
            {"itemStyle": {"borderColor": "#fff", "borderWidth": border_width, "gapWidth": gap_width}},
            {"itemStyle": {"borderColor": "#eee", "borderWidth": border_width, "gapWidth": gap_width}},
            {"itemStyle": {"borderColor": "#ddd", "borderWidth": border_width, "gapWidth": gap_width}},
        ]

        entry: dict = {
            "type": "treemap", "data": data,
            "leafDepth": leaf_depth, "roam": roam,
            "label": {"show": True, "formatter": label_formatter},
            "breadcrumb": {"show": True}, "levels": default_levels,
        }
        if emphasis is not None:
            entry["emphasis"] = emphasis.to_dict()
        entry.update(series_kw)
        self._series.append(entry)
        self._series_meta.append(_SeriesMeta("treemap", "treemap"))
        self._tooltip_cfg = {"trigger": "item", "confine": True}
        return self

    # ─── FUNNEL ───────────────────────────────────────────────────────────

    def funnel(
        self, df: pd.DataFrame, names: str, values: str, *,
        sort_order: Literal["descending", "ascending", "none"] = "descending",
        gap: int = 2, label_position: str = "inside",
        label_formatter: str = "{b}: {c}", emphasis: Optional[FunnelEmphasis] = None, **series_kw: Any,
    ) -> "Figure":
        """Add a funnel chart."""
        self._ensure_mode("funnel", "funnel")
        df = _validate_df(df, "funnel")
        _validate_columns(df, [names, values], "funnel")

        dff = df.copy()
        dff[values] = _coerce_numeric(dff, values, "funnel")
        dff = dff.dropna(subset=[names, values])

        data = [
            {"name": str(n), "value": round(float(v), 4)}
            for n, v in zip(dff[names], dff[values])
        ]

        entry: dict = {
            "type": "funnel", "data": data, "sort": sort_order,
            "gap": gap,
            "label": {"show": True, "position": label_position, "formatter": label_formatter},
        }
        if emphasis is not None:
            entry["emphasis"] = emphasis.to_dict()
        entry.update(series_kw)
        self._series.append(entry)
        self._series_meta.append(_SeriesMeta("funnel", names))
        self._legend_items = [str(n) for n in dff[names]]
        self._tooltip_cfg = {"trigger": "item", "confine": True}
        return self

    # ─── BOXPLOT ──────────────────────────────────────────────────────────

    def boxplot(
        self, df: pd.DataFrame, x: str, y: str, *,
        orient: Literal["v", "h"] = "v", emphasis: Optional[Emphasis] = None, **series_kw: Any,
    ) -> "Figure":
        """Add a box-and-whisker plot — equivalent to ``plt.boxplot()``."""
        self._ensure_cartesian("boxplot")
        df = _validate_df(df, "boxplot")
        _validate_columns(df, [x, y], "boxplot")

        dff = df.copy()
        dff[y] = _coerce_numeric(dff, y, "boxplot")
        dff = dff.dropna(subset=[x, y])

        categories = list(dict.fromkeys(dff[x].astype(str).tolist()))
        self._merge_x_categories(categories)

        box_data = []
        for cat in categories:
            vals = dff.loc[dff[x].astype(str) == cat, y].dropna().values
            if len(vals) == 0:
                box_data.append([0, 0, 0, 0, 0])
            else:
                q1, med, q3 = np.percentile(vals, [25, 50, 75])
                box_data.append([
                    round(float(vals.min()), 4), round(float(q1), 4),
                    round(float(med), 4), round(float(q3), 4),
                    round(float(vals.max()), 4),
                ])

        entry: dict = {"type": "boxplot", "data": box_data, "name": y}
        if emphasis is not None:
            entry["emphasis"] = emphasis.to_dict()
        entry.update(series_kw)
        self._series.append(entry)
        self._series_meta.append(_SeriesMeta("boxplot", y))
        self._tooltip_cfg["trigger"] = "item"
        return self

    # ═══════════════════════════════════════════════════════════════════════
    # Build + render
    # ═══════════════════════════════════════════════════════════════════════

    def to_option(self) -> dict:
        """Assemble and return the raw ECharts option dict without rendering.

        Useful for debugging, testing, or feeding into a custom renderer.
        """
        if not self._series:
            raise BuilderConfigError("Cannot build option — no series have been added.")

        mode = self._chart_mode or "cartesian"

        # ── Non-cartesian modes ───────────────────────────────────────────
        if mode == "pie":
            option: dict = {}
            if self._title_cfg:
                option["title"] = copy.deepcopy(self._title_cfg)
            option["tooltip"] = {"trigger": "item", "formatter": "{b}: {c} ({d}%)", "confine": True}
            legend_cfg = copy.deepcopy(self._legend_cfg) or {"orient": self._style.legend_orient, "left": "left"}
            legend_cfg["data"] = list(self._legend_items)
            option["legend"] = legend_cfg
            if self._palette:
                option["color"] = list(self._palette)
            option["series"] = copy.deepcopy(self._series)
            if self._toolbox_cfg:
                option["toolbox"] = copy.deepcopy(self._toolbox_cfg)
            option.update({k: copy.deepcopy(v) for k, v in self._extra.items() if not k.startswith("_")})
            return option

        if mode == "radar":
            option = {}
            if self._title_cfg:
                option["title"] = copy.deepcopy(self._title_cfg)
            option["tooltip"] = {"trigger": "item", "confine": True, "appendTo": "body"}
            legend_cfg = copy.deepcopy(self._legend_cfg) or {"left": "center", "show": True, "padding": 40}
            legend_cfg["data"] = list(self._legend_items)
            option["legend"] = legend_cfg
            radar_cfg = copy.deepcopy(self._extra.get("_radar_cfg", {"indicator": [], "radius": 150, "center": ["50%", "55%"]}))
            option["radar"] = radar_cfg
            if self._palette:
                option["color"] = list(self._palette)
            option["series"] = copy.deepcopy(self._series)
            if self._toolbox_cfg:
                option["toolbox"] = copy.deepcopy(self._toolbox_cfg)
            option.update({k: copy.deepcopy(v) for k, v in self._extra.items() if not k.startswith("_")})
            return option

        if mode in ("sankey", "treemap", "funnel", "heatmap"):
            option = {}
            if self._title_cfg:
                option["title"] = copy.deepcopy(self._title_cfg)
            option["tooltip"] = copy.deepcopy(self._tooltip_cfg)
            if self._palette:
                option["color"] = list(self._palette)
            if mode == "heatmap":
                option["xAxis"] = copy.deepcopy(self._x_axis)
                option["yAxis"] = copy.deepcopy(self._y_axes[0] if len(self._y_axes) == 1 else self._y_axes)
                option["grid"] = copy.deepcopy(self._grid_cfg)
            if self._legend_items and mode == "funnel":
                legend_cfg = copy.deepcopy(self._legend_cfg) or {"orient": "vertical", "left": "left"}
                legend_cfg["data"] = list(self._legend_items)
                option["legend"] = legend_cfg
            option["series"] = copy.deepcopy(self._series)
            if self._toolbox_cfg:
                option["toolbox"] = copy.deepcopy(self._toolbox_cfg)
            if "visualMap" in self._extra:
                option["visualMap"] = copy.deepcopy(self._extra["visualMap"])
            option.update({k: copy.deepcopy(v) for k, v in self._extra.items() if not k.startswith("_")})
            return option

        # ── Cartesian mode ────────────────────────────────────────────────
        is_h_bar = self._extra.get("_bar_orient_h", False)

        x_axis_cfg = copy.deepcopy(self._x_axis)
        y_axis_cfg = copy.deepcopy(self._y_axes)

        if not is_h_bar:
            x_axis_cfg["data"] = self._x_categories

        if is_h_bar:
            x_axis_cfg = {"type": "value"}
            y_axis_cfg = [{"type": "category", "data": self._x_categories}]

        option = {}
        if self._title_cfg:
            option["title"] = copy.deepcopy(self._title_cfg)
        if self._palette:
            option["color"] = list(self._palette)
        option["tooltip"] = copy.deepcopy(self._tooltip_cfg)

        if self._legend_items:
            legend_cfg = copy.deepcopy(self._legend_cfg) or {}
            legend_cfg["data"] = list(dict.fromkeys(self._legend_items))
            option["legend"] = legend_cfg

        option["grid"] = copy.deepcopy(self._grid_cfg)
        option["xAxis"] = x_axis_cfg
        option["yAxis"] = y_axis_cfg if len(y_axis_cfg) > 1 else y_axis_cfg[0]
        option["series"] = copy.deepcopy(self._series)

        if self._toolbox_cfg:
            option["toolbox"] = copy.deepcopy(self._toolbox_cfg)
        if self._datazoom_cfg:
            option["dataZoom"] = self._datazoom_cfg

        if self._style.bg:
            option.setdefault("backgroundColor", self._style.bg)
        option.update({k: v for k, v in self._extra.items() if not k.startswith("_")})

        # Pass internal metadata for the layout resolver (stripped before output)
        option["_meta"] = {"user_set_rotate": self._user_set_rotate}

        # Anti-overlap pass
        option = _resolve_layout(option, self._series_meta)

        return option

    def show(self, **render_kw: Any) -> None:
        """Render the chart using the currently configured engine.

        Calls :meth:`to_option` to assemble the full config, runs the
        anti-overlap engine, and dispatches to the active renderer.

        Returns ``None`` so that Jupyter does not auto-display the option
        dict below the chart.  Use :meth:`to_option` if you need the raw
        dict.
        """
        option = self.to_option()

        render(
            option,
            height=self._height,
            width=self._width,
            theme=self._theme,
            renderer=self._renderer,
            key=self._key or self._auto_key(),
            **render_kw,
        )

    def to_html(self, filepath: str = "chart.html") -> str:
        """Export the chart to a standalone HTML file.

        Parameters
        ----------
        filepath : str
            Output file path.

        Returns
        -------
        str
            The filepath written to.
        """
        import os
        from echartsy._config import get_adaptive
        from echartsy.renderers._html_template import build_html

        # Validate parent directory exists
        parent = os.path.dirname(os.path.abspath(filepath))
        if not os.path.isdir(parent):
            raise FileNotFoundError(
                f"to_html(): directory '{parent}' does not exist. "
                "Please create it first or use a different path."
            )

        option = self.to_option()
        html = build_html(
            option, height=self._height,
            width=self._width or "100%",
            theme=self._theme, renderer=self._renderer,
            adaptive=get_adaptive(),
        )
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html)
        except OSError as e:
            raise OSError(f"Cannot write to '{filepath}': {e}") from e
        abs_path = os.path.abspath(filepath)
        print(f"Chart saved to {abs_path}")
        return filepath


# ═══════════════════════════════════════════════════════════════════════════
# Convenience alias — feels like matplotlib
# ═══════════════════════════════════════════════════════════════════════════

def figure(
    height: str = "400px",
    width: Optional[str] = None,
    renderer: Literal["canvas", "svg"] = "canvas",
    style: Optional[StylePreset] = None,
    **kwargs: Any,
) -> Figure:
    """Module-level factory — equivalent to ``plt.figure()``.

    Example
    -------
    >>> import echartsy as ec
    >>> fig = ec.figure(height="600px", style=ec.StylePreset.KPI_REPORT)
    >>> fig.bar(df, "x", "y").show()
    """
    return Figure(height=height, width=width, renderer=renderer, style=style, **kwargs)
