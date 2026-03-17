"""Shared fixtures for echartsy test suite."""
from __future__ import annotations

import pytest
import pandas as pd

import echartsy._config as _cfg


# ── Auto-reset global config after every test ────────────────────────────

@pytest.fixture(autouse=True)
def _reset_config():
    """Reset echartsy global config to defaults after each test."""
    yield
    _cfg._current_engine = "python"
    _cfg._adaptive_theme = "auto"
    _cfg._overlap_warnings = True


# ── Small DataFrames ─────────────────────────────────────────────────────

@pytest.fixture
def simple_df():
    """3-row DataFrame with X (category) and Y (numeric) columns."""
    return pd.DataFrame({
        "X": ["A", "B", "C"],
        "Y": [10, 20, 30],
    })


@pytest.fixture
def time_df():
    """DataFrame with a time_col for timeline testing."""
    return pd.DataFrame({
        "Month": ["Jan", "Jan", "Feb", "Feb", "Mar", "Mar"],
        "Category": ["East", "West", "East", "West", "East", "West"],
        "Value": [100, 150, 120, 160, 140, 170],
    })


@pytest.fixture
def hue_df():
    """DataFrame with a hue/grouping column."""
    return pd.DataFrame({
        "X": ["A", "A", "B", "B", "C", "C"],
        "Y": [10, 15, 20, 25, 30, 35],
        "Group": ["G1", "G2", "G1", "G2", "G1", "G2"],
    })


@pytest.fixture
def ohlc_df():
    """OHLC candlestick data (5 rows)."""
    return pd.DataFrame({
        "Date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
        "Open": [100.0, 102.0, 101.0, 105.0, 103.0],
        "Close": [102.0, 101.0, 105.0, 103.0, 106.0],
        "Low": [99.0, 100.0, 100.5, 102.0, 102.5],
        "High": [103.0, 103.5, 106.0, 106.0, 107.0],
    })


@pytest.fixture
def sankey_df():
    """Multi-level data for sankey/treemap/sunburst."""
    return pd.DataFrame({
        "Level1": ["A", "A", "B", "B"],
        "Level2": ["X", "Y", "X", "Z"],
        "Value": [10, 20, 30, 40],
    })


@pytest.fixture
def nodes_df():
    """Graph node data."""
    return pd.DataFrame({
        "name": ["Alice", "Bob", "Carol"],
        "group": ["team1", "team1", "team2"],
    })


@pytest.fixture
def edges_df():
    """Graph edge data."""
    return pd.DataFrame({
        "source": ["Alice", "Alice", "Bob"],
        "target": ["Bob", "Carol", "Carol"],
    })


@pytest.fixture
def calendar_df():
    """Date + value data for calendar heatmap."""
    dates = pd.date_range("2024-01-01", periods=5, freq="D")
    return pd.DataFrame({
        "date": dates.strftime("%Y-%m-%d"),
        "value": [1, 3, 2, 5, 4],
    })
