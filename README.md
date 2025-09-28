m# TIL & Project Overview

> Today I Learned — small, self-contained learning notes and tiny demos.  

**Personal page:** [https://github.com/philkleer](https://github.com/philkleer)

**Repo:** [https://github.com/philkleer/til_notes](https://github.com/philkleer/til_notes)

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
- 2025-09-14 — [Interactive graphics in R: ggiraph vs plotly](til/2025/08/2025-08-24-ggiraph-vs-plotly.md)
- 2025-09-14 — [Dual gates: Air + lintr on staged files and diffs](til/2025/09/2025-09-14-dual-gates-air-+-lintr-on-staged-files-and-diffs.md)
- 2025-09-14 — [R CMD check badge from CI (pure R)](til/2025/09/2025-09-07-r-cmd-check-badge-from-ci-(pure-r).md)
- 2025-09-14 — [Release automation with release-cli](til/2025/09/2025-09-10-release-automation-with-release-cli.md)
- 2025-09-02 — [GitLab CI for R packages: fast caches with pak](til/2025/09/2025-09-02-gitlab-ci-for-r-packages-fast-caches-with-pak.md)
- 2025-09-01 — [Users vs contributors: smooth install with pak](til/2025/09/2025-09-01-users-vs-contributors-smooth-install-with-pak.md)
- 2025-08-30 — [Leaflet in R and Python — beginner caveats](til/2025/08/2025-08-30-leaflet-r-vs-python-caveats.md)
- 2025-08-14 — [Shiny modularization — key lessons](til/2025/08/2025-08-14-modularization.md)
- 2025-08-01 — [Spatial in R: sf — beginner caveats](til/2025/08/2025-08-01-sf-vs-geopolars-caveats.md)

_Last updated: 2025-09-28 14:48 UTC_
<!-- END:INDEX -->

## 🌁 Project Overview

<details>

<summary><h3>⬇️ Restructuring Portal OBIA</h3></summary>

In this project, I worked on an initial version started by former colleagues for the [Observatório de Inteligência Artificial portal](https://obia.nic.br), which monitors AI use and development across federal organizations. **Before** I joined, the project was managed by a single person and **consisted of a monolithic Shiny application with just four files** and many duplicated code blocks (mean LOC: 4,685.25; max LOC: 10,651). There was a CI/CD process in place to deploy the application, but quality checks such as formatting and linting were not implemented, and no tests had been included yet.  

**My role and goal** was to **refactor** this monolithic Shiny application **into a modular, maintainable codebase** using modules and pure R components. In addition, the objective was to ensure the code was written and documented in a way that enabled multiple developers to collaborate effectively. Overall, my contribution led to a **~41% reduction** in total lines of code (~18.7k → ~11.13k LOC) **while including more functionality** like unit tests. The **largest file size** shrank from **10,651** lines to **2,884** lines (improving navigation and reviews), and the project is now clearly separated into **UI modules** (`src/modules`) and **pure logic** (`src/R`), alongside `ui.R`, `server.R`, `global.R`, and `global-var.R`.  

Additionally, **I implemented** `renv` for **environment management** to support developers, and integrated it into the CI/CD pipeline. Since the project would eventually involve multiple contributors, **I integrated formatting (`Air`) and linting (`lintr`)** into both CI/CD and a pre-commit configuration, ensuring that only code with consistent style and linting passes is committed. To further improve maintainability and quality, **I wrote unit tests** for `src/R` and **Shiny tests for modules** in `src/modules`.  


#### Stats after transitioning code

| dir          | n_files | n_funcs | min_LOC |  max_LOC |   mean_LOC | median_LOC |
|--------------|--------:|--------:|--------:|---------:|-----------:|-----------:|
| src/         |       4 |       9 |     229 |      479 |        312 |        270 |
| src/modules/ |       4 |      18 |     253 |     1142 |     604.75 |        512 |
| src/R/       |       8 |     121 |     222 |     2884 |     933.38 |      690.5 |
| **<TOTAL>**  |  **16** | **148** | **222** | **2884** | **695.88** |    **481** |

#### See more about the project: [Case study](notes/case-studies/2025-08-14-modularizing-large-shiny-app.md), 

</details>

<details>
<summary><h3>⬇️ Levelling up the team's own R package</h3></summary>

When I started at a new company, I was excited to see that the team was already using a shared R package to centralize common functionality. The package had a clear structure, but it lacked **standardization** (inconsistent formatting and styles across files), a clear separation of logic for **users vs. contributors/maintainers**, and a **CI/CD process** for versioning and internal releases.  

**My first goals** with the package were to:  
1. Standardize the project layout and tooling for **consistency and quality**.  
2. Introduce **CI/CD** to automate checks, builds, and releases.  
3. Establish a **versioned installation path for users**, ensuring older products remain stable.  
4. Add **unit tests** with `testthat`.  

To achieve **standardization**, I split the package logic between **users** (with an updated and clear **README.md**) and **contributors** (with a new **CONTRIBUTING.md**). Contributors received setup instructions for editor/CLI, guidance on `Air` + `lintr`, and conventions for commits and releases. To ensure consistent development across environments, I implemented **`renv` environment management** (compatible with `rig` for multiple R versions [see Case study](notes/case-studies/2025-09-19-debugging-multiple-R-versions-with-rig-and-renv.md)). Additionally, I enforced **formatting** with `Air`, **linting** with `lintr`, and **clean environment checks** via pre-commit hooks. This ensured that all contributions followed a unified style and reproducible environment setup.  

For **safe usage and stability**, I established a **versioning strategy**. This was crucial because many older products depended on the package, and updates could otherwise break functionality. I built a **CI/CD pipeline** that automatically formats and lints code, checks test coverage, builds the package (including a manual landing in `dist/`), and finally **releases a tagged version** (e.g., `v0.13.1`). Team members could then install specific versions directly using `pak`, ensuring both stability and reproducibility.  

The **impact** of this work was significant: team members could now install the package natively with version control, onboarding became faster thanks to clear documentation, and the pipeline guaranteed **reproducible builds** with downloadable artifacts. This established clear roles for **users vs. contributors** and made the overall workflow more reliable and scalable.  

#### See more in the [case study](notes/case-studies/2025-09-14-nicverso-ci-overhaul.md)

</details>

## License
MIT (see `LICENSE`).
