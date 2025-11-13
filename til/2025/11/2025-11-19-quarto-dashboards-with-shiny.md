# TIL: Embedding Shiny elements inside Quarto Dashboards
_Date: 2025-11-19_

## Context
While working with **Quarto**, I learned how to integrate **Shiny** components directly into a dashboard to make static documents interactive. This allows adding live charts, filters, and reactive UI elements without leaving the Quarto ecosystem.

The biggest advantage of this setup is **collaboration** — colleagues who aren’t familiar with Shiny can still work on the **static content** (text, Markdown, layout) while I handle the interactive components. That means we can build rich, mixed dashboards in a single framework, without splitting the project across multiple tools.

## Project structure for clarity
To keep a clear overview of the Shiny logic and modularize code, I organized the project like this:

```md
.
├── _brand.yml
├── _publish.yml
├── _quarto.yml
├── data/
├── dashboard.html
├── dashboard.qmd
├── R/
│   ├── helpers.R
│   ├── reactives.R
│   ├── tab-diagnostics.R
│   ├── tab-geral.R
│   ├── tab-mapas.R
│   ├── tab-regressao.R
│   └── tab-tabelas.R
└── server.R
```

- The `.qmd` file defines layout and Markdown structure.  
- The `R/` folder holds Shiny-specific code, split by topic (tabs, helpers, data).  
- `server.R` ties all reactivity together and runs the app.  
- The `_quarto.yml` configures the dashboard (theme, navbar, output).  

This separation makes it easier for non-Shiny contributors to edit text or configuration, while developers focus on the reactive backend.

## Example setup
By setting the document runtime to `shiny`, Quarto can run Shiny server logic alongside its markdown content.

```yaml
---
title: "Interactive Dashboard"
format: html
server: shiny
---
```

### Example code
```{r}
#| context: server

data <- reactive({
  mtcars[mtcars$cyl == input$cyl, ]
})

output$plot <- renderPlot({
  plot(data()$mpg, data()$hp, main = paste("Cyl =", input$cyl))
})
```

```{r}
#| context: ui

selectInput("cyl", "Choose cylinders", choices = sort(unique(mtcars$cyl)))
plotOutput("plot")
```

## Lessons Learned

- Quarto + Shiny bridges reproducible reporting and interactivity.
- The **structured folder layout** helps teams collaborate — static content and Shiny code stay organized but connected.
- Keep reactivity minimal; only reactive parts re-render.
- Perfect for quick dashboards without a full Shiny app structure.

## References
- [Quarto: Interactive Shiny for R Documents](https://quarto.org/docs/dashboards/interactivity/shiny-r.html)
- [Quarto: Interactive Shiny for Python Documents](https://quarto.org/docs/dashboards/interactivity/shiny-python.html)
