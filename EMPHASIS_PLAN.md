# Emphasis Feature — Architectural Plan

## 1. Problem Statement

Today, emphasis behavior in echartsy is either hardcoded (pie gets a shadow on hover, heatmap gets a shadow) or requires passing a raw dictionary via `**series_kw` / the `emphasis` parameter (only sankey currently exposes this). There is no consistent, Pythonic, attribute-based API for configuring emphasis across chart types.

**Goal:** Expose emphasis as typed dataclass attributes on every chart method — matching the existing `StylePreset` pattern — so users never need to pass raw ECharts dicts for common emphasis configurations.

---

## 2. ECharts Emphasis — What Each Chart Type Supports

Every ECharts series type supports an `emphasis` object with these **common** keys:

| Key | Type | Description |
|-----|------|-------------|
| `disabled` | `bool` | Turn off hover highlighting entirely |
| `focus` | `"none"` \| `"self"` \| `"series"` \| `"adjacency"` | What to highlight on hover |
| `blurScope` | `"coordinateSystem"` \| `"series"` \| `"global"` | What to dim when focus is active |

Beyond that, each chart type supports a **unique mix** of style sub-objects:

| Chart Type | `itemStyle` | `label` | `lineStyle` | `areaStyle` | `labelLine` | `endLabel` | `scale` / `scaleSize` |
|------------|:-----------:|:-------:|:-----------:|:-----------:|:-----------:|:----------:|:---------------------:|
| **bar** | ✓ | ✓ | — | — | — | — | — |
| **line** | ✓ | ✓ | ✓ | ✓ | — | ✓ | — |
| **scatter** | ✓ | ✓ | — | — | — | — | `scale` (bool) |
| **pie** | ✓ | ✓ | — | — | ✓ | — | `scale` + `scaleSize` |
| **radar** | ✓ | ✓ | ✓ | ✓ | — | — | — |
| **heatmap** | ✓ | ✓ | — | — | — | — | — |
| **treemap** | ✓ | ✓ | — | — | ✓ | — | — |
| **funnel** | ✓ | ✓ | — | — | ✓ | — | — |
| **sankey** | ✓ | ✓ | ✓ | — | — | — | focus supports `"adjacency"` |
| **boxplot** | ✓ | ✓ | — | — | — | — | — |
| **hist** | ✓ | ✓ | — | — | — | — | — |
| **kde** | ✓ | ✓ | ✓ | ✓ | — | — | — |

---

## 3. Architecture — Dataclass Hierarchy

### 3.1 Design Principles

1. **Attribute-based, not dict-based** — users set named Python attributes, not nested dicts.
2. **Frozen dataclasses** — immutable, consistent with `StylePreset`.
3. **Hierarchy via composition** — a base class holds common fields; chart-specific classes add their unique fields.
4. **`None` means "use ECharts default"** — only non-`None` values are emitted into the final config dict.
5. **`.to_dict()` method** — each dataclass knows how to serialize itself to an ECharts-compatible dict.

### 3.2 Class Design

All classes live in a new file: **`echartsy/emphasis.py`**

