---
title: "From ad‑hoc repo to versioned, CI‑driven R package: nicverso"
date: 2025-09-14
tags: [r, package, gitlab-ci, release, refactoring]
---

<img src="../../assets/nicverso/hex.png" align="right" width="140" alt="nicverso hex" />


## Context
The `nicverso` package (*not public*) started as a plain repo that teammates cloned and deployed manually. There was no clear split between **contributors** (who change code) and **users** (who only install/use), and breaking changes could ship unnoticed.

## Goals
- Standardize the project layout and tooling for **consistency and quality**.
- Introduce **CI/CD** to automate checks, builds, and releases.
- Establish a **versioned install path for users** so older products remain stable.

## What I changed
### 1. Standardization & docs
- Adopted `devtools`, `roxygen2`, `testthat` (edition 3).
- Added a full **README** and a **CONTRIBUTING.md** (Portuguese) with editor/CLI setup, Air + lintr usage, and commit/release conventions.
- Codified style: **Air** (formatter) + **lintr** (static analysis).

### 2. Pre-commit & pre-push hooks
- `.pre-commit-config.yaml` runs Air/lintr on staged files (**pre-commit**) and on diffs vs default branch (**pre-push**) to keep the main branch clean without slowing developers.

### 3. CI/CD with GitLab
- **Image**: `rocker/r2u:jammy` (fast apt + r2u binaries).
- **Stages**: `lint` → `check` → `coverage` → `build` → `release`.
- **Caching**: keyed by `DESCRIPTION`/`NAMESPACE` so installs are fast, reusing `/usr/local/lib/R/site-library`/`$R_LIBS_USER`.

- **Check**: `rcmdcheck --as-cran` with `_R_CHECK_FORCE_SUGGESTS_=false`.
- **Coverage**: `covr::package_coverage()` prints a single `Total: NN.N%` line for CI parsing.
- **Build**: `devtools::build()` tarball + `build_manual()`; keeps artifacts in `dist/`.
- **Release**: tags `vX.Y.Z` via `release-cli` and publishes links to the exact build job artifacts.
- **Pages**: publishes simple SVG badges (check status, current release) under `public/`.
- **Safety**: a `workflow: rules` block prevents double pipelines on tags created by the API.

### 4. Users vs contributors
- **Contributors** work via MR pipelines and follow style gates automatically.
- **Users** install **versioned** builds with `pak` (examples):

  ```r
  # Install latest release
  pak::pkg_install("gitlab:group/nicverso")

  # Or pin a specific version by tag
  pak::pkg_install("gitlab:group/nicverso@v1.2.3")
  ```

## Impact
- Predictable installs for users; older products can pin `vX.Y.Z`.
- Fewer regressions: code style + lint + check + coverage run in CI.
- Clearer roles and faster onboarding due to documented workflows.
- Reproducible builds and downloadable artifacts (tarball + manual PDF).

## Lessons learned
- **Cache smartly**: key on files that change dependency graphs (e.g., `DESCRIPTION`), not the whole tree.
- **Gate on diffs**: running Air/lintr only on changed files scales better and keeps feedback tight.
- **Link releases to artifacts**: end users love a stable URL to the exact tarball/manual.
- **Keep release triggers explicit**: a conventional commit message (e.g., `new version vX.Y.Z`) keeps pipelines predictable.

## Next steps
- Add CRON job for revdep checks on key dependencies.
- Track coverage trend over time; fail the build on large drops.

## Appendix (sanitized snippets)
**Stages**
```yaml
stages: [lint, check, coverage, build, release]
```

**Coverage job**
```yaml
coverage: '/^Total:\s+(\d+(?:\.\d+)?)%$/'
```

**Install for users**
```r
pak::pkg_install("gitlab:group/nicverso@v1.2.3")
```
