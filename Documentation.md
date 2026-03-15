# echartsy Documentation

A matplotlib-style fluent builder API for [Apache ECharts](https://echarts.apache.org/) in Python, Jupyter Notebooks, and Streamlit.

Build interactive, publication-quality charts with a familiar chaining syntax. One API, three renderers.

```python
import echartsy as ec

ec.config(engine="jupyter")  # or "python" or "streamlit"

fig = ec.figure(height="500px")
fig.bar(df, x="Month", y="Revenue", hue="Region", stack=True)
fig.plot(df_totals, x="Month", y="Target", smooth=True, axis=1)
fig.title("Revenue vs Target")
fig.ylabel("Revenue")
fig.ylabel_right("Target (%)")
fig.show()
```

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Chart Types](#chart-types)
  - [Bar Chart](#bar-chart)
  - [Line Chart](#line-chart)
  - [Scatter Plot](#scatter-plot)
  - [Pie / Donut Chart](#pie--donut-chart)
  - [Histogram](#histogram)
  - [Area Chart](#area-chart)
  - [Horizontal Bar](#horizontal-bar)
  - [Radar Chart](#radar-chart)
  - [Heatmap](#heatmap)
  - [Box Plot](#box-plot)
  - [KDE (Kernel Density)](#kde-kernel-density)
  - [Funnel Chart](#funnel-chart)
  - [Treemap](#treemap)
  - [Sankey Diagram](#sankey-diagram)
  - [Candlestick Chart](#candlestick-chart)
- [Composite Charts](#composite-charts)
  - [Dual Axis (Bar + Line)](#dual-axis-bar--line)
  - [Bar + Pie Overlay](#bar--pie-overlay)
  - [Triple Composite](#triple-composite)
  - [Side-by-Side Pies](#side-by-side-pies)
  - [Stacked + Trend + Breakdown](#stacked--trend--breakdown)
  - [Candlestick + Moving Average + Volume](#candlestick--moving-average--volume)
- [Chart Configuration](#chart-configuration)
  - [Titles](#titles)
  - [Axes & Ticks](#axes--ticks)
  - [Grid & Margins](#grid--margins)
  - [Legend](#legend)
  - [Tooltip](#tooltip)
  - [Axis Pointer](#axis-pointer)
  - [Data Zoom](#data-zoom)
  - [Toolbox](#toolbox)
  - [Palette](#palette)
  - [Extra Options](#extra-options)
- [Timeline Animations](#timeline-animations)
  - [Animated Bar Chart](#animated-bar-chart)
  - [Animated Line Chart](#animated-line-chart)
  - [Animated Pie Chart](#animated-pie-chart)
  - [Animated Scatter Plot](#animated-scatter-plot)
  - [Animated Histogram](#animated-histogram)
  - [Playback Controls](#playback-controls)
- [Style Presets](#style-presets)
  - [Built-in Presets](#built-in-presets)
  - [Custom Presets](#custom-presets)
  - [Palettes](#palettes)
  - [Dark Theme](#dark-theme)
- [Emphasis & Hover Effects](#emphasis--hover-effects)
  - [Bar Emphasis](#bar-emphasis)
  - [Line Emphasis](#line-emphasis)
  - [Pie Emphasis](#pie-emphasis)
  - [Scatter Emphasis](#scatter-emphasis)
  - [Sankey Emphasis](#sankey-emphasis)
  - [Heatmap Emphasis](#heatmap-emphasis)
- [Exporting](#exporting)
  - [HTML Export](#html-export)
  - [Image Export](#image-export)
  - [Raw ECharts Option](#raw-echarts-option)
- [Streamlit Integration](#streamlit-integration)
- [API Reference](#api-reference)
  - [Figure](#figure)
  - [TimelineFigure](#timelinefigure)
  - [StylePreset](#stylepreset)
  - [Emphasis Classes](#emphasis-classes)
  - [Exceptions](#exceptions)

---

## Installation

```bash
pip install echartsy
```

Optional dependencies for specific renderers:

```bash
pip install echartsy[jupyter]     # Jupyter Notebook / Lab
pip install echartsy[streamlit]   # Streamlit apps
pip install echartsy[scipy]       # KDE (kernel density estimation)
pip install echartsy[all]         # Everything
```

**Requirements:** Python 3.9+, pandas >= 1.5.0, numpy >= 1.23.0

---

## Quick Start

```python
import pandas as pd
import echartsy as ec

ec.config(engine="jupyter")  # "python" opens in browser, "streamlit" for Streamlit apps

df = pd.DataFrame({
    "Fruit": ["Apples", "Bananas", "Cherries", "Dates", "Elderberries"],
    "Sales": [120, 95, 78, 42, 63],
})

fig = ec.figure()
fig.bar(df, x="Fruit", y="Sales", gradient=True, labels=True)
fig.title("Fruit Sales")
fig.show()
```

Every method returns `self`, so you can chain:

```python
(
    ec.figure(height="500px")
    .bar(df, x="Fruit", y="Sales", gradient=True, border_radius=8)
    .title("Fruit Sales")
    .ylabel("Units Sold")
    .tooltip()
    .toolbox()
    .show()
)
```

---

## Configuration

Set the global rendering engine before creating charts:

```python
import echartsy as ec

# Choose one:
ec.config(engine="python")      # Opens chart in default browser
ec.config(engine="jupyter")     # Inline in Jupyter Notebook / Lab
ec.config(engine="streamlit")   # Inside a Streamlit app
```

**Adaptive dark mode** (for Python and Jupyter renderers):

```python
ec.config(engine="jupyter", adaptive="auto")   # Detect OS dark/light (default)
ec.config(engine="jupyter", adaptive="dark")   # Force dark mode
ec.config(engine="jupyter", adaptive="light")  # Force light mode
```

**Silence layout warnings** when the auto-layout resolver rotates labels or adjusts margins:

```python
ec.config(engine="jupyter", overlap_warnings=False)
```

---

## Chart Types

### Bar Chart

```python
df = pd.DataFrame({
    "Quarter": ["Q1", "Q2", "Q3", "Q4"] * 3,
    "Revenue": [120, 145, 160, 180, 90, 110, 130, 155, 60, 80, 95, 110],
    "Region": ["North"] * 4 + ["South"] * 4 + ["West"] * 4,
})

# Simple bar
fig = ec.figure()
fig.bar(df, x="Quarter", y="Revenue")
fig.show()

# Grouped bar (one group per hue value)
fig = ec.figure()
fig.bar(df, x="Quarter", y="Revenue", hue="Region")
fig.title("Quarterly Revenue by Region")
fig.ylabel("Revenue ($K)")
fig.legend(top=40)
fig.show()

# Stacked bar
fig = ec.figure()
fig.bar(df, x="Quarter", y="Revenue", hue="Region",
        stack=True, labels=True, border_radius=4)
fig.title("Stacked Revenue by Region")
fig.show()

# Gradient bar
fig = ec.figure()
fig.bar(df, x="Quarter", y="Revenue",
        gradient=True, gradient_colors=("#83bff6", "#188df0"),
        labels=True, border_radius=8)
fig.title("Gradient Bars")
fig.show()
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `df` | `DataFrame` | *required* | Source data |
| `x` | `str` | *required* | Category column |
| `y` | `str` | *required* | Value column |
| `hue` | `str` | `None` | Grouping column (one series per value) |
| `stack` | `bool` | `False` | Stack bars |
| `orient` | `"v"` / `"h"` | `"v"` | Vertical or horizontal |
| `bar_width` | `str` | `None` | Bar width (e.g. `"60%"`) |
| `bar_gap` | `str` | `None` | Gap between bars |
| `border_radius` | `int` | `4` | Corner rounding |
| `labels` | `bool` | `False` | Show value labels |
| `label_formatter` | `str` | `"{c}"` | Label format string |
| `label_font_size` | `int` | `12` | Label font size |
| `label_color` | `str` | `"#333"` | Label text color |
| `gradient` | `bool` | `False` | Enable gradient fill |
| `gradient_colors` | `tuple` | `("#83bff6", "#188df0")` | Gradient start/end |
| `agg` | `str` | `"sum"` | Aggregation: `"sum"`, `"mean"`, `"median"`, `"max"`, `"min"`, `"count"` |
| `axis` | `int` | `0` | Y-axis index (0 = left, 1 = right) |
| `emphasis` | `Emphasis` | `None` | Hover effect configuration |

---

### Line Chart

```python
df = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Temperature": [5, 7, 12, 18, 23, 28],
})

# Simple line
fig = ec.figure()
fig.plot(df, x="Month", y="Temperature", smooth=True, labels=True)
fig.title("Monthly Temperature")
fig.ylabel("Temp (C)")
fig.show()
```

Multi-series with hue:

```python
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
df = pd.DataFrame({
    "Month": months * 3,
    "Visitors": [100, 120, 150, 200, 180, 210,
                 80, 95, 120, 160, 140, 170,
                 60, 70, 90, 110, 100, 130],
    "Source": ["Organic"] * 6 + ["Paid"] * 6 + ["Social"] * 6,
})

fig = ec.figure()
fig.plot(df, x="Month", y="Visitors", hue="Source", smooth=True)
fig.title("Traffic by Source")
fig.legend(top=30)
fig.show()
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `df` | `DataFrame` | *required* | Source data |
| `x` | `str` | *required* | Category column |
| `y` | `str` | *required* | Value column |
| `hue` | `str` | `None` | Grouping column |
| `smooth` | `bool` | `False` | Bezier-smooth the line |
| `area` | `bool` | `False` | Fill area under line |
| `area_opacity` | `float` | `0.15` | Area fill opacity |
| `connect_nulls` | `bool` | `False` | Connect across null values |
| `line_width` | `int` | `2` | Line width (px) |
| `symbol_size` | `int` | `6` | Point size |
| `symbol` | `str` | `"circle"` | Point type |
| `labels` | `bool` | `False` | Show value labels |
| `label_position` | `str` | `"top"` | Label placement |
| `label_prefix` | `str` | `""` | Text before label value |
| `label_suffix` | `str` | `""` | Text after label value |
| `agg` | `str` | `"mean"` | Aggregation function |
| `axis` | `int` | `0` | Y-axis index |
| `emphasis` | `LineEmphasis` | `None` | Hover effect |

---

### Scatter Plot

```python
import numpy as np

np.random.seed(42)
n = 80
df = pd.DataFrame({
    "Height": np.random.normal(170, 10, n),
    "Weight": np.random.normal(70, 12, n),
    "Gender": np.random.choice(["Male", "Female"], n),
    "Age": np.random.randint(20, 60, n),
})

fig = ec.figure()
fig.scatter(df, x="Height", y="Weight", color="Gender", size="Age",
            size_range=(5, 30))
fig.title("Height vs Weight")
fig.xlabel("Height (cm)")
fig.ylabel("Weight (kg)")
fig.legend(top=40)
fig.show()
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `df` | `DataFrame` | *required* | Source data |
| `x` | `str` | *required* | X-axis numeric column |
| `y` | `str` | *required* | Y-axis numeric column |
| `color` | `str` | `None` | Grouping column for colors |
| `size` | `str` | `None` | Column for bubble size |
| `size_range` | `tuple` | `(5, 30)` | Min/max symbol size |
| `symbol` | `str` | `"circle"` | Symbol type |
| `opacity` | `float` | `0.7` | Point opacity |
| `labels` | `bool` | `False` | Show labels |
| `emphasis` | `ScatterEmphasis` | `None` | Hover effect |

---

### Pie / Donut Chart

```python
df = pd.DataFrame({
    "Browser": ["Chrome", "Safari", "Firefox", "Edge", "Other"],
    "Share": [65.7, 18.2, 6.3, 5.1, 4.7],
})

# Donut chart
fig = ec.figure()
fig.pie(df, names="Browser", values="Share", inner_radius="40%")
fig.title("Browser Market Share")
fig.show()

# Nightingale rose chart
fig = ec.figure()
fig.pie(df, names="Browser", values="Share",
        inner_radius="30%", outer_radius="75%",
        border_radius=8, rose_type="area")
fig.title("Rose Chart")
fig.show()
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `df` | `DataFrame` | *required* | Source data |
| `names` | `str` | *required* | Category column |
| `values` | `str` | *required* | Value column |
| `inner_radius` | `str` | `None` | Inner radius for donut (e.g. `"40%"`) |
| `outer_radius` | `str` | `"60%"` | Outer radius |
| `radius` | `str / list` | `None` | Shorthand `[inner, outer]` |
| `center` | `list` | `None` | Position as overlay (e.g. `["80%", "25%"]`) |
| `border_radius` | `int` | `0` | Slice corner rounding |
| `start_angle` | `int` | `45` | Starting angle (degrees) |
| `label_inside` | `bool` | `False` | Labels inside slices |
| `label_outside` | `bool` | `True` | Labels outside slices |
| `label_formatter` | `str` | `"{b}: {c} ({d}%)"` | Label format |
| `label_font_size` | `int` | `None` | Label size |
| `rose_type` | `str` | `None` | `"radius"` or `"area"` for rose chart |
| `emphasis` | `PieEmphasis` | `None` | Hover effect |

---

### Histogram

```python
np.random.seed(7)
df = pd.DataFrame({"Score": np.random.normal(72, 15, 500)})

fig = ec.figure()
fig.hist(df, column="Score", bins=20)
fig.title("Exam Score Distribution")
fig.xlabel("Score")
fig.ylabel("Count")
fig.show()
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `df` | `DataFrame` | *required* | Source data |
| `column` | `str` | *required* | Numeric column to bin |
| `bins` | `int` | `10` | Number of bins |
| `density` | `bool` | `False` | Normalize to probability density |
| `bar_color` | `str` | `None` | Override bar color |
| `border_radius` | `int` | `2` | Corner rounding |
| `labels` | `bool` | `False` | Show value labels |

---

### Area Chart

```python
df = pd.DataFrame({
    "Hour": list(range(24)),
    "Users": [12, 8, 5, 3, 4, 8, 25, 60, 95, 120, 110, 105,
              115, 108, 100, 98, 112, 130, 95, 70, 50, 35, 22, 15],
})

fig = ec.figure()
fig.plot(df, x="Hour", y="Users", smooth=True,
         area=True, area_opacity=0.3)
fig.title("Website Traffic - 24hr")
fig.xlabel("Hour of Day")
fig.ylabel("Active Users")
fig.show()
```

---

### Horizontal Bar

```python
df = pd.DataFrame({
    "Language": ["Python", "JavaScript", "TypeScript", "Java", "C#",
                 "C++", "Go", "Rust", "Kotlin", "Swift"],
    "Popularity": [100, 95, 72, 68, 60, 55, 48, 42, 38, 35],
})

fig = ec.figure()
fig.bar(df, x="Language", y="Popularity", orient="h",
        gradient=True, gradient_colors=("#83bff6", "#188df0"))
fig.title("Programming Language Popularity")
fig.show()
```

---

### Radar Chart

```python
indicators = [
    {"name": "Attack", "max": 100},
    {"name": "Defense", "max": 100},
    {"name": "Speed", "max": 100},
    {"name": "Stamina", "max": 100},
    {"name": "Magic", "max": 100},
    {"name": "Intelligence", "max": 100},
]

data = [
    [90, 60, 80, 70, 40, 55],   # Warrior
    [30, 40, 50, 60, 95, 90],   # Mage
    [70, 50, 95, 80, 20, 65],   # Rogue
]

fig = ec.figure(height="500px")
fig.radar(indicators, data, series_names=["Warrior", "Mage", "Rogue"])
fig.title("Character Class Comparison")
fig.show()
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `indicators` | `list[dict]` | *required* | `[{"name": "...", "max": n}, ...]` |
| `data` | `list[list]` | *required* | Data rows, one per series |
| `series_names` | `list[str]` | `None` | Names for each data series |
| `show_labels` | `bool` | `True` | Show value labels |
| `area_opacity` | `float` | `0.15` | Filled area opacity |
| `radius` | `int / str` | `150` | Radar radius |
| `center` | `list` | `None` | Center position |
| `emphasis` | `RadarEmphasis` | `None` | Hover effect |

---

### Heatmap

```python
days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
hours = ["9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm"]

rows = []
for d in days:
    for h in hours:
        rows.append({"Day": d, "Hour": h, "Emails": np.random.randint(2, 50)})

df = pd.DataFrame(rows)

fig = ec.figure()
fig.heatmap(df, x="Hour", y="Day", value="Emails")
fig.title("Emails Received per Hour")
fig.show()
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `df` | `DataFrame` | *required* | Source data |
| `x` | `str` | *required* | X-axis category column |
| `y` | `str` | *required* | Y-axis category column |
| `value` | `str` | *required* | Numeric color column |
| `label_show` | `bool` | `True` | Show cell values |
| `label_formatter` | `str` | `"{c}"` | Label format |
| `visual_min` | `float` | `None` | Min color value |
| `visual_max` | `float` | `None` | Max color value |
| `in_range_colors` | `list[str]` | `None` | Color palette |
| `emphasis` | `Emphasis` | `None` | Hover effect |

---

### Box Plot

```python
np.random.seed(99)
df = pd.DataFrame({
    "Department": np.repeat(["Engineering", "Marketing", "Sales", "Design"], 50),
    "Salary": np.concatenate([
        np.random.normal(120, 20, 50),
        np.random.normal(90, 15, 50),
        np.random.normal(85, 25, 50),
        np.random.normal(95, 18, 50),
    ]),
})

fig = ec.figure()
fig.boxplot(df, x="Department", y="Salary")
fig.title("Salary Distribution by Department")
fig.ylabel("Salary ($K)")
fig.show()
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `df` | `DataFrame` | *required* | Source data |
| `x` | `str` | *required* | Category column |
| `y` | `str` | *required* | Numeric value column |
| `orient` | `"v"` / `"h"` | `"v"` | Orientation |
| `emphasis` | `Emphasis` | `None` | Hover effect |

---

### KDE (Kernel Density)

Requires `scipy`. Install with `pip install echartsy[scipy]`.

```python
df = pd.DataFrame({
    "Velocity": np.concatenate([
        np.random.normal(200, 50, 100),
        np.random.normal(500, 80, 100),
    ]),
    "Type": ["Spiral"] * 100 + ["Elliptical"] * 100,
})

fig = ec.figure()
fig.kde(df, column="Velocity", hue="Type")
fig.title("Galaxy Radial Velocities")
fig.xlabel("Velocity (km/s)")
fig.ylabel("Density")
fig.legend()
fig.show()
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `df` | `DataFrame` | *required* | Source data |
| `column` | `str` | *required* | Numeric column |
| `hue` | `str` | `None` | Grouping column |
| `bandwidth` | `float` | `None` | Kernel bandwidth (auto if `None`) |
| `grid_size` | `int` | `200` | Grid resolution |
| `show_median` | `bool` | `True` | Include median in legend |
| `emphasis` | `LineEmphasis` | `None` | Hover effect |

---

### Funnel Chart

```python
df = pd.DataFrame({
    "Stage": ["Visitors", "Sign-ups", "Trial", "Paid", "Enterprise"],
    "Count": [10000, 3200, 1400, 600, 120],
})

fig = ec.figure()
fig.funnel(df, names="Stage", values="Count")
fig.title("Conversion Funnel")
fig.show()
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `df` | `DataFrame` | *required* | Source data |
| `names` | `str` | *required* | Stage name column |
| `values` | `str` | *required* | Stage value column |
| `sort_order` | `str` | `"descending"` | `"descending"`, `"ascending"`, `"none"` |
| `gap` | `int` | `2` | Gap between segments |
| `label_position` | `str` | `"inside"` | Label placement |
| `label_formatter` | `str` | `"{b}: {c}"` | Label format |
| `emphasis` | `FunnelEmphasis` | `None` | Hover effect |

---

### Treemap

```python
df = pd.DataFrame({
    "Category": ["Electronics"] * 3 + ["Clothing"] * 3 + ["Food"] * 2,
    "SubCategory": ["Phones", "Laptops", "Tablets",
                    "Shirts", "Pants", "Shoes",
                    "Fruit", "Dairy"],
    "Sales": [500, 420, 180, 300, 250, 200, 150, 100],
})

fig = ec.figure(height="500px")
fig.treemap(df, path=["Category", "SubCategory"], value="Sales", roam=False)
fig.title("Sales by Category")
fig.show()
```

Supports deep hierarchies:

```python
fig.treemap(df, path=["Region", "Category", "Sector"], value="Market Cap ($B)")
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `df` | `DataFrame` | *required* | Source data |
| `path` | `list[str]` | *required* | Hierarchy columns (ordered) |
| `value` | `str` | `None` | Numeric column (`None` = count) |
| `leaf_depth` | `int` | `2` | Display depth |
| `roam` | `bool` | `True` | Interactive zoom/pan |
| `gap_width` | `int` | `2` | Gap between rectangles |
| `border_width` | `int` | `1` | Border width |
| `label_formatter` | `str` | `"{b}\n{c}"` | Label format |
| `emphasis` | `TreemapEmphasis` | `None` | Hover effect |

---

### Sankey Diagram

```python
df = pd.DataFrame({
    "Source": ["Organic", "Organic", "Paid", "Paid", "Referral", "Referral"],
    "Channel": ["Landing Page A", "Landing Page B",
                "Landing Page A", "Landing Page B",
                "Landing Page A", "Landing Page B"],
    "Outcome": ["Converted", "Bounced", "Converted", "Bounced",
                "Converted", "Bounced"],
    "Users": [350, 150, 200, 300, 180, 70],
})

fig = ec.figure(height="500px")
fig.sankey(df, levels=["Source", "Channel", "Outcome"], value="Users",
           layout="orthogonal",
           emphasis=ec.SankeyEmphasis(focus="adjacency"))
fig.title("User Flow: Source -> Page -> Outcome")
fig.show()
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `df` | `DataFrame` | *required* | Source data |
| `levels` | `list[str]` | *required* | Ordered flow stage columns (>= 2) |
| `value` | `str` | *required* | Flow magnitude column |
| `node_width` | `int / str` | `20` | Node width |
| `node_gap` | `int` | `8` | Gap between nodes |
| `layout` | `str` | `"none"` | `"none"` or `"orthogonal"` |
| `orient` | `str` | `"horizontal"` | `"horizontal"` or `"vertical"` |
| `emphasis` | `SankeyEmphasis` | `None` | Hover effect (supports `"adjacency"` focus) |

---

### Candlestick Chart

```python
df = pd.DataFrame({
    "Date": ["Mon", "Tue", "Wed", "Thu", "Fri"],
    "Open": [20, 34, 31, 38, 20],
    "Close": [34, 35, 38, 15, 30],
    "Low": [10, 30, 28, 5, 18],
    "High": [38, 50, 44, 42, 35],
})

fig = ec.figure(height="500px")
fig.candlestick(df, date="Date", open="Open", close="Close",
                low="Low", high="High")
fig.title("Weekly Prices")
fig.tooltip()
fig.show()
```

Custom colours:

```python
fig = ec.figure(height="500px")
fig.candlestick(df, date="Date", open="Open", close="Close",
                low="Low", high="High",
                up_color="#00DA3C", down_color="#EC0000",
                up_border="#008F28", down_border="#8A0000")
fig.title("Custom Candlestick Colors")
fig.show()
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `df` | `DataFrame` | *required* | Source data |
| `date` | `str` | *required* | Category axis column (date / label) |
| `open` | `str` | *required* | Opening price column |
| `close` | `str` | *required* | Closing price column |
| `low` | `str` | *required* | Low price column |
| `high` | `str` | *required* | High price column |
| `up_color` | `str` | `"#EE6666"` | Bullish (close > open) body colour |
| `down_color` | `str` | `"#73C0DE"` | Bearish (close < open) body colour |
| `up_border` | `str` | `None` | Bullish border (defaults to `up_color`) |
| `down_border` | `str` | `None` | Bearish border (defaults to `down_color`) |
| `axis` | `int` | `0` | Y-axis index (`0` = left, `1` = right) |
| `emphasis` | `Emphasis` | `None` | Hover effect |

---

## Composite Charts

Combine multiple series on one figure. Mix bar, line, pie, and scatter freely.

### Dual Axis (Bar + Line)

```python
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
fig.show()
```

Use `axis=1` on any series to bind it to the right Y-axis.

---

### Bar + Pie Overlay

Place a pie chart as an inset on a bar chart by passing `center` to `.pie()`:

```python
df = pd.DataFrame({
    "Department": ["Engineering", "Marketing", "Sales", "Design", "Support"],
    "Budget": [450, 280, 320, 180, 120],
})

fig = ec.figure(height="500px")
fig.bar(df, x="Department", y="Budget", gradient=True, labels=True)
fig.pie(df, names="Department", values="Budget",
        center=["82%", "25%"], radius=["18%", "28%"],
        border_radius=4, label_font_size=9)
fig.title("Department Budgets ($K)")
fig.legend(top=40, left=200)
fig.margins(right=120)
fig.show()
```

---

### Triple Composite

```python
df_monthly = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Revenue": [250, 310, 280, 400, 520, 480],
})

df_growth = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Growth": [5.2, 8.1, 6.5, 12.3, 18.7, 15.0],
})

df_mix = pd.DataFrame({
    "Plan": ["Enterprise", "Pro", "Starter", "Free-trial"],
    "Share": [45, 30, 15, 10],
})

fig = ec.figure(height="550px")
fig.bar(df_monthly, x="Month", y="Revenue", labels=True, border_radius=4)
fig.plot(df_growth, x="Month", y="Growth", smooth=True, axis=1,
         line_width=3, symbol_size=8)
fig.pie(df_mix, names="Plan", values="Share",
        center=["25%", "32%"], radius=["15%", "25%"],
        border_radius=4, label_font_size=9)
fig.title("Monthly KPIs: Revenue, Growth & Product Mix")
fig.ylabel("Revenue ($K)")
fig.ylabel_right("Growth %")
fig.legend(top=40, left=350)
fig.show()
```

---

### Side-by-Side Pies

Use `center` to position multiple pies. Add annotations with `.extra()`:

```python
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
        center=["28%", "55%"], radius=["25%", "40%"], border_radius=6)
fig.pie(df_q2, names="Product", values="Revenue",
        center=["72%", "55%"], radius=["25%", "40%"], border_radius=6)
fig.title("Product Mix: Q1 vs Q2")
fig.extra(
    legend={"data": ["Product A", "Product B", "Product C"],
            "top": 40, "left": "center"},
    graphic=[
        {"type": "text", "left": "18%", "top": "88%",
         "style": {"text": "Q1 2025", "fontSize": 14,
                    "fontWeight": "bold", "fill": "#888"}},
        {"type": "text", "left": "62%", "top": "88%",
         "style": {"text": "Q2 2025", "fontSize": 14,
                    "fontWeight": "bold", "fill": "#888"}},
    ],
)
fig.show()
```

---

### Stacked + Trend + Breakdown

```python
df_rev = pd.DataFrame({
    "Quarter": ["Q1", "Q2", "Q3", "Q4"] * 3,
    "Revenue": [120, 145, 160, 180, 90, 110, 130, 155, 60, 80, 95, 110],
    "Region": ["North"] * 4 + ["South"] * 4 + ["West"] * 4,
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
fig.show()
```

---

### Candlestick + Moving Average + Volume

Combine a candlestick chart with a moving-average line and volume bars on a
secondary axis — a common stock-chart layout:

```python
df = pd.DataFrame({
    "Date": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Open": [20, 34, 31, 38, 20, 28],
    "Close": [34, 35, 38, 15, 30, 42],
    "Low": [10, 30, 28, 5, 18, 25],
    "High": [38, 50, 44, 42, 35, 48],
    "Volume": [120, 98, 140, 200, 160, 110],
    "MA5": [28, 32, 34, 30, 26, 33],
})

fig = ec.figure(height="500px")
fig.candlestick(df, date="Date", open="Open", close="Close",
                low="Low", high="High")
fig.plot(df, x="Date", y="MA5", smooth=True, line_width=2)
fig.bar(df, x="Date", y="Volume", axis=1, bar_width="40%")
fig.title("Stock Chart: OHLC + MA + Volume")
fig.ylabel("Price")
fig.ylabel_right("Volume")
fig.legend(top=35)
fig.show()
```

---

## Chart Configuration

All configuration methods return `self` for chaining.

### Titles

```python
fig.title("Main Title")
fig.title("Main Title", subtitle="Optional subtitle")
fig.title("Left-aligned", left="left")
fig.title("With top offset", top=20)
```

### Axes & Ticks

```python
# Axis labels
fig.xlabel("X Label")
fig.xlabel("Rotated", rotate=30, font_size=14, color="#333")
fig.ylabel("Left Y")
fig.ylabel_right("Right Y")

# Axis limits
fig.xlim(0, 100)
fig.ylim(0, 500)
fig.ylim(0, 100, axis=1)  # Right Y-axis

# Tick formatting
fig.xticks(rotate=45)
fig.xticks(interval=2)                  # Show every 2nd label
fig.yticks(formatter="{value} $K")      # Custom format
fig.yticks(rotate=0, axis=1)            # Right Y-axis ticks
```

### Grid & Margins

```python
# Grid lines
fig.grid(show=True)                           # Y-axis grid only (default)
fig.grid(show=True, axis="both")              # Both axes
fig.grid(show=True, axis="x")                 # X-axis only
fig.grid(style="dashed", color="#ddd")         # Dashed grid

# Margins (pixels or CSS strings)
fig.margins(left=100, right=120, top=40, bottom=60)
fig.margins(left="15%", right="15%")
```

### Legend

```python
fig.legend()                                          # Default: top center
fig.legend(show=False)                                # Hide
fig.legend(orient="vertical", left="right", top=40)   # Vertical on right
fig.legend(top=50, left=200)                           # Custom position
```

### Tooltip

```python
fig.tooltip()                                    # Default: axis trigger, cross pointer
fig.tooltip(trigger="item")                      # Item trigger (for pie, scatter)
fig.tooltip(trigger="axis", pointer="shadow")    # Shadow band
fig.tooltip(formatter="{b}: {c}")                # Custom format
fig.tooltip(
    trigger="axis", pointer="cross",
    cross_color="#e74c3c", cross_width=2, cross_type="dashed"
)
```

### Axis Pointer

Fine-grained control over the cursor indicator:

```python
fig.axis_pointer(type="line")           # Vertical line
fig.axis_pointer(type="shadow")         # Shadow band
fig.axis_pointer(type="cross")          # Crosshair
fig.axis_pointer(
    type="shadow", snap=True, label=True,
    shadow_color="rgba(150,150,150,0.15)"
)
```

### Data Zoom

Add a slider to pan/zoom through data:

```python
fig.datazoom()                                 # Horizontal, full range
fig.datazoom(start=0, end=80)                  # Show first 80%
fig.datazoom(orient="vertical")                # Vertical zoom
fig.datazoom(show_slider=False)                # Scroll-only (no slider bar)
```

### Toolbox

Add interactive tools (download, zoom, reset):

```python
fig.toolbox()                                 # Download + Restore
fig.toolbox(download=True, zoom=True)         # Download + Zoom + Restore
fig.toolbox(download=True, zoom=True, restore=True)
```

### Palette

Override the color cycle:

```python
fig.palette(["#667eea", "#764ba2", "#f093fb", "#f5576c", "#4facfe"])
fig.palette(ec.PALETTE_RUSTY)
fig.palette(ec.PALETTE_CLINICAL)
fig.palette(ec.PALETTE_DARK)
```

### Extra Options

Inject any raw ECharts option key. Useful for advanced customization:

```python
fig.extra(
    graphic=[{
        "type": "text", "left": "center", "top": "90%",
        "style": {"text": "Footnote", "fontSize": 12, "fill": "#999"}
    }],
    animationDuration=2000,
)
```

---

## Timeline Animations

`TimelineFigure` creates animated charts with a playback slider. Each unique value in `time_col` becomes one animation frame.

### Animated Bar Chart

```python
np.random.seed(1)
years = ["2020", "2021", "2022", "2023", "2024"]
countries = ["USA", "China", "Germany", "Japan", "India"]

rows = []
for yr in years:
    for c in countries:
        base = {"USA": 21, "China": 15, "Germany": 4, "Japan": 5, "India": 3}[c]
        rows.append({"Year": yr, "Country": c, "GDP": round(base + np.random.uniform(0, 5), 2)})

df = pd.DataFrame(rows)

fig = ec.TimelineFigure(height="500px", interval=1.5)
fig.bar(df, x="Country", y="GDP", time_col="Year", labels=True)
fig.title("GDP by Country")
fig.ylabel("GDP (Trillion USD)")
fig.legend(top=30)
fig.show()
```

### Animated Line Chart

```python
fig = ec.TimelineFigure(height="460px", interval=2.0)
fig.plot(df, x="Continent", y="Population", time_col="Year",
         smooth=True, area=True, area_opacity=0.3,
         line_width=3, symbol_size=8)
fig.title("World Population by Continent")
fig.ylabel("Population (Billions)")
fig.legend(top=40)
fig.show()
```

### Animated Pie Chart

```python
df = pd.DataFrame({
    "Quarter": ["Q1 2024"] * 4 + ["Q2 2024"] * 4 + ["Q3 2024"] * 4,
    "Product": ["Widget A", "Widget B", "Widget C", "Widget D"] * 3,
    "Revenue": [40, 30, 20, 10, 35, 32, 22, 11, 28, 35, 25, 12],
})

fig = ec.TimelineFigure(height="500px", interval=2.0)
fig.pie(df, names="Product", values="Revenue", time_col="Quarter")
fig.title("Product Revenue Share")
fig.legend(top=40)
fig.show()
```

### Animated Scatter Plot

```python
fig = ec.TimelineFigure(height="500px", interval=2.5)
fig.scatter(df, x="Orbital Period", y="Mass", time_col="Era",
            size_range=[5, 20], opacity=0.75)
fig.title("Exoplanet Discoveries")
fig.xlabel("Orbital Period (days)")
fig.ylabel("Mass (Jupiter Masses)")
fig.show()
```

### Animated Histogram

```python
np.random.seed(42)
df = pd.DataFrame({
    "Score": np.concatenate([
        np.random.normal(65, 12, 200),
        np.random.normal(72, 10, 200),
        np.random.normal(78, 8, 200),
    ]),
    "Year": ["2022"] * 200 + ["2023"] * 200 + ["2024"] * 200,
})

fig = ec.TimelineFigure(height="450px", interval=2.0)
fig.hist(df, column="Score", time_col="Year", bins=15, labels=True)
fig.title("Exam Scores Over Time")
fig.ylabel("Count")
fig.show()
```

### Playback Controls

```python
fig = ec.TimelineFigure(
    height="500px",
    interval=1.5,     # Seconds between frames
    autoplay=True,     # Start playing automatically
    loop=True,         # Loop the animation
)

# Or adjust after creation:
fig.playback(interval=2.0, autoplay=False, loop=True, rewind=True)
```

### Supported Time Formats

`TimelineFigure` auto-parses these temporal formats for the `time_col`:

| Format | Examples |
|--------|----------|
| Year | `"2024"` |
| Quarter | `"Q1 2024"`, `"Q1/2024"`, `"2024/Q1"` |
| Month | `"Jan 2024"`, `"January 2024"`, `"2024-01"` |
| Week | `"W1 2024"`, `"W01/2024"` |
| Half-year | `"H1 2024"`, `"H1/2024"` |
| Fiscal year | `"FY 2024"`, `"FY2024"` |
| Day | `"2024-01-15"`, `"2024/1/15"` |

Use `detect_time_format()` to test your column:

```python
from echartsy import detect_time_format
detect_time_format(df["Quarter"])  # Prints format detection results
```

---

## Style Presets

### Built-in Presets

```python
fig = ec.figure(style=ec.StylePreset.CLINICAL)         # Clean defaults
fig = ec.figure(style=ec.StylePreset.DASHBOARD_DARK)    # Dark background
fig = ec.figure(style=ec.StylePreset.KPI_REPORT)        # Warm rusty tones
fig = ec.figure(style=ec.StylePreset.MINIMAL)            # Light and minimal
```

### Custom Presets

```python
my_style = ec.StylePreset(
    palette=("#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51"),
    bg="#fefae0",
    font_family="Georgia",
    title_font_size=20,
    subtitle_font_size=13,
    axis_label_font_size=12,
    axis_label_color="#555",
    grid_line_color="#ddd",
)

fig = ec.figure(style=my_style)
```

**StylePreset attributes:**

| Attribute | Type | Default |
|-----------|------|---------|
| `palette` | `tuple[str, ...]` | `PALETTE_CLINICAL` |
| `bg` | `str / None` | `None` |
| `font_family` | `str` | `"sans-serif"` |
| `title_font_size` | `int` | `16` |
| `subtitle_font_size` | `int` | `12` |
| `axis_label_font_size` | `int` | `12` |
| `axis_label_color` | `str` | `"#666"` |
| `grid_line_color` | `str` | `"#eee"` |
| `tooltip_pointer` | `str` | `"cross"` |
| `legend_orient` | `str` | `"horizontal"` |

### Palettes

Three built-in palettes:

```python
ec.PALETTE_CLINICAL  # ["#5470C6", "#91CC75", "#FAC858", "#EE6666", "#73C0DE", ...]
ec.PALETTE_DARK      # ["#dd6b66", "#759aa0", "#e69d87", "#8dc1a9", "#ea7e53", ...]
ec.PALETTE_RUSTY     # ["#893448", "#d95850", "#eb8146", "#ffb248", "#f2d643", "#ebdba4"]
```

### Dark Theme

Use the ECharts built-in `"dark"` theme:

```python
fig = ec.figure(height="500px", theme="dark", style=ec.StylePreset.DASHBOARD_DARK)
fig.bar(df, x="Quarter", y="Revenue", hue="Region",
        stack=True, border_radius=6)
fig.title("Revenue (Dark Mode)")
fig.toolbox()
fig.show()
```

---

## Emphasis & Hover Effects

Emphasis controls what happens when the user hovers over chart elements. Each chart type has its own emphasis class.

### Bar Emphasis

```python
from echartsy import Emphasis, ItemStyle

fig = ec.figure()
fig.bar(df, x="Month", y="Revenue", hue="Region",
        emphasis=Emphasis(
            focus="series",
            item_style=ItemStyle(shadow_blur=10, shadow_color="rgba(0,0,0,0.3)"),
        ))
fig.show()
```

### Line Emphasis

```python
from echartsy import LineEmphasis, LineStyle, LabelStyle

fig = ec.figure()
fig.plot(df, x="Date", y="Price", hue="Stock",
         emphasis=LineEmphasis(
             focus="series",
             line_style=LineStyle(width=4),
             label=LabelStyle(show=True, formatter="{c}"),
         ))
fig.show()
```

### Pie Emphasis

```python
from echartsy import PieEmphasis, ItemStyle, LabelStyle

fig = ec.figure()
fig.pie(df, names="Category", values="Amount",
        emphasis=PieEmphasis(
            scale=True, scale_size=15,
            item_style=ItemStyle(shadow_blur=20, shadow_color="rgba(0,0,0,0.6)"),
            label=LabelStyle(show=True, font_size=16, font_weight="bold"),
        ))
fig.show()
```

### Scatter Emphasis

```python
from echartsy import ScatterEmphasis

fig = ec.figure()
fig.scatter(df, x="Height", y="Weight",
            emphasis=ScatterEmphasis(scale=True))
fig.show()
```

### Sankey Emphasis

The `"adjacency"` focus mode highlights connected nodes and links:

```python
from echartsy import SankeyEmphasis

fig = ec.figure()
fig.sankey(df, levels=["Source", "Channel", "Outcome"], value="Users",
           emphasis=SankeyEmphasis(focus="adjacency"))
fig.show()
```

### Heatmap Emphasis

```python
from echartsy import Emphasis, ItemStyle

fig = ec.figure()
fig.heatmap(df, x="Day", y="Hour", value="Value",
            emphasis=Emphasis(
                item_style=ItemStyle(border_color="#000", border_width=2, shadow_blur=15),
            ))
fig.show()
```

### Emphasis Shared Parameters

All emphasis classes support:

| Parameter | Type | Description |
|-----------|------|-------------|
| `disabled` | `bool` | Disable emphasis entirely |
| `focus` | `str` | `"none"`, `"self"`, `"series"` (+ `"adjacency"` for Sankey) |
| `blur_scope` | `str` | `"coordinateSystem"`, `"series"`, `"global"` |
| `item_style` | `ItemStyle` | Fill, border, shadow styling |
| `label` | `LabelStyle` | Label visibility, format, font |

**ItemStyle properties:** `color`, `border_color`, `border_width`, `border_radius`, `shadow_blur`, `shadow_color`, `shadow_offset_x`, `shadow_offset_y`, `opacity`

**LabelStyle properties:** `show`, `position`, `formatter`, `font_size`, `font_weight`, `color`

**LineStyle properties:** `color`, `width`, `type` (`"solid"` / `"dashed"` / `"dotted"`), `shadow_blur`, `opacity`

**AreaStyle properties:** `color`, `opacity`

---

## Exporting

### HTML Export

Generate a self-contained HTML file:

```python
fig = ec.figure()
fig.bar(df, x="Fruit", y="Sales")
fig.title("Fruit Sales")

path = fig.to_html("chart.html")
print(f"Saved to: {path}")
```

The file includes the ECharts library from CDN and adaptive dark-mode support.

### Image Export

Add a download button to the chart toolbar:

```python
fig.save(name="my_chart", fmt="png", dpi=3, bg="#ffffff")
fig.save(name="vector_chart", fmt="svg")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | `"chart"` | Downloaded filename |
| `fmt` | `str` | `"png"` | `"png"` or `"svg"` |
| `dpi` | `int` | `3` | Pixel ratio (PNG only) |
| `bg` | `str` | `"#ffffff"` | Background color |

### Raw ECharts Option

Inspect or reuse the generated ECharts configuration:

```python
import json

fig = ec.figure()
fig.bar(df, x="Fruit", y="Sales")
fig.title("Fruit Sales")

option = fig.to_option()
print(json.dumps(option, indent=2))
```

Inject raw ECharts options with `raw_series()`:

```python
fig.raw_series({
    "type": "line",
    "data": [120, 200, 150, 80, 70],
    "markLine": {"data": [{"type": "average", "name": "Avg"}]},
})
```

---

## Streamlit Integration

echartsy renders natively in Streamlit with `st.tabs()` support. Charts persist across tab switches.

```python
import streamlit as st
import pandas as pd
import echartsy as ec

ec.config(engine="streamlit")

tab1, tab2 = st.tabs(["Revenue", "Growth"])

with tab1:
    fig = ec.figure(height="400px")
    fig.bar(df, x="Month", y="Revenue", gradient=True, labels=True)
    fig.title("Monthly Revenue")
    fig.show()

with tab2:
    fig = ec.figure(height="400px")
    fig.plot(df, x="Month", y="Growth", smooth=True, area=True)
    fig.title("Growth Trend")
    fig.show()
```

**Adaptive theming** in Streamlit is opt-in. To auto-detect Streamlit's dark/light theme:

```python
ec.config(engine="streamlit", adaptive="dark")   # Force dark
```

By default (`adaptive="auto"`), Streamlit charts use the standard light theme with no auto-detection.

---

## API Reference

### Figure

```python
ec.Figure(
    height="400px",        # CSS height
    width=None,            # CSS width (None = container)
    renderer="canvas",     # "canvas" or "svg"
    theme=None,            # ECharts theme (e.g. "dark")
    style=None,            # StylePreset instance
    key=None,              # Streamlit widget key (optional)
)
```

**Series methods** (all return `self`):

| Method | Chart Type |
|--------|-----------|
| `.bar(df, x, y, ...)` | Bar (vertical/horizontal, grouped, stacked) |
| `.plot(df, x, y, ...)` | Line (smooth, multi-series, area fill) |
| `.scatter(df, x, y, ...)` | Scatter / Bubble |
| `.pie(df, names, values, ...)` | Pie / Donut / Rose |
| `.hist(df, column, ...)` | Histogram |
| `.kde(df, column, ...)` | Kernel Density Estimation |
| `.boxplot(df, x, y, ...)` | Box-and-whisker |
| `.radar(indicators, data, ...)` | Radar / Spider |
| `.heatmap(df, x, y, value, ...)` | Heatmap matrix |
| `.funnel(df, names, values, ...)` | Funnel / Conversion |
| `.treemap(df, path, value, ...)` | Hierarchical treemap |
| `.sankey(df, levels, value, ...)` | Sankey flow diagram |
| `.candlestick(df, date, open, close, low, high, ...)` | Candlestick / OHLC |
| `.raw_series(config)` | Raw ECharts series dict |

**Configuration methods** (all return `self`):

| Method | Purpose |
|--------|---------|
| `.title(text, subtitle, left, top)` | Chart title |
| `.xlabel(name, rotate, font_size, color)` | X-axis label |
| `.ylabel(name, font_size, color)` | Left Y-axis label |
| `.ylabel_right(name, font_size, color)` | Right Y-axis label |
| `.xlim(min, max)` | X-axis range |
| `.ylim(min, max, axis)` | Y-axis range |
| `.xticks(rotate, interval, formatter)` | X-axis tick format |
| `.yticks(rotate, interval, formatter, axis)` | Y-axis tick format |
| `.grid(show, axis, style, color)` | Grid lines |
| `.margins(left, right, top, bottom)` | Chart margins |
| `.legend(show, orient, left, top, bottom)` | Legend |
| `.tooltip(trigger, pointer, formatter, ...)` | Tooltip behavior |
| `.axis_pointer(type, snap, label, ...)` | Cursor indicator |
| `.palette(colors)` | Color cycle |
| `.datazoom(start, end, orient, show_slider)` | Scroll/zoom slider |
| `.toolbox(download, zoom, restore)` | Interactive tools |
| `.save(name, fmt, dpi, bg)` | Configure download |
| `.extra(**kwargs)` | Inject raw ECharts options |

**Output methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `.show(**render_kw)` | `None` | Render the chart |
| `.to_option()` | `dict` | Raw ECharts option dict |
| `.to_html(filepath)` | `str` | Export to HTML file |

Convenience factory:

```python
ec.figure(height="400px", width=None, renderer="canvas", style=None, **kwargs)
```

---

### TimelineFigure

```python
ec.TimelineFigure(
    height="450px",
    width=None,
    renderer="canvas",
    theme=None,
    style=None,
    key=None,
    interval=2.0,      # Seconds between frames
    autoplay=True,      # Auto-start animation
    loop=True,          # Loop playback
)
```

Supports `.bar()`, `.plot()`, `.scatter()`, `.pie()`, and `.hist()` with the additional required `time_col` parameter. Each unique value in `time_col` becomes one animation frame.

Configuration methods are the same as `Figure`, plus:

| Method | Purpose |
|--------|---------|
| `.playback(interval, autoplay, loop, rewind)` | Adjust playback settings |

Convenience factory:

```python
ec.timeline_figure(height="450px", interval=2.0, autoplay=True, loop=True, **kwargs)
```

---

### StylePreset

Frozen dataclass for visual defaults:

```python
ec.StylePreset(
    palette=("color1", "color2", ...),
    bg=None,
    font_family="sans-serif",
    title_font_size=16,
    subtitle_font_size=12,
    axis_label_font_size=12,
    axis_label_color="#666",
    grid_line_color="#eee",
    tooltip_pointer="cross",
    legend_orient="horizontal",
)
```

Built-in: `StylePreset.CLINICAL`, `StylePreset.DASHBOARD_DARK`, `StylePreset.KPI_REPORT`, `StylePreset.MINIMAL`

---

### Emphasis Classes

| Class | For | Extra attributes |
|-------|-----|-----------------|
| `Emphasis` | Bar, Heatmap, Boxplot | Base class |
| `LineEmphasis` | Line / Plot | `line_style`, `area_style`, `end_label` |
| `ScatterEmphasis` | Scatter | `scale` |
| `PieEmphasis` | Pie / Donut | `scale`, `scale_size`, `label_line` |
| `RadarEmphasis` | Radar | `line_style`, `area_style` |
| `SankeyEmphasis` | Sankey | `line_style`, focus supports `"adjacency"` |
| `FunnelEmphasis` | Funnel | `label_line` |
| `TreemapEmphasis` | Treemap | `label_line`, `upper_label` |

Supporting style classes: `ItemStyle`, `LabelStyle`, `LineStyle`, `AreaStyle`, `LabelLineStyle`

---

### Exceptions

| Exception | When |
|-----------|------|
| `BuilderError` | Base class for all builder errors |
| `BuilderConfigError` | Invalid or contradictory configuration |
| `DataValidationError` | Missing columns or wrong dtypes in DataFrame |
| `TimelineConfigError` | Invalid TimelineFigure configuration |
| `OverlapWarning` | Non-fatal: layout resolver auto-adjusted labels (silenceable) |

---

## Full Example: Dashboard

Putting it all together:

```python
import pandas as pd
import numpy as np
import echartsy as ec

ec.config(engine="jupyter")

np.random.seed(2026)
months = pd.date_range("2024-01", periods=24, freq="MS").strftime("%b %Y").tolist()

df_kpi = pd.DataFrame({
    "Month": months,
    "Revenue": np.cumsum(np.random.normal(50, 15, 24)).clip(100).tolist(),
})

df_margin = pd.DataFrame({
    "Month": months,
    "Margin": np.random.uniform(15, 35, 24).tolist(),
})

fig = ec.figure(height="550px", style=ec.StylePreset.KPI_REPORT)
fig.bar(df_kpi, x="Month", y="Revenue", labels=False, border_radius=4)
fig.plot(df_margin, x="Month", y="Margin", smooth=True, axis=1,
         line_width=3, symbol_size=8)
fig.title("KPI Dashboard: Revenue & Margin", subtitle="Jan 2024 - Dec 2025")
fig.ylabel("Cumulative Revenue ($K)")
fig.ylabel_right("Margin %")
fig.toolbox()
fig.legend(top=50)
fig.datazoom()
fig.margins(top=40)
fig.save(name="kpi_dashboard")
fig.show()
```
