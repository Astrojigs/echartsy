#!/usr/bin/env python3
"""Generate demo chart HTML files for README screenshots.

Run this script from the project root:

    python generate_demos.py

It creates HTML files in the ``assets/`` directory that can then be
screenshotted with ``capture_screenshots.py``.
"""
import os
import sys

import pandas as pd
import numpy as np

# Ensure local echartslib is importable
sys.path.insert(0, os.path.dirname(__file__))
import echartslib as ec

ec.config(engine="python")  # we only use to_html(), engine doesn't matter

ASSETS = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(ASSETS, exist_ok=True)


def _save(fig, name):
    path = os.path.join(ASSETS, f"{name}.html")
    fig.to_html(path)
    print(f"  ✓ {path}")


# ── 1.  Gradient Bar ────────────────────────────────────────────────
df_bar = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Revenue": [120, 200, 150, 300, 250, 280],
})
fig = ec.figure(height="420px")
fig.bar(df_bar, x="Month", y="Revenue", border_radius=6, gradient=True)
fig.title("Monthly Revenue", subtitle="2025 H1 · echartslib")
fig.ylabel("Revenue ($K)")
fig.toolbox(download=True)
_save(fig, "demo_bar")


# ── 2.  Multi-line with hue + area ─────────────────────────────────
np.random.seed(42)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"] * 3
regions = (["North"] * 6) + (["South"] * 6) + (["West"] * 6)
values = np.random.randint(50, 300, 18).tolist()
df_line = pd.DataFrame({"Month": months, "Region": regions, "Sales": values})

fig = ec.figure(height="420px")
fig.plot(df_line, x="Month", y="Sales", hue="Region", smooth=True, area=True)
fig.title("Regional Sales Trends")
fig.ylabel("Sales ($K)")
fig.toolbox(download=True)
_save(fig, "demo_line")


# ── 3.  Donut chart ────────────────────────────────────────────────
df_pie = pd.DataFrame({
    "Browser": ["Chrome", "Safari", "Firefox", "Edge", "Other"],
    "Share":   [64.7, 18.6, 6.3, 5.1, 5.3],
})
fig = ec.figure(height="420px")
fig.pie(df_pie, names="Browser", values="Share", inner_radius="40%")
fig.title("Browser Market Share", subtitle="2025 Q1")
_save(fig, "demo_pie")


# ── 4.  Scatter ─────────────────────────────────────────────────────
np.random.seed(7)
n = 80
df_scatter = pd.DataFrame({
    "Height": np.round(np.random.normal(170, 10, n), 1),
    "Weight": np.round(np.random.normal(70, 12, n), 1),
    "Gender": np.random.choice(["Male", "Female"], n),
})
fig = ec.figure(height="420px")
fig.scatter(df_scatter, x="Height", y="Weight", color="Gender")
fig.title("Height vs Weight Distribution")
fig.xlabel("Height (cm)")
fig.ylabel("Weight (kg)")
fig.toolbox(download=True)
_save(fig, "demo_scatter")


# ── 5.  Composite: bar + pie overlay ───────────────────────────────
df_dept = pd.DataFrame({
    "Dept":   ["Engineering", "Marketing", "Sales", "HR", "Finance"],
    "Budget": [450, 200, 350, 120, 180],
})
fig = ec.figure(height="480px")
fig.bar(df_dept, x="Dept", y="Budget", gradient=True, border_radius=6)
fig.pie(df_dept, names="Dept", values="Budget",
        center=["82%", "25%"], radius=["15%", "28%"],
        label_font_size=9)
fig.title("Department Budgets", subtitle="with pie breakdown")
fig.ylabel("Budget ($K)")
_save(fig, "demo_composite")


# ── 6.  Dual-axis ──────────────────────────────────────────────────
df_dual = pd.DataFrame({
    "Month":   ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Revenue": [120, 200, 150, 300, 250, 280],
    "Growth":  [5.2, 8.1, 3.0, 12.4, 9.6, 10.2],
})
fig = ec.figure(height="420px")
fig.bar(df_dual, x="Month", y="Revenue", gradient=True, border_radius=4)
fig.plot(df_dual, x="Month", y="Growth", axis=1, smooth=True)
fig.title("Revenue & Growth")
fig.ylabel("Revenue ($K)")
fig.ylabel_right("Growth (%)")
fig.toolbox(download=True)
_save(fig, "demo_dual")


# ── 7.  Dark-mode bar ──────────────────────────────────────────────
fig = ec.figure(height="420px", style=ec.StylePreset.DASHBOARD_DARK)
fig.bar(df_bar, x="Month", y="Revenue", gradient=True, border_radius=6)
fig.title("Monthly Revenue", subtitle="Dark Theme")
fig.ylabel("Revenue ($K)")
_save(fig, "demo_dark")


# ── 8.  Radar ───────────────────────────────────────────────────────
indicators = [
    {"name": "Attack", "max": 100},
    {"name": "Defense", "max": 100},
    {"name": "Speed", "max": 100},
    {"name": "Power", "max": 100},
    {"name": "Endurance", "max": 100},
    {"name": "Technique", "max": 100},
]
data = [
    [90, 60, 85, 70, 80, 95],
    [70, 85, 60, 90, 75, 65],
]
fig = ec.figure(height="460px")
fig.radar(indicators, data, series_names=["Player A", "Player B"])
fig.title("Player Comparison")
_save(fig, "demo_radar")


# ── 9.  Stacked bar ────────────────────────────────────────────────
quarters = ["Q1", "Q2", "Q3", "Q4"] * 3
products = (["Widget"] * 4) + (["Gadget"] * 4) + (["Doohickey"] * 4)
sales = [30, 40, 35, 50, 25, 30, 45, 40, 15, 20, 25, 30]
df_stack = pd.DataFrame({"Quarter": quarters, "Product": products, "Sales": sales})

fig = ec.figure(height="420px")
fig.bar(df_stack, x="Quarter", y="Sales", hue="Product", stack=True,
        border_radius=[4, 4, 0, 0], gradient=True)
fig.title("Quarterly Sales by Product", subtitle="Stacked")
fig.ylabel("Sales ($K)")
fig.toolbox(download=True)
_save(fig, "demo_stacked")


# ── 10. Horizontal bar ─────────────────────────────────────────────
df_h = pd.DataFrame({
    "Language": ["Python", "JavaScript", "TypeScript", "Java", "Go", "Rust"],
    "Stars":    [450, 380, 290, 210, 180, 160],
})
fig = ec.figure(height="400px")
fig.bar(df_h, x="Language", y="Stars", orient="h", gradient=True, border_radius=4)
fig.title("GitHub Stars by Language")
fig.margins(left=100)
_save(fig, "demo_horizontal")


print(f"\nDone — {10} demo HTML files written to {ASSETS}/")
