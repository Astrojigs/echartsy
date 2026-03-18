"""Shared chart-method logic — extracted from Figure and TimelineFigure.

This mixin contains the core series-building logic for common chart types
(bar, plot, scatter, pie, hist). Each method validates input, coerces
data, and returns series dicts + metadata without knowing how the caller
stores them.

This DRY approach means bug fixes and new parameters propagate to both
Figure and TimelineFigure automatically.
"""
from __future__ import annotations

import warnings
from typing import Any, Dict, List, Literal, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd

from echartsy._helpers import (
    _coerce_numeric,
    _resolve_agg,
    _sort_categories,
    _validate_columns,
    _validate_df,
)
from echartsy.emphasis import Emphasis, LineEmphasis, ScatterEmphasis


def build_line_series(
    df: pd.DataFrame, x: str, y: str, *,
    hue: Optional[str] = None, smooth: bool = False,
    area: bool = False, area_opacity: float = 0.15,
    connect_nulls: bool = False, line_width: int = 2,
    symbol_size: int = 6, symbol: str = "circle",
    labels: bool = False, label_position: str = "top",
    label_prefix: str = "", label_suffix: str = "",
    agg: str = "mean", axis: int = 0,
    emphasis: Optional[LineEmphasis] = None,
    categories: Optional[List[str]] = None,
    align_fn=None,
    **series_kw: Any,
) -> Tuple[List[dict], List[str], List[str]]:
    """Build line series dicts from a DataFrame.

    Returns
    -------
    (series_list, legend_names, categories)
    """
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
        warnings.warn(f"plot(): {n_dropped} rows dropped due to missing values", stacklevel=3)
    if dff.empty:
        warnings.warn("plot(): all rows dropped; chart will be empty", stacklevel=3)
        return [], [], categories or []

    cats = _sort_categories(dff[x])
    all_cats = list(categories or [])
    existing = set(all_cats)
    for c in cats:
        if c not in existing:
            all_cats.append(c)
            existing.add(c)

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

    series_list: List[dict] = []
    legend_names: List[str] = []
    groups = dff.groupby(hue) if hue else [(y, dff)]
    for name, grp in groups:
        name_str = str(name)
        agg_fn = _resolve_agg(agg)
        grouped = grp.groupby(x)[y].agg(agg_fn)
        values = [
            None if cat not in grouped.index or pd.isna(grouped.get(cat))
            else round(float(grouped.get(cat)), 4)
            for cat in all_cats
        ]
        entry = {**base, "name": name_str, "data": values}
        series_list.append(entry)
        legend_names.append(name_str)

    return series_list, legend_names, all_cats


def build_bar_series(
    df: pd.DataFrame, x: str, y: str, *,
    hue: Optional[str] = None, stack: bool = False,
    orient: Literal["v", "h"] = "v",
    bar_width: Optional[Union[int, str]] = None,
    bar_gap: Optional[str] = None,
    border_radius: int = 4, labels: bool = False,
    label_formatter: str = "{c}", label_font_size: int = 12,
    label_color: str = "#333",
    gradient: bool = False,
    gradient_colors: Tuple[str, str] = ("#83bff6", "#188df0"),
    agg: str = "sum", axis: int = 0,
    emphasis: Optional[Emphasis] = None,
    categories: Optional[List[str]] = None,
    **series_kw: Any,
) -> Tuple[List[dict], List[str], List[str], bool]:
    """Build bar series dicts from a DataFrame.

    Returns
    -------
    (series_list, legend_names, categories, is_horizontal)
    """
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
        warnings.warn(f"bar(): {n_dropped} rows dropped due to missing values", stacklevel=3)
    if dff.empty:
        warnings.warn("bar(): all rows dropped; chart will be empty", stacklevel=3)
        return [], [], categories or [], orient == "h"

    cats = _sort_categories(dff[x])
    all_cats = list(categories or [])
    existing = set(all_cats)
    for c in cats:
        if c not in existing:
            all_cats.append(c)
            existing.add(c)

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
        base["barWidth"] = bar_width
    if bar_gap is not None:
        base["barGap"] = bar_gap
    if emphasis is not None:
        base["emphasis"] = emphasis.to_dict()
    base.update(series_kw)

    series_list: List[dict] = []
    legend_names: List[str] = []
    groups = dff.groupby(hue) if hue else [(y, dff)]
    for name, grp in groups:
        name_str = str(name)
        agg_fn = _resolve_agg(agg)
        grouped = grp.groupby(x)[y].agg(agg_fn)
        values = [
            None if cat not in grouped.index or pd.isna(grouped.get(cat))
            else round(float(grouped.get(cat)), 4)
            for cat in all_cats
        ]
        entry = {**base, "name": name_str, "data": values}
        series_list.append(entry)
        legend_names.append(name_str)

    return series_list, legend_names, all_cats, orient == "h"