```python
# echartsy/emphasis.py
from __future__ import annotations
from dataclasses import dataclass, fields
from typing import Optional, Literal

# ── Shared sub-style dataclasses ──────────────────────────────────────

@dataclass(frozen=True)
class ItemStyle:
    """Emphasis item style — colors, borders, shadows."""
    color: Optional[str] = None
    border_color: Optional[str] = None
    border_width: Optional[int] = None
    border_radius: Optional[int] = None
    shadow_blur: Optional[int] = None
    shadow_color: Optional[str] = None
    shadow_offset_x: Optional[int] = None
    shadow_offset_y: Optional[int] = None
    opacity: Optional[float] = None

    def to_dict(self) -> dict:
        mapping = {
            "color": "color", "border_color": "borderColor",
            "border_width": "borderWidth", "border_radius": "borderRadius",
            "shadow_blur": "shadowBlur", "shadow_color": "shadowColor",
            "shadow_offset_x": "shadowOffsetX", "shadow_offset_y": "shadowOffsetY",
            "opacity": "opacity",
        }
        return {mapping[f.name]: getattr(self, f.name)
                for f in fields(self) if getattr(self, f.name) is not None}


@dataclass(frozen=True)
class LabelStyle:
    """Emphasis label style."""
    show: Optional[bool] = None
    position: Optional[str] = None
    formatter: Optional[str] = None
    font_size: Optional[int] = None
    font_weight: Optional[str] = None
    color: Optional[str] = None

    def to_dict(self) -> dict:
        mapping = {
            "show": "show", "position": "position", "formatter": "formatter",
            "font_size": "fontSize", "font_weight": "fontWeight", "color": "color",
        }
        return {mapping[f.name]: getattr(self, f.name)
                for f in fields(self) if getattr(self, f.name) is not None}


@dataclass(frozen=True)
class LineStyle:
    """Emphasis line style (for line, radar, sankey)."""
    color: Optional[str] = None
    width: Optional[int] = None
    type: Optional[Literal["solid", "dashed", "dotted"]] = None
    shadow_blur: Optional[int] = None
    opacity: Optional[float] = None

    def to_dict(self) -> dict:
        mapping = {
            "color": "color", "width": "width", "type": "type",
            "shadow_blur": "shadowBlur", "opacity": "opacity",
        }
        return {mapping[f.name]: getattr(self, f.name)
                for f in fields(self) if getattr(self, f.name) is not None}


@dataclass(frozen=True)
class AreaStyle:
    """Emphasis area style (for line, radar)."""
    color: Optional[str] = None
    opacity: Optional[float] = None

    def to_dict(self) -> dict:
        return {k: v for k, v in [("color", self.color), ("opacity", self.opacity)] if v is not None}


@dataclass(frozen=True)
class LabelLineStyle:
    """Emphasis label line (for pie, funnel, treemap)."""
    show: Optional[bool] = None
    length: Optional[int] = None
    length2: Optional[int] = None

    def to_dict(self) -> dict:
        return {k: v for k, v in [("show", self.show), ("length", self.length), ("length2", self.length2)]
                if v is not None}
```

### 3.3 Chart-Specific Emphasis Dataclasses

