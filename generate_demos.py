#!/usr/bin/env python3
"""Generate demo chart HTML files for README screenshots.

Uses the same examples from examples.ipynb with proper legend/title spacing.

Run from project root:
    python generate_demos.py

Then capture screenshots:
    python capture_screenshots.py
"""
import os
import sys

import pandas as pd
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import echartslib as ec

ec.config(engine="python")

ASSETS = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(ASSETS, exist_ok=True)


def _save(fig, name):
    path = os.path.join(ASSETS, f"{name}.html")
    fig.to_html(path)
    print(f"  ✓ {path}")


# ── 1.  Simple Bar + Pie Overlay (Example 1 from notebook) ─────────
df_fruit = pd.DataFrame({
    "Fruit": ["Apples", "Bananas", "Cherries", "Dates", "Elderberries"],
    "Sales": [120, 95, 78, 42, 63],
})

fig = ec.figure(renderer="svg")
fig.bar(df_fruit, x="Fruit", y="Sales")
fig.title("Fruit Sales")
fig.pie(df_fruit, names="Fruit", values="Sales",
        center=["85%", "25%"], radius=["10%", "30%"],
        label_font_size=5)
fig.legend(top=40)
fig.margins(top=40)
fig.toolbox()
_save(fig, "demo_bar_pie")


# ── 2.  Smooth Line (Example 2) ────────────────────────────────────
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

df_temp = pd.DataFrame({
    "Month": months,
    "Temperature": [5, 7, 12, 18, 23, 28, 31, 30, 25, 18, 11, 6],
})

fig = ec.figure(height="400px")
fig.plot(df_temp, x="Month", y="Temperature", smooth=True)
fig.title("Average Monthly Temperature")
fig.ylabel("Temp (°C)")
fig.legend(top=40)
fig.margins(top=40)
_save(fig, "demo_line")


# ── 3.  Donut Chart (Example 3) ────────────────────────────────────
df_market = pd.DataFrame({
    "Browser": ["Chrome", "Safari", "Firefox", "Edge", "Other"],
    "Share": [65.7, 18.2, 6.3, 5.1, 4.7],
})

fig = ec.figure(height="450px")
fig.pie(df_market, names="Browser", values="Share", inner_radius="40%")
fig.title("Browser Market Share 2025")
_save(fig, "demo_pie")


# ── 4.  Scatter Plot (Example 4) ───────────────────────────────────
np.random.seed(42)
n = 80
df_scatter = pd.DataFrame({
    "Height": np.random.normal(170, 10, n),
    "Weight": np.random.normal(70, 12, n),
    "Gender": np.random.choice(["Male", "Female"], n),
})

fig = ec.figure(height="450px")
fig.scatter(df_scatter, x="Height", y="Weight", color="Gender")
fig.title("Height vs Weight")
fig.xlabel("Height (cm)")
fig.ylabel("Weight (kg)")
fig.legend(top=40)
fig.margins(top=40)
_save(fig, "demo_scatter")


# ── 5.  Stacked Bar with Hue (Example 6) ───────────────────────────
df_revenue = pd.DataFrame({
    "Quarter": ["Q1", "Q2", "Q3", "Q4"] * 3,
    "Revenue": [120, 145, 160, 180, 90, 110, 130, 155, 60, 80, 95, 110],
    "Region": ["North"] * 4 + ["South"] * 4 + ["West"] * 4,
})

fig = ec.figure(height="450px")
fig.bar(df_revenue, x="Quarter", y="Revenue", hue="Region",
        stack=True, labels=True)
fig.palette(ec.PALETTE_RUSTY)
fig.title("Stacked Revenue by Region")
fig.ylabel("Revenue ($K)")
fig.legend(top=40)
fig.margins(top=40)
_save(fig, "demo_stacked")


# ── 6.  Area Chart (Example 8) ─────────────────────────────────────
df_traffic = pd.DataFrame({
    "Hour": list(range(24)),
    "Users": [12, 8, 5, 3, 4, 8, 25, 60, 95, 120, 110, 105,
              115, 108, 100, 98, 112, 130, 95, 70, 50, 35, 22, 15],
})

