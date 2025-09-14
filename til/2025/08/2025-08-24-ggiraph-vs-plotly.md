---
title: "Interactive graphics in R: ggiraph vs plotly"
date: 2025-09-14
tags: [r, ggplot2, ggiraph, plotly, visualization]
---

**TL;DR**
- **ggiraph** = ggplot2 + interactive geoms → SVG tooltips/hover/select; great for publication-quality plots and precise tooltips.
- **plotly** = JavaScript charting via R → rich pan/zoom/legend toggles, 3D & WebGL; great for dashboards and big datasets.

## When to pick which
- **Pick ggiraph** when you already have **ggplot2** code, want **pixel-perfect SVG** (reports/Quarto), and need **click/hover/select** with custom tooltips.
- **Pick plotly** when you need **zoom/pan out of the box**, **3D/ternary/maps**, or **WebGL** for lots of points (`toWebGL()`).
- Converting `ggplot` → `ggplotly()` works, but direct `plot_ly()` gives more control.
- Very large data: **plotly** (WebGL) tends to stay snappier than **ggiraph** (SVG DOM size).

## Minimal examples

### ggiraph (interactive ggplot2 → SVG)
```r
library(ggplot2)
library(ggiraph)

gg <- ggplot(mtcars, aes(wt, mpg, color = factor(cyl))) +
  geom_point_interactive(
    aes(
      tooltip = paste("mpg:", mpg),
      data_id = rownames(mtcars)
    ),
    size = 3
  )

girafe(
  ggobj = gg,
  options = list(
    opts_hover(css = "stroke-width:3"),
    opts_selection(type = "single", only_shiny = FALSE)
  )
)
```
*Shiny integration:* `input$<girafe_id>_selected` returns `data_id` values.

### plotly (JS charts; rich interactions)
```r
library(plotly)

plot_ly(
  data = mtcars,
  x = ~wt, y = ~mpg, color = ~factor(cyl),
  type = "scatter", mode = "markers",
  text = ~paste("mpg:", mpg), hoverinfo = "text+x+y"
)
```
*Shiny integration:* `event_data("plotly_click")`, `event_data("plotly_selected")`, etc.

## Gotchas
- `ggplotly()` doesn’t always preserve **all** ggplot theming/labels—tweak with plotly APIs if needed.
- **Static export** from plotly needs external helpers (e.g., kaleido); ggiraph outputs **SVG** natively.
- For huge point clouds, prefer **plotly + WebGL** (`plotly::toWebGL()`).