```python
# ── Base emphasis (shared by ALL chart types) ─────────────────────────

@dataclass(frozen=True)
class Emphasis:
    """Base emphasis config — works for bar, heatmap, boxplot, hist."""
    disabled: Optional[bool] = None
    focus: Optional[Literal["none", "self", "series"]] = None
    blur_scope: Optional[Literal["coordinateSystem", "series", "global"]] = None
    item_style: Optional[ItemStyle] = None
    label: Optional[LabelStyle] = None

    def to_dict(self) -> dict:
        d: dict = {}
        if self.disabled is not None:
            d["disabled"] = self.disabled
        if self.focus is not None:
            d["focus"] = self.focus
        if self.blur_scope is not None:
            d["blurScope"] = self.blur_scope
        if self.item_style is not None:
            d["itemStyle"] = self.item_style.to_dict()
        if self.label is not None:
            d["label"] = self.label.to_dict()
        return d


@dataclass(frozen=True)
class LineEmphasis(Emphasis):
    """Emphasis for line/kde charts — adds lineStyle, areaStyle, endLabel."""
    line_style: Optional[LineStyle] = None
    area_style: Optional[AreaStyle] = None
    end_label: Optional[LabelStyle] = None

    def to_dict(self) -> dict:
        d = super().to_dict()
        if self.line_style is not None:
            d["lineStyle"] = self.line_style.to_dict()
        if self.area_style is not None:
            d["areaStyle"] = self.area_style.to_dict()
        if self.end_label is not None:
            d["endLabel"] = self.end_label.to_dict()
        return d


@dataclass(frozen=True)
class ScatterEmphasis(Emphasis):
    """Emphasis for scatter — adds scale."""
    scale: Optional[bool] = None

    def to_dict(self) -> dict:
        d = super().to_dict()
        if self.scale is not None:
            d["scale"] = self.scale
        return d


@dataclass(frozen=True)
class PieEmphasis(Emphasis):
    """Emphasis for pie/donut — adds scale, scaleSize, labelLine."""
    scale: Optional[bool] = None
    scale_size: Optional[int] = None
    label_line: Optional[LabelLineStyle] = None

    def to_dict(self) -> dict:
        d = super().to_dict()
        if self.scale is not None:
            d["scale"] = self.scale
        if self.scale_size is not None:
            d["scaleSize"] = self.scale_size
        if self.label_line is not None:
            d["labelLine"] = self.label_line.to_dict()
        return d


@dataclass(frozen=True)
class RadarEmphasis(Emphasis):
    """Emphasis for radar — adds lineStyle and areaStyle."""
    line_style: Optional[LineStyle] = None
    area_style: Optional[AreaStyle] = None

    def to_dict(self) -> dict:
        d = super().to_dict()
        if self.line_style is not None:
            d["lineStyle"] = self.line_style.to_dict()
        if self.area_style is not None:
            d["areaStyle"] = self.area_style.to_dict()
        return d


@dataclass(frozen=True)
class SankeyEmphasis(Emphasis):
    """Emphasis for sankey — focus supports 'adjacency'."""
    focus: Optional[Literal["none", "self", "series", "adjacency"]] = None
    line_style: Optional[LineStyle] = None

    def to_dict(self) -> dict:
        d = super().to_dict()
        if self.line_style is not None:
            d["lineStyle"] = self.line_style.to_dict()
        return d


@dataclass(frozen=True)
class FunnelEmphasis(Emphasis):
    """Emphasis for funnel — adds labelLine."""
    label_line: Optional[LabelLineStyle] = None

    def to_dict(self) -> dict:
        d = super().to_dict()
        if self.label_line is not None:
            d["labelLine"] = self.label_line.to_dict()
        return d


@dataclass(frozen=True)
class TreemapEmphasis(Emphasis):
    """Emphasis for treemap — adds labelLine and upperLabel."""
    label_line: Optional[LabelLineStyle] = None
    upper_label: Optional[LabelStyle] = None

    def to_dict(self) -> dict:
        d = super().to_dict()
        if self.label_line is not None:
            d["labelLine"] = self.label_line.to_dict()
        if self.upper_label is not None:
            d["upperLabel"] = self.upper_label.to_dict()
        return d
```

---

## 4. Integration into Figure Methods

### 4.1 Method Signature Changes

Each chart method gains an `emphasis` keyword parameter typed to its specific class. `None` means the current hardcoded defaults are used (backward compatible).

| Method | New Parameter | Type |
|--------|--------------|------|
| `plot()` | `emphasis=None` | `Optional[LineEmphasis]` |
| `bar()` | `emphasis=None` | `Optional[Emphasis]` |
| `scatter()` | `emphasis=None` | `Optional[ScatterEmphasis]` |
| `pie()` | `emphasis=None` | `Optional[PieEmphasis]` |
| `hist()` | `emphasis=None` | `Optional[Emphasis]` |
| `radar()` | `emphasis=None` | `Optional[RadarEmphasis]` |
| `kde()` | `emphasis=None` | `Optional[LineEmphasis]` |
| `heatmap()` | `emphasis=None` | `Optional[Emphasis]` |
| `sankey()` | `emphasis=None` | `Optional[SankeyEmphasis]` (replaces current `dict`) |
| `treemap()` | `emphasis=None` | `Optional[TreemapEmphasis]` |
| `funnel()` | `emphasis=None` | `Optional[FunnelEmphasis]` |
| `boxplot()` | `emphasis=None` | `Optional[Emphasis]` |

### 4.2 Integration Pattern (same for every method)

The pattern is identical across all chart methods — insert these lines right before `entry.update(series_kw)`:

```python
# In bar(), for example:
def bar(self, df, x, y, *, ..., emphasis: Optional[Emphasis] = None, **series_kw):
    ...
    base: dict = { "type": "bar", ... }

    # ── NEW: emphasis injection ──
    if emphasis is not None:
        base["emphasis"] = emphasis.to_dict()

    base.update(series_kw)   # series_kw can still override if needed
    ...
```