fig = ec.figure(height="400px")
fig.plot(df_traffic, x="Hour", y="Users", smooth=True,
         area=True, area_opacity=0.3)
fig.title("Website Traffic — 24hr")
fig.xlabel("Hour of Day")
fig.ylabel("Active Users")
fig.legend(top=40)
fig.margins(top=40)
_save(fig, "demo_area")


# ── 7.  Horizontal Bar (Example 9) ─────────────────────────────────
df_lang = pd.DataFrame({
    "Language": ["Python", "JavaScript", "TypeScript", "Java", "C#",
                 "C++", "Go", "Rust", "Kotlin", "Swift"],
    "Popularity": [100, 95, 72, 68, 60, 55, 48, 42, 38, 35],
})

fig = ec.figure(height="450px")
fig.bar(df_lang, x="Language", y="Popularity", orient="h",
        gradient=True, gradient_colors=("#83bff6", "#188df0"))
fig.title("Programming Language Popularity")
fig.margins(top=40)
_save(fig, "demo_horizontal")


# ── 8.  Dual Axis: Bar + Line (Example 10) ─────────────────────────
df_sales = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Revenue": [250, 310, 280, 400, 520, 480],
})
df_growth = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "GrowthRate": [5.2, 8.1, 6.5, 12.3, 18.7, 15.0],
})

fig = ec.figure(height="500px")
fig.bar(df_sales, x="Month", y="Revenue", labels=True)
fig.plot(df_growth, x="Month", y="GrowthRate", smooth=True, axis=1)
fig.title("Revenue & Growth Rate")
fig.ylabel("Revenue ($K)")
fig.ylabel_right("Growth %")
fig.legend(top=40)
fig.margins(top=40)
_save(fig, "demo_dual")


# ── 9.  Radar Chart (Example 11) ───────────────────────────────────
indicators = [
    {"name": "Attack", "max": 100},
    {"name": "Defense", "max": 100},
    {"name": "Speed", "max": 100},
    {"name": "Stamina", "max": 100},
    {"name": "Magic", "max": 100},
    {"name": "Intelligence", "max": 100},
]
data = [
    [90, 60, 80, 70, 40, 55],
    [30, 40, 50, 60, 95, 90],
    [70, 50, 95, 80, 20, 65],
]

fig = ec.figure(height="500px")
fig.radar(indicators, data, series_names=["Warrior", "Mage", "Rogue"])
fig.title("Character Class Comparison")
_save(fig, "demo_radar")


# ── 10. Dark Theme + Stacked (Example 17) ──────────────────────────
fig = ec.figure(height="500px", theme="dark", style=ec.StylePreset.DASHBOARD_DARK)
fig.bar(df_revenue, x="Quarter", y="Revenue", hue="Region",
        stack=True, border_radius=6)
fig.title("Revenue by Region (Dark Mode)")
fig.ylabel("Revenue ($K)")
fig.toolbox()
fig.datazoom()
fig.legend(top=40)
fig.margins(top=40)
_save(fig, "demo_dark")


# ── 11. Gradient Bars (Example 18) ─────────────────────────────────
fig = ec.figure(height="450px")
fig.bar(df_fruit, x="Fruit", y="Sales",
        gradient=True, gradient_colors=("#667eea", "#764ba2"),
        labels=True, border_radius=8)
fig.title("Fruit Sales (Gradient)")
fig.ylabel("Units Sold")
fig.palette(["#667eea", "#764ba2", "#f093fb", "#f5576c", "#4facfe"])
fig.grid(show=True)
fig.margins(top=40)
_save(fig, "demo_gradient")


# ── 12. Multi-Line with Hue (Example 19) ───────────────────────────
months6 = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
df_multi = pd.DataFrame({
    "Month": months6 * 3,
    "Visitors": [100, 120, 150, 200, 180, 210,
                 80, 95, 120, 160, 140, 170,
                 60, 70, 90, 110, 100, 130],
    "Source": ["Organic"] * 6 + ["Paid"] * 6 + ["Social"] * 6,
})

