---
title: "Users vs contributors: smooth install with pak"
date: 2025-09-01
tags: [r, gitlab-ci, nicverso, pak]
---

- Contributors use MR pipelines; users install a specific version with one line.
- Examples: `pak::pkg_install('gitlab:group/nicverso')` or `@v1.2.3` for pinned builds.
- Prevents breaking older projects when the package evolves.

Full write-up: ../../../../notes/case-studies/2025-09-14-nicverso-ci-overhaul.md
