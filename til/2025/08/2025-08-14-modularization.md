---
title: "Shiny modularization — key lessons"
date: 2025-08-14
tags: [r, shiny, refactoring, modularization]
---

- Shiny modules (`mod_*_ui/server`) create clear boundaries and shrink files.
- Extracting pure functions to `src/R` makes logic testable; UI stays thin.
- Namespacing with `NS(id)` prevents ID collisions and wiring bugs.
- Smaller files + consistent naming make reviews/onboarding faster.

Full write-up: ../../../../notes/case-studies/2025-08-14-modularizing-large-shiny-app.md
