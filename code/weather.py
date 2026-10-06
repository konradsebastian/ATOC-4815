import datetime,pytz
import matplotlib.pyplot as plt
import numpy as np
import urllib.request
#import ssl 
#ssl._create_default_https_context = ssl._create_unverified_context

path = 'https://sundowner.colorado.edu/weather/atoc8/'

class WEATHER:
    def __init__(self,date,datatimezone='America/Denver',verbose=False):
        file = 'wxobs'+date+'.txt'       
        url = path+file
        if verbose: print('Reading: ',url)        
        jul    = [] # initialize julian day
        loc    = [] # initialize local times
        t2m    = [] # 2m temperatures
        wind   = [] # wind speed --> added
        dto    = [] # initialize datetime object

        try:
            # get julian day of requested date and timezone difference
            y0=int(date[0:4]); m0=int(date[4:6]); d0= int(date[6:8])
            d    = datetime.datetime(y0,m0,d0)
            utc  = pytz.UTC # UTC timezone definition
            mt   = pytz.timezone(datatimezone) # MT timezone definition
            tu   = utc.localize(d) # define time as UTC
            tm   = mt.localize(d)  # define same time as MT
            diff = (tm-tu).total_seconds()/3600. # calculate difference in h
            jday0= (datetime.datetime(y0,m0,d0)-datetime.datetime(y0,1,1)).total_seconds()/86400.0 + 1.0

            try:
                lines  = urllib.request.urlopen(url).readlines()
                for line in lines[3:]: # go through all lines, ignoring first three (header)
                    entries = line.decode("utf-8").split(" ")
                    columns = []       # will contain columns
                    for entry in entries:
                        if len(entry) > 1: columns.append(entry)
                    mmddyy= columns[0].zfill(8) # assigns date, filling in leading '0'
                    mo=int(mmddyy[0:2]); dd=int(mmddyy[3:5]); yyyy=int('20'+mmddyy[6:8])
                    # get julian day of acquired date
                    jday = (datetime.datetime(yyyy,mo,dd)-datetime.datetime(y0,1,1)).total_seconds()/86400.0 + 1.0
                    # get time and convert from am/pm format to military time
                    hhmmX = columns[1].zfill(6) # assigns time, filling in leading '0'
                    hh    = float(hhmmX[0:2])
                    if (hhmmX[5] == 'p') & (hh < 12): hh=hh+12.
                    if (hhmmX[5] == 'a') & (hh > 11): hh=hh-12.
                    mm    = float(hhmmX[3:5])
                    # The following if statement prevents reading of any data that belongs
                    # to a day different from the one requested. Some files do have data from
                    # other days.
                    if jday == jday0: 
                        loc.append(hh+mm/60.)
                        jul.append(jday)
                        t2m.append((float(columns[2])-32)*5./9.) # conversion from Fahrenheit into Celsius
                        wind.append(float(columns[7]))           # no conversion (keep in miles/h)
                        dto.append(datetime.datetime(yyyy,mo,dd,int(hh),int(mm))) 
                self.doy = jday0
                self.date= date
                self.frc=(np.array(loc)+diff)/24.+self.doy          # fractional Julian day; correction for local time
                self.loc=np.array(loc)
                self.t2m=np.array(t2m)
                self.wsp=np.array(wind)
                self.dto=dto
            except:
                print("File does not exist: "+file,flush=True)
                self.doy  = jday0
                self.date = date
                self.t2m  = [np.nan,np.nan,np.nan]
                self.frc  = [jday0,jday+0.5,jday0+1]
        except:
            if verbose: print("Requested date does not exist: "+date,flush=True)
    def plot(self):
        plt.figure()
        #plt.plot(self.frc,self.t2m)
        plt.plot(self.dto,self.t2m)
        plt.title(self.date+' mean temp='+str(round(np.mean(self.t2m),1))+'C')

def make_climate(start,end): # start,end; 1= January, 2=February, ...
    climate=[] # start with empty list
    for j in range(start-1,end): # 1,2 = February only
        mm=str(j+1).zfill(2)
        for i in range(31): # loop through days
            dd=str(i+1).zfill(2)
            weatherdata=WEATHER('2017'+mm+dd)
            if hasattr(weatherdata,'doy'):  # check whether object comes back filled with data or not
                climate.append(weatherdata) # append to list of days only if it does have data
    return(climate)
        
def plot_t2m(climate): 
    frcs=[] 
    t2ms=[]
    for weather in climate:
        frcs.append(weather.frc) # fractional days out
        t2ms.append(weather.t2m) # get temperature data out
    frcs=np.hstack(frcs)    # flatten dimensions into simple time series
    t2ms=np.hstack(t2ms)
    nodata=np.where(np.isnan(t2ms))
    plt.figure('temperatures')
    plt.plot(frcs,t2ms,'k.',label='T$_{2m}$')    
    if(len(nodata[0])>0):
        t2ms[nodata]=np.nanmin(t2ms)-1
        plt.plot(frcs[nodata],t2ms[nodata],'ro',label='no data')
    plt.xlabel('Fractional Julian Day of '+weather.date[0:4])
    plt.ylabel('Temperature [C]')
    plt.legend()
    plt.show()
    
if __name__=='__main__':
    # Included: basic plotting function
    weather = WEATHER('20180702') 
    weather.plot()
    
    # Class: Use "climate" function and "plot" function to plot January data
    # climate = ... [functions are already provided]
    #
    # Class: Based on "climate", make histograms of temperature data over that time frame
    # Can we write this as climate.make_histograms ?
    #
    # Class: Rewrite this code to convert the time axis with datetime
    #
    