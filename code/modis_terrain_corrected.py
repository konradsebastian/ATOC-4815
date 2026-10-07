"""
modis_terrain_corrected.py
---------------------------
Corrected, annotated version of modis_terrain.py (ATOC 4815/5815).

WHAT THIS SCRIPT DOES
----------------------
Reads MODIS geolocation data (the MOD03 product: latitude, longitude,
and terrain height for every pixel in one satellite "swath") and makes
two plots:

  Figure 0: a geographic overview of the whole swath -- a cartopy
            contour map of altitude, drawn on top of country borders.
  Figure 1: a flattened, cropped scatter plot of the same data, zoomed
            into a small region over Colorado / the Rockies.

Both plots exist so we can LOOK at the data in its native form before
doing anything more sophisticated with it. MODIS pixels are NOT laid
out on a simple rectangular lat/lon grid -- the satellite's scan
geometry makes the data form a curved, irregular ("non-rectilinear")
swath. That is exactly the kind of data we will need to re-grid onto a
clean, regular 1 km geographic grid in the upcoming homework, using the
same gridding approach we built together in grid_regular.py in class
today (grid-cell BOUNDARIES vs. MIDPOINTS, and a np.argmin()-based
nearest-index lookup). This script stops short of doing that regridding
-- it is just the "look at the raw data first" step that comes before it.

WHAT WAS BROKEN, AND WHY
--------------------------
This line used to run fine in the old class environment:

    ax.contour(lon, lat, alt, 20, projection=cartopy.crs.PlateCarree())

In the new `atoc4815` environment (newer matplotlib), it raises:

    AttributeError: QuadContourSet.set() got an unexpected keyword
    argument 'projection'

Here is why:

  - cartopy GeoAxes methods like .contour() do not accept a
    `projection` keyword at all. `projection=` is for *creating axes*
    (plt.axes(projection=...)). The keyword that tells a plotting call
    "the coordinates I'm handing you are in THIS coordinate system" is
    `transform=`.
  - `projection=` was ALWAYS the wrong keyword on .contour(). But older
    matplotlib versions let unrecognized keyword arguments quietly fall
    through to Artist.set(...) and silently ignored anything that did
    not match a real property. So the plot still appeared -- and it
    never actually needed a transform anyway, since our MOD03 lon/lat
    values are already in Plate Carree, the same projection as the axes.
  - Newer matplotlib tightened Artist.set() to RAISE on any keyword it
    does not recognize, instead of silently dropping it. So the exact
    same (always-slightly-wrong) line now fails loudly instead of
    quietly doing nothing.

The fix is simply the correct keyword:

    ax.contour(lon, lat, alt, 20, transform=cartopy.crs.PlateCarree())

TEACHING POINT: "it ran fine before" does not mean "it was correct
before." A newer, stricter library version often catches a mistake
that an older, more permissive version let slide silently. Don't
assume an upgrade broke your code just because an error appeared --
sometimes the upgrade just revealed a bug that was there all along.
"""

import matplotlib.pyplot as plt
import numpy as np
from pyhdf.SD import SD, SDC
import cartopy

# ---------------------------------------------------------------------
# 1) Read the raw MODIS geolocation product (MOD03)
# ---------------------------------------------------------------------
# MOD03 stores, for every pixel of one satellite swath, its latitude,
# longitude, and the terrain height ("Height") below it. Unlike a
# weather-model grid, these lat/lon values are NOT evenly spaced --
# they trace out the curved path the instrument actually scanned.
file = '../dat/MOD03.A2017233.1745.006.2017234003402.hdf'
file = SD(file, SDC.READ)

sds = file.select('Latitude')     # select the Latitude science dataset (SDS)
lat = sds.get()                   # pull it into a numpy array
sds = file.select('Longitude')
lon = sds.get()
sds = file.select('Height')       # terrain altitude at each pixel (meters)
alt = sds.get()

# ---------------------------------------------------------------------
# 2) Figure 0: geographic overview (sanity check of the whole swath)
# ---------------------------------------------------------------------
# Step one of "look at the data before gridding it": draw the swath on
# an actual map, so we can see its shape and extent and confirm lat,
# lon, and alt line up the way we expect.
plt.figure(0)
ax = plt.axes(projection=cartopy.crs.PlateCarree())   # <-- `projection=` IS
                                                       #     correct HERE --
                                                       #     this call creates
                                                       #     the map axes
                                                       #     themselves.
ax.add_feature(cartopy.feature.BORDERS)

# `transform=` tells cartopy what coordinate system lon/lat/alt are
# ALREADY expressed in, so it can correctly project them onto the map.
# *** This is the line that was broken: it used to say `projection=...`
# here, and .contour() does not accept that keyword. ***
ax.contour(lon, lat, alt, 20, transform=cartopy.crs.PlateCarree())

# ---------------------------------------------------------------------
# 3) Flatten and crop: turn the 2D swath into a simple list of points
# ---------------------------------------------------------------------
# lat, lon, and alt are each 2D arrays, shaped like the satellite's scan
# pattern (along-track x cross-track). For gridding -- and for the
# homework -- it is easier to work with a flat (1D) list of
# (lon, lat, alt) points: exactly the "scattered input points" we
# talked about alongside grid_regular.py. np.ravel() does the flattening.
lat = np.ravel(lat)
lon = np.ravel(lon)
alt = np.ravel(alt)

# Crop down to a small region of interest (roughly the Colorado Front
# Range / Rockies) so the next plot -- and the eventual homework
# gridding -- is not working with the whole globe's worth of pixels.
# This plays the same role as the `wesn` (west/east/south/north)
# bounding box that defined your target grid's extent in grid_regular.py.
flt = np.where((lat > 38) & (lat < 42) & (lon > -110) & (lon < -100))
lat = lat[flt]
lon = lon[flt]
alt = alt[flt]

# ---------------------------------------------------------------------
# 4) Figure 1: scattered points -- this is what we will grid next
# ---------------------------------------------------------------------
# THIS is the picture that matters for the homework: a cloud of
# scattered (lon, lat) points, each carrying an altitude value, that do
# NOT fall on any regular grid. Recall from grid_regular.py how we built
# a regular TARGET grid:
#     x, y    = cell BOUNDARIES  (np.linspace over the wesn box,
#                                  length nx+1 / ny+1)
#     xm, ym  = cell MIDPOINTS   ((x[1:] + x[:-1]) * 0.5, length nx/ny)
# and assigned each scattered point to its nearest grid cell with the
# nearest-index lookup:
#     ix = np.argmin(np.abs(x - xs))
# In the upcoming homework, you will do exactly that with the lon/lat/alt
# points plotted below: build a 1 km target grid the same way, then use
# that nearest-midpoint lookup to average all the MODIS altitude points
# landing in each grid cell. For now, this plot is only the "before"
# picture -- scattered data, not yet gridded.
plt.figure(1)
plt.scatter(lon, lat, c=alt, cmap='terrain', vmin=-1000, vmax=4500)
plt.show()
