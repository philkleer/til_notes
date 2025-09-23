---
title: "From ad‑hoc repo to versioned, CI‑driven R package: nicverso"
date: 2025-09-14
tags: [r, package, gitlab-ci, release, refactoring]
---

<img src="../../assets/nicverso/hex.png" align="right" width="140" alt="nicverso hex" />


## Context
The `nicverso` package (*not public*) started as a plain repo that teammates cloned and deployed manually without any standardization of code within the package, formatting, lintering or versioning of the package. Furthermore, there was no clear split between **contributors** (who change code) and **users** (who only install/use), and breaking changes could ship unnoticed.

## Goals
- Standardize the project layout and tooling for **consistency and quality**.
- Introduce **CI/CD** to automate checks, builds, and releases.
- Establish a **versioned install path for users** so older products remain stable.

## What I changed
### 1. Standardization & docs
- Adopted `devtools`, `roxygen2`, `testthat` (edition 3).
- Added a full **README.md** and a **CONTRIBUTING.md** with editor/CLI setup, `Air` + `lintr` usage, and commit/release conventions.
- Codified style: **Air** (formatter) + **lintr** (static analysis), even as pre-commit check so that no dirty code lands in the repository
- Added `renv` so that developers work in the same environment

### 2. Pre-commit & pre-push hooks
- `.pre-commit-config.yaml` runs `Air`/`lintr` on staged files (**pre-commit**) and on diffs vs. default branch (**pre-push**) to keep the main branch clean without slowing developers.

### 3. CI/CD with GitLab
- Added a release CI/CD so that versions get released and the package can be loaded from different versions once code changes largely but old versions are still used in functioning products
- **Image**: `rocker/r-ver:4.5.1` to assure version in congruence with `renv`
- **Stages**: `lint` → `check` → `coverage` → `build` → `release`.
- **Coverage**: `covr::package_coverage()` prints a single `Total: NN.N%` line for CI parsing.
- **Build**: `devtools::build()` tarball + `build_manual()`; keeps artifacts in `dist/`.
- **Release**: tags `vX.Y.Z` via `release-cli` and publishes links to the exact build job artifacts.
- **Pages**: publishes simple SVG badges (check status, current release) under `public/`.
- **Safety**: a `workflow: rules` block prevents double pipelines on tags created by the API.

### 4. Users vs contributors
- **Contributors** work via MR pipelines and follow style gates automatically via pre-commit.
- **Users** install **versioned** builds with `pak` (examples):

  ```r
  # Install latest release
  pak::pkg_install("gitlab:group/nicverso")

  # Or pin a specific version by tag
  pak::pkg_install("gitlab:group/nicverso@v1.2.3")
  ```

## Impact
- Predictable installs for users; older products can pin version `vX.Y.Z`.
- Fewer regressions: code style + lint + check + coverage run in CI.
- Clearer roles and faster onboarding due to documented workflows.
- Reproducible builds and downloadable artifacts (tarball + manual PDF).

## Lessons learned
- **Cache smartly**: key on files that change dependency graphs (e.g., `DESCRIPTION`), not the whole tree.
- **Gate on diffs**: running `Air`/`lintr` only on changed files scales better and keeps feedback tight.
- **Link releases to artifacts**: end users love a stable URL to the exact tarball/manual.
- **Keep release triggers explicit**: a conventional commit message (e.g., `new version vX.Y.Z`) keeps pipelines predictable.

## Next steps
- Add CRON job for revdep checks on key dependencies.
- Track coverage trend over time; fail the build on large drops.

## Public disclosure note
This write-up is **code-free** and describes techniques, not proprietary logic or data. It is safe to publish publicly and to discuss at a high level in a portfolio.
