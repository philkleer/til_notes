---
title: "GitLab CI for R packages: fast caches with pak"
date: 2025-09-02
tags: [r, gitlab-ci, nicverso, pak]
---

- Cache R libraries keyed by `DESCRIPTION`/`NAMESPACE` to avoid full reinstalls.
- Use `pak::pkg_sysreqs('local::.')` to prefetch system deps in CI.
- A stable base image like `rocker/r2u:jammy` speeds up `apt` + R binary installs.
- Result: checks/builds run in minutes instead of tens of minutes.

Full write-up: ../../../../notes/case-studies/2025-09-14-nicverso-ci-overhaul.md
