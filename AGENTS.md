# Language Scope

This document contains language-specific rules.

- **R rules apply only to R code**
- **Python rules apply only to Python code**
- Shared rules (response behavior, modification rules) apply to both

If the user is working in a specific language, the agent MUST follow
the corresponding section.

# R Coding Guidelines

If a rule conflicts with a previous instruction in the conversation, AGENTS.md takes precedence unless explicitly overridden.

These rules apply **only to R code**.

## R Environment Management

All R projects MUST use `renv`.

- Dependency management is handled exclusively via `renv`
- `renv::status()` must be checked at the start of scripts
- `renv::snapshot()` must be run after dependency changes
- The `renv.lock` file must be committed for reproducibility

## How to Respond
- Provide complete, runnable code blocks (not fragments)
- Explain your reasoning BEFORE the code, not after
- When modifying existing code, show the full function/section, not just changed lines
- If uncertain about requirements, ask ONE clarifying question before proceeding
- Match the existing code style in the file

---

## PRIMARY DIRECTIVE: Keep Each Step Simple

**Pipes are fine. Complexity within steps is not.**
Each step in a pipeline should do ONE simple thing. Don't write steps that transform many variables at once or contain complex nested logic. If you have different stages like transforming x or transforming y (or logging or cleaning) you can write a block of each stage. A ‘simple thing’ means: one conceptual operation (e.g. cleaning x, logging y, filtering rows), not a full feature-engineering pipeline. When computing summaries inside mutate(), always consider NA handling.

### ✅ GOOD: Simple pipes with one operation per step
```r
result <- data |>
  filter(x > 0) |>
  mutate(y = log(x)) |>
  group_by(group) |>
  summarise(mean_y = mean(y), .groups = "drop")
```

### ✅ Still GOOD: Multiple mutations if they are simple and related
```r
result <- data |> 
  mutate(
    x_log = log(x),
    x_squared = x^2
  ) |>
  mutate(
    y_log = log(x),
    y_squared = y^2
  ) |>
  filter(x_log > 0)
```

### ❌ BAD: Complex transformations crammed into single steps
```r
result <- data |>
  mutate(
    x_clean = ifelse(x < 0, NA, x),
    x_log = log(x_clean + 1),
    x_scaled = (x_log - mean(x_log, na.rm = TRUE)) / sd(x_log, na.rm = TRUE),
    y_clean = case_when(
      y < quantile(y, 0.01, na.rm = TRUE) ~ quantile(y, 0.01, na.rm = TRUE),
      y > quantile(y, 0.99, na.rm = TRUE) ~ quantile(y, 0.99, na.rm = TRUE),
      TRUE ~ y
    ),
    y_log = log(y_clean),
    z_factor = factor(z, levels = c("low", "med", "high")),
    outcome = x_scaled * y_log + as.numeric(z_factor)
  )
```

### ✅ GOOD: Break complex transformations into readable steps with comments
```r
# Clean x
data_clean <- data |>
  mutate(
    x_clean = ifelse(x < 0, NA, x),
    x_log = log(x_clean + 1)
  ) |>
  # Scale x
  mutate(
    x_mean = mean(x_log, na.rm = TRUE),
    x_sd = sd(x_log, na.rm = TRUE),
    x_scaled = (x_log - x_mean) / x_sd
   ) |>
  # Winsorize y
  mutate(
    y_bounds = quantile(y, c(0.01, 0.99)),
    y_clean = pmax(pmin(y, y_bounds[2]), y_bounds[1]),
    y_log = log(y_clean)
  ) |>
  # Create z_factor (final outcome)
  mutate(
    z_factor = factor(z, levels = c("low", "med", "high")),
    outcome = x_scaled * y_log + as.numeric(z_factor)
  )
```

### When to add verification output
Add `cat()`, `glimpse()`, or `summary()` after steps that:
- Filter rows (check how many remain)
- Create variables that could produce NA/Inf (check for problems)
- Merge datasets (check row counts)
- Involve complex logic (spot-check results)

---

## SECOND DIRECTIVE: Adjust graphics generated with ggplot

### Colorblind-Friendly Visualization

