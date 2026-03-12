"""Internal helper functions — data validation, aggregation, time parsing, layout."""
from __future__ import annotations

import copy
import re
import warnings
from typing import Any, Dict, List, Literal, Optional, Sequence

import numpy as np
import pandas as pd

from echartslib.exceptions import (
    BuilderConfigError,
    DataValidationError,
    OverlapWarning,
)

# ═══════════════════════════════════════════════════════════════════════════
# Time-parsing helpers
# ═══════════════════════════════════════════════════════════════════════════

_QUARTER_RE = re.compile(r"^Q([1-4])\s+(\d{4})$")
_YEAR_RE = re.compile(r"^\d{4}$")


def _parse_time_value(v: str) -> Optional[pd.Timestamp]:
    """Attempt to parse common time-like strings into a ``pd.Timestamp``.

    Recognised formats: "January 2024", "Q1 2024", "2024".
    Returns ``None`` when no format matches.
    """
    v = str(v).strip()
    try:
        return pd.to_datetime(v, format="%B %Y")
    except (ValueError, TypeError):
        pass
    m = _QUARTER_RE.match(v)
    if m:
        q, y = int(m.group(1)), int(m.group(2))
        return pd.Timestamp(y, (q - 1) * 3 + 1, 1)
    if _YEAR_RE.match(v):
        return pd.Timestamp(int(v), 1, 1)
    return None


def _sort_categories(series: pd.Series) -> List[str]:
    """Sort a string category column chronologically if possible, else first-seen."""
    uniq = series.astype(str).str.strip()
    parsed = uniq.apply(_parse_time_value)
    if parsed.notna().mean() > 0.6:
        df_tmp = pd.DataFrame({"label": uniq, "_dt": parsed}).dropna(subset=["_dt"])
        return df_tmp.sort_values("_dt")["label"].drop_duplicates().tolist()
    return list(dict.fromkeys(uniq.tolist()))


# ═══════════════════════════════════════════════════════════════════════════
# Data validation helpers
# ═══════════════════════════════════════════════════════════════════════════

def _validate_df(df: Any, caller: str) -> pd.DataFrame:
    """Ensure *df* is a non-empty DataFrame."""
    if df is None:
        raise DataValidationError(f"{caller}() received None instead of a DataFrame.")
    if not isinstance(df, pd.DataFrame):
        raise DataValidationError(
            f"{caller}() expected a pandas DataFrame, got {type(df).__name__}."
        )
    if df.empty:
        raise DataValidationError(f"{caller}() received an empty DataFrame — nothing to plot.")
    return df


def _validate_columns(
    df: pd.DataFrame,
    columns: Sequence[Optional[str]],
    caller: str,
) -> None:
    """Assert that every non-None column name exists in *df*."""
    cols = [c for c in columns if c is not None]
    missing = [c for c in cols if c not in df.columns]
    if missing:
        avail = list(df.columns)
        raise DataValidationError(
            f"{caller}(): Column(s) {missing} not found in DataFrame.\n"
            f"  Available columns: {avail}"
        )


def _coerce_numeric(df: pd.DataFrame, col: str, caller: str) -> pd.Series:
    """Coerce *col* to numeric, raising if every value becomes NaN."""
    s = pd.to_numeric(df[col], errors="coerce")
    if s.isna().all():
        raise DataValidationError(
            f"{caller}(): Column '{col}' contains no numeric values after coercion."
        )
    return s


# ═══════════════════════════════════════════════════════════════════════════
# Aggregation helper
# ═══════════════════════════════════════════════════════════════════════════

AggStr = Literal["sum", "mean", "median", "max", "min", "count"]

_AGG_MAP: Dict[str, str] = {
    "sum": "sum", "mean": "mean", "avg": "mean",
    "median": "median", "max": "max", "min": "min", "count": "count",
}


def _resolve_agg(agg: str) -> str:
    """Map a user-friendly aggregation name to a pandas-compatible one."""
    key = agg.lower().strip()
    if key not in _AGG_MAP:
        raise BuilderConfigError(
            f"Unknown aggregation '{agg}'. Choose from: {', '.join(_AGG_MAP)}"
        )
    return _AGG_MAP[key]


