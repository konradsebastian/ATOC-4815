# first, import text file in a faster way than we learned in week #1
import pandas as pd
file = '../dat/ARCSIX-MetNav_P3B_20240815_RA.ict'
df = pd.read_csv(file,sep=',', header=72, 
                 usecols=['Time_Start','Longitude','Latitude','GPS_Altitude','Ground_Speed']) # names=['name1','name2']; usecols=[0,2,3,4]
print('The following keys were imported:',df.keys())

# Now imprt matplotlib and cartopy
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# Set up coordinate system and draw costlines
ax = plt.axes(projection=ccrs.NorthPolarStereo(central_longitude=-30)) # NorthPolarStereo, PlateCarree, Mollweide
ax.coastlines(resolution='10m')

color=df['GPS_Altitude'] # GPS_Altitude or Time_Start
color=color/max(color)*255

# Put flight track on map
ax.scatter(df['Longitude'],df['Latitude'], s=5, c=color,cmap='jet',transform=ccrs.PlateCarree())

# define map extent
plot_extent=[-80,0,75,90]
ax.set_extent(plot_extent, crs=ccrs.PlateCarree())

# add grid lines
ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='gray', alpha=0.5, linestyle='--', zorder=10)

# add a point of interest
lat_k =  81.32498056
lon_k = -57.18576111
ax.scatter(lon_k,lat_k, s=300, marker = '+',color='red',transform=ccrs.PlateCarree())