boulder_sat.pyimport matplotlib.pyplot as plt
from cartopy.io.img_tiles import OSM
import cartopy.crs as ccrs
import scipy.io as io

#lon, lat, d, zoom = -105.24360, 40.00999, 0.002, 16 # Boulder, SEEC
lon, lat, d, zoom = 14.41, 50.0875, 0.004, 17 # Prague

extent = [lon - 2*d, lon + 2*d, lat - d, lat + d]

request = OSM()
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(1, 1, 1, projection=request.crs)
ax.set_extent(extent, crs=ccrs.PlateCarree())   
ax.add_image(request, zoom)

cafe = [-105.2427, 40.01005]
ax.scatter(cafe[0], cafe[1], marker='+', s=250, color='red',
           linewidths=3, zorder=10,
           transform=ccrs.PlateCarree())

# Overlay GPS track
trackfile='../dat/joyride.idl'
track=io.readsav(trackfile)             # get lat/lon from IDL save file
ax.plot(track['lon'],track['lat'],transform=ccrs.PlateCarree(),c='g')
plt.show()