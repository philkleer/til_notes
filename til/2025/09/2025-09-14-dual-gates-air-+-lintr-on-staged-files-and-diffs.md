---
title: "Dual gates: Air + lintr on staged files and diffs"
date: 2025-09-14
tags: [r, gitlab-ci, nicverso, pak]
---

- Run **Air** + **lintr** on staged files via `pre-commit` for local feedback.
- Add a `pre-push` hook that checks only files changed vs `origin/<default-branch>`.
- Keeps the main branch clean without slowing down the entire tree.

Full write-up: ../../../../notes/case-studies/2025-09-14-nicverso-ci-overhaul.md
