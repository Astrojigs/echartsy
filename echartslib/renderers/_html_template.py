"""Shared HTML template for rendering ECharts in a browser or Jupyter."""
from __future__ import annotations

import json
from typing import Optional

# CDN URL for Apache ECharts
ECHARTS_CDN = "https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"


def build_html(
    option: dict,
    height: str = "400px",
    width: str = "100%",
    theme: Optional[str] = None,
    renderer: str = "canvas",
    chart_id: str = "ec_chart",
) -> str:
    """Build a self-contained HTML page that renders an ECharts option dict.

    Parameters
    ----------
    option : dict
        The ECharts option configuration.
    height : str
        CSS height for the chart container.
    width : str
        CSS width for the chart container.
    theme : str or None
        ECharts built-in theme name (e.g. ``"dark"``).
    renderer : str
        ``"canvas"`` or ``"svg"``.
    chart_id : str
        DOM element id for the chart div.

    Returns
    -------
    str
        Complete HTML document string.
    """
    option_json = json.dumps(option, indent=2, default=str)
    theme_arg = f"'{theme}'" if theme else "null"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EChartsLib Chart</title>
<script src="{ECHARTS_CDN}"></script>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
         background: #fafafa; display: flex; justify-content: center;
         align-items: center; min-height: 100vh; padding: 20px; }}
  #{chart_id} {{ width: {width}; height: {height}; background: #fff;
                 border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }}
</style>
</head>
<body>
<div id="{chart_id}"></div>
<script>
  var chart = echarts.init(
    document.getElementById('{chart_id}'),
    {theme_arg},
    {{ renderer: '{renderer}' }}
  );
  var option = {option_json};
  chart.setOption(option);
  window.addEventListener('resize', function() {{ chart.resize(); }});
</script>
</body>
</html>"""


def build_jupyter_html(
    option: dict,
    height: str = "400px",
    width: str = "100%",
    theme: Optional[str] = None,
    renderer: str = "canvas",
    chart_id: str = "ec_chart",
) -> str:
    """Build an HTML fragment suitable for embedding inside a Jupyter IFrame.

    Similar to :func:`build_html` but as a minimal fragment without the
    full page chrome, optimised for ``IPython.display.IFrame``.
    """
    option_json = json.dumps(option, indent=2, default=str)
    theme_arg = f"'{theme}'" if theme else "null"

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<script src="{ECHARTS_CDN}"></script>
<style>
  html, body {{ margin: 0; padding: 0; width: 100%; height: 100%;
               overflow: hidden; background: transparent; }}
  #{chart_id} {{ width: {width}; height: {height}; }}
</style>
</head>
<body>
<div id="{chart_id}"></div>
<script>
  var chart = echarts.init(
    document.getElementById('{chart_id}'),
    {theme_arg},
    {{ renderer: '{renderer}' }}
  );
  var option = {option_json};
  chart.setOption(option);
  window.addEventListener('resize', function() {{ chart.resize(); }});
</script>
</body>
</html>"""
