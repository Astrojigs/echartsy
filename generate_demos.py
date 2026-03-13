#!/usr/bin/env python3
"""Generate demo chart HTML files for README screenshots.

Mirrors the examples from examples.ipynb exactly.

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
import echartsy as ec

ec.config(engine="python")

ASSETS = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(ASSETS, exist_ok=True)


def _save(fig, name):
    path = os.path.join(ASSETS, f"{name}.html")
    fig.to_html(path)
    print(f"  ✓ {path}")


# ── 1.  Simple Bar + Pie Overlay (Notebook #1) ─────────────────────
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


# ── 2.  Smooth Line (Notebook #2) ──────────────────────────────────
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
_save(fig, "demo_line")


# ── 3.  Donut Chart (Notebook #3) ──────────────────────────────────
df_market = pd.DataFrame({
    "Browser": ["Chrome", "Safari", "Firefox", "Edge", "Other"],
    "Share": [65.7, 18.2, 6.3, 5.1, 4.7],
})

fig = ec.figure(height="450px")
fig.pie(df_market, names="Browser", values="Share", inner_radius="40%")
fig.title("Browser Market Share 2025")
_save(fig, "demo_pie")


# ── 4.  Scatter Plot (Notebook #4) ─────────────────────────────────
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
_save(fig, "demo_scatter")


# ── 5.  Grouped Bar with Hue (Notebook #5) ─────────────────────────
df_revenue = pd.DataFrame({
    "Quarter": ["Q1", "Q2", "Q3", "Q4"] * 3,
    "Revenue": [120, 145, 160, 180, 90, 110, 130, 155, 60, 80, 95, 110],
    "Region": ["North"] * 4 + ["South"] * 4 + ["West"] * 4,
})

fig = ec.figure(height="450px")
fig.bar(df_revenue, x="Quarter", y="Revenue", hue="Region")
fig.title("Quarterly Revenue by Region")
fig.ylabel("Revenue ($K)")
fig.legend(top=40)
_save(fig, "demo_grouped")


# ── 6.  Stacked Bar (Notebook #6) ──────────────────────────────────
fig = ec.figure(height="450px")
fig.bar(df_revenue, x="Quarter", y="Revenue", hue="Region",
        stack=True, labels=True)
fig.palette(ec.PALETTE_RUSTY)
fig.title("Stacked Revenue by Region")
fig.ylabel("Revenue ($K)")
fig.legend(top=40)
_save(fig, "demo_stacked")


# ── 7.  Histogram (Notebook #7) ────────────────────────────────────
np.random.seed(7)
df_scores = pd.DataFrame({"Score": np.random.normal(72, 15, 500)})

fig = ec.figure(height="400px")
fig.hist(df_scores, column="Score", bins=10)
fig.title("Exam Score Distribution")
fig.xlabel("Score")
fig.ylabel("Count")
_save(fig, "demo_histogram")


# ── 8.  Area Chart (Notebook #8) ───────────────────────────────────
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
_save(fig, "demo_area")


# ── 9.  Horizontal Bar (Notebook #9) ───────────────────────────────
df_lang = pd.DataFrame({
    "Language": ["Python", "JavaScript", "TypeScript", "Java", "C#",
                 "C++", "Go", "Rust", "Kotlin", "Swift"],
    "Popularity": [100, 95, 72, 68, 60, 55, 48, 42, 38, 35],
})

fig = ec.figure(height="450px")
fig.bar(df_lang, x="Language", y="Popularity", orient="h",
        gradient=True, gradient_colors=("#83bff6", "#188df0"))
fig.title("Programming Language Popularity")
fig.legend(top=40)
fig.margins(top=70)
_save(fig, "demo_horizontal")


# ── 10. Dual Axis: Bar + Line (Notebook #10) ───────────────────────
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
fig.legend(top=40)
fig.ylabel_right("Growth %")
_save(fig, "demo_dual")


# ── 11. Radar Chart (Notebook #11) ─────────────────────────────────
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
fig.palette(ec.PALETTE_CLINICAL)
_save(fig, "demo_radar")


# ── 12. Heatmap (Notebook #12) ─────────────────────────────────────
days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
hours = ["9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm"]

np.random.seed(123)
rows = []
for d in days:
    for h in hours:
        rows.append({"Day": d, "Hour": h, "Emails": np.random.randint(2, 50)})

df_heatmap = pd.DataFrame(rows)

fig = ec.figure(height="450px")
fig.heatmap(df_heatmap, x="Hour", y="Day", value="Emails")
fig.title("Emails Received per Hour")
_save(fig, "demo_heatmap")


# ── 13. Funnel Chart (Notebook #13) ────────────────────────────────
df_funnel = pd.DataFrame({
    "Stage": ["Visitors", "Sign-ups", "Trial", "Paid", "Enterprise"],
    "Count": [10000, 3200, 1400, 600, 120],
})

fig = ec.figure(height="450px")
fig.funnel(df_funnel, names="Stage", values="Count")
fig.title("Conversion Funnel")
_save(fig, "demo_funnel")


# ── 14. Treemap (Notebook #14) ─────────────────────────────────────
df_tree = pd.DataFrame({
    "Category": ["Electronics", "Electronics", "Electronics",
                 "Clothing", "Clothing", "Clothing",
                 "Food", "Food"],
    "SubCategory": ["Phones", "Laptops", "Tablets",
                    "Shirts", "Pants", "Shoes",
                    "Fruit", "Dairy"],
    "Sales": [500, 420, 180, 300, 250, 200, 150, 100],
})

fig = ec.figure(height="500px")
fig.treemap(df_tree, path=["Category", "SubCategory"], value="Sales", roam=False)
fig.title("Sales by Category")
_save(fig, "demo_treemap")


# ── 15. Sankey Diagram (Notebook #15) ──────────────────────────────
df_flow = pd.DataFrame({
    "Source": ["Organic", "Organic", "Paid", "Paid", "Referral", "Referral"],
    "Channel": ["Landing Page A", "Landing Page B",
                "Landing Page A", "Landing Page B",
                "Landing Page A", "Landing Page B"],
    "Outcome": ["Converted", "Bounced", "Converted", "Bounced",
                "Converted", "Bounced"],
    "Users": [350, 150, 200, 300, 180, 70],
})

fig = ec.figure(height="500px")
fig.sankey(df_flow, levels=["Source", "Channel", "Outcome"], value="Users")
fig.title("User Flow: Source → Page → Outcome")
_save(fig, "demo_sankey")


# ── 16. Boxplot (Notebook #16) ─────────────────────────────────────
np.random.seed(99)
df_box = pd.DataFrame({
    "Department": np.repeat(["Engineering", "Marketing", "Sales", "Design"], 50),
    "Salary": np.concatenate([
        np.random.normal(120, 20, 50),
        np.random.normal(90, 15, 50),
        np.random.normal(85, 25, 50),
        np.random.normal(95, 18, 50),
    ]),
})

fig = ec.figure(height="450px")
fig.boxplot(df_box, x="Department", y="Salary")
fig.title("Salary Distribution by Department")
fig.ylabel("Salary ($K)")
_save(fig, "demo_boxplot")


# ── 17. Dark Theme (Notebook #17) ──────────────────────────────────
fig = ec.figure(height="500px", theme="dark", style=ec.StylePreset.DASHBOARD_DARK)
fig.bar(df_revenue, x="Quarter", y="Revenue", hue="Region",
        stack=True, border_radius=6)
fig.title("Revenue by Region (Dark Mode)")
fig.ylabel("Revenue ($K)")
fig.toolbox()
fig.legend(top=40)
_save(fig, "demo_dark")


# ── 18. Gradient Bars (Notebook #18) ───────────────────────────────
fig = ec.figure(height="450px")
fig.bar(df_fruit, x="Fruit", y="Sales",
        gradient=True, gradient_colors=("#667eea", "#764ba2"),
        labels=True, border_radius=8)
fig.title("Fruit Sales (Gradient)")
fig.ylabel("Units Sold")
fig.palette(["#667eea", "#764ba2", "#f093fb", "#f5576c", "#4facfe"])
fig.grid(show=True)
fig.legend(top=40)
_save(fig, "demo_gradient")


# ── 19. Multi-Line with Hue (Notebook #19) ─────────────────────────
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
fig.legend(show=True, top=30)
_save(fig, "demo_multiline")


# ── 20. KPI Dashboard (Notebook #20) ───────────────────────────────
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
fig.margins(top=40)
fig.save(name="kpi_dashboard")
_save(fig, "demo_dashboard")


# ── 25. Bar + Pie Overlay — Dark Style (Notebook #25) ──────────────
df_dept = pd.DataFrame({
    "Department": ["Engineering", "Marketing", "Sales", "Design", "Support"],
    "Budget": [450, 280, 320, 180, 120],
})

fig = ec.figure(height="500px", style=ec.StylePreset.DASHBOARD_DARK)
fig.bar(df_dept, x="Department", y="Budget", border_radius=6,
        gradient=True, gradient_colors=["#f4f1de", "#e07a5f"],
        labels=True, label_color="orange")
fig.title("Department Budgets ($K)")
fig.ylabel("Budget ($K)")
fig.pie(df_dept, names="Department", values="Budget",
        center=["82%", "25%"], radius=["18%", "28%"],
        border_radius=4, label_font_size=9)
fig.legend(top=40, left=200)
fig.margins(right=120)
_save(fig, "demo_composite_dark")


# ── 26. Triple Composite (Notebook #26) ────────────────────────────
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
        center=["25%", "32%"], radius=["15%", "25%"],
        border_radius=4, label_font_size=9)
fig.title("Monthly KPIs: Revenue, Growth & Product Mix")
fig.ylabel("Revenue ($K)")
fig.ylabel_right("Growth %")
fig.legend(top=40, left=350)
fig.margins(right=20)
_save(fig, "demo_composite")


# ── 27. Side-by-Side Pies (Notebook #27) ───────────────────────────
df_q1 = pd.DataFrame({
    "Product": ["Product A", "Product B", "Product C"],
    "Revenue": [40, 35, 25],
})
df_q2 = pd.DataFrame({
    "Product": ["Product A", "Product B", "Product C"],
    "Revenue": [30, 42, 28],
})

fig = ec.figure(height="450px")
fig.pie(df_q1, names="Product", values="Revenue",
        center=["28%", "55%"], radius=["25%", "40%"],
        border_radius=6, label_font_size=10)
fig.pie(df_q2, names="Product", values="Revenue",
        center=["72%", "55%"], radius=["25%", "40%"],
        border_radius=6, label_font_size=10)
fig.title("Product Mix: Q1 vs Q2")
fig.extra(
    legend={"data": ["Product A", "Product B", "Product C"],
            "top": 40, "left": "center"},
    graphic=[
        {"type": "text", "left": "18%", "top": "88%",
         "style": {"text": "Q1 2025", "fontSize": 14, "fontWeight": "bold",
                    "fill": "#888"}},
        {"type": "text", "left": "62%", "top": "88%",
         "style": {"text": "Q2 2025", "fontSize": 14, "fontWeight": "bold",
                    "fill": "#888"}},
    ],
)
_save(fig, "demo_sidebyside_pies")


# ── 28. Stacked + Trend + Pie Breakdown (Notebook #28) ─────────────
df_rev = pd.DataFrame({
    "Quarter": ["Q1", "Q2", "Q3", "Q4"] * 3,
    "Revenue": [120, 145, 160, 180, 90, 110, 130, 155, 60, 80, 95, 110],
    "Region":  ["North"] * 4 + ["South"] * 4 + ["West"] * 4,
})

df_totals = df_rev.groupby("Quarter", sort=False)["Revenue"].sum().reset_index()
df_totals.columns = ["Quarter", "Total"]
region_totals = (df_rev.groupby("Region")["Revenue"].sum()
                 .reset_index().rename(columns={"Revenue": "Total"}))

fig = ec.figure(height="550px")
fig.bar(df_rev, x="Quarter", y="Revenue", hue="Region",
        stack=True, border_radius=4)
fig.plot(df_totals, x="Quarter", y="Total", smooth=True, axis=1,
         line_width=3, symbol_size=10, labels=True)
fig.pie(region_totals, names="Region", values="Total",
        center=["26%", "20%"], radius=["12%", "22%"],
        border_radius=4, label_font_size=9)
fig.title("Quarterly Revenue: Stacked + Trend + Breakdown")
fig.ylabel("Revenue ($K)")
fig.ylabel_right("Total ($K)")
fig.margins(right=120)
fig.legend(top=35)
_save(fig, "demo_full_dashboard")


print(f"\nDone — all demo HTML files written to {ASSETS}/")
