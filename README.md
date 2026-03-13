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

- **Feels like matplotlib** — If you know `plt.figure()` / `plt.show()`, you already know 90% of the API. No JSON wrangling, no JavaScript.
- **Interactive out of the box** — Every chart ships with tooltips, legend toggling, zoom, and a built-in export toolbox.  Zero configuration needed.
- **One library, three engines** — Write once, render in Jupyter notebooks, Streamlit apps, or plain Python scripts that pop open a browser.
- **Composable & animated** — Layer pies on bar charts, build dual-axis dashboards, or animate any chart across time with `TimelineFigure`.

---

## Installation

```bash
pip install echartsy
```

Need extras?

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
<p align="center"><strong>Area Chart</strong></p>
<p align="center"><img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_area.png" alt="Area Chart" width="100%" /></p>

```python
fig = ec.figure()
fig.plot(df, x="Month", y="Users",
         area=True, smooth=True)
fig.show()
```
</td>
<td width="50%">
<p align="center"><strong>Horizontal Bar</strong></p>
<p align="center"><img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_horizontal.png" alt="Horizontal Bar" width="100%" /></p>

```python
fig = ec.figure()
fig.bar(df, x="Country", y="Population",
        orient="h")
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
<p align="center"><strong>Gradient Bars</strong></p>
<p align="center"><img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_gradient.png" alt="Gradient Bars" width="100%" /></p>

```python
fig = ec.figure()
fig.bar(df, x="City", y="Temp",
        gradient=True,
        gradient_colors=["#83bff6","#188df0"])
fig.show()
```
</td>
</tr>
<tr>
<td width="50%">
<p align="center"><strong>Multi-Line with Area</strong></p>
<p align="center"><img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_multiline.png" alt="Multi-Line" width="100%" /></p>

```python
fig = ec.figure()
fig.plot(df, x="Month", y="Value",
         hue="Series", smooth=True,
         area=True)
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
<tr>
<td width="50%">
<p align="center"><strong>Side-by-Side Pies</strong></p>
<p align="center"><img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_sidebyside_pies.png" alt="Side-by-Side Pies" width="100%" /></p>
</td>
<td width="50%">
<p align="center"><strong>Dark Theme</strong></p>
<p align="center"><img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_dark.png" alt="Dark Theme" width="100%" /></p>
</td>
</tr>
</table>

> Every chart is fully interactive — hover for tooltips, click legend items to toggle series, use the toolbox to export.
> Open the [HTML demos in `assets/`](assets/) for the live experience, or run `python generate_demos.py` yourself.

---

## Supported Chart Types

| Category | Method | Description |
|:---|:---|:---|
| **Line** | `fig.plot()` | Smooth/straight lines, multi-series via `hue`, optional filled area |
| **Bar** | `fig.bar()` | Vertical/horizontal, grouped (`hue`), stacked, gradient fills |
| **Scatter** | `fig.scatter()` | Color and size encoding, numeric axes |
| **Histogram** | `fig.hist()` | Auto-binned frequency distribution |
| **Boxplot** | `fig.boxplot()` | Five-number statistical summary |
| **KDE** | `fig.kde()` | Kernel density estimation (requires `scipy`) |
| **Pie / Donut** | `fig.pie()` | Pie, donut (`inner_radius`), rose charts, side-by-side multiples |
| **Radar** | `fig.radar()` | Multi-indicator polygon charts |
| **Heatmap** | `fig.heatmap()` | Matrix visualisation with colour mapping |
| **Sankey** | `fig.sankey()` | Multi-level flow diagrams |
| **Treemap** | `fig.treemap()` | Hierarchical area charts |
| **Funnel** | `fig.funnel()` | Stage-based conversion funnels |

---

## Rendering Engines

echartsy writes your chart once; `ec.config()` controls where it renders.

| Engine | Use case | Install |
|:---|:---|:---|
| `"python"` | Standalone scripts — opens the default browser | No extra deps |
| `"jupyter"` | Jupyter Notebook / JupyterLab inline widgets | `pip install echartsy[jupyter]` |
| `"streamlit"` | Streamlit applications | `pip install echartsy[streamlit]` |

```python
ec.config(engine="jupyter")
```

---

## Adaptive Dark Mode

Charts automatically respond to the user's OS or browser `prefers-color-scheme` setting.

```python
ec.config(engine="jupyter", adaptive="auto")     # auto-detect (default)
ec.config(engine="jupyter", adaptive="dark")     # force dark
ec.config(engine="jupyter", adaptive="light")    # force light
```

---

## Style Presets & Palettes

Apply a pre-built visual theme in one argument:

```python
fig = ec.figure(style=ec.StylePreset.CLINICAL)         # Clean defaults
fig = ec.figure(style=ec.StylePreset.DASHBOARD_DARK)    # Dark background
fig = ec.figure(style=ec.StylePreset.KPI_REPORT)        # Warm rusty tones
fig = ec.figure(style=ec.StylePreset.MINIMAL)            # Minimal & light
```

