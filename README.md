<p align="center">
  <img src="https://echarts.apache.org/en/images/logo.png" alt="Apache ECharts" width="70" />
</p>

<h1 align="center">echartsy</h1>

<p align="center">
  <em>Interactive charts in Python — the matplotlib workflow, the ECharts experience.</em>
</p>

<p align="center">
  <a href="https://pypi.org/project/echartsy/"><img src="https://img.shields.io/pypi/v/echartsy?color=%2334d058&label=PyPI" alt="PyPI version" /></a>
  <a href="https://pypi.org/project/echartsy/"><img src="https://img.shields.io/pypi/pyversions/echartsy?color=%2334d058" alt="Python versions" /></a>
  <a href="https://github.com/astrojigs/echartsy/blob/main/LICENSE"><img src="https://img.shields.io/github/license/astrojigs/echartsy?color=blue" alt="License" /></a>
  <a href="https://github.com/astrojigs/echartsy/stargazers"><img src="https://img.shields.io/github/stars/astrojigs/echartsy?style=flat&color=yellow" alt="Stars" /></a>
  <a href="https://github.com/astrojigs/echartsy/issues"><img src="https://img.shields.io/github/issues/astrojigs/echartsy?color=orange" alt="Issues" /></a>
</p>

<p align="center">
  Build publication-quality interactive charts with a familiar<br/>
  <code>fig = figure()</code> &rarr; <code>fig.bar()</code> &rarr; <code>fig.show()</code> workflow.<br/>
  Works everywhere: <b>Jupyter</b> &middot; <b>Streamlit</b> &middot; <b>standalone scripts</b>
</p>

---

## Why echartsy?

| | |
|:---|:---|
| **Familiar API** | If you know `plt.figure()` / `plt.show()`, you already know 90% of the API. No JSON, no JavaScript. |
| **Interactive by default** | Every chart ships with tooltips, legend toggling, zoom, and an export toolbox. Zero config needed. |
| **Three render engines** | Write once, render in Jupyter notebooks, Streamlit apps, or standalone browser windows. |
| **18 chart types** | From bar charts and scatter plots to sankey diagrams, sunbursts, gauges, and network graphs. |
| **Composable & animated** | Layer pies on bar charts, build dual-axis dashboards, use multi-grid subplots, or animate across time with `TimelineFigure`. |
| **Dark mode** | Adaptive dark/light theming out of the box, including automatic Streamlit theme detection. |

---

## Installation

```bash
pip install echartsy
```

Optional extras:

```bash
pip install echartsy[jupyter]     # Jupyter Notebook / JupyterLab
pip install echartsy[streamlit]   # Streamlit apps
pip install echartsy[scipy]       # KDE density plots
pip install echartsy[all]         # Everything
```

> **Requirements:** Python 3.9+ &middot; pandas &ge; 1.5 &middot; numpy &ge; 1.23

---

## Quick Start

```python
import pandas as pd
import echartsy as ec

ec.config(engine="jupyter")          # or "python" / "streamlit"

df = pd.DataFrame({
    "Fruit": ["Apples", "Bananas", "Cherries", "Dates", "Elderberries"],
    "Sales": [120, 95, 78, 42, 63],
})

fig = ec.figure()
fig.bar(df, x="Fruit", y="Sales", gradient=True, labels=True)
fig.title("Fruit Sales")
fig.show()
```

Three lines from DataFrame to interactive chart.

<p align="center">
  <img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_bar.png" alt="Quick Start — Bar Chart" width="600" />
</p>

---

## Chart Types

echartsy v0.5.1 supports **18 chart types** covering cartesian, standalone, hierarchical, relational, and statistical visualizations.

### Cartesian Charts