# ═══════════════════════════════════════════════════════════════════════════
# Layout resolver (anti-overlap engine)
# ═══════════════════════════════════════════════════════════════════════════

_CATEGORY_COUNT_ROTATE_30 = 10
_CATEGORY_COUNT_ROTATE_45 = 20
_CATEGORY_COUNT_ROTATE_90 = 40
_LABEL_LENGTH_ROTATE = 12
_LEGEND_SCROLL_THRESHOLD = 8
_PX_PER_CHAR = 7
_PX_PER_ROTATED_CHAR = 5


def _resolve_layout(option: dict, series_meta: List[dict]) -> dict:
    """Run the anti-overlap engine over a fully assembled ECharts option dict.

    Mutates a deep copy and returns it. Auto-adjusts:
    1. Label rotation for crowded x-axes
    2. Grid margins for rotated labels
    3. Scroll-mode legends for many items
    4. Tooltip confinement
    5. Dual-axis right margin
    """
    opt = copy.deepcopy(option)

    # 1) Tooltip safety
    tooltip = opt.setdefault("tooltip", {})
    tooltip["confine"] = True
    tooltip.setdefault("appendTo", "body")

    # 2) X-axis label rotation
    x_axis = opt.get("xAxis")
    if isinstance(x_axis, dict) and x_axis.get("type") == "category":
        cats = x_axis.get("data", [])
        n_cats = len(cats)
        max_label_len = max((len(str(c)) for c in cats), default=0)
        label_cfg = x_axis.setdefault("axisLabel", {})
        current_rotate = label_cfg.get("rotate", 0)

        if current_rotate == 0:
            if n_cats >= _CATEGORY_COUNT_ROTATE_90:
                auto_rotate = 90
            elif n_cats >= _CATEGORY_COUNT_ROTATE_45 or max_label_len > 20:
                auto_rotate = 45
            elif n_cats >= _CATEGORY_COUNT_ROTATE_30 or max_label_len > _LABEL_LENGTH_ROTATE:
                auto_rotate = 30
            else:
                auto_rotate = 0

            if auto_rotate > 0:
                label_cfg["rotate"] = auto_rotate
                warnings.warn(
                    f"{n_cats} x-axis categories detected (max label length "
                    f"{max_label_len}) — auto-rotating labels to {auto_rotate}°.",
                    OverlapWarning,
                    stacklevel=4,
                )

        # 3) Grid margin expansion
        grid = opt.setdefault("grid", {})
        grid.setdefault("containLabel", True)
        effective_rotate = label_cfg.get("rotate", 0)
        if effective_rotate > 0:
            estimated_px = max_label_len * _PX_PER_ROTATED_CHAR
            current_bottom = grid.get("bottom", 50)
            needed = max(
                int(current_bottom) if isinstance(current_bottom, (int, float)) else 60,
                estimated_px + 20,
            )
            grid["bottom"] = needed

    # 4) Legend scroll
    legend = opt.get("legend")
    if isinstance(legend, dict):
        legend_data = legend.get("data", [])
        if len(legend_data) > _LEGEND_SCROLL_THRESHOLD:
            legend["type"] = "scroll"
            legend.setdefault("pageButtonItemGap", 5)
            legend.setdefault("pageButtonGap", 10)
            grid = opt.setdefault("grid", {})
            current_top = grid.get("top", 60)
            if isinstance(current_top, (int, float)) and current_top < 80:
                grid["top"] = 80

    # 5) Dual-axis right margin
    y_axis = opt.get("yAxis")
    if isinstance(y_axis, list) and len(y_axis) >= 2:
        right_name = y_axis[1].get("name", "")
        grid = opt.setdefault("grid", {})
        needed_right = max(70, len(right_name) * _PX_PER_CHAR + 30)
        current_right = grid.get("right", 70)
        if isinstance(current_right, (int, float)):
            grid["right"] = max(int(current_right), needed_right)

    return opt
