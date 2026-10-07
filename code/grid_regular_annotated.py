"""
grid_regular_annotated.py
--------------------------
Annotated version of grid_regular.py (ATOC 4815/5815, gridding tutorial).

WHAT THIS SCRIPT DOES
----------------------
Builds a regular lat/lon grid over a small test image (a WorldView
satellite snapshot, `test.png`) and demonstrates the two core moves
you'll need for the homework:

  1) Defining a regular target grid two ways -- as cell BOUNDARIES and
     as cell MIDPOINTS -- and checking, visually, that the grid you
     built actually lines up with the real data (the image's own pixel
     grid).
  2) Taking one arbitrary (not-on-the-grid) data point and figuring out
     which grid cell it belongs in, using a nearest-index lookup.

In the homework, this exact pattern -- build boundaries/midpoints, then
assign each data point to its nearest cell -- is what you'll use to
grid the scattered MODIS altitude points from modis_terrain_corrected.py
onto a real 1 km geographic grid (and, later, to grid reanalysis weather
fields). Here, we practice it on an image because an image already *is*
regularly gridded, so we can sanity-check our math against ground truth
we can literally see.

WHY AN IMAGE?
--------------
A PNG is just a regular array of pixels. If we define our own lat/lon
grid to match the image's known geographic extent (`wesn`), we can
verify our grid construction by overlaying it on the image and
confirming the lines and points land exactly where they should. That
same grid-construction code is what you'll reuse on real (non-image)
scattered data in the homework -- except there, there's no image to
check against, so getting the boundaries/midpoints math right *here*,
where you can see it, is what makes it trustworthy there.
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

png = '../dat/test.png'

# wesn = [West, East, South, North] -- the geographic bounding box that
# this image covers. This plays the same role as the `flt =
# np.where((lat > 38) & ...)` crop in modis_terrain_corrected.py: it's
# how we tell the code "here is the region we're gridding."
wesn = [-105.7756, -105.7006, 46.0743, 46.1252]

# Load image: a WorldView satellite image, already on its own regular
# pixel grid. img.shape is (rows, cols, channels) = (ny, nx, 3) for an
# RGB image.
img = mpimg.imread(png)

# Make plot of WorldView background, telling matplotlib the image's
# real-world extent via `extent=wesn` so pixel coordinates on screen
# correspond to actual lon/lat.
plt.imshow(img, extent=wesn)
plt.xlim(wesn[0] - 0.01, wesn[1] + 0.01)
plt.ylim(wesn[2] - 0.01, wesn[3] + 0.01)
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# -----------------------------------------------------------------
# STEP 1: Assign a lat/lon grid to the WorldView image
# -----------------------------------------------------------------
# nx, ny = number of pixels (columns, rows) in the image. This is the
# "resolution" of our target grid. In the homework, this becomes the
# number of grid cells you choose for your 1 km target grid, instead
# of being handed to you by an image's shape.
nx = img.shape[1]
ny = img.shape[0]

# *** BOUNDARIES vs. MIDPOINTS -- the key distinction of this whole
# tutorial ***
#
# For nx pixels (cells), there are nx+1 BOUNDARIES between/around them
# -- think of a fence with nx fields needing nx+1 fence posts. x and y
# below are those boundary coordinates, running from the west edge to
# the east edge (x) and south edge to north edge (y).
x = np.linspace(wesn[0], wesn[1], nx + 1)  # nx+1 boundaries, W to E
y = np.linspace(wesn[2], wesn[3], ny + 1)  # ny+1 boundaries, S to N

# xm, ym = MIDPOINTS of each cell -- the single representative
# coordinate for "the center of grid cell i". There are exactly nx (not
# nx+1) midpoints, one per cell, each the average of the two boundaries
# on either side of it.
xm = (x[1:] + x[:-1]) * 0.5  # x mid-points (length nx)
ym = (y[1:] + y[:-1]) * 0.5  # y mid-points (length ny)

# Sanity check #1 (green dots): overplot one row of midpoints. If the
# grid construction above is correct, these should sit exactly in the
# middle of one row of image pixels -- not on a boundary line.
plt.scatter(np.repeat(xm[0], ny), ym, color='green')

# Sanity check #2 (red lines): plot every column BOUNDARY as a
# vertical line. If correct, these should run exactly along the edges
# between pixel columns, not through the middle of any pixel.
for i, x0 in enumerate(x):
    plt.plot(np.repeat(x0, ny + 1), y, 'r-')

# -----------------------------------------------------------------
# STEP 2: "Grid" a new, arbitrary data point
# -----------------------------------------------------------------
# This is the part that generalizes directly to the homework: given
# ONE scattered (lon, lat) point that does NOT fall exactly on our
# grid, which grid cell does it belong to?
#
# In the homework, you will do this for every MODIS altitude point
# (thousands of them, from modis_terrain_corrected.py) instead of just
# one -- typically in a loop, or vectorized -- and then AVERAGE the
# altitude values that land in each cell to produce one gridded value
# per cell.
xs = -105.7368
ys = 46.093

# --- Naive approach (commented out on purpose) ---
# You could try to compute the index directly with arithmetic, assuming
# the grid spacing is perfectly uniform:
#
#   xind = int((xs - wesn[0]) / (x[1] - x[0]))
#   yind = int((ys - wesn[2]) / (y[1] - y[0]))
#
# This WORKS for a perfectly regular grid like this one, but it is
# fragile: it silently assumes uniform spacing, it can be off by one
# at cell edges due to floating-point rounding, and it breaks outright
# if you ever grid onto a non-uniform grid (e.g. one defined in a
# different map projection, or with variable resolution). It's left
# here, commented out, as a cautionary example -- not as code to copy.

# --- Robust approach (what we actually use, and what you should use
# in the homework) ---
# np.argmin(np.abs(x - xs)) finds, among ALL the boundary coordinates
# in x, the single index whose value is closest to xs. This works
# regardless of whether the grid is uniform, and it's the same idea
# you'll use to find the nearest grid index for every MODIS point in
# the homework.
xind = np.argmin(np.abs(x - xs))
yind = np.argmin(np.abs(y - ys))

print(xind, yind)

# Sanity check #3 (blue dot): the actual data point we're gridding.
plt.scatter(xs, ys, color='blue')
# Sanity check #4 (red dot): the nearest grid BOUNDARY corner to that
# point -- should land visibly close to the blue dot if argmin worked.
plt.scatter(x[xind], y[yind], color='red')
# Sanity check #5 (green dot): the MIDPOINT of the cell the point was
# assigned to -- this is "the gridded location" you'd actually report
# or average into, in the homework.
plt.scatter(xm[xind], ym[yind], color='green')

# Because this image already has a real, known value at every pixel,
# we can use it to verify the indices we computed are correct: pull
# the green-channel pixel value at (xind, yind) directly out of the
# image array. Note the `ny-1-yind` -- image arrays are indexed from
# the TOP-left corner (row 0 = north), while our y boundaries/midpoints
# were built from south to north, so the row index has to be flipped.
# This exact row-order gotcha is worth remembering: it's a common
# source of "my grid looks upside-down" bugs when gridding real data,
# including in the homework.
green_at_grid_cell = img[ny - 1 - yind, xind, 2]
print(green_at_grid_cell)