| Method | Description | Key options |
|:---|:---|:---|
| `fig.plot()` | Line chart | `smooth`, `area`, `hue` (multi-series), dual-axis via `axis=1` |
| `fig.bar()` | Vertical bar | `hue` (grouped), `stack`, `gradient`, `labels`, `border_radius` |
| `fig.barh()` | Horizontal bar | Same as `bar()`, horizontal orientation |
| `fig.scatter()` | Scatter plot | `color` and `size` encoding columns |
| `fig.hist()` | Histogram | `bins`, auto-binned frequency distribution |
| `fig.boxplot()` | Box plot | Five-number statistical summary |
| `fig.kde()` | KDE density | Kernel density estimation (requires `scipy`) |
| `fig.candlestick()` | Candlestick / OHLC | Configurable bullish/bearish colours, composable with `plot()` + `bar()` |
| `fig.heatmap()` | Matrix heatmap | Colour-mapped grid with `visual_map` integration |

### Standalone & Hierarchical Charts

| Method | Description | Key options |
|:---|:---|:---|
| `fig.pie()` | Pie / donut | `inner_radius` (donut), rose mode, side-by-side multiples |
| `fig.radar()` | Radar / spider | Multi-indicator polygon charts |
| `fig.funnel()` | Funnel | Stage-based conversion funnels |
| `fig.gauge()` | Gauge / meter | Speedometer style with colour stops |
| `fig.treemap()` | Treemap | Hierarchical area via `path` columns |
| `fig.sunburst()` | Sunburst | Hierarchical ring chart (same `path` API as treemap) |

### Relational & Calendar Charts

| Method | Description | Key options |
|:---|:---|:---|
| `fig.sankey()` | Sankey diagram | Multi-level flow via `levels` columns |
| `fig.graph()` | Network graph | Force / circular layout, node categories, edge weights |
| `fig.calendar_heatmap()` | Calendar heatmap | GitHub-style contribution grid with auto year detection |

---

## Gallery

### Cartesian Charts

<table>
<tr>
<td width="50%">
<p align="center"><strong>Bar + Pie Overlay</strong></p>
<p align="center"><img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_bar_pie.png" alt="Bar + Pie Overlay" width="100%" /></p>

```python
fig = ec.figure(height="500px")
fig.bar(df, x="Dept", y="Budget",
        gradient=True, labels=True)
fig.pie(df, names="Dept", values="Budget",
        center=["82%","25%"],
        radius=["18%","28%"])
fig.show()
```
</td>
<td width="50%">
<p align="center"><strong>Smooth Line</strong></p>
<p align="center"><img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_line.png" alt="Line Chart" width="100%" /></p>

```python
fig = ec.figure()
fig.plot(df, x="Month", y="Sales",
         smooth=True, area=True)
fig.show()
```
</td>
</tr>
<tr>
<td width="50%">
<p align="center"><strong>Scatter Plot</strong></p>
<p align="center"><img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_scatter.png" alt="Scatter Plot" width="100%" /></p>

```python
fig = ec.figure()
fig.scatter(df, x="Height", y="Weight",
            color="Gender", size="Age")
fig.show()
```
</td>
<td width="50%">
<p align="center"><strong>Grouped Bar</strong></p>
<p align="center"><img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_grouped.png" alt="Grouped Bar" width="100%" /></p>

```python
fig = ec.figure()
fig.bar(df, x="Quarter", y="Revenue",
        hue="Region")
fig.show()
```
</td>
</tr>
<tr>
<td width="50%">
<p align="center"><strong>Stacked Bar</strong></p>
<p align="center"><img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_stacked.png" alt="Stacked Bar" width="100%" /></p>

```python
fig = ec.figure()
fig.bar(df, x="Month", y="Revenue",
        hue="Product", stack=True)
fig.show()
```
</td>
<td width="50%">
<p align="center"><strong>Histogram</strong></p>
<p align="center"><img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_histogram.png" alt="Histogram" width="100%" /></p>

```python
fig = ec.figure()
fig.hist(df, column="Score", bins=20)
fig.show()
```
</td>
</tr>
<tr>
<td width="50%">
<p align="center"><strong>Dual Axis: Bar + Line</strong></p>
<p align="center"><img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_dual.png" alt="Dual Axis" width="100%" /></p>

```python
fig = ec.figure()
fig.bar(df, x="Month", y="Revenue")
fig.plot(df, x="Month", y="Growth",
         smooth=True, axis=1)
fig.ylabel("Revenue ($K)")
fig.ylabel_right("Growth %")
fig.show()
```
</td>
<td width="50%">
<p align="center"><strong>Boxplot</strong></p>
<p align="center"><img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_boxplot.png" alt="Boxplot" width="100%" /></p>

