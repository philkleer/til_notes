---
title: "Release automation with release-cli"
date: 2025-09-14
tags: [r, gitlab-ci, nicverso, pak]
---

- Tag releases as `vX.Y.Z` and link artifacts (tarball/manual) to the *build job* that produced them.
- Avoid duplicate pipelines on API-created tags via `workflow: rules`.

Full write-up: ../../../../notes/case-studies/2025-09-14-nicverso-ci-overhaul.md