**ALL visualizations MUST use colorblind-friendly color palettes.**

This is my standard colorblind palette:

#### Standard colorblind palette
```r
cb_palette <- c(
  "#E69F00", # Orange
  "#56B4E9", # Light Blue
  "#009E73", # Green
  "#D55E00", # Vermillion
  "#F0E442", # Yellow
  "#0072B2", # Blue
  "#CC79A7", # Pink
  "#970756",  # Magenta
  "#26EAE2", # teal
  "#C7AA55", # gold
  "#259585",  # turquoise
  "#A64DE8", # purple  
  "#A2D8FF" # pale_blue
)
```

#### Never use
- Default ggplot2 colors
- Rainbow palettes
- Red/green combinations

### Text and Font Settings

Always use packages showtext and sysfonts and remind to load these at the start of scripts that generate graphics. Use Google Fonts like "Exo" or "Fira Sans" for better aesthetics.

```r
library(showtext)
library(sysfonts)

font_add_google("Exo", "Exo")
font_add_google("Fira Sans", "Fira Sans")
font_add_google("Fira Code", "Fira Code")
showtext_auto()
```

---

## THIRD DIRECTIVE: Code Style
- Use tidyverse packages for all data manipulation
- if datasets are large use duckplyr or dbplyr to speed up dplyr verbs
- Use `<-` for assignment (not `=`)
- Use native pipes `|>` (not `%>%`)
- Use `snake_case` for variable names
- Keep lines under 80 characters
- Use `here::here()` for file paths (never `setwd()`)
- Always `set.seed()` for reproducibility

---

## FOURTH DIRECTIVE: Project Structure
```
.
├── data/raw/       # Never modify files here
├── data/processed/ # Cleaned data goes here
├── docs/           # additional documentary stuff like PDFs, md-files or notes about what I did
├── output/         # Results, tables, figures
│    ├── diagnostics/    # model diagnostics (if applies)
│    ├── images/    # images or figures
│    └── models/    # model files or model results (ML)
├── src/            # Analysis scripts (numbered: 01_clean.R, 02_analyze.R)
│    ├── R/         # Function definitions
│    └── modules/   # Module definitions (if shiny is used)
└── tests/          # testthat tests
```

- Use `here::here()` for all paths
- Scripts should be self-contained and runnable from project root

---

## FIFTH DIRECTIVE: Script Structure

```r
################################################################################
#
# Title
# Author: Philipp Kleer
# Last change: 01/01/2026
#
################################################################################

# Check R environment first (renv is mandatory) --------------------------------
renv::status()

# Packages ---------------------------------------------------------------------
library(tidyverse)
library(here)
library(showtext)
library(sysfonts)

# Graphics settings ------------------------------------------------------------
font_add_google("Exo", "Exo")
font_add_google("Fira Sans", "Fira Sans")
font_add_google("Fira Code", "Fira Code")
showtext_auto()

theme_phil <- function() {
  ggplot2::theme(
    # text = element_text(size = rel(2.5)),
    plot.title = element_text(size = rel(1.8), family = "Exo"),
    plot.subtitle = element_text(size = rel(1.4), family = "Exo"),
    plot.caption = element_text(
      size = rel(0.8),
      family = "Exo",
      margin = margin(r = 0.1, unit = "in")
    ),
    plot.margin = margin(t = 0.15, r = 0.15, b = 0.25, l = 0.25, unit = "in"),
    axis.title = element_text(size = rel(1.1), family = "Exo"),
    axis.title.y = element_text(margin = margin(r = 15)),
    axis.text = element_text(size = rel(0.8), family = "Exo"),
    axis.text.x = element_text(angle = -45, hjust = 0, vjust = 0),
    axis.ticks = element_line(linewidth = 0.5, color = "#5B6770"),
    strip.text = element_text(size = rel(1), family = "Exo"),
    panel.border = element_rect(color = "#5B6770", fill = NA, linewidth = 1),
    panel.grid = element_blank(),
    legend.background = element_blank(),
    legend.position = "none",
    legend.text = element_text(
      size = rel(1.1),
      family = "Exo",
      margin = margin(r = 0.4, l = 0.1, unit = "in")
    )
  )
}

# Local functions --------------------------------------------------------------
# ... 

# Loading Data -----------------------------------------------------------------
data <- read_csv(here("data", "raw", "datafile.csv"))

glimpse(data)
summary(data)

# Manipulating Data ------------------------------------------------------------


# Analysis (step-by-step with verification) ------------------------------------
set.seed(12345)

# ...

```