```python
fig = ec.figure()
fig.boxplot(df, x="Department", y="Salary")
fig.show()
```
</td>
</tr>
</table>

### Standalone Charts

<table>
<tr>
<td width="50%">
<p align="center"><strong>Donut / Pie</strong></p>
<p align="center"><img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_pie.png" alt="Donut Chart" width="100%" /></p>

```python
fig = ec.figure()
fig.pie(df, names="Browser", values="Share",
        inner_radius="40%")
fig.show()
```
</td>
<td width="50%">
<p align="center"><strong>Radar</strong></p>
<p align="center"><img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_radar.png" alt="Radar Chart" width="100%" /></p>

```python
fig = ec.figure()
fig.radar(indicators, data,
          series_names=["Warrior","Mage"])
fig.show()
```
</td>
</tr>
<tr>
<td width="50%">
<p align="center"><strong>Heatmap</strong></p>
<p align="center"><img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_heatmap.png" alt="Heatmap" width="100%" /></p>

```python
fig = ec.figure()
fig.heatmap(df, x="Day", y="Hour",
            value="Count")
fig.show()
```
</td>
<td width="50%">
<p align="center"><strong>Funnel</strong></p>
<p align="center"><img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_funnel.png" alt="Funnel" width="100%" /></p>

```python
fig = ec.figure()
fig.funnel(df, names="Stage", values="Count")
fig.show()
```
</td>
</tr>
<tr>
<td width="50%">
<p align="center"><strong>Treemap</strong></p>
<p align="center"><img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_treemap.png" alt="Treemap" width="100%" /></p>

```python
fig = ec.figure()
fig.treemap(df,
    path=["Category","SubCat"],
    value="Sales")
fig.show()
```
</td>
<td width="50%">
<p align="center"><strong>Sankey Diagram</strong></p>
<p align="center"><img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_sankey.png" alt="Sankey Diagram" width="100%" /></p>

```python
fig = ec.figure()
fig.sankey(df,
    levels=["Source","Channel","Outcome"],
    value="Users")
fig.show()
```
</td>
</tr>
</table>

### Composite & Dashboard Charts

<table>
<tr>
<td width="50%">
<p align="center"><strong>Bar + Pie (Dark)</strong></p>
<p align="center"><img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_composite_dark.png" alt="Composite Dark" width="100%" /></p>
</td>
<td width="50%">
<p align="center"><strong>Triple Composite</strong></p>
<p align="center"><img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_composite.png" alt="Triple Composite" width="100%" /></p>
</td>
</tr>
<tr>
<td width="50%">
<p align="center"><strong>KPI Dashboard</strong></p>
<p align="center"><img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_dashboard.png" alt="KPI Dashboard" width="100%" /></p>
</td>
<td width="50%">
<p align="center"><strong>Stacked + Trend + Pie</strong></p>
<p align="center"><img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_full_dashboard.png" alt="Full Dashboard" width="100%" /></p>
</td>
</tr>
</table>

> Every chart is fully interactive -- hover for tooltips, click legend items to toggle series, use the toolbox to export.
> Open the [HTML demos in `assets/`](assets/) for the live experience, or run `python generate_demos.py` yourself.

---

## Rendering Engines

Write your chart once; `ec.config()` controls where it renders.

| Engine | Use case | Install |
|:---|:---|:---|
| `"python"` | Standalone scripts -- opens the default browser | No extra deps |
| `"jupyter"` | Jupyter Notebook / JupyterLab inline widgets | `pip install echartsy[jupyter]` |
| `"streamlit"` | Streamlit applications | `pip install echartsy[streamlit]` |

```python
ec.config(engine="jupyter")          # or "python" / "streamlit"
```

---

## Advanced Features

### Multi-Grid Subplots

Create vertically stacked chart panels sharing independent axes:

```python
fig = ec.figure(rows=2, height="700px", row_heights=["60%", "40%"])
fig.bar(df, x="Month", y="Revenue", grid=0)
fig.plot(df, x="Month", y="Growth", grid=1, smooth=True)
fig.show()
```

