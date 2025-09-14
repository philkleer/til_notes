---
title: "Python packaging with Poetry — quick start & pitfalls (for R package devs)"
date: 2025-09-30
tags: [python, packaging, poetry, pyproject, pytest]
---

**TL;DR**  
Use **Poetry** to manage virtualenvs + dependencies + build from **`pyproject.toml`**. Prefer the **`src/` layout**, pin a Python version, and expose a console script via `tool.poetry.scripts`.

## Quick start
```bash
# install poetry once (platform-specific; see docs) then:
poetry new --src mypkg
cd mypkg

# set Python version constraint and project metadata
# (edits to pyproject.toml shown below)

# add runtime deps and dev tools
poetry add requests
poetry add --group dev pytest

# run inside the managed venv
poetry run pytest
poetry run python -m mypkg

# build & publish (TestPyPI as a safe first step)
poetry build
poetry publish -r testpypi  # configure token once via 'poetry config'
```

## `pyproject.toml` essentials (PEP 621 + Poetry)
```toml
[tool.poetry]
name = "mypkg"
version = "0.1.0"
description = "Example package"
authors = ["Your Name <you@example.com>"]
readme = "README.md"
packages = [{
  include = "mypkg",
  from = "src"
}]

[tool.poetry.dependencies]
python = ">=3.10,<3.14"
requests = "^2"

[tool.poetry.group.dev.dependencies]
pytest = "^8"

[tool.poetry.scripts]
mypkg = "mypkg.__main__:main"   # console script

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## Layout
```
src/
  mypkg/
    __init__.py
    __main__.py   # entry point
tests/
  test_basic.py
```

## Pitfalls (coming from R)
- **Lock & venv**: Poetry maintains `.venv` and `poetry.lock`. Commit the lock for apps; for libraries it’s optional.
- **`src/` layout**: ensures tests import the installed package, not local files. (Common gotcha.)
- **Package data**: add via `include`/`exclude` in `tool.poetry` or `MANIFEST.in` if you need non-code files.
- **Versioning**: bump in `pyproject.toml` (SemVer). Tag releases just like R releases.
- **Entry points**: declare console scripts in `[tool.poetry.scripts]` (Python equivalent of R `exec`). 
- **Relative imports**: keep package imports absolute (`from mypkg import foo`) to avoid path confusion.
- **CI**: use `poetry install --no-interaction --no-root` + `poetry build`. Cache `.venv` or Poetry cache by keying on `pyproject.toml`.

## R ↔ Python mental model
- `DESCRIPTION` → `pyproject.toml`  
- `devtools::build()` → `poetry build`  
- `testthat` → `pytest`  
- `NAMESPACE` → `__init__.py` + explicit exports (`__all__`)  
- vignettes → sphinx/markdown docs or examples folder
