from netCDF4 import Dataset as nc
import matplotlib.pyplot as plt
import numpy as np
from warnings import filterwarnings
filterwarnings(action='ignore', category=DeprecationWarning, message='`np.bool` is a deprecated alias')

# Read satellite data
file = '../dat/MET10.20170713.1200.03km.C01.nc'

handle = nc(file)
#print(handle.dimensions.keys())
#print(handle.variables)

lon  = handle.variables['Longitude'][...]*0.01
lat  = handle.variables['Latitude' ][...]*0.01
raw  = handle.variables['RAW'][...] #2D; lat first
handle.close()

# Process satellite data
nx,ny=raw.shape # lat,lon
wesn =[np.min(lon),np.max(lon),np.min(lat),np.max(lat)] # image range lon, lat
#raw=raw/np.max(raw) # normalize to 1
#grs=np.stack([raw,raw,raw],axis=2) # make gray scale
    
# overplot image
plt.figure(0)
#plt.imshow(grs,extent=wesn,alpha=1.)
plt.imshow(raw,extent=wesn,cmap='jet') 

#,extent=wesn,cmap='jet')
#plt.title(file)
plt.plot([-15,20],[-25,-25],'r--')

# extract data along line
idxlat =np.argmin(np.abs(lat-(-25)))
idxlonl=np.argmin(np.abs(lon-(-15)))
idxlonr=np.argmin(np.abs(lon-20))
plt.figure(1)
plt.plot(lon[idxlonl:idxlonr],raw[idxlat,idxlonl:idxlonr],'k.')
