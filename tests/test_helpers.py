"""Tests for internal helper functions in echartsy._helpers."""
from __future__ import annotations

import warnings

import pandas as pd
import pytest

from echartsy._helpers import (
    _coerce_numeric,
    _resolve_agg,
    _resolve_layout,
    _sort_categories,
    _validate_columns,
    _validate_df,
)
from echartsy.exceptions import (
    BuilderConfigError,
    DataValidationError,
    OverlapWarning,
)


# ═══════════════════════════════════════════════════════════════════════════
# _validate_df tests
# ═══════════════════════════════════════════════════════════════════════════

class TestValidateDf:
    def test_validate_df_none(self):
        with pytest.raises(DataValidationError, match="None"):
            _validate_df(None, "test")

    def test_validate_df_not_dataframe(self):
        with pytest.raises(DataValidationError, match="expected a pandas DataFrame"):
            _validate_df([1, 2, 3], "test")

    def test_validate_df_empty(self):
        with pytest.raises(DataValidationError, match="empty"):
            _validate_df(pd.DataFrame(), "test")

    def test_validate_df_valid(self):
        df = pd.DataFrame({"a": [1]})
        result = _validate_df(df, "test")
        assert result is df


# ═══════════════════════════════════════════════════════════════════════════
# _validate_columns tests
# ═══════════════════════════════════════════════════════════════════════════

class TestValidateColumns:
    def test_validate_columns_missing(self):
        df = pd.DataFrame({"a": [1], "b": [2]})
        with pytest.raises(DataValidationError, match="not found"):
            _validate_columns(df, ["a", "missing_col"], "test")

    def test_validate_columns_did_you_mean(self):
        df = pd.DataFrame({"Revenue": [1], "Region": [2]})
        with pytest.raises(DataValidationError, match="Did you mean"):
            _validate_columns(df, ["Revnue"], "test")

    def test_validate_columns_valid(self):
        df = pd.DataFrame({"a": [1], "b": [2]})
        # Should not raise
        _validate_columns(df, ["a", "b"], "test")

    def test_validate_columns_skips_none(self):
        df = pd.DataFrame({"a": [1]})
        # None columns are skipped
        _validate_columns(df, ["a", None], "test")


# ═══════════════════════════════════════════════════════════════════════════
# _coerce_numeric tests
# ═══════════════════════════════════════════════════════════════════════════

class TestCoerceNumeric:
    def test_coerce_numeric_valid(self):
        df = pd.DataFrame({"x": ["1", "2.5", "3"]})
        result = _coerce_numeric(df, "x", "test")
        assert result.dtype.kind == "f"
        assert list(result) == [1.0, 2.5, 3.0]

    def test_coerce_numeric_all_nan(self):
        df = pd.DataFrame({"x": ["abc", "def", "ghi"]})
        with pytest.raises(DataValidationError, match="no numeric values"):
            _coerce_numeric(df, "x", "test")


# ═══════════════════════════════════════════════════════════════════════════
# _resolve_agg tests
# ═══════════════════════════════════════════════════════════════════════════

class TestResolveAgg:
    @pytest.mark.parametrize("agg_name,expected", [
        ("sum", "sum"),
        ("mean", "mean"),
        ("avg", "mean"),
        ("median", "median"),
        ("max", "max"),
        ("min", "min"),
        ("count", "count"),
    ])
    def test_resolve_agg_valid(self, agg_name, expected):
        assert _resolve_agg(agg_name) == expected

    def test_resolve_agg_case_insensitive(self):
        assert _resolve_agg("SUM") == "sum"
        assert _resolve_agg("  Mean  ") == "mean"

    def test_resolve_agg_invalid(self):
        with pytest.raises(BuilderConfigError, match="Unknown aggregation"):
            _resolve_agg("foobar")


# ═══════════════════════════════════════════════════════════════════════════
# _sort_categories tests
# ═══════════════════════════════════════════════════════════════════════════

class TestSortCategories:
    def test_sort_categories_temporal(self):
        s = pd.Series(["March 2024", "January 2024", "February 2024"])
        result = _sort_categories(s)
        assert result == ["January 2024", "February 2024", "March 2024"]

    def test_sort_categories_non_temporal(self):
        s = pd.Series(["Banana", "Apple", "Cherry", "Apple"])
        result = _sort_categories(s)
        # Preserves first-seen order
        assert result == ["Banana", "Apple", "Cherry"]


# ═══════════════════════════════════════════════════════════════════════════
# _resolve_layout tests
# ═══════════════════════════════════════════════════════════════════════════

class TestResolveLayout:
    def _make_option(self, n_cats, user_set_rotate=False, label_len=5):
        """Build a minimal cartesian option dict with n_cats categories."""
        cats = [f"{'C' * label_len}_{i}" for i in range(n_cats)]
        return {
            "xAxis": {
                "type": "category",
                "data": cats,
                "axisLabel": {"rotate": 0},
            },
            "yAxis": {"type": "value"},
            "grid": {"left": 60, "right": 60, "top": 60, "bottom": 50},
            "tooltip": {},
            "legend": {"data": []},
            "_meta": {"user_set_rotate": user_set_rotate},
        }

    def test_resolve_layout_auto_rotate(self):
        """Many categories with long labels trigger rotation."""
        # Use enough categories with long enough labels to exceed fill ratio
        opt = self._make_option(n_cats=20, label_len=8)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = _resolve_layout(opt, [])
        rotated = result["xAxis"]["axisLabel"]["rotate"]
        assert rotated > 0

    def test_resolve_layout_respects_user_rotate(self):
        """When user has explicitly set rotation, layout does not override it."""
        opt = self._make_option(n_cats=20, user_set_rotate=True, label_len=8)
        opt["xAxis"]["axisLabel"]["rotate"] = 0  # user explicitly set to 0
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = _resolve_layout(opt, [])
        # Should stay at 0 because user set it
        assert result["xAxis"]["axisLabel"]["rotate"] == 0
        # No OverlapWarning should be emitted
        overlap_warnings = [x for x in w if issubclass(x.category, OverlapWarning)]
        assert len(overlap_warnings) == 0

    def test_resolve_layout_legend_scroll(self):
        """Many legend items triggers scroll-type legend."""
        opt = self._make_option(n_cats=3)
        opt["legend"]["data"] = [f"Series_{i}" for i in range(12)]
        result = _resolve_layout(opt, [])
        assert result["legend"]["type"] == "scroll"

    def test_resolve_layout_tooltip_confine(self):
        """Layout always sets tooltip confine to True."""
        opt = self._make_option(n_cats=3)
        result = _resolve_layout(opt, [])
        assert result["tooltip"]["confine"] is True
