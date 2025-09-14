---
title: "Modularizing a Large Shiny App (R)"
date: 2025-08-14
tags: [r, shiny, refactoring, modularization]
---

# Modularizing a Large Shiny App (R)

> Refactor case study — converting a monolithic Shiny application into a modular, maintainable codebase using Shiny modules and pure R components.

## Context
- Inherited a large Shiny app originally authored by a predecessor.
- Goal: **refactor** (behaviour-preserving changes) and **modularize** (structural decomposition) to improve maintainability, readability, and change-safety.
- Constraints: keep feature parity, minimize downtime, and avoid exposing proprietary logic/data.

> **Terminology**
> - *Refactoring* = change structure without changing behaviour.
> - *Modularization* = split responsibilities into isolated, reusable components (Shiny modules + pure R functions).

## Approach (high level)
1. **Define module boundaries** by feature/concern (e.g., authentication, filters, charts, tables, export) and create `mod_*` pairs:
   - `mod_feature_ui(id)` and `mod_feature_server(id, deps...)`.
2. **Extract business logic** from server code into pure functions under `src/R/` (functional, testable, no `input/output/session`).
3. **Standardize naming & IDs** using `NS()`; avoid global state; pass dependencies explicitly.
4. **Thin UI composition** in `app_ui()`; wire modules in `app_server()`.
5. **Consistency tooling**: `lintr`, `styler`, `renv` lockfile; pre-commit hooks for formatting/linting.

### Minimal module pattern (generic)
```r
# src/modules/mod_widget.R
mod_widget_ui <- function(id) {
  ns <- NS(id)
  tagList(
    shiny::textInput(ns("name"), "Name"),
    shiny::actionButton(ns("go"), "Go"),
    shiny::tableOutput(ns("tbl"))
  )
}

mod_widget_server <- function(id, compute_fn) {
  moduleServer(id, function(input, output, session) {
    shiny::observeEvent(input$go, {
      vals <- compute_fn(input$name)  # pure function from src/R
      output$tbl <- shiny::renderTable(vals)
    })
  })
}

# src/R/compute.R
compute_values <- function(name) {
  data.frame(greeting = paste0("Hello, ", name))
}

# app_server/app_ui (excerpt)
ui <- fluidPage(mod_widget_ui("w1"))
server <- function(input, output, session) {
  mod_widget_server("w1", compute_values)
}
```

## File metrics (before → intermediate)

### Baseline (before)
Monolithic layout with a few very large files.

| dir           | n_files | min_lines | max_lines |      mean_lines | median_lines |
|:--------------|--------:|----------:|----------:|----------------:|-------------:|
| `src/`        |       4 |       503 |     10651 |          4685.2 |       3793.5 |
| `src/modules` |       3 |        62 |       115 |            88.7 |         89.0 |
| `src/www`     |       1 |       495 |       495 |           495.0 |        495.0 |
| **Total**     |   **8** |         — |         — | **≈19,502 LOC** |            — |

### Intermediate state (after modularization pass in progress)
More files, each much smaller and easier to reason about.

| dir           | n_files | min_lines | max_lines |     mean_lines | median_lines |
|:--------------|--------:|----------:|----------:|---------------:|-------------:|
| `src/`        |       4 |       218 |       298 |          251.2 |        244.5 |
| `src/modules` |       6 |       278 |       985 |          529.5 |        427.5 |
| `src/R`       |       7 |       182 |      1615 |          754.4 |        612.5 |
| **Total**     |  **17** |         — |         — | **≈9,463 LOC** |            — |

**Impact so far**
- **~51% reduction** in total lines of code (~19.5k → ~9.46k LOC) while maintaining behaviour.
- **Max file size** shrank from **10,651** lines to **1,615** lines (easier navigation & reviews).
- Clear separation between **UI modules** (`src/modules`) and **pure logic** (`src/R`).

> Note: LOC is a coarse proxy; the larger win is reduced coupling and clearer boundaries.

## Why this helps (my takeaways)
- **Single fix, single place**: shared logic lives once; bug fixes don’t require hunting across similar blocks.
- **Cognitive load ↓**: smaller files and named modules make intent obvious; onboarding and reviews are faster.
- **Testability ↑**: pure functions in `src/R` are trivial to unit test with `testthat`.
- **Reusability**: a module can be dropped into other apps with minimal changes.

## Practices adopted
- Module naming: `mod_<feature>_{ui,server}`; IDs are namespaced via `NS(id)`.
- Dependency injection: pass functions/services into modules; avoid `<<-`/globals.
- Error handling: validate inputs early; surface user-friendly messages in UI.
- Style & lint: `styler::style_dir()`, `lintr::lint_dir()` via pre-commit.
- Project hygiene: `renv::init()` for reproducible dependencies.

## Next steps
- Add **unit tests** for `src/R` and **shiny tests** for modules (e.g., `shiny::testServer`).
- Introduce **type-like checks** with `checkmate` or `vctrs` for critical paths.
- Split any remaining >800-line files.
- Capture metrics in CI to prevent regressions (see script below).

## Appendix: Recreate the metrics (local script)
```r
# scripts/loc_summary.R
summarize_loc <- function(root = "src") {
  files <- list.files(root, recursive = TRUE, full.names = TRUE)
  # Focus on code-like files
  keep <- grepl("\\\.(R|Rmd|js|css|html)$", files, ignore.case = TRUE)
  files <- files[keep]
  nlines <- sapply(files, function(p) length(readLines(p, warn = FALSE)))
  df <- data.frame(file = files, dir = dirname(files), lines = as.integer(nlines))
  agg <- aggregate(lines ~ dir, df, function(x) c(n_files = length(x), min = min(x), max = max(x), mean = mean(x), median = median(x)))
  # Unpack the list columns
  out <- do.call(data.frame, agg)
  names(out) <- c("dir", "n_files", "min_lines", "max_lines", "mean_lines", "median_lines")
  out[order(out$dir), ]
}

print(summarize_loc("src"))
```

## Public disclosure note
This write-up is **code-free** and describes techniques, not proprietary logic or data. It is safe to publish publicly and to discuss at a high level in a portfolio.

