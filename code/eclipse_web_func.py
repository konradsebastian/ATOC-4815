import matplotlib.pyplot as plt
import numpy as np
from function import download

url = 'http://skywatch.colorado.edu/data/spn/spn_17_08_21.dat'

utc,tti = download(url)

# Now do the plotting
plt.close() # closes previous plot
fig=plt.figure(figsize=[6,6]) 
plt.plot(utc,tti,'o',markersize=1,label='Radiation') 
plt.xlabel('UTC [h]',fontsize=14)
plt.ylabel('Irradiance [W m$^{-2}$]',fontsize=14) 
plt.title('Solar Eclipse',fontsize=18)
plt.legend(fontsize=14)
fig.savefig('../dat/eclipse.png',dpi=200)