### Timeline Animations

Animate any chart across a time dimension with `TimelineFigure`:

```python
fig = ec.TimelineFigure(height="500px", interval=1.5)
fig.bar(df, x="Country", y="GDP", time_col="Year", labels=True)
fig.title("GDP by Country")
fig.show()
```

<p align="center">
  <img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_timeline.png" alt="Timeline Animation" width="700" />
</p>

| Feature | API |
|:---|:---|
| Playback control | `TimelineFigure(interval=2.0, autoplay=True, loop=True)` |
| Adjust after creation | `fig.playback(interval=1.0, rewind=True)` |
| Fixed axis ranges | `fig.xlim()`, `fig.ylim()` -- consistent scales across frames |
| Smart frame sorting | Parses years, quarters (`Q1 2024`), months, ISO dates, fiscal years |
| Supported series | `bar()`, `plot()`, `scatter()`, `pie()`, `hist()` |
| Diagnose format | `ec.detect_time_format(df["Year"])` |

### Annotations

Add reference lines, points, and shaded regions to any series:

```python
fig.plot(df, x="Month", y="Sales", smooth=True)
fig.mark_line(y=500, label="Target", color="red", line_dash="dashed")
fig.mark_point(type="max")
fig.mark_area(y_range=[200, 400], color="#ccc", opacity=0.15)
fig.show()
```

### Visual Map

Attach a colour-mapping control for continuous or piecewise data ranges:

```python
fig.heatmap(df, x="Day", y="Hour", value="Count")
fig.visual_map(min_val=0, max_val=100,
               colors=["#313695", "#ffffbf", "#a50026"],
               calculable=True)
fig.show()
```

### Log Scale

Switch any y-axis to logarithmic scale:

```python
fig.yscale("log")          # shorthand
fig.ylim(scale="log")      # equivalent
```

### Emphasis (Hover Highlighting)

Control what happens when users hover over chart elements using typed Python dataclasses:

```python
from echartsy import Emphasis, ItemStyle

fig.bar(df, x="Month", y="Revenue", hue="Region",
        emphasis=Emphasis(
            focus="series",
            item_style=ItemStyle(shadow_blur=10),
        ))
```

Every chart method accepts an optional `emphasis` parameter with a chart-specific type:

| Chart method | Emphasis class |
|:---|:---|
| `bar()`, `hist()`, `boxplot()`, `heatmap()`, `candlestick()` | `Emphasis` |
| `plot()`, `kde()` | `LineEmphasis` |
| `scatter()` | `ScatterEmphasis` |
| `pie()` | `PieEmphasis` |
| `radar()` | `RadarEmphasis` |
| `sankey()` | `SankeyEmphasis` |
| `funnel()` | `FunnelEmphasis` |
| `treemap()` | `TreemapEmphasis` |
| `graph()` | `GraphEmphasis` |

### Adaptive Dark Mode

Charts automatically respond to the user's OS or browser `prefers-color-scheme` setting:

```python
ec.config(engine="jupyter", adaptive="auto")     # auto-detect (default)
ec.config(engine="jupyter", adaptive="dark")     # force dark
ec.config(engine="streamlit")                    # auto-adapts to Streamlit theme
```

### Style Presets and Palettes

Apply a pre-built visual theme or set custom colour palettes:

```python
fig = ec.figure(style=ec.StylePreset.CLINICAL)
fig = ec.figure(style=ec.StylePreset.DASHBOARD_DARK)
fig = ec.figure(style=ec.StylePreset.KPI_REPORT)
fig = ec.figure(style=ec.StylePreset.MINIMAL)

fig.palette(["#667eea", "#764ba2", "#f093fb", "#f5576c", "#4facfe"])
fig.palette(ec.PALETTE_RUSTY)
```

Build custom presets for full control over fonts, grid lines, tooltip style, and more:

```python
my_style = ec.StylePreset(
    palette=("#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51"),
    bg="#fefae0",
    font_family="Georgia",
    title_font_size=20,
)
fig = ec.figure(style=my_style)
```

---

## Configuration Reference

