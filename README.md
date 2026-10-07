# ATOC 4815/5815 -- Fall 2026 course repo

Code, data-reading examples and the class Python environment for ATOC 4815/5815.
This repo is the new way to get course material -- in addition to Canvas, which stays
the official/graded site for assignments and grades.

## Get the environment (do this once)

```
git clone https://github.com/konradsebastian/ATOC-4815.git
cd ATOC-4815
conda env create -f environment.yml      # have mamba? it's faster: mamba env create -f environment.yml
conda activate atoc4815
```

If you don't have mamba/conda yet, install Miniforge first (Windows/Mac/Linux):
https://github.com/conda-forge/miniforge

### Mac + Anaconda Navigator users: one extra step

If you plan to launch Jupyter Notebook by clicking "Launch" in Anaconda Navigator
(rather than typing `jupyter notebook` yourself), run this once, right after the
`conda env create` step above:

```
bash fix_navigator_mac.sh
```

Without it, Navigator's Notebook button will fail with an error like "The file
.../atoc4815/bin/jupyter_mac.command does not exist." That's because our environment
installs `notebook` from conda-forge (for the best Apple-Silicon support), and
conda-forge's build doesn't include the small launcher script Navigator looks for the
way Anaconda's own build does -- `notebook` itself works fine either way. The script
just adds that one file back. If you're launching from a terminal instead (`jupyter
notebook` or `jupyter lab`), you don't need this step at all.

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
