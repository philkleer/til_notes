# TIL & Project Overview

> Today I Learned — small, self-contained learning notes and tiny demos.  
> Public and **work-safe** (no company IP).

**Personal page:** [https://github.com/philkleer](https://github.com/philkleer)

**Repo:** [https://github.com/philkleer/til-and-notes](https://github.com/philkleer/til-and-notes)

## Entries

<!-- START:INDEX -->
### 📚 Case studies
- 2025-09-19 — [Case Study: Debugging across multiple R versions with `rig` + `renv`](notes/case-studies/2025-09-19-debugging-multiple-R-versions-with-rig-and-renv.md)
- 2025-09-14 — [From ad‑hoc repo to versioned, CI‑driven R package: nicverso](notes/case-studies/2025-09-14-nicverso-ci-overhaul.md)
- 2025-08-30 — [R big data benchmarks: dplyr/duckplyr/polars & Postgres/DuckDB](notes/case-studies/2025-08-30-r-bigdata-benchmarks-updated.md)
- 2025-08-14 — [Modularizing a Large Shiny App (R)](notes/case-studies/2025-08-14-modularizing-large-shiny-app.md)

### 📝 TILs (latest 12)
- 2025-09-30 — [Python packaging with Poetry — quick start & pitfalls (for R package devs)](til/2025/09/2025-09-30-poetry-quickstart-pitfalls.md)
- 2025-09-19 — [TIL: Managing multiple R versions with `rig`](til/2025/09/2025-09-19-managing-multiple-r-versions-with-rig.md)
- 2025-09-14 — [R CMD check badge from CI (pure R)](til/2025/09/2025-09-07-r-cmd-check-badge-from-ci-(pure-r).md)
- 2025-09-14 — [Dual gates: Air + lintr on staged files and diffs](til/2025/09/2025-09-14-dual-gates-air-+-lintr-on-staged-files-and-diffs.md)
- 2025-09-14 — [Release automation with release-cli](til/2025/09/2025-09-10-release-automation-with-release-cli.md)
- 2025-09-14 — [Interactive graphics in R: ggiraph vs plotly](til/2025/08/2025-08-24-ggiraph-vs-plotly.md)
- 2025-09-02 — [GitLab CI for R packages: fast caches with pak](til/2025/09/2025-09-02-gitlab-ci-for-r-packages-fast-caches-with-pak.md)
- 2025-09-01 — [Users vs contributors: smooth install with pak](til/2025/09/2025-09-01-users-vs-contributors-smooth-install-with-pak.md)
- 2025-08-30 — [Leaflet in R and Python — beginner caveats](til/2025/08/2025-08-30-leaflet-r-vs-python-caveats.md)
- 2025-08-14 — [Shiny modularization — key lessons](til/2025/08/2025-08-14-modularization.md)
- 2025-08-01 — [Spatial in R: sf — beginner caveats](til/2025/08/2025-08-01-sf-vs-geopolars-caveats.md)

_Last updated: 2025-09-24 12:31 UTC_
<!-- END:INDEX -->

## Project Overview

### Restructuring Portal OBIA

# DEBUG: MAKE THIS LIKE UNFOLDABLE (SO IT IS FOLDED AND THEN PEOPLE CAN EXPAND IT)

In this project, I worked on an initial version of former colleagues for the [portal Observatório de Inteligência Artifical](https://obia.nic.br) which monitors IA use and development through federal organizations. **Before** I started working on this project, the project was only managed by a single person and **was a monolithic Shiny application with just four files** and a lot of copied lines after each other (mean LOC: 4685.25, max LOC: 10,651). There was a process implemented in CI/CD to launch the application, however, quality tests like formatting/lintering code wasn't implemented and tests were not yet included. 

**My role and goal** was to **turn** this monolithic Shiny application **into a modular, maintainable codebase** using modules and pure R components. Furthermore, the aim was to write and document code in a way that several people can work on the project. Overall, my contribution led to a **~41% reduction** in total lines of code (~18.7k → ~11.13k LOC) while maintaining behaviour. The **Max file size** shrank from **10,651** lines to **2,884** lines (easier navigation & reviews) and the project is clearly separated between **UI modules** (`src/modules`) and **pure logic** (`src/R`) besides `ui.R`, `server.R`, `global.R` and `global-var.R`.

Besides this, **I implemented** `renv` for an **environment management** for developers and also implemented the use of `renv` within the CI/CD. Since in the future more than a single person works on this project, **I implemented formatting (`Air`) and lintering (`lintr`)** into the CI/CD and also into a pre-commit configuration, so that only code gets to the repository that shares the common styling and lintering. To further develop the state of the project, **I wrote unit tests** for `src/R` and **shiny tests for modules** in `src/modules`.

#### Stats after transitioning code

| dir          | n_files | n_funcs | min_LOC |  max_LOC |   mean_LOC | median_LOC |
|--------------|--------:|--------:|--------:|---------:|-----------:|-----------:|
| src/         |       4 |       9 |     229 |      479 |        312 |        270 |
| src/modules/ |       4 |      18 |     253 |     1142 |     604.75 |        512 |
| src/R/       |       8 |     121 |     222 |     2884 |     933.38 |      690.5 |
| **<TOTAL>**  |  **16** | **148** | **222** | **2884** | **695.88** |    **481** |

#### See more about the project: [Case study](notes/case-studies/2025-08-14-modularizing-large-shiny-app.md), 

### Levelling up the team's own R package

# DEBUG: MAKE THIS LIKE UNFOLDABLE (SO IT IS FOLDED AND THEN PEOPLE CAN EXPAND IT)

When I started working in a new company, I was quite excited that the team already used a common R package for the team to gather common functionality at a shared point. When I arrived the package included a clear package structure, but lacked on standardization (different code formatting in files, different styling formats), a separated logic of the package for users on one side and for contributors/maintainers on the other side as well as a CI/CD practice for versioning and releasing the package internally.

Hence, my first steps in this new package were three main goals:

1. Standardize the project layout and tooling for **consistency and quality**.
2. Introduce **CI/CD** to automate checks, builds, and releases.
3. Establish a **versioned install path for users** so older products remain stable.
4. Include unit tests with `testthat`

Regarding **standardization** of the project, I **split the logic** of the use for **users** (updated and clear **README.md**) and **contributors** (new instructions in **CONTRIBUTING.md**) with editor/CLI setup, instructions for the use of `Air` + `lintr`, and commit/release conventions. To **make the development consistent** across different contributors, **I implemented environment settings** with `renv` which can also be used together with `rig` on different versions of  R [see Case study](notes/case-studies/2025-09-19-debugging-multiple-R-versions-with-rig-and-renv.md). Furthermore, **I added formatting** with `Air` and **linting** with `lintr` as well as **checking a clean status of the environment** in the pre-commit check. Hence, code in the package follows now a clear pattern. 

To secure a safe use of the package when changes in the code happens, versioning is mandatory. Especially regarding the use in older products where a recent update of functionality might lead to crashes. Therefore, **I implemented a CI/CD** to **release new versions** of the package that can then be installed by team users with the package `pak` and specific versioning (i.e., `v0.13.1`). The **pipeline assures congruence with `renv`**, **formats** and **lint codes**, **checks coverage of tests** implemented, **builds** the package (inclusive manual landing in `dist/`) and **finally releases** the new version with its version tag. 

The **impact of this project** was large on the team: It made it possible that team members who are just users can install the packages in a native way with `pak` and its specific version. With this, there are also clearer roles and faster onboarding due to documented workflows. It assures reproducible builds and downloadable artifacts.

#### See more in the [case study](notes/case-studies/2025-09-14-nicverso-ci-overhaul.md)

## License
MIT (see `LICENSE`).
