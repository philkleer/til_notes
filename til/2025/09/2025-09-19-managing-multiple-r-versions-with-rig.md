# TIL: Managing multiple R versions with `rig`
_Date: 2025-09-19_

When you need to test packages/projects across different R versions, [`rig`](https://github.com/r-lib/rig) makes installs and switching dead simple.

## Why
- Install several R versions side-by-side.
- Switch the system/RStudio default quickly.
- Use symbolic names like `release`, `oldrel`, `devel`, `next`.

## Install
**macOS**
```bash
brew install --cask rig
# later: brew upgrade --cask rig
```

**Windows (WinGet)**
```powershell
winget install Posit.rig
```

**Linux**
- Debian/Ubuntu (APT repo), RPM, or tarball. See the README’s “Installation” section for exact commands for your distro.
```

## Core commands I used
```bash
# See what you can install
rig available

# Install a version (examples)
rig add release          # latest stable
rig add 4.4.1            # specific version

# List installed versions
rig list                 # alias: rig ls

# Make a version the default (terminal & RStudio)
rig default 4.4.1
rig default release

# Launch RStudio with a specific R
rig rstudio 4.4.1

# Remove an installed version
rig rm 4.3.3
```

### Nice touches
- Quick links let you run specific versions directly, e.g. `R-4.1` or `R-4.1.2`.
- On Ubuntu, `rig` expects R under `/opt/R/` (won’t detect APT-installed R).
- For VS Code terminals, setting `rig default <version>` changes the R you get when launching `R`.

### Tips
- Pair `rig` (R versions) with `renv` (per-project packages).
- For per-project R selection: open the project via `rig rstudio <version>` or switch with `rig default` before starting your IDE.

## References
- r-lib/rig README (features, install, quick links).  
- Command overview & aliases (`add/install`, `list/ls`, `default/switch`, `rm/del`).  
- macOS install via Homebrew cask.  
- Windows install via WinGet (`Posit.rig`).  
- Ubuntu note about `/opt/R/` vs APT installs.  
- VS Code terminal uses the current default set by `rig default`.