### 4.3 Backward Compatibility for Pie and Heatmap

Pie and heatmap currently have hardcoded emphasis. The plan preserves these as **defaults** that the user can override:

```python
# In pie():
def pie(self, ..., emphasis: Optional[PieEmphasis] = None, ...):
    ...
    # Default emphasis (existing behavior)
    emphasis_dict: dict = {
        "itemStyle": {
            "shadowBlur": 10, "shadowOffsetX": 0,
            "shadowColor": "rgba(0, 0, 0, 0.5)",
        }
    }
    if center_on_hover:
        emphasis_dict["label"] = { ... }  # existing logic
    if is_overlay:
        emphasis_dict["focus"] = "self"

    # User override replaces the defaults entirely
    if emphasis is not None:
        emphasis_dict = emphasis.to_dict()
        # Still apply overlay focus if not explicitly set
        if is_overlay and "focus" not in emphasis_dict:
            emphasis_dict["focus"] = "self"

    entry["emphasis"] = emphasis_dict
```

### 4.4 Backward Compatibility for Sankey

Sankey currently accepts `emphasis: Optional[dict]`. We change the type but keep dict support during a deprecation period:

```python
def sankey(self, ..., emphasis: Optional[Union[SankeyEmphasis, dict]] = None, ...):
    ...
    if emphasis is not None:
        if isinstance(emphasis, dict):
            warnings.warn(
                "Passing emphasis as a dict is deprecated. "
                "Use SankeyEmphasis(...) instead.",
                DeprecationWarning, stacklevel=2,
            )
            entry["emphasis"] = emphasis
        else:
            entry["emphasis"] = emphasis.to_dict()
```

---

## 5. Usage Examples

### 5.1 Bar — highlight the hovered series, dim others

```python
from echartsy import Figure
from echartsy.emphasis import Emphasis, ItemStyle

fig = (
    Figure()
    .bar(
        df, x="Month", y="Revenue", hue="Region",
        emphasis=Emphasis(
            focus="series",
            item_style=ItemStyle(shadow_blur=10, shadow_color="rgba(0,0,0,0.3)"),
        ),
    )
    .title("Revenue by Region")
    .show()
)
```

### 5.2 Line — bold the line and show labels on hover

```python
from echartsy.emphasis import LineEmphasis, LineStyle, LabelStyle

fig = (
    Figure()
    .plot(
        df, x="Date", y="Price", hue="Stock",
        emphasis=LineEmphasis(
            focus="series",
            line_style=LineStyle(width=4),
            label=LabelStyle(show=True, formatter="{c}"),
        ),
    )
    .show()
)
```

### 5.3 Pie — scale on hover with custom size

```python
from echartsy.emphasis import PieEmphasis, ItemStyle, LabelStyle

fig = (
    Figure()
    .pie(
        df, names="Category", values="Amount",
        emphasis=PieEmphasis(
            scale=True,
            scale_size=15,
            item_style=ItemStyle(shadow_blur=20, shadow_color="rgba(0,0,0,0.6)"),
            label=LabelStyle(show=True, font_size=16, font_weight="bold"),
        ),
    )
    .show()
)
```

### 5.4 Scatter — disable emphasis entirely

```python
from echartsy.emphasis import ScatterEmphasis

fig = (
    Figure()
    .scatter(df, x="Height", y="Weight", emphasis=ScatterEmphasis(disabled=True))
    .show()
)
```

### 5.5 Sankey — focus on adjacent nodes

```python
from echartsy.emphasis import SankeyEmphasis, LineStyle

fig = (
    Figure()
    .sankey(
        df, levels=["Source", "Target"], value="Flow",
        emphasis=SankeyEmphasis(
            focus="adjacency",
            line_style=LineStyle(opacity=0.6),
        ),
    )
    .show()
)
```

### 5.6 Heatmap — custom hover color