---

## SIXTH DIRECTIVE: Documentation
- Use roxygen2 for all functions
- Required tags: `@param`, `@return`, `@examples`
- Set author tag: `@author Philipp Kleer`
- Include at least one runnable example

```r
#' Calculate group means with robust SEs
#'
#' @param data A data frame containing the variables
#' @param outcome Character. Name of the outcome variable
#' @param group Character. Name of the grouping variable
#' @author Philipp Kleer
#' 
#' @return A tibble with group means and standard errors
#'
#' @examples
#' calc_group_means(mtcars, "mpg", "cyl")
calc_group_means <- function(data, outcome, group) {
  # ...
}
```

---

## SEVENTH DIRECTIVE: Testing
- Write tests for any function with more than 5 lines
- Use `testthat` framework (version 3)
- Include edge cases: empty inputs, NA values, single-row data

```r
test_that("function handles empty data gracefully", {
  expect_error(my_function(data.frame()), "Data must have")
})

test_that("function handles NA values", {
  result <- my_function(data_with_nas)
  expect_false(any(is.na(result$estimate)))
})
```

---

## EIGHTH DIRECTIVE: Error Handling
- Fail fast with informative messages
- Validate inputs at function start
- Error messages should say what was expected AND what was received
- Use `tryCatch()` for external operations (file I/O, API calls)

```r
my_function <- function(data, var) {
  # Input validation first
  stopifnot(
    "data must be a data frame" = is.data.frame(data),
    "data cannot be empty" = nrow(data) > 0,
    "var must be in data" = var %in% names(data)
  )
  
  # For external operations
  result <- tryCatch(
    read_csv(here("data", "file.csv")),
    error = function(e) {
      stop("Failed to read data file: ", e$message)
    }
  )
}
```

---

## NINTH DIRECTIVE: Statistical Analysis
- Check assumptions before running models
- Use `broom::tidy()` for clean model output
- Use `estimatr::lm_robust()` for robust standard errors
- Report confidence intervals alongside point estimates
- Use `modelsummary` for publication-ready tables

---

## TENTH DIRECTIVE: Causal Inference Workflow
When estimating treatment effects:
1. Show balance table before/after matching
2. Report both ATE and ATT when relevant
3. Include sensitivity analysis (e.g., Rosenbaum bounds)
4. Always cluster standard errors at treatment assignment level
5. Use `fixest` for high-dimensional fixed effects

---

## ELEVENTH DIRECTIVE: Packages

### Essential
- `tidyverse`, `here`, `broom`, `cli`, `testthat`, `renv`, `assertthat`, `glue`

### Machine Learning
- `tidymodels`, `recipe`, `parsnip`, `tune`, `yardstick`

### Visualization
- `ggplot2`, `ggiraph`, `patchwork`, `ggeffects`

### Spatial analysis
- `sf`, `spdep`, `tmap`

### DB handling
- `RPostgres`, `DBI`, `duckdb`, `dbplyr`, `jsonlite`
- `plumber`, `pool` for APIs

### Data handling
- `qs2` or `arrow` for large data files
- `rio` for loading various formats

### Shiny applications
- `shiny`, `shinyWidgets`, `shinydashboardPlus`, `shinyBS`, `shinydashboard`, `shinyjs`, `shinyloadtest`

### Statistical
- `estimatr`, `marginaleffects`, `fixest`, `sandwich`, `lmtest`, `brms`

### Dependency rules
- Minimize dependencies—prefer base R or tidyverse over niche packages
- If suggesting a new package, note installation: `# install.packages("pkg")`
- Don't use `library()` inside functions—use `::` notation

---

## TWELFTH DIRECTIVE: When Modifying My Code
- Preserve my variable naming conventions
- Don't refactor unrelated code unless asked
- If you see a bug unrelated to my question, mention it but don't fix it silently
- Match the existing indentation and spacing style

