# Case Study: Debugging across multiple R versions with `rig` + `renv`
_Date: 2025-09-19_

## Context
I was working on a package that depends on `dplyr`. On my machine, everything ran smoothly with R **4.4.1**. But when a collaborator (on R **4.3.3**) tried the same code, they hit an error related to data frame printing. This highlighted the classic problem: code that works in one R version may behave differently in another.

## Problem
- Collaborator’s R 4.3.3 session failed with:
  ```
  Error in format.data.frame(...) : argument "..." is missing, with no default
  ```
- My R 4.4.1 session showed no error.

## Using `rig` to reproduce quickly
```bash
# What was already installed?
rig list
#> 4.4.1 (default)

# Install the older release my collaborator was using
rig add 4.3.3

# Switch temporarily
rig default 4.3.3

# Launch R and run the same script
Rscript my_analysis.R
```
Sure enough, the error reproduced under 4.3.3.

---

## Using `renv` together with `rig`
There are two common strategies to manage environments per R version:

### Option A — **Profiles** (multiple environments in the same repo)
`renv` supports **profiles**, which let you keep more than one independent environment **in the same project** (one active at a time). This is perfect for testing on R 4.3 vs 4.4 without cloning the repo.

**Initialize once (default profile):**
```r
# In an interactive R session (any R version)
install.packages("renv")
renv::init()
```

**Create and use a profile for R 4.3 (Linux/macOS shell):**
```bash
rig default 4.3.3
export RENV_PROFILE=r-4.3
R -q -e 'renv::restore()'          # installs packages for this profile & R version
R -q -e 'renv::snapshot()'         # writes a lockfile for this profile
```

**Create and use a profile for R 4.4:**
```bash
rig default 4.4.1
export RENV_PROFILE=r-4.4
R -q -e 'renv::restore()'
R -q -e 'renv::snapshot()'
```

**On Windows (PowerShell) replace `export` with:**
```powershell
$env:RENV_PROFILE="r-4.3"
R -q -e "renv::restore(); renv::snapshot()"

$env:RENV_PROFILE="r-4.4"
R -q -e "renv::restore(); renv::snapshot()"
```

**What this gives you**
- Each profile has its own library and lockfile (stored under `renv/profiles/<name>/renv.lock`).
- `renv` also caches binaries **by R version**, so packages for R 4.3 and 4.4 are fully isolated.
- Switch profiles by changing the `RENV_PROFILE` environment variable. Only one profile is active at a time.

**Helpful patterns**
- Add tiny helper scripts to the repo:
  - `tools/use-r-4.3.sh` → sets `RENV_PROFILE=r-4.3`, runs `rig default 4.3.3`, launches RStudio with that version.
  - `tools/use-r-4.4.sh` → same idea for 4.4.1.
- In CI, run a **matrix** over R versions and set `RENV_PROFILE` accordingly.

### Option B — **Separate clones** (one environment per checkout)
Keep two copies of the repo (e.g., `proj-r43/` and `proj-r44/`). Each has its own single `renv` environment. Switch R with `rig default` before working in a checkout. This is simpler but doubles the working directories.

---

## Answering the key question
> *“In a project I couldn't switch R version and then create a second renv… can I define different environments for different R versions in one project?”*

- **By default:** a project has **one** `renv` environment and **one** lockfile, so you can’t have two active environments at the same time.
- **Use profiles to achieve this:** with `RENV_PROFILE`, you can maintain **multiple** independent `renv` environments **in the same project** (e.g., `r-4.3` and `r-4.4`). You switch between them by setting the environment variable before running R or your IDE.
- `renv` will warn if the project’s lockfile R version doesn’t match your current interpreter; profiles avoid that mismatch and keep things clean.

---

## Resolution (back to the bug)
- I created two profiles, reproduced the bug under `r-4.3`, and confirmed it was tied to an older dependency version.
- After updating the package set in the `r-4.3` profile, the script ran without errors.
- Final step to return to my daily setup:
  ```bash
  rig default 4.4.1
  export RENV_PROFILE=r-4.4
  ```

## Takeaways
- Use `rig` to install/switch R versions fast.
- Use `renv` **profiles** (or separate clones) to keep per-R-version environments reproducible.
- Automate with CI matrices so every PR runs on `release` and `oldrel`.

## Quick command recap
```bash
# Install and list R versions
rig add 4.3.3
rig add 4.4.1
rig list

# Switch R and set the matching profile
rig default 4.3.3
export RENV_PROFILE=r-4.3    # PowerShell: $env:RENV_PROFILE="r-4.3"

# Restore deps for that profile under that R
R -q -e 'renv::restore(); renv::snapshot()'

# Repeat for the other R version
rig default 4.4.1
export RENV_PROFILE=r-4.4
R -q -e 'renv::restore(); renv::snapshot()'
```

## References
- `renv` Profiles: multiple environments per project (set via `RENV_PROFILE`).
- Lockfiles record the R version used; caches are isolated per R version.
- `rig` handles side-by-side R installations and IDE launching.