```python
from echartsy.emphasis import Emphasis, ItemStyle

fig = (
    Figure()
    .heatmap(
        df, x="Day", y="Hour", value="Value",
        emphasis=Emphasis(
            item_style=ItemStyle(
                border_color="#000", border_width=2, shadow_blur=15,
            ),
        ),
    )
    .show()
)
```

---

## 6. Implementation Plan — Step by Step

### Phase 1: Foundation (emphasis.py + exports)

1. **Create `echartsy/emphasis.py`** with all dataclasses from Section 3.
2. **Update `echartsy/__init__.py`** to export the emphasis classes:
   ```python
   from echartsy.emphasis import (
       Emphasis, LineEmphasis, ScatterEmphasis, PieEmphasis,
       RadarEmphasis, SankeyEmphasis, FunnelEmphasis, TreemapEmphasis,
       ItemStyle, LabelStyle, LineStyle, AreaStyle, LabelLineStyle,
   )
   ```
3. **Write unit tests** for every `to_dict()` method to confirm correct camelCase serialization and `None`-omission.

### Phase 2: Integrate into Figure methods

4. **Add `emphasis` parameter** to all 12 chart methods (signatures listed in Section 4.1).
5. **Inject emphasis into series config** using the pattern from Section 4.2.
6. **Preserve backward compatibility** for pie, heatmap, and sankey (Sections 4.3–4.4).
7. **Add type hints** using `Union[SpecificEmphasis, None]` for each method.

### Phase 3: Tests & Documentation

8. **Unit tests** — one test per chart type verifying:
   - Default behavior unchanged when `emphasis=None`
   - Emphasis dict correctly injected into `to_option()` output
   - Backward-compatible dict path for sankey triggers deprecation warning
9. **Integration test** — render a figure with emphasis and verify the HTML output contains the expected emphasis config.
10. **Update `examples.ipynb`** with 2–3 emphasis examples.

### Phase 4: Timeline support

11. **Extend `TimelineFigure`** — ensure emphasis params flow through when building timeline frames (emphasis is per-series, so this should work automatically if the frame-building logic passes `**series_kw`).

---

## 7. File Changes Summary

| File | Action |
|------|--------|
| `echartsy/emphasis.py` | **NEW** — all emphasis dataclasses |
| `echartsy/__init__.py` | **EDIT** — add emphasis exports to `__all__` |
| `echartsy/figure.py` | **EDIT** — add `emphasis` param to 12 methods |
| `tests/test_emphasis.py` | **NEW** — unit tests for emphasis serialization |
| `tests/test_figure.py` | **EDIT** — add emphasis integration tests |
| `examples.ipynb` | **EDIT** — add emphasis examples |

---

## 8. Design Decisions & Trade-offs

**Q: Why frozen dataclasses instead of mutable dicts?**
Immutability prevents accidental mutation after creation. It matches `StylePreset`. Users who need dynamic emphasis can create new instances (they're cheap).

**Q: Why a class hierarchy instead of one flat class with all fields?**
Type safety. If you pass `LineEmphasis` to `bar()`, your IDE/type-checker will warn you. A flat class would silently accept `line_style` on a bar chart, which ECharts would ignore — confusing.

**Q: Why not a `.emphasis()` builder method on Figure (like `.title()`, `.tooltip()`)?**
Emphasis is per-series, not per-figure. A single figure can have a line series with `LineEmphasis(focus="series")` and a bar series with `Emphasis(disabled=True)`. A figure-level method can't express this. Keeping it on the series method is the correct semantic.

**Q: Can users still pass raw dicts via `series_kw`?**
Yes. `series_kw` is applied after the emphasis injection via `entry.update(series_kw)`, so `series_kw={"emphasis": {...}}` will override the dataclass. This is the existing escape hatch and remains fully functional.

**Q: What about `select` and `blur` states?**
These can follow the same pattern in a future PR. The architecture is extensible — add `SelectEmphasis`, `BlurEmphasis` dataclasses using the same sub-style classes (`ItemStyle`, `LabelStyle`, etc.).
