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
    
    lon0=-105
    lat0=40
    indutc = np.argmin(np.abs(utc-utc0)) # find the requested time
    indlon = np.argmin(np.abs(lon-lon0))
    indlat = np.argmin(np.abs(lat-lat0))
    
    print(ts.shape,lon.shape,lat.shape)
    
    #frj    = frj[indutc]    
    t   = ts[:,indlat,indlon]-273.15        # extract time series in given location and convert K-->C

    return(frj,lat,lon,t) 
    
#if __name__=='__main__':
import matplotlib.pyplot as plt
date='20180702'
frj,lat,lon,t = read_merra(date)
plt.plot(t)
