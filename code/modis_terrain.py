import matplotlib.pyplot as plt
import numpy as np
from pyhdf.SD import SD, SDC
import cartopy
file='../dat/MOD03.A2017233.1745.006.2017234003402.hdf'
file = SD(file, SDC.READ)

# Get data    
sds = file.select('Latitude') # select sds
lat = sds.get() # get sds data
sds = file.select('Longitude') # select sds
lon = sds.get() # get sds data
sds = file.select('Height') # select sds
alt = sds.get() # get sds data

# plt.figure(0)
ax = plt.axes(projection=cartopy.crs.PlateCarree())
ax.add_feature(cartopy.feature.BORDERS)
ax.contour(lon,lat,alt,20,projection=cartopy.crs.PlateCarree())

# # Flatten lat, lon, and data to prepare scatter plot
# lat=np.ravel(lat)
# lon=np.ravel(lon)
# alt=np.ravel(alt)

# flt=np.where((lat > 38) & (lat < 42) & (lon >-110) & (lon <-100))
# lat=lat[flt]
# lon=lon[flt]
# alt=alt[flt]

# plt.figure(1)
# plt.scatter(lon,lat,c=alt,cmap='terrain',vmin=-1000,vmax=4500)
# plt.show()
