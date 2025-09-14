---
title: "R big data benchmarks: dplyr/duckplyr/polars & Postgres/DuckDB"
date: 2025-08-30
tags: [r, dplyr, duckplyr, polars, postgres, duckdb, dbplyr, benchmarks, big-data]
---

> Exploratory benchmarks comparing **data-frame backends** (dplyr/duckplyr/polars) and **query engines** (PostgreSQL/DuckDB). The goal is to document *trade‑offs* and a repeatable method—not crown a universal winner.

## Setup (summarized)
- **Machine:** MacBook (fill in model/RAM/CPU here)
- **R:** 4.x; Packages: `dplyr`, `duckdb`, `duckplyr`, `DBI`, `RPostgres`, `polars`, `bench`, `covr`
- **Data:** multiple regional subsets (e.g., *Sudeste*, *Sul*, *Nordeste*, etc.), up to ~millions of rows per region
- **Note:** Largest region first in the plots; cold caches flushed between major runs

## Libraries used
- `DBI`
- `RPostgres`
- `bench`
- `dbplyr`
- `dplyr`
- `duckdb`
- `duckplyr`
- `duckspatial`
- `glue`
- `lubridate`
- `nicverso`
- `polars`
- `pool`
- `processx`
- `qs`
- `rlang`
- `rmapshaper`
- `sf`
- `stringr`
- `tidyr`

## Approach
- **Reproducible runs** using `bench::mark()` with explicit iterations and `check = FALSE`.
- Data-frame pipelines composed with `dplyr` verbs; alternative backends via `duckplyr` and `polars` where present.
- **Database-backed** runs via `DBI` + `RPostgres`, with queries expressed through `dbplyr::tbl()` -> `dplyr` verbs and `collect()` at the end.
- For **DuckDB**, connections created with `duckdb::duckdb()`; CSV/Parquet ingestion via `read_csv_auto()` or equivalent.
- Measurements captured for **wall time** (and optionally memory) across regional slices.

## What I measured
- **Wall-clock execution time** for a representative transformation pipeline (filters → joins → group-by aggregations → optional sorting).
- **Peak memory** reported by the tooling/runner during each run (approximate, but comparable across backends).
- Two scenarios measured separately:
  - **Data-frame pipelines** (`dplyr`, `duckplyr`, `polars`).
  - **Database-backed queries** (`PostgreSQL`, `DuckDB`) expressed with `dplyr`/`dbplyr` verbs and collected at the end.

To keep comparisons fair: largest region processed first; repeated runs summarized; caches treated consistently between runs.

## Figures
If you already committed the charts, they live under `assets/benchmarks/` and are referenced here:

<img src="../../assets/benchmarks/execution.jpeg" alt="Execution time (data frames)" width="640"/>

<img src="../../assets/benchmarks/memory.jpeg" alt="Memory usage (data frames)" width="640"/>

<img src="../../assets/benchmarks/execution-postgresql.jpeg" alt="Execution time (databases)" width="640"/>

<img src="../../assets/benchmarks/memory-postgresql.jpeg" alt="Memory usage (databases)" width="640"/>

## Why these results make sense

- `dplyr` (in-memory) works on R vectors in RAM; many verbs create new copies. That’s ergonomic on small/medium tables but scales poorly when rows/columns grow—both time (copy/GC) and memory rise quickly.
- `duckplyr` (`dplyr` on `DuckDB`) translates verbs to `DuckDB` SQL and executes them in a vectorized, columnar engine. Work happens close to the data, minimizing copies and making joins/aggregations much faster than in-memory `dplyr` for large inputs.
-`polars` (lazy) builds a query plan first (predicate/column pushdown, projection pruning) and executes late, which typically reduces memory pressure and speeds up wide scans and grouped aggregations.
- PostgreSQL vs `DuckDB`:
  - PostgreSQL excels with persistent data, indexes, statistics, and repeated queries; a tuned plan (`EXPLAIN` ...) can beat default settings and scan engines on selective workloads.
  - `DuckDB` shines for local analytics (Parquet/CSV), large sequential scans, and ad-hoc pipelines without a running server.

## TL;DR
- On the **largest region/slice**, a tuned PostgreSQL plan (indexes + analyzed stats) outperformed default PostgreSQL and DuckDB in my runs; on smaller slices, differences narrowed and were often comparable.
- For **data-frame style code**, `dplyr` (in-memory) was consistently the slowest and most memory-hungry on big slices. **`duckplyr`** and **`polars`** (lazy) were much faster; **`polars`** typically had the lowest memory footprint.
- Results are **directional**: I/O, data types, cardinality/selectivity, and cache warmth materially affect both time and memory.

## Notes
- When data grows beyond comfortable RAM or you need repeatability/concurrency, prefer **`duckplyr`/`polars`** or push work into a **database engine**.
- Tune the engine you use:
  - PostgreSQL: create relevant indexes, `ANALYZE`, and inspect plans with `EXPLAIN` (`ANALYZE`, `BUFFERS`).
  - DuckDB: enable the profiler and review operator timings; store data in columnar formats when possible.
- Compare **like-for-like**: identical filters/joins/aggregations, same materialization point, and similar cache conditions (cold vs warm) when timing.