---

## THIRTEENTH DIRECTIVE: Never Do These
- Don't use `attach()` – causes namespace conflicts
- Don't use `T`/`F` – use `TRUE`/`FALSE`
- Don't use `=` for assignment – use `<-`
- Don't use `1:length(x)` – use `seq_along(x)`
- Don't use `sapply()` – use `vapply()` or `map_*()` for type safety
- Don't use `subset()` in functions – use `filter()`
- Don't suppress warnings without documenting why
- Don't hardcode file paths
- Don't leave `print()` statements in production functions
- Don't forget to set seeds
- **Never cram complex multi-variable transformations into a single step**
- **Never use default color palettes**

---

## FOURTEENTH DIRECTIVE: Reproducibility

Every analysis script must end with session info:

```r
cat("\n=== Session Info ===\n")
sessionInfo()
```

After installing, upgrading, or removing packages, ALWAYS:

```r
# Check status:
renv::status()

# Lock package versions:
renv::snapshot()
```

The renv.lock file must be kept in sync with the project state.

---

## Agent Compliance Checklist (R, MANDATORY)

This checklist is **binding**.

Before responding, the agent MUST internally verify compliance with all
applicable items below.

If a checklist item conflicts with:
1. Earlier conversation instructions, or
2. Default agent behavior,

**AGENTS.md takes precedence unless the user explicitly overrides it.**

Do not mention the checklist in the final response.

If an item is not applicable (e.g. no plots, no functions), it may be skipped. The agent must comply silently; do not announce that the checklist was followed.

1. Response Behavior

- [ ] Provide complete, runnable code (no fragments)
- [ ] Explain reasoning before code
- [ ] When modifying code, show the full section/function
- [ ] Ask at most ONE clarifying question if requirements are unclear
- [ ] Match the existing code style exactly

2. Pipes & Data Transformation

- [ ] Each pipe step does ONE simple thing
- [ ] Do NOT cram complex multi-variable logic into a single step
- [ ] Break transformations into conceptual stages (e.g. clean x, log y)
- [ ] Multiple mutate() calls are allowed if each is simple and focused
- [ ] Add verification output (glimpse(), summary(), cat()) after:
  - [ ] Filters
  - [ ] Joins
  - [ ] NA / Inf–prone transformations
  - [ ] Complex logic

3. Code Style

- [ ] Use tidyverse for data manipulation
- [ ] Use native pipe |> (never %>%)
- [ ] Use <- for assignment
- [ ] Use snake_case
- [ ] Keep lines ≤ 80 characters
- [ ] Use here::here() for all paths
- [ ] Call set.seed() for reproducibility
- [ ] Never use:
  - [ ] attach(), subset(), T/F, 1:length(), sapply()
  - [ ] Default ggplot palettes
  - [ ] Hardcoded paths
  - [ ] Silent refactors of unrelated code

4. Graphics

- [ ] Use colorblind-friendly palette only
- [ ] Never use default ggplot2 colors or rainbow palettes
- [ ] Load and use showtext and sysfonts
- [ ] Use Google Fonts (e.g. Exo, Fira Sans)
- [ ] Apply project theme where appropriate

5. Functions & Documentation

- [ ] All functions use roxygen2
- [ ] Required tags present:
  - [ ] @param
  - [ ] @return
  - [ ] @examples
  - [ ] @author Philipp Kleer
- [ ] Examples are runnable
- [ ] Use :: inside functions (no library() calls)

6. Testing & Error Handling

- [ ] Functions > 5 lines have testthat (v3) tests
- [ ] Tests include:
  - [ ] Empty input
  - [ ] NA handling
  - [ ] Edge cases
- [ ] Validate inputs at function start
- [ ] Fail fast with informative error messages
- [ ] Use tryCatch() for external I/O or APIs

7. Analysis & Statistics

- [ ] Check assumptions before modeling
- [ ] Use broom::tidy() for model output
- [ ] Report confidence intervals
- [ ] Use robust SEs (estimatr, clustering where required)
- [ ] Use modelsummary for final tables

8. Project & Reproducibility

