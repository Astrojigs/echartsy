"""Internal helper functions — data validation, aggregation, time parsing, layout."""
from __future__ import annotations

import copy
import difflib
import re
import warnings
from typing import Any, Dict, List, Literal, Optional, Sequence

import numpy as np
import pandas as pd

from echartsy.exceptions import (
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
    first_seen = list(dict.fromkeys(series.astype(str).str.strip().tolist()))
    parsed = {cat: _parse_time_value(cat) for cat in first_seen}
    if all(v is not None for v in parsed.values()) and len(first_seen) > 1:
        return sorted(first_seen, key=lambda c: parsed[c])
    return first_seen


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
        parts = [f"{caller}(): Column(s) {missing} not found in DataFrame."]
        parts.append(f"  Available columns: {avail}")
        for m in missing:
            suggestions = difflib.get_close_matches(m, [str(c) for c in avail], n=1, cutoff=0.6)
            if suggestions:
                parts.append(f"  Did you mean {suggestions[0]!r}? (for {m!r})")
        raise DataValidationError("\n".join(parts))


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

# --- Pixel estimation constants ---
_PX_PER_CHAR = 7           # Approx pixel width per character (normal text)
_PX_PER_ROTATED_CHAR = 5   # Approx pixel width per character (rotated text)
_DEFAULT_CHART_WIDTH = 800  # Assumed container width in pixels

# --- Label density thresholds ---
# Instead of rigid category-count cutoffs, we use a fill-ratio approach:
#   fill_ratio = (n_cats * avg_label_px) / available_width
# These thresholds define when rotation kicks in.
_FILL_RATIO_ROTATE_30 = 0.85   # Labels fill ≥85% of width → rotate 30°
_FILL_RATIO_ROTATE_45 = 1.4    # Labels fill ≥140% of width → rotate 45°
_FILL_RATIO_ROTATE_90 = 2.5    # Labels fill ≥250% of width → rotate 90°

# --- Hard limits (safety net for extreme cases) ---
_HARD_COUNT_ROTATE_45 = 30     # Always rotate ≥45° at 30+ categories
_HARD_COUNT_ROTATE_90 = 60     # Always rotate 90° at 60+ categories

# --- Series-type multipliers ---
# Some chart types space labels by cell/point width, so they tolerate more
# labels before overlapping.  A multiplier > 1 means "more forgiving".
_SERIES_TYPE_TOLERANCE: Dict[str, float] = {
    "heatmap": 1.6,     # Labels spaced by cell width
    "scatter": 1.4,     # Labels spaced by point distribution
    "bar":     1.0,     # Default
    "line":    1.0,     # Default
}

# --- Legend ---
_LEGEND_SCROLL_THRESHOLD = 8

# Sentinel value indicating the user has NOT explicitly set rotation.
_ROTATE_NOT_SET = "__rotate_not_set__"


def _estimate_available_width(option: dict) -> float:
    """Estimate the pixel width available for x-axis labels.

    Uses the chart's configured width if it's a pixel value, otherwise
    falls back to ``_DEFAULT_CHART_WIDTH``.  Subtracts left/right grid
    margins to get the actual plotting area width.
    """
    # Try to parse chart width from the option (only if it's a px value)
    chart_width = _DEFAULT_CHART_WIDTH
    # ECharts doesn't store width in the option dict normally — it's set
    # on the container.  But we can check grid margins to narrow the estimate.
    grid = option.get("grid", {})
    left = grid.get("left", 60)
    right = grid.get("right", 60)
    left_px = int(left) if isinstance(left, (int, float)) else 60
    right_px = int(right) if isinstance(right, (int, float)) else 60
    return max(chart_width - left_px - right_px, 200)


def _dominant_series_type(series_meta: List[Any]) -> str:
    """Return the most common series type, used for tolerance lookup."""
    if not series_meta:
        return "bar"
    from collections import Counter
    counts = Counter(getattr(m, "chart_type", "bar") for m in series_meta)
    return counts.most_common(1)[0][0]


def _resolve_layout(option: dict, series_meta: List[Any]) -> dict:
    """Run the anti-overlap engine over a fully assembled ECharts option dict.

    Mutates a deep copy and returns it. Auto-adjusts:

    1. Label rotation for crowded x-axes (width-aware, series-aware)
    2. Grid margins for rotated labels
    3. Scroll-mode legends for many items
    4. Tooltip confinement
    5. Dual-axis right margin

    The resolver **respects explicit user intent**: if the user has called
    ``xlabel(rotate=...)`` or ``xticks(rotate=...)``, the resolver will
    not override that rotation or emit a warning.  This is signalled by
    the presence of ``_user_set_rotate`` in the option's ``_meta`` dict.

    Warnings can be globally silenced via
    ``ec.config(overlap_warnings=False)`` while keeping the auto-fixes.
    """
    from echartsy._config import get_overlap_warnings

    opt = copy.deepcopy(option)

    # Pop internal metadata (not part of the ECharts spec)
    meta = opt.pop("_meta", {})
    user_set_rotate = meta.get("user_set_rotate", False)

    # 1) Tooltip safety
    tooltip = opt.setdefault("tooltip", {})
    tooltip["confine"] = True
    tooltip.setdefault("appendTo", "body")

    # 2) X-axis label rotation (smart heuristics)
    x_axis = opt.get("xAxis")
    if isinstance(x_axis, dict) and x_axis.get("type") == "category":
        cats = x_axis.get("data", [])
        n_cats = len(cats)
        max_label_len = max((len(str(c)) for c in cats), default=0)
        avg_label_len = (
            sum(len(str(c)) for c in cats) / n_cats if n_cats > 0 else 0
        )
        label_cfg = x_axis.setdefault("axisLabel", {})
        current_rotate = label_cfg.get("rotate", 0)

        # Only auto-rotate if user hasn't explicitly set rotation
        if current_rotate == 0 and not user_set_rotate:
            # Estimate how much space labels need vs how much is available
            available_px = _estimate_available_width(opt)
            # Use average label length (not max) for the fill ratio — this
            # avoids one long outlier label triggering rotation for all.
            label_px_each = avg_label_len * _PX_PER_CHAR
            # Add inter-label gap (~12px between labels)
            total_label_px = n_cats * (label_px_each + 12) - 12

            # Series-type tolerance: heatmaps/scatter are more forgiving
            dominant_type = _dominant_series_type(series_meta)
            tolerance = _SERIES_TYPE_TOLERANCE.get(dominant_type, 1.0)

            fill_ratio = total_label_px / (available_px * tolerance)

            # Determine rotation angle
            if n_cats >= _HARD_COUNT_ROTATE_90:
                auto_rotate = 90
            elif n_cats >= _HARD_COUNT_ROTATE_45:
                auto_rotate = 45
            elif fill_ratio >= _FILL_RATIO_ROTATE_90:
                auto_rotate = 90
            elif fill_ratio >= _FILL_RATIO_ROTATE_45:
                auto_rotate = 45
            elif fill_ratio >= _FILL_RATIO_ROTATE_30:
                auto_rotate = 30
            else:
                auto_rotate = 0

            # Extra check: even if fill ratio is low, very long individual
            # labels (>25 chars) at moderate counts can still overlap
            if auto_rotate == 0 and max_label_len > 25 and n_cats >= 6:
                auto_rotate = 30

            if auto_rotate > 0:
                label_cfg["rotate"] = auto_rotate
                if get_overlap_warnings():
                    warnings.warn(
                        f"{n_cats} x-axis categories (avg length "
                        f"{avg_label_len:.0f}, fill ratio {fill_ratio:.1f}×) "
                        f"— auto-rotating labels to {auto_rotate}°. "
                        f"Suppress with ec.config(overlap_warnings=False) or "
                        f"set explicitly with fig.xlabel(rotate=0).",
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