Or set a custom palette at any time:

```python
fig.palette(["#667eea", "#764ba2", "#f093fb", "#f5576c", "#4facfe"])
fig.palette(ec.PALETTE_RUSTY)
fig.palette(ec.PALETTE_CLINICAL)
```

Build your own `StylePreset` for full control over fonts, grid lines, tooltip style, and more:

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

## Composite Charts

Overlay pies on cartesian charts, or combine bar + line on dual axes — all on one figure.

```python
fig = ec.figure(height="550px")

# Primary axis: bars
fig.bar(df, x="Month", y="Revenue", labels=True, border_radius=4)

# Secondary axis: trend line
fig.plot(df, x="Month", y="Growth", smooth=True, axis=1, line_width=3)

# Inset pie
fig.pie(df_mix, names="Plan", values="Share",
        center=["25%", "32%"], radius=["15%", "25%"])

fig.ylabel("Revenue ($K)")
fig.ylabel_right("Growth %")
fig.legend(top=40, left=350)
fig.show()
```

---

## Timeline Animations

Animate any chart across a time dimension with `TimelineFigure`. It mirrors the `Figure` API; every series method gains one extra parameter: `time_col`.

```python
fig = ec.TimelineFigure(height="500px", interval=1.5)
fig.bar(df, x="Country", y="GDP", time_col="Year", labels=True)
fig.title("GDP by Country")
fig.ylabel("GDP (Trillion USD)")
fig.legend(top=30)
fig.show()
```

<p align="center">
  <img src="https://raw.githubusercontent.com/astrojigs/echartsy/main/assets/demo_timeline.png" alt="Timeline Animation" width="700" />
</p>

**TimelineFigure features:**

| Feature | API |
|:---|:---|
| Playback control | `TimelineFigure(interval=2.0, autoplay=True, loop=True)` |
| Adjust after creation | `fig.playback(interval=1.0, rewind=True)` |
| Smart frame sorting | Parses years, quarters (`Q1 2024`), months (`Jan 2024`), ISO dates, fiscal years |
| Supported series | `bar()`, `plot()`, `scatter()`, `pie()` |
| Diagnose format | `ec.detect_time_format(df["Year"])` |

---

## Chart Configuration Reference

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

# Layout
fig.legend(orient="vertical", left="right", top=40)
fig.margins(left=100, right=120, top=40)
fig.grid(show=True)

# Interactivity
fig.datazoom(start=0, end=80)
fig.toolbox(download=True, zoom=True)
fig.tooltip(trigger="axis")

# Export
fig.save(name="my_chart", fmt="png", dpi=3)
fig.to_html("my_chart.html")

# Palette
fig.palette(["#5470C6", "#91CC75", "#FAC858"])
```

---

## Exporting

```python
# Standalone HTML file (fully interactive, no server needed)
fig.to_html("report.html")

# Raw ECharts option dict (for debugging or custom renderers)
option = fig.to_option()
```

---

## API at a Glance

### `ec.config(engine, adaptive="auto")`

Set the global rendering engine (`"python"`, `"jupyter"`, `"streamlit"`) and theme adaptation mode (`"auto"`, `"light"`, `"dark"`).

### `ec.figure(**kwargs)` / `ec.Figure(**kwargs)`

Create a chart canvas. Key keyword arguments:

| Parameter | Default | Description |
|:---|:---|:---|
| `height` | `"400px"` | CSS height of the chart container |
| `width` | `None` | CSS width (defaults to full container) |
| `renderer` | `"canvas"` | `"canvas"` or `"svg"` |
| `style` | `StylePreset.CLINICAL` | A `StylePreset` instance |

### `ec.TimelineFigure(**kwargs)` / `ec.timeline_figure(**kwargs)`

Same as `Figure` but adds timeline animation. Extra parameters:

| Parameter | Default | Description |
|:---|:---|:---|
| `interval` | `2.0` | Seconds between animation frames |
| `autoplay` | `True` | Start playing automatically |
| `loop` | `True` | Loop back to the first frame |

### `ec.StylePreset`

Frozen dataclass bundling visual defaults: `palette`, `bg`, `font_family`, `title_font_size`, `axis_label_font_size`, `grid_line_color`, and more.

### `ec.detect_time_format(series)`

Diagnostic helper that inspects a pandas Series and reports how well TimelineFigure will parse its values.

---

## Generating Showcase Images

To regenerate the demo screenshots shown above:

```bash
# 1. Generate the interactive HTML demos
python generate_demos.py

# 2. Capture PNG screenshots (requires Playwright)
pip install playwright && playwright install chromium
python capture_screenshots.py
```

---

## Contributing

Contributions, bug reports, and feature requests are welcome. Please open an [issue](https://github.com/astrojigs/echartsy/issues) or submit a pull request on [GitHub](https://github.com/astrojigs/echartsy).

## License

[MIT](LICENSE) &mdash; Jigar, 2026