- [ ] Project uses `renv` and `renv.lock` is up to date
- [ ] Respect project directory structure
- [ ] Scripts are runnable from project root
- [ ] End scripts with sessionInfo()
- [ ] Run renv::status() and renv::snapshot() after dependency changes

9. Modification Rules

- [ ] Preserve variable names and structure
- [ ] Do not refactor unrelated code
- [ ] Mention unrelated bugs, do not fix silently
- [ ] Follow AGENTS.md over default agent preferences

# Python Coding Guidelines

If a rule conflicts with a previous instruction in the conversation,
AGENTS.md takes precedence unless explicitly overridden.

These rules apply **only to Python code**.

## PRIMARY DIRECTIVE: Keep Each Step Simple

**Pipelines are fine. Complexity within steps is not.**

Each step in a data-processing workflow should do **ONE simple thing**.
Do not write steps that transform many variables at once or contain deeply
nested logic. Data manipulation **MUST** use Polars.

A “simple thing” means:
- one conceptual operation (e.g. filtering rows, cleaning one variable,
  computing one feature group),
- not a full feature-engineering pipeline.

If you have different stages (e.g. cleaning, feature creation, aggregation),
write them as **separate, readable steps**.

### ✅ GOOD: Simple, readable steps (polars)
```python
import polars as pl

df = df.filter(pl.col("x") > 0)

df = df.with_columns(
    y_log=pl.col("x").log()
)

result = (
    df.group_by("group")
      .agg(pl.col("y_log").mean().alias("mean_y"))
)
```

### ❌ BAD: Complex transformations crammed into one step

```python
df = df.with_columns(
    outcome=(
        (pl.col("x").clip(lower_bound=0).log1p()
         - pl.col("x").log().mean())
        / pl.col("x").log().std()
        * pl.col("y").clip(
            lower_bound=pl.col("y").quantile(0.01),
            upper_bound=pl.col("y").quantile(0.99),
        ).log()
        + pl.col("z").replace({"low": 1, "med": 2, "high": 3})
    )
)
```

### ✅ GOOD: Break complex transformations into stages

```python
# Clean x
df = df.with_columns(
    x_clean=pl.when(pl.col("x") >= 0).then(pl.col("x")).otherwise(None),
    x_log=pl.when(pl.col("x") >= 0).then(pl.col("x").log1p()).otherwise(None),
)

# Scale x (compute stats once)
x_stats = df.select(
    x_mean=pl.col("x_log").mean(),
    x_std=pl.col("x_log").std(),
).row(0)

df = df.with_columns(
    x_scaled=(pl.col("x_log") - x_stats[0]) / x_stats[1]
)

# Winsorize y (compute bounds once)
y_bounds = df.select(
    y_low=pl.col("y").quantile(0.01),
    y_high=pl.col("y").quantile(0.99),
).row(0)

df = df.with_columns(
    y_clean=pl.col("y").clip(lower_bound=y_bounds[0], upper_bound=y_bounds[1]),
    y_log=pl.col("y_clean").log(),
)
```

### When to add verification output

Add df.shape, df.info(), df.describe(), or explicit assertions after steps that:

- Filter rows
- Merge / join data
- Create variables that could produce NaN / inf
- Involve non-trivial logic

## SECOND DIRECTIVE: Visualization (plotnine)

### Colorblind-Friendly Visualization

**ALL visualizations MUST use colorblind-friendly palettes.**

- Do NOT use plotnine defaults
- Do NOT use rainbow palettes
- Do NOT rely on implicit color cycling

Define and use an explicit palette, e.g.:

```python
CB_PALETTE = [
  "#E69F00", "#56B4E9", "#009E73", "#D55E00", "#F0E442", "#0072B2",
  "#CC79A7", "#970756",  "#26EAE2", "#C7AA55", "#259585", "#A64DE8",
  "#A2D8FF"
]
```

Always apply it explicitly, e.g.:

```python
from plotnine import ggplot, aes, geom_point, scale_color_manual, theme_minimal

p = (
    ggplot(polars_df, aes("x", "y", color="group"))
    + geom_point()
    + scale_color_manual(values=CB_PALETTE)
    + theme_minimal()
)
```

