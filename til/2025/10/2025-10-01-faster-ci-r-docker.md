# TIL: Speeding up R CI pipelines with a custom Docker image
_Date: 2025-10-01_

## Context
For the [**nicverso** project](../../../notes/case-studies/2025-09-14-nicverso-ci-overhaul.md), I implemented automated releases of versions. Initially I used `rocker/r-ver` images (e.g. `rocker/r-ver:4.4.1`) to pin R versions. But this meant that on every CI run, all required R packages had to be installed **from scratch**, which made the pipeline slow.

## Problem
- Jobs took long because packages were built/installed on every run (and their Debian pendants).  
- The `rocker/r-ver` images are minimal, so nothing comes preinstalled.

## Solution
I created a **custom Dockerfile** and `docker-compose.yml` to define my own image:  
- Based on the required `rocker/r-ver` tag.  
- Pre-installed all the project’s critical R packages (via `renv::restore()`).  
- Pushed this image to our registry.  

Then in the CI/CD workflow:  
- Instead of pulling `rocker/r-ver:4.5.1`, the pipeline pulls my pre-built image.  
- CI runs start faster because the packages are already present in the container.
- Image gets build automatically new, if there is a change in `renv.lock`, `Dockerfile`, or `docker-compose.yaml`

## Results
- Dramatically reduced CI run time (minutes saved on every build).  
- More predictable builds, since the Docker image pins both **R version** and **package versions**.  
- Team members can use the same image locally via `docker-compose up`, ensuring dev/prod parity.

## Lessons Learned
- **Base images are great for flexibility**, but custom images pay off when pipelines run often.  
- Pinning both R and package versions gives reproducible, fast CI.  
- The same image can be reused in development, CI, and deployment.
