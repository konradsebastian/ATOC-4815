import matplotlib.pyplot as plt
import numpy as np
import urllib.request
import datetime

url = 'http://skywatch.colorado.edu/data/spn/spn_17_08_21.dat'

# open URL to read
urlhandle = urllib.request.urlopen(url)

# read all lines into list of strings "lines"
lines = urlhandle.readlines()

# close the handle
urlhandle.close()

# lines came back as bytes, so convert each one to a string
lines = [line.decode("utf-8") for line in lines]

# Loop over the lines in the file
utc=[] # initialize list for times
dtl=[]
tti=[] # initialize list for radiation
for line in lines:
    entries = line.split(',')
    #print(entries);quit()
    if entries[0][0] != ';':
        hh = entries[0][0:2]
        mm = entries[0][3:5]
        ss = entries[0][6:8]
        utc.append(float(hh) + \
                   float(mm)/60. + \
                   float(ss)/3600.)
        tti.append(float(entries[1]))   
        #if int(hh)<7: dayoff=1
        dtl.append(datetime.datetime(2017,8,21,int(hh),int(mm),int(ss)))

# Append +24 hours if data was measured on next day
utc=np.array(utc)
next_day=np.where(utc < 7) # This is not quite clean, cut off at locat midnight
utc[next_day]=utc[next_day]+24.

# Now do the plotting
plt.close() # closes previous plot
fig=plt.figure(figsize=[6,6]) 
plt.plot(dtl,tti,'o',markersize=1,label='Radiation') 
plt.xlabel('LOC TIME',fontsize=14)
plt.ylabel('Irradiance [W m$^{-2}$]',fontsize=14) 
plt.title('Solar Eclipse',fontsize=18)
plt.legend(fontsize=14)
fig.savefig('../dat/eclipse.png',dpi=200)




