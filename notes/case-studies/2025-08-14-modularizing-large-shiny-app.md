---
title: "Modularizing a Large Shiny App (R)"
date: 2025-08-14
tags: [r, shiny, refactoring, modularization]
---

# Modularizing a Large Shiny App (R)

> Refactor case study (work from prior employees) — converting a monolithic Shiny application into a modular, maintainable codebase using Shiny modules and pure R components.

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

## File metrics (before → intermediate)

### Baseline (before)
Monolithic layout with a few very large files.

| dir  | n_files | n_funcs | min_LOC | max_LOC | mean_LOC | median_LOC |
|------|--------:|--------:|--------:|--------:|---------:|-----------:|
| src/ |       4 |      91 |     503 |   10651 |  4685.25 |     3793.5 |

### After factorization/modularization
More files, each much smaller and easier to reason about.

| dir          | n_files | n_funcs | min_LOC |  max_LOC |   mean_LOC | median_LOC |
|--------------|--------:|--------:|--------:|---------:|-----------:|-----------:|
| src/         |       4 |       9 |     229 |      479 |        312 |        270 |
| src/modules/ |       4 |      18 |     253 |     1142 |     604.75 |        512 |
| src/R/       |       8 |     121 |     222 |     2884 |     933.38 |      690.5 |
| **<TOTAL>**  |  **16** | **148** | **222** | **2884** | **695.88** |    **481** |

**Impact so far**
- **~41% reduction** in total lines of code (~18.7k → ~11.13k LOC) while maintaining behaviour.
- **Max file size** shrank from **10,651** lines to **2,884** lines (easier navigation & reviews).
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
- Style & lint: styling/formatting with `Air`, `lintr::lint_dir()` via pre-commit.
- Project hygiene: `renv::init()` for reproducible dependencies.

## Next steps
- Add **unit tests** for `src/R` and **shiny tests** for modules (e.g., `shiny::testServer`).
- Introduce **type-like checks** with `checkmate` or `vctrs` for critical paths.

## Public disclosure note
This write-up is **code-free** and describes techniques, not proprietary logic or data. It is safe to publish publicly and to discuss at a high level in a portfolio.
