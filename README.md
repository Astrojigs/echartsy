# echartslib

A matplotlib-style fluent builder API for [Apache ECharts](https://echarts.apache.org/) in Python.

Build interactive, publication-quality charts with a familiar `fig = figure()` → `fig.bar()` → `fig.show()` workflow. Works in Jupyter Notebooks, Streamlit apps, and standalone Python scripts.

## Installation

```bash
pip install echartslib
```

With optional extras:

```bash
pip install echartslib[jupyter]     # Jupyter Notebook support
pip install echartslib[streamlit]   # Streamlit support
pip install echartslib[scipy]       # KDE plots
pip install echartslib[all]         # Everything
```

## Quick Start

```python
import pandas as pd
import echartslib as ec

ec.config(engine="jupyter")  # or "python" or "streamlit"

df = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
    "Revenue": [120, 200, 150, 300, 250],
})

fig = ec.figure(height="400px")
fig.bar(df, x="Month", y="Revenue", border_radius=6, gradient=True)
fig.title("Monthly Revenue")
fig.ylabel("Revenue ($K)")
fig.show()
```

## Rendering Engines

| Engine | Use case | Setup |
|---|---|---|
| `"jupyter"` | Jupyter Notebook / JupyterLab | `pip install echartslib[jupyter]` |
| `"python"` | Standalone scripts (opens browser) | No extra deps |
| `"streamlit"` | Streamlit applications | `pip install echartslib[streamlit]` |

```python
ec.config(engine="jupyter")
ec.config(engine="jupyter", adaptive="dark")  # Force dark mode
```

## Supported Chart Types

### Cartesian Charts
- **Bar** — `fig.bar(df, x, y, hue=, stack=, orient="h", gradient=True)`
- **Line** — `fig.plot(df, x, y, hue=, smooth=True, area=True)`
- **Scatter** — `fig.scatter(df, x, y, color=, size=)`
- **Histogram** — `fig.hist(df, column=, bins=10)`
- **Boxplot** — `fig.boxplot(df, x, y)`
- **KDE** — `fig.kde(df, column=, hue=)` *(requires scipy)*

### Standalone Charts
- **Pie / Donut** — `fig.pie(df, names, values, inner_radius="30%")`
- **Radar** — `fig.radar(indicators, data)`
- **Heatmap** — `fig.heatmap(df, x, y, value)`
- **Sankey** — `fig.sankey(df, levels=["src", "tgt"], value="flow")`
- **Treemap** — `fig.treemap(df, path=["group", "item"], value="count")`
- **Funnel** — `fig.funnel(df, names, values)`

### Composite Charts
Overlay a pie chart on a bar/line figure without raw ECharts JSON:

```python
fig = ec.figure(height="500px")
fig.bar(df, x="Dept", y="Budget", gradient=True)
fig.pie(df, names="Dept", values="Budget",
        center=["82%", "25%"], radius=["18%", "28%"],
        label_font_size=9)
fig.show()
```

### Timeline Animations

```python
fig = ec.TimelineFigure(height="500px", interval=1.5)
fig.bar(df, x="Country", y="GDP", time_col="Year")
fig.title("GDP by Year")
fig.show()
```

## Dual-Axis Charts

```python
fig = ec.figure()
fig.bar(df, x="Month", y="Revenue")
fig.plot(df, x="Month", y="Growth", axis=1, smooth=True)
fig.ylabel("Revenue ($K)")
fig.ylabel_right("Growth (%)")
fig.show()
```

## Style Presets

```python
fig = ec.figure(style=ec.StylePreset.CLINICAL)        # Default
fig = ec.figure(style=ec.StylePreset.DASHBOARD_DARK)   # Dark theme
fig = ec.figure(style=ec.StylePreset.KPI_REPORT)       # Warm tones
fig = ec.figure(style=ec.StylePreset.MINIMAL)           # Clean & simple
```

Or create a custom palette:

```python
fig = ec.figure()
fig.palette(["#e74c3c", "#3498db", "#2ecc71", "#f39c12"])
```

## Chrome Configuration

```python
fig.title("Chart Title", subtitle="Optional subtitle")
fig.xlabel("X Label", rotate=30)
fig.ylabel("Y Label")
fig.legend(orient="vertical", left="right")
fig.margins(left=100, right=120)
fig.datazoom(start=0, end=80)
fig.toolbox(download=True, zoom=True)
fig.save(name="my_chart", fmt="png", dpi=3)
```

## Exporting

```python
# HTML file
fig.to_html("my_chart.html")

# Raw ECharts option dict (for debugging or custom renderers)
option = fig.to_option()
```

## Adaptive Dark Mode

Charts automatically adapt to the user's OS dark/light mode preference. Control this with:

```python
ec.config(engine="jupyter", adaptive="auto")   # Auto-detect (default)
ec.config(engine="jupyter", adaptive="dark")   # Force dark
ec.config(engine="jupyter", adaptive="light")  # Force light
```

## License

MIT
