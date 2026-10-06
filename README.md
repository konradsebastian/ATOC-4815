# ATOC 4815/5815 -- Fall 2026 course repo

Code, data-reading examples and the class Python environment for ATOC 4815/5815.
This repo is the new way to get course material -- in addition to Canvas, which stays
the official/graded site for assignments and grades.

## Get the environment (do this once)

```
git clone https://github.com/konradsebastian/ATOC-4815.git
cd ATOC-4815
mamba env create -f environment.yml      # or: conda env create -f environment.yml
conda activate atoc4815
```

If you don't have mamba/conda yet, install Miniforge first (Windows/Mac/Linux):
https://github.com/conda-forge/miniforge

## Staying up to date

Whenever new material is pushed here, just pull it:

```
git pull
```

## A note on conda vs. newer tools (uv, Poetry, ...)

You'll see faster, more modern alternatives like `uv` and `Poetry` in the wild.
We're sticking with conda/mamba for this class because several packages we rely on
(cartopy, pyhdf, netCDF4) depend on compiled, non-Python libraries (GEOS, PROJ, HDF)
that conda-forge builds and manages far more reliably across Windows/Mac/Linux than a
pure-pip resolver. Worth knowing they exist for your own projects later.

## Code in this repo

`code/` holds the lecture Python examples referenced in class (not homework solutions, not
grades, not student data — those stay on Canvas only).