Every `Figure` and `TimelineFigure` supports these configuration methods:

```python
# Titles
fig.title("Main Title", subtitle="Sub-title")

# Axes
fig.xlabel("X Label", rotate=30)
fig.ylabel("Y Label")
fig.ylabel_right("Secondary Y")
fig.xlim(0, 100)
fig.ylim(0, 500)
fig.yscale("log")

# Layout
fig.legend(orient="vertical", left="right", top=40)
fig.margins(left=100, right=120, top=40)
fig.grid(show=True)

# Interactivity
fig.datazoom(start=0, end=80)
fig.toolbox(download=True, zoom=True)
fig.tooltip(trigger="axis", pointer="cross")
fig.axis_pointer(type="shadow", snap=True)
fig.visual_map(min_val=0, max_val=100)

# Export
fig.save(name="my_chart", fmt="png", dpi=3)
fig.to_html("my_chart.html")
option = fig.to_option()       # raw ECharts option dict

# Palette
fig.palette(["#5470C6", "#91CC75", "#FAC858"])
```

---

## API at a Glance

### `ec.config(engine, adaptive="auto")`

Set the global rendering engine (`"python"`, `"jupyter"`, `"streamlit"`) and theme adaptation mode (`"auto"`, `"light"`, `"dark"`).

### `ec.figure(**kwargs)` / `ec.Figure(**kwargs)`

Create a chart canvas.

| Parameter | Default | Description |
|:---|:---|:---|
| `height` | `"400px"` | CSS height of the chart container |
| `width` | `None` | CSS width (defaults to full container) |
| `renderer` | `"svg"` | `"canvas"` or `"svg"` |
| `style` | `StylePreset.CLINICAL` | A `StylePreset` instance |
| `rows` | `1` | Number of vertical grid panels (subplots) |
| `row_heights` | `None` | List of CSS heights per grid panel |

### `ec.TimelineFigure(**kwargs)` / `ec.timeline_figure(**kwargs)`

Same as `Figure` but adds timeline animation. Extra parameters:

| Parameter | Default | Description |
|:---|:---|:---|
| `interval` | `2.0` | Seconds between animation frames |
| `autoplay` | `True` | Start playing automatically |
| `loop` | `True` | Loop back to the first frame |

### Sub-style Dataclasses

| Class | Key fields |
|:---|:---|
| `ec.ItemStyle` | `color`, `border_color`, `border_width`, `border_radius`, `shadow_blur`, `shadow_color`, `opacity` |
| `ec.LabelStyle` | `show`, `position`, `formatter`, `font_size`, `font_weight`, `color` |
| `ec.LineStyle` | `color`, `width`, `type` (`"solid"` / `"dashed"` / `"dotted"`), `shadow_blur`, `opacity` |
| `ec.AreaStyle` | `color`, `opacity` |
| `ec.LabelLineStyle` | `show`, `length`, `length2` |

---

## Changelog (Recent)

### v0.5.1

Current release. See [Releases](https://github.com/astrojigs/echartsy/releases) for full details.

### v0.4.8

- **Changed:** Default renderer switched from `"canvas"` to `"svg"` -- fixes the broken toolbox download button under canvas/iframe sandbox restrictions.

### v0.4.7

- **Added:** `fig.candlestick()` -- native OHLC candlestick charts with dual-axis support and full composability.

### v0.4.6

- **Added:** `Emphasis` support for `boxplot()`, `heatmap()`, and `funnel()`.

### v0.4.5

- **Fixed:** Charts vanishing across `st.tabs()` in Streamlit 1.48+.

---

## Support the Project

If echartsy saves you time or you enjoy using it, consider buying me a coffee. It helps keep the project maintained and growing.

<p align="center">
  <a href="https://www.buymeacoffee.com/astrojigs2a" target="_blank">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="50" width="200" />
  </a>
</p>

---

## Contributing

Contributions, bug reports, and feature requests are welcome. Please open an [issue](https://github.com/astrojigs/echartsy/issues) or submit a pull request on [GitHub](https://github.com/astrojigs/echartsy).

## License

[MIT](LICENSE) &mdash; Jigar, 2026