fig = ec.figure(height="450px")
fig.plot(df_multi, x="Month", y="Visitors", hue="Source",
         smooth=True, area=True, area_opacity=0.15)
fig.title("Traffic by Source")
fig.ylabel("Visitors (K)")
fig.legend(show=True, top=40)
fig.margins(top=40)
_save(fig, "demo_multiline")


# ── 13. KPI Dashboard (Example 20) ─────────────────────────────────
np.random.seed(2026)
months_full = pd.date_range("2024-01", periods=24, freq="MS").strftime("%b %Y").tolist()

df_kpi = pd.DataFrame({
    "Month": months_full,
    "Revenue": np.cumsum(np.random.normal(50, 15, 24)).clip(100).tolist(),
})
df_margin = pd.DataFrame({
    "Month": months_full,
    "Margin": np.random.uniform(15, 35, 24).tolist(),
})

fig = ec.figure(height="550px", style=ec.StylePreset.KPI_REPORT)
fig.bar(df_kpi, x="Month", y="Revenue", labels=False, border_radius=4)
fig.plot(df_margin, x="Month", y="Margin", smooth=True, axis=1,
         line_width=3, symbol_size=8)
fig.title("KPI Dashboard: Revenue & Margin", subtitle="Jan 2024 – Dec 2025")
fig.ylabel("Cumulative Revenue ($K)")
fig.ylabel_right("Margin %")
fig.toolbox()
fig.legend(top=50)
fig.datazoom()
fig.margins(top=50)
fig.save(name="kpi_dashboard")
_save(fig, "demo_dashboard")


# ── 14. Bar + Line + Pie Triple Composite (Example 26) ─────────────
df_monthly = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Revenue": [250, 310, 280, 400, 520, 480],
})
df_growth2 = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Growth": [5.2, 8.1, 6.5, 12.3, 18.7, 15.0],
})
df_mix = pd.DataFrame({
    "Plan": ["Enterprise", "Pro", "Starter", "Free-trial"],
    "Share": [45, 30, 15, 10],
})

fig = ec.figure(height="550px")
fig.bar(df_monthly, x="Month", y="Revenue", labels=True, border_radius=4)
fig.plot(df_growth2, x="Month", y="Growth", smooth=True, axis=1,
         line_width=3, symbol_size=8)
fig.pie(df_mix, names="Plan", values="Share",
        center=["85%", "22%"], radius=["15%", "25%"],
        border_radius=4, label_font_size=9)
fig.title("Monthly KPIs: Revenue, Growth & Product Mix")
fig.ylabel("Revenue ($K)")
fig.ylabel_right("Growth %")
fig.margins(right=120, top=40)
fig.legend(top=40)
_save(fig, "demo_composite")


# ── 15. Stacked + Trend + Pie Breakdown (Example 28) ───────────────
df_totals = df_revenue.groupby("Quarter", sort=False)["Revenue"].sum().reset_index()
df_totals.columns = ["Quarter", "Total"]
region_totals = (df_revenue.groupby("Region")["Revenue"].sum()
                 .reset_index().rename(columns={"Revenue": "Total"}))

fig = ec.figure(height="550px")
fig.bar(df_revenue, x="Quarter", y="Revenue", hue="Region",
        stack=True, border_radius=4)
fig.plot(df_totals, x="Quarter", y="Total", smooth=True, axis=1,
         line_width=3, symbol_size=10, labels=True)
fig.pie(region_totals, names="Region", values="Total",
        center=["86%", "20%"], radius=["12%", "22%"],
        border_radius=4, label_font_size=9)
fig.title("Quarterly Revenue: Stacked + Trend + Breakdown")
fig.ylabel("Revenue ($K)")
fig.ylabel_right("Total ($K)")
fig.margins(right=120, top=50)
fig.legend(top=45)
_save(fig, "demo_full_dashboard")


print(f"\nDone — 15 demo HTML files written to {ASSETS}/")
