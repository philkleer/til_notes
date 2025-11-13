# TIL: Speeding up Shiny apps with smarter reactive design
_Date: 2025-11-04_

## Context
While working on a large Shiny app, I noticed slow loading times and reactivity when transforming large datasets or regenerating outputs unnecessarily.  
I explored techniques to optimize Shiny performance without changing the app’s logic.

## Key insights

### Move heavy transformations into `reactive()` blocks
Instead of repeating transformations in multiple outputs:

```r
filtered_data <- reactive({
  req(input$region)
  df |> dplyr::filter(region == input$region)
})
```

Then reuse it across plots and tables:

```r
output$plot <- renderPlot({ plot(filtered_data()$x, filtered_data()$y) })
output$table <- renderTable({ head(filtered_data()) })
```

### Use `eventReactive()` for actions triggered by buttons
Avoid unnecessary recomputation:

```r
result <- eventReactive(input$run, { heavy_computation() })
```

### Cache stable results with `bindCache()`

```r
output$plot <- renderPlot({
  plot(filtered_data()$x, filtered_data()$y)
}) |> bindCache(input$region)
```

### Preload global data and libraries
Move static data loading to `global.R` or the top of `server.R` so it loads once.

### Profile and benchmark
Use tools like `reactlog`, `profvis`, or `shinyloadtest` to detect bottlenecks.

## Results
- Apps react faster (especially with large data).
- CPU use dropped as redundant recalculations disappeared.
- Improved user experience — smoother updates.

## Lessons Learned
- Think in **reactive dependencies**, not procedural flow.
- Use caching and separation of reactives to minimize recomputation.
- Small changes in reactivity design can yield huge speedups.

## References
- [Mastering Shiny – Reactive Programming](https://mastering-shiny.org/reactivity.html)
- [Posit: Improving Shiny Performance](https://shiny.posit.co/r/articles/improve/performance/)
