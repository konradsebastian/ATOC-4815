import numpy as np
import matplotlib.pyplot as plt
import h5py
import cartopy.crs as ccrs


def read_aviris_h5(directory,file):
    handle = h5py.File(directory+'/'+file+'_3ch.h5', 'r')
    lons = np.array(handle['longitude'][...])
    lats = np.array(handle['latitude'][...])
    img1 = np.array(handle['radiance'][...])
    return(lons,lats,img1)

# Specify the directory name and file header
directory_name = "../dat"
file           = "ang20240815t133303"
plot           = True

lons, lats, img1 = read_aviris_h5(directory_name, file)


if plot:
    fig = plt.figure()
    ax = plt.axes(projection=ccrs.NorthPolarStereo(central_longitude=-30))
    ax.pcolormesh(lons, lats, img1/np.nanmax(img1), transform=ccrs.PlateCarree())
    ax.coastlines()
    ax.gridlines(draw_labels=True)
    