## THIRD DIRECTIVE: Code Style

- Use `polars` for data manipulation/wrangling
- Prefer vectorized operations over loops
- Use `snake_case` for variables and functions
- Keep lines ≤ 80 characters
- Never mutate global state implicitly
- Use explicit imports (no `import *`)
- Set random seeds for reproducibility

## FOURTH DIRECTIVE: Project Structure

### Rules:
- Use `pyproject.toml` for dependencies
- Keep `uv.lock` committed for reproducibility
- Scripts must be runnable from the project root

Common commands:
- `uv sync`
- `uv run python -m project_name.some_module`
- `uv run pytest`

### Recommended Directory Structure
```
.
├── data/
│   ├── raw/            # Never modify files here
│   └── processed/      # Cleaned data goes here
├── docs/    # additional documentary stuff like PDFs, md-files or notes about what I did
├── output/    # Results, tables, figures
│   ├── diagnostics/    # model diagnostics (if applies)
│   ├── images/    # images or figures
│   └── models/    # model files or model results (ML)
├── src/      # Analysis scripts
│   ├── python/         # Function definitions
│   ├── modules/   # Module definitions (if shiny is used)
│   └── project_name/
├── tests/  # test with pytest
├── pyproject.toml
└── uv.lock
```

## FIFTH DIRECTIVE: Script Structure

```python
"""
Title
Author: Philipp Kleer
Last change: 01/01/2026
"""

# Libraries —-------------------------------------------------------------------
import polars as pl

# Graphics settings ------------------------------------------------------------
# ...

# Local functions --------------------------------------------------------------
# ... (right here or sourced from src/python)

# Loading data ----------------------------------------------------------------
df = pl.read_csv("data/raw/datafile.csv")

print(df.shape)
print(df.head())

# Data manipulation ------------------------------------------------------------
# ...

# Analysis (step-by-step with verification) ------------------------------------
# If randomness is used:
# import numpy as np
# np.random.seed(12345)

```

### SIXTH DIRECTIVE: Documentation

- All non-trivial functions must have docstrings
- Use NumPy-style or Google-style docstrings
- Document parameters, returns, and edge cases
- Include at least one runnable example when useful

## SEVENTH DIRECTIVE: Testing
Write tests for any function longer than ~10 lines

- Use pytest
- Include edge cases:
  - Empty inputs
  - Missing values
  - Single-row inputs

## EIGHTH DIRECTIVE: Error Handling

- Validate inputs at function start
- Fail fast with informative messages
- Catch external I/O and API errors explicitly
- Do NOT silence warnings without justification

## Agent Compliance Checklist (Python, MANDATORY)

This checklist is binding.

Before responding, the agent MUST internally verify compliance with all
applicable items below.

If a checklist item conflicts with:
1. Earlier conversation instructions, or
2. Default agent behavior,

**AGENTS.md takes precedence unless explicitly overridden.**

Do not mention the checklist in the final response.

If an item is not applicable, it may be skipped.

1. Response Behavior

- [ ] Provide complete, runnable code
- [ ] Explain reasoning before code
- [ ] Show full functions/sections when modifying code
- [ ] Ask at most ONE clarifying question if unclear
- [ ] Match existing code style

2. Data Transformation

- [ ] Each step does ONE simple thing
- [ ] No complex multi-variable logic in one step
- [ ] Transformations broken into stages
- [ ] Verification output after risky operations

3. Code Style

- [ ] Prefer `polars` for wrangling (pandas only when necessary)
- [ ] snake_case naming
- [ ] Explicit imports
- [ ] Seed set for reproducibility
- [ ] No hidden global state
- [ ] No silent refactors

4. Visualization

- [ ] Use `plotnine`
- [ ] Colorblind-friendly palette only
- [ ] No default `plotnine` colors

5. Testing & Errors

- [ ] pytest tests for non-trivial functions
- [ ] Input validation present
- [ ] Informative error messages

6. Project & Reproducibility

- [ ] Project uses `uv` (`pyproject.toml` + `uv.lock`)
- [ ] Correct directory usage
- [ ] Script runnable from project root