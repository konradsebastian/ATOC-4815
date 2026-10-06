from netCDF4 import Dataset as nc
import datetime
import numpy as np
from warnings import filterwarnings
filterwarnings(action='ignore', category=DeprecationWarning, message='`np.bool` is a deprecated alias')

def read_merra(date,utc0=12.):
    file = 'MERRA2_400.inst1_2d_asm_Nx.'+date+'.nc4'
    print(file)
    handle = nc('../dat/'+file)
    lat = handle.variables['lat'][...]      # 
    lon = handle.variables['lon'][...]      # 
    mts = handle.variables['time'][...]     # minutes since day start
    ts  = handle.variables['TS'][...]       # surface temp [time,nlat,nlon]
    
    handle.close()

    # get julian day (it is not necessary, just an extra in the solutions)
    y0=int(date[0:4]); m0=int(date[4:6]); d0= int(date[6:8])
    doy = (datetime.datetime(y0,m0,d0)-datetime.datetime(y0,1,1)).total_seconds()/86400.0 + 1.0
    # convert time to fractional julian day
    utc    = np.array(mts)/60.
    frj    = doy + utc/24.
    
    indutc = np.argmin(np.abs(utc-utc0)) # find the requested time
    frj    = frj[indutc]    
    t   = ts[indutc,:,:]-273.15        # extract time series in given location and convert K-->C

    return(frj,lat,lon,t) 
    
#if __name__=='__main__':
import matplotlib.pyplot as plt
date='20180702'
frj,lat,lon,t = read_merra(date, utc0=20.)
plt.contourf(lon,lat,t,30,cmap='jet',vmin=-40,vmax=40)
#plt.imshow(t,cmap='jet',vmin=-40,vmax=40,origin='lower')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('MERRA '+date+' '+str(round(frj,2)))
