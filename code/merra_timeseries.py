from netCDF4 import Dataset as nc
import datetime
from warnings import filterwarnings
import numpy as np
filterwarnings(action='ignore', category=DeprecationWarning, message='`np.bool` is a deprecated alias')


def read_merra(date,lon0=-105.24496,lat0 = 40.00999):
    file = 'MERRA2_400.inst1_2d_asm_Nx.'+date+'.nc4'
    handle = nc('../dat/'+file)
    lat = handle.variables['lat'][...]      # 
    lon = handle.variables['lon'][...]      # 
    mts = handle.variables['time'][...]     # minutes since day start
    ts  = handle.variables['T2M'][...]       # surface temp [time,nlat,nlon]
    
    handle.close()
        
    indlon = np.argmin(np.abs(lon-lon0))    # find longitude index
    indlat = np.argmin(np.abs(lat-lat0))    # find latitude  index
    nt,nlat,nlon=ts.shape                   # got dimensions from Panoply, now get time,lat,lon gridding
    t   = ts[:,indlat,indlon]-273.15        # extract time series in given location and convert K-->C

    # get julian day (it is not necessary, just an extra in the solutions)
    y0=int(date[0:4]); m0=int(date[4:6]); d0= int(date[6:8])
    doy = (datetime.datetime(y0,m0,d0)-datetime.datetime(y0,1,1)).total_seconds()/86400.0 + 1.0
    # convert time to fractional julian day
    frj = doy + np.array(mts)/60./24.

    return(frj,t) 
    
if __name__=='__main__':
    import matplotlib.pyplot as plt
    date='20180702'
    frj,t = read_merra(date,lon0=-105.24496,lat0 = 40.00999)
    plt.plot((frj-np.min(frj))*24.,t,'bo--',label='MERRA-2')
    plt.xlabel('UTC [h]');plt.ylabel('Temperature [C]'),plt.title(date